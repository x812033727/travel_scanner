---
id: 2026-11-10-news-first-party-lab-example
title: Prepare evidence-backed lazy loading field test article
status: done
priority: P2
area: docs
owner: codex-news-lab-coordinator
claimed_at: 2026-11-10T13:02:24Z
created_at: 2026-11-10T13:02:22Z
completed_at: 2026-11-10T13:27:45Z
branch: codex/mokaair-news-layout-20261110
depends_on: []
scope:
  - docs/news-reader-enhancements/lazy-loading-lab
---

# Prepare evidence-backed lazy loading field test article

## Why

More attractive news needs real reader value. A first-party experiment must contain
observable evidence, rather than relabelled third-party claims or invented results.
This task prepares one reproducible experiment and a reviewed article preview.

## Definition of done

- [x] Execute the declared local experiment and retain requests, geometry, screenshots and hashes.
- [x] A different author writes a useful zh-TW tutorial; an independent reviewer checks its claims.
- [x] The preview distinguishes observations, documented explanations and untested suggestions.
- [x] Public evidence passes path/privacy hygiene with transparent derived receipts.
- [x] Preview the structured draft in the actual article layout on desktop and mobile.

## Steps

- [x] Use 20 original SVGs, eager/lazy/disabled-script conditions, two viewports and three repetitions.
- [x] Complete 18/18 browser cases and 165/165 evidence consistency checks.
- [x] Write a structured draft and Markdown; independently compare all six result rows and official sources.
- [x] Improve first-use terminology and move internal verification detail to author notes.
- [x] Integrate the public bundle and read back its exact-byte provenance.

## How to verify

Copy the committed evidence folder to a disposable local directory before running the
experiment verifier, which writes its result files. Validate draft.json with
GuideDocument. Compare the independent review hashes and all result rows. Run repository
hygiene; preview the same structured draft in the real local article component.

## Notes

2026-11-10: Edge 157.0.4341.42 on Windows arm64, headless; CSS viewports 1440x900 and
390x844, not physical phones. Initial eager and scripting-disabled groups loaded 20/20;
lazy with scripting enabled loaded 2/20, including one offscreen image. Every group
loaded 20/20 after complete traversal. No page-speed, bandwidth-saving, LCP, SEO or
cross-browser effect was measured. No paid service, user account or production write.

The v2 article and GuideDocument independently passed full rereading, original-result
comparison and JSON-to-Markdown reproduction. Original article SHA-256 starts c5d1921a;
draft starts dbc15e22. The old v1 text was not retained, so no exact v1-v2 diff is claimed.
This is a content preview with reproducible evidence, not an ingested/published pack.

The public derivative strips individual workstation paths and rebinds the affected
metadata chain; it is explicitly not a new experiment. All original measurements,
request logs, fixtures and article bytes remain unchanged. Independent review and root
both verified 71 manifest entries. The original verifier ran 165/165 checks on the
publication candidate; 58 text files passed the repository's actual hygiene matcher.
Full original and intermediate receipt identities are distinguished in PUBLICATION-REBIND.md.

The real production-build article component rendered the reviewed draft at desktop,
390px and 320px. Title, table and code were captured; horizontal table/code scroll
reached the exact right edge without document overflow. Final shared browser evidence
contains 35 page states, 63 PNGs and zero page errors; independent visual review passed.
