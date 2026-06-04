## Summary

- 

## Validation

- [ ] I ran the relevant local checks, or explained why they were not run.
- [ ] The GPT review workflow is expected to start automatically on this PR.
- [ ] Any generated teacher-facing summary can be understood by a non-engineer.
- [ ] Any required Codex Advisory can be acted on without the user rewriting the repair instruction.

## GPT Review Setup

- [ ] `.github/workflows/gpt-review.yml` is present.
- [ ] The workflow runs on pull request `opened`, `synchronize`, `reopened`, and `ready_for_review` events.
- [ ] The workflow has no `paths` restriction that would skip ordinary PRs.
- [ ] The workflow uses trusted base-branch review code separately from PR content.
- [ ] OpenAI secrets are scoped only to the trusted review step.
- [ ] Codex does not need to request GPT Review manually.
- [ ] `scripts/project_gpt_review.py` is present and classifies PRs from changed files.
- [ ] `.github/prompts/project_review_prompt.md` is present.
- [ ] GPT Review output includes a `Codex Advisory` section with problem, reason, recommended fix, files to edit, and acceptance criteria.
- [ ] `OPENAI_API_KEY` is configured in GitHub Actions secrets.
- [ ] `PRIMARY_REVIEW_MODEL` is `gpt-4.1-mini` unless intentionally changed.
- [ ] `FINAL_REVIEW_MODEL` is `gpt-5.5` unless intentionally changed.
- [ ] The expected flow is Codex -> PR -> automatic GPT review -> teacher-facing summary -> Codex Advisory.

## Auto-Merge / Autopilot

- [ ] `.github/workflows/auto-merge-reviewed-pr.yml` is present when this repository should auto-merge passing PRs.
- [ ] `scripts/auto_merge_reviewed_pr.py` only merges after GPT Review success and `FINAL_REVIEW_STATUS: PASS`.
- [ ] Draft, blocked, human-needed, held, and unmergeable PRs do not auto-merge.
- [ ] Ready implementation work is represented as `codex-ready` issues.
- [ ] Stop conditions use labels such as `needs-human`, `blocked`, `hold`, or `no-auto-merge`.

## Notes

-
