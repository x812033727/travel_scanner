# H12 first-pass keyframe audit and prompt revision

2026-10-16. Media root: `<home>/mokaair-work/videos/curio-h12`. The first pass produced one take for each of 86 illustrated shots: 56 judge PASS, 30 judge held. All first-pass illustrations were screened against the approved line and scene intent using contact sheets; high-risk images were also inspected individually. A trim is derived from the same take; the cache contains no alternate take for any of the 12 human-flagged PASS images.

## Judge-PASS images requiring a targeted retake

| Priority | Shot and first-pass file | Visual conflict with approved narration or reveal | Revised prompt intent |
| --- | --- | --- | --- |
| P0 | `landing-no-reply` — `landing-no-reply-1-trim.jpg` | Red flag flies from the lighthouse although Moore arrives to find no usual flag. | Keeper on tender looks toward shore; keep lighthouse and flagpole outside the tight composition. |
| P0 | `boat-waits` — `boat-waits-1-trim.jpg` | Same red lighthouse flag appears behind the waiting sailor. | Close view of sailor, oar, boat rail and water. |
| P0 | `serious-absence` — `serious-absence-1.jpg` | Red lighthouse flag remains visible in the discovery sequence. | Keeper runs along rocky path with sea behind him. |
| P0 | `lamp-ready` — `lamp-ready-1-trim.jpg` | Oil lamp and a bulb-like prop glow during the daytime inspection, before the narrated evening relighting. | Unlit oil lamp with dark wick and filled oil container in window daylight. |
| P0 | `passing-ship` — `passing-ship-1-trim.jpg` | Distant lighthouse glows at midnight although the passing ship reported seeing no light. | Captain scans a fully dark island silhouette; only his ship lantern glows. |
| P0 | `landing-clothes` — `landing-clothes-1-trim.jpg` | Boots stand at the lighthouse doorway even though the account says the sea boots were missing. | Keeper points to a bare boot shelf and empty floor. |
| P0 | `overturned-chair` — `overturned-chair-1-trim.jpg` | Model chair stands upright while the line says the later poem has an overturned chair. | Reader looks at a model chair lying unmistakably on its side. |
| P1 | `poem-tease` — `poem-tease-1.jpg` | Chair appears in the opening tease before the approved script reveals the poem's chair detail. | Tight view of reader, page and bare tabletop model only. |
| P1 | `slate-entry` — `slate-entry-1-trim.jpg` | A blank paper sheet covers the log instead of showing the distinct slate cited in the report. | Dark framed chalk slate held over a separate bound logbook. |
| P1 | `kitchen-work` — `kitchen-work-1.jpg` | Modern gas hob/apartment kitchen misplaces the 1900 lighthouse scene. | Stone-walled kitchen and plain cast-iron range. |
| P1 | `rope-question` — `rope-question-1-trim.jpg` | Inspector pulls out a loose rope end although the next evidence says coils were still wound; implies use not established by the record. | Inspector studies an untouched, tightly wound coil. |
| P2 | `buoy-ties` — `buoy-ties-1-trim.jpg` | The canvas scrap that supports the subsequent inference is not visible on the tie. | Close view of intact knot with a conspicuous ragged canvas scrap. |

The other judge-PASS images showed no direct contradiction requiring a retake. Small prop/style variations were accepted under the Curio image-review rule; a cartoon illustration is not an evidentiary reconstruction. In particular, `buoy-height-1.jpg` shows colored remnants near the rail, not a clearly intact life buoy, so it was left accepted.

## Judge-held prompt triage

Twenty-one held prompts were tightened before the next take because their first outputs repeatedly misread the action, object or location: `boat-launched`, `cold-fire`, `replacement-duty`, `relight-night`, `report-delay`, `visibility-question`, `platform-height`, `box-contents`, `box-height`, `box-gone`, `crane-safe`, `crane-covered`, `railings-twisted`, `buoy-question`, `buoy-inference`, `wave-hypothesis`, `wind-compared`, `west-wind`, `poem-bridge`, `memory-recalled`, `exhibit-first`. The rewrites favor one visible person doing one action, a small fixed landing derrick instead of a modern ship crane, and a raised clay terrain model on a solid table instead of a printed map with invented text. `relight-night` now explicitly uses an oil flame rather than an electric bulb. `exhibit-first` now centers one attendant placing a letter in an open glass case.

Nine held prompts can use the judge correction on the next seed without a prompt rewrite: `letter-tease`, `opening-question`, `captain-volunteers`, `slate-later`, `work-date-inference`, `inference-boundary`, `two-records`, `inspector-lands`, `kitchen-recalled`. The last has letterbox bars and the wrong hand gesture; inspect its next take before accepting.

## Scope and checks

- `video.json` before SHA-256: `D16413FCD54ED2AA5FCFD12B88054FCF8B211AA96110C1514184467615AD3BF1`.
- `video.json` after SHA-256: `55F886845D1A52F55FE5EFC30C4018FF8360EDD94ECB308FB870DDF75D66A2BD`.
- Exactly 33 existing `data.prompt` strings changed: 12 judge-PASS and 21 judge-held. JSON scene count and order, line IDs, narration, claims, cards, cameras and all other scene fields were unchanged by structured comparison with `HEAD`.
- Approved `script.md` SHA-256 remains `408E3C8BAAFC0063B0B53410B579D14BA09D650753DB466A409E59470F9A620B`.
- `node tools/video/cli.mjs lint --slug curio-h12`: exit 0, 0 errors, 5 warnings (three repeated-word variety warnings, a long `coiled-rope` shot, and 8.8-minute textual estimate).
- `node tools/video/cli.mjs keyframes --slug curio-h12 --dry-run`: exit 0. `git diff --check`: exit 0. No image, audio, manifest, cache or paid-generation call was made during this revision.

The revised prompts are proposals for targeted new takes. Final image acceptance still requires visual review and judge result after generation.
