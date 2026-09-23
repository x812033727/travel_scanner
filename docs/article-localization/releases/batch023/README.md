# Batch023: domain billing guides

Four previously Traditional-Chinese-only lifestyle articles now provide complete
English, Japanese, Korean and Simplified Chinese documents. Each translation includes
a localized SVG cover, its 1600x900 JPEG output and a localized SVG diagram: 48 new
files in total. All four Traditional Chinese documents and 12 original image files
remain unchanged. Image credit remains Mokaair / © Mokaair.

Content PR: [#695](https://github.com/x812033727/travel_scanner/pull/695).
The content PR was already merged before this release executor continued. The nine checks passed for exact content head `b15ae270ca570f57ca6c29229bf245535a081c30`.
Its full Git tree matches deployed merge `b7f131c576070b9b1446c5956ad56e4201767d80`.

| Article | Slug | Content | Draft import | Public publication | Browser verification |
| --- | --- | --- | --- | --- | --- |
| Bluehost 網域與帳務問題：加購、付款與續約逐項確認 | `bluehost-domain-billing` | Complete | 4 new locales | 5 languages | Desktop + mobile |
| 網域或主機到期會怎樣：續約與停用前的檢查表 | `domain-hosting-renewal` | Complete | 4 new locales | 5 languages | Desktop + mobile |
| Gandi 網域管理：註冊、DNS 與續約檢查 | `gandi-domain-management` | Complete | 4 new locales | 5 languages | Desktop + mobile |
| Namecheap 網域設定：註冊後如何連到網站與信箱 | `namecheap-domain-setup` | Complete | 4 new locales | 5 languages | Desktop + mobile |

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
their frozen bytes. Sitemap API pages contain [1000, 1000], totaling
2000 unique rows; all API article URLs are covered by XML.

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
