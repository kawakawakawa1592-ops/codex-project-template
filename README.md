# Codex Project Template

This repository is the starter template for Codex development projects.

Use `Use this template` when creating new repositories such as `medical-paper-app`, `radio-app`, `discussion-generator`, or any future Codex project. New projects should not need to rebuild the GPT review system from scratch.

Every pull request automatically runs GPT Review through GitHub Actions. Codex does not need to request the review manually, and the user does not need to add a special instruction for each PR.

```text
Codex
v
PR opened or updated
v
GitHub Actions GPT Review
v
GPT-4.1-mini primary review
v
GPT-5.5 final review
v
Teacher-facing summary and Codex Advisory
v
PASS / WARN / FAIL
```

## What This Template Provides

New repositories that use this template get:

- An automatic GPT Review workflow at `.github/workflows/gpt-review.yml`
- A repository-local review script at `scripts/project_gpt_review.py`
- A review prompt at `.github/prompts/project_review_prompt.md`
- `PROJECT_VISION.md` for project goals, users, and completion criteria
- `PROJECT_MEMORY.md` for decisions, constraints, review notes, and next actions
- An issue template for Codex tasks
- A pull request template with GPT review checks
- A new project startup checklist at `docs/new-project-checklist.md`
- Documentation for OpenAI API key, GitHub Variables, and GitHub Secrets setup

## Project Context Files

Each project created from this template includes two context files for Codex and GPT Review.

### PROJECT_VISION.md

Use this file to record the product owner's intent:

- project purpose
- target users
- product goals
- out-of-scope items
- definition of done

### PROJECT_MEMORY.md

Use this file to record what changed during the project:

- decisions and reasons
- technical, design, and operation constraints
- GPT Review notes
- Codex fixes
- next actions

Automatic GPT Review can use these files together with the issue, PR, README, workflow, prompt, and diff to judge whether the result matches the creator's intent.

## Automatic GPT Review Workflow

Every new Codex project includes this workflow:

```text
.github/workflows/gpt-review.yml
```

It runs on every pull request creation or update event:

```yaml
on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]
  pull_request_target:
    types: [opened, synchronize, reopened, ready_for_review]
```

The workflow intentionally has no `paths` restriction. Template-only, workflow-only, script-only, prompt-only, README-only, generated-file, manuscript, and reference changes are all eligible for automated review.

For secret safety, the workflow uses two jobs:

- `review-script-safety-check` runs on `pull_request` with no OpenAI secret. It checks only review-script syntax from the PR.
- `project-gpt-review` runs on `pull_request_target`. It uses trusted base-branch review code and treats the PR checkout only as review content.

The GPT review job checks out two copies:

- `trusted`: the base commit, used to run trusted review code.
- `pr`: the pull request head commit, used only as review content.

The OpenAI API key is scoped only to the trusted review step, and that step runs:

```text
python trusted/scripts/project_gpt_review.py
```

The script reviews files under the PR checkout and gathers changed files plus important repository context, including workflow files, scripts, prompts, README files, docs, templates, project_rules, manuscripts, references, and other reviewable changed files.

## Codex Advisory

GPT Review is not only a PASS / FAIL gate. It also acts as an advisor for Codex running inside GitHub.

Every review includes a `Codex Advisory` section. When a PR needs revision, the advisory explains:

- what is wrong
- why it matters
- the recommended repair approach
- which files Codex should edit
- the acceptance criteria for the next fix

This lets GitHub-internal Codex read the PR review comment and repair the PR without the user rewriting the instruction manually.

A failing review should include guidance like this:

```text
Codex Advisory:
- Problem: README documents the feature, but docs/new-project-checklist.md does not include the required setup step.
- Why it matters: New repositories may omit the setup and the automation will be incomplete.
- Recommended fix: Add a checklist item under Automatic GPT Review.
- Files to edit: docs/new-project-checklist.md
- Acceptance criteria: The checklist names the required setup step and the review output returns PASS.
- Optional follow-up: None.
```

The `Codex Fix Instructions` section then gives Codex a short ordered repair list.

## PR Type Detection

`project_gpt_review.py` automatically classifies PRs into one of these modes:

- `TEMPLATE_OR_WORKFLOW_PR`
- `MANUSCRIPT_SETUP_OR_GENERATED_FILES_PR`
- `MANUSCRIPT_SUBMISSION_PR`

PR type detection is based on changed files. Repository context is still included for review evidence, but unchanged context files do not change the detected PR mode.

A PR without `submission/` is not skipped. If it changes template, workflow, prompt, script, README, docs, project_rules, templates, manuscripts, or references, GPT Review audits the actual work under the appropriate mode.

## Use This Template Guarantee

Projects created from this template are wired for the full automatic review path:

```text
Codex change
v
Pull request
v
.github/workflows/gpt-review.yml
v
trusted scripts/project_gpt_review.py
v
Primary GPT review
v
Final GPT review
v
Teacher-facing PR summary and Codex Advisory
```

This path is guaranteed by the committed template files when these repository settings are present:

- GitHub Actions is enabled.
- `OPENAI_API_KEY` exists as an Actions secret.
- `PRIMARY_REVIEW_MODEL` exists as an Actions variable with value `gpt-4.1-mini`, or the default is accepted.
- `FINAL_REVIEW_MODEL` exists as an Actions variable with value `gpt-5.5`, or the default is accepted.
- The pull request event is one of `opened`, `synchronize`, `reopened`, or `ready_for_review`.

Codex does not need to ask GPT Review to run. The first test PR should confirm that the workflow starts automatically and posts a GPT review comment containing a teacher-facing summary and Codex Advisory.

## Initial Setup For A New Repository

1. Open this repository on GitHub.
2. Click `Use this template`.
3. Create the new Codex project repository.
4. Register the `OPENAI_API_KEY` secret.
5. Register the GitHub Variables.
6. Fill in `PROJECT_VISION.md`.
7. Update `PROJECT_MEMORY.md` as decisions are made.
8. Open a small test PR.
9. Confirm the `GPT Review` workflow starts automatically.
10. Confirm the PR receives a GPT review comment with a teacher-facing summary and Codex Advisory.

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

## PASS / WARN / FAIL Policy

The primary review returns `REVIEW_STATUS: NEEDS_REVISION` when the diff appears to contain a likely bug, missing requirement, security risk, broken workflow, weakened automatic review behavior, vague Codex Advisory, or important test gap. Otherwise it returns `REVIEW_STATUS: PASS`.

The final review checks the primary result and the PR diff again. It returns `FINAL_REVIEW_STATUS: PASS` only when the pull request appears mergeable from the available diff, `FINAL_REVIEW_STATUS: WARN` when only non-blocking human follow-up remains, and `FINAL_REVIEW_STATUS: FAIL` when blocking issues remain.

When `FINAL_REVIEW_STATUS: FAIL` or `REVIEW_STATUS: NEEDS_REVISION` appears in the review, the workflow fails so the PR cannot be treated as passing review accidentally.
