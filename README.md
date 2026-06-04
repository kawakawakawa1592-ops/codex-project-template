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
v
Auto-merge when PASS and no stop condition exists
v
Next codex-ready issue is handed to @codex when available
```

## What This Template Provides

New repositories that use this template get:

- An automatic GPT Review workflow at `.github/workflows/gpt-review.yml`
- An automatic merge workflow at `.github/workflows/auto-merge-reviewed-pr.yml`
- A next-issue handoff workflow at `.github/workflows/codex-next-issue-handoff.yml`
- A repository-local review script at `scripts/project_gpt_review.py`
- A repository-local auto-merge script at `scripts/auto_merge_reviewed_pr.py`
- A repository-local handoff script at `scripts/codex_next_issue_handoff.py`
- A review prompt at `.github/prompts/project_review_prompt.md`
- `PROJECT_VISION.md` for project goals, users, and completion criteria
- `PROJECT_MEMORY.md` for decisions, constraints, review notes, and next actions
- An issue template for Codex tasks and the `codex-ready` queue
- A pull request template with GPT review and auto-merge checks
- A new project startup checklist at `docs/new-project-checklist.md`
- Autopilot loop guidance at `docs/codex-autopilot.md`
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

## Auto-Merge

Every new Codex project includes this workflow:

```text
.github/workflows/auto-merge-reviewed-pr.yml
```

It runs after `GPT Review` completes. It merges a PR only when all of these are true:

- `GPT Review` completed successfully.
- The completed GPT Review run is the trusted `pull_request_target` run.
- The `project-gpt-review` artifact contains `FINAL_REVIEW_STATUS: PASS`.
- The artifact does not contain `REVIEW_STATUS: NEEDS_REVISION`.
- The reviewed head SHA matches the current PR head SHA.
- The PR is open.
- The PR is not a draft.
- The PR is mergeable.
- The PR does not have a blocking label.

Default blocking labels:

```text
needs-human,blocked,no-auto-merge,hold
```

The merge method defaults to `merge`. You can override it with this repository variable:

```text
AUTO_MERGE_METHOD=merge / squash / rebase
```

You can override blocking labels with:

```text
AUTO_MERGE_BLOCK_LABELS=needs-human,blocked,no-auto-merge,hold
```

## Codex Next-Issue Handoff

Every new Codex project includes this workflow:

```text
.github/workflows/codex-next-issue-handoff.yml
```

It runs after a pull request is merged, and can also be run manually with `workflow_dispatch`. It selects the next issue and posts an `@codex` start comment so Codex Cloud can begin the next task.

The handoff workflow selects an issue only when all of these are true:

- The issue is open.
- The issue has `codex-ready` or `ready-for-codex`.
- The issue is not a pull request.
- The issue does not have `needs-human`, `blocked`, `hold`, `no-auto-merge`, or `codex-active`.
- The issue has not already received the handoff marker comment.

Selection order:

```text
priority-high first
then oldest eligible issue
```

When selected, the issue receives:

- `codex-active`
- an `@codex` comment with project-context, scope, PR, GPT Review, and stop-condition instructions

This automatic pickup requires a Codex Cloud environment for the repository. If no environment is configured, the connector may reply with setup instructions instead of starting work.

You can override handoff labels with these repository variables:

```text
CODEX_HANDOFF_READY_LABELS=codex-ready,ready-for-codex
CODEX_HANDOFF_BLOCK_LABELS=needs-human,blocked,hold,no-auto-merge,codex-active
CODEX_HANDOFF_ACTIVE_LABEL=codex-active
CODEX_HANDOFF_PRIORITY_LABEL=priority-high
```

## Codex Autopilot Loop

This template supports a queue-based project loop through GitHub issues.

Recommended flow:

```text
User describes the desired product
v
Codex writes PROJECT_VISION.md and PROJECT_MEMORY.md
v
Codex breaks the project into small issues
v
Ready issues receive codex-ready or ready-for-codex
v
User says 作成開始 or 次へ, or a merged PR triggers handoff
v
Codex chooses the next ready issue
v
Codex implements one issue and opens one PR
v
GPT Review audits the PR and provides Codex Advisory if needed
v
PASS triggers auto-merge unless a stop condition exists
v
Merged PR triggers @codex handoff to the next ready issue when available
```

Use `docs/codex-autopilot.md` for the full issue queue and stop-condition rules.

Important limitation: GitHub Actions can auto-merge passing PRs and post `@codex` handoff comments, but automatic Codex pickup requires a configured Codex Cloud environment for the repository. If automatic pickup does not occur, the user can still say `次へ` and Codex should continue from the next ready issue or the handoff comment.

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
v
.github/workflows/auto-merge-reviewed-pr.yml
v
Auto-merge when PASS and no stop condition exists
v
.github/workflows/codex-next-issue-handoff.yml
v
@codex handoff to the next ready issue when one exists
```

This path is guaranteed by the committed template files when these repository settings are present:

- GitHub Actions is enabled.
- `OPENAI_API_KEY` exists as an Actions secret.
- `PRIMARY_REVIEW_MODEL` exists as an Actions variable with value `gpt-4.1-mini`, or the default is accepted.
- `FINAL_REVIEW_MODEL` exists as an Actions variable with value `gpt-5.5`, or the default is accepted.
- A Codex Cloud environment exists for repositories that should auto-start Codex from `@codex` handoff comments.
- The pull request event is one of `opened`, `synchronize`, `reopened`, or `ready_for_review`.

Codex does not need to ask GPT Review to run. The first test PR should confirm that the workflow starts automatically and posts a GPT review comment containing a teacher-facing summary and Codex Advisory.

## Initial Setup For A New Repository

1. Open this repository on GitHub.
2. Click `Use this template`.
3. Create the new Codex project repository.
4. Register the `OPENAI_API_KEY` secret.
5. Register the GitHub Variables.
6. Create a Codex Cloud environment if `@codex` handoff should start Codex automatically.
7. Fill in `PROJECT_VISION.md`.
8. Update `PROJECT_MEMORY.md` as decisions are made.
9. Plan small ready issues.
10. Open a small test PR.
11. Confirm the `GPT Review` workflow starts automatically.
12. Confirm the PR receives a GPT review comment with a teacher-facing summary and Codex Advisory.
13. Confirm a PASS PR auto-merges when no stop condition exists.
14. Confirm a merged PR hands off the next ready issue with an `@codex` comment.

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
AUTO_MERGE_METHOD=merge
AUTO_MERGE_BLOCK_LABELS=needs-human,blocked,no-auto-merge,hold
CODEX_HANDOFF_READY_LABELS=codex-ready,ready-for-codex
CODEX_HANDOFF_BLOCK_LABELS=needs-human,blocked,hold,no-auto-merge,codex-active
CODEX_HANDOFF_ACTIVE_LABEL=codex-active
CODEX_HANDOFF_PRIORITY_LABEL=priority-high
```

## Codex Cloud Environment Setup

Create a Codex Cloud environment for each repository where `@codex` handoff comments should start Codex automatically.

1. Open [Codex environments](https://chatgpt.com/codex/cloud/settings/environments).
2. Create a new environment for the target repository.
3. Use the `universal` container image unless the project needs a custom image.
4. Leave setup script on automatic unless the project needs custom dependencies.
5. Leave agent internet access disabled unless the project requires internet during the agent phase.
6. Save the environment.
7. Test with an issue comment such as `@codex please confirm you can run from this issue`.

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

The primary review returns `REVIEW_STATUS: NEEDS_REVISION` when the diff appears to contain a likely bug, missing requirement, security risk, broken workflow, weakened automatic review behavior, unsafe auto-merge behavior, unsafe handoff behavior, vague Codex Advisory, or important test gap. Otherwise it returns `REVIEW_STATUS: PASS`.

The final review checks the primary result and the PR diff again. It returns `FINAL_REVIEW_STATUS: PASS` only when the pull request appears mergeable from the available diff, `FINAL_REVIEW_STATUS: WARN` when only non-blocking human follow-up remains, and `FINAL_REVIEW_STATUS: FAIL` when blocking issues remain.

When `FINAL_REVIEW_STATUS: FAIL` or `REVIEW_STATUS: NEEDS_REVISION` appears in the review, the workflow fails so the PR cannot be treated as passing review accidentally.
