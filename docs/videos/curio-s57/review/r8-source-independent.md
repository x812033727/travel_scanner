# S57 R8｜獨立史料與書面畫面覆核

2026-10-21 00:25 UTC。**史料／逐句主張 PASS；書面畫面 PASS。**本判定只對下列 R8 固定五檔有效。我沒有參與 R8 改稿，沒有修改創作檔、呼叫付費媒體、代替新雙盲敘事判定或網站站主審核。

| 創作檔 | 實測 SHA-256 |
| --- | --- |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `brief.md` | `5eadc760e95287cebc97c61007333007348939c18ec505d38ddd9acc5cb88abd` |
| `claims.md` | `cff4abfd700e501ecdc32700138fda27d143320f0f666f233d2792266e0cc861` |
| `video.json` | `bb0cf8d70f565a0c34d0923c08678665b26e24c6637d208d96f474dafb5841d4` |
| `script.md` | `d9605ab9b06528780454cdecd6af3604e34e1be3e09a379ac14e4b46a3fa674d` |

## 獨立取原文及差分

我重新抓取兩個固定 Git 提交的原始文字。史丹利出版**節錄本** S `5157.txt` SHA-256 `de84c2eb2089e18c8e080fe24ecac95c44c1cc993be355987cdd3221036d158f`；Waller 1874 年身後編刊《最後日記》第二卷 L `17024-0.txt` SHA-256 `e6658569be045054c89e59c2aac9819a430a9a84fbdbed289a2ba0fa27750962`。這些行號屬電子轉錄本，不是手稿頁碼；S 的對白與記者行動是其出版敘述，L 的晚年日記與臨終段另有編者層級。

我把[R8 作者差分](r8-author-diff.patch)反向套到五檔副本，所得五個 SHA 逐一等於[R7 獨立覆核](r7-source-independent.md)的固定五檔。解析兩版 `video.json`，R8 只刪 `s57106`，更動 `s57100,s57101,s57104,s57105,s57144` 五句旁白、`s57101,s57104,s57105,s57144` 四個 prompt，以及 `s57008` 的 loop payoff；其餘 parsed JSON 相同。`brief.md` 與 `claims.md` 另同步說明和引註，`script.md` 由新版場景重生。這證明此次新查核的實際範圍，並不把 R7 的 PASS 當作 R8 的自動核准。

| R8 位置 | 我在固定原文查到的支持與界線 |
| --- | --- |
| `s57100` | [L5420–5422](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5420-L5422)明記 **1871 年 12 月 13 日**史丹利轉好，繼續到烏吉吉；改成確切十三日有依據，不重播下一句返村。 |
| `s57101` | [L5427–5428](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5427-L5428)記 **15 日在烏吉吉準備東行取自己的貨**。旁白說「在日記裡寫，正準備」，沒有宣稱當天已出發。 |
| `s57104` | [L5430](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5430-L5430)明記 **16 日聘到通韋的划船者及一名嚮導**；腳本沒有把聘雇改寫成已開航。 |
| `s57105` | [L5432–5435](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5432-L5435)把 **19–20 日**寫信、將馬紐埃馬劍及矛頭等器物裝入大鐵箱，並計畫由史丹利送回家列在同段。旁白及 prompt 都停在裝箱／寫下託送安排；沒有畫交箱或說已送達。 |
| `s57144` | [L5812–5818](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5812-L5818)明記 **2 月 20 日**從 Agnes 得四件法蘭絨襯衫、最初缺 733¾ 碼、藏布拿出後仍缺 **436½ 碼**；[L5747–5749](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5747-L5749)明指 Agnes 為女兒。新句不重述 18 日史丹利援助或 20 日藏布回收，前一句 `s57143` 已交代回收。 |
| `s57189` 引註 | [L10–60](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L10-L60)包含編者 Waller、書名及 1874 年刊記；R8 標籤擴至 L60，修正 R7 的小型引註精度註記。結尾只說日記**文字**收入編刊版，不推定實體日記如何交給編者。 |

高風險未改處也重新比對：[S9305–9307](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L9305-L9307)與[L5252–5263](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5252-L5263)對精確相遇日不一致，本片仍未口播確切日；[L5796–5818](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5796-L5818)仍是 18 日新援助、19 日藥品、20 日藏布拿出與剩餘缺額的次序；[L5873–5881](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5873-L5881)仍支持 3 月 14 日封日記託史丹利；[L10254–10275](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L10254-L10275)仍屬僕人追述與編者推定，口播維持「1873 年五月初」。

## 全稿對齊與書面分鏡

逐一比對 **162 個唯一 scene ID、162 列 claims 與 162 個 script 標記**，次序及旁白文字 **162／162 完全相同**。`claims.md` 的 **184** 個 S／L URL（S 47、L 137）均指兩個固定提交，起迄行號在各自原始檔範圍內。`video.json` 維持 `format: drama`、`look: {"preset":"cute-mystery"}`，144／162 景為插圖、18 景為排版卡，配樂仍使用系列固定設定。`lint --slug curio-s57 --json` 實測 **0 error／0 warning**，估時 13.764 分、第一章 00:45，未因修稿破壞開場或系列畫風設定。

四個新 prompt 各以**單一人物做一個主要動作**示意：`s57101` 李文斯頓打包、`s57104` 一名划船者穩住船、`s57105` 李文斯頓裝箱、`s57144` 李文斯頓摺襯衫。沒有要求可讀文字、實際寄達的鐵箱、未到齊的人手或不存在的書信；舊圖風格及情節的最後判定仍須看 MiniMax 原生圖片與 judge。未改的 `s57139` 交接布包等多人動作可能增加生圖難度，但原文有交付新援助、畫面也未冒稱不同日期；實際圖片如手部或人物動作混亂應依原生圖退件，不把紙上 PASS 當圖片驗收。

**非阻擋編輯註記：**`claims.md` 首段仍寫「R7 作者候選稿」與 R6 關卡，雖然本表 162 列已是 R8，與 `brief.md`、本收據的版本文字不一致。下次創作修訂宜同步更新此首段；若現在改，須重新綁定本收據及新雙盲的五檔雜湊，不能暗改已凍結檔案。

此 PASS 僅限固定史料、逐句主張及**書面**分鏡。R8 仍需兩位新隔離讀者的正式固定 OR 敘事合併、policy gate、網站試聽／核准、付費語音與實際圖片驗收、合成及上架。
