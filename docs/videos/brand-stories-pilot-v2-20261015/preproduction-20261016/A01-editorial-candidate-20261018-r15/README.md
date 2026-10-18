# A01 輪子行李箱 r15：安檢畫面揭露順序候選 — HOLD

r15 從凍結的 r14 離線稿衍生；r14 `manifest.json` SHA-256 為 `B0F44AC19FF6A449113570A9FE0CCC20667D9093EEF383219C95A8CE2DAE9231`。建置器先驗證 r14 的 manifest、建置器、README 和每個輸出檔，再只寫 r15 目錄。r14 及更早稿、正式機和付費素材均不改動；舊審查不核准 r15。

## 兩鏡畫面修訂

r14 口播已把安檢一幕拆成三個節拍：`turn-05/crcw` 看見旅客費力處理箱子與金屬推車，`turn-security-question/r6t01` 問把兩樣東西鎖在一起能否過安檢，`turn-06/iu9y` 才說明彈力繩與卸箱動作。獨立審查指出，r14 前兩鏡的**插畫提示詞**仍讓觀眾提前看見解繩或接點。r15 只改前兩鏡的英文 MiniMax 可愛靜圖提示詞：

- 第 42 鏡改為安檢隊伍廣角。箱體、獨立金屬推車的輪子與把手仍可辨認，Plath 匿名示意人物在後方觀察；旅客與前景排隊欄杆遮住繩索、結點、接觸處和卸箱動作。
- 第 43 鏡改為機師肩後中景。兩件物品仍清楚，前景欄杆和旅客外套遮住相接處；不畫拆綁、鎖定成品或安檢員答覆。
- 第 44 鏡的近景保持 r14 原樣，讓彈力繩與卸箱動作到此才成為畫面焦點。

[ABC News 刊登的 USA TODAY 2012 年報導](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)支持旅客在安檢隊伍中費力把箱子從外置金屬推車卸下；報導沒有說推車卡住，也未精確標明該回憶年份。這些圖是匿名編輯示意，不得當作歷史影像。提示詞禁止具體年份標記、安檢員回答、已通過安檢與提前出現的固定原型；生成後仍須檢查實際畫面是否遵守遮擋與故事揭露順序。

65 鏡、77 句的口播文字和 ID、全部主張與 18 筆實際引用來源、作品設定、字典、其他 63 鏡及鏡頭方式均與 r14 相同。全部主張仍為 `PENDING`；`source-map.json` 標為待獨立 r15 審查的 **HOLD**。

## 待完成關卡

- 正文目標 7–8 分鐘；`validation.json` 只有文字代理估時，沒有實際 TTS、盲聽或影片時長。
- 正式企劃 23 筆來源、r15 真正引用 18 筆、工人重併後 25 筆的差異仍待逐筆對齊和審核。`plan-source-addition.json` 是未匯入提案。
- `turn-09/t7b` 是離線主張 ID；正式工人的 `numberClaims` 會重編。正式機六章銜接後需重做查核、聽眾審稿、兩名獨立敘事讀者及以正式 ID／雜湊綁定的 `story/reviews/script-review.json`。
- 本候選未匯入正式機，沒有製作圖片、配音或成片；A01 保持 **HOLD**。

從此工作樹的儲存庫根目錄執行：

```bash
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-editorial-candidate-20261018-r15/build.mjs --check
```
