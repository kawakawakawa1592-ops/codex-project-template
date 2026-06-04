#!/usr/bin/env python3
"""Hand off the next ready issue to Codex after a PR merge."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API_ROOT = "https://api.github.com"
READY_LABELS = [
    label.strip()
    for label in os.environ.get("CODEX_HANDOFF_READY_LABELS", "codex-ready,ready-for-codex").split(",")
    if label.strip()
]
ACTIVE_LABEL = os.environ.get("CODEX_HANDOFF_ACTIVE_LABEL", "codex-active").strip() or "codex-active"
BLOCK_LABELS = {
    label.strip()
    for label in os.environ.get("CODEX_HANDOFF_BLOCK_LABELS", "needs-human,blocked,hold,no-auto-merge,codex-active").split(",")
    if label.strip()
}
BLOCK_LABELS.add(ACTIVE_LABEL)
PRIORITY_LABEL = os.environ.get("CODEX_HANDOFF_PRIORITY_LABEL", "priority-high").strip() or "priority-high"
COMMENT_MARKER = "<!-- codex-next-issue-handoff -->"


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
            return response.status, json.loads(body) if body else {}, response.headers
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(body) if body else {}
        except json.JSONDecodeError:
            parsed = {"message": body}
        return exc.code, parsed, exc.headers


def next_link(headers) -> str | None:
    link_header = headers.get("Link", "")
    for part in link_header.split(","):
        section = part.strip()
        if 'rel="next"' not in section:
            continue
        if section.startswith("<") and ">" in section:
            return section[1 : section.index(">")]
    return None


def paged_json(url: str, token: str) -> list[dict]:
    results: list[dict] = []
    while url:
        status, payload, headers = request_json("GET", url, token)
        if status != 200:
            raise RuntimeError(f"GitHub list request failed: {payload.get('message', status)}")
        if not isinstance(payload, list):
            raise RuntimeError("GitHub list request returned an unexpected payload")
        results.extend(payload)
        url = next_link(headers)
    return results


def issue_labels(issue: dict) -> set[str]:
    return {label.get("name") for label in issue.get("labels", []) if label.get("name")}


def issue_is_ready(issue: dict) -> bool:
    labels = issue_labels(issue)
    return bool(labels.intersection(READY_LABELS)) and not labels.intersection(BLOCK_LABELS)


def list_issues_for_label(repo: str, token: str, label: str) -> list[dict]:
    query = urllib.parse.urlencode({"state": "open", "labels": label, "per_page": "100"})
    payload = paged_json(f"{API_ROOT}/repos/{repo}/issues?{query}", token)
    return [item for item in payload if "pull_request" not in item]


def has_handoff_comment(repo: str, token: str, issue_number: int) -> bool:
    comments = paged_json(f"{API_ROOT}/repos/{repo}/issues/{issue_number}/comments?per_page=100", token)
    return any(COMMENT_MARKER in (comment.get("body") or "") for comment in comments)


def find_next_issue(repo: str, token: str) -> dict | None:
    issues_by_number: dict[int, dict] = {}
    for label in READY_LABELS:
        for issue in list_issues_for_label(repo, token, label):
            if issue_is_ready(issue):
                issues_by_number[issue["number"]] = issue

    candidates = []
    for issue in issues_by_number.values():
        if not has_handoff_comment(repo, token, issue["number"]):
            candidates.append(issue)

    if not candidates:
        return None

    def sort_key(issue: dict):
        labels = issue_labels(issue)
        return (0 if PRIORITY_LABEL in labels else 1, issue.get("created_at") or "", issue["number"])

    return sorted(candidates, key=sort_key)[0]


def ensure_label(repo: str, token: str, name: str, color: str, description: str) -> None:
    encoded = urllib.parse.quote(name, safe="")
    status, payload, _ = request_json("GET", f"{API_ROOT}/repos/{repo}/labels/{encoded}", token)
    if status == 200:
        return
    if status != 404:
        raise RuntimeError(f"Could not inspect label {name}: {payload.get('message', status)}")
    status, payload, _ = request_json(
        "POST",
        f"{API_ROOT}/repos/{repo}/labels",
        token,
        {"name": name, "color": color, "description": description},
    )
    if status >= 300:
        raise RuntimeError(f"Could not create label {name}: {payload.get('message', status)}")


def add_labels(repo: str, token: str, issue_number: int, labels: list[str]) -> None:
    status, payload, _ = request_json(
        "POST",
        f"{API_ROOT}/repos/{repo}/issues/{issue_number}/labels",
        token,
        {"labels": labels},
    )
    if status >= 300:
        raise RuntimeError(f"Could not add labels to issue #{issue_number}: {payload.get('message', status)}")


def comment(repo: str, token: str, issue_number: int, body: str) -> None:
    status, payload, _ = request_json(
        "POST",
        f"{API_ROOT}/repos/{repo}/issues/{issue_number}/comments",
        token,
        {"body": body[:65000]},
    )
    if status >= 300:
        raise RuntimeError(f"Could not comment on issue #{issue_number}: {payload.get('message', status)}")


def handoff_body(issue: dict) -> str:
    return f"""{COMMENT_MARKER}
@codex please start work on this issue.

Context:
- This issue was selected automatically after a pull request was merged.
- Follow `PROJECT_VISION.md`, `PROJECT_MEMORY.md`, `README.md`, and `docs/codex-autopilot.md`.
- Keep the scope to this issue when possible.
- Open one PR for this issue when implementation is needed.
- GPT Review will run automatically on the PR.

Stop conditions:
- If the issue needs human judgment, add or keep `needs-human` and explain what is needed.
- If the issue is blocked, add or keep `blocked` and explain the blocker.
- Do not proceed outside the issue scope without asking.

Selected issue: #{issue['number']} - {issue.get('title', '')}
"""


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN", "")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    if not token or not repo:
        raise RuntimeError("GITHUB_TOKEN and GITHUB_REPOSITORY are required")
    if not READY_LABELS:
        raise RuntimeError("At least one ready label is required")

    issue = find_next_issue(repo, token)
    if not issue:
        print("No eligible codex-ready issue found for handoff.")
        return 0

    issue_number = issue["number"]
    ensure_label(repo, token, ACTIVE_LABEL, "0e8a16", "Codex has been asked to start this issue.")
    add_labels(repo, token, issue_number, [ACTIVE_LABEL])
    comment(repo, token, issue_number, handoff_body(issue))
    print(f"Handed off issue #{issue_number} to Codex.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
