---
id: 2026-10-05-life-ai-income-investing-batch
title: Life batch: AI side income and investing with AI concept stocks (12 articles)
status: review
priority: P2
area: docs
owner: claude-opus-5-5
claimed_at: 2026-10-05T04:11:29Z
created_at: 2026-10-05T02:52:27Z
completed_at:
branch: claude/determined-clarke-1laipc
depends_on: []
scope:
  - apps/api/app/guides/content/ai-freelance-getting-started.json
  - apps/api/app/guides/content/ai-freelance-client-confidentiality.json
  - apps/api/app/guides/content/ai-translation-subtitle-freelance.json
  - apps/api/app/guides/content/selling-ai-digital-products.json
  - apps/api/app/guides/content/ai-content-side-business-costs.json
  - apps/api/app/guides/content/ai-money-making-course-red-flags.json
  - apps/api/app/guides/content/ai-concept-stocks-explained.json
  - apps/api/app/guides/content/ai-server-supply-chain-layers.json
  - apps/api/app/guides/content/thematic-etf-index-rules.json
  - apps/api/app/guides/content/ai-financial-report-reading.json
  - apps/api/app/guides/content/robo-advisor-taiwan-explained.json
  - apps/api/app/guides/content/ai-trading-bot-claims.json
  - apps/web/public/guides/ai-freelance-getting-started
  - apps/web/public/guides/ai-freelance-client-confidentiality
  - apps/web/public/guides/ai-translation-subtitle-freelance
  - apps/web/public/guides/selling-ai-digital-products
  - apps/web/public/guides/ai-content-side-business-costs
  - apps/web/public/guides/ai-money-making-course-red-flags
  - apps/web/public/guides/ai-concept-stocks-explained
  - apps/web/public/guides/ai-server-supply-chain-layers
  - apps/web/public/guides/thematic-etf-index-rules
  - apps/web/public/guides/ai-financial-report-reading
  - apps/web/public/guides/robo-advisor-taiwan-explained
  - apps/web/public/guides/ai-trading-bot-claims
  - apps/api/app/guides/taxonomy.py
  - apps/api/migrations/versions/0125_ai_income_topic.py
  - apps/api/tests/test_guides_migration.py
  - docs/life-ai-income-investing
---

# Life batch: AI side income and investing with AI concept stocks (12 articles)

## Why

The owner compared the site with maplefeather.com's AI page and found two missing subjects:
earning with AI (side income, freelancing) and investing (AI concept stocks, AI and money).
The site had no article on the first and `investing` had none at all. Spec and assignments:
[`docs/life-ai-income-investing/README.md`](../../docs/life-ai-income-investing/README.md).

## Definition of done

- [x] Sub-topic `ai-income` under `ai` (taxonomy + migration 0125 + migration test).
- [x] Twelve zh-TW packs, each with a self-drawn hero, one diagram, at least 3 h2s, a table,
      sources with `checked_on` 2026-10-05, and internal links (sibling links added by the
      cross-check).
- [x] Finance-tagged pieces (7, 9-12): no named company or product, no buy/sell advice, no
      market figures, disclaimer callout last with 「不是投資建議」. The industry piece (8)
      names no company. Read by hand and checked by a sweep for company names and absolute
      wording.
- [x] `intake_check.py --from-content`: 0 FAIL x 12; `pack_cli lint --kind life`: no errors
      (one expected `finance_claim_language` warning on ai-trading-bot-claims, which quotes
      scam pitches); `tests/test_guides_content_pack.py` green.
- [ ] Deployed and published on mokaair.com: needs the owner's explicit go-ahead
      (content-pipeline rule 8). Then `guides-import --slug ... --locale zh-TW --dry-run`,
      `--publish`, `guides-links-rebuild`, `verify_public.py`.

## How to verify

```bash
cd apps/api
for s in $(ls ../../docs/life-ai-income-investing/records); do
  .venv/bin/python ../../.agents/skills/content-pipeline/scripts/intake_check.py --slug $s \
    --from-content --manifest ../../docs/life-ai-income-investing/batch.json; done
.venv/bin/python -m app.guides.pack_cli lint --kind life
.venv/bin/python -m pytest tests/test_guides_content_pack.py -q
```

## Notes

- Changed from the first plan so nothing duplicates the finance series' own tickets: ETF
  basics (`what-is-an-etf`, batch 05), sub-brokerage (`sub-brokerage-vs-foreign-broker`,
  batch 06) and side-income tax (`side-income-tax-taiwan`, batch 04) are left to them; "can
  AI images be sold" already exists as `ai-image-copyright-taiwan`, and deepfake scams as
  `ai-scams-deepfake-taiwan`. "US AI concept stocks: NVIDIA, AMD..." became
  `ai-concept-stocks-explained`, which names no company (series rule 1).
- Process (one workflow, 49 agents): writer -> independent fact-check (4-14 factual
  corrections per article) -> second checker on compliance and reader-first plus re-checking
  round 1's changes and a third of the rest (0-5 more corrections, mostly scope and precision)
  -> mechanical and visual gate -> batch cross-check (no contradictions between articles;
  sibling links; one hero redrawn as too close to another). Records per article in
  `docs/life-ai-income-investing/records/<slug>/` (notes, verify-1, verify-2) and
  `CROSS-CHECK.md`.
- Spot-checked by the coordinator against the live pages: Shutterstock's no-AI policy,
  Gumroad's 10% + $0.50 / 30%, SITCA's phone number.
- Volatile: platform fees and policies (articles 1-5), the GPT Store / custom GPT status
  (4), statute articles and fees (6, 7, 9-12). Recheck before the next tax season or when a
  platform announces a change.
- Bodies are 2,590-2,790 characters; four are above the 2,200-2,600 target but inside the
  1,800-3,000 band. 新台幣 and 新臺幣 are mixed, as they are across the site.
