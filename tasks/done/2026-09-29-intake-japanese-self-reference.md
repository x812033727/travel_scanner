---
id: 2026-09-29-intake-japanese-self-reference
title: Use Japanese self-reference terms in content intake
status: done
priority: P2
area: tools
owner: codex-batch041-summary
claimed_at: 2026-09-29T05:25:28Z
created_at: 2026-09-29T05:25:28Z
completed_at: 2026-09-29T05:37:52Z
branch: codex/batch041-summary-correction
depends_on: []
scope:
  - .agents/skills/content-pipeline/scripts/intake_check.py
  - apps/api/tests/test_content_pipeline_intake.py
---

# Use Japanese self-reference terms in content intake

## Why

The intake script applies the Chinese 本文/這篇 matcher to every locale. In
Japanese title-writing material, 本文 means the body text, so legitimate examples
are reported as 16 self-references and fail the one-reference threshold.

## Definition of done

- [x] Japanese body-text references do not trigger this false positive.
- [x] Explicit Japanese references to this article/manuscript still enforce the
      existing threshold and manifest override.
- [x] Other locales and the independent reader-first, summary and link checks
      retain their existing behavior.
- [x] Focused regression tests prove the original failure and corrected behavior.

## Steps

- [x] Check local/remote branches and all open PR file scopes; no competing fix.
- [x] Implement the locale-specific matcher and accurate diagnostic.
- [x] Run regression tests, scoped Ruff/mypy and shared-skill contract checks.

## How to verify

Run the new API test module, Ruff on the script and test, mypy on the test,
and `node --test tools/skills.test.mjs`. Run strict intake on both Batch041
keyword/title guides in all five locales with the separately reviewed summaries.

## Notes

Only ja selects 本記事/この記事/本稿; the fallback 本文/這篇 expression remains
unchanged. Do not raise the limit, delete Japanese article wording, or use
--no-reader-first. The canonical script exists only under .agents; there is no
.claude script copy. The existing SKILL.md mirror is not changed.

This task changes local editorial tooling, not content publication policy or
production settings. Content changes have their own task and review binding.

## Completion evidence

See `docs/article-localization/batch041-summary-correction.md` for before/after
source and locale hashes, two independent content review receipts, preserved
asset hashes, strict-intake results and the formal-release handoff.

- Applied ten three-sentence summaries; no facts, dates, assets or later blocks changed.
- Real strict intake: 10/10 pass without disabled checks or higher limits.
- New matcher regression: old tool 9 failed/12 passed; corrected tool 21 passed.
- Installed targeted pytest (intake, content pack, content links): 33 passed,
  5 isolated-PostgreSQL skips. Scoped Ruff/mypy and six skill contract tests pass.
- Independent code review passed. Twenty standalone desktop/mobile previews
  pass DOM checks and changed-region visual review; forty image loads succeed.
- Original T2 freeze is immutable. The new two-source/eight-target hashes require
  separately approved source reconciliation, release rebinding and PostgreSQL
  rehearsal before publication. The original release task remains open.

This ticket closes the reviewed local correction only, within a draft PR;
it does not mark source publication or the original localization release done.
