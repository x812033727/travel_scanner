# S29 R3｜新盲評交接

2026-10-19。**R3 前製稿，尚未經這個確切版本的新讀者盲評或付費媒體驗收。** [R2 獨立讀者核查](verify-3.md)固定 `script.md` SHA `982ba73d97e45eca366e5cff7fba02bd8ae3fa93824893e92edacbc89f94cb8b`，必答敘事題過 **9／12**，未過章節銜接、懸念回收、重複表述。該讀者也獨立重取並核對下列兩份來源的完整原始檔，R2 逐行來源與文字對位通過；這不自動批准 R3。

## R3 固定檔與來源

| 檔案 | SHA-256 |
| --- | --- |
| `video.json` | `4e0f58bf8ae8abac3791a6008b8966cd80a7d3cf436c689756f186c277c245c0` |
| `script.md` | `091f43cfcbfaeb8d8201746b46d80e45bb757e2f57de03e5c2c98c3f5807ad95` |
| 陳壽《三國志》卷二十固定 HTML | `dec2ae1713a56e2a33d367d691904004db60740f9490023b52695bfd3740bbc8` |
| CBETA《雜寶藏經》固定 XML | `0b0d59c2c02da42fae95e3ed48f64e20813602b6f48032770a0ce557a6ff90b1` |

固定 URL、原文和行號見 [research.md](research.md)。[claims.md](claims.md)按 R3 **108 個旁白 ID**重建來源對位；每句與當前 `script.md`、`video.json` 精確相符。若改任一個檔案，SHA 和後續盲評須重做。`verify-1.md`、`verify-2.md` 和 `verify-3.md` 保留舊版歷史。

## 同組修正的問題

| R2 讀者指出的問題 | R3 的修正 |
| --- | --- |
| `boat048` 留下另一艘船，`boat049` 突然轉到逐老法令 | `boat048` 保留船與水線，同句接出**地下藏人為什麼**；下一章 `boat049` 立即以逐老法令回答，`boat051` 再明說是大臣藏父。`boat048→049` 現在是同一因果問題。 |
| `boat094` 問「誰最早說出」，原 payoff `boat099` 卻另問故事日期 | `boat099` 改為陳述卷首只能定漢譯層；`boat100` 明答**兩份文字無法判定最早說此法的是誰**。第八組 `loops` 指到 `boat094→boat100`。 |
| `boat028`、`boat046`、`boat078` 三次說「實行」，沒有回扣 | `boat028` 第一次報告傳記結局；`boat046` 改問辦法來源、`boat047` 答傳記缺師承／引書；`boat078` 明說「回看……前面那句」，只在比較 `即施行焉`／`即以此智以答` 時回扣。 |
| 經文只記老父提議、大臣答題，`boat065` 等池邊畫面像已實作 | `boat005` 明說有人**提議**讓白象上船；`boat065`–`boat070` 全改成**現代書房盆中模型**，由讀者演示父親的辦法，無譬喻人物在大池實際稱象。`boat011` 亦移走史文未提的秤具。 |
| 章名先揭示「物」「石」答案 | 第三、第五章仍用事件作章名，但不先念出載物的字，讓 `boat031`、`boat068` 的旁白交付答案。 |

## 本地驗證與下一關

- `node tools/video/cli.mjs lint --slug curio-s29`：**0 errors、0 warnings**；估算全片 **10.5 分鐘**，108 句旁白。
- `node tools/video/cli.mjs script --slug curio-s29`：已生成上方 hash；敘事內部版號 `c7d48b179ae1b308`。這不是獨立讀者盲評。
- `estimateTimeline(video.json)`：開場 **44.57 秒**；正文從第二章起點至 `outro` 起點為 **573.47 秒／9 分 33 秒**，較 480 秒最低限多 **93.47 秒**；全片 **629.27 秒／10 分 29 秒**。合成聲音後仍須按實際 `timeline.json` 再量正文，片頭片尾不能補足。
- 本地逐行檢查：**108／108** 句在 `script.md`、`video.json`、`claims.md` 精確對位；**106／106** 張 `shot` 都是單一構圖、`visual: still`，其中 `boat065`–`boat070` 全是可辨識的現代盆中模型；10 組 `loops`，第八組 payoff 現在是 `boat100`。
- `npm run test:docs-videos`：**236／236 通過**。`npm run check:tasks`：**exit 0**；其他久置或重疊範圍警告不涉及 S29。提交只收本集檔案及本集任務票，另以 staged diff 核對。

請**未讀 R1／R2 審查及本集材料的全新讀者**先只看 SHA `091f43cf…` 的 [script.md](script.md)，依十三題盲評，尤其檢查三個 R2 未過題目與 45 秒開場的自然度。然後另一位讀者逐句核對 [research.md](research.md)、[claims.md](claims.md) 與全部 106 個畫面：`[S1]` 的「物／刻／施行」與 `[B2]` 的「石／畫／以答」不能交換；後出的**漢譯**不能替故事本源定年，也不能推出借用方向。R3 任一字句或畫面改動都要更新 SHA 再評。**在新盲評及相應站主關卡通過前，不跑付費 TTS、MiniMax、音樂或成片。**
