# C14 CamelBak v8｜N10 獨立來源與配鏡窄修覆核

- 審查者：Codex `codex-c14-independent-v8`，非 v8 作者；2026-10-23（台北時間）。受審作者 commit `5207b03fec6adf054eb2217e5270eb687b7805ff`，去向為 [draft PR #1695](https://github.com/x812033727/travel_scanner/pull/1695)。
- **判定：N10 聲畫窄修 PASS。** v7 [獨立覆核](independent-v7-source-visual-review.md)的唯一來源 HOLD 是 N10 把出口控制說成水只在喝時才靠近嘴邊。v8 改為「兩者都讓人決定什麼時候讓水從出口流出」，刪掉未證的水／嘴距離主張。此 PASS 只補上 v7 的 N10 缺口；它不是 v8 全片純旁白盲讀、TTS 時長、生成圖、站主採用或付費／發布授權。

| 受審檔案 | SHA-256 |
| --- | --- |
| `treatment.md`（已採用，未改） | `078DC1D77C46EB49BB6F27F60535F22775781E5963783BDA7C1F7625B1A8700E` |
| `source-matrix.md`（已採用，未改） | `F8CF68AA36264DF18CDBE6ECD698D4AF1F22E405DEAADA8ED275B7685050587E` |
| `script.md` | `167DB38F368484951C56972B86A9838BB92B3B0B874952A87FBBAD26B8429312` |
| `script-source-notes.md` | `EF3AA1C79AB5EB19F0C52E9B024468AD6AF7A3EDC26AF17894D8C97D81BE538C` |
| `visual-plan.md` | `75E6AD2973078B72A28E17C5B2B9B58ACA5A1A247319CE5AB298D85E6F45DC2C` |
| `visual-plan.json` | `B211410713F271459AF267CC2F8DB4E8938A7EDB9938B6048A552A1076D4C063` |

## N10 原件與相鄰聲畫

| ID | 獨立核對 |
| --- | --- |
| S2／N10 左半句 | [CamelBak NZ 品牌回顧](https://camelbak.co.nz/pages/about-us)的「From IV to Oh Yeah」記述 Eidson 把裝水的點滴袋放進襪子、塞在車衣背後，管子越過肩膀，末端用衣夾夾住。這是後來的品牌敘事，支持「背在身上」及衣夾控制出口的有限推論；不證飲水前水或管子遠離嘴邊。 |
| S11／N10 右半句 | [GearJunkie 2006-02-02 同時期展場報導](https://gearjunkie.com/uncategorized/outdoor-retailer-trade-show-winter-market-2006-gear-highlights)的「CamelBak Bottle」段記記者所見瓶子使用背水包系的咬合閥設計、翻起式口器連到瓶內短吸管；「不漏」是記者轉述的公司說法。瓶子作為手握容器、由使用者控制出口出水時機是窄幅機能對照；未認定展場品精確採用某件專利的全部零件。 |
| N08–N11 語境 | N08 說展場瓶的翻起咬合口；N09 明說原型衣夾與較晚咬合口不是同一零件；N10 只對照背上／手上及何時從出口出水；N11 用「假如」明示今日騎乘與桌前場景是編輯示例。N10 沒有回到 v7 的物理位置過度主張，也沒有把兩種零件說成相同。 |
| N10 配鏡 | v8 仍是左右分屏的**無標誌背水包**與**泛用手中水瓶**；prompt、kind、motion 均與 v7 相同，沒有畫嘴邊水位、閥門細節、實際出水狀態或特定歷史現場。這個概念鏡頭和新版口播相容。 |

## Delta 與紙上算術

以 v7 獨立收據 commit `3cf2e67736cdc1470d48831eed0df92ab562209d` 為基準，逐 ID 比較 `script.md` 的 70 個口播列：**僅 N10 句子改動**，其餘 69 句及來源標記不變。逐 shot 物件比較 v7／v8 JSON：**僅 N10 `planned_duration_s` 由 7.4 改為 7.9**；70 鏡的 ID、順序及其餘欄位均不變。檔案版號、審查說明、來源註解和分鏡文字摘要也更新，故「只有 N10 改動」僅指口播列和 JSON 鏡頭內容，不指整份檔案逐位元組。

重新合計 70 鏡正文 **496.5 秒**，較 v7 增 **0.5 秒**；54 幅概念插圖 **373.3 秒**，占 **75.19%**，另有 16 張卡片。正文紙估距 ≥480 秒只有 **16.5 秒**餘裕；片頭 5 秒、片尾 21 秒加總為 **522.5 秒（約 8:43）**。這些是分鏡估算，不是正常語速 TTS 或成片驗證。

## 下一關

請把**完整 v8 的純旁白**交給兩位未讀此版的讀者獨立盲讀，再以正常語速 TTS 實測正文是否 ≥480 秒及敘事節奏；之後仍需生成圖逐張驗收、站主稿／分鏡採用及另行授權的付費製作。若任一受審作者檔案 SHA 改變，本窄修 PASS 不自動延伸。沒有執行付費生成、匯入、上傳、發布、合併或自我採用。

本機 `npm run check:tasks` 仍會被既存且未追蹤的 v4 同 ID open/done task 兩份擋下；先前刪除受政策阻擋，這次未碰觸它們。此限制與 N10 來源判定分開。
