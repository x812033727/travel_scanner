# S54 R7 isolated narrative merge

2026-10-20 UTC. Two frozen readers evaluated the R7 `script.md` SHA-256 `3c8f44af5d1af7a8f5c65e71e8866faa12d32ff0ff09e89f408291b132791684` against the official 13-question `NARRATIVE_PANEL`. Their machine-ready [A](r7-isolated-blind-a.json) and [B](r7-isolated-blind-b.json) answers were passed unchanged to `panelVerdict`, then `mergePanelVerdicts` applied the repository's **any-reader-Yes** rule. The [audit](r7-isolated-merge-audit.json) retains both reader verdicts and the merged result; [merged CLI answers](r7-isolated-merged-answers.json) retain the exact 13 Yes/No cells submitted to the command.

| Question | Reader A | Reader B | Official OR |
| --- | --- | --- | --- |
| `scene_first` | Yes | Yes | Yes |
| `no_spoiler` | Yes | Yes | Yes |
| `one_line` | Yes | Yes | Yes |
| `no_toc` | Yes | Yes | Yes |
| `chapters_link` | Yes | Yes | Yes |
| `open_loops` | Yes | Yes | Yes |
| `payoffs` | **Yes** | No | **Yes** |
| `no_recap` | **No** | **No** | **No** |
| `chapters_are_events` (advisory) | Yes | Yes | Yes |
| `outro_no_next` | Yes | Yes | Yes |
| `opening_hooks` | Yes | Yes | Yes |
| `one_thread` | Yes | Yes | Yes |
| `no_detour` | Yes | Yes | Yes |

**Official merged verdict: FAIL, 12/13 Yes; only `no_recap` fails.** Both readers identify the repeated printing status at `s54075` and `s54104`. Reader B also finds the `s54110` question “who opposed” insufficiently answered by `s54111`'s unnamed “department”; Reader A judged `payoffs` Yes, so that item passes the official OR rule. The writer may still narrow that question and answer in a new revision.

Command: `node tools/video/cli.mjs narrative --slug curio-s54 --answers docs/videos/curio-s54/review/r7-isolated-merged-answers.json --workdir /tmp/curio-s54-r7-isolated-merge --json`. It exited **1**, expected for the required `no_recap` failure. The frozen [CLI verdict](r7-isolated-cli-verdict.json) and [receipt](r7-isolated-cli-receipt.json) show round 1, `passed: false`, `failed: ["no_recap"]`; panel rules SHA-256 `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`.

| Artifact | SHA-256 |
| --- | --- |
| A raw JSON | `521fae49e3438b2d1b1966887da918ef77b8a10505ed210285508817b9d00c6a` |
| B raw JSON | `51c25af705645641a8969b5c73812c051d0828ec0153edc306b7c6fdc8b62e81` |
| [Merge audit](r7-isolated-merge-audit.json) | `c568ff58ea890167243fb94069c5337ff055a0d71539d9edb5a853f586eff0b5` |
| [Merged answers](r7-isolated-merged-answers.json) | `e89663f88666bb11dd041fe08f4c388e93a89e916e420f4844c6acafc6178c94` |
| [CLI verdict](r7-isolated-cli-verdict.json) | `f22a7e4fab352f1fcf06de6a18550fa873d34ba7921a39bf08aaf81430fa9737` |
| [CLI receipt](r7-isolated-cli-receipt.json) | `ef8673c1192e8c04bf04fe9b0470a1849d8d103800107312abb3517e65ee6abb` |

The R7 author inputs were not edited for this merge.
