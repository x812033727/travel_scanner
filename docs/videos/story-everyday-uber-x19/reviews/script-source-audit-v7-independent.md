# Uber X19 v7｜獨立 SEC 原件與修稿查核

**事實 PASS；敘事雙盲和正式媒體另驗。** 本票綁定 `video.json` SHA-256 `f4e373a53a3424f29f9c3e511f13c2489ac9c7e93c4500413038060d8d08a385`、`shorts.json` `b6b0212372d776c96572450baa8e9c4350499c72923d088ad0bd6833e8681d95`、`source-matrix.md` `5e949609bf8163b28cfeea3ca3592c52855e6ece34f52f3da37549efe3d31043`、`drafts/narration.md` `959b8da99002f86239897d52fbc2559b22bf040f179bc8d3e91178fccf965d6f`、`visual-plan.md` `137cd29316b1ec634d299f23b543974a865d77415916ea2d83ae8afad0c668ee`。任一受審檔案再改，須重新查核。

2026-10-21 我從 v7 矩陣 URL **重新 HTTP GET** S1–S8、S3a、S5a 共十份 Uber 提交 SEC 的 issuer originals，解開 HTTP gzip 後各 HTTP 200、各低於 3 MiB。今日原始 HTML bytes 和 SHA 如下，與同日 v6 獨立重抓相同；**不同於矩陣記錄的 10/20 原始 SHA**。先前已逐份隔離出 SEC 頁尾單一輪替 script 標籤，不把正規化後的吻合冒稱兩日原始位元組相同。

| 原件 | 今日 raw bytes | 今日 raw SHA-256 |
| --- | ---: | --- |
| S1 | 548,316 | `4aef7703ea764828bc5f93a9b1792c66653df195514aea77206b07e27f272512` |
| S2 | 829,748 | `7b0c4bd318d0cd35899157b6027c21966225833a5590d0d973721b85e49c6780` |
| S3 | 53,764 | `f1d55c4ff0cc805b5182fb4762691bb47af7ff8e571513480523329af8cac5b5` |
| S3a | 37,486 | `1c93dbf8e1d25f0ea3d1876b10672e1aa61107b68b51c104f87db728e074a461` |
| S4 | 512,053 | `ab2391b5d58283794e266c2d2ae664b2a13a02ec796af7df2ea3af388ec71eef` |
| S5 | 8,692 | `efa0a6afb043dd3009cbe0c514b59b2ca0424b4475d9097b3b5608dac3156d30` |
| S5a | 33,744 | `66201fcd39ff41e2f4b5d6589de0cae6bedfcccebfc70fa789d084b35e8419f0` |
| S6 | 499,879 | `a61d34a9ad1be17ab40692314e3ebedceb4d988a44b3b3ec8e2ef93241abddfc` |
| S7 | 520,393 | `55891e3d97914c0b699734703265da8ce3387f2c891329c188e7dcbebe181b40` |
| S8 | 583,078 | `9270b2d4aa90a0225e510c8666eed917b6c96fb98ca73f427ccc8e667fcc6d82` |

我將 v7 的旁白、卡片、Shorts 和上架說明與上述原件和 [v6 逐項事實審核](script-source-audit-v6-independent.md)重新比對。唯一**口播事實差異**是 `x190421` 從「收購仍只是紙上的約定，另一套 App 還沒有接進來」刪去前半句，剩「另一套 App 還沒有接進來」。這是較窄、仍受 S4 當季未交割與 S5 交割時兩個消費者 App 仍各自存在支持的敘述；沒有把七月簽約、十二月交割或 2021 年整合倒填進六月反超的因果。其他日期、訂單額、營收、調整後部門 EBITDA、Postmates 五百萬消費者遷移和 2021／2022 後續轉折口播不變；Shorts 的兩條時間線與分母亦不變。S3 電話會逐字稿有一句孤立的 “100% cash consideration”，仍以 S3a 正式 8-K 和 S5/S5a 交割公告的 **all-stock** 口徑為準，未採孤句。S6 的 Delivery 虧損同比收窄 US$71m 仍是**部門合計**，不能拆歸 Postmates。

原件均低於工人 3 MiB；本次是完整來源重抓與人工逐項比對，正式工人仍須驗證關鍵錨點擷取實際命中。事實 PASS 不代表兩名全新首讀者的同 SHA 敘事 PASS，也不代表實測 TTS 正文 ≥8:00、官方 5 秒片頭／21 秒片尾、畫面／字幕 QA、US$25 實際結算、MP4 或真實上傳連結。
