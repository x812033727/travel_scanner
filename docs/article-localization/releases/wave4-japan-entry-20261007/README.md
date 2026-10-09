# Completed localization release: wave4-japan-entry-20261007

The Japan entry intel article now has all five published languages. [Content PR #1374](https://github.com/x812033727/travel_scanner/pull/1374) was approved at `a80e9cb55d3174fc0bdfaa56d00ccf580866345c`, integrated with green CI at `271efebb21460a271913623b1913daf7722510d6`, and merged and normally deployed as `c6454463d0eb53e4c8166be0b93a587598c03208`. The original approved content bytes were preserved during main integration. The owner's authorization covered the 13 articles and seven reviewed source corrections; the release used no force or hold bypass.

This record covers 4 new language documents and 1 reviewed zh-TW source correction, for 5 publication targets. Public acceptance covered 5 pages, 10 original desktop and mobile screenshots, and 7 distinct media files. The two scoped records share one release: 13 articles, 52 new language documents, seven source corrections, 59 targets, 65 pages, 130 screenshots and 187 media files.

## Actual release and preserved attempts

All nine phases completed: prepare, dry-run, backup, isolated rehearsal, drafts, publish-articles, publish-hubs, replay and complete. The consistent backup covered 161 tables, and isolated restoration and replay guards passed. Both publication journals settled with no pending operation; replay created no new versions. Only the release driver's own hold was cleared.

The first prepare process exited 0 while its separate read-only capture exited 1. A corrected read-only capture exited 0 without repeating prepare. The first publication process exited 1 after five committed operations; its capture exited 0. After diagnosing a users-row lock and observing its release through a read-only check, one explicit journal resumption exited 0 with capture 0. It preserved the five completed operations and the original start marker. Original failures and recovery receipts remain preserved; no automatic retry occurred.

The public document bodies and versions, raw media bytes, canonical and hreflang URLs, routes, links and sitemap were checked. Three reviewers personally inspected all 130 original screenshots, including native glyphs and images; there were no unresolved findings. Review covered the captured desktop and mobile views. The mobile Japan table keeps overflow inside its own horizontal viewport; desktop text was visible, and this review does not claim a swipe inspection of mobile text outside that viewport. The site's fixed mobile navigation can overlay initial content in the captured view.

## Source and authoring boundaries

The reviewed source correction changes ten exact document pointers, one visible SVG `text` label and one SVG `desc` accessibility description. The source cutoff and unrelated citation dates remain unchanged. The approved exception changes `/sources/8/checked_on` from 2026-09-13 to 2026-10-07 together with its verified Customs URL and title. Both original photographs retain their original SHA-256 bytes. The single source SVG uses the approved replacement. The four translations received independent full-text and native-image review, including a repair to English card and arrow padding. Details: `docs/article-localization/japan-entry-source-review-20261007.md`.

The shared 39 source-media guards comprise 38 unchanged originals and one approved Japan SVG replacement. This scope has 3 expected source-media files: 2 unchanged originals and 1 approved SVG replacement. Original provider attempts, local validation failures and final review evidence remain preserved. `evidence.json` retains their receipt hashes.

## Actual link-check result

The global link checks exited 1 in every locale. These results remain recorded as observed:

- zh-TW: global CLI exit 1; selected findings none.
- en: global CLI exit 1; selected findings none.
- ja: global CLI exit 1; selected findings none.
- ko: global CLI exit 1; selected findings none.
- zh-CN: global CLI exit 1; selected findings none.

The life cohort has nine related-target findings in each new locale, covering 36 edges to eight articles whose corresponding locale is unpublished. The published frontend displays those references as plain text rather than a missing-page link; the approved document nodes remain unchanged. The global remaining-language task covers these targets. Japan has no selected findings. The global link backlog remains open.

## Published source guards

| Article | zh-TW public version | Normalized public document SHA-256 |
| --- | --- | --- |
| japan-entry-2026-visit-japan-web | 8 | `4709f8e36b080bc76a1703704db2744b28409fcc31289eebf5c3105c7ca3f3c5` |

`evidence.json` records every published document version, normalized hash and public URL, plus the scoped media hashes and original execution receipts. The independent postpublication audit preserved the previous 44 articles and all 220 public documents. The completion ledger now totals 57 published articles and 228 newly published language documents.

The full snapshot observed at 2026-10-08 20:02 Asia/Taipei contained 1,509 published intel/howto/life articles; 805 articles still lacked 3,220 language documents. These are observed counts, and the remaining localization task stays open.

Only the sanitized README and evidence belong in this release scope. Full snapshots, raw logs, original screenshots and backup evidence remain in private external storage.
