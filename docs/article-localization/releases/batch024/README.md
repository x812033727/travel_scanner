# Batch024: hosting setup guides

Four previously Traditional-Chinese-only lifestyle articles now provide complete
English, Japanese, Korean and Simplified Chinese documents. Each translation includes
a localized SVG cover, its 1600x900 JPEG output and a localized SVG diagram: 48 new
files in total. All four Traditional Chinese documents and 12 original image files
remain unchanged. Image credit remains Mokaair / © Mokaair.

Content PR: [#699](https://github.com/x812033727/travel_scanner/pull/699).
The content PR was already merged before this release executor continued. The nine checks passed for exact content head `91b685627bdf524a9da1ab9da965b845e9dfe19d`.
Its full Git tree matches deployed merge `85b76908543e1fb59256a2c8ec30e9c3e8196275`.
The release executor observed the external merge and did not perform it. The earlier
70-version merge attempt was blocked before merging. The accepted 91-version includes
security-document/task ancestor `cb4960b031789d89ea99619b669af42cc52c578b`: those
nine history changes preserve all reviewed article, image and runtime bytes, and
the complete nine-check CI was rerun for the actual accepted 91-version tree.

| Article | Slug | Content | Draft import | Public publication | Browser verification |
| --- | --- | --- | --- | --- | --- |
| Bluehost 架站流程：購買前確認，到安裝後驗收 | `bluehost-wordpress-setup` | Complete | 4 new locales | 5 languages | Desktop + mobile |
| hosting.com 架站入門：從舊 A2 名稱到目前的服務選擇 | `hosting-com-wordpress-setup` | Complete | 4 new locales | 5 languages | Desktop + mobile |
| Hostinger 架站教學：把第一個 WordPress 網站整理好 | `hostinger-wordpress-setup` | Complete | 4 new locales | 5 languages | Desktop + mobile |
| WordPress 主機比較怎麼做：用同一張需求表評估供應商 | `managed-hosting-comparison` | Complete | 4 new locales | 5 languages | Desktop + mobile |

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

This deployment also includes previously merged application changes and migration
`0084_ai_news_automation`; it is not a no-migration or no-runtime-change deployment.
The exact 107-file before/after Git delta was independently checked. After deployment,
a repeatable-read, read-only probe confirmed schema revision 0084, one disabled news
settings row in shadow mode, all three automatic-publication flags false, and zero
enabled news sources. The probe did not activate sources or the news scheduler profile.
Its actual capture time and immutable evidence hashes appear in `runtime_deployment`.

Public acceptance covers 20 language URLs, 40 desktop/mobile cases and 80 actual
top/diagram screenshots independently viewed. Full body, headings, Mokaair image
credits, expanded diagram descriptions, sources, original URLs and same-language internal links,
canonical and reciprocal hreflang checks passed. All 60 public image files match
their frozen bytes. Sitemap API pages contain [1000, 1000, 16], totaling
2016 unique rows; all API article URLs are covered by XML.

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
