# S54 R8 isolated narrative merge

2026-10-20 UTC. Two frozen readers evaluated the R8 `script.md` SHA-256 `b9981a1b503504e48b452b2a37ddc42731ee7a4bcc6096dd6d7f79ec9d25438c` against the official 13-question panel. Their [A](r8-isolated-blind-a.json) and [B](r8-isolated-blind-b.json) machine-ready answers were passed unchanged to `panelVerdict`; `mergePanelVerdicts` then applied the repository's **any-reader-Yes** rule. The [audit](r8-isolated-merge-audit.json) retains both full verdicts and their official OR result.

| Question | Reader A | Reader B | Official OR |
| --- | --- | --- | --- |
| `scene_first` | Yes | Yes | Yes |
| `no_spoiler` | Yes | Yes | Yes |
| `one_line` | Yes | Yes | Yes |
| `no_toc` | Yes | Yes | Yes |
| `chapters_link` | Yes | Yes | Yes |
| `open_loops` | Yes | Yes | Yes |
| `payoffs` | Yes | Yes | Yes |
| `no_recap` | **No** | **No** | **No** |
| `chapters_are_events` (advisory) | Yes | Yes | Yes |
| `outro_no_next` | Yes | Yes | Yes |
| `opening_hooks` | Yes | Yes | Yes |
| `one_thread` | Yes | Yes | Yes |
| `no_detour` | Yes | **No** | **Yes** |

**Official merged verdict: FAIL, 12/13 Yes; only `no_recap` fails.** Reader A says `s54084` repeats the cash-prepayment point at `s54078`; Reader B adds that `s54085` rephrases the collection benefit already given at `s54031–32`. Reader B also finds `s54140–43` a cancellation detour, while Reader A judges it part of the same payment story. The latter item passes the official OR rule, but can be shortened in a later revision.

Command: `node tools/video/cli.mjs narrative --slug curio-s54 --answers docs/videos/curio-s54/review/r8-isolated-merged-answers.json --workdir /tmp/curio-s54-r8-isolated-merge --json`. It exited **1**, expected for a required failure. Frozen [merged answers](r8-isolated-merged-answers.json), [CLI verdict](r8-isolated-cli-verdict.json), and [receipt](r8-isolated-cli-receipt.json) show round 1, `passed: false`, `failed: ["no_recap"]`; panel rules SHA-256 `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`.

| Artifact | SHA-256 |
| --- | --- |
| A raw JSON | `4df4d6db79ea56fdc742ed0fa8da79f328e5d42522b63f33f6707cce89431031` |
| B raw JSON | `2944d71b209d418bf817ab857fd7891cc8cb242e2a2c98a4fa4ea22de16fe211` |
| [Merge audit](r8-isolated-merge-audit.json) | `3ba8984c2112ad1534f74a557b72f1145ef9bb607a3875b45af2f8d6a9969cba` |
| [Merged answers](r8-isolated-merged-answers.json) | `4096853d2c37442b1248a4a890da6f39c96edefa19ace7e7a87ba217eec542b8` |
| [CLI verdict](r8-isolated-cli-verdict.json) | `87d0a98e25cbe919638014eb7708374bf32910ce471e96f685549424d47f3d7c` |
| [CLI receipt](r8-isolated-cli-receipt.json) | `ed293fae83aa2cb9a787f6913b45c36422e704ff01695ab8bad94345a4edefa3` |

The R8 author inputs were not edited for this merge.
