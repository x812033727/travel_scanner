---
id: 2026-09-27-half-width-punctuation-in-zh-tw
title: Half-width punctuation in zh-TW, zh-CN and ja news passes every check
status: done
priority: P2
area: api
owner: codex-gpt6-news-policy
claimed_at: 2026-09-30T02:49:07Z
created_at: 2026-09-27T09:42:30Z
completed_at: 2026-09-30T02:56:51Z
branch: codex/news-cjk-punctuation
depends_on: []
scope:
  - apps/api/app/news_automation/policy.py
  - apps/api/tests/test_news_automation.py
---

# Half-width punctuation in zh-TW, zh-CN and ja news passes every check

## Why

Three of the 11 held drafts reviewed on 2026-09-27 had ASCII `, : ; ? ( )` throughout their
zh-TW and zh-CN text, and `: ? ( )` in ja. The affected drafts were
`ai-news-anthropic-founders-voting-control-ipo-20260925`,
`crypto-news-kelpdao-sues-layerzero-20260925` and `tech-news-aema-alliance-20260916`. That
included headlines such as 「KelpDAO 起訴 LayerZero 與其執行長,指控 2.92 億美元跨鏈橋漏洞」.
The other drafts in the same batch use full-width punctuation. The text reads as broken
typesetting, and no stage flags it: the locale reviews pass it, and `hard_policy_problems`
does not look at punctuation. The repo has corrected the same thing by hand before
(`docs/news-2026-batch-4/translation-corrections.json`).

The 2026-09-27 fix normalised those three drafts by script. The rule it used: an ASCII
`, : ; ? ! ( )` next to a CJK character becomes full-width; numbers, times, URLs and Latin
runs stay as they are; and ja commas are not changed.

## Definition of done

- [x] A zh-TW, zh-CN or ja news document with half-width punctuation next to CJK text either
      fails a hard check with the places listed, or is normalised before the checks run.
- [x] `50.1%`, `17:35`, URLs and Latin names inside the text are untouched.

## Steps

- [x] Choose between normalising (deterministic, no model cost) and failing a hard check.
- [x] Implement it in `policy.py` with tests for the cases above.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_automation.py -q
```

## Notes

- 2026-09-30: chose a hard check with field locations, preserving the original
  document and its review fingerprint. Scope/branch audit at main 444d52af found
  no overlapping live PR among 16 open PRs or dirty edits in 177 worktrees.
  Source titles and image credits remain original evidence metadata; code and
  URLs are not localized prose. Japanese ASCII commas remain allowed.
- `news_punctuation` errors name each affected reader field and its 1-based
  character positions. The check covers immediate Han/kana adjacency in titles,
  descriptions, hero alt text, and every prose block field; rendered rich-inline
  boundaries are checked together, with code kept as opaque spans. English and
  Korean documents are unaffected.
- Bare URL tokens end at whitespace, ASCII quotes or angle brackets; full-width
  punctuation can belong to a Unicode path/query. A URL-shaped structured link
  label and each contiguous plain-text run are masked separately before joining
  inlines so neither can hide punctuation in the other.
  The check changes no text or document fingerprints and uses existing hard-check
  gates in the pipeline and manual publication path.
- Validation: 94 news automation tests passed (60 new punctuation cases), plus
  85 pipeline/review/admin tests, with pytest cache disabled. Five URL boundary
  regressions failed before the fix and passed afterward. Full API Ruff,
  mypy app (444 files), and mypy tests (333 files) passed. No production data,
  settings or model calls were used; full service integration remains CI validation.
- Final pre-PR audit: main remains 444d52af, with no competing changes among
  16 open PRs, 48 remote heads and 177 accessible worktrees. Independent review
  passed eight URL/inline-boundary and offset cases. `check:tasks` also passed.
- Before push, rebased onto 7c8e524d (web hreflang change only). The tested API
  source and test files are byte-identical after rebase; task validation passed again.
- If the normalisation is added, `document_fingerprint` must see the normalised text.
  Otherwise a verification made before normalising goes stale.
