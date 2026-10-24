# S51 R15｜政策及真實音訊零旗標；網站兩卡待審、插圖續畫仍停

2026-10-20 UTC。本收據只綁 [R15 作者五檔凍結](review/r15-author-freeze.md)。另一人對同版的[史料、逐句主張與書面畫面](review/r15-source-independent.md)均判 **PASS**；兩名真正隔離讀者的[官方 OR 合併](review/r15-isolated-merge.md)為 **13/13 PASS**。R14 的敘事、政策與語音回條不轉用為 R15 證據。

| 精確內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `bea6a0ff26ddfed12ee2b9d077b2359a12392c301bf9032c69e66a403337a0e3` |
| `research.md` | `039ca3ecc3f5099537e51e48d0f1788faf0bdf9c5d254f2ae64dd5ff89b56459` |
| `claims.md` | `78a401c52ca7b0bbf4393a4f354dab07393d454f852c38c21acc77d292f63a4b` |
| `script.md` | `cbc5a1891deacd029e081b61eb316e076e422cdb45ebceb4b072fa875e55ce83` |
| `video.json` | `7864bac6650ec3e632d174a20739bb9fa55954b284206c713d04a31f2a81a51a` |

## 政策與網站精確版

完整 `policyRequest` SHA-256 `edd2aa586de0145680adb8d42f8857196ea842a9ab9053c822d4faa9e98f5444`，對站台只呼叫一次；[政策原始回條及說明](review/r15-policy.md)記 `explainer` **PASS**，立場 `0.79`、示範不適用、建議 `0.01`、業配 `0.09`。站台讀回分類仍為 `explainer`。網站精確劇本卡 `9b619966-dec8-4bd1-a0a2-385f20fc9b39` 綁上述 `script.md` SHA；R15 旁白卡 `b8016f41-9924-4912-b5f3-63ef6ea71127` 綁下列 `timeline.json` SHA。兩卡都是 `hand_pushed: true`、`pending`；分別執行 `review-pull --gate script` 與 `--gate audio` 皆回 `waiting for the owner`。本地 `approvals.json` 的 R15 outline／script 項明記 **LOCAL delegated editorial selection**，不是網站人工核准；沒有本地音訊聆聽核准。

## TTS、完整音檢及實測

主工作目錄的 `STOP` 留在 `/workspace/.video-work/curio-s51/STOP`。為不解除插圖停手，先把已付費語音快取與舊轉錄複製到 `/tmp/s51-r15-audio/curio-s51`，在該隔離目錄執行 `tts --dry-run`、`tts`、`check-audio`。dry run 得 **131** 請求、**5** 句需新合成（`cal058/091/103/134/135`）、估 **97** 計費字；實際 **5** 句合成、**126** 句沿用、**97** 計費字，沒有 fallback。一次完整 `check-audio` 核 **131/131** 現稿句：**114** 逐字相合、**14** 同音／語助差異、**3** 由既有 Jev 判可接受、**0 原始旗標／0 未查**。本輪只新轉錄 5 句、Jev 新呼叫 0 次；**無需定點重錄**。`review/check.json` 仍保留 3 筆舊稿 ID，原檔共 134 鍵；用現行時間軸與音檔雜湊篩選是 **131/131**，統計沒有混入舊行。

| R15 音訊檔（已裝回主工作目錄） | SHA-256 |
| --- | --- |
| `narration.wav` | `7df974a903ba671b05312599c525c070a4f8d74454e90adb2a2e2ddc08a98c0c` |
| `timeline.json` | `2c431b002119cecd79744cb425b064786d97a7b8c753cfc3c0d0c094cdf8088b` |
| `review/check.json` | `bfef2b3552dc59a48d8693629ee74b62beba7e4f33a5743566f0de4d305f81e8` |
| `review/check-flags.json`（`flags: []`） | `899c0293418872d7c520808fed1ef581d5eb2591435314a69c51832acfe8abd3` |
| `audio/cache.json` | `3345f30919310474a2fec9d8d391ff9fc1c569117a45a908ca184da573e6338d` |

五個新 WAV SHA-256：`cal058` `c2f7cff0e6f8b709b2e49379d5a27d5e7ebcedb32ddff1b7724ef3ac7acb1a8f`；`cal091` `bc881f8ccbd6f09fad694237fc5f4b325e232b9806e3a1257818511ab41d7aa0`；`cal103` `efdea75ef763a382f7397bcc7e358095909270f7fd3b2ee9bcb5fba1ce1593c8`；`cal134` `6ef5a47dcb6eef459a9c8f8124ce5deec9af4a4303938a8e131b108bf8fce098`；`cal135` `d096a552968b8dc7bea83271a23b79b2055d9c0d104faa98a3fd68fa3579fbc2`。`timeline.json` 與零旗標檔的 `speech_hash` 都是 `becca77be007279e`；`audioEvidenceProblems` 回空陣列，整個主目錄 `audio/` 與隔離 R15 目錄逐檔一致，語音日誌沒有未結請求。

按 30 fps 的現稿時間軸，開場 `cal001–008` **47.63 秒**；開場後到片尾前正文 `cal009–132` **645.07 秒／10:45.07**，高於 480 秒下限；片尾旁白 **13.53 秒**；全旁白 **706.23 秒／11:46.23**，`ffprobe` 為 706.233333 秒。21 秒 `v4-endscreen` 尚未合成，不能把旁白時長稱為成片時長。

主目錄恢復時只以逐檔 SHA 比對後原子替換 **5 個變動 WAV、cache、narration、timeline、check、flags、R15 narrative 回條**，並把兩筆新 TTS／音檢狀態併入原 `state.json`；未動 `STOP` 或插圖檔。舊 R14 `narration.wav`（SHA `6ec4d04de19d0bb5863da639cde62e89e9176be5817df5f795e5cc77addbcc95`）連同當時時間軸、音檢、快取與五個覆寫前 WAV 暫存在 `/tmp/s51-r14-audio/curio-s51`。主目錄的 keyframes manifest SHA 仍為 `da83761083263963f085c501e98d9b1621b2e427a6fd39ac0ed2622e9088693b`，70 個 keyframe 檔案名稱集合未變；`STOP` 仍存在。

**媒體關卡：**R15 `visual_hash` `0c86b0932e41484e` 使 R14 manifest 過期。首 23 景現有素材只有 20 景在**自動評審**有通過選圖；`cal008/010` 還是 `needs_review`，`cal023` 仍 `incomplete`。其後的[首 23 景原圖目視覆核](review/r15-native-art-audit.md)另判可收 10、退圖 5、待定 7、未完成 1，不能以自動評審替代原圖驗收。插圖、配樂、成片、字幕與 Studio 可點元素均未完成或驗收；待主責者獨立檢查零旗標收據並決定後續，勿以本收據解除 `STOP`。

`brief.md` 末段仍用舊時態描述 R14 後續及 132 句計畫；本輪為保持五檔凍結與政策請求的精確綁定，沒有改該段。R15 製作數字以本收據的 131 句與實測時間為準；若修訂企劃文字，須重新凍結五檔並重綁後續關卡。
