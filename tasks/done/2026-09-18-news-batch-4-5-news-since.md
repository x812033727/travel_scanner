---
id: 2026-09-18-news-batch-4-5-news-since
title: News batch 4.5: news since 2026-09-16 for the three verticals
status: done
priority: P1
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-18T05:17:48Z
created_at: 2026-09-18T05:17:33Z
completed_at: 2026-09-18T08:44:16Z
branch: claude/news-batch-4-5-since-0916
depends_on: []
scope:
  - apps/api/app/guides/content/ai-news-chatgpt-sponsored-agents-20260916.json
  - apps/web/public/guides/ai-news-chatgpt-sponsored-agents-20260916
  - apps/api/app/guides/content/ai-news-firefox-smart-window-mistral-20260916.json
  - apps/web/public/guides/ai-news-firefox-smart-window-mistral-20260916
  - apps/api/app/guides/content/ai-news-openai-misalignment-reports-20260917.json
  - apps/web/public/guides/ai-news-openai-misalignment-reports-20260917
  - apps/api/app/guides/content/ai-news-anthropic-pace-metrics-20260917.json
  - apps/web/public/guides/ai-news-anthropic-pace-metrics-20260917
  - apps/api/app/guides/content/ai-news-astra-for-law-20260917.json
  - apps/web/public/guides/ai-news-astra-for-law-20260917
  - apps/api/app/guides/content/ai-news-google-cc-family-agent-20260918.json
  - apps/web/public/guides/ai-news-google-cc-family-agent-20260918
  - apps/api/app/guides/content/tech-news-apple-att-eu-20260916.json
  - apps/web/public/guides/tech-news-apple-att-eu-20260916
  - apps/api/app/guides/content/tech-news-app-store-bundles-multiseat-20260916.json
  - apps/web/public/guides/tech-news-app-store-bundles-multiseat-20260916
  - apps/api/app/guides/content/tech-news-eu-kids-act-20260917.json
  - apps/web/public/guides/tech-news-eu-kids-act-20260917
  - apps/api/app/guides/content/tech-news-taiwan-matsu-cable-tm4-20260918.json
  - apps/web/public/guides/tech-news-taiwan-matsu-cable-tm4-20260918
  - apps/api/app/guides/content/crypto-news-fca-perimeter-guidance-20260916.json
  - apps/web/public/guides/crypto-news-fca-perimeter-guidance-20260916
  - apps/api/app/guides/content/crypto-news-cftc-passive-software-20260917.json
  - apps/web/public/guides/crypto-news-cftc-passive-software-20260917
  - apps/api/app/guides/content/crypto-news-fca-p2p-crypto-crackdown-20260917.json
  - apps/web/public/guides/crypto-news-fca-p2p-crypto-crackdown-20260917
  - docs/ai-news-2026-09-late
  - docs/tech-news-2026
  - docs/crypto-news-2026
  - apps/api/app/guides/content/ai-news-2026-january-september-index.json
  - apps/api/app/guides/content/tech-news-2026-index.json
  - apps/api/app/guides/content/crypto-news-2026-index.json
  - docs/news-2026-batch-4/check_article.py
  - docs/news-2026-batch-4/build_assets.py
  - docs/news-2026-batch-4/update_index.py
  - docs/news-2026-batch-4/review_dumps.py
  - docs/news-2026-batch-4/HANDOVER.md
  - docs/news-2026-batch-4/candidates-since-0916-ai.md
  - docs/news-2026-batch-4/candidates-since-0916-tech.md
  - docs/news-2026-batch-4/candidates-since-0916-crypto.md
  - docs/news-2026-batch-4/research
  - docs/news-2026-batch-4/factcheck-draft
  - docs/news-2026-batch-4/translation-corrections.json
  - docs/news-2026-batch-4/coordinator-corrections.json
  - docs/news-2026-batch-4/agents
---

# News batch 4.5: news since 2026-09-16 for the three verticals

## Why

Batches 4.1-4.3 (crypto #544, tech #546, AI #548) covered the news up to 2026-09-15. The owner chose
to skip the 15 minor items of 8/1-9/15 (task 2026-09-16-news-batch-4-4-the-8) and to keep only the
news since 2026-09-16 flowing: three discovery agents swept the official feeds, the owner picked 13
of the candidates (AI 6, tech 4, crypto 3), and each is written, fact-checked twice, translated into
four languages, reviewed per language and added to its vertical's index -- the same line as 4.1-4.3,
with the differences written down in `docs/news-2026-batch-4/agents/DELTA-4-5.md`.

## Definition of done

- [x] 13 content packs in five locales, each with an original hero and a diagram in every locale,
      passing `check_article.py <slug> --full --assets`.
- [x] Two rounds of independent fact-checking per article (reports in `factcheck-draft/`,
      `factcheck` + `second_round` in each research record) and a per-language review applied
      through `apply_corrections.py`.
- [x] The three indexes expanded in place in five languages (`update_index.py`), without rerunning
      `build_*_index.py`.
- [x] `pack_cli lint --kind life` 0 errors, content tests green, `npm run check:tasks` green.
- [x] Published: deploy, then `guides-import --slug` for the 13 articles and the 3 indexes in one run
      (dry-run first), then the public URLs verified.

## Steps

- [x] Discovery: `candidates-since-0916-{ai,tech,crypto}.md` + `research/*.json`, owner's pick.
- [x] `check_article.py` RELATED (display_order AI 161-166, tech 313-316, crypto 211-213).
- [x] Writers (sonnet) x13, first-round fact-check (opus) x13, second round x13.
- [x] Coordinator read-through, hero alts, 13 drawings in `build_assets.py`.
- [x] Translators (sonnet) x13, `translation_checks.py`, `normalize_locales.py`.
- [x] Reviewers: two groups per language (ja/ko opus, en/zh-CN sonnet), 248 corrections applied.
- [x] `align_links.py`, `sync_captions.py`, `related`, `pack_cli relink`, image builds.
- [x] `update_index.py` for all three verticals (INSERT table: tech group paragraphs, crypto UK section).
- [x] Checks, HANDOVER 1d, workspace READMEs, PR.
- [x] Owner's explicit choice to merge and publish; deploy; import; verify.

## How to verify

```bash
cd apps/api
for s in <13 slugs>; do PYTHONUTF8=1 ./.venv/Scripts/python.exe ../../docs/news-2026-batch-4/check_article.py $s --full --assets; done
./.venv/Scripts/python.exe -m app.guides.pack_cli lint --kind life
./.venv/Scripts/python.exe -m pytest tests/test_guides_content_pack.py tests/test_guides_content_links.py -q
cd ../.. && npm run check:tasks
```

## Notes

- Done 2026-09-18: PR #550 squash-merged as f5cf4950, deploy_20260918_083808, `guides-import --slug` x16
  (create 65 / update 15, failed null), 80 public URLs verified (200, sitemap, hero). Details in HANDOVER 1d.

- Scope lists the batch directory file by file: the whole directory would cover the only scope file
  of task 2026-09-16-news-batch-4-4-the-8, which stays open for the 8/1-9/15 items.
- The AI index's expansion sentences now say "expanded several times since (most recently on
  EXPANDED_ON)"; the next batch changes that constant in `update_index.py` and nothing else.
- `review_dumps.py` takes an optional slug list now (a later batch adds a few packs to a vertical
  whose earlier packs were reviewed already); `update_index.py` has an `INSERT` table.
