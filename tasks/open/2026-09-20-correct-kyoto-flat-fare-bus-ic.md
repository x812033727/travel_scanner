---
id: 2026-09-20-correct-kyoto-flat-fare-bus-ic
title: Correct Kyoto flat-fare bus IC and one-day-pass boarding steps
status: in-progress
priority: P2
area: api
owner: claude-opus-5-5-board-closures
claimed_at: 2026-10-06T00:48:41Z
created_at: 2026-09-20T09:43:51Z
completed_at:
branch: claude/board-closures
depends_on: []
scope:
  - apps/api/app/guides/content/kyoto-bus-subway-guide.json
  - apps/web/public/guides/kyoto-bus-subway-guide/diagram-1.svg
---

# Correct Kyoto flat-fare bus IC and one-day-pass boarding steps

## Why

The published zh-TW Kyoto bus guide tells IC riders to tap at rear boarding
and front exit on the standard 230-yen flat-fare City Bus. It also places the
first use of a subway/bus one-day pass at boarding. The official
[Kyoto City Bus riding guide](https://www.city.kyoto.lg.jp/kotsu/page/0000324695.html)
says flat-fare buses have no boarding reader: board without tapping and pay or
tap at the front exit. Distance-adjusted buses require the boarding and exit
IC taps. A first-use one-day pass goes through the fare reader at the front
exit; on later rides show the printed date to the driver there. Four staged
Batch 005 translations inherit the wrong steps and are blocked.
The map also draws the sightseeing-express bus as a solid line, despite its
source caption and heading claiming all solid lines are rail.

## Definition of done

- [ ] Correct the ordered boarding/payment steps and applicable bus type in the published zh-TW source, preserving unrelated prose and visibility.
- [ ] Guard the live revision/hash and publish the exact corrected source with backup and desktop/mobile receipts.
- [ ] Rebase and review all four Kyoto translations and diagrams before their publication.
- [ ] Make the source SVG heading and article caption accurately explain solid EX and dashed ordinary bus lines.
- [x] Render the source SVG at 1600x900 and remove existing destination-card/label overlaps without changing route facts or credits.

## Steps

- [x] Check Kyoto City's official boarding, IC and pass guidance.
- [x] Reconcile the 2026-09-20 read-only live snapshot with repository pack and prepare exact source correction PR.
- [ ] Deploy, publish and validate source, then refresh Batch 005 baseline.

## How to verify

Validate pack schema; verify the published zh-TW document hash and locale
revision after release; signed-out desktop/mobile pages must state one exit
tap on flat-fare buses and both taps only on distance-adjusted buses.

## Notes

Official guide checked 2026-09-20, particularly boarding sections [1], [4]
and the one-day pass instruction. The 2026-03-20 Kyoto City bus brochure also
shows the boarding tap as the distance-adjusted exception:
https://www.city.kyoto.lg.jp/kotsu/cmsfiles/contents/0000019/19770/JPN(omote)260320busnavi.pdf
Do not release any Kyoto Batch 005 language until the corrected live source
is version-pinned and translations are updated.
The 2026-09-20 09:12 UTC read-only snapshot confirms a public zh-TW-only
article (id `17e8b6b8-4455-4461-8a6d-fa5edc52200f`, metadata version 2,
zh-TW locale id `374bf7dd-4b9f-4cc7-bbc7-6ec0841e50fb`, version 6) at
document SHA-256 `ef895904cf7b208f1dfe6955f196665f6256cf5525e5cb5d6df2e50358faedda`.
Refresh the live revision and hash before any production write. This PR changes
only blocks 4 and 14, two items in block 5, the block 19 map caption,
and the source SVG heading/layout. The independent visual review counted all
48 original text nodes and found no remaining text-to-text collision or canvas
overflow after the layout patch.

- 2026-09-30 (claude-opus-5-5, owner-approved `--force` on `2026-09-21-91-ci`):
  that ticket touched this scope only to satisfy the content checker. In
  `diagram-1.svg` every 14 px label became 15 px (layout re-rendered and
  checked), and zh-TW `blocks[18]` item 0 now says `早上 6:00 開門` instead of
  `早上 6 點開門`. Nothing about fares or IC cards changed; rebase onto main.

- 2026-09-30 (claude-opus-5-5, owner-approved `--force` on
  `2026-09-20-lodging-tax-wording-site-wide`): in this ticket's packs the zh-TW
  title, description and body now say 住宿稅 where they said 宿泊稅 or 宿泊税.
  No number changed; Japanese official page names in `sources` are unchanged.
- 2026-10-04 board sweep (claude-opus-5-5-incomplete-tickets, approved by the owner): the claim by codex-article-localization (since 2026-09-20T09:43:56Z) was stale and is released so it stops locking its scope. Landed: #593 #1001 #1028. Still open: Correct boarding/payment steps in published zh-TW source (repo pack done in #593; live publish pending); Guard live revision/hash and publish corrected source with backup and desktop/mobile receipts; Rebase and review four Kyoto Batch 005 translations and diagrams; SVG heading/caption explain solid EX vs dashed bus lines (likely done in #593, unticked); Deploy, publish, validate source, refresh Batch 005 baseline.
