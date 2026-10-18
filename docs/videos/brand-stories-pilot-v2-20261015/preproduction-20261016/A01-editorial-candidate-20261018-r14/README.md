# A01 輪子行李箱 r14：安檢段落節奏修訂候選 — HOLD

r14 是從凍結的 r13 離線稿產生，r13 `manifest.json` SHA-256 為 `9A2D05A012DA83B569181C0A6E69847B4D72858BE23861A4210C7B69F115886C`。建置器驗證 r13 manifest、建置器、README 與全部輸出雜湊，並只寫 r14 目錄。r13 及更早稿、正式機和付費素材均不改動；先前審查不自動核准 r14。

## 唯一改句

獨立編輯回饋指出，r13 第 42 鏡 `turn-05/crcw` 與第 44 鏡 `turn-06/iu9y` 先後都說拆箱，讓中間的問題失去遞進。r14 只把第 42 鏡改為：

> 另一次日期未明的回憶裡，Plath 在安檢隊伍中，看見前方旅客正費力處理箱子和金屬推車。

[ABC News 刊登的 USA TODAY 2012 年報導](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)確實寫到 Plath 在安檢隊伍後方，看見旅客費力處理綁在獨立金屬推車上的箱子；沒有說推車卡住。r14 第 42 鏡口播只指出兩件東西與旅客的困難；第 43 鏡問「如果把兩樣東西鎖在一起，安檢員會讓它過嗎？」；第 44 鏡口播才說明彈力繩與卸箱動作。第 42 鏡原有插畫提示詞已會畫出繩索，本輪沒有改畫面；延後的是口播的完整解釋。

第 44 鏡和其他 64 鏡、所有插畫提示詞、場景／台詞 ID、主張、來源、作品設定與 lexicon 均與 r13 逐位元組一致。`t5` 主張仍為 `PENDING`；r14 `source-map.json` 的新狀態是待獨立審查的 **HOLD**，沒有繼承舊審查或核准。

## 待完成的正式關卡

- 正文目標 7–8 分鐘；`validation.json` 僅記錄 250／275／300 字每分鐘的文字代理估時，實際 TTS、盲聽與成片時長尚未量測。
- 正式企劃 23 筆來源、r14 實際引用 18 筆、工人重併後 25 筆的差異仍須逐筆核對及審核；`plan-source-addition.json` 仍只是未匯入提案。
- `turn-09/t7b` 是離線主張 ID；正式工人的 `numberClaims` 會重編。正式機六章銜接後須重做查核、聽眾審稿、兩名獨立敘事讀者與以正式 ID／雜湊綁定的 `story/reviews/script-review.json`。
- 本候選不授權主機寫入、付費圖片、配音、合成、上傳或後續集數製作。A01 維持 **HOLD**。

從儲存庫根目錄可重跑：

```bash
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-editorial-candidate-20261018-r14/build.mjs --check
```
