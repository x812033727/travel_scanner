# Curio S51 R15 isolated narrative merge

## Frozen independent reads

Both readers reviewed `docs/videos/curio-s51/script.md` at SHA-256 `cbc5a1891deacd029e081b61eb316e076e422cdb45ebceb4b072fa875e55ce83`. Reader B wrote and hashed its [JSON](r15-isolated-blind-b.json) and [Markdown](r15-isolated-blind-b.md) before seeing reader A's frozen answer.

| Reader | Frozen JSON SHA-256 | Individual result |
| --- | --- | --- |
| [A](r15-isolated-blind-a.json) | `8a15530414dd42113feb6f6efcd3929b8201a42feedaf4eb44693e4eb162b687` | 13 Yes / 0 No |
| [B](r15-isolated-blind-b.json) | `f5852787e963d9fd5e8df1aba4dd18fb9b80027d4c5d2c306374e7d9c35745d8` | 12 Yes / 1 No |

## Official OR merge

Each frozen `pass` field was mapped to the official `yes` field, then each reader was checked with `panelVerdict` and combined with `mergePanelVerdicts` from `tools/video/core/narrative.mjs`. A's frozen scene IDs were prefixed in square brackets to its evidence because its evidence text did not itself contain bracketed IDs; this is a format adaptation of A's recorded citations, not a change to either frozen verdict. The [audit](r15-isolated-merge-audit.json) contains the two normalized official verdicts and the OR merge. The [CLI answer file](r15-isolated-merged-answers.json) contains the resulting 13 answers.

| Question | A | B | OR merge |
| --- | --- | --- | --- |
| `one_line` | Yes | Yes | Yes |
| `no_recap` | Yes | **No** | Yes |
| Other 11 | Yes | Yes | Yes |

The two readers agree that the late July inquiry [cal107] follows the night and dawn events [cal009]-[cal105]. Its timing comparison [cal108]-[cal114] supplies a new identity finding; the story does not return to recount the night's events in a second chronological block. The sole disagreement is `no_recap`: B finds that the dawn arrival is stated in the opening [cal007] and again in the body [cal098] without the explicit callback required by the rubric's teaser exception. A treats the later rementions as story development and finds no repeated fact that fails the question. The official OR rule makes `no_recap` Yes while preserving B's No in the audit.

## Isolated CLI receipt

Command: `VIDEO_WORKDIR=/workspace/.video-work/r15-isolated-b node tools/video/cli.mjs narrative --slug curio-s51 --answers docs/videos/curio-s51/review/r15-isolated-merged-answers.json --json`

The command exited **0: PASS**. The [CLI verdict](r15-isolated-cli-verdict.json) reports 13 Yes, no failed required questions, no advisory questions, and no problems. The [CLI receipt](r15-isolated-cli-receipt.json) is the round 1 snapshot from `/workspace/.video-work/r15-isolated-b/curio-s51/review/narrative.json`, SHA-256 `b030ec26f02e1a681f1e517085c470b89fae9b7836915adcd9cd08d555931ff4`. It records narrative hash `1c1f567a24f26cbf`, script hash `2c4c1edca17ea9c4f01ba4edc5b0878628f6863b50f1f94c3cdc3b1ebe581e17`, and panel narration SHA-256 `23dac21506e43b33da91874eeca40c3c5150b9a9b2c2f4fa491c2ce96faed40c`.

The script still matches the frozen SHA-256. No script or paid media was changed.
