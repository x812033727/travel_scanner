# S49 R9｜六句音訊旗標的作者窄修與凍結

2026-10-20 UTC。接續 [R8 完整音檢](verify-11.md)的 136/136 檢查及兩輪定點補錄（旗標 21 → 8 → 6），只改 `moon011/012/015/026/030/100` 六句旁白，逐字同步 `claims.md`，用 CLI 重生 `script.md`。沒有改動其餘旁白、`loops`、分鏡提示詞、字卡、來源清單、聲音設定或說明欄；沒有重新合成語音或執行付費媒體、政策、正式自評。R8 的既有 WAV 與音檢仍綁定舊 speech hash，不可當成 R9 通過音訊關的證據。

| ID | R8 轉錄旗標 | R9 修法及固定來源界線 |
| --- | --- | --- |
| `moon011` | 「遠行」聽成「遠航」 | 改說赫歇爾到好望角研究北方難觀察的南天星區；真實南天工作只依 1902 雅各比評論 [P06](research.md)，不冒充赫歇爾原信。 |
| `moon012` | 「報紙借走」聽成「伴著節奏」 | 分成真實雙星／星雲觀測與《太陽報》拿它當故事背景兩句；仍依 P06，沒有把虛構月面發現算成真觀測。 |
| `moon015` | 「真名」聽成「聲明」 | 明說標題寫上名字，再問能否證明後面的發現；不暗示赫歇爾發過證實聲明。[P03](research.md) 是 1859 重印的虛構文章。 |
| `moon026` | 「增刊、助手」連成「增刊著者」 | 說成報導提到的增刊、格蘭特來信及皇家學會文件，問讀者能查哪一份；[P02／P03](research.md) 只支持文章自稱，沒有新增原件。 |
| `moon030` | 「鏡筒」聽成「鏡頭」 | 改用望遠鏡沉重的管子；仍以「故事先安排」限定 [P05](research.md) 的虛構對話。 |
| `moon100` | 「早晨聚住陽光」聽成「造成聚焦陽光」 | 分句說鏡片沒放平、日出後集中陽光；仍以「報導說」限定 [P12](research.md) 的虛構火災。 |

固定全文仍是 Locke 名下 **1859 重印本** L SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`，以及 Jacoby **1902 後出評論** J SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029`。未開到 1835 原報、赫歇爾原信或獨立發行帳；沒有改寫 1859 出版者序及反應選錄的歸屬。

| R9 固定檔 | SHA-256 |
| --- | --- |
| `brief.md` | `eb622b1471461f61a213a66c2bf646274e0e4887c82e102bea83ef2aa4aaea0e` |
| `research.md` | `3574780b890d96ce436af3b1542cc153cc3de4231e93c8fdaff87740fd0783f3` |
| `claims.md` | `34d270d19c80e8c5f81112e32ac2e79dde386839339cf708276a0626b7c8aa92` |
| `script.md` | `10f912c63ba438c676372469e8e44a52a8252113efc22f3af9fb74f91ae22354` |
| `video.json` | `547409b2cb87e1ea5ba0133e3c140aa15ba4cce793e26a55d0cbde49fe1bb396` |

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs script --slug curio-s49` 已重生劇本（narrative `b78ecac3fbd4b17c`；speech `4a981607764aff19`）。逐欄機械比對 R8：JSON 僅六句 `text` 改動；133 行 claims 僅同六句旁白改動，其來源及畫面欄均同文；136/136 句與 CLI 劇本逐字同序，ID 唯一，11 個 loop 端點有效。133 個編號景仍為 126 `shot`、7 `big`，片尾三句不動。前八景開場 176 spoken units，按偏快的 325 units／分鐘估 **32.49 秒**；正文 2,729 units，同速估 **503.82 秒（8:23.82）**。這是文字估時，不是新稿的 TTS 實長。

`lint --slug curio-s49 --json`：**0 errors／0 warnings、136 lines**。`npm run test:docs-videos`：**236 pass／0 fail**。`npm run check:tasks`：**退出碼 0、2,124 票**，另有倉庫其他票既有 stale／scope overlap 提醒。`git diff --check -- docs/videos/curio-s49` 通過。

**R9 狀態：作者稿已凍結，音訊關 HOLD。** 新 SHA 要交由另一位工作者按固定 L／J 原文差分重核六句與書面畫面，再用新稿做正式敘事與後續必要關卡。舊 R8 音檔不能代表 R9；受影響句子與 136/136 完整音檢仍待，零旗標及必要核准前不進入插畫、配樂或成片。
