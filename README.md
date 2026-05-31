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
- Documentation for the required OpenAI API key and optional model overrides

The caller workflow uses the shared reusable workflow from:

```text
kawakawakawa1592-ops/ai-review-workflows/.github/workflows/reusable-gpt-review.yml@main
```

## Template GPT Review Workflow

Every new Codex project includes this caller workflow:

```text
.github/workflows/gpt-review.yml
```

It calls the central reusable workflow and passes only the required secret:

```yaml
jobs:
  gpt-review:
    uses: kawakawakawa1592-ops/ai-review-workflows/.github/workflows/reusable-gpt-review.yml@main
    secrets:
      OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

Model defaults are provided by the reusable workflow:

```text
PRIMARY_REVIEW_MODEL=gpt-4.1-mini
FINAL_REVIEW_MODEL=gpt-5.5
```

## Use This Template Flow

```text
Use this template
v
Create repository
v
Register OPENAI_API_KEY
v
Start Codex
```

## Required Setting

Register this Actions secret in each new repository:

```text
OPENAI_API_KEY=sk-...
```

Use the OpenAI API key for the account that should pay for review usage. Do not commit the key to the repository, do not put it in README files, and do not paste it into issues or pull requests.

## Optional Settings

These Actions variables are optional. Add them only when you want to override the default models:

```text
PRIMARY_REVIEW_MODEL=gpt-4.1-mini
FINAL_REVIEW_MODEL=gpt-5.5
```

If these variables are not configured, the reusable workflow automatically uses `gpt-4.1-mini` for the primary review and `gpt-5.5` for the final review.

## Initial Setup For A New Repository

1. Click `Use this template`.
2. Create the new repository.
3. Register the `OPENAI_API_KEY` Actions secret.
4. Start Codex.

The first test PR should confirm that the `GPT Review` workflow runs and posts a teacher-facing summary.

## PASS / FAIL Policy

The primary review returns `REVIEW_STATUS=FAIL` when the diff appears to contain a likely bug, missing requirement, security risk, broken workflow, or important test gap. Otherwise it returns `REVIEW_STATUS=PASS`.

The final review checks the primary result and the PR diff again. It returns `FINAL_REVIEW_STATUS=PASS` only when the pull request appears mergeable from the available diff.

When `FINAL_REVIEW_STATUS=FAIL`, the workflow fails so the PR cannot be treated as passing review accidentally.
