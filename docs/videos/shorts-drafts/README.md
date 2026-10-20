# Curio Shorts awaiting episode-directory claims

These are checked **draft scripts**, not built Shorts or upload packages. The episode directories below are still claimed by other in-progress tasks. Keep their claims intact. Once a claim is released or stale under `tasks/README.md`, the next producer should claim a narrow episode task, copy the corresponding JSON to `docs/videos/<slug>/shorts.json`, check the text against the then-current source notes and keyframe manifest, and run `from-episode --check` before building.

| Episode | Draft | SHA-256 | Check completed here |
| --- | --- | --- | --- |
| S02 草船借箭 | [curio-s02-shorts.json](curio-s02-shorts.json) | `94d225d91fe45a84669671fc16b0606d127a2de53cb9f8a1b4066a628f891f76` | Independent source readback: 《吳歷》 forbids random shooting; 《魏略》 describes arrows. 6 unique selected assets hash-bound. |
| S03 空城計 | [curio-s03-shorts.json](curio-s03-shorts.json) | `2c38a7dba7b803bfd9c1d9c1846e5d23108fccbc9baf74e1b2dfff7fe80753ca` | Independent source readback: 郭沖 passage has open gates and no zither; the novel has zither. 6 unique selected assets hash-bound. |
| S04 周瑜 | [curio-s04-shorts.json](curio-s04-shorts.json) | `785bf4aaf6aa0938f1085d134d98c3c734418d532766016edbdf302e47bc69de` | Independent source attribution readback after revision; 7 selected assets hash-bound. |
| S23 哈里森 | [curio-s23-shorts.json](curio-s23-shorts.json) | `72c0b29274be8cd71456cd1aa9d5832a4f100e613c4c7ebd69353378138e06dd` | Independent source readback after adding the 30 geographical-mile unit; 6 unique selected assets hash-bound. |
| S30 玄奘 | [curio-s30-shorts.json](curio-s30-shorts.json) | `02823639a61f5dd91326513c222e3a15ad42663d8132fd0ddbf95d9485329906` | Independent source readback: later disciple biography attributes 李昌's torn notice; 6 selected assets hash-bound. |

Each JSON passed the one-Curio-Short schema check and `episodeShort`/`verifyEvidence` against the selected keyframes in `/workspace/.video-work/<slug>/keyframes/manifest.json` on 2026-10-20. This does not grant use of another task's directory. Duration, voice, audio checks, vertical crop, 13-item QA and YouTube source link have **not** been verified. A true long-video YouTube ID is required for the Short's full-video description link and package gate; do not insert a placeholder URL.
