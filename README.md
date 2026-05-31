# Codex Project Template

This repository is the starter template for Codex development projects.

Use `Use this template` when creating new repositories such as `medical-paper-app`, `radio-app`, `discussion-generator`, or any future Codex project. New projects should not need to rebuild the GPT review system from scratch.

Every pull request can run this common review flow:

```text
Codex
v
PR
v
GPT-4.1-mini
v
GPT-5.5
v
Teacher-facing summary
v
PASS / FAIL
```

## What This Template Provides

New repositories that use this template get:

- A caller workflow at `.github/workflows/gpt-review.yml`
- An issue template for Codex tasks
- A pull request template with GPT review checks
- A new project startup checklist at `docs/new-project-checklist.md`
- Documentation for OpenAI API key, GitHub Variables, and GitHub Secrets setup

The caller workflow uses the shared reusable workflow from:

```text
kawakawakawa1592-ops/ai-review-workflows/.github/workflows/reusable-gpt-review.yml@main
```

## Template GPT Review Workflow

Every new Codex project includes this caller workflow:

```text
.github/workflows/gpt-review.yml
```

It calls the central reusable workflow:

```yaml
jobs:
  gpt-review:
    uses: kawakawakawa1592-ops/ai-review-workflows/.github/workflows/reusable-gpt-review.yml@main
```

The workflow pins the default model configuration:

```text
PRIMARY_REVIEW_MODEL=gpt-4.1-mini
FINAL_REVIEW_MODEL=gpt-5.5
```

## Use This Template Guarantee

Projects created from this template are wired for the full review path:

```text
Codex change
v
Pull request
v
.github/workflows/gpt-review.yml
v
kawakawakawa1592-ops/ai-review-workflows reusable workflow
v
Primary GPT review
v
Final GPT review
v
Teacher-facing PR summary
```

This path is guaranteed by the committed template files when these repository settings are present:

- GitHub Actions is enabled.
- `OPENAI_API_KEY` exists as an Actions secret.
- `PRIMARY_REVIEW_MODEL` exists as an Actions variable with value `gpt-4.1-mini`, or the default is accepted.
- `FINAL_REVIEW_MODEL` exists as an Actions variable with value `gpt-5.5`, or the default is accepted.
- The pull request event is one of `opened`, `synchronize`, `reopened`, or `ready_for_review`.

The first test PR should confirm that the workflow posts a GPT review comment containing a teacher-facing summary.

## Initial Setup For A New Repository

1. Open this repository on GitHub.
2. Click `Use this template`.
3. Create the new Codex project repository.
4. Register the `OPENAI_API_KEY` secret.
5. Register the GitHub Variables.
6. Open a small test PR.
7. Confirm the `GPT Review` workflow runs.
8. Confirm the PR receives a GPT review comment with a teacher-facing summary.

## GitHub Variables Setup

Configure variables in each repository created from this template.

1. Open the target repository on GitHub.
2. Open `Settings`.
3. Open `Secrets and variables`.
4. Open `Actions`.
5. Select the `Variables` tab.
6. Click `New repository variable`.
7. Add these values:

```text
PRIMARY_REVIEW_MODEL=gpt-4.1-mini
FINAL_REVIEW_MODEL=gpt-5.5
```

## GitHub Secrets Setup

Configure the OpenAI API key in each repository created from this template.

1. Open the target repository on GitHub.
2. Open `Settings`.
3. Open `Secrets and variables`.
4. Open `Actions`.
5. Select the `Secrets` tab.
6. Click `New repository secret`.
7. Add this secret:

```text
OPENAI_API_KEY=sk-...
```

GitHub masks secret values in Actions logs.

## OPENAI_API_KEY Registration

The required secret name is:

```text
OPENAI_API_KEY
```

Use the OpenAI API key for the account that should pay for review usage. Do not commit the key to the repository, do not put it in README files, and do not paste it into issues or pull requests.

## PASS / FAIL Policy

The primary review returns `REVIEW_STATUS=FAIL` when the diff appears to contain a likely bug, missing requirement, security risk, broken workflow, or important test gap. Otherwise it returns `REVIEW_STATUS=PASS`.

The final review checks the primary result and the PR diff again. It returns `FINAL_REVIEW_STATUS=PASS` only when the pull request appears mergeable from the available diff.

When `FINAL_REVIEW_STATUS=FAIL`, the workflow fails so the PR cannot be treated as passing review accidentally.
