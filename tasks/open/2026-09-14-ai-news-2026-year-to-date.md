---
id: 2026-09-14-ai-news-2026-year-to-date
title: Publish five-language AI news from January 2026 to present
status: review
priority: P2
area: docs
owner: codex-ai-news-ytd
claimed_at: 2026-09-14T11:08:54Z
created_at: 2026-09-14T10:58:34Z
completed_at:
branch: codex/ai-news-2026-year-to-date
depends_on: []
scope:
  - docs/ai-news-2026-ytd
  - apps/api/app/guides/content/ai-news-nvidia-rubin-20260105.json
  - apps/web/public/guides/ai-news-nvidia-rubin-20260105
  - apps/api/app/guides/content/ai-news-chatgpt-health-20260107.json
  - apps/web/public/guides/ai-news-chatgpt-health-20260107
  - apps/api/app/guides/content/ai-news-gemini-personal-intelligence-20260114.json
  - apps/web/public/guides/ai-news-gemini-personal-intelligence-20260114
  - apps/api/app/guides/content/ai-news-gpt-53-codex-20260205.json
  - apps/web/public/guides/ai-news-gpt-53-codex-20260205
  - apps/api/app/guides/content/ai-news-claude-opus-46-20260205.json
  - apps/web/public/guides/ai-news-claude-opus-46-20260205
  - apps/api/app/guides/content/ai-news-qwen-35-20260216.json
  - apps/web/public/guides/ai-news-qwen-35-20260216
  - apps/api/app/guides/content/ai-news-gemini-31-pro-20260219.json
  - apps/web/public/guides/ai-news-gemini-31-pro-20260219
  - apps/api/app/guides/content/ai-news-gpt-54-20260305.json
  - apps/web/public/guides/ai-news-gpt-54-20260305
  - apps/api/app/guides/content/ai-news-claude-interactive-visuals-20260312.json
  - apps/web/public/guides/ai-news-claude-interactive-visuals-20260312
  - apps/api/app/guides/content/ai-news-lyria-3-pro-20260325.json
  - apps/web/public/guides/ai-news-lyria-3-pro-20260325
  - apps/api/app/guides/content/ai-news-project-glasswing-20260407.json
  - apps/web/public/guides/ai-news-project-glasswing-20260407
  - apps/api/app/guides/content/ai-news-meta-muse-spark-20260408.json
  - apps/web/public/guides/ai-news-meta-muse-spark-20260408
  - apps/api/app/guides/content/ai-news-chatgpt-images-20-20260421.json
  - apps/web/public/guides/ai-news-chatgpt-images-20-20260421
  - apps/api/app/guides/content/ai-news-gpt-55-20260423.json
  - apps/web/public/guides/ai-news-gpt-55-20260423
  - apps/api/app/guides/content/ai-news-gemini-omni-20260519.json
  - apps/web/public/guides/ai-news-gemini-omni-20260519
  - apps/api/app/guides/content/ai-news-gemini-spark-20260519.json
  - apps/web/public/guides/ai-news-gemini-spark-20260519
  - apps/api/app/guides/content/ai-news-claude-fable-5-access-20260609.json
  - apps/web/public/guides/ai-news-claude-fable-5-access-20260609
  - apps/api/app/guides/content/ai-news-gpt-56-sol-preview-20260626.json
  - apps/web/public/guides/ai-news-gpt-56-sol-preview-20260626
  - apps/api/app/guides/content/ai-news-claude-sonnet-5-20260630.json
  - apps/web/public/guides/ai-news-claude-sonnet-5-20260630
  - apps/api/app/guides/content/ai-news-chatgpt-work-20260709.json
  - apps/web/public/guides/ai-news-chatgpt-work-20260709
  - apps/api/app/guides/content/ai-news-gemini-36-flash-20260721.json
  - apps/web/public/guides/ai-news-gemini-36-flash-20260721
  - apps/api/app/guides/content/ai-news-2026-january-september-index.json
  - apps/web/public/guides/ai-news-2026-january-september-index
---

# Publish five-language AI news from January 2026 to present

## Why

The user expanded the published ten-article AI news project to cover 2026-01-01 through the current date, 2026-09-14, retaining all five site languages. They explicitly chose coverage of important news in every month, without limiting the new batch to ten articles. Preserve the previous ten published news articles, add complementary dated analyses and a chronological index, then complete the existing PR/CI/merge/deploy/scoped-import/public-verification workflow.

## Definition of done

- [x] Official-source inventory covers every month January through September; existing news and active tutorial scopes are checked for overlap.
- [x] Every new news article has a complete 1800-3000-character zh-TW original and faithful en/ja/ko/zh-CN versions, table, callout, original localized hero and diagram, dated sources and relevant links.
- [x] Exact article and asset paths are added to scope and the claim revalidated before those files are created.
- [ ] Content checks, isolated import/publication/replay and required CI pass; content PR is merged.
- [ ] Fresh verified backup and approved-scope deployment/import succeed; all new locale documents, images, listing, metadata and sitemap pass signed-out desktop/mobile verification.
- [ ] Deliver the dated index and formal article links; mark done only when publication and QA are complete.

## Steps

- [x] Research and reserve exact topics.
- [x] Author, translate, review and illustrate the batch.
- [ ] Validate, merge, publish and verify the full batch.

## How to verify

Use the existing content-pack CLI lint, apps/api/tests/test_guides_content_pack.py, isolated scoped import/publication/idempotence checks, npm run check:tasks, and signed-out public browser verification for every article and locale. Production writes must be limited to a fixed manifest and five explicit locales.

## Notes

Starting branch base: 46298e2863e9c2c4d6776e9d58a821be683a4b32. The earlier receipt PR #487 merged as 50591be5. Its post-merge web CI later failed a pre-existing modal-close timing test; current main includes PR #493's commit-phase effect fix and documented regression validation. No change to those frontend scopes is part of this content task.

Existing late-July–September news are recorded in docs/ai-news-2026-09/manifest.json. Active AI-terms/tutorial and mobile-table tasks were inspected. Research currently uses a unique docs directory; exact new slugs will be reserved after source verification. User confirmed unlimited additional important monthly coverage in the asynchronous reply.

2026-09-14: Reserved 22 exact article/asset paths (21 news plus chronological index), verified against 177 live life articles and active scopes. All 22 zh-TW originals have been fully read and edited; official-source audit completed. 88 full translations and 22 fidelity reviews are complete, with 19 editorial corrections recorded. All 220 localized public images reviewed in 60 final contact sheets. Local scoped lint/import/publication/replay passed; content tests 9 passed/5 PostgreSQL skips, tools 48 passed, release-hold tests 2 passed. No production content writes yet. Main synced to a9d5b40e, matching fresh production HEAD; intervening changes are workflow dependencies and unrelated travel content only.
