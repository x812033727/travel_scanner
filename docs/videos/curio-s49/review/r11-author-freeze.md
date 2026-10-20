# S49 R11｜兩個未回收問題的作者窄修與精確凍結

2026-10-20 UTC。[R10 固定來源／書面畫面獨立覆核](r10-source-independent.md)依其五檔 SHA 判 PASS；[R10 正式雙盲合併](r10-official-panel.md)則為 **FAIL，12/13**：兩位全新讀者共同否決必答的 `payoffs`。`moon018` 問被冒稱的《愛丁堡科學期刊》增刊能從哪裡翻到，舊 `moon019` 只重述報導自稱；A 另指出 `moon022` 問所有見證者的原始材料，舊 `moon023` 只回答助手來信。本輪僅修這兩個問答。

| ID | R11 台詞與錨點 | 來源及畫面界線 |
| --- | --- | --- |
| `moon019` | 「那份增刊原件，這次沒查到；能翻的是一八五九年重印本。雅各比說，文章在美國造出來。」逐句來源欄縮到 [L 145–165](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L145-L165)（1859 出版者日期及重印標題）和 [J 4063–4070](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4063-L4070)（Jacoby 說增刊是冒稱、稿件在美國製造）。 | 「這次沒查到」只交代本次固定材料沒有增刊原件，不斷言世上所有館藏都無該刊。J 是 **1902 後出評論**，不是另一張 1835 原紙。`moon019` 的提示詞由不明冊子改為檔案室讀者翻無字重印小書；claims 視覺欄明寫不是增刊原件或 1835 原報影像。 |
| `moon022` | 「開場問的格蘭特來信，現在有原件可核嗎？」直接回呼 `moon004`，把「每個名字各自有無原始材料」縮為 `moon023` 確實回答的那封信。來源欄直連 [L 224–239](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L224-L239) 的報導內 Grant 通信說法。 | `moon023` 仍明說這只是報導角色與傳遞路線，沒有查到實際信件。`moon022` 原有無字名卡與信封提示詞未改，並未畫出可讀的 Herschel 或 Grant 原信。 |

L 固定全文仍是 Locke 名下 **1859 重印本** SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`；J 仍是 Jacoby **1902 評論** SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029`。`brief.md`、`research.md`、兩個固定來源 URL、1859 出版者序與反應選錄的歸屬不變。沒有新增 1835 原紙、Herschel 原信、增刊原件或獨立發行帳的主張。

| R11 固定檔 | SHA-256 |
| --- | --- |
| `brief.md` | `eb622b1471461f61a213a66c2bf646274e0e4887c82e102bea83ef2aa4aaea0e` |
| `research.md` | `3574780b890d96ce436af3b1542cc153cc3de4231e93c8fdaff87740fd0783f3` |
| `claims.md` | `867593fb21255f4b4764471347f8ebe779241931537970294ec39cca12d2e1fb` |
| `script.md` | `a9fb4bcc6e271609d79e34d2f4278cdb2c797d0fc8af32b52d4f68b3b1629259` |
| `video.json` | `ff048feb89d227ed88f0ddd648a746ea5d41e70fde9a432f4f4ea80d062e42b9` |

以 R10 精確五檔反向還原自檢，`video.json` 只改 `moon019/022` 兩句 text 與 `moon019` 一個 prompt；`claims.md` 只改同兩列的旁白／來源欄及 `moon019` 的視覺欄；`script.md` 只改同兩句和末尾 narrative／speech 短碼。還原後三檔 SHA 均精確等於 R10 凍結值。其餘台詞（含前八景開場與三句片尾）、提示詞、字卡、`loops`、聲音、配樂及來源清單不變。`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs script --slug curio-s49` 重生劇本；narrative 短碼 `1867678278fd3696`、speech 短碼 `987656f8804e0bd3`。

130 編號景（124 `shot`、6 `big`）及一景三句片尾未變：**133/133** 劇本台詞／情緒與 JSON 同文同序，**130/130** claims ID／旁白與編號景同序，**124/124** shot 提示詞與 **6/6** big 字卡對齊；11 組 loop 的端點存在。`lint --slug curio-s49 --json`：**0 errors／0 warnings、133 lines**。`npm run test:docs-videos`：**236 pass／0 fail／0 skipped**。`npm run check:tasks`：退出碼 **0**、驗證 2,124 票；其他票既有 stale／scope overlap 提醒不影響本票。`git diff --check` 通過。前八景 176 spoken units，按偏快 325 units／分鐘估 **32.49 秒**；正文 2,665 units，同速估 **492 秒（8:12）**；片尾 59 units。這些仍是文字估時，不是新稿 TTS 實長。

**R11 狀態：作者稿已凍結，尚待另一位獨立來源／書面畫面覆核與兩位全新隔離讀者依新稿做正式 13 題雙盲。**R10 的來源 PASS 和敘事 FAIL 均不自動移轉到新 SHA。R8／R9 舊 WAV 不代表 R11 新 speech hash；後續音訊與必要關卡另做。本輪未做正式盲評、政策、本站關卡、TTS、付費插畫、配樂或成片。
