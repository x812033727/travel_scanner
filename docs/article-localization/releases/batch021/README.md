# Batch021: household purchasing guides

Two previously Traditional-Chinese-only lifestyle articles now provide complete
English, Japanese, Korean and Simplified Chinese documents. Eight new localized
SVG diagrams accompany those translations; both existing Traditional Chinese
documents and four original image files remain unchanged.

Content PR: [#687](https://github.com/x812033727/travel_scanner/pull/687).
The content PR was already merged before this release executor continued. The nine checks passed for exact content head `27e8ec56e5e88cdad94bb83d2950c13d544d3001`.
Its full Git tree matches deployed merge `e4476b843d43eaa603737b2adef270dfa0368e1c`.

| Article | Slug | Content | Draft import | Public publication | Browser verification |
| --- | --- | --- | --- | --- | --- |
| 買新 3C 前先寫需求：從真實問題、相容性到維修與退場成本 | `gadget-purchase-needs-checklist` | Complete | 4 new locales | 5 languages | Desktop + mobile |
| 家裡用品一直重複買？用簡單庫存表記位置、數量與補貨狀態 | `household-inventory-spreadsheet` | Complete | 4 new locales | 5 languages | Desktop + mobile |

The gadget article remains at version 1 and the household-inventory article remains
at version 2; both full zh-TW version 6 rows are unchanged. Eight missing locales
were created and then published at version 2.
Category, ordering, visibility, expiry and original publication timestamps were
preserved. The explicit dry run selected 8 translation starts, 8 article
publications and zero hub publications. All 16 commits are sealed in the accepted
journal, with no pending operation and no duplicate publication.

A fresh custom-format database backup passed `pg_restore --list` before deployment.
The guarded hostinger2 deployment, import, publication, three consecutive service
health checks, actual database/journal acceptance and public browser verification
completed. Final evidence was staged before the owned deployment hold was cleared.
The post-clear snapshot confirms the exact clean deployed revision and healthy services.

Public acceptance covers 10 language URLs, 20 desktop/mobile cases and 40 actual
top/diagram screenshots independently viewed. Full body, headings, expanded AI
illustration disclosures, sources, original URLs, same-language internal links,
canonical and reciprocal hreflang checks passed. All 12 public image files match
their frozen bytes. Sitemap API pages contain [1000, 968], totaling
1968 unique rows; all API article URLs are covered by XML.

The known desktop global search placeholder/icon overlap remains tracked separately
in task `2026-09-22-fix-desktop-global-search-placeholder-icon`. Browser viewport
checks are not physical-device acceptance. Mobile diagram captures show a center
pan; complete labels also have desktop and frozen local SVG/render evidence.
This release accepts only these two already-public articles and eight new
locale publications, not the entire remaining localization backlog or a site-wide
draft-visibility audit.

See [evidence.json](evidence.json) for each article's five public URLs, document
hashes, publication versions/times, separated completion states and immutable
receipt hashes. Private database identities, actor IDs and raw snapshots remain
outside Git in the stated evidence archive.
