---
id: 2026-10-05-gemini-grounding-citations-simplified-typo
title: gemini-api-search-grounding-citations writes 報错 with a simplified 错
status: in-progress
priority: P3
area: docs
owner: claude-opus-5-5-small-content-fixes
claimed_at: 2026-10-05T13:39:08Z
created_at: 2026-10-05T06:45:31Z
completed_at:
branch: claude/small-content-fixes
depends_on: []
scope:
  - apps/api/app/guides/content/gemini-api-search-grounding-citations.json
---

# gemini-api-search-grounding-citations writes 報错 with a simplified 错

## Why

The zh-TW article `gemini-api-search-grounding-citations` has one simplified character in its
running text: the testing paragraph ends "最後以 wrong-byte-offset.json 測中文字元被切開時能否報错，而非顯示亂碼".
`错` is the simplified form; Traditional Chinese readers expect `錯` (報錯). It was noticed on
2026-10-05 while fixing the offset-unit paragraph of the same pack
(`2026-10-03-gemini-grounding-offset-unit-recheck`), whose coordinator asked to leave every other
sentence unchanged, so it was not fixed there.

## Definition of done

- [x] The article reads 報錯, and no other simplified character is left in the pack's zh-TW text.
- [x] `pack_cli lint --kind life --slug gemini-api-search-grounding-citations` stays at 0 errors.

## Steps

- [x] Change 報错 to 報錯 (`grep -c '報错' <pack>` is 1 on 2026-10-05).
- [x] Scan the rest of the pack's zh-TW strings for other simplified-only characters (for example with
      OpenCC `s2t` on a copy and a diff), and fix what it finds.
- [ ] After the merge, re-import the slug on the host with `guides-import --slug` (owner consent).

## How to verify

```bash
grep -c '報错' apps/api/app/guides/content/gemini-api-search-grounding-citations.json   # 0 after the fix
cd apps/api && PYTHONUTF8=1 uv run python -m app.guides.pack_cli lint --kind life --slug gemini-api-search-grounding-citations
```

## Notes

- Text-only fix; no fact changes, so no source needs re-reading.
- Filed by claude-opus-5-5-ai-article-rechecks from branch `claude/ai-article-rechecks`.
- 2026-10-05, claude-opus-5-5-small-content-fixes (branch `claude/small-content-fixes`): changed the
  one 報错 to 報錯 in block 23; `grep -c '報错'` is now 0. The scan walked every string of the zh-TW
  document through OpenCC `s2t` (the `opencc` package in the API venv) and compared character by
  character. It flagged two: 错 (fixed) and 占 → 佔 in block 15 (「繁體中文通常占多個位元組」).
  占 is a Traditional character too (Taiwan writes "occupy" both as 占 and 佔); OpenCC only prefers
  佔, so it is not a simplified character and stays. The pack has only the zh-TW locale.
  `pack_cli lint --kind life --slug gemini-api-search-grounding-citations`: 0 errors, 1 warning
  (`no_summary`, unchanged from main).
- The re-import step is left unticked on purpose: this slug is deliberately unpublished, part of
  the unreleased Gemini advanced series, so it goes live with that series' release rather than in a
  `guides-import --slug` of its own. Nothing else is left; the ticket is closed.
