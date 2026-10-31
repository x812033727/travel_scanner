# S54 R4 isolated narrative merge

## Frozen independent reads

Both readers reviewed the same `script.md`, SHA-256 `cef9c47c8a7bc980b327e4753041821a7e35ac2b9fe1ec17581f70441ea40b2d`, against the official 13-question `NARRATIVE_PANEL`. Reader B froze its [raw JSON](r4-isolated-blind-b.json) and [Markdown](r4-isolated-blind-b.md) before opening A's [raw JSON](r4-isolated-blind-a.json) or [Markdown](r4-isolated-blind-a.md). The script hash still matched after the merge.

| Reader | Raw JSON SHA-256 | Individual score |
| --- | --- | --- |
| A | `5f708fd7ab2ac19b3493807ffba84711cada065463df0fd52d59ebe3be65d18a` | 9/13 Yes; 4 required No |
| B | `9f44e86d791f672d535d09b5c1c4c35322970e6ea42f5433bd2142c20e1969ea` | 8/13 Yes; 5 required No |

## Official OR result

The frozen Yes/No judgments were normalized to the official `{"answers": [{"id", "yes", "evidence"}]}` shape. Each answer's first cited scene was quoted verbatim from the CLI narration; B's `outro` citation maps to CLI line `s54997`. All 149 spoken lines in the CLI narration matched the frozen script (146 numbered scenes and three outro lines). Normalization changed no judgment. `panelVerdict` checked each reader, then `mergePanelVerdicts` applied the official any-reader-Yes rule. The [audit](r4-isolated-merge-audit.json) retains both normalized reader verdicts, their evidence, and the full OR result. The [merged CLI answers](r4-isolated-merged-answers.json) contain the resulting 13 Yes/No answers.

| Question | A | B | OR |
| --- | --- | --- | --- |
| `scene_first` | Yes | Yes | Yes |
| `no_spoiler` | No | No | **No** |
| `one_line` | Yes | No | Yes |
| `no_toc` | Yes | Yes | Yes |
| `chapters_link` | Yes | Yes | Yes |
| `open_loops` | Yes | Yes | Yes |
| `payoffs` | No | No | **No** |
| `no_recap` | No | No | **No** |
| `chapters_are_events` | Yes | Yes | Yes |
| `outro_no_next` | Yes | Yes | Yes |
| `opening_hooks` | Yes | Yes | Yes |
| `one_thread` | Yes | Yes | Yes |
| `no_detour` | No | No | **No** |

The shared failures are concrete: [s54006] reveals the later missing-word distribution result [s54119]-[s54121]; [s54113] asks about direct sales at three general post offices but [s54114]-[s54116] never resolves the decision; [s54058] and [s54060] repeat the unused-stamp rule, while [s54111] and [s54116]-[s54118] repeat May dates; and [s54024]-[s54028] plus [s54068]-[s54069] branch into reform history and extra charges without advancing the cash-to-stamp delay. A and B disagree only on `one_line`: A sees one chronological reform story; B finds that [s54111]-[s54118] advances to 6 May, backs up to 1 May, then returns to 6 May. The OR rule passes that item while preserving B's concern.

**Merged verdict: FAIL, 9/13 Yes, four shared required No.** Hold the R4 narrative release gate and review a revised script under a new hash.

## CLI receipt

Command: `node tools/video/cli.mjs narrative --slug curio-s54 --answers docs/videos/curio-s54/review/r4-isolated-merged-answers.json --workdir /tmp/s54-r4-isolated-workbase --json`

The CLI exited **1**, its expected result for failed required questions. Its [verdict](r4-isolated-cli-verdict.json) reports those four No items; the copied [receipt](r4-isolated-cli-receipt.json) records round 1, `passed: false`, narrative hash `b8a8969eb0bfc61b`, panel rules SHA-256 `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`, and panel narration SHA-256 `261bed7062944fdb76c6b044a4e4e096a97523552d4b6e8bbdc6c2da052f034d`.

| Artifact | SHA-256 |
| --- | --- |
| [Merge audit](r4-isolated-merge-audit.json) | `8d8187f4e33de165d314de4892da230f2511eb3f8075571e9062cfdc25f953ac` |
| [Merged answers](r4-isolated-merged-answers.json) | `f00ba7d8aa5d0826495e4e4ba42395e7fb1a4e3483937a87467d82212caac126` |
| [CLI verdict](r4-isolated-cli-verdict.json) | `7a4b973f926f8b1ae619e49dc2fe8f7633a6d870a649e07ed3cb24ab83ebc426` |
| [CLI receipt](r4-isolated-cli-receipt.json) | `6f1efdc4493127a678cf8e4a9fda237dc695db3f2ccea569cdb6e1616f0ffd98` |

No script or paid media was edited.
