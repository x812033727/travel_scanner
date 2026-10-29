# S60｜固定稿史料與逐句查核

2026-10-22 UTC。**PASS：僅限下列 R4 雜湊的史料、109 句旁白與書面畫面。**這份查核不代替原生插圖驗收、實際語音審聽、網站關卡、成片或 YouTube 上架。我沒有修改創作檔案或呼叫付費媒體工具。

| 固定輸入 | SHA-256 |
| --- | --- |
| `brief.md` | `f177fe4e14067efb7cc8b6d0d1b817343c38ce5343271383ae8f9f7a48d4c8e1` |
| `research.md` | `e4ec4ac5abb2628d8c3efcabcf3a5beb8f33c5d2ce3ab92113e473a6bebd7689` |
| `claims.md` | `3a1bc97deb2be249b4b5fe2a90fd51f0d4ac8625c2e5fbc73a02e921276d6a88` |
| `script.md` | `f09ce432bfdec71135e44bc9ed3ad6f48119e95e01b2acd318fda13f8bda9dd1` |
| `video.json` | `c0a474072ffa37604dfe2acb9a46f600cac37c9815da5b4b692e213f560fd8ac` |

## 固定來源與主張

我在 2026-10-22 重新取得 [Amundsen, *The South Pole*（1912 英譯固定版）](https://github.com/GITenberg/The-South-Pole--an-account-of-the-Norwegian-Antarctic-expedition-in-the--Fram---1910-12---Volu__4229/blob/242036c254a5ff483c59e5dc4c66a97f4486f70c/4229.txt) 與 [Scott, *Scott's Last Expedition* vol. I（1913 編訂日記固定版）](https://github.com/GITenberg/Scott-s-Last-Expedition-Volume-I--13-Being-the-journals-of-Captain-R.-F.-Scott_11579/blob/06ff155e7ebf76842906286ae8aa85487ac6a87d/11579.txt) 的 raw 全文；SHA-256 分別為 `741b12f3e558a172bb03a1904df5479a130fd2208085b45c403911e71fdefe00`、`ddf48b1e0fc296b4862bad161bada2797a964ac6e6c7a0a7306a0a73940f8b26`，與[固定來源及 P01–P14 錨點](research.md)相同。GITenberg 行號是轉錄文本的行號。Amundsen 1912 年回顧不是 1911 年當日日記；同書測位附錄亦不是另一份獨立實地測量。

| 關鍵主張 | 直接支持與限制 |
| --- | --- |
| 1911-12-14 初次升旗後仍須測位 | Amundsen [L12754–12811](https://github.com/GITenberg/The-South-Pole--an-account-of-the-Norwegian-Antarctic-expedition-in-the--Fram---1910-12---Volu__4229/blob/242036c254a5ff483c59e5dc4c66a97f4486f70c/4229.txt#L12754-L12811)記 15 時按雪橇里程估算抵達，也明說當時不能確知腳下是精確地理點；後續觀測和附錄的誤差不能改說成「零誤差踩中」。 |
| 1911-12-17 小帳與兩封信 | Amundsen [L13062–13091](https://github.com/GITenberg/The-South-Pole--an-account-of-the-Norwegian-Antarctic-expedition-in-the--Fram---1910-12---Volu__4229/blob/242036c254a5ff483c59e5dc4c66a97f4486f70c/4229.txt#L13062-L13091)記袋內留給哈康七世的信、另外寫給預期會先找到帳篷的 Scott 的短箋；他說返程漫長，可能無法親自報告。兩封信收件人不同；固定文本沒有兩封信的逐字全文。 |
| 1912-01-16 黑旗、01-18 小帳 | Scott [L15947–15978](https://github.com/GITenberg/Scott-s-Last-Expedition-Volume-I--13-Being-the-journals-of-Captain-R.-F.-Scott_11579/blob/06ff155e7ebf76842906286ae8aa85487ac6a87d/11579.txt#L15947-L15978)記前一事件，[L15981–16052](https://github.com/GITenberg/Scott-s-Last-Expedition-Volume-I--13-Being-the-journals-of-Captain-R.-F.-Scott_11579/blob/06ff155e7ebf76842906286ae8aa85487ac6a87d/11579.txt#L15981-L16052)記後一事件及「A note from Amundsen, which I keep」；「當時收下短箋」不能推成「國王最終收到信」。 |
| 後續 | Amundsen [L13983–14006](https://github.com/GITenberg/The-South-Pole--an-account-of-the-Norwegian-Antarctic-expedition-in-the--Fram---1910-12---Volu__4229/blob/242036c254a5ff483c59e5dc4c66a97f4486f70c/4229.txt#L13983-L14006)記 01-25 五人、兩橇、十一犬返抵弗拉姆之家；Scott [L17294–17328](https://github.com/GITenberg/Scott-s-Last-Expedition-Volume-I--13-Being-the-journals-of-Captain-R.-F.-Scott_11579/blob/06ff155e7ebf76842906286ae8aa85487ac6a87d/11579.txt#L17294-L17328)的最後日記與編者記述支持其未返、日記後被找到。兩份固定文本在這些段落均未追到國王信最終送達。 |

我重新解析 `video.json`、[逐句主張表](claims.md)與 `script.md`：**109／109 個 ID 與旁白逐字相同**，沒有遺漏或重複 ID；R4 為 103 個互不相同的插圖提示詞、6 個字卡場景，最長僅 1 張連續字卡，11 個伏筆。R1 獨立查核指出的四處事實／畫面問題由[R2 獨立查核](review/r2-independent-source-visual.md)重新驗過；[R3 獨立查核](review/r3-independent-source-visual.md)重核其後的 15 景改動及全稿。R4 只刪去重複結尾 `s60107`、把 `s60008` 的伏筆回收到仍有證據邊界的 `s60106`，其餘創作未改；[R4 獨立來源與書面畫面覆核](review/r4-independent-source-visual.md)已按可逆差分及上述固定原文判為 PASS。我另核對了兩份原文中首次升旗、留信、黑旗、小帳、收下短箋、返基地及日記被找到等核心錨點；沒有把「留信／發現／收下」偷換成「國王收到」。

書面畫面只授權**原創示意**：`s60046` 指定五人共同扶旗，`s60073–082` 的信、牌只畫不可讀原創物件，`s60105–106` 不當成歷史現場照片。提示詞可以作出圖輸入，不能預先視為 MiniMax 原圖已通過；每張原圖仍須獨立檢查人物年齡、年代、可讀假文字、黑邊及敘事時序。

敘事另有[R4 兩名隔離讀者及正式 OR 合併稽核](review/r4-formal-merge-audit.json)：同一稿與 panel 規則雜湊下，一人 13／13 YES、一人 11／13 YES，依規則合併 **13／13 PASS**、無共同必答失敗；這是敘事關卡，與本史料 PASS 各自獨立。`lint --slug curio-s60 --json` 重新實跑 0 error／0 warning，109 句，第二章 00:46 開始，正文估算 10.6178 分鐘；實際語音長度尚未測得。
