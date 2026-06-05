# Codex Project Template

This repository is a starter template for Codex development projects. Use `Use this template` when creating a new repository so each project starts with automatic GPT Review, guarded auto-merge, and Codex issue-queue handoff already wired in.

Codex does not need to ask GPT Review to run. Every pull request is reviewed automatically by GitHub Actions.

```text
Codex opens or updates a PR
v
GitHub Actions GPT Review runs automatically
v
Primary GPT review and final GPT review run
v
PASS / WARN / FAIL is posted with Codex Advisory
v
PASS can auto-merge when no stop condition exists
v
Merged PR can hand off the next ready issue to @codex
```

## What This Template Provides

- `.github/workflows/gpt-review.yml`: automatic GPT Review for all PR creation/update/reopen/ready-for-review events.
- `.github/workflows/auto-merge-reviewed-pr.yml`: auto-merge after a trusted GPT Review PASS.
- `.github/workflows/codex-next-issue-handoff.yml`: post-merge handoff to the next ready issue.
- `scripts/project_gpt_review.py`: trusted review runner.
- `scripts/auto_merge_reviewed_pr.py`: guarded merge runner.
- `scripts/codex_next_issue_handoff.py`: ready-issue selector and Codex handoff runner.
- `.github/prompts/project_review_prompt.md`: review and Codex Advisory prompt.
- `PROJECT_VISION.md`: project goals, users, scope, and definition of done.
- `PROJECT_MEMORY.md`: decisions, constraints, review notes, and next actions.
- `docs/codex-autopilot.md`: issue queue and stop-condition rules.
- `docs/new-project-checklist.md`: setup checklist for repositories created from this template.

## Required Secrets

Configure these repository secrets under `Settings` -> `Secrets and variables` -> `Actions` -> `Secrets`.

```text
OPENAI_API_KEY=sk-...
CODEX_TRIGGER_TOKEN=github_pat_...
```

`OPENAI_API_KEY` is used only by the trusted `pull_request_target` GPT Review job.

`CODEX_TRIGGER_TOKEN` is used only when a ready issue is selected for Codex handoff. It must be a fine-grained GitHub token for an account that can comment on issues in the repository. Give it repository access and at least Issues read/write permission. The default Actions `GITHUB_TOKEN` posts comments as `github-actions[bot]`; those bot-authored `@codex` mentions may not start Codex Cloud, so the handoff workflow fails clearly when a ready issue exists but `CODEX_TRIGGER_TOKEN` is missing.

Do not commit secrets to the repository, README files, issues, or pull requests.

## Required Variables

Configure these repository variables under `Settings` -> `Secrets and variables` -> `Actions` -> `Variables`.

```text
PRIMARY_REVIEW_MODEL=gpt-4.1-mini
FINAL_REVIEW_MODEL=gpt-5.2
AUTO_MERGE_METHOD=merge
AUTO_MERGE_BLOCK_LABELS=needs-human,blocked,no-auto-merge,hold
CODEX_HANDOFF_READY_LABELS=codex-ready,ready-for-codex
CODEX_HANDOFF_BLOCK_LABELS=needs-human,blocked,hold,no-auto-merge,codex-active
CODEX_HANDOFF_ACTIVE_LABEL=codex-active
CODEX_HANDOFF_PRIORITY_LABEL=priority-high
```

The model and label variables have defaults, but setting them explicitly makes new repositories easier to audit. Older repositories that still have `FINAL_REVIEW_MODEL=gpt-5.5` are normalized by the review runner to `gpt-5.2`.

## Codex Cloud Environment

Create a Codex Cloud environment for every repository where `@codex` handoff comments should start Codex automatically.

1. Open [Codex environments](https://chatgpt.com/codex/cloud/settings/environments).
2. Create a new environment for the target repository.
3. Use the `universal` container image unless the project needs a custom image.
4. Leave setup script on automatic unless the project needs custom dependencies.
5. Save the environment.
6. Test with an issue comment such as `@codex please confirm you can run from this issue`.

Automatic pickup requires both the Codex Cloud environment and `CODEX_TRIGGER_TOKEN`. The environment lets Codex run in the repository; the token lets the GitHub Actions workflow post an `@codex` comment from a non-Actions identity that Codex Cloud can pick up.

## Automatic GPT Review

`gpt-review.yml` runs on both `pull_request` and `pull_request_target`.

The `pull_request` job has no OpenAI secret and validates Python syntax from the PR. The `pull_request_target` job uses trusted base-branch code, checks out PR content only as review material, and calls:

```text
python trusted/scripts/project_gpt_review.py
```

The review has no `paths` restriction. Template, workflow, script, prompt, README, docs, templates, project rules, manuscript, reference, and generated-file PRs are all audited.

GPT Review classifies PRs into:

- `TEMPLATE_OR_WORKFLOW_PR`
- `MANUSCRIPT_SETUP_OR_GENERATED_FILES_PR`
- `MANUSCRIPT_SUBMISSION_PR`

The PR mode is based on changed files. A PR is not skipped just because `submission/` is absent.

## Codex Advisory

GPT Review is also an advisor for Codex running inside GitHub. Each review includes a `Codex Advisory` and `Codex Fix Instructions` section. When the PR needs revision, the advisory should explain what is wrong, why it matters, which files to edit, how to repair the issue, and how Codex can know the fix is complete.

## Auto-Merge

`auto-merge-reviewed-pr.yml` runs after `GPT Review` completes. It merges only when all of these are true:

- The completed workflow is `GPT Review`.
- The workflow conclusion is `success`.
- The review run is the trusted `pull_request_target` run.
- The review artifact contains `FINAL_REVIEW_STATUS: PASS`.
- The artifact does not contain `REVIEW_STATUS: NEEDS_REVISION` or `FINAL_REVIEW_STATUS: FAIL`.
- The reviewed head SHA matches the current PR head SHA.
- The PR is open, not draft, and mergeable.
- The PR does not have a blocking label.

Default blocking labels:

```text
needs-human,blocked,no-auto-merge,hold
```

## Codex Next-Issue Handoff

`codex-next-issue-handoff.yml` runs after a PR is merged and can also be run manually with `workflow_dispatch`.

It selects one issue only when all of these are true:

- The issue is open.
- The issue has `codex-ready` or `ready-for-codex`.
- The issue is not a pull request.
- The issue does not have `needs-human`, `blocked`, `hold`, `no-auto-merge`, or `codex-active`.
- The issue has not already received the stable handoff marker comment.

Selection order:

```text
priority-high first
then oldest eligible issue
```

When selected, the issue receives `codex-active`, then an `@codex` handoff comment posted with `CODEX_TRIGGER_TOKEN`. If the token is missing, the workflow fails instead of silently posting with `github-actions[bot]`.

## Codex Autopilot Loop

Recommended project flow:

```text
User describes the desired product
v
Codex writes PROJECT_VISION.md and PROJECT_MEMORY.md
v
Codex creates small codex-ready issues
v
User says 作成開始, or a merged PR triggers handoff
v
Codex implements one issue and opens one PR
v
GPT Review audits the PR and gives Codex Advisory if needed
v
PASS triggers auto-merge unless a stop condition exists
v
Merged PR triggers the next eligible issue handoff
```

Use `docs/codex-autopilot.md` for the full issue queue and stop-condition rules.

## Stop Conditions

Automation should stop when any of these are true:

- No ready issue exists.
- The next issue has `needs-human`, `blocked`, `hold`, or `codex-active`.
- `CODEX_TRIGGER_TOKEN` is missing when a ready issue needs automatic Codex pickup.
- The PR is draft, blocked, unmergeable, or labeled `no-auto-merge`.
- GPT Review returns `FINAL_REVIEW_STATUS: WARN` or `FAIL` and requires human confirmation.
- The work needs secrets, billing changes, destructive operations, or unclear product judgment.

## New Repository Setup

1. Click `Use this template`.
2. Create the new repository.
3. Add `OPENAI_API_KEY` as an Actions secret.
4. Add `CODEX_TRIGGER_TOKEN` as an Actions secret if automatic next-issue pickup is desired.
5. Add the repository variables listed above.
6. Create a Codex Cloud environment for the repository.
7. Fill in `PROJECT_VISION.md`.
8. Update `PROJECT_MEMORY.md` as decisions are made.
9. Create small issues and label ready work with `codex-ready` or `ready-for-codex`.
10. Open a small test PR and confirm GPT Review runs automatically.
11. Confirm a PASS PR auto-merges when no stop condition exists.
12. Confirm a merged PR hands off the next ready issue and Codex Cloud responds.

## Use This Template Guarantee

When the required secrets, variables, and Codex Cloud environment are configured, projects created from this template are wired for this path:

```text
Codex change
v
Pull request
v
Automatic GPT Review
v
Codex Advisory
v
Auto-merge after trusted PASS
v
Next ready issue receives @codex handoff
v
Codex Cloud starts the next issue
```
