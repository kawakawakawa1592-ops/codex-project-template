# New Codex Project Checklist

Use this checklist whenever starting a new Codex GitHub repository.

## Repository Setup

- [ ] Create the new GitHub repository with `Use this template`.
- [ ] Confirm `.github/workflows/gpt-review.yml` exists.
- [ ] Confirm `.github/prompts/project_review_prompt.md` exists.
- [ ] Confirm `scripts/project_gpt_review.py` exists.
- [ ] Confirm `PROJECT_VISION.md` exists.
- [ ] Confirm `PROJECT_MEMORY.md` exists.
- [ ] Confirm `.github/ISSUE_TEMPLATE/codex_project_task.yml` exists.
- [ ] Confirm `.github/pull_request_template.md` exists.
- [ ] Confirm `docs/new-project-checklist.md` exists.
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

## First Pull Request

- [ ] Create a small initial PR.
- [ ] Confirm the `GPT Review` workflow starts automatically.
- [ ] Confirm the PR receives a GPT review comment.
- [ ] Confirm the GPT review comment includes a teacher-facing summary.
- [ ] Confirm `REVIEW_STATUS` is shown in the workflow logs.
- [ ] Confirm `FINAL_REVIEW_STATUS` is shown in the workflow logs.
- [ ] Confirm the flow is `Codex -> PR -> automatic GPT review -> teacher-facing summary`.
- [ ] Fix any setup problems before starting real feature work.
