# A01 r16 獨立差異複核：離線畫面候選 PASS，正式製作 HOLD

日期：2026-10-19。審查對象為 `manifest.json` SHA-256 **`5DADE9FCD0F76C03B2C463ADDEF935B0764D8D78EDA9C621BB18E9BFF462EDEF`** 的 r16 候選；基準為 r15 manifest SHA-256 `604285CFCBEFA1B85AC3A923442DC6CCE2ACDBD459DC3E1758138C445F53629C`。結論只涵蓋本輪五處畫面提示詞及其衍生檔：**P0 = 0、P1 = 0、P2 = 0**。r15 的審查不自動核准 r16。

## 精確變更與史料邊界

相較 r15，`candidate/video.json` 只有 `turn-05`、`turn-security-question`、`turn-06`、`turn-07b`、`turn-07c` 五鏡的英文 MiniMax 可愛靜圖 `data.prompt` 改動。所有旁白、場景與台詞 ID、主張錨點、18 筆引用來源、`camera`、`visual`、其他 60 鏡均未變；`candidate/script.md`、`claims.md`、`series.json`、`lexicon.json`、`plan-source-addition.json` 與 r15 位元組相同。建置器、README、來源映射、驗證與 manifest 僅隨候選版本和畫面差異更新，來源索引沒有改動。

[ABC News 刊登的 USA TODAY 2012 年採訪](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)記述：Plath 在安檢隊伍中，看見旅客費力把用彈力繩固定的行李從獨立金屬推車卸下；報導未指定那些旅客行李的殼體材質，也未明確標定該安檢一幕的年份。報導另說 Plath 後來在車庫把推車鎖到自己的硬殼箱上。r16 前三鏡將旅客行李寫成材質不明的旅行袋，安檢口不標精確年代；後兩鏡才保留 Plath 自己的硬殼箱與固定接點，符合這個區別。五鏡都定位為匿名編輯插畫，不冒充歷史照片。

第 42–43 鏡只呈現獨立的旅行袋與推車，遮住繩索、接點和卸下動作；第 44 鏡才以近景揭示彈力繩與卸箱。第 47–48 鏡呈現其後的安檢員對話，提示詞禁止把一句「好」畫成通關或安檢放行。這維持既有鉤子與答案的先後順序，也沒有把 1987 年產品設計年代當成該回憶的確切日期。

## 檢查與後續關卡

`node build.mjs --check` 退出碼 0：65 鏡、77 句、78 筆仍為 `PENDING` 的主張、18 個引用來源；lint 0 error、31 warning，可愛畫風檢查 0 error。文字代理估計正文 **436.6 秒（300 字／分）、471.3 秒（275 字／分）、511.0 秒（250 字／分）**；這不是實際 TTS 或剪輯時長。

**A01 正式製作維持 HOLD。** 實際 MiniMax 聯絡表仍須逐張確認材質不被生成成可辨硬殼、42–43 鏡遮擋成功、44 鏡才揭示繩索、五鏡時代感與畫風一致，且沒有真實人物樣貌或通關暗示。正式機還須核對六章與稽核鏈，對齊企劃 23 筆／本稿引用 18 筆／工人重併 25 筆來源及重編主張 ID，重新完成 verifier、listener、兩名獨立 narrative 讀者審稿，產生綁定正式檔案雜湊的 `story/reviews/script-review.json`，並實測配音正文 7–8 分鐘。本報告不是該正式收據，不核准主機寫入、模型或付費媒體呼叫、合成及上傳。
