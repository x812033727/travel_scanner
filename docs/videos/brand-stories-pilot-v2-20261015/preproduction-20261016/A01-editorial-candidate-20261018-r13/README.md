# A01 輪子行李箱 r13：安檢拆綁敘述修訂候選 — HOLD

r13 由凍結的 r12 離線稿衍生。r12 `manifest.json` 的 SHA-256 為 `17CC760B8573F97D189DB7C476D57C61EDDD4050F79E54A0460EEE5C15B7A9D3`。r12 獨立全文審查的 SHA-256 為 `123F4650EAA55197DDCC955C9DD6BCF6F9BF3F1137C8FF0ADB7C16EF30BCEB4E`；該審查**不會自動核准 r13**。建置器會驗證這些輸入及 r12 全部輸出雜湊，不修改 r12 或更早版本。

## 本輪修訂

[ABC News 刊登的 USA TODAY 2012 年採訪](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)記述，Plath 排在機場安檢隊伍裡，看見前方旅客費力把用彈力繩綁住的箱子從**獨立、笨重的金屬推車**卸下。報導並未說推車本身卡住。r12 第 42 鏡 `turn-05/crcw` 的「推車卡在安檢口」超出來源；r13 改成「Plath 排在安檢隊伍中，看見前面的旅客費力拆開箱子和金屬推車」。第 43 鏡「如果把兩樣東西鎖在一起，安檢員會讓它過嗎？」因而有明確的兩件物品；第 44 鏡 `turn-06/iu9y` 再揭示彈力繩與卸箱動作。後續車庫與安檢回應才逐步回答這個問題。

兩鏡的場景 ID、台詞 ID、插畫提示詞、鏡頭順序與主張錨點均不變。`t5` 原主張表已精確描述拆繩卸箱，因此主張文字和 18 筆實際引用來源維持原樣，所有主張仍為 `PENDING`。`candidate/series.json`、`candidate/lexicon.json`、`candidate/claims.md`、`plan-source-addition.json` 與 r12 逐位元組相同。

## 收據邊界與待解問題

- r12 `source-map.json` 原標 `PENDING_INDEPENDENT_FULL_R12_REVIEW`，但獨立 r12 審查後已過時。r13 重建 `source-map.json`，明確標為 **HOLD，待 r13 獨立審查**；舊審查 SHA 只是來源鏈，不是核准。
- 目前企劃來源 23 筆、r13 真正引用 18 筆、工人重併時 25 筆的差異仍須逐筆核對並形成受審的來源對齊方案；`plan-source-addition.json` 只是未匯入提案。不得由離線來源索引推稱主機已對齊。
- `turn-09/t7b` 是離線主張 ID；正式工人的 `numberClaims` 會重編 ID。六章重新銜接、查核與敘事審稿後，應以正式輸出的 ID 和檔案雜湊重做收據，不得拿 r13 的離線映射當 `story/reviews/script-review.json`。
- 文字代理估時與 lint 不等於真實 TTS 或聲畫小樣。正文需實際量到 7–8 分鐘，並經查核、聽眾審稿、兩名獨立敘事讀者和正式收據。正式機六章與稽核鏈即使唯讀核對通過，也不等於 r13 已安裝或獲准續製。

## 可重現檢查

從此工作樹的儲存庫根目錄執行：

```bash
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-editorial-candidate-20261018-r13/build.mjs --check
```

`--write` 只重建本 r13 目錄內的 `candidate/video.json`、`script.md`、`claims.md`、`source-map.json`、`validation.json`、提案檔和雜湊清單，不接正式機或付費 API。**A01 持續 HOLD**：本檔未簽發審稿收據，未啟動配音、插圖、影片合成、匯入或上傳。
