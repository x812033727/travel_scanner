# S57 R9｜獨立史料與書面畫面覆核

2026-10-21 UTC。**史料／逐句主張 PASS；書面畫面 PASS。**本判定只對下列 R9 固定五檔有效。我未參與 R9 改稿；未修改創作檔、製作付費媒體，亦不代替隔離讀者的敘事、政策或站主核准。

| 創作檔 | 覆核前實測 SHA-256 |
| --- | --- |
| `research.md` | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| `brief.md` | `c7900d23f61699c506abbde288aadbe2d32c0e5020721a2e2c44ee04ff2876ea` |
| `claims.md` | `241f5a2fa4b25e977baf832907213b7be98cda7a9cfa55ea58331f0a31466beb` |
| `video.json` | `940046297c87511a82c9e42eb5d0c0fbcf8bdaa9b5528ce17234ac77c7cf8588` |
| `script.md` | `7edc924366e588787794e9c2ceac53ce8f5131188f19aa9c0a71a3543c326b43` |

## 原文、差分與史料結論

我獨立取得兩個固定 Git 提交的原始文字，沒有只沿用作者引文。[S：史丹利出版敘述的節錄本 `5157.txt`](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt) SHA-256 `de84c2eb2089e18c8e080fe24ecac95c44c1cc993be355987cdd3221036d158f`；[L：Waller 1874 年身後編刊《最後日記》第二卷 `17024-0.txt`](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt) SHA-256 `e6658569be045054c89e59c2aac9819a430a9a84fbdbed289a2ba0fa27750962`。下列行號屬電子轉錄本，並非手稿頁碼。S 的班奈特對話及送行細節是史丹利後來的出版敘述；L 包含本人日記、Waller 編刊及僕人追述等不同層級。

[R9 作者精確差分](r9-author-diff.patch)的 SHA-256 是 `64899a0941250700708a076ce6e697324a7a3c7920baff00427df454ded776c3`。我在 `/tmp` 副本反向套用它，五檔 SHA 逐一還原成[R8 固定版](r8-source-independent.md)所列的 `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667`、`5eadc760e95287cebc97c61007333007348939c18ec505d38ddd9acc5cb88abd`、`cff4abfd700e501ecdc32700138fda27d143320f0f666f233d2792266e0cc861`、`bb0cf8d70f565a0c34d0923c08678665b26e24c6637d208d96f474dafb5841d4`、`d9605ab9b06528780454cdecd6af3604e34e1be3e09a379ac14e4b46a3fa674d`。解析兩版 `video.json`，除刪 `s57163,s57180`、改 `s57016,s57032,s57161,s57162` 四句與其中三個 prompt 外，其他場景和頂層欄位相同。`research.md` 不變；`brief.md`、`claims.md` 同步版本說明與逐句引註，`script.md` 重生後場景序號隨刪景前移。

| R9 改動 | 固定原文的支持與限制 |
| --- | --- |
| `s57016` | [L5219–5223](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5219-L5223)先記抵烏吉吉受到迎接、每日市場有食物，**傍晚**才從自己的人聽到貨物已賣的消息。新句保留日內先後；`s57019` 才揭示具體壞消息。原文稱迎接者為「Arabs」，新句「商人們」是場景性概稱，不是逐字翻譯或每人職業的獨立證明。 |
| `s57032` | [S89–109](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L89-L109)有按自己計畫行事及先領一千英鎊、用完再領下一筆的指示。新句明說「按史丹利的回憶」，未冒稱班奈特的獨立證詞，也沒有演成確證逐字對白。 |
| `s57161` | [L5868–5871](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5868-L5871)記 **3 月 10 日**交史丹利五千盧比支票，僅在 Kirk 已花完先前一千英鎊餘款時才兌，否則銷毀。旁白的「備用／原有款項用盡才兌」保留條件；沒有說已兌、已購貨或已送達。 |
| `s57162`、刪 `s57163` | [L5873–5881](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5873-L5881)：**12 日**條目僅「Writing」，**13 日**才記完成兩份文件，**14 日**才記史丹利離開及封日記託交。新句沒有把 13 日完成的文件提前，也不再第三次報寫信。 |
| 刪 `s57180` | [S14392–14443](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L14392-L14443)記送行、蘇西和楚馬等人在場；保留的 `s57179` 已報在場者。刪去換句重述未消除這一來源層級。 |

未改的高風險處亦覆核：[S9305–9307](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L9305-L9307)的相遇日與[L5252–5263](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5252-L5263)括號日期不一致，本版仍只說「晚秋」；[L5796–5818](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5796-L5818)及 `s57139,s57142,s57143,s57144`仍維持 **2 月 18 日新援助→19 日藥品→20 日舊藏布拿出及剩餘缺額**，未把布包追回提前。[L10254–10275](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L10254-L10275)仍屬僕人追述加編者推定，片尾只稱 1873 年五月初。

## 全稿對齊與書面畫面結論

我逐一解析 **160 個唯一 scene ID、160 列 claims、160 個 script 標記**，ID、次序及旁白文字 **160／160 完全相同**，script 序號亦為 1–160。`claims.md` 的 **182** 個 S／L URL（S 46、L 136）、`research.md` 的 27 個及 `brief.md` 的 2 個均指上述固定提交，行號落在原始檔範圍；`video.json` 的兩個來源條目和說明欄 URL 亦指同一固定全文。`video.json` 有 142／160 個插圖鏡頭、18 張資訊卡、15 條 loops；`look` 僅為 `cute-mystery` 預設，配樂參數保持系列設定。實測 `node tools/video/cli.mjs lint --slug curio-s57 --json`：**0 errors／0 warnings**、160 句、估時 **13.778 分**，第一章後轉場於 **00:45**。

三個新 prompt 均是一位主體做一個主要動作：`s57016` 一名迎客者舉手、`s57032` 一名記者整理素面紙、`s57161` 一名旅人折素面付款紙。三者都不要求可讀文件、精確歷史路線、支票已兌或多人互動；改句但未改 prompt 的 `s57162` 仍是一人書寫。刪掉兩景後，告別的 `s57179` 留作單人示意，不假裝重建整支隊伍。

**界線：**書面 prompt PASS 不是 MiniMax 圖像的實際驗收，尤其 `s57016` 的「local merchant」與原文「Arabs」並非可驗的個人肖像；成圖若誤示具體身分或動作仍須照原生圖片與 judge 檢查。R9 還需兩位真正隔離的盲讀者正式敘事合併、policy gate 及後續站主與媒體關卡；本覆核不替它們判 PASS。
