# Curio S51 R14 isolated narrative merge

## Frozen readers

Both readers answered the same 13 official questions against `docs/videos/curio-s51/script.md` SHA-256 `d8d8a8c726a4849bb2320af9556a63b32e40f99076adc42f1833f481de2e8fbf`, before comparing answers. Reader B read only the script and official question list before freezing its answer files.

| Reader | Frozen answers | SHA-256 | Yes / No |
| --- | --- | --- | --- |
| A | [r14-isolated-blind-a.json](r14-isolated-blind-a.json) | `426cf644ac6f7eedfc6d63f326673ceccf4a038e249d87da8387d38a44539810` | 12 / 1 |
| B | [r14-isolated-blind-b.json](r14-isolated-blind-b.json) | `170de92764106ece7742df229b2c83e49a13e031a0c526314a33fb40e960273c` | 11 / 2 |

## Official OR merge

`mergePanelVerdicts` in `tools/video/core/narrative.mjs` makes a question Yes when either reader gives a cited Yes. Both frozen answers were passed through `panelVerdict` and then through that official function; the [full audit](r14-isolated-merge-audit.json) retains each reader's verdict. The resulting [13 merged answers](r14-isolated-merged-answers.json) have SHA-256 `9796ddc50730c6f84f27d982c5e3e6501aae289124ecb1c4ef34cbd41aca5aa1`.

| Question | A | B | Merged |
| --- | --- | --- | --- |
| `one_line` | No | No | **No** |
| `no_recap` | Yes | No | Yes |
| Other 11 | Yes | Yes | Yes |

The shared failure is the return to the same nighttime report after the story has reached the July inquiry. [cal077]「二副史東說，他約一點十分已向船長報五枚。」 and [cal090]「他說自己只聽過一枚」 have already told that exchange; after [cal107]「到了七月底，英國正式調查報告逐一對照船橋證詞。」 the script returns at [cal134]「還記得史東通報火箭嗎？他說船長還交代了什麼？」 and [cal135]「史東說，船長讓他有新消息就派實習生來報；當下沒有起航指示。」 Reader A and B both found this late return incompatible with `one_line`.

For `no_recap`, B separately flagged [cal058]「較近的加州人號呢？」 followed immediately by [cal059]「那艘更近的加州人號，此刻有人在耳機旁嗎？」 as a repeated relative-distance fact. A answered Yes, pointing instead to distinct meanings of the two eight-rocket figures and to an explicit later callback. The official OR therefore records `no_recap` as Yes while retaining B's objection in the audit.

## Isolated CLI result

Command: `VIDEO_WORKDIR=/workspace/.video-work/r14-isolated-b node tools/video/cli.mjs narrative --slug curio-s51 --answers docs/videos/curio-s51/review/r14-isolated-merged-answers.json --json`

The CLI exited **1** and recorded **HOLD / FAIL**: 12 Yes, one required No (`one_line`), `advisory: []`, and one problem. The [CLI verdict](r14-isolated-cli-verdict.json) is the command output; the [CLI receipt](r14-isolated-cli-receipt.json) is a snapshot of `/workspace/.video-work/r14-isolated-b/curio-s51/review/narrative.json` at round **1**, SHA-256 `51595d23c4d127e388db866cbce23e1de88661dc1ec4d0dce72c4d898fd9dde0`. The receipt binds narrative hash `04924dac375124f2` and panel narration SHA-256 `6c6bdb1d743b1ba193caaaa21127d63ec69bce0696e0787fe870fa489a1e67bb`.

The script remained at its frozen SHA-256. No script or paid media was changed.
