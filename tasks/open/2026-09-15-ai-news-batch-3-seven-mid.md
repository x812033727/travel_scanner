---
id: 2026-09-15-ai-news-batch-3-seven-mid
title: AI news batch 3: seven mid-September stories and the month index
status: review
priority: P2
area: docs
owner: claude-opus-5
claimed_at: 2026-09-15T13:13:31Z
created_at: 2026-09-15T13:13:25Z
completed_at:
branch: claude/recent-ai-news-4fadd1
depends_on: []
scope:
  - docs/ai-news-2026-09-mid
  - apps/api/app/guides/content/ai-news-2026-january-september-index.json
  - apps/api/app/guides/content/ai-news-gpt-live-voice-20260708.json
  - apps/web/public/guides/ai-news-gpt-live-voice-20260708
  - apps/api/app/guides/content/ai-news-google-assistant-gemini-20260904.json
  - apps/web/public/guides/ai-news-google-assistant-gemini-20260904
  - apps/api/app/guides/content/ai-news-anthropic-threat-report-20260910.json
  - apps/web/public/guides/ai-news-anthropic-threat-report-20260910
  - apps/api/app/guides/content/ai-news-openai-agents-api-20260910.json
  - apps/web/public/guides/ai-news-openai-agents-api-20260910
  - apps/api/app/guides/content/ai-news-deepseek-v41-flash-20260910.json
  - apps/web/public/guides/ai-news-deepseek-v41-flash-20260910
  - apps/api/app/guides/content/ai-news-pace-the-frontier-20260912.json
  - apps/web/public/guides/ai-news-pace-the-frontier-20260912
  - apps/api/app/guides/content/ai-news-siri-ai-ios-27-20260914.json
  - apps/web/public/guides/ai-news-siri-ai-ios-27-20260914
---

# AI news batch 3: seven mid-September stories and the month index

## Why

The 2026 AI news album (`docs/ai-news-2026-09`, `docs/ai-news-2026-ytd`, PRs #473/#497) stops at
ChatGPT Images 2.5 on 2026-09-08. Between 9/4 and 9/14 several stories that change what ordinary
readers can do landed (Gemini replacing Google Assistant, Siri AI, a misuse threat report, the
OpenAI Agents API, DeepSeek V4.1-Flash, Amodei's "We Must Pace the Frontier"), and GPT-Live voice
from 2026-07-08 was never covered. The site owner picked these seven on 2026-09-15.

## Definition of done

- [x] Seven new `kind=life` packs, each in zh-TW, en, ja, ko, zh-CN, with sources checked on 2026-09-15.
- [x] Each has an original hero (JPEG ≤ 300 KB) and a 2×2 SVG diagram per locale.
- [x] `ai-news-2026-january-september-index` links all 38 articles in five languages, and its
      Japanese month headings read 「2026年N月のニュース解説」.
- [ ] Merged, deployed, imported with `guides-import --slug`, and verified logged out.

## Steps

- [x] Research and zh-TW drafts, one agent per article (`docs/ai-news-2026-09-mid/BRIEF.md`).
- [x] Independent fact-check of every draft against the primary sources.
- [x] Translations and a translation review.
- [x] `build_assets.py`, then look at every hero and diagram.
- [x] `update_index.py`.
- [x] Local checks and a rendered look at one article on desktop and phone.
- [ ] Pull request; after merge, deploy and import the eight slugs.

## How to verify

```bash
cd apps/api
PY=/c/Users/x8120/mokaair/apps/api/.venv/Scripts/python.exe   # or uv run python
for s in $($PY -c "import json;print(' '.join(e['slug'] for e in json.load(open('../../docs/ai-news-2026-09-mid/manifest.json',encoding='utf-8'))))"); do $PY ../../docs/ai-news-2026-09-mid/check_article.py $s --full --assets; done
$PY -m app.guides.pack_cli lint --kind life
uv run pytest tests/test_guides_content_pack.py tests/test_guides_content_links.py
```

After the import: each of the 40 locale URLs answers 200 without noindex, h1 equals the pack
title, and `/sitemap.xml` lists it.

## Notes

- Aggregator sites (aiweekly, llm-stats, releasebot) are leads only. Their numbers about an
  "OpenAI agents attacked Hugging Face" incident are not used; the Pace the Frontier article only
  relays Amodei's own description of that incident (he links METR's 2026-08-26 report), attributed
  to him and not verified by us.
- GPT-Live's official launch date is 2026-07-08, not 07-09 as first planned; the slug follows it.
- Seen in passing, outside this scope: `apple-intelligence-guide` dates iOS 27 to September 15
  (Apple: 14) and cites a support page still describing iOS 26; `deepseek-beginner-guide` says the
  V4.1-Flash model card shows vLLM/SGLang launch commands, which the card does not.
- The earlier batches drafted and translated with the site's Gemini provider inside the production
  API container. This batch drafts and translates with Claude agents locally, then reviews.
- The Japanese month headings in the published index were wrong since #497: the callout text and
  eight article titles sat where 「2026年N月のニュース解説」 belongs. `update_index.py` repairs them.
