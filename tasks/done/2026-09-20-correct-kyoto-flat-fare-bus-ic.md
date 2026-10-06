---
id: 2026-09-20-correct-kyoto-flat-fare-bus-ic
title: Correct Kyoto flat-fare bus IC and one-day-pass boarding steps
status: done
priority: P2
area: api
owner: claude-opus-5-5-board-closures
claimed_at: 2026-10-06T00:48:41Z
created_at: 2026-09-20T09:43:51Z
completed_at: 2026-10-06T01:40:26Z
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

- [x] Correct the ordered boarding/payment steps and applicable bus type in the published zh-TW source, preserving unrelated prose and visibility.
- [x] Guard the live revision/hash and publish the exact corrected source with backup and desktop/mobile receipts.
- [ ] Rebase and review all four Kyoto translations and diagrams before their publication.
  Moved to `2026-10-06-batch-005-nikko-kyoto-translations-refresh`.
- [x] Make the source SVG heading and article caption accurately explain solid EX and dashed ordinary bus lines.
- [x] Render the source SVG at 1600x900 and remove existing destination-card/label overlaps without changing route facts or credits.

## Steps

- [x] Check Kyoto City's official boarding, IC and pass guidance.
- [x] Reconcile the 2026-09-20 read-only live snapshot with repository pack and prepare exact source correction PR.
- [x] Deploy, publish and validate source.
- [ ] Refresh Batch 005 baseline. Moved to `2026-10-06-batch-005-nikko-kyoto-translations-refresh`.

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
- 2026-10-06 (claude-opus-5-5-board-closures). The publication was done on 2026-09-20; it is
  verified read-only here, and the translation rebase is split off:
  - **Live text.** The public API (editorial User-Agent) returns `status: published`,
    `published_locales: ['zh-TW']`, document `version: 8` and
    `modified_at: 2026-09-20T11:56:56Z`, an hour after #593 merged (10:51:54Z). Normalized
    through `GuideDocument`, its `document_hash` is `865362fe…9caa`, the same as the pack at
    #593 (42adda043). The corrected sentences are all live:
    - 「上車時不用感應，前門下車時在運賃箱的讀卡機感應一次」
    - 「整理券車，才要在上車與下車時各感應一次」
    - 「第一次在前門下車時把卡插入運賃箱的讀卡機印上日期」
    - the caption 「實線是電車或觀光特急巴士，虛線是一般市巴士」
  - **Live diagram.** `https://mokaair.com/guides/kyoto-bus-subway-guide/diagram-1.svg` has
    SHA-256 `34d93fba…c395d`, byte-identical to main. Its heading reads
    「京都站出發觀光走廊　實線：電車／觀光特急；虛線：一般市巴士」. EX100 is drawn solid, and
    206 and 205 are dashed (`stroke-dasharray`). The 15 px labels from #1001 are live too,
    because the SVG ships with the web deploy.
  - **Repo ahead of live.** The repo pack's hash is `da86dc07…513c`. It differs from live in
    two fields only, neither belonging to this ticket. `blocks[18].items[0]` says 6:00
    instead of 6 點 (#1001), and `blocks[22].text` says 住宿稅 instead of 宿泊税 (#1028).
    Publishing them is filed as `2026-10-06-publish-onsen-kyoto-bus-zh-tw` (host only,
    owner consent).
  - **Desktop and mobile.** In the built-in browser, signed out, at 1366×900 and 375×812, the
    page shows the corrected IC and caption text, and on mobile has no page-level horizontal
    overflow (scrollWidth 375). The diagram loads at 1600 px inside its own `overflow-x-auto`
    strip. `verify_public.py --slug kyoto-bus-subway-guide --kind howto --locale zh-TW
    --sitemap` passed. en, ja, ko and zh-CN are still `unpublished` with `noindex`.
  - **Sources re-read 2026-10-06, both HTTP 200.** On Kyoto City's riding guide, 均一区間車
    have no boarding reader (「均一区間車には設置されていません」), and
    「整理券車においては乗車時にもタッチが必要です」. The 地下鉄・バス1日券 goes through the
    reader on first use, and later rides show the date to the driver. The 2026-03-20
    busnavi PDF also returns 200.
  - **Not verified.** The 2026-09-20 backup and receipts are not in the repository. What is
    verified is the outcome.
  - **Split.** DoD 3 and the "refresh Batch 005 baseline" half of the last step moved to
    `2026-10-06-batch-005-nikko-kyoto-translations-refresh`. It asks for the publish ticket to
    land first, so the four locales bind to the zh-TW readers will see.
  - `pack_cli lint --slug kyoto-bus-subway-guide`: clean.
