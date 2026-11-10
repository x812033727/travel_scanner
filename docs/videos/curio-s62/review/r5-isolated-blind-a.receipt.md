# Curio S62 R5 isolated blind reader A

- Official 13-question panel SHA-256: `15cfd34356840ae8036c91bc9d8b29f210be52aa761f28379a2bd9ed263fa5ad`
- Script read SHA-256: `2d92a72e535f03b53c70c3aa3b52c218c035c1ee53eb1ca82d3d0a802a6cc091`
- Frozen raw ballot: `r5-isolated-blind-a.raw.json` (SHA-256 `b49e6575be0e6c319a6a09120d86dd9f0e6bec6693948fbaaaf49b6990f0ce9c`); original freeze at `/tmp/curio-s62-r5-blind-a-raw.md` has the same hash.
- Official bound record: `r5-isolated-blind-a.official-narrative.json` (SHA-256 `3929e5de443f38027f99daa45069ff6593a93a9b3900d9e8f56a8487ec00ce76`).
- Official CLI stdout: `r5-isolated-blind-a.cli-stdout.json` (SHA-256 `944aa287d394d21da7ddc7ae0ccb662aaa03b74d3efe00ab41fc51f85ba8347d`); stderr was empty.

The ballot was frozen before reading the official narrative CLI or schema. The CLI ran with an isolated workdir and exited 1 because two required answers were **No**. Its record reports `passed: false`, `round: 1`, `panel_rules_sha256: 5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`, and `panel_narration_sha256: 086d3daad13a5416a1f409b57034213a876c480b252b9cc6701b97a407ff3f01`.

| Failed question | Script-only reason |
| --- | --- |
| `no_spoiler` | `[s62006]` already says the later close light emerges after several hours; the body narrates that observation at `[s62075]`. The opening gives the later observation's result while holding back its explanation. |
| `no_recap` | `[s62057]` says a finer point appears after a few hours; `[s62058]` says the same point enters view after a few hours. The latter adds a note about how the book records time, but repeats the observation and timing. |

Verification after binding: all 114 spoken lines in the script matched the official CLI's rendered narration in order; panel question IDs and wording matched the supplied panel; `narrativeReviewMatches` returned `true`. No script edits or commits were made.
