# S53 R40 `s53030` second native image: independent claims-match paper review

2026-10-22 UTC. **PASS** for the claims-only visual annotation correction. I independently checked the exact current `s53030` row, the R40 second original and selected 1280×720 trim, fixed Survey D, the reversible diff, lint, STOP, and the 19 selected images. This paper review adds no media and changes no production file.

## Frozen inputs and exact reversal

| Input | SHA-256 |
| --- | --- |
| `video.json` (unchanged) | `65bec2d34c7d8443b9e45112e1193c6645feee86e676c0552d78b79f2335c312` |
| `script.md` (unchanged) | `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc` |
| `claims.md` (corrected) | `68c2ab442dd0b20daef0b39977360f6b03a0974132bfd5967d90a2a07db53a0c` |
| [Structured diff](r40-s53030-second-native-claims-match-structured-diff.json) | `c0ce1b1664bb39c039add808e24be468a9fc7359e918d62d1bd2f512121d6957` |
| `/tmp/s53-sf-relief/56217-0.txt` (fixed Survey D) | `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72` |
| `s53030-1.jpg` (original) | `35935d8a7dc06cc6ba40a64ca3bdea5c6be948d62031afe16b7803dd868b7de9` |
| `s53030-1-trim.jpg` (selected) | `4391aabeb46fe056953d83e881ba4ca579d1b7d39f5043303f44b05ac1d504b8` |

The structured diff names one change, `claims.md` `line:s53030`. Its new full row occurs exactly once in the current file; its old row occurs zero times. Replacing that one row with the recorded old bytes reproduces the prior full-file SHA-256 **`4e6ac59efe8a07e7159547cada6da853f0367dae125ee628643be94822664010`**. The current file, unchanged `video.json`, and unchanged `script.md` all match the diff's recorded hashes. The `s53030` narration, source URL, scene prompt, and camera did not change in this correction. In this preproduction checkout, the generic `建屋宣布、9 月施工及分散營地` annotation belongs to **`s53031`**, not to the old or new `s53030` row.

## Source and selected image

Survey D lines 4858–4865 says the cottages were built to replace tents, construction began September 10, 1906, 20 Hamilton Square cottages were completed September 16, and a considerable number would not be ready for refugees until at least two or three months later. The `s53030` spoken question asks how long people waiting to move into cottages must wait. The selected cartoon shows a grey-haired adult woman outside a canvas tent, looking toward two adult workers at a low, visibly unfinished timber cottage frame. It does not show an inhabitable cottage or identify a documented person or work site.

The revised row accurately describes those visible facts and says the exact age, plank attachment step, and work site cannot be determined. Utility wires and ordinary buildings are visible behind the camp; no modern road sign or suburban road is visible. The image's wires deviate from the unchanged prompt's exclusion, and the woman may appear older than its requested middle age, but neither fact contradicts the narration or Survey D. Handling the frame is legible even though attaching one specific board is not. The flat 2D cartoon style remains within the series look. Under [the illustration acceptance rule](../../../../.agents/skills/curio-episode/SKILL.md) lines 97–103, a judge-PASS image is kept unless it materially contradicts the narration/source or drifts in style. The independent visual verdict remains **HUMAN KEEP**; the claims wording now matches that verdict without adding unsupported historical particulars.

## Current gate

`node tools/video/cli.mjs lint --slug curio-s53 --json` exited 0 with **0 errors, 0 warnings, 126 lines**. `/workspace/.video-work/curio-s53/STOP` is present; `media/jobs.json` is empty (`{ "jobs": {} }`, SHA-256 `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3`). The current keyframe manifest SHA-256 is **`87c6150128b00a2a383d59ccc3ed450625c090877ad050a82abac3fade9c8ee3`**: exactly **19** entries, all judge-passed and not marked for review, with selected-file hashes matching disk. Its previous 18 entries match the saved pre-R40 manifest; the added `s53030` entry selects the trim above, request key `c7c01c95128e82d5`, judge **9.29 PASS**. The ledger SHA-256 is **`d8cddfc8aa1bac91ca9e20dc820ae3915921ea5c060878c12841c912cdfccbd9`**, totaling **US$0.7020 / 53 images / 52 judges / 0 reservations**, below the recorded US$4.78 ceiling.

**Verdict: PASS for this exact claims annotation correction and the 19-KEEP gate.** No image, judge, music, manifest, ledger, STOP, job, script, or video mutation was performed in this review.
