# S29 R4｜全新盲評交接

2026-10-20。**R4 前製稿，尚未經這個確切版本的獨立敘事盲評或付費媒體驗收。** [R3 核查](verify-5.md)固定 `script.md` SHA `091f43cfcbfaeb8d8201746b46d80e45bb757e2f57de03e5c2c98c3f5807ad95`，官方必答題過 **11／12**，只有 `no_recap` 未過；來源與全部 106 個舊版提示詞核查通過。R3 讀者指出的相鄰重述與結尾再次陳述，已在 R4 一組處理。R3 的判定不自動批准 R4。

## R4 固定檔與來源

| 檔案 | SHA-256 |
| --- | --- |
| `video.json` | `3beeb3982af5cd79e76388a0f65eb20631f2301693ba8bc28752e1a790b93fe5` |
| `script.md` | `3c39392d9072370ae1a8138cbf1957a63fbd8228cf76bdc792b362b76ff89fe1` |
| 陳壽《三國志》卷二十固定 HTML | `dec2ae1713a56e2a33d367d691904004db60740f9490023b52695bfd3740bbc8` |
| CBETA《雜寶藏經》固定 XML | `0b0d59c2c02da42fae95e3ed48f64e20813602b6f48032770a0ce557a6ff90b1` |

來源固定 URL、原文和行號見 [research.md](research.md)；[claims.md](claims.md)按 R4 **103 個旁白 ID**重新生成。五個刪去的重述鏡頭保留 ID 空缺，其餘 ID 不重編，方便逐句核查。任何 `script.md` 或 `video.json` 改字都會使上表與新盲評作廢。

## 集中處理 R3 的重述

| 問題 | R4 的修正 |
| --- | --- |
| `boat032` 說「物」非「石」，`boat033` 立刻再說史文沒點石 | `boat032` 一句說清：傳記只寫「物」，**既沒指定也沒排除石頭**；刪 `boat033`。`boat034` 轉問已稱物件怎樣合計象重，`boat036` 回答。 |
| `boat047` 與 `boat102` 兩次說傳記沒有師承／引書 | 刪 `boat047`。`boat046` 留下來源問題，`boat048` 直接帶出另一故事；至最後 `boat102` 才首次明說傳記的「沖曰」未留下可追查的師承名字。 |
| `boat013` 與 `boat096` 都說稱象當日不定年 | `boat013` 改成傳記提議的起句「置象大船之上」，沿著船推進；去世時十三歲和稱象日期未知只在 `boat095`–`boat096` 的年代檢查交代。 |
| 方法段落還有自行重問／重述 | 刪 `boat035`、`boat038`、`boat042`；`boat037` 改問**換船**是否仍能比較，`boat039` 用同船及可比水面條件作答。`boat105` 只用相似水線提最後的證據問題，不重說已缺連接材料。 |

## 本地驗證與下一關

- `node tools/video/cli.mjs lint --slug curio-s29`：**0 errors、0 warnings**；估算全片 **10.1 分鐘**，103 句旁白。
- `node tools/video/cli.mjs script --slug curio-s29`：已生成上方 hash；敘事內部版號 `4220f9db2851894e`。這不是獨立讀者盲評。
- `estimateTimeline(video.json)`：開場 **44.57 秒**；正文從第二章起點至 `outro` 起點 **547.77 秒／9 分 08 秒**，較 480 秒下限多 **67.77 秒**；全片 **603.57 秒／10 分 04 秒**。實際 TTS 與組片後須按 `timeline.json` 重新量正文，片頭片尾不能補足。
- 本地逐行檢查：**103／103** 句在 `script.md`、`video.json`、`claims.md` 精確對位；**101／101** 張 `shot` 有單一構圖提示詞、`visual: still`；10 組 `loops` 的設問、交付 ID 均存在且依序。佛經方法的 `boat065`–`boat070` 仍是現代盆中模型，沒有變成史料未記的古代實作。
- `npm run check:tasks`：**exit 0**；現有其他任務警告不涉及 S29。`npm run test:docs-videos`：**236／236 通過**。提交只收 S29 與本集任務票，另以 staged diff 核對。

**下一關**：請一位無本集既有審查脈絡的新讀者，在隔離的新對話中先只讀 SHA `3c39392d…` 的 [script.md](script.md)，再單獨取官方 `narrative --slug curio-s29 --json` 十三題，不併行讀取舊 review、brief、claims、research 或本頁；逐題答覆並用官方 CLI 評核，保留完整證據。之後請另一位讀者重取固定來源，逐行查 [claims.md](claims.md)、全部 101 個提示詞及片頭片尾；特別核「物／刻／施行」與「石／畫／以答」、後出**漢譯**不等於原故事日期、相似水線不證明借用。**在新盲評、來源／畫面審查及相應站主關卡通過前，不跑付費 TTS、MiniMax、音樂或成片。**
