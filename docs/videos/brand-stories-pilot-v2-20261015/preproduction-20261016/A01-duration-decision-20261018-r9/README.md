# A01 輪子行李箱：7–8 分鐘片長決定與 r9 離線候選 — HOLD

2026-10-18 站主選擇讓 **A01 `story-rolling-suitcase-v2`** 維持緊湊故事，旁白正文目標 **420–480 秒**（`video.json` 的 `target_minutes: [7, 8]`）。不要補重複段落、放慢配音或拉長畫面湊到九分鐘。這是 A01 單集決定；B18 與後五集仍按原本約十分鐘製作，試作系列 `target_minutes: 10` 不變。

本目錄以 [r8 凍結候選](../A01-story-depth-candidate-20261018-r8/README.md)與其 manifest SHA-256 `3475e820d22df7f9d8fd850764d450f17630a2dcdd390949f9147d03062c42b8` 為基底。`build.mjs` 僅把 A01 `candidate/video.json` 的 `[9, 11]` 改為 `[7, 8]`；旁白、鏡頭、回路、主張、發音表及 `candidate/series.json` 均逐位元組承接 r8。它也核對試作系列及 B18 企劃原檔的 SHA，原 r8 和正式機資料都不改。此 r9 是**離線提案**，不能因片長欄位更新就把舊審稿視為通過。

**繼承的來源索引阻擋：**後續獨立全文審查發現 r8 `candidate/video.json.sources` 還留著與這支故事無關的 NASA／Ms. Magazine／Wikipedia 項目，卻沒有把 1939 年 Midland 報導、Emmer、1993 年《洛杉磯時報》、Yale Shiller 與 Global Traveler 等已用於逐景主張的來源完整列入。r9 只改片長，因此原封不動繼承這項 **P1／HOLD**。須另做來源綁定的內容修訂、重新核查與雜湊審稿；不能把本包當可匯入稿，亦不能以 `claims.md` 的來源列代替 `video.json.sources` 的完整性驗收。

`target_minutes` 管旁白正文。固定 **5 秒片頭**接第一章之後，正文後接 **21 秒片尾**；若正文實測正好 420–480 秒，含兩段動畫的影片約 **446–506 秒（7:26–8:26）**，仍須以實際資產影格和合成片驗收。r8 的紙上時間估算（包含正文中的最後口播／片尾卡台詞，**不包含**這兩段獨立動畫）在 300／275／250 口語單位每分鐘分別是 **443.1／478.2／518.5 秒**；只有真實 TTS、停頓、合成時間軸能證明是否落在 420–480 秒。較慢的 250 估算已超過上限，不應為了符合字面速度要求機械加速。

## 驗證

在儲存庫根目錄執行：

```bash
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-duration-decision-20261018-r9/build.mjs --check
```

`manifest.json` 綁定 r8、目前試作系列與 B18 企劃的確切檔案雜湊，並列出 r9 輸出。`validation.json` 只是靜態 lint／估時：預設 250 CPM 把正文估為 518.5 秒，**會**執行逐集敘事／稿型 lint；按 300 CPM 估為 443.1 秒時，現行 `lintVideo` 的八分鐘門檻會**略過**那些檢查。故零 lint error 不等於真正 7–8 分鐘節奏的敘事 PASS。上述 P1 來源索引、每 30–45 秒的有效事件、完整來源與畫面、實際配音、盲聽、正式六章銜接及 `story/reviews/script-review.json` 都尚未過關。正式工人目前按系列十分鐘推算章稿和 540–660 秒片長；本地 `target_minutes` 並不會自行更新正式機或放行它的長度關卡。A01 STOP、主機與預算前檢、既有審核及付費媒體 HOLD 繼續有效；不要匯入、配音、產圖或啟動 B18／後五集。
