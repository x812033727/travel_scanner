---
id: 2026-09-26-news-batch-4-8-ten-five
title: News batch 4.8: ten five-language stories the hourly automation missed (2026-09-17 to 09-25)
status: done
priority: P2
area: docs
owner: claude-opus-5-5-news-backfill
claimed_at: 2026-09-26T13:37:18Z
created_at: 2026-09-26T13:37:11Z
completed_at: 2026-09-26T18:17:23Z
branch: claude/news-batch-4-8-work
depends_on: []
scope:
  - docs/news-2026-batch-4/agents/DELTA-4-8.md
  - docs/news-2026-batch-4/candidates-since-0922-ai.md
  - docs/news-2026-batch-4/candidates-since-0922-tech.md
  - docs/news-2026-batch-4/candidates-since-0922-crypto.md
  - docs/news-2026-batch-4/check_article.py
  - docs/news-2026-batch-4/build_assets.py
  - docs/news-2026-batch-4/update_index.py
  - docs/news-2026-batch-4/HANDOVER.md
  - docs/news-2026-batch-4/translation-corrections.json
  - docs/news-2026-batch-4/factcheck-draft
  - docs/ai-news-2026-09-late/research
  - docs/ai-news-2026-09-late/manifest.json
  - docs/tech-news-2026/research
  - docs/tech-news-2026/manifest.json
  - docs/crypto-news-2026/research
  - docs/crypto-news-2026/manifest.json
  - apps/api/app/guides/content/ai-news-2026-january-september-index.json
  - apps/api/app/guides/content/tech-news-2026-index.json
  - apps/api/app/guides/content/crypto-news-2026-index.json
  - apps/api/app/guides/content/ai-news-chatgpt-ads-taiwan-20260923.json
  - apps/web/public/guides/ai-news-chatgpt-ads-taiwan-20260923
  - apps/api/app/guides/content/ai-news-gpt-6-sol-luna-20260923.json
  - apps/web/public/guides/ai-news-gpt-6-sol-luna-20260923
  - apps/api/app/guides/content/ai-news-claude-opus-55-20260922.json
  - apps/web/public/guides/ai-news-claude-opus-55-20260922
  - apps/api/app/guides/content/ai-news-google-vids-omni-free-20260924.json
  - apps/web/public/guides/ai-news-google-vids-omni-free-20260924
  - apps/api/app/guides/content/tech-news-wordpress-712-20260922.json
  - apps/web/public/guides/tech-news-wordpress-712-20260922
  - apps/api/app/guides/content/tech-news-synology-dsm-sa2613-20260918.json
  - apps/web/public/guides/tech-news-synology-dsm-sa2613-20260918
  - apps/api/app/guides/content/tech-news-snapdragon-8-elite-gen6-20260922.json
  - apps/web/public/guides/tech-news-snapdragon-8-elite-gen6-20260922
  - apps/api/app/guides/content/crypto-news-japan-onchain-finance-forum-20260925.json
  - apps/web/public/guides/crypto-news-japan-onchain-finance-forum-20260925
  - apps/api/app/guides/content/crypto-news-taiwan-cbc-stablecoin-deposit-token-cbdc-20260917.json
  - apps/web/public/guides/crypto-news-taiwan-cbc-stablecoin-deposit-token-cbdc-20260917
  - apps/api/app/guides/content/crypto-news-korea-market-manipulation-referrals-20260923.json
  - apps/web/public/guides/crypto-news-korea-market-manipulation-referrals-20260923
---

# News batch 4.8: ten five-language stories the hourly automation missed (2026-09-17 to 09-25)

## Why

The hourly news automation produced almost nothing from 2026-09-24. Besides re-running the 127
candidates old rules and old models had stopped (PR #806), the owner asked on 2026-09-26 for one
more hand-made batch as practice: ten articles in five languages, AI 4, tech 3, crypto 3. All ten
come from publishers the automation does not read (OpenAI, Anthropic, Qualcomm, WordPress.org,
Synology, Japan FSA, Taiwan's central bank, Korea FSC). Rules: `docs/news-2026-batch-4/agents/DELTA-4-8.md`.

## Definition of done

- [x] Ten packs (slugs and `display_order` in DELTA-4-8 item 4), each with a research record
      (`sourcing_verdict: full`), two fact-check rounds by different agents
      (`factcheck-draft/<slug>-round1|2.md`), four translations and per-language review, one drawing
      (`build_assets.py` `# 4.8`).
- [x] Every slug passes `check_article.py <slug> --full --assets`; `pack_cli lint --kind life` zero errors.
- [x] The three indexes carry the ten links in all five locales (`update_index.py`, not `build_*_index.py`).
- [x] Merged, deployed, `guides-import --slug` x10 plus the three indexes (dry-run first, owner's
      consent before `--publish`), recheck dry-run all unchanged, `verify_public.py` all PASS.

## Steps

- [x] Research records (opus, one per slug).
- [x] zh-TW drafts (sonnet), then fact check round 1 and round 2 (opus, different agents).
- [x] Translation x4 (sonnet), review (ja/ko opus, en/zh-CN sonnet), apply corrections, normalize.
- [x] Drawings, relink, related, index update, lint.
- [x] PR, CI, merge.
- [x] Deploy, import, verify; numbers into HANDOVER and this ticket.

## How to verify

- `PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe ../../docs/news-2026-batch-4/check_article.py <slug> --full --assets` exits 0 for each slug.
- `pytest tests/test_guides_content_pack.py tests/test_guides_content_links.py -q`, `npm run check:tasks`.

## Notes

- Claimed with `--force`: batch 4.4 (`2026-09-16-news-batch-4-4-the-8`) holds `check_article.py`,
  `build_assets.py`, `update_index.py`, HANDOVER and the research folders but is parked until the
  weekly reset. Both batches only append their own `# 4.4` / `# 4.8` sections; whoever merges
  second rebases.
- Work directory outside the repo: `<home>\mokaair-work\news-batch-4-8\` (STATE.md,
  ASSIGNMENTS.md, the shared agent prompts, raw fetches).
- The WordPress slug is `tech-news-wordpress-712-20260922` (event = the 9/22 release; CISA's KEV
  listing is the follow-up), not the discovery agent's `...-kev-20260925`.
- Found in passing and filed separately: `2026-09-26-update-chatgpt-ads-taiwan-status-openai`,
  `2026-09-26-review-evergreen-ai-pages-after-claude`, `2026-09-26-refresh-stale-parts-of-the-three`.
- Numbers, rulings and the coordinator's own zh-TW edits: `docs/news-2026-batch-4/HANDOVER.md` §1h.

## Result (2026-09-26 UTC)

PR #817 (`fe852236`) merged and deployed 17:50Z. `guides-import` published 65 locale pages
(50 created, 15 index updates), failed null; the recheck dry run is 65 unchanged and
`verify_public.py --from-report --sitemap` passes all 65. Details in HANDOVER §1h.
