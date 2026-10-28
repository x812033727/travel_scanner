# Ansoff and BCG localization release — 2026-10-28

Eight reviewed English, Japanese, Korean and Simplified Chinese documents are
published for `ansoff-growth-options` and `bcg-portfolio-review`. Each new locale
is public v2. Both existing Traditional Chinese documents remain public v4;
their complete locale rows and six original asset files are unchanged.

Status: released and accepted. Twenty original screenshots passed independent
visual review; the managed hold is cleared and the final host verification passed.

The owner explicitly authorized backup, deployment and publication of these
eight documents. This release is separate from the older seventeen-article wave
and does not complete the wider localization backlog.

- Content PR: [#1901](https://github.com/x812033727/travel_scanner/pull/1901).
- Deployed commit: `b78895e5fad1285d68a49a9e059eb318b846e40d`.
- Native manifest: `5717849d1e3407a3dd1fe762a96067236837562aed3fc8c1faeb575c160668d1`.
- Completed production journal: `6fb04aa0ac7193278340ebe41bfda5517f79b09c9b2afabe9e3ada7d20d3540d`.

| Gate | Actual result |
| --- | --- |
| Full database backup | 565,854,427 bytes; dump exit 0; readable archive |
| Actual isolated restore | Restore exit 0; retained for recovery |
| Restored-database publication | 8 drafts, 8 publications, 0 hubs; 16 new revisions and 16 audit rows |
| Isolated preservation and replay | Protected data across 167 tables unchanged; whole 167-table rowsets identical after four successful replay phases |
| Deployment | Native exit 0, three consecutive healthy checks, two runtime packs and 24 new assets matched |
| Fresh production guards | Reviewed source versions, hashes, visibility, holds and actor matched |
| Production publication | Completed 06:22:28 UTC; 8 drafts, 8 publications, 0 hubs; all four replay phases exited 0 |
| Public HTTP acceptance | 10 exact documents, 24 new assets plus 4 public source images, complete API/XML sitemap chains; 58 requests returned 200 |
| Actual browser acceptance | 10 pages, 20 original desktop/mobile screenshots; all seven automated checks passed |
| Independent visual acceptance | Two reviewers actually viewed all 20 original captures and 49 native crops; no blocking finding |
| Managed-hold closure and final host verification | Own hold cleared after fresh readback; unmodified verifier: 11 PASS, 0 FAIL |

Backup SHA-256:
`0231347ceed6970b9baf6f90159c8fd9cfdd1569e910d4bc276841dbd8de7993`.

The browser closed its context and browser and drained all route tasks before
sealing evidence. All 103 actual HTTP requests returned 200. Six optional
requests were cancelled before fetching; they are recorded separately and are
not counted as HTTP successes. Original raw DOM, unreviewed captures and sealed
reports remain preserved. An offline inert-DOM audit passed for all ten bodies.

The official link graph rebuild dry-run and application succeeded. The five
global link checks retained existing findings. Four added findings are reviewed
references to an unpublished same-language article: the actual API marks those
references unavailable and all four rendered pages retain their text without a
live link. There are no unexpected added findings; this is not a claim that the
entire site's link backlog is resolved.

| Locale | Ansoff | BCG |
| --- | --- | --- |
| Traditional Chinese | [v4](https://mokaair.com/zh-TW/life/ansoff-growth-options) | [v4](https://mokaair.com/zh-TW/life/bcg-portfolio-review) |
| English | [v2](https://mokaair.com/en/life/ansoff-growth-options) | [v2](https://mokaair.com/en/life/bcg-portfolio-review) |
| Japanese | [v2](https://mokaair.com/ja/life/ansoff-growth-options) | [v2](https://mokaair.com/ja/life/bcg-portfolio-review) |
| Korean | [v2](https://mokaair.com/ko/life/ansoff-growth-options) | [v2](https://mokaair.com/ko/life/bcg-portfolio-review) |
| Simplified Chinese | [v2](https://mokaair.com/zh-CN/life/ansoff-growth-options) | [v2](https://mokaair.com/zh-CN/life/bcg-portfolio-review) |

The Simplified Chinese BCG desktop capture ends before the bottom copyright
strip; the corresponding mobile capture includes it. Article content and figures
were inspected. This capture boundary is preserved in the visual receipt.

Sanitized document, asset, screenshot and receipt hashes are in [evidence.json](evidence.json).

Full private receipts, snapshots, journals, logs and original screenshots are
retained outside the repository. Only sanitized hashes, counts and public URLs
belong in this release directory.
