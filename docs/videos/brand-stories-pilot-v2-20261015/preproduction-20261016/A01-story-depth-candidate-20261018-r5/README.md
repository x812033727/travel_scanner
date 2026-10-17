# A01 輪子行李箱：r5 證據註記候選 — HOLD

本資料夾只修正已凍結 r4 的兩處審稿中繼資料；`base/` 保存 r4 的候選檔、manifest、來源表、驗證表與 README 位元組快照。建置會同時核對快照和原 r4 資料夾。r5 的 `video.json`、`script.md`、`series.json`、`lexicon.json` 與 r4 **逐位元組相同**，沒有改旁白、畫面、鉤子、章節或時間估計，也不繼承審稿 PASS。

## 兩處證據修正

- 1939 年 2 月 9 日的[米德蘭當地報紙第 4 頁](https://newspapers.swco.ttu.edu/bitstreams/b9cd84b8-2ba7-4506-9eff-7cca3e5c6376/download)記錄安妮塔在前一天茶會出場時披著黑色**斗篷**、戴實用帽子，並帶一只輪子行李箱。r4 的 o34 主張與 README 曾誤寫成「披肩」；r5 改成「斗篷」，與既有口播、畫面相符。該報導只證這場出席，無法識別它是否為 1928 年的同一只箱子。
- [Travelpro 公司沿革](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage)把 Plath 的直立 Rollaboard 設計記為 **1987 年**；[Smithsonian Magazine 的歷史回顧](https://www.smithsonianmag.com/history/history-humble-suitcase-180951376/)說 Rollaboard 在 **1987 年**改變登機箱，但沒有獨立記錄車庫製作的確切日期。Plath 在 [2024 年《Chinook》校友刊第 17 頁的第一人稱簡歷](https://wshsalumniassociation.org/wp-content/uploads/2024/05/Chinook-May-2024.pdf)卻寫 **1988 年**發明直立 Travelpro Rollaboard。r5 保留原旁白「依 Travelpro 回顧，1987 年……」的歸屬；年份差異列為尚待獨立審查的來源衝突，不能把 1987 或 1988 說成已定讞的唯一年份。

上述年份註記是審稿警示，**不是新增的播出主張**。o34 以外的主張文字及 73 個主張 ID 不變。逐鏡證據和限制見 `source-map.json`、`candidate/claims.md`；r4 的其他證據邊界仍適用。

## 機械檢查與停止線

在儲存庫根目錄執行 `node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-story-depth-candidate-20261018-r5/build.mjs --check`。r5 沿用 r4 的 **69 鏡、79 句、1,873 口語單位**；250／275／300 單位每分鐘的六章估計分別為 **523.3／482.7／447.4 秒**。距 540 秒下限分別差 **16.7／57.3／92.6 秒**；300 單位每分鐘估計的嚴格問句最長空檔仍為 **174.8 秒**，未審的來源動作代理最長 **123.4 秒**。這些是文字估計，不是實際 TTS。

`validation.json` 的片長與 45 秒鉤子關卡繼續 **HOLD**；獨立事實覆核、盲聽、視覺審查、正式機六章遷移及審稿收據尚未完成。本資料夾不授權主機匯入、媒體生成或任何付費工作。
