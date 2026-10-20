# S33 前製交接（2026-10-20）

題目：崔萬理等人為何先讚造字「神妙」，又向世宗上疏反對。站主尚未在 `/admin/videos` 選企劃或核劇本；本集**沒有**配音、購圖、音樂或成片。

## 定稿與覆核

| 檔案 | SHA-256／狀態 |
| --- | --- |
| `brief.md` | `b1cfc6aff2db4cf64a4f3e3fa1784d929d97f5a441ee23328101bf0c81f946a2`；後台能解析 A（推薦）與 B 兩選項。 |
| `script.md` | `3db98a782e552385def131784e1dc4c8096e2bceb36e10e58cb75a277e004815`；95 句，約 9.8 分鐘。 |
| `video.json` | `f88c9269709a34272a58ccc6bb59bdacf1b417d0a95e10c8bcb99ab6b4f572ef`；93 景、87 插圖提詞、5 短引卡、12 個伏筆。 |
| `claims.md` | `496caad73962337fbc9b18640f8f1cdf276dbd210af3af90432d3b8451807581`；正文 `hj001`–`hj092` 各有來源節點。 |

來源是 `research.md` 固定 commit 的三卷《世宗實錄》XML（SHA 見該檔）；第三方鏡像尚未對韓國官方掃描。逐句作者覆核見 `verify-1.md`，獨立原文二讀及修改差分見 `verify-r2-source.md`、`verify-r3-source-delta.md`、`verify-r4-source-delta.md`、`verify-r6-source-delta.md`。最新版雙盲：R6 11/13、R7 13/13；按系列「同題兩人皆 No 才不過」規則為 13/13，R6 的兩項具體疑慮和保留理由見 `verify-r6-r7-editorial.md`。`lint` 0 errors、3 個畫面用詞重複 warnings；`npm run tasks -- check` 通過，有其他任務的既有 warnings。

## 後台關卡

2026-10-20 已執行 `review-push --gate outline` 與 `review-push --gate script`。第一次 outline 提交綁較早 `brief.md` SHA `d7253dd958046067b7cb47f32f3eac2991d703dee88cbebf2a0ebd04db1178f9`，工具未解析出選項；隨後已將同一 A/B 內容轉為工具接受的選項格式，重新提交綁上表新版 SHA。Jev 對新版建議 **A**；CLI 同時明說本機 `hand_pushed` 須站主逐關決定，故 Jev 建議**不是站主核准**。`review-pull --gate outline` 和 `--gate script` 均回 exit 3 `waiting for the owner`。請在後台按上表 `brief.md` 雜湊認新版卡片；如舊零選項卡仍可見，以新版為準。

待站主真正選案及核此劇本後，用 `review-pull` 把兩項決定與精確檔案雜湊記回本機，才進行 TTS／音質檢查。插圖有 87 景，仍需整集一次報價與授權；之後按系列畫風製作、原生尺寸查看嚴重矛盾、分鏡站台審核、成片與字幕 QA、Shorts 和上架包。所有卡片和素材應維持史料歸屬；尤其 `是月` 不得被改成造字／成書的某個單日。
