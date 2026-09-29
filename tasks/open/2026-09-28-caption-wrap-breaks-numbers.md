---
id: 2026-09-28-caption-wrap-breaks-numbers
title: Caption wrapping can break inside numbers and product names, and start a line with a full stop, in CJK locales
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-28T05:04:19Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/captions.mjs
  - tools/video/core/captions.test.mjs
---

# Caption wrapping can break inside numbers and product names, and start a line with a full stop, in CJK locales
## Why

Found on 2026-09-28 while translating the English season's captions into zh-CN (`docs/videos/<slug>/i18n/zh-CN.json` for `openai-agents-broke-in`, `always-on-agent-explained`, `gpt6-vs-opus55-worth-paying`). Simulating the cues with `buildCues` in `tools/video/core/captions.mjs`, the CJK line wrap produced breaks inside a number or product name (「4 / .0」, 「GPT / -6」, 「0. / 50」) and let a caption line start with 「。」. The translator reworded about 60 lines so these three videos never hit it; the next CJK translation will.

## Definition of done

- [ ] A CJK caption line never breaks inside a run of Latin letters, digits and the joiners `. - + # ' _` (a version like `4.0`, a price like `0.50`, a name like `GPT-6`), unless the run alone is longer than the line.
- [ ] A caption line never starts with closing punctuation, 「。」 included (`OPENS_BADLY` covers it and the break search honours it).
- [ ] Tests in `tools/video/core/captions.test.mjs` cover each case; existing zh-TW captions of earlier videos are unchanged where they had no such break.

## Steps

- [ ] Reproduce with a zh-CN line like 「Terminal-Bench 4.0 得分 66.4%」 and a narrow `maxChars`.
- [ ] Fix the tokenizer or the break search, add tests, run `npm run test:tools`.

## How to verify

```bash
node --test tools/video/core/captions.test.mjs
npm run test:tools
```

## Notes

- The zh-CN translator's simulation scripts are in the session scratchpad (`zhcn/`), not in the repo; the cases above are enough to reproduce.
