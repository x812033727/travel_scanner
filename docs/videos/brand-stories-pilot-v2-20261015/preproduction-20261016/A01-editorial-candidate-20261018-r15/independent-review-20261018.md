# A01 r15 獨立複核：離線編輯基準可用，正式製作 HOLD

日期：2026-10-18。審查對象為 `manifest.json` SHA-256 **`604285CFCBEFA1B85AC3A923442DC6CCE2ACDBD459DC3E1758138C445F53629C`** 的 r15 候選。結論限於此精確版本：**P0 = 0、P1 = 0、P2 = 0**。它可作為後續正式機差異審查的離線編輯基準，並非正式六章稿的核准。

## 變更與史料

相對 r14 manifest `B0F44AC19FF6A449113570A9FE0CCC20667D9093EEF383219C95A8CE2DAE9231`，`candidate/video.json` 的實質變更只有第 42 鏡 `turn-05` 與第 43 鏡 `turn-security-question` 的兩段英文 MiniMax 可愛靜圖提示詞。旁白、場景與台詞 ID、主張錨點、來源、`camera` 和 `visual` 均未變；`candidate/script.md`、`claims.md`、`series.json`、`lexicon.json` 及 `plan-source-addition.json` 與 r14 位元組相同。建置器、說明、來源映射、驗證與 manifest 的版本及雜湊資料隨之更新；來源索引的 18 個網址未改。

[ABC News 刊登的 USA TODAY 2012 年報導](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)支持 Plath 在安檢隊伍中，看見旅客費力把用彈力繩綁住的箱子從獨立金屬推車卸下。報導沒有說推車卡住，也未給該安檢回憶的確切年份。r15 前兩鏡保留箱子與推車的區別，遮住繩索、接點與卸箱動作；第 44 鏡 `turn-06` 才揭示。提示詞禁止安檢員答覆、通關、固定原型、具體年份標記和真人樣貌，並將畫面定位為編輯插畫，不能視為歷史照片。

## 檢查與邊界

`node build.mjs --check` 退出碼 0：65 鏡、77 句、78 筆仍為 `PENDING` 的主張、18 個引用來源；lint 0 error、31 warning，可愛畫風檢查 0 error。文字代理估計正文為 **436.6 秒（300 字／分）、471.3 秒（275 字／分）、511.0 秒（250 字／分）**；前兩種落在站主選定的 420–480 秒範圍，沒有實際 TTS 量測。

**正式製作維持 HOLD。** MiniMax 實際產圖後仍須檢查兩鏡遮擋、前後畫風與年代一致性，以及是否誤畫安檢放行、歷史人物或提前揭示。正式機還須核對六章與稽核鏈、對齊企劃 23 筆／本稿引用 18 筆／工人重併 25 筆來源及重編主張 ID，重新完成 verifier、listener、兩名獨立 narrative 讀者審稿，產生綁定正式檔案雜湊的 `story/reviews/script-review.json`，並實測配音正文 7–8 分鐘。此報告**不是**該正式審稿收據，也不核准主機寫入、付費圖片／配音／合成或影片上傳。
