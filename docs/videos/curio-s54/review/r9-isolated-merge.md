# S54 R9 isolated narrative merge

2026-10-20 UTC. Two frozen readers evaluated the R9 `script.md` SHA-256 `d3d85c6b69290596690a83e28acd8cdf95c07a912f25d98abc718f57406e20db` against the official 13-question panel. Their [A](r9-isolated-blind-a.json) and [B](r9-isolated-blind-b.json) raw answers are retained. B's `pass`/`line_ids`/`reason` fields were [normalized](r9-isolated-blind-b-normalized.json) to the CLI's `yes`/quoted `evidence` shape using only B's cited IDs and the frozen R9 script. `panelVerdict` evaluated each reader, then `mergePanelVerdicts` applied the repository's **any-reader-Yes** rule. The [audit](r9-isolated-merge-audit.json) retains both full verdicts and the official OR result.

| Question | Reader A | Reader B | Official OR |
| --- | --- | --- | --- |
| `scene_first` | Yes | Yes | Yes |
| `no_spoiler` | Yes | Yes | Yes |
| `one_line` | **No** | **No** | **No** |
| `no_toc` | **No** | Yes | Yes |
| `chapters_link` | Yes | Yes | Yes |
| `open_loops` | Yes | Yes | Yes |
| `payoffs` | Yes | Yes | Yes |
| `no_recap` | **No** | **No** | **No** |
| `chapters_are_events` (advisory) | Yes | Yes | Yes |
| `outro_no_next` | Yes | Yes | Yes |
| `opening_hooks` | Yes | Yes | Yes |
| `one_thread` | Yes | Yes | Yes |
| `no_detour` | **No** | Yes | Yes |

**Official merged verdict: FAIL, 11/13 Yes; required `one_line` and `no_recap` fail.** Both readers identify `s54082` reporting the next day's confusion before `s54083` moves back to January 10 and `s54089` again reaches January 11. Both also identify `s54146` as a closing restatement of the January cash solution. A additionally finds “回到” at `s54083` a narration instruction and the Shrewsbury workaround at `s54013–18` too long, while B passes those two questions; they therefore pass the official OR rule.

Command: `node tools/video/cli.mjs narrative --slug curio-s54 --answers docs/videos/curio-s54/review/r9-isolated-merged-answers.json --workdir /tmp/curio-s54-r9-isolated-merge --json`. It exited **1**, expected for two required failures. Frozen [merged answers](r9-isolated-merged-answers.json), [CLI verdict](r9-isolated-cli-verdict.json), and [receipt](r9-isolated-cli-receipt.json) show round 1, `passed: false`, `failed: ["one_line", "no_recap"]`; panel rules SHA-256 `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`.

| Artifact | SHA-256 |
| --- | --- |
| A raw JSON | `1df5c53b229b08d4b03ccb1c03aa143ab03cb55fa60870a89c796327947f7a0f` |
| B raw JSON | `99cafabd1a48464f065c7169ff4be331d89c3dd656eafe5e5a1ac076f467b06b` |
| [B normalized](r9-isolated-blind-b-normalized.json) | `31195acaf2bde69190373ca8b87f6ec78f1a61afe082ca569967aca1f39d693d` |
| [Merge audit](r9-isolated-merge-audit.json) | `537953db7219d2913425df74e6f8da040bc00d2e459bc9e3ec5da6170e6318cc` |
| [Merged answers](r9-isolated-merged-answers.json) | `2f0a008465e388b41386a0f561fedff583843730fff9405c14b998263cf28c96` |
| [CLI verdict](r9-isolated-cli-verdict.json) | `a50e84b5bc0288048310de09a4a194674bdc16feecc5166d6cbc9d4fbe6ba4f7` |
| [CLI receipt](r9-isolated-cli-receipt.json) | `2c62baa079e31b26a3b52593d6f06666604f30c8b6e24c70c37e00b8151efc0d` |

The R9 author inputs were not edited for this merge.
