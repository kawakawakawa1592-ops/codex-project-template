#!/usr/bin/env python3
"""Merge a PR only after GPT Review has passed with FINAL_REVIEW_STATUS: PASS."""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from io import BytesIO
from pathlib import Path

API_ROOT = "https://api.github.com"
BLOCK_LABELS = {
    label.strip()
    for label in os.environ.get("AUTO_MERGE_BLOCK_LABELS", "needs-human,blocked,no-auto-merge,hold").split(",")
    if label.strip()
}


def request_json(method: str, url: str, token: str, payload: dict | None = None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read().decode("utf-8")
            return response.status, json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(body) if body else {}
        except json.JSONDecodeError:
            parsed = {"message": body}
        return exc.code, parsed


def request_bytes(url: str, token: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def load_event() -> dict:
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        raise RuntimeError("GITHUB_EVENT_PATH is not set")
    return json.loads(Path(event_path).read_text(encoding="utf-8"))


def get_pull_request(repo: str, run: dict, token: str) -> dict | None:
    prs = run.get("pull_requests") or []
    if prs:
        number = prs[0].get("number")
        if number:
            status, payload = request_json("GET", f"{API_ROOT}/repos/{repo}/pulls/{number}", token)
            if status == 200:
                return payload

    head_branch = run.get("head_branch")
    owner = run.get("head_repository", {}).get("owner", {}).get("login") or repo.split("/", 1)[0]
    if not head_branch:
        return None
    query = urllib.parse.urlencode({"state": "open", "head": f"{owner}:{head_branch}"})
    status, payload = request_json("GET", f"{API_ROOT}/repos/{repo}/pulls?{query}", token)
    if status == 200 and isinstance(payload, list) and payload:
        return payload[0]
    return None


def review_artifact_text(repo: str, run_id: int, token: str) -> str | None:
    status, payload = request_json("GET", f"{API_ROOT}/repos/{repo}/actions/runs/{run_id}/artifacts", token)
    if status != 200:
        raise RuntimeError(f"Could not list artifacts for run {run_id}: {payload.get('message', status)}")
    artifacts = payload.get("artifacts", [])
    artifact = next((item for item in artifacts if item.get("name") == "project-gpt-review" and not item.get("expired")), None)
    if not artifact:
        return None

    archive = request_bytes(artifact["archive_download_url"], token)
    with zipfile.ZipFile(BytesIO(archive)) as zipped:
        for name in zipped.namelist():
            if name.endswith("project_gpt_review.md"):
                return zipped.read(name).decode("utf-8", errors="replace")
    return None


def has_passing_review(review: str) -> bool:
    return (
        "FINAL_REVIEW_STATUS: PASS" in review
        and "REVIEW_STATUS: NEEDS_REVISION" not in review
        and "FINAL_REVIEW_STATUS: FAIL" not in review
    )


def fresh_pr(repo: str, number: int, token: str) -> dict:
    status, payload = request_json("GET", f"{API_ROOT}/repos/{repo}/pulls/{number}", token)
    if status != 200:
        raise RuntimeError(f"Could not fetch PR #{number}: {payload.get('message', status)}")
    return payload


def wait_for_mergeable(repo: str, number: int, token: str) -> dict:
    for _ in range(8):
        pr = fresh_pr(repo, number, token)
        if pr.get("mergeable") is not None:
            return pr
        time.sleep(5)
    return fresh_pr(repo, number, token)


def stop_reason(pr: dict) -> str | None:
    if pr.get("draft"):
        return "PR is draft"
    if pr.get("state") != "open":
        return "PR is not open"
    labels = {label.get("name") for label in pr.get("labels", []) if label.get("name")}
    blocked = sorted(labels.intersection(BLOCK_LABELS))
    if blocked:
        return f"PR has blocking label(s): {', '.join(blocked)}"
    if pr.get("mergeable") is not True:
        return "PR is not mergeable"
    if pr.get("mergeable_state") not in {"clean", "has_hooks"}:
        return f"PR mergeable_state is {pr.get('mergeable_state')}"
    return None


def comment(repo: str, issue_number: int, token: str, body: str) -> None:
    request_json("POST", f"{API_ROOT}/repos/{repo}/issues/{issue_number}/comments", token, {"body": body[:65000]})


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN", "")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    if not token or not repo:
        raise RuntimeError("GITHUB_TOKEN and GITHUB_REPOSITORY are required")

    event = load_event()
    run = event.get("workflow_run", {})
    if run.get("name") != "GPT Review" or run.get("conclusion") != "success":
        print("Skipping because the completed workflow run is not a successful GPT Review run.")
        return 0

    review = review_artifact_text(repo, run["id"], token)
    if not review:
        print("Skipping because this GPT Review run has no project-gpt-review artifact.")
        return 0
    if not has_passing_review(review):
        print("Skipping because the GPT Review artifact does not contain a clean FINAL_REVIEW_STATUS: PASS.")
        return 0

    pr = get_pull_request(repo, run, token)
    if not pr:
        print("Skipping because no open PR was found for the workflow run.")
        return 0

    pr_number = pr["number"]
    pr = wait_for_mergeable(repo, pr_number, token)
    reason = stop_reason(pr)
    if reason:
        print(f"Skipping auto-merge for PR #{pr_number}: {reason}")
        comment(repo, pr_number, token, f"## Auto Merge Skipped\n\n{reason}\n\nGPT Review passed, but this PR still needs human/Codex attention before merge.")
        return 0

    method = os.environ.get("AUTO_MERGE_METHOD", "merge").strip() or "merge"
    head_sha = pr.get("head", {}).get("sha")
    status, payload = request_json(
        "PUT",
        f"{API_ROOT}/repos/{repo}/pulls/{pr_number}/merge",
        token,
        {
            "commit_title": f"Auto-merge PR #{pr_number}: {pr.get('title', '')}",
            "commit_message": "Merged automatically after GPT Review returned FINAL_REVIEW_STATUS: PASS.",
            "sha": head_sha,
            "merge_method": method,
        },
    )
    if status >= 300 or not payload.get("merged"):
        raise RuntimeError(f"Auto-merge failed for PR #{pr_number}: {payload.get('message', status)}")

    print(f"Auto-merged PR #{pr_number}: {payload.get('sha')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
