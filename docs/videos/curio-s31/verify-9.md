# S31 R6 spoken-line revision — independent review passed

2026-10-20. Two targeted `tts --redo` rounds left 18 `check-audio` flags on R5a audio. This R6 candidate rewrites exactly those 18 narration lines and the corresponding 18 claim rows for clearer spoken wording. `ly019` also changes its voice direction from question cadence to statement cadence. No still prompt, source URL, chapter, loop, or other scene field changed.

| Artifact | R5a (audio version) SHA-256 | R6 candidate SHA-256 |
| --- | --- | --- |
| `script.md` | `332c875a835f89b428c124f578c380079976b9e35b396d098b086a56ba08cef2` | `60613153b84425c19ee6abe31a74a46a874a1691599e1cdee5059be1fd9f42b0` |
| `video.json` | `930b04118fc8eaab69a904e986a5888322d0d942247535f1567e347bd0a4bf11` | `28adf661838a0c0feb87865a1638795b75edc2d5477de8e3d8b8a6d7e450bc07` |
| `claims.md` | `83063009c6fec93840e0e6043118f7ed2df691b3e38651bc1590f12ad0ec2127` | `aaa50b3a3fc6aa66ab35bd1476186bba984380004e20ec5299a779052575d59f` |

## Exact changed IDs

| IDs | Spoken change and source boundary |
| --- | --- |
| `ly004` | Names Du Mu and renders his poetic rider and smile without making the poem a courier record (`DM`). |
| `ly006` | Asks how far the later history says the fruit traveled; `ly034` still supplies its broad `數千里` answer (`NBG`). |
| `ly008` | Asks which quality of Bai Juyi's Ba Gorge fruit changes first; `ly068` still gives color, aroma, then taste (`BJ`). |
| `ly009` | Asks whether the writings share a shipment mark before drawing a route (`DM`, `NBG`, `NBL`, `BJ`). |
| `ly013` | Uses Du Mu as the subject and keeps the fruit reveal for `ly015` (`DM`). |
| `ly017` | Says the poem gives no list of informed people, so `無人知` is not a population count (`DM`). |
| `ly019`, `ly020` | Distinguish the poem's one rider from the later history's mounted transmission; the second poem then moves to another subject. `ly019` now has statement cadence (`DM`, `NBG`). |
| `ly022`, `ly023` | Paraphrase the second poem's court music, the third poem's Lushan dance, and the sequence's court satire. No route is inferred from these poems (`DM`). |
| `ly032` | States that the later history says mounted transmission while Du Mu's poetic rider cannot count all horses used (`NBG`, `DM`). |
| `ly039`, `ly040` | Keeps the history's capital arrival separate from the poem's palace gates and asks for matching arrival dates before identifying one shipment (`NBG`, `DM`). |
| `ly058` | Says the birthday music account does not identify its fruit arrival as the biography's mounted shipment (`NBL`, `NBG`). |
| `ly076`, `ly077` | Uses a conditional for a hypothetical shared batch, then retains the biography's **taste unchanged at the capital**, without substituting aroma or a palace receipt (`BJ`, `NBG`). |
| `ly081`, `ly082` | Requires an exact shared route and elapsed time before computing delivery speed; Bai Juyi's Ba Gorge is questioned, not declared the court fruit's origin (`BJ`, `NBG`). |

The four complete pinned transcription files at `/tmp/curio-s31-{fanchuan,newtang,oldtang,baiji}.txt` were reopened. Their SHA-256 values match [research.md](research.md): `f6a2c78a1da55168b03e7556ac4a57c7c7f64c74b63ffe4af2d56558cceb42d1`, `c9b7a46b1f4f1c3950c40a5e4b30f3ccb3bfd19acd2d638d38359d0db7f5f559`, `ff840f4e9f94cdee86f3e6db86b99ecb923fea56046d30803d2576459400c0fd`, and `6074f3b5cc14e45b4c1c18edfddd7ec814709038f8351bb7cbcde17b66ddbb81`, respectively. The author compared the changed lines with the pinned passages. **This is an author check, not the independent source verdict.**

`node tools/video/cli.mjs script --slug curio-s31` regenerated the script. `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s31` reports **0 errors, 0 warnings**, 97 lines, 1,936 spoken units, and 9.4 minutes estimated total duration. A structural diff confirms only the 18 flagged scene texts plus `ly019` voice direction changed, all 97 claims exactly match their scene text and ID, and 96 still prompts plus 10 loops remain unchanged. The latest **R5a audio** timeline (speech hash `725ed39511c3b994`) measures `ly010` frame 1,497 through `ly097` frame 17,887 at 30 fps: **546.3 seconds / 9:06.3**. Those same body lines now contain 2,033 Unicode code points versus 1,997 before, so the rewrite does not shorten the body; R6's actual duration has not been measured.

`npm run test:docs-videos` passed 236/236 tests. `npm run check:tasks` validated 2,098 task files with existing queue warnings and exit code 0. `git diff --check` passed.

## R6 independent checks

The R5a approvals and audio check bind the **old hashes**. A fresh reviewer sealed a narration-only 13-question PASS on this exact R6 script before opening claims or sources; those initial questions were self-formulated, so they were **not** used as the official narrative verdict. A second independent reader then used `narrative --slug curio-s31 --json`, sealed the official thirteen answers and submitted them with `narrative --answers`: **13/13 PASS**, recorded in `/workspace/.video-work/curio-s31/review/narrative.json` for this exact script. The first independent reader separately reopened all four pinned primary texts, passed each of the 18 changed lines, all 97 aligned claims and all 96 prompts, with lint 0/0. Full source and prompt receipt: `/tmp/curio_s31_r6_independent_audit.md`. The slight repetition at `ly085–ly095` was advisory, not a failed panel item.

The old R5a audio still has 18 flags and cannot approve the R6 spoken revision. Next: record a new local script approval under the owner's standing delegated production instruction, synthesize changed R6 lines, then rerun `check-audio` on all 97. No R6 images or music should be requested before zero unresolved audio flags and a current quote. The preauthorized image-plus-music ceiling remains US$3.97. Local delegated approval must not be described as the owner personally listening or watching; site review remains a separate pending gate.
