# Klook direct affiliate products

This integration supplies reviewed outbound booking links, not live prices,
availability, reservations or commission guarantees. The existing Stay22,
Travelpayouts and ordinary hotel links remain independent.

## Enrollment and access

On 2026-09-09 (Asia/Taipei), the signed-in official affiliate account showed
Mokaair / `https://mokaair.com/` with Affiliate ID **134379**. This is a public
tracking identifier, not an API credential. It is deliberately **not a global
application default**: another installation must configure its own account.

The official [text-link tool](https://affiliate.klook.com/zh-TW/my_ads/text_links?type=all)
documents adding `aid` to a `https://www.klook.com` destination and warns that
`s.klook.com` links cannot track. The backend stores the original URL and appends
the configured numeric AID only on a validated clickout. It does not guess tag
parameters or send member IDs, email addresses or private trip identifiers to
Klook. Product/city/module click attribution remains in the site's own logs.

The signed-in [help centre](https://affiliate.klook.com/zh-TW/help/) says activity
search API and product lists are available to designated partners. An inquiry was
submitted through [Contact us](https://affiliate.klook.com/zh-TW/contact_us).
Submission is **not approval** for an activity feed, hotel price API, comparison,
storage rights or booking API. No price adapter is implemented or enabled here.

## What belongs where

| Site surface | Exact reviewed product | Broader discovery |
| --- | --- | --- |
| Hotel booking platforms | A specific hotel's verified Klook hotel page, alongside other platforms | Explicit destination search, never presented as a matched hotel |
| Day trips and experiences | Day tour or attraction ticket with its actual Klook activity ID | Activities for the selected destination |
| Airport transfers | Correct airport and direction; distinguish bus from private transfer | Destination/airport transport entrance |
| Connectivity | Country coverage; exact package duration only when checked | Connectivity entrance for the destination |

The existing catalog has `hotel`, `tour`, `transfer` and `esim` types. Tickets use
the experience category; rail passes must not be invented as airport transfers.
Useful rail-pass or car-rental portals may be reviewed as destination transport
links, but are not new bookable local product types in this change.

Catalog discovery fetches only the selected category. Switching category or city
cancels outdated requests; no quote API or provider test is triggered by browsing.
An empty or unapproved destination link remains absent. This release does not
auto-create broad search links from guessed city slugs.

## Settings and review

1. In system settings, open
   `/zh-TW/admin/settings?provider=klook&field=klook_affiliate_id` and enter the
   approved account's AID. Klook activation is separate from Travelpayouts.
   Leave API credentials and quote policies disabled until written authorization
   and an implemented adapter exist.
2. In the hotel workspace (hotels) or travel-services workspace (other products),
   choose **Klook direct affiliate**. Record enrollment evidence from
   `https://affiliate.klook.com/zh-TW/my_account`, approval and activation. This
   does not transfer Travelpayouts approvals or approve any product.
3. Add a canonical `www.klook.com` exact product URL. Do not paste an AID,
   third-party affiliate code, shortener or nested redirect into the target.
   For a hotel, independently review the matching Klook booking option as well
   as its product offer. Preserve all existing hotel facts and platform options.
4. Review each product and each link separately. Compare the exact hotel name
   and address, or the tour/transfer service identity and relevant package.
   A search result or name-only match is not sufficient hotel identity evidence.
5. If automated HTTP verification is blocked, an administrator may explicitly
   attest to a successful browser review of the same canonical target. The
   checkbox starts unchecked, is tied to the link version, and is audited.
   Attestation does not bypass origin, identity, DNS or unsafe-link checks.
6. Only enable the intended catalog types/cities and reviewed records. Catalog,
   enrollment, product, offer and hotel-platform gates are independent. Editing
   the configured AID invalidates the old enrollment/review context rather than
   reusing another account's approval. Reviews retain the existing 30-day window.

The affiliate generator's Hotel Gracery Shinjuku result (`285841`) initially showed
a device-check page. It completed normally without challenge interaction. The
[final Klook page](https://www.klook.com/zh-TW/hotels/detail/285841-hotel-gracery-shinjuku/)
showed the same hotel name and Kabukicho 1-19-1 street address as the freshly read
[official hotel access page](https://gracery.com/shinjuku/access/). The source
manifest records that identity check; imported option/offer records nevertheless
remain pending until the site's independent admin review. No room price is copied.

## Source manifest and safe rollout

Source records in `docs/klook-products/` contain short original editorial labels,
canonical URLs, observed identity and review limitations. They contain no scraped
prices, stock, photos or copied product descriptions. Sources do not assert a
particular date or package is available, or that every product earns commission.
Eligibility/exclusions and final booking conditions remain subject to the account
and Klook checkout.

Klook activity IDs are the durable candidate identity: for example, the Osaka /
Kyoto tour `3217` is one source, not two invented products. The current product
model has one catalog city, so Osaka is its primary placement and Kyoto coverage
is recorded in source notes. The same restriction applies to KIX bus `18203`.

The dedicated importer defaults to read-only preview and requires explicit apply.
It creates only pending candidates/offers under an existing, matching direct
enrollment; it does not create or approve a brand or change public settings.
Existing identities, reviewed facts, status and other channels must survive
preview, apply and replay unchanged. Resolve any conflict before applying.
Do not replay the general CSV importer over production hotel records: it also
supports updates and is not an add-only operation.

From `apps/api`, using the deployment's normal environment and runtime settings:

```sh
python -m app.travel_services.klook_catalog --manifest ../../docs/klook-products/representative-products-2026-09-09.json
# Only after reviewing the preview and obtaining rollout authorization:
python -m app.travel_services.klook_catalog --manifest ../../docs/klook-products/representative-products-2026-09-09.json --apply
```

The initial package includes 10 activity products (five tours and five airport
transfers), one hotel-platform link, and two manifest-only candidates (Tokyo Disney
tickets and Japan eSIM). The candidates are not database imports; their package
scope still needs review. Missing primary hotel records are reported and skipped,
not recreated from a booking provider. A nonzero exit or `blockers` means no apply.

Before an authorized production rollout: verify the merged SHA and schema,
preserve runtime configuration and backups, configure the correct AID, preview
the exact manifest, then apply it once and verify a zero-addition replay.
Review the pending candidates in the existing admin panels before publication.
No production import, publication, provider activation, booking or paid API
request is part of this development run.

## Verification boundaries

- API tests cover channel separation, safe direct clickouts, review context,
  permissions, version conflicts and additive import/replay behavior.
- Browser tests use explicit API fixtures, not production stock or affiliate
  orders. They cover Klook alongside other hotel platforms, native safe new-tab
  POST, honest external pricing and category-specific discovery in five locales,
  desktop Chromium and Pixel 7.
- Real source checks only establish product identity and described service scope;
  they do not demonstrate that Klook attributed a commission. Confirm attribution
  later in the affiliate dashboard after a legitimate user click/order. Do not
  place a test purchase or fabricate conversions.
