# R4 formal blind reader B

Raw answers were frozen after reading only the official 13-question panel and the frozen narration script, in that order. No episode isolation breach. The panel, script, and video file SHA256 values were verified after the raw freeze. See `r4-formal-blind-b.isolation.json` for the read order.

- Official panel SHA256: `15cfd34356840ae8036c91bc9d8b29f210be52aa761f28379a2bd9ed263fa5ad`
- Script SHA256: `8343a4f903fe4b405b1e6364cd67737ed7f3aead625b5fe713bf91c873c05c14`
- Video SHA256: `abed73ef3b14dcfc1b8ff1804f0234919d2f03cffa70a0b4c901a72ce6b14f92`
- Raw answers SHA256: `1223c931f7ea19261ca0035c5b144a33c3234e523083d677746f264e7d32a75d`
- Official record SHA256: `fb74f4e43544f0fbec2d08de0e6cb91d322f944ac5a8f2dd9b0b137076e839f0`
- Score: **8/13 Yes**; required checks **7/12 Yes**; optional checks **1/1 Yes**. Official CLI verdict: **FAIL**.

Required No votes and line evidence:

- `one_line` — `s62084` explicitly returns to the first night after the story has reached later dates and repeats the missing-point uncertainty.
- `no_toc` — `s62084` announces a move back to the first night's three points, a narration-structure cue.
- `payoffs` — `s62080` asks where two missing points went; `s62081` offers only Galileo's guess and explicitly labels it a contemporary interpretation. No clear later resolution follows.
- `no_recap` — `s62062` repeats the fact in `s62046` that the original book does not identify the missing point from the first night, without a recall cue.
- `no_detour` — `s62105`–`s62106` pause the changing-count problem to give the dedication name and explain that it was not an early numbering scheme.

The official CLI command was `node tools/video/cli.mjs narrative --slug curio-s62 --answers docs/videos/curio-s62/review/r4-formal-blind-b.raw.json --workdir /tmp/curio-s62-r4-formal-blind-b --json`. It wrote round 1, bound to narrative hash `dc5b230a7d70f26b`, script hash `1c69c6dd6ff7a44ca1332f4726b74e05fc83799bf68e2d651b684c2699aa1a77`, and panel narration SHA256 `65559d6c55df0c6e6b769330f1f9e44aa56e765393b3e3c49c01fa95378c201f`. Exit code 1 is the expected result for five required No votes. The generated record was copied to `r4-formal-blind-b.official-narrative.json`. The video and script file SHA256 values remained unchanged after the CLI run.
