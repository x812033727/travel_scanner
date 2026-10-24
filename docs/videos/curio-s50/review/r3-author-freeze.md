# S50 R3｜敘事修訂與作者凍結

2026-10-20 UTC。針對 [R2 正式雙盲 FAIL](r2-official-panel.md) 共同判 No 的五項修稿。這是作者交接紀錄，**不是獨立來源覆核、R3 盲讀 PASS 或網站核准**。下列五檔構成須由後續讀者使用的同一版；R2 雜湊保留在前輪報告。

| R3 內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `60040a61dcf7b2b4b62bba30773537d4c559104724a7f6d83926082211d983e1` |
| `research.md` | `109557d74963733a6b8b3715739d49ec1d68648f5f34a7c9e10d52a9f940e6c7` |
| `claims.md` | `82b6d40f102993787a7653171b3c2d59e61ac27afaf6f1e30c7ca6fe729294df` |
| `video.json` | `25760745a0c21ccba5e27a57d8e778bcc8ac03a6839faf4dcc38407e74725661` |
| `script.md` | `f87630b96934854af46a30e2f3aa5fb7b60733f3b6359efc7e95973fcb7ac256` |

`node tools/video/cli.mjs narrative --slug curio-s50 --json` 的精確輸出另存 `/tmp/s50-r3-author-payload.json`，SHA-256 `5373dd2da36b185f22bdacd49912c2337de10cc7aee3a3557b6b47dd287fe8b7`。新雙盲應重新產生並核對此 payload；這一步沒有自行回答題目。

## R2 五項共同 No 的修訂

- `no_spoiler`：`fire001–008` 留在布丁巷起火、坡路與教堂，將塔官、市長、屋主、損失寫成待解問題；移走開場的 13,200 棟答案和屋主餘燼供詞。
- `one_line`：正文 `fire009` 接回開場那一夜，先走文森特的火線，再循佩皮斯當日塔上、初次船行、國王與市長、下午船行，以及後續止火和隔年委員會；提到來源的出版時點時不另開倒序情節。
- `chapters_link`：`fire104` 以「議會會判定起火原因嗎？」收章，`fire105` 用二月休會前未判、證詞卻出版的下一步接章。
- `payoffs`：明確回收開場的教堂 `fire004→014`、塔官 `fire005→029`、市長 `fire006→049`、屋主 `fire007→095` 和標題問題 `fire008→116`；起因只回答至證據允許的程度。
- `no_recap`：統計數字留至測量員段落才揭露；末段分開交代地址、點火機制及蔓延損失三種證據，`fire999a` 只蓋「未結」章，不再重複烤爐火星句。

## 差異、檢查及待辦

- 相對目前倉庫基線的內容差異：`brief.md` +3/−3 行、`claims.md` +74/−74、`script.md` +78/−78、`video.json` +179/−124；`research.md` 未修改。116 個故事場景和三句片尾共 119 句；113 個 `shot`、三個資訊卡；29 個 loop 的 payoff 都在 setup 之後。
- `node tools/video/cli.mjs lint --slug curio-s50 --json`：**0 errors、0 warnings**，119 句、2426 spoken units、9 章。逐句比對 JSON 與 claims 的 **119 個 ID 和文字相同**，JSON 與生成 `script.md` 的 **119 句順序和文字相同**。
- 專案 `estimateTimeline`（含場景停頓）於 250／300／325 CPM：8 景冷開場 **47.5／40.8／38.4 秒**，其後至 `fire116` 正文 **640.9／550.8／518.6 秒**；最快估速仍超過 8 分鐘。這些是估算，實際 TTS 要另量。
- 片頭仍排在首章後 5 秒；共用 `v4-endscreen` 片尾仍 21 秒，最後 16 秒留 Studio 可點元素。本輪只改文字與書面畫面提示，沒有生成媒體、網站送審或發布。
- R2 獨立覆核的 Pepys、Vincent、1667 年刊本證據邊界仍維持：塔上得知地址、河上所見和見國王／市長按日記先後；塔街炸屋只作 9 月 4 日局部止火；委員會印出證詞但議會休會前未判；法里納與休伯特各自的供詞不等於已證實的點火原因。Gazette `fire037` 與 London Museum `fire108` 仍是 P17 衍生有限用語，官網直接重驗尚待完成。R3 新文字和畫面仍須交獨立來源／書面畫面覆核，並由兩位新讀者按同一 R3 旁白盲讀。
