# Codex Autopilot Loop

This document defines the recommended semi-autonomous project loop for repositories created from this template.

## Goal

The user should only need to define the project goal, approve the start of work, and intervene when the automation reaches a stop condition. Codex and GPT Review should handle implementation, review guidance, repair, merge, and next-issue handoff as much as the repository can safely support.

## Labels

Use these labels to control the work queue:

- `codex-ready`: Codex may work on this issue.
- `ready-for-codex`: Alias for `codex-ready`, useful when a project prefers explicit handoff wording.
- `priority-high`: Prefer this issue before other ready issues.
- `codex-active`: Codex has been asked to start this issue; do not hand it off again.
- `needs-human`: Stop automation and wait for human judgment.
- `blocked`: Stop until the blocking condition is resolved.
- `no-auto-merge`: Do not auto-merge the linked PR even if GPT Review passes.
- `hold`: Temporary pause.

## Planning Flow

1. The user describes the desired product or project.
2. Codex reads `PROJECT_VISION.md`, `PROJECT_MEMORY.md`, README, and existing issues.
3. Codex writes or updates `PROJECT_VISION.md` with purpose, target users, goals, out-of-scope items, and definition of done.
4. Codex writes or updates `PROJECT_MEMORY.md` with decisions, constraints, review notes, and next actions.
5. Codex breaks the work into small issues.
6. Each issue should be independently reviewable and should usually produce one PR.
7. Issues ready for implementation receive `codex-ready` or `ready-for-codex`.
8. Issues needing human clarification receive `needs-human` instead of a ready label.

## Execution Flow

When the user says `作成開始`, `次へ`, or `次の作業に進んで`, Codex should:

1. Find open issues with `codex-ready` or `ready-for-codex`.
2. Prefer `priority-high` issues.
3. Otherwise choose the oldest ready issue that is not blocked or active.
4. Confirm the issue is still aligned with `PROJECT_VISION.md` and `PROJECT_MEMORY.md`.
5. Implement only that issue's scope.
6. Open a PR.
7. Let GPT Review run automatically.
8. If GPT Review fails, follow the `Codex Advisory` and update the PR.
9. If GPT Review passes, the auto-merge workflow may merge the PR.
10. After merge, `.github/workflows/codex-next-issue-handoff.yml` may hand off the next ready issue by posting an `@codex` comment.
11. Codex Cloud can start the next issue automatically when the repository has a configured Codex environment.
12. If no automatic pickup occurs, the user can say `次へ` and Codex should continue from the ready issue or the handoff comment.

## Auto-Merge Conditions

The repository can automatically merge a PR only when all of these are true:

- The completed workflow is `GPT Review`.
- The workflow conclusion is `success`.
- The completed GPT Review run is the trusted `pull_request_target` run.
- The `project-gpt-review` artifact contains `FINAL_REVIEW_STATUS: PASS`.
- The artifact does not contain `REVIEW_STATUS: NEEDS_REVISION`.
- The reviewed head SHA from the workflow run or review metadata matches the current PR head SHA.
- The PR is open.
- The PR is not a draft.
- The PR is mergeable.
- The PR does not have any blocking label listed in `AUTO_MERGE_BLOCK_LABELS`.

Default blocking labels:

```text
needs-human,blocked,no-auto-merge,hold
```

## Next-Issue Handoff Conditions

The repository can hand off the next issue to Codex only when all of these are true:

- A pull request was merged, or the handoff workflow was run manually.
- An open issue has `codex-ready` or `ready-for-codex`.
- The issue does not have `needs-human`, `blocked`, `hold`, `no-auto-merge`, or `codex-active`.
- The issue has not already received a handoff marker comment.
- `priority-high` issues are preferred.
- Otherwise the oldest eligible issue is selected.

When a next issue is selected, the handoff workflow:

1. Ensures the `codex-active` label exists.
2. Adds `codex-active` to the selected issue.
3. Posts an `@codex` comment with scope, project-context, and stop-condition instructions.

This requires a Codex Cloud environment for the repository if the `@codex` comment should start Codex automatically.

## Stop Conditions

Codex should stop and ask for human direction when any of these are true:

- No ready issue exists.
- The next issue has `needs-human`, `blocked`, `hold`, or `codex-active` from another active handoff.
- The requested work conflicts with `PROJECT_VISION.md`.
- GPT Review returns `FINAL_REVIEW_STATUS: WARN` or `FAIL` and the `Codex Advisory` requires human confirmation.
- The PR requires secrets, billing changes, destructive data operations, or irreversible repository changes.
- The next step is ambiguous enough that Codex would need to invent product requirements.

## User Commands

Recommended short commands:

```text
作成開始
次へ
次のcodex-ready issueに進んで
GPT ReviewのCodex Advisoryに従って修正して
```

In the same project thread, Codex should interpret those commands using this document, `PROJECT_VISION.md`, `PROJECT_MEMORY.md`, open issues, and any `@codex` handoff comment.
