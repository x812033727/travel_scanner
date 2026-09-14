---
id: 2026-09-14-guide-sitemap-capacity
title: Paginate guide sitemap before the next large multilingual publication
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-14T15:12:12Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/lib/guides.server.ts
  - apps/web/app/sitemap.ts
  - apps/web/app/sitemap.test.ts
  - apps/api/app/guides/service.py
  - apps/api/app/guides/router.py
  - apps/api/app/guides/schemas.py
  - apps/api/tests/test_guides.py
---

# Paginate guide sitemap before the next large multilingual publication

## Why

The content-pack inventory already reported 836 potential article/locale rows after the large life-content integration on 2026-09-14. Both apps/web/lib/guides.server.ts and apps/api/app/guides/service.py cap the guide sitemap at 1,000 entries. Additional multilingual tutorial publications can exceed that application cap and omit published URLs. This is a repository capacity warning, not a claim that 836 rows are currently public. The AI-news publication verifies its own 110 URLs independently.

## Definition of done

- [ ] Every eligible published translation remains discoverable through a sitemap even when there are more than 1,000 guide entries.
- [ ] Expired, unpublished and hidden content stays excluded; locale alternates and publication dates remain correct.
- [ ] Enumeration remains bounded through pagination or sitemap partitioning and preserves existing failure behavior.

## Steps

- [ ] Confirm live eligible row counts and current API/frontend cap behavior before choosing a compatible pagination design.
- [ ] Implement complete enumeration, test beyond the cap, and validate XML plus existing metadata behavior.

## How to verify

Add focused API and frontend regression coverage with more than 1,000 eligible translations, alongside expired/unpublished fixtures. Run the affected guide tests and sitemap tests, then confirm all published URLs in the resulting sitemap or sitemap index. Do not solve this by bulk publishing draft packs.

## Notes

Filed from the news publication's scoped content lint, recorded in docs/ai-news-2026-ytd/validation.json. The warning counts repository content packs, which must remain distinct from actual publication state. No sitemap implementation changes are part of the news release.
