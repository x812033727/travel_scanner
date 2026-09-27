---
id: 2026-09-27-half-width-punctuation-in-zh-tw
title: Half-width punctuation in zh-TW, zh-CN and ja news passes every check
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-27T09:42:30Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/policy.py
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

- [ ] A zh-TW, zh-CN or ja news document with half-width punctuation next to CJK text either
      fails a hard check with the places listed, or is normalised before the checks run.
- [ ] `50.1%`, `17:35`, URLs and Latin names inside the text are untouched.

## Steps

- [ ] Choose between normalising (deterministic, no model cost) and failing a hard check.
- [ ] Implement it in `policy.py` with tests for the cases above.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_automation.py -q
```

## Notes

- If the normalisation is added, `document_fingerprint` must see the normalised text.
  Otherwise a verification made before normalising goes stale.
