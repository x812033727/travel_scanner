---
id: 2026-09-21-taiwan-zh-tw-batch-005-entry
title: Taiwan zh-TW batch 005: entry and connectivity
status: done
priority: P1
area: docs
owner: codex-taiwan-zh-tw-batch005
claimed_at: 2026-09-21T16:17:41Z
created_at: 2026-09-21T16:17:30Z
completed_at: 2026-09-21T16:48:24Z
branch: codex/taiwan-zh-tw-batch-005
depends_on: []
scope:
  - apps/api/app/guides/content/taiwan-entry-2026-arrival-card.json
  - apps/api/app/guides/content/taiwan-esim-sim-wifi.json
  - apps/web/public/guides/taiwan-entry-2026-arrival-card/diagram-1-zh-tw.svg
  - apps/web/public/guides/taiwan-esim-sim-wifi/diagram-1-zh-tw.svg
---

# Taiwan zh-TW batch 005: entry and connectivity

## Why

The next two published Taiwan guides in the original launch order still expose
English, Japanese, Korean, and Simplified Chinese but no Traditional Chinese
document. Add complete `zh-TW` versions without changing the four existing
locales, publication metadata, provenance, visibility, or licensing.

## Definition of done

- [x] `taiwan-entry-2026-arrival-card` has a complete native-quality `zh-TW`
  `GuideDocument` and a matching Traditional Chinese entry-flow diagram.
- [x] `taiwan-esim-sim-wifi` has a complete native-quality `zh-TW`
  `GuideDocument` and a matching Traditional Chinese connectivity diagram.
- [x] Reader-visible official sources support changing entry, customs,
  eligibility, carrier, counter, and device-compatibility claims.
- [x] Existing locale documents and top-level pack metadata remain unchanged.
- [x] Both SVGs render cleanly at 1600x900 and 390x219.
- [x] An independent fact/content review has no unresolved blocker or major
  finding, and focused checks pass after its findings are resolved.

## Steps

- [x] Revalidate the repository and public API baselines and confirm that both
  selected guides are published in four locales but lack `zh-TW`.
- [x] Write the complete Traditional Chinese documents with explicit
  nationality and eligibility scope and same-language internal links.
- [x] Create original `zh-TW` SVG diagrams and verify their text against the
  document claims and numbers.
- [x] Run schema, target-locale, number-parity, source-reachability, API pack,
  tooling, task, diff, and desktop/mobile render checks.
- [x] Resolve independent-review findings, rebase onto current `origin/main`,
  prove content hashes are unchanged, and record the final checks.

## How to verify

```text
cd apps/api
uv run pytest tests/test_guides_pack_ingest.py tests/test_guide_rich_blocks.py tests/test_guides_content_pack.py
cd ../..
npm run test:tools
npm run check:tasks
git diff --check
```

Run `pack_cli lint` for both exact slugs, the target-only structural and number
parity check, and the source-reachability check. Render each localized SVG in
Chromium at 1600x900 and 390x219 and inspect all four PNGs.

## Notes

- Production was inspected through read-only public API requests. At the
  baseline snapshot, each guide had published `en`, `ja`, `ko`, and `zh-CN`
  documents and no published or stored `zh-TW` document. Production overlays
  differ from repository copies, so the new locale follows the live document
  structure while preserving every repository locale byte-for-byte.
- Entry guidance distinguishes TWAC, visa-free entry, e-Gate eligibility,
  Mainland Chinese, Hong Kong/Macao, customs declarations, medicine, and
  tobacco-product rules. Connectivity guidance distinguishes eSIM support,
  double-identification rules, tourist plans, promotional plans, payment, and
  counter hours instead of implying one rule or price applies to everyone.
- Official NIA, BOCA, Customs, APHIA, MOHW, Chunghwa Telecom, Taiwan Mobile,
  Far EasTone, Apple, and airport pages were checked on 2026-09-22. Two official
  Taoyuan Airport pages return HTTP 403 to automated requests through their
  Cloudflare protection; the reader-visible URLs remain official sources.
- Full pack lint reports pre-existing shared entry-diagram findings for other
  locales and an English length warning. The new entry locale has no target
  finding. The eSIM target has only the pack's existing `no_summary` warning,
  shared by all of its locales; its block structure deliberately preserves
  parity rather than adding a new summary-only shape.
- Focused API tests: 51 passed, 7 skipped. Tool tests: 75 passed, 1 skipped.
- Independent review found one major omission in the 14-day visa-exemption
  conditions and three minor source/wording issues. The document now names the
  Thai/Philippine ordinary-passport limit, Brunei passport/CI limit and
  diplomatic/official-passport exclusion, plus the three countries' booking,
  Taiwan-contact, and financial-evidence requirements. The Taiwan Mobile source
  now uses its Traditional Chinese page; the Taipei Free and third-party eSIM
  sentences now stay within their cited evidence. The reviewer rechecked all
  four changes and reported no remaining blocker, major, or minor finding.
- Final pre-rebase canonical document SHA-256 values: entry
  `102740432014b284fb0761e26bc5cc9c138af5412c3ed2a92e2e2e465bf03396`;
  eSIM `bec3082749af3a93a0a11208930e481100d2f09e128728789bca46f2ee6acf40`.
  Raw SVG SHA-256 values: entry
  `fc6695b3fc73b380eaa390eae578f7d578c485f6a22a75429706b1016a01c94f`;
  eSIM `ff6c61b512c0aecd0630c57c525772a9eae26ce62db42e02298c284b17770691`.
- `origin/main` remained at the starting baseline
  `f33005805c031ba2dad6d7c2268760f6f67dbc97` after the final fetch, so the
  required rebase is a no-op; verify the hashes again after the final commit.
