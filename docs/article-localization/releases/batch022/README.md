# Batch022: website planning guides

Four previously Traditional-Chinese-only lifestyle articles now provide complete
English, Japanese, Korean and Simplified Chinese documents. Each translation includes
a localized SVG cover, its 1600x900 JPEG output and a localized SVG diagram: 48 new
files in total. All four Traditional Chinese documents and 12 original image files
remain unchanged. Image credit remains Mokaair / © Mokaair.

Content PR: [#692](https://github.com/x812033727/travel_scanner/pull/692).
The content PR was already merged before this release executor continued. The nine checks passed for exact content head `25da625679a5b1f10a46cce69e07b918c2d2befe`.
Its full Git tree matches deployed merge `32f032b161534328f95366010fda1722397ae10c`.

| Article | Slug | Content | Draft import | Public publication | Browser verification |
| --- | --- | --- | --- | --- | --- |
| Cloudways 建站：伺服器、應用程式與帳戶驗證 | `cloudways-wordpress-setup` | Complete | 4 new locales | 5 languages | Desktop + mobile |
| 架站預算怎麼編：把首年、續約與維護分開算 | `website-budget-worksheet` | Complete | 4 new locales | 5 languages | Desktop + mobile |
| WordPress.com 與自架 WordPress：維護、費用與掌控權怎麼取捨 | `wordpress-com-org-choice` | Complete | 4 new locales | 5 languages | Desktop + mobile |
| 第一次架設 WordPress：從測試站到公開網站 | `wordpress-first-site` | Complete | 4 new locales | 5 languages | Desktop + mobile |

All four source articles remain at version 2, and all four complete zh-TW version 4
rows are unchanged. Sixteen missing locales were created and then published at version 2.
Category, ordering, visibility, expiry and original publication timestamps were
preserved. The explicit dry run selected 16 translation starts, 16 article
publications and zero hub publications. All 32 commits are sealed in the accepted
journal, with no pending operation and no duplicate publication.

A fresh custom-format database backup passed `pg_restore --list` before deployment.
The guarded hostinger2 deployment, import, publication, three consecutive service
health checks, actual database/journal acceptance and public browser verification
completed. Final evidence was staged before the owned deployment hold was cleared.
The post-clear snapshot confirms the exact clean deployed revision and healthy services.

Public acceptance covers 20 language URLs, 40 desktop/mobile cases and 80 actual
top/diagram screenshots independently viewed. Full body, headings, Mokaair image
credits, expanded diagram descriptions, sources, original URLs and same-language internal links,
canonical and reciprocal hreflang checks passed. All 60 public image files match
their frozen bytes. Sitemap API pages contain [1000, 984], totaling
1984 unique rows; all API article URLs are covered by XML.

Known nonblocking findings are listed in the evidence record. Browser viewport
checks are not physical-device acceptance. Mobile diagram captures show a center
pan; complete labels also have desktop and frozen local SVG/render evidence.
This release accepts only these four already-public articles and sixteen new
locale publications, not the entire remaining localization backlog or a site-wide
draft-visibility audit.

See [evidence.json](evidence.json) for each article's five public URLs, document
hashes, publication versions/times, separated completion states and immutable
receipt hashes. Private database identities, actor IDs and raw snapshots remain
outside Git in the stated evidence archive.
