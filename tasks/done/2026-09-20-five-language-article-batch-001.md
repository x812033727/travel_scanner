---
id: 2026-09-20-five-language-article-batch-001
title: Five-language article batch 001
status: done
priority: P1
area: meta
owner: codex-article-localization
claimed_at: 2026-09-20T02:55:48Z
created_at: 2026-09-20T02:55:32Z
completed_at: 2026-09-20T05:46:54Z
branch: codex/article-localization-batch-001
depends_on:
  - 2026-09-20-five-language-article-release-tooling
scope:
  - docs/article-localization
  - apps/api/app/guides/content/taichung-sun-moon-lake-2-day.json
  - apps/api/app/guides/content/taipei-4-day-itinerary.json
  - apps/api/app/guides/content/taipei-hot-springs-beitou-wulai.json
  - apps/api/app/guides/content/taiwan-convenience-store-guide.json
  - apps/api/app/guides/content/taiwan-hsr-tra-ticket-guide.json
  - apps/api/app/guides/content/taiwan-winter-events-2026-2027.json
  - apps/web/public/guides/taichung-sun-moon-lake-2-day
  - apps/web/public/guides/taipei-4-day-itinerary
  - apps/web/public/guides/taipei-hot-springs-beitou-wulai
  - apps/web/public/guides/taiwan-convenience-store-guide
  - apps/web/public/guides/taiwan-hsr-tra-ticket-guide
  - apps/web/public/guides/taiwan-winter-events-2026-2027
---

# Five-language article batch 001

## Why

The live baseline has 20 public Taiwan travel guides whose English, Japanese, Korean
and Simplified Chinese documents are complete while Traditional Chinese is missing.
Fourteen pack files are already covered by the active AIO description task, so this
non-overlapping first batch fills the other six without changing classifications,
ordering, visibility or existing prose.

## Definition of done

- [x] All six guides contain complete independently reviewed zh-TW documents.
- [x] Any embedded image text has a hash-bound zh-TW rendition with visual checks.
- [x] The reviewed bundle installs idempotently and passes local guide and link checks.
- [x] The exact PR head is merged, backed up, deployed and health checked.
- [x] Only the six authorized zh-TW locales are published and browser verified.

## Steps

- [x] Capture a fresh read-only production snapshot and rebuild the baseline.
- [x] Translate, render and independently review the six zh-TW documents.
- [x] Assemble and install batch 001 from the reviewed, hash-bound artifacts.
- [x] Open and merge the content PR.
- [x] Back up and deploy the exact merged revision.
- [x] Dry-run, publish and verify the six zh-TW public pages.

## How to verify

Run the article localization pipeline status/report, guide pack tests, i18n checks and
CI. After deployment, verify body, images, canonical, hreflang and internal links on
desktop and mobile for every slug.

## Notes

Production snapshot captured at 2026-09-20T10:54:26.661901+08:00 from deployed commit
7f2c5478151da10ba284fa8bc50552456e84ffb3. It contains 972 database articles. The
combined repository/database baseline contains 1,067 articles, 3,604 missing language
documents and 3,468 missing publication locales. This replaces the stale 626/2,404
inventory. The other 14 Taiwan guides remain queued until task
2026-09-19-aio-answer-first-descriptions-part-2 releases their pack scope.

Batch 001 reviewed release manifest:
`8edac5238eb3856c688f797c9563acfc47b7fd579bba0a3352077c79de8a877e`.
It contains six reviewed zh-TW documents and 24 hash-pinned assets. Installation
changed the six declared packs plus six localized SVG files and was idempotent on
rerun. The progress report records 6 translated, 6 rendered, 6 reviewed, 6
assembled and zero imported, published or browser-verified at this stage.

The first Windows bundle (`d022d3be...`) was rejected before publication because
Git's LF checkout would not match its CRLF byte hashes. PR #577 made pipeline and
bundle text portable, added `svg_tag` binding, and rejects CRLF or trailing whitespace
in reviewed SVGs. The six jobs were freshly prepared in `work-batch-001-v2`; their
translation and document bytes match the first review, all preview PNGs are byte
identical, two independent reviewers reapproved text, visual layout and glyphs, and
the new install completed twice with the same 30-file journal.

Local validation: all six packs load with exactly five locales; 38 guide content
and series tests passed with 24 environment skips; five-locale i18n validation
passed. Assembled internal routes use zh-TW paths, article references retain their
identity for runtime publication checks, and existing locale prose stayed intact.

PR #579 was merged as `9d5f77e2f8af516a4260aa555145bd13fa6e5547`
after all eight required checks passed. Main-branch CI run 35491278150 then passed
the API, web, container and full-stack smoke jobs for that exact commit. The guarded
production release built and activated the same commit; `/health` and `/ready`
returned HTTP 200 and all application services used the target images.

The custom-format pre-deploy backup is
`/root/mokaair-localization-9d5f77e2f8af/predeploy.dump` with SHA-256
`11d1af993592407d92002743a94285130d3dfa38eac61c0d369684505587dc42`.
The pre-publication backup is
`/root/mokaair-localization-9d5f77e2f8af/prepublish.dump` with SHA-256
`71dbff1f1fd96a2b5a01890a54aceabf0ea542d891fb35394a45eedefec3160d`.
Both were verified with `pg_restore --list` before their protected phase proceeded.

The sealed publication journal finished with six draft operations, six article
publication operations, zero hub operations and no pending entry. A direct database
snapshot matched the journal's expected state: all six zh-TW documents have
`version=2`, `published_version=2` and `latest_action=published`, while all 24
pre-existing en, ja, ko and zh-CN locale records remained byte-for-byte unchanged.

Browser verification covered every zh-TW route at desktop 1440x1000 and mobile
390x844. All six pages and all six localized SVGs returned HTTP 200; the exact
Traditional Chinese title and substantive body rendered, canonical and all five
language alternates were correct, localized internal links had no wrong-locale
targets, and no page had horizontal document overflow. The guarded clear-hold phase
wrote its completion receipt only after this browser receipt and then removed the
shared deployment hold.
