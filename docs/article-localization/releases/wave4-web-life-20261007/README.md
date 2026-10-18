# Completed localization release: wave4-web-life-20261007

12 life articles now have all five published languages. [Content PR #1374](https://github.com/x812033727/travel_scanner/pull/1374) was approved at `a80e9cb55d3174fc0bdfaa56d00ccf580866345c`, integrated with green CI at `271efebb21460a271913623b1913daf7722510d6`, and merged and normally deployed as `c6454463d0eb53e4c8166be0b93a587598c03208`. The original approved content bytes were preserved during main integration. The owner's authorization covered the 13 articles and seven reviewed source corrections; the release used no force or hold bypass.

This record covers 48 new language documents and 6 reviewed zh-TW source corrections, for 54 publication targets. Public acceptance covered 60 pages, 120 original desktop and mobile screenshots, and 180 distinct media files. The two scoped records share one release: 13 articles, 52 new language documents, seven source corrections, 59 targets, 65 pages, 130 screenshots and 187 media files.

## Actual release and preserved attempts

All nine phases completed: prepare, dry-run, backup, isolated rehearsal, drafts, publish-articles, publish-hubs, replay and complete. The consistent backup covered 161 tables, and isolated restoration and replay guards passed. Both publication journals settled with no pending operation; replay created no new versions. Only the release driver's own hold was cleared.

The first prepare process exited 0 while its separate read-only capture exited 1. A corrected read-only capture exited 0 without repeating prepare. The first publication process exited 1 after five committed operations; its capture exited 0. After diagnosing a users-row lock and observing its release through a read-only check, one explicit journal resumption exited 0 with capture 0. It preserved the five completed operations and the original start marker. Original failures and recovery receipts remain preserved; no automatic retry occurred.

The public document bodies and versions, raw media bytes, canonical and hreflang URLs, routes, links and sitemap were checked. Three reviewers personally inspected all 130 original screenshots, including native glyphs and images; there were no unresolved findings. Review covered the captured desktop and mobile views. The mobile Japan table keeps overflow inside its own horizontal viewport; desktop text was visible, and this review does not claim a swipe inspection of mobile text outside that viewport. The site's fixed mobile navigation can overlay initial content in the captured view.

## Source and authoring boundaries

The six reviewed zh-TW corrections remove eight irrelevant AI glossary links without changing their visible words, and correct one Traditional Chinese character. The other six source documents and all 36 original source media files remain unchanged. All 48 translations received independent full-text and native-image review. Details: `docs/article-localization/source-corrections/wave4-web-life-20261007.md`.

The shared 39 source-media guards comprise 38 unchanged originals and one approved Japan SVG replacement. This scope has 36 expected source-media files: 36 unchanged originals and 0 approved SVG replacements. Original provider attempts, local validation failures and final review evidence remain preserved. `evidence.json` retains their receipt hashes.

## Actual link-check result

The global link checks exited 1 in every locale. These results remain recorded as observed:

- zh-TW: global CLI exit 1; selected findings none.
- en: global CLI exit 1; selected findings {"unpublished": 9}.
- ja: global CLI exit 1; selected findings {"unpublished": 9}.
- ko: global CLI exit 1; selected findings {"unpublished": 9}.
- zh-CN: global CLI exit 1; selected findings {"unpublished": 9}.

The life cohort has nine related-target findings in each new locale, covering 36 edges to eight articles whose corresponding locale is unpublished. The published frontend displays those references as plain text rather than a missing-page link; the approved document nodes remain unchanged. The global remaining-language task covers these targets. Japan has no selected findings. The global link backlog remains open.

## Published source guards

| Article | zh-TW public version | Normalized public document SHA-256 |
| --- | --- | --- |
| css-layout-basics | 4 | `a76d6ab42e6485c12cf8dfc2d441c4d55fa2271444d16c36630450e3d2794870` |
| image-formats-compression | 4 | `61a23989db771823bc03ecc966da043d6128f4df4f9b5524dc4ede6fdfbea5a9` |
| responsive-layout-basics | 4 | `df8766b842162180cd0d34e21399e7c8bd8964c58243b2d6f9829a1f42a6f177` |
| search-crawlers-explained | 6 | `9c0eddb1eb5a3b20488e50fd12790b813de07df0d6e0251e8cef45f28a67aa2f` |
| seo-content-cannibalization | 6 | `23597ff42dbca107e5c9fe8f12b00a7958d8a7887f165e05e121aac41ed0c7ed` |
| sitemap-website-submission | 6 | `408b7c6920616b79ad7432771ecafa6df817860f468e8110f159b717916423c9` |
| structured-data-basics | 6 | `68d319da771c574e4cb98dedd07e7199cc6eca108e32fde53f2b2bccc892f241` |
| web-design-project-workflow | 4 | `7f7b44f51743dc55e8699ef76fd221a8e8505a70072e3856d4d5913d59833ddc` |
| web-layout-hierarchy | 4 | `1320b0a496a519123321f8d123fb40d6e8b069a91daf4fe0259ea486793e7835` |
| website-cache-cdn | 4 | `4204060b1fa1b43f7e23a6fd9d59fa6602a579b8cea7d20e39919da25f6a5050` |
| website-color-system | 6 | `371d7de707fbc5ad7cebdbffbe52c82510b22060e07750415e9d289af7c924b3` |
| website-information-architecture | 6 | `7f1a381191f69fb5eee20901a90ef06bb19c09e4123537233b42d625990fb59c` |

`evidence.json` records every published document version, normalized hash and public URL, plus the scoped media hashes and original execution receipts. The independent postpublication audit preserved the previous 44 articles and all 220 public documents. The completion ledger now totals 57 published articles and 228 newly published language documents.

The full snapshot observed at 2026-10-08 20:02 Asia/Taipei contained 1,509 published intel/howto/life articles; 805 articles still lacked 3,220 language documents. These are observed counts, and the remaining localization task stays open.

Only the sanitized README and evidence belong in this release scope. Full snapshots, raw logs, original screenshots and backup evidence remain in private external storage.
