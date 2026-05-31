## Summary

- 

## Validation

- [ ] I ran the relevant local checks, or explained why they were not run.
- [ ] The GPT review workflow is expected to run on this PR.
- [ ] Any generated teacher-facing summary can be understood by a non-engineer.

## GPT Review Setup

- [ ] `.github/workflows/gpt-review.yml` is present.
- [ ] The workflow calls `kawakawakawa1592-ops/ai-review-workflows`.
- [ ] `OPENAI_API_KEY` is configured in GitHub Actions secrets.
- [ ] `PRIMARY_REVIEW_MODEL` is `gpt-4.1-mini` unless intentionally changed.
- [ ] `FINAL_REVIEW_MODEL` is `gpt-5.5` unless intentionally changed.
- [ ] The expected flow is Codex -> PR -> GPT review -> teacher-facing summary.

## Notes

-
