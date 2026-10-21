# S38 R8m｜`pf007` 日記引文卡與 30 秒開場

2026-10-21 00:55 UTC。**作者候選；待獨立來源／書面畫面覆核。沒有重畫、清帳、上傳或簽核。**[R8l 第三張原生圖](verify-32-r8l-pf007-final-native-stop.md)因上下黑邊與白日窗景判退，`pf007` 已到三圖兩修停點；這輪不再購圖。私有 `STOP` 保持存在。

固定 [佩皮斯日記 1666 年 9 月 2 日](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65795-L65801) 的原句是 `Jane called us up about three in the morning`，以及 `I rose and slipped on my nightgowne, and went to her window`。`pf007` 保留原旁白「她叫醒佩皮斯。他套上睡袍，走到窗邊。」；畫面改為承載後半句的**中文譯文卡**，明標「佩皮斯日記・中文譯文」及日期來源。卡片寫「我穿上睡袍，走到她的窗邊」，不宣稱是中文原文，也不臆造室內照明、衣貌或窗外日光。它緊接 `pf006` 日期／人名卡，共兩張連卡，未超過三張上限；正文插圖預計 **109／111＝98.2%**。`pf007` 原語音約 4.83 秒，前卡約 7.10 秒，均低於單卡 15 秒上限。這是一次有確切文字證據的窄例外，不把失敗圖任意換成抽象卡。

開場末句 `pf005` 的三個懸念之一是「日記有沒有交代起司下落」。在這個問題後把停頓從預設 **300 ms** 調成 **1600 ms**；使用現有 112 句音訊樣本數純計算，第一章從 **867／30＝28.90 秒**到 **906／30＝30.20 秒**，達 30–60 秒濃縮開場。旁白字、語音檔與其他停頓未改；修改 `pause_after_ms` 會使 speech hash 和私有 timeline 過期，正式重建前不能宣稱現有 timeline／成片已是 R8m。

[結構化差分](verify-33-r8m-structured-diff.json)限 `pf005.pause_after_ms` 與 `pf007` 模板／資料；從目前原始位元組精確還原二處，整檔 SHA-256 回到 R8l **`2e9ec8c6f2962b420719ef62185d38def7f915bac3fac2e55fb0f16b231c6778`**。R8m `video.json` SHA-256 **`980c371a793bfe3f4d2772d6d002309026a8cbd8874187ab8cd1d8fdeba82065`**、`visualHash` **`98742d01363e5597`**；`brief.md`、`research.md`、`claims.md`、`script.md` 未改。`lint --slug curio-s38 --json` 為 **0 errors／0 warnings**；目前純樣本時序全片約 9:57.5，**不是**成片 QC。

私有帳本仍 **US$0.3300**（20 image、18 judge、1 music），包含 `pf003` 未收到圖的 US$0.0035 預約；原整集硬上限 US$4.58。`pf001/002/004/005` 既有合格圖仍須在新版逐景核對 request key／judge stamp；`pf003` 不得重送相同不明付款請求。網站持有者音訊及分鏡審核、全片其餘原生圖、動畫片頭片尾與連結、QA 與成片均 HOLD。請非作者查固定原文／翻譯、卡片資訊密度和顯示、30.20 秒時序、精確差分與 STOP，再決定是否接受 R8m 書面方案。
