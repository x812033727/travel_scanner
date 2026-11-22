# 第 12 集真人版第二波重拍（round4，2026-11-22）

依據 `review-zt/WAVE2-BRIEF.md`、`WAVE2-CANDIDATES.md`（e012 s10→s11 小禾髮型衣服）。種子 9129401、9129402；1 鏡 2 支、16 秒 → `runpod/live/fixp4/`。沒有送出任何工作。

**決定重拍哪一鏡**：拿定妝照 `xiaohe-portrait-l1`（與角度 a、b）比對現行成片：s05、s06、s10 的小禾都是中分、兩條紅繩短辮、淡紫補丁盤扣短襖，跟定妝照一樣；第一波新的 s11（fixp 9129101）是散髮瀏海、深紫棉襖。s10 對、s11 錯，所以重拍 s11，s10 不拍。

| 鏡 | 錯在哪 | 改了什麼 | 換圖 | 拿不準的 |
| --- | --- | --- | --- | --- |
| s11 | 散髮、深紫棉襖，接 s10 的雙辮淡紫短襖對不上 | 原因：第一波構圖句寫了 `tousled hair`（睡亂的頭髮），模型就放下辮子。拿掉，改成照定妝照的中分、兩條紅繩短辮各垂在耳後到肩、淡紫短襖盤扣方補丁（兩處寫 exactly as in <Picture 1>），蹦一下時加「兩條辮子在肩上甩」；官差一圈火把、錢袋、台詞、低角度、一個動作都照第一波（第一波那部分已修好） | 不換（定妝照＋夜院 l2，照第一波） | 這是改字不是改設計：第一次出這個錯，原因是那個字，所以只改那個字。角度圖不送（兩張都朝畫左，她要朝畫右）。夜裡火光會把淡紫照深，挑片時跟 s10 並排看顏色；分鏡原本寫「頭髮睡亂」（c05），辮子微亂可以接受 |

## 檢查

```
python3 -I _scripts/polish-build.py 12 4                       -> e912: 1 shots, 2 drafts, 16 s
python3 -I _scripts/preflight-prompts.py …/fixp4/colab-jobs.json -> 0 error(s), 0 warning(s)
h3r.sh check --manifest …/fixp4/colab-jobs.json                 -> 0 error(s), 0 warning(s)
```
