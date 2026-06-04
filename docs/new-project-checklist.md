# New Codex Project Checklist

Use this checklist whenever starting a new Codex GitHub repository.

## Repository Setup

- [ ] Create the new GitHub repository with `Use this template`.
- [ ] Confirm `.github/workflows/gpt-review.yml` exists.
- [ ] Confirm `.github/workflows/auto-merge-reviewed-pr.yml` exists.
- [ ] Confirm `.github/prompts/project_review_prompt.md` exists.
- [ ] Confirm `scripts/project_gpt_review.py` exists.
- [ ] Confirm `scripts/auto_merge_reviewed_pr.py` exists.
- [ ] Confirm `PROJECT_VISION.md` exists.
- [ ] Confirm `PROJECT_MEMORY.md` exists.
- [ ] Confirm `.github/ISSUE_TEMPLATE/codex_project_task.yml` exists.
- [ ] Confirm `.github/pull_request_template.md` exists.
- [ ] Confirm `docs/new-project-checklist.md` exists.
- [ ] Confirm `docs/codex-autopilot.md` exists.
- [ ] Confirm GitHub Actions are enabled for the repository.

## Project Context Files

- [ ] Fill in `PROJECT_VISION.md` with the project purpose, target users, product goals, out-of-scope items, and definition of done.
- [ ] Update `PROJECT_MEMORY.md` with important decisions, constraints, review notes, Codex fixes, and next actions.
- [ ] Keep both files current so Codex and automatic GPT Review can evaluate work against the creator's intent.

## GitHub Secrets

- [ ] Open the repository on GitHub.
- [ ] Go to `Settings`.
- [ ] Go to `Secrets and variables`.
- [ ] Go to `Actions`.
- [ ] Open the `Secrets` tab.
- [ ] Add `OPENAI_API_KEY`.

## GitHub Variables

- [ ] Open the repository on GitHub.
- [ ] Go to `Settings`.
- [ ] Go to `Secrets and variables`.
- [ ] Go to `Actions`.
- [ ] Open the `Variables` tab.
- [ ] Add `PRIMARY_REVIEW_MODEL` with value `gpt-4.1-mini`.
- [ ] Add `FINAL_REVIEW_MODEL` with value `gpt-5.5`.
- [ ] Optionally add `AUTO_MERGE_METHOD` with value `merge`, `squash`, or `rebase`.
- [ ] Optionally add `AUTO_MERGE_BLOCK_LABELS` with value `needs-human,blocked,no-auto-merge,hold`.

## Automatic GPT Review

- [ ] Confirm the workflow runs on pull request `opened`, `synchronize`, `reopened`, and `ready_for_review` events.
- [ ] Confirm the workflow uses both `pull_request` and `pull_request_target` with no `paths` restriction.
- [ ] Confirm the `pull_request` job performs only no-secret syntax validation.
- [ ] Confirm the `pull_request_target` job checks out trusted base code separately from PR content.
- [ ] Confirm OpenAI secrets are scoped only to the trusted review step.
- [ ] Confirm Codex does not need to request GPT Review manually.
- [ ] Confirm `scripts/project_gpt_review.py` detects PR mode from changed files.
- [ ] Confirm PRs without `submission/` are still reviewed as template/workflow/setup PRs when appropriate.
- [ ] Confirm workflow, script, prompt, README, docs, templates, project_rules, manuscripts, and references can be included in review context when present.

## Codex Advisory

- [ ] Confirm GPT Review comments include a `Codex Advisory` section.
- [ ] Confirm failed reviews explain the problem, why it matters, recommended fix, files to edit, and acceptance criteria.
- [ ] Confirm `Codex Fix Instructions` are specific enough for GitHub-internal Codex to implement without the user rewriting the instruction.
- [ ] Confirm passing reviews say no required Codex repair is needed and separate optional follow-up from required fixes.

## Auto-Merge

- [ ] Confirm `.github/workflows/auto-merge-reviewed-pr.yml` runs after `GPT Review` completes.
- [ ] Confirm auto-merge requires `FINAL_REVIEW_STATUS: PASS` in the review artifact.
- [ ] Confirm auto-merge refuses artifacts containing `REVIEW_STATUS: NEEDS_REVISION` or `FINAL_REVIEW_STATUS: FAIL`.
- [ ] Confirm auto-merge skips draft PRs.
- [ ] Confirm auto-merge skips unmergeable PRs.
- [ ] Confirm auto-merge skips PRs with `needs-human`, `blocked`, `no-auto-merge`, or `hold`.

## Codex Autopilot

- [ ] Create small issues for each implementation step.
- [ ] Label ready issues with `codex-ready`.
- [ ] Label high-priority ready issues with `priority-high`.
- [ ] Use `needs-human`, `blocked`, or `hold` when Codex should stop.
- [ ] Keep each `codex-ready` issue narrow enough for one PR when possible.
- [ ] Confirm Codex reads `PROJECT_VISION.md`, `PROJECT_MEMORY.md`, and open issues before choosing the next step.
- [ ] Confirm the repository has a Codex trigger integration if Codex should start automatically after merge. Otherwise, the user can say `次へ`.

## First Pull Request

- [ ] Create a small initial PR.
- [ ] Confirm the `GPT Review` workflow starts automatically.
- [ ] Confirm the PR receives a GPT review comment.
- [ ] Confirm the GPT review comment includes a teacher-facing summary.
- [ ] Confirm the GPT review comment includes a Codex Advisory.
- [ ] Confirm `REVIEW_STATUS` is shown in the workflow logs.
- [ ] Confirm `FINAL_REVIEW_STATUS` is shown in the workflow logs.
- [ ] Confirm the flow is `Codex -> PR -> automatic GPT review -> teacher-facing summary -> Codex Advisory`.
- [ ] Confirm a PASS PR auto-merges when no stop condition exists.
- [ ] Fix any setup problems before starting real feature work.
