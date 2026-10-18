# A01 輪子行李箱 r19：安檢揭曉鏡頭的來源綁定候選 — HOLD

這是從已釘選 r18 離線稿衍生的**另一份候選**。建置器驗證 r18 `manifest.json`、其盲審收據與修正後的 25 筆來源企劃提案，再只建立本資料夾的輸出。r18 與更早稿、正式機、媒體及付費素材均不改動；r18 的審查不自動核准 r19。

## 修訂範圍

- 第 44 鏡 `turn-06/iu9y` 原本敘述旅客把以彈力繩綁在金屬推車上的箱子解開、取下，鏡頭的 `claims` 卻是空陣列。新增 `t46` 綁定此鏡，引用 [2012 年 USA TODAY 對 Plath 的受訪報導](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)。這是受訪報導記述的經歷，不以 Plath 專利獨立證實特定旅客的動作。
- `t5` 留在 `turn-05`；`t46` 的企劃來源索引 **5**、公開來源索引 **10**，與受訪報導 URL 相符。`claims.md`、`source-map.json`、`source-alignment.json`、`validation.json` 與 manifest 同步更新，主張數 **73 → 74**，仍全部為 `PENDING`。
- 旁白、鏡頭畫面、畫風、循環鉤子、65 鏡與 77 句均沿用 r18。盲審的三項 P2（Shiller 首次介紹、年份歸屬位置、片尾口語）需待實際試聽與完整查核後決定；本次沒有用新句子製造新的時序或史實判斷。

## 來源集合與限制

| 集合 | 筆數 | 狀態 |
| --- | ---: | --- |
| 此候選 `candidate/series.json` 的編輯企劃來源 | **23** | 沿用 r18，未新增來源。 |
| `A01-r16-source-plan-25-candidate-20261019/candidate/series.json` 的**擬採用**企劃來源 | **25** | 本建置器只讀並驗證；未裝入此候選，也未寫入正式機。 |
| 此候選 `candidate/video.json.sources` 的公開引用 | **18** | 與 74 筆主張的 URL 對齊；不得把 25 筆內部來源直接公開。 |

`validation.json` 的約 436 秒（300 單位／分）與 470.6 秒（275 單位／分）只由文字代理估算，不是實際 TTS 或剪輯量測。正式機仍須核對 104→新版本、六章、重新編號的主張、全部史料與時序、verifier、listener、兩名獨立敘事讀者、正式 `story/reviews/script-review.json`、圖片聯絡表及 US$25 帳本。此候選保持 **HOLD**，不授權主機寫入、解除 STOP、付費呼叫、合成或上傳。

在儲存庫根目錄執行：

```bash
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-editorial-candidate-20261019-r19/build.mjs --check
```
