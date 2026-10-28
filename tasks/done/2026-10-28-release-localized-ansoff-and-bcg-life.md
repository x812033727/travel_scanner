---
id: 2026-10-28-release-localized-ansoff-and-bcg-life
title: Release localized Ansoff and BCG life guides
status: done
priority: P1
area: docs
owner: codex-gpt6-two-life-release-20261028
claimed_at: 2026-10-28T05:22:49Z
created_at: 2026-10-28T02:26:36Z
completed_at: 2026-10-28T06:48:11Z
branch: codex/release-two-life-20261028
depends_on:
  - 2026-10-28-localize-ansoff-and-bcg-life-guides
scope:
  - docs/article-localization/releases/two-life-20261028
---

# Release localized Ansoff and BCG life guides

## Why

The authoring task adds eight reviewed en/ja/ko/zh-CN documents for two already
public life articles. Their current zh-TW v4 sources remain unchanged. Publication
must follow the merged/deployed content and fresh database guards, separately
from the owner's approval of the older seventeen-article wave.

## Definition of done

- [x] Content PR merged with required checks and exact runtime content/assets verified.
- [x] Fresh source/target versions, visibility and holds match the reviewed bundle.
- [x] Concrete owner release decision, verified backup and isolated rehearsal precede writes.
- [x] Eight missing target documents published through the native journal; no source changes.
- [x] Idempotent replay, five-language public API/image/link/desktop/mobile acceptance and sanitized release records complete.

## Steps

- [x] Verify the content merge and deployed image, avoiding unnecessary rebuilds.
- [x] Refresh snapshot and scoped dry-run; obtain the concrete release decision.
- [x] Back up, rehearse and publish only the two selected articles/four target languages.
- [x] Verify actual public state and write release receipts before closing this task.

## How to verify

Use the unchanged localization publisher with the exact manifest, native journal
and fresh source guards. Verify all ten public locale pages and media through the
public API/browser, including exact canonical/hreflang and publication-aware
related links. Unpublished Similarweb target references remain plain text.

## Notes

Authoring manifest SHA256:
`5717849d1e3407a3dd1fe762a96067236837562aed3fc8c1faeb575c160668d1`.
PR [#1901](https://github.com/x812033727/travel_scanner/pull/1901) merged as
`b78895e5fad1285d68a49a9e059eb318b846e40d` after all 22 candidate checks passed.
The owner separately authorized: first back up, then deploy and publish these
eight translations. This authorization is limited to the two selected articles.

A fresh full database backup and actual isolated restore both completed with
exit 0 before deployment. The archive is 565,854,427 bytes, SHA256
`0231347ceed6970b9baf6f90159c8fd9cfdd1569e910d4bc276841dbd8de7993`.
The restored-database rehearsal and exact four-phase replay passed; all 167
protected/whole table fingerprints matched and the only new history was the
authorized 16 revisions plus 16 audit rows. Deployment completed with exit 0 and
three consecutive healthy checks; actual two packs and 24 new assets matched.

Production native publication completed at 2026-10-28T06:22:28Z with 8 draft,
8 publication and 0 hub operations, followed by four successful replay phases.
The eight new locales are public v2; both complete zh-TW source rows remain v4
and unchanged. Production journal SHA256:
`6fb04aa0ac7193278340ebe41bfda5517f79b09c9b2afabe9e3ada7d20d3540d`.

Public API/media/sitemap acceptance passed: 10 exact documents, 28 asset files,
all sitemap chains. All 10 actual browser pages passed seven automated checks;
two independent reviewers actually viewed 20 original screenshots and 49 native
crops. All 103 issued requests returned 200; six optional requests were cancelled
before fetching and are not counted as HTTP successes. Four new unpublished
references retain visible text without live links; no unexpected link findings.

Fresh final readback passed, and this release's own hold was cleared at
2026-10-28T06:44:56Z. The unchanged final host verifier reported 11 PASS, 0 FAIL.
Backup and isolated restore are retained. Sanitized records:
`docs/article-localization/releases/two-life-20261028/README.md` and
`evidence.json`. A BCG zh-CN desktop capture ends before the bottom copyright
strip; its mobile capture includes that strip, with no observed article cutoff.
This task does not complete the overall localization backlog.
