---
id: 2026-09-20-five-language-article-batch-004
title: Five-language article batch 004
status: in-progress
priority: P1
area: docs
owner: codex-article-localization
claimed_at: 2026-09-20T08:53:03Z
created_at: 2026-09-20T08:22:34Z
completed_at:
branch: codex/article-localization-batch-004
depends_on: []
scope:
  - apps/api/app/guides/content/japan-train-disruption-plan.json
  - apps/api/app/guides/content/japan-travel-laundry-guide.json
  - apps/api/app/guides/content/kyoto-cycling-parking-guide.json
  - apps/api/app/guides/content/tokyo-rainy-day-museum-plan.json
  - apps/api/app/guides/content/hong-kong-ferry-tram-day.json
  - apps/web/public/guides/japan-train-disruption-plan
  - apps/web/public/guides/japan-travel-laundry-guide
  - apps/web/public/guides/kyoto-cycling-parking-guide
  - apps/web/public/guides/tokyo-rainy-day-museum-plan
  - apps/web/public/guides/hong-kong-ferry-tram-day
---

# Five-language article batch 004

## Why

Five published travel guides still have only their complete Traditional Chinese
document. Each lacks English, Japanese, Korean and Simplified Chinese, and each
has an editable SVG diagram containing Traditional Chinese labels. The exact
pack and asset paths above do not overlap another open task.

## Definition of done

- [ ] Five complete, independently reviewed documents per article, preserving
      the published source and all existing editorial state.
- [ ] Localized text-bearing diagrams pass visual and glyph review.
- [ ] An exact reviewed bundle installs idempotently; its content PR is merged,
      deployed, and only the missing public locales are published.
- [ ] Twenty new public pages pass desktop/mobile content, image, canonical,
      hreflang and same-language link checks.

## Steps

- [x] Claim five non-overlapping paths and capture a fresh production snapshot.
- [x] Translate twenty missing documents and render twenty localized SVGs.
- [x] Complete hash-bound automated pre-review and read-only link-target checks.
- [x] Independently review all translated text, artwork glyphs and source images.
- [ ] Assemble/install the reviewed bundle, then perform guarded PR and release.

## How to verify

Run `pipeline.py status` on the pinned baseline and all twenty jobs; inspect
the document and render hashes and independent review. Run the bundle
assembler/installer twice, focused guide tests, CI, a production dry-run, and
read-only post-publication database/browser audits on all twenty locales.

## Notes

Read-only production snapshot captured at 2026-09-20T08:23:08Z while deployed
repository HEAD was `80ad55c6a85b7a5635f9763c5837094aa5dbc513` before and
after. Snapshot SHA-256:
`b5c8baac5d10b4205c0ab35a5e52d618fc5c67c325267a4a67abba13d8384593`.
Branch base is `2699a1faf946ba94477873c014ae7d7534b61ebc`; combined baseline
SHA-256 is `0f4b4681059509928a0871c628a75c4ac1cd9dc7088991245111f70c9a1345b5`.
Each selected source document exactly matches its live published version;
all five are active/published and each lacks exactly `en`, `ja`, `ko`, `zh-CN`.
Production locale version is 8 for the train-disruption guide and 6 for the
other four. Full baseline and authoring evidence live outside the repository
at `C:\Users\x8120\.codex\article-localization-batch-004`. No pack or public
asset is changed before independent review.

All twenty jobs are `rendered` with schema/field/token checks and one 1600×900
localized SVG each; automated SVG bounds and overlap checks found no issues.
The pre-review progress report records twenty translated and rendered, zero
reviewed, assembled, imported, published or browser-verified, and zero
article/locale issues. Independent visual sample inspection covered each
article and all four target scripts, but is not editorial approval. Each of
the five hero images is an unchanged AI conceptual raster, with its translated
non-photograph disclosure in the new locale; diagrams have translated text.

Initial pre-review validation SHA-256:
`8da9540920ccb30e13e5f70647cffa3b3924dd533390dd7eafe986f8ba9dbf88`.
Its twenty rows bind source document, pack, translated document, SVG and render
hashes. The current manual correction log SHA-256 is
`b56189ede65e9bd9a324641d2c0fbde181dabeadf46f7eef5eea1b0c0de56a85`;
it records two Korean number-word fixes, twenty hero credit disclosures,
four same-locale Tokyo links and the three later reviewer fixes. The read-only route-check SHA-256 is
`f002768c85ff6a82ba44585f39e2728e05e25d81ab77c992bb565dd4d788dc65`:
the four target-language Tokyo city pages and four Cheung Chau guide pages
returned HTTP 200 with substantive localized headings. Other ArticleInline
targets were zh-TW-only at the snapshot and must stay plain text in new
locales until those targets are published. Source and URL publication states
must be rechecked before assembly and release.

The localization pipeline's 27 Python tests, 14 artifact integrity tests,
3 layout tests and `check:tasks` passed. The five pack and public image paths
remain unchanged; no review, PR, import or publication has been claimed.

Independent review later requested three field-level corrections in the four
non-Hong Kong guides: the laundry ja/ko checklist now says collect clothes,
check dryness, then pack; train-disruption ko now uses the broader `열차` in
its title. Each corrected job was rematerialized, its previously documented
localized AI credit reapplied, and its SVG rerendered. The other seventeen
jobs' six core file hashes remained byte-identical. Current pre-review SHA-256
is `e5274d483fb1ac15625a8bf9703e3b976bb26c89757f4a31a886f1a4d31d9355`;
the unaffected-job comparison SHA-256 is
`046b0c286470bf543d440feda4fb559a81f0b0e2b1752fbc0cbae7a40f9312c4`.
All sixteen new-locale documents for the four non-Hong Kong guides subsequently
received independent hash-bound review. Hong Kong remains held because its
published source needs a luggage-rule correction in a separate task/PR.

The four reviewed Japan guides are installed idempotently from release manifest
`c7c85a4dcf2c2735009f0cbfa924e08ee50bbfa26a9091c7daf4f9d70cb2e9b9`.
The external installation journal SHA-256 is
`0293a365ddfa68c8ca38ab27afa98fc9bceddfcb435184b0bb219cbd76e1a8a8`.
This PR carries only those four packs and sixteen localized SVGs. The four
existing hero images are byte-identical references. Hong Kong will be handled
after its corrected source is published and its four translations are rebased.
Hong Kong ferry/tram was held until source PR #590 was merged and the live zh-TW
locale republished at version 8, normalized SHA-256
`e59b60f8ca4b19233820cc03e9126ddb0c4a29c70b06bed79ec43a3e359c5efa`.
Four rebased jobs were independently reviewed against that source, including the
7 kg OR 30 L rule, motorman discretion, alternate transport, attribution, links
and 1600x900 SVG renders. The hash-bound handoff SHA-256 is
`621e2ccbba95cab440aaae5de3a52011bfe4051afa7b70b84f08148cc7a4f0dd`;
all four reviews pass `assemble_bundle.reviewed_document`. The single-article
reviewed release bundle is staged outside the repository with manifest SHA-256
`69d1bd84d1713492292472b8ef17cd78a0c27a8de410a8f055b2fe834bc9f02b`.
Its repository pack retains the original metadata and zh-TW JSON unchanged and
adds only en, ja, ko and zh-CN plus their four localized diagrams. Merge,
deployment, publication and browser verification remain outstanding.
The four-locale content PR is #595; it does not perform publication.
