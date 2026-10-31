# R15 isolated narrative merge

The script was frozen at SHA-256 `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`. Readers [A](r15-isolated-blind-a.json) and [B](r15-isolated-blind-b.json) separately answered the 13 official narrative questions using that script. B's decisions were saved before A's file was opened. Afterward, B's Markdown record was expanded to show every evidence string, and two quotation marks in B's JSON evidence were corrected to match the script exactly; no decisions changed.

| Check | A | B | Official OR merge |
| --- | ---: | ---: | ---: |
| Yes | 13 | 13 | 13 |
| No | 0 | 0 | 0 |
| Required failures | 0 | 0 | 0 |

`panelVerdict` accepted both readers' answers with bracketed line IDs; A's bracket format required no normalization. The merge used `mergePanelVerdicts(panelVerdict(A), panelVerdict(B))` from `tools/video/core/narrative.mjs`. For each question, the official policy returns yes if either reader supplies a valid cited yes. There were no disagreements. [The merge audit](r15-isolated-merge-audit.json) records both input hashes, all merged answers, and the 13 `yes_readers: 2` counts. [Merged CLI answers](r15-isolated-merged-answers.json) contain the accepted answer and citation for every question.

The CLI ran with `VIDEO_WORKDIR=/tmp/curio-s49-r15-isolated-b-final-20261020`:

```bash
node tools/video/cli.mjs narrative --slug curio-s49 --answers docs/videos/curio-s49/review/r15-isolated-merged-answers.json --json
```

It exited 0 and returned **passed: true**, 13 yes, no failed or advisory questions. The [CLI verdict](r15-isolated-cli-verdict.json) is the command output. Its [round 1 receipt](r15-isolated-cli-receipt.json) was copied from `/tmp/curio-s49-r15-isolated-b-final-20261020/curio-s49/review/narrative.json`; it binds the verdict to `panel_rules_sha256` `5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75` and `panel_narration_sha256` `948b8f8ba77051fe6a6155b22dd00de0f6eaa4c1f670d221e0f55a303911cf04`. A `status --slug curio-s49` check using the isolated workdir reported `storytelling panel: passed`.

This is a narrative verdict on the frozen script. No script or media files were edited for this review.
