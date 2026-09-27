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

### 2026-09-24 placement plan, ready before the links exist

Prepared while the ticket waits on the owner, so that the owner's links are the only
missing piece. Rule, from decision D2 in `docs/monetization-alternatives.md`:

- Link only the brand the article teaches, once per locale.
- Put the link at the end of the section where the reader decides what to buy. It goes after
  a paragraph and before the next section's heading.
- Nothing in the article text changes.

The five locales of every pack below have identical block structures (checked 2026-09-24), so
one index works for all of them. Insert the new block at 0-based position `after + 1` in
`locales.<locale>.blocks`.

| Pack | Batch | After block | Before the heading (zh-TW / en) |
| --- | --- | --- | --- |
| `hostinger-wordpress-setup` | 1 | 4 | 從 Websites 新增 WordPress / Add WordPress from Websites |
| `siteground-wordpress-setup` | 1 | 4 | 新網站依設定精靈建立 / Create a new website with the setup wizard |
| `hosting-com-wordpress-setup` | 1 | 7 | cPanel 與 Webuzo 依自己的入口安裝 / Install through your own cPanel or Webuzo |
| `namecheap-domain-setup` | 1 | 1 | 在 Domain List 確認你要管理的網域 / Find the domain you want to manage in Domain List |
| `fastcomet-wordpress-setup` | later | 9 | 用 Softaculous 建立新站 / Create a new site with Softaculous |
| `hostgator-wordpress-setup` | later | 4 | 從客戶入口建立 WordPress / Create WordPress from the customer portal |
| `bluehost-wordpress-setup` | later | 4 | 從 Websites 建立正確的 WordPress 網站 / Create the correct WordPress site from Websites |
| `bluehost-domain-billing` | later | 7 | 註冊前核對拼法，完成後再驗證 / Check spelling before registration, then verify |
| `cloudways-wordpress-setup` | later | 7 | 依網站工作選擇伺服器 / Choose a server for the work your website does |
| `cloudways-ssl-setup` | none | | Written for people who already run Cloudways; no buying step, zh-TW only |
| `managed-hosting-comparison` | only if both | 20 | 用取捨說明選擇，保留重新評估時點 / Explain the trade-offs and set a review date |

- **The comparison** names FastComet and Cloudways only as examples (twice each). Link both, or
  neither: only when both programmes are joined, as two blocks. Two links stay within the
  three-per-article limit.
- **`namecheap-domain-setup`** is for readers who already registered, so its purchase intent is
  low. The link sits right after the introduction, for readers who still need a domain.
- **Generic domain guides are not candidates.** For example, `domain-registration-guide`,
  `domain-registrar-transfer` and `gandi-domain-management` do not teach Namecheap, and D2 keeps
  a brand link out of an article about something else. This replaces the earlier note that
  called them candidates.

**Block text.** `label` is at most 80 characters and `note` at most 200. The component adds
the badge (合作連結 / Affiliate link …) and the brand name, and the article's opening
disclosure switches to `partnerDisclosure` automatically. Hosting brands:

| Locale | `label` | `note` |
| --- | --- | --- |
| zh-TW | 到 {Brand} 官網查看主機方案 | 先照上面的清單核對需求，再比較首期與續約價格。 |
| zh-CN | 前往 {Brand} 官网查看主机方案 | 先按上面的清单核对需求，再比较首期与续约价格。 |
| en | See {Brand} hosting plans | Check your needs against the list above, then compare the first-term and renewal prices. |
| ja | {Brand} の公式サイトでプランを見る | 上のリストで必要な条件を確認してから、初回と更新時の料金を比べてください。 |
| ko | {Brand} 공식 사이트에서 요금제 보기 | 위 목록으로 필요한 조건을 먼저 확인한 뒤, 첫 결제와 갱신 가격을 비교하세요. |

Namecheap (after the introduction):

| Locale | `label` | `note` |
| --- | --- | --- |
| zh-TW | 還沒有網域：到 Namecheap 查詢 | 註冊前先確認拼法、持有人資料與續約價格。 |
| zh-CN | 还没有域名：到 Namecheap 查询 | 注册前先确认拼写、持有人资料与续费价格。 |
| en | No domain yet? Search on Namecheap | Before registering, check the spelling, the owner details and the renewal price. |
| ja | ドメインがまだなら Namecheap で検索 | 登録前に、つづり・登録者情報・更新料金を確認してください。 |
| ko | 도메인이 아직 없다면 Namecheap에서 검색 | 등록 전에 철자, 소유자 정보, 갱신 가격을 확인하세요. |

These strings still go through the per-locale review in skill `content-pipeline`. They are
a draft, not a reviewed translation.

**Owner's sign-up checklist, batch 1.** The official pages are in section 9 of the document.

1. For each of Hostinger (affiliate programme), SiteGround, hosting.com (FirstPromoter) and
   Namecheap (Impact):
   - Apply on the official affiliate page.
   - Promoting site: `https://mokaair.com`.
   - Method: content website with tutorials; no paid search and no brand-keyword ads.
2. Payout and tax:
   - PayPal is the simplest everywhere.
   - Impact pays by wire in TWD.
   - US programmes ask for a W-8BEN; the owner signs it personally.
3. Once approved, generate one link to the brand's home or plans page and send the full URL.
   Do not send Hostinger's `REFERRALCODE` customer-referral link: its terms forbid websites,
   and `content_links.py` rejects it.
4. Then: `npm run tasks -- status 2026-09-24-hosting-affiliate-links-in-the-hosting open`.
