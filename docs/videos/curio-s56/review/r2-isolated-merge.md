# Curio S56 R2 isolated narrative merge

## Frozen independent reads

Both readers scored `docs/videos/curio-s56/script.md` at SHA-256 `70720bc2c5b84764247193bbbfdff199aef3b16dbc2e8d3c6ded25276f2a521d`. B's [JSON](r2-isolated-blind-b.json) and [Markdown](r2-isolated-blind-b.md) were written and hashed before B saw A's frozen answer.

| Reader | Frozen JSON SHA-256 | Individual result |
| --- | --- | --- |
| [A](r2-isolated-blind-a.json) | `d49aeaac08a694b7131d1d0e223c9940df473d2dc38938697f6b4a5aa3b244ed` | 8 Yes / 5 No |
| [B](r2-isolated-blind-b.json) | `2d701a3281b523e1574f74b9ae6cce5f6449280ad1e7dc1c1b50c8d9a91f8dbe` | 7 Yes / 6 No |

## Official OR merge

Each frozen `pass` field was mapped to the official `yes` field. Each reader was checked with `panelVerdict`, then combined with `mergePanelVerdicts` from `tools/video/core/narrative.mjs`: a criterion passes when either reader supplies a cited Yes. The [audit](r2-isolated-merge-audit.json) retains both normalized verdicts, input hashes, and the merged result. The [merged answer file](r2-isolated-merged-answers.json) feeds the narrative CLI. Raw reviews remain unchanged.

A recorded scene IDs separately, so its first ID was prefixed in brackets to each recorded reason. B's optional `chapters_are_events` evidence described the chapter titles without a bracketed ID; `[s56014]`, the start of the first cited chapter, was prefixed for the official parser. These are citation format adaptations, with no judgment changed. The audit records both.

| Criterion | A | B | OR | Key evidence |
| --- | --- | --- | --- | --- |
| `no_spoiler` | Yes | No | **Yes** | B sees [s56006]–[s56007] as revealing the new fire later described at [s56073]–[s56075]; A treats the opener as a preview that holds back the main fire's later crossing and union with the new fire [s56079]. |
| `one_line` | No | No | **No** | After Foster reaches Monday dawn [s56124]–[s56126], [s56127] rewinds to Luo Xu earlier the same night. |
| `chapters_link` | No | No | **No** | [s56144] asks where water failed; the next chapter's first sentence [s56145] only reports black smoke. [s56146] gives the answer. |
| `payoffs` | No | No | **No** | [s56101] asks whether small items can be retrieved, without a clear outcome through [s56113]; [s56163] asks whether stored well water gets used, without an explicit answer through [s56170]. |
| `no_recap` | No | No | **No** | The opening's new fire 400 yards behind Foster [s56006] recurs at [s56073] without a named callback; the prior night's stopped fire is restated at [s56030]–[s56032]. |
| `no_detour` | No | No | **No** | [s56109]–[s56113] dwell on a named box, fares, and payment bargaining; [s56126] adds a biscuit stop, without advancing why the river failed. |
| Other seven | Yes | Yes | **Yes** | `scene_first`, `no_toc`, `open_loops`, `chapters_are_events`, `outro_no_next`, `opening_hooks`, `one_thread`. |

The merge has **8/13 Yes and five failed required criteria**: `one_line`, `chapters_link`, `payoffs`, `no_recap`, `no_detour`.

## Isolated CLI receipt

Command: `VIDEO_WORKDIR=/tmp/curio-s56-r2-isolated node tools/video/cli.mjs narrative --slug curio-s56 --answers docs/videos/curio-s56/review/r2-isolated-merged-answers.json --json`

The CLI exited **1: FAIL**, as expected for five failed required criteria. The [CLI verdict](r2-isolated-cli-verdict.json) reports 8 Yes, those five failures, no advisory failures, and 13 answers. The [CLI receipt](r2-isolated-cli-receipt.json) is the round 1 snapshot from `/tmp/curio-s56-r2-isolated/curio-s56/review/narrative.json`, SHA-256 `dbd8d713e8cc7af0a9d95a8055808b78cc3be54fc24ec3ac5b5314c38a503f84`. It records narrative hash `005341a354efd0b4`, script hash `33150079756bb9b4348cad90f51d8b510f9ab5c29a029781d9211233a98c0f02`, panel rules SHA-256 `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`, and panel narration SHA-256 `34b42d8ce81efe04c64bcefddf20c75f15ccd51702c6564800914917b303a8a7`.

The script still matches the frozen SHA-256. No script or media was changed by this review.
