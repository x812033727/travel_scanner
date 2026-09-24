---
id: 2026-09-24-hosting-affiliate-links-in-the-hosting
title: Hosting affiliate links in the hosting setup guides
status: blocked
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-24T00:30:02Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/affiliates/content_links.py
  - apps/api/tests/test_guide_partner_links.py
  - apps/api/app/guides/content/bluehost-domain-billing.json
  - apps/api/app/guides/content/bluehost-wordpress-setup.json
  - apps/api/app/guides/content/cloudways-ssl-setup.json
  - apps/api/app/guides/content/cloudways-wordpress-setup.json
  - apps/api/app/guides/content/fastcomet-wordpress-setup.json
  - apps/api/app/guides/content/hostgator-wordpress-setup.json
  - apps/api/app/guides/content/hosting-com-wordpress-setup.json
  - apps/api/app/guides/content/hostinger-wordpress-setup.json
  - apps/api/app/guides/content/managed-hosting-comparison.json
  - apps/api/app/guides/content/namecheap-domain-setup.json
  - apps/api/app/guides/content/siteground-wordpress-setup.json
---

# Hosting affiliate links in the hosting setup guides

## Why

The site has step-by-step setup guides for eight hosting and domain brands, ten of the
eleven in all five locales (list in `scope`). A reader of "set up WordPress on X" is about
to buy X, which is the highest purchase intent anywhere on the site. Yet none of the 1,117
packs uses a `partner_link` block, and only Hostinger (plus 博客來) is registered in
`CONTENT_PARTNERS` (`apps/api/app/affiliates/content_links.py:51`).

One hosting sale pays more than months of display advertising at the site's traffic
(`docs/monetization-alternatives.md`, section 5). The mechanism already exists and needs
no third-party script: `partner_link` renders a direct `rel="sponsored"` link with a badge
and counts the click first-party (PR #450).

**Blocked on the owner**: joining the programmes is personal (tax forms, payout details), so
it cannot be done here. Section 4.2 of the document recommends SiteGround, Namecheap and
hosting.com, plus the already-registered Hostinger (decision D1, section 7). Bluehost,
HostGator and Cloudways are left for later: at this traffic a single sale would likely
never reach their payout threshold. Move this ticket to `open` once the owner has joined
at least one programme and has a real tracking link from its dashboard.

## Definition of done

- [ ] Each programme the owner joined is a `ContentPartner` whose `hosts` match the links
      its dashboard actually generates (tracking domains included; never guessed).
- [ ] The guide for that brand carries one `partner_link` per locale, where the guide
      tells the reader to sign up, with the owner's real link.
- [ ] The published pages show the link with its badge in all five locales, and a click
      writes an `affiliate_clicks` row with `sub_id` starting `cnt_` and the article slug.

## Steps

- [ ] Owner: join the programme, register mokaair.com as the promoting site, send one
      generated link per brand.
- [ ] `content_links.py`: one `ContentPartner` per programme; `tracking_params` or
      `tracking_path_prefixes` from the real link; any referral-only link form the terms
      forbid goes in `forbidden_params`, as Hostinger's does. Tests in
      `tests/test_guide_partner_links.py`.
- [ ] Packs: add the block in every locale of the brand's guide. The block limit is three
      per article. Follow skill `content-pipeline` for the edit, the per-locale review and the
      post-deploy `guides-import`; the pack text itself does not change.
- [ ] `managed-hosting-comparison`: link every compared brand that has a joined programme,
      or none. Linking some brands and not others makes the comparison read as bought.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guide_partner_links.py -q
```

After import on production: open the brand's guide in each locale, the badge shows;
click it in a real browser (the click report is a keepalive `fetch`, which `curl` does not
exercise) and check the admin affiliate report's by-article row.

## Notes

- Deploy the API and web together: `isPublishedGuide` rejects a whole article with a block
  type it does not know (already true for `partner_link` since PR #450, so only relevant if
  the block shape changes).
- Terms per programme (commission, cookie, Taiwan eligibility, tracking host) are in the
  document's section 4.2, read 2026-09-24. Re-read them before joining.
- Hosts seen in the programmes' own docs, still to be confirmed against the owner's real links:
  - SiteGround: `siteground.com/go/...` redirects to regional subdomains, so the
    `siteground.com` host with subdomain matching covers it.
  - Namecheap: `namecheap.pxf.io` (Impact) or `www.anrdoezrs.net` (CJ).
  - hosting.com: stays on `hosting.com` with `?fpr=`.
  - Impact dashboards can issue other domains; copy the host from the dashboard.
- Namecheap pays on domains too, so the domain guides are candidates once the brand
  guides are done. Nine packs have `domain` in the slug; two of them are in this scope.
  The other seven are not; add them in a follow-up.
