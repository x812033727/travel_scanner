# S55 R3 isolated narrative merge

Two readers independently froze [A](r3-isolated-blind-a.md) and [B](r3-isolated-blind-b.md) against the same `script.md` SHA-256 `0e8365605d1d01c6199d74843a31f59b1430dbbc56d5b19efb9922c0feb7b619` and the official 13-question panel. A answered 5 Yes; B answered 6 Yes. Their raw reviews were preserved without edits. The script hash remained the same after merging and after the CLI run.

The frozen Yes/No columns were parsed into the panel's answer shape. Each normalized evidence field quotes a line verbatim from the official CLI narration, with its bracketed line ID and estimated start time. Where a script block contains two spoken sentences, the CLI assigns the second a new ID: A's tether sentence maps to `[s55004]`, A's repeated no-passenger sentence to `[s55052]`, and B's ticket question to `[s55134]`. These citation corrections changed no judgment. The [merge audit](r3-isolated-merge-audit.json) retains both normalized answers, both `panelVerdict` results, and the `mergePanelVerdicts` OR result; the [merged answers](r3-isolated-merged-answers.json) are the input to the CLI.

| Official question | A | B | OR |
| --- | --- | --- | --- |
| `scene_first` | Yes | Yes | **Yes** |
| `no_spoiler` | No | Yes | **Yes** |
| `one_line` | No | No | **No** |
| `no_toc` | No | No | **No** |
| `chapters_link` | No | No | **No** |
| `open_loops` | Yes | Yes | **Yes** |
| `payoffs` | No | No | **No** |
| `no_recap` | No | No | **No** |
| `chapters_are_events` (advisory) | Yes | Yes | **Yes** |
| `outro_no_next` | Yes | Yes | **Yes** |
| `opening_hooks` | Yes | Yes | **Yes** |
| `one_thread` | No | No | **No** |
| `no_detour` | No | No | **No** |

**Official OR result: FAIL, 6/13 Yes and seven shared required No.** The seven failures are:

- `one_line`, `one_thread`, `no_detour`: `[s55122]` answers the November tree and free-flight mystery, then `[s55124]` begins a separate December hydrogen-balloon flight. Its carriage view, ticket drawing, landing, and balloon-type comparison occupy a long new arc after the opening difficulty is settled.
- `no_toc`: `[s55009]` announces “these three questions” and says which balloon story to start with.
- `chapters_link`: `[s55078]` starts with apparatus details after `[s55077]` promises an accident; the tree does not appear until `[s55086]`. `[s55124]` starts a new crew after `[s55123]` merely says Franklin's notes are unfinished.
- `payoffs`: `[s55134]` asks what suspension was actually used, while `[s55135]` only says the altered ticket drawing may not match it. No later line gives the answer.
- `no_recap`: `[s55015]` says the August balloon had no passenger; `[s55052]` repeats that fact without an explicit callback.

Readers disagree only on `no_spoiler`. A reads `[s55004]` and `[s55005]` as prematurely revealing that the opening tree incident was a tethered test, later restated at `[s55095]`. B reads the tether as part of the immediate scene and finds the later free-flight result still open. The official any-reader-Yes rule passes this item; the dissent remains in the audit and raw reviews.

## CLI record

Command: `VIDEO_WORKDIR=/tmp/curio-s55-r3-isolated node tools/video/cli.mjs narrative --slug curio-s55 --answers docs/videos/curio-s55/review/r3-isolated-merged-answers.json --json`

The CLI exited **1**, its expected result for required No answers. Its [verdict](r3-isolated-cli-verdict.json) matches all 13 merged Yes/No answers and reports the same seven failures. The copied [receipt](r3-isolated-cli-receipt.json) is round 1, `passed: false`, with narrative hash `71bddb52db1e48de`, panel-rules SHA-256 `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`, and panel-narration SHA-256 `c39c37661be379c940c6854b8ce05e04f1605a236215853a44c5e9570ab7fb9b`.

| Archived artifact | SHA-256 |
| --- | --- |
| [Raw A](r3-isolated-blind-a.md) | `18dca2217390c7573320d2574d9346e27b26b4c06761a4e5522bc8a96870fc84` |
| [Raw B](r3-isolated-blind-b.md) | `8d2c22ae434329b0cae1289d4286ef011806cd3533599c3d00417354850230ac` |
| [Merge audit](r3-isolated-merge-audit.json) | `109ac86efcdd37e195ceb28f10847e80d56aac147f9b1dcfe864c0180085b039` |
| [Merged answers](r3-isolated-merged-answers.json) | `d39af554d4501ccd636a43f1c8733a22a602f9ccd752b4853c069569f80afa2e` |
| [CLI verdict](r3-isolated-cli-verdict.json) | `904f966890dc1728f835a5cb4bc0625adec1140e4e57c31c4447a9294274b777` |
| [CLI receipt](r3-isolated-cli-receipt.json) | `45f346f187daba5659a717e80983f81358607bf69262bd143966425c6aa617ae` |

No script or media was changed. A revised script needs a new blind review under its new hash.
