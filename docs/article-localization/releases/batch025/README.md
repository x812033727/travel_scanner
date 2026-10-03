# Batch025: domain transfer and hosting guides

Four already-published Traditional Chinese lifestyle articles gained complete English,
Japanese, Korean and Simplified Chinese documents, with localized text in their cover
and diagram assets. Content [PR #700](https://github.com/x812033727/travel_scanner/pull/700)
passed all nine required checks and merged at 0f9eb1dc02cb5663a0ae3590422e4764c269bde8
from content head 7d19183e0967b408df67ae395a2bb7643f452170.

| Article | Content | Draft import | Public publication | Browser verification |
| --- | --- | --- | --- | --- |
| [Domain registrar transfer](https://mokaair.com/zh-TW/life/domain-registrar-transfer) | Complete | Four new locales | Five languages | Desktop and mobile |
| [FastComet WordPress setup](https://mokaair.com/zh-TW/life/fastcomet-wordpress-setup) | Complete | Four new locales | Five languages | Desktop and mobile |
| [HostGator WordPress setup](https://mokaair.com/zh-TW/life/hostgator-wordpress-setup) | Complete | Four new locales | Five languages | Desktop and mobile |
| [SiteGround WordPress setup](https://mokaair.com/zh-TW/life/siteground-wordpress-setup) | Complete | Four new locales | Five languages | Desktop and mobile |

The guarded `<saved-session>` release completed on 2026-09-23 UTC. A fresh custom-format
database backup passed pg_restore --list before deployment. The release imported
only the 16 missing-language drafts and then published those 16 languages. All four
source articles stayed at article version 2 and Traditional Chinese locale version 4.
The new locale rows reached published version 2. Original source bodies, metadata,
visibility, revisions and 12 original image files remained unchanged. The journal
records 32 committed operations and no pending or duplicate publication. The owned
deployment hold was cleared only after final acceptance, followed by read-only
health and revision checks.

Public acceptance checked 20 five-language article URLs, 40 desktop/mobile viewport
cases, 80 screenshots, 20 expanded description/source cases, all 60 public image
files (48 localized and 12 originals), canonical and reciprocal hreflang, and
same-language internal links. Sitemap API pagination returned [1000, 1000, 32]
unique rows and the XML covered all 2032 API article URLs. The actual database,
journal, transport, final evidence and visual captures received independent review.

[evidence.json](evidence.json) lists each article's five public URLs, document hashes,
publication versions and times, acceptance scope and immutable receipt hashes.
Private database identities, actor IDs, backups and raw host captures remain in the
local release evidence archive, outside Git.

One existing, separately tracked desktop header issue caused the global search icon
to overlap its placeholder text. It did not affect article content or images. Browser
viewport review is not physical-device acceptance; mobile diagram captures used a
center pan while complete labels were checked on desktop and in local SVG renders.
This record attests the 2026-09-23 release and post-clear snapshot, not the site's
current 2026-09-27 runtime state or the remaining localization backlog.
