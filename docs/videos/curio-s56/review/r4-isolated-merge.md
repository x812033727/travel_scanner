# S56 R4 isolated narrative panel — official OR PASS

2026-10-20 UTC. Two isolated readers judged the same R4 script at SHA-256 `b76995caa74f0a1f65b068d9e115659d7c48678600b80e9ff502e641a6505152`. The [R4 source/written-visual review](r4-source-independent.md) separately passed at the five R4 author hashes. This receipt merges the frozen **narrative** reads; it is not a new source review or an author self-review.

| Reader | Frozen JSON SHA-256 | Own judgment |
| --- | --- | --- |
| [A](r4-isolated-blind-a.json) | `81fe94721908ee8c878a88d6838d21d3d19b4c8eeca54ad0dd4c874cdc1985cf` | 12 Yes / 1 No (`no_recap`) |
| [B](r4-isolated-blind-b.json) | `06e2c71d2bab8918b872df1b7a4eee619d0aee1ea297f02cf45f9ebdfa34c98c` | 12 Yes / 1 No (`no_detour`) |

## Official OR merge

I ran `panelVerdict` on each reader, then `mergePanelVerdicts` from `tools/video/core/narrative.mjs`. The rule accepts a criterion if **either** reader gives a Yes with a bracketed line-ID citation. The [audit](r4-isolated-merge-audit.json) records both normalized individual verdicts, raw input hashes, citation-format adaptations, and the merged verdict; the [merged answers](r4-isolated-merged-answers.json) fed the narrative CLI. Raw reader files are unchanged.

B's frozen JSON wrote scene IDs as `s56073` rather than `[s56073]`. I prefixed one bracketed anchor to each of B's 13 evidence strings without changing its judgment or original wording. Nine anchors use an ID already present in that evidence. Four evidence strings contained no ID; their anchors are `one_line` `[s56014]`, `no_toc` `[s56009]`, `chapters_are_events` `[s56070]`, and `one_thread` `[s56001]`. The audit names each adaptation. A needed no adaptation.

| Criterion | A | B | OR | Distinguishing evidence |
| --- | :---: | :---: | :---: | --- |
| `scene_first` | Yes | Yes | **Yes** | Foster is across the South Branch at [s56001]–[s56004]. |
| `no_spoiler` | Yes | Yes | **Yes** | The opening questions [s56006]–[s56013] withhold outcomes. |
| `one_line` | Yes | Yes | **Yes** | The earlier fire at [s56014] leads through Monday [s56145] and Tuesday [s56166]. |
| `no_toc` | Yes | Yes | **Yes** | [s56009]–[s56013] pose events, without a spoken outline. |
| `chapters_link` | Yes | Yes | **Yes** | [s56144] asks about water; [s56145] answers. |
| `open_loops` | Yes | Yes | **Yes** | Roof [s56051], river [s56069], and grass [s56156] remain live questions. |
| `payoffs` | Yes | Yes | **Yes** | Named rear-house and North Side callbacks arrive at [s56073] and [s56129]. |
| `no_recap` | **No** | Yes | **Yes** | A hears the same sturdy-building belief at [s56090] and [s56095]; B accepts the larger recalls as named callbacks and new facts. |
| `chapters_are_events` (reference) | Yes | Yes | **Yes** | Titles describe burning bridges, new fires, and rain. |
| `outro_no_next` | Yes | Yes | **Yes** | [s56172]–[s56176] close without naming another video. |
| `opening_hooks` | Yes | Yes | **Yes** | Houses, stone district, bridge, and North Side resident are distinct withheld moments [s56007]–[s56012]. |
| `one_thread` | Yes | Yes | **Yes** | Foster's safety-boundary question begins at [s56001] and returns in the ending [s56173]. |
| `no_detour` | Yes | **No** | **Yes** | A sees the grass defense [s56157]–[s56167] as the last safety boundary; B hears [s56153]–[s56171] as an extended shelter coda beyond the river-crossing question. |

The official OR result is **13/13 Yes, all 12 required Yes: PASS**. A's `no_recap` No and B's `no_detour` No remain **individual editorial advisories**; they do not fail the OR gate or appear as official advisory failures.

## Isolated CLI record

Command: `VIDEO_WORKDIR=/tmp/curio-s56-r4-isolated node tools/video/cli.mjs narrative --slug curio-s56 --answers docs/videos/curio-s56/review/r4-isolated-merged-answers.json --json`

It exited **0: PASS**, with 13 answers, no required failures, and no advisory failures. The [CLI verdict](r4-isolated-cli-verdict.json) hashes to `fc8923f00ddccae09a167b8c12d398fe790f870a2a1bbb8e2501c34fdcd8a58a`; the [round-1 receipt](r4-isolated-cli-receipt.json), copied from the isolated `/tmp` workdir, hashes to `17e3f4c6c4a261641b762d303ffc8d42a62cf6f7b9834bc8043e71ac8b99abe9`. The receipt binds narrative hash `dbc43879c1e8b46c`, script hash `1fffb9bdbfe548d8606434b7eaf16594bc85923088b42eeb5ce613a4275e320f`, panel rules SHA-256 `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`, and panel narration SHA-256 `70f7f6d2b6138d144ad8d05c66bc1a1cccb32d9772af168e636fdea326baaf8f`.

Any subsequent narration change gets new hashes and needs fresh independent readers; this R4 receipt remains a historical PASS for the R4 freeze only.
