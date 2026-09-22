# Five-language guide releases — 2026-09-22

This directory is the shareable evidence record for two completed article-localization releases:

| Batch | Public scope | Merged commit | Published operations | Public QA |
| --- | --- | --- | ---: | --- |
| 010 | Two Singapore guides, five locales each | `d52af4d95a40f5e353c567d366ee1b2b69dc5696` | 10 drafts, 10 article publications, 0 hubs | 10 HTML pages and 20 desktop/mobile browser cases passed |
| 011 | Jeju car-rental guide, five locales | `222a6a0d385eae989c0736ae8ace2a0df066f1f1` | 5 drafts, 5 article publications, 0 hubs | 5 HTML pages and 10 desktop/mobile browser cases passed |

Each batch directory contains a compact `release-evidence.json` plus the exact small JSON review receipts that bind editorial, source-correction, numeric, structural and SVG decisions to content hashes. Production database snapshots, deployment logs, credentials and browser screenshots are deliberately excluded.

## Batch 010: Singapore

PR [#635](https://github.com/x812033727/travel_scanner/pull/635) has zero GitHub review objects. That fact must not be read as “zero independent review.” Before publication, the exact five-language content was approved by an independent editorial receipt, both zh-TW source corrections were independently approved, and all final numeric warnings were independently classified. The final release bundle then received a separate topics-order-only equivalence review.

The Changi fare correction is explicit: 39.3–40.2 km belongs to the 256/206-cent band, and 257/207 cents applies only above 40.2 km. The final numeric receipt approves 115 of 115 warnings as equivalent and records zero blockers. The earlier 112-warning classifier was an intermediate return-to-author artifact.

The two English SVG slot omissions and four condensed-duration questions named in merged task-only PR [#639](https://github.com/x812033727/travel_scanner/pull/639) were likewise intermediate findings. V5 restored “Singapore in 4 days” and “trains to the city,” and independently reviewed the duration fields. The public `/foods?city=singapore` URLs are correctly localized for all five languages; the earlier pipeline message meant “route needs review,” not that the public link was broken.

PR [#647](https://github.com/x812033727/travel_scanner/pull/647) was opened after the completed release but describes the earlier pre-release state. Its claims that nothing is live, no independent editorial review exists, the source correction is unapproved, and the numeric/SVG/eligibility gates remain open are superseded by [batch010-singapore/release-evidence.json](batch010-singapore/release-evidence.json) and the receipts beside it. Its narrower statement that #635 has no GitHub review objects is accurate.

## Batch 011: Jeju

PR [#643](https://github.com/x812033727/travel_scanner/pull/643) released `jeju-car-rental-guide` only. The reviewed zh-TW correction and four translations were hash-bound before publication; the four localized LF SVG blobs and desktop/mobile scroll renders received an independent byte and visual review. Nami and Seoul were excluded from the release.

The initial offline package and the deployed Git pack differed only in topic ordering. The final v2 receipt proves that all five documents, eight assets, source review and baseline were unchanged, while the resulting `ArticlePack` model matches the merged Git content.

## Evidence boundaries

The JSON records describe the exact releases and verification completed on 2026-09-22. A later content edit, locale revision or asset change needs its own evidence. The public URLs are listed in each batch record so status can be checked without reconstructing locale paths.
