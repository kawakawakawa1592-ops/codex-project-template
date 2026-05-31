# New Codex Project Checklist

Use this checklist whenever starting a new Codex GitHub repository.

## Repository Setup

- [ ] Create the new GitHub repository with `Use this template`.
- [ ] Confirm `.github/workflows/gpt-review.yml` exists.
- [ ] Confirm `.github/ISSUE_TEMPLATE/codex_project_task.yml` exists.
- [ ] Confirm `.github/pull_request_template.md` exists.
- [ ] Confirm `docs/new-project-checklist.md` exists.
- [ ] Confirm GitHub Actions are enabled for the repository.

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

## First Pull Request

- [ ] Create a small initial PR.
- [ ] Confirm the `GPT Review` workflow starts.
- [ ] Confirm `.github/workflows/gpt-review.yml` calls `kawakawakawa1592-ops/ai-review-workflows`.
- [ ] Confirm the PR receives a GPT review comment.
- [ ] Confirm the GPT review comment includes a teacher-facing summary.
- [ ] Confirm `REVIEW_STATUS` is shown in the workflow logs.
- [ ] Confirm `FINAL_REVIEW_STATUS` is shown in the workflow logs.
- [ ] Confirm the flow is `Codex -> PR -> GPT review -> teacher-facing summary`.
- [ ] Fix any setup problems before starting real feature work.
