# A29／A16 episode row 交接證據

狀態：兩筆 story row 均已由另一位審稿者獨立核對，審稿收據各自綁新內容 hash，並與另三題編成[五集本機輸入](../stories.json)。尚未在正式主機 dry-run、apply、製作媒體或上架。系列 slug 為 `brand-stories-curio-five`；系列資訊由組裝檔提供，story row schema 不接受額外的 `series` 欄位。

## 來源與雜湊

抽取基準是 [`brand-stories-100/stories.json`](../../story-plans/brand-stories-100/stories.json)，檔案 SHA-256 為 `c8fb18102634459c62f556022139e0bdc733ef432321c412ff810faed0ac0194`。下表的母企劃及原審稿均在同一 `brand-stories-100` 目錄；原審稿於 2026-09-28 給出 `fixed`，其 `story_sha256` 只綁定當時母企劃，**不代表這次重排的章節已獲審核**。

| ID | 母企劃檔案 SHA-256 | 原審稿檔案 SHA-256 | 原審稿綁定的 `story_sha256` |
| --- | --- | --- | --- |
| [A29](../../story-plans/brand-stories-100/stories/A29.json)／[review](../../story-plans/brand-stories-100/reviews/A29.json) | `5802ac3dbb5a5b823f1cadcd04b793e8ac6d041bf012279c1516fe0b2904a59c` | `e6768539e4a458dcc1b03ff9e34013a925cd0c40644b61026e33efc6284dad5c` | `010bb29f7bb1041d9d1079607485ae5a42a61a522a22b5a0f87a6d82a044e1b0` |
| [A16](../../story-plans/brand-stories-100/stories/A16.json)／[review](../../story-plans/brand-stories-100/reviews/A16.json) | `bd2895c18ebdd17381804b7e2bf7ee7a128b4f1f9e931d92f2eb39026aa43d9a` | `3a8419705a172265f2898d0b4e42a81ffde9e426bb6912e766c5ac9df0b9a8bd` | `3fbce19194b53282f47679e9f4f66b6805f297a36c1e95bae6106c658980c8d9` |

## 這次的兩筆 row

| Row | 新 slug | 序號／發佈時段 | 檔案 SHA-256 | 新章節內容的 `storyHash` |
| --- | --- | --- | --- | --- |
| [A29.json](A29.json) | `story-five-lego-legoland` | 1／第 1 天 12:00 | `e669ab136e5d52faf24d498aa1b9456a22269143665ea369274ecee70a1c8b87` | `61c2d43d80306280bd03c0564546b561d858a74a58a1919ed7afd15096d5210b` |
| [A16.json](A16.json) | `story-five-costco-hot-dog` | 2／第 2 天 12:00 | `c17b3f68ba706b91080c3b54d7efa60c9dd5ec6211c18ebc8c23c36c543ebbbb` | `a577be0d1b974f3c9fb1068c1d73dd818e1312c4522f63f07c79cfbcbfe26ef1` |

兩個新 slug 與母題庫、目前 `episodes/A21.json` 的 slug 均不相撞，故可在五支系列中保留原題庫 ID 而避免 slug 衝突。A29 從母題庫序號 33／第 17 天 12:00 改為 1／第 1 天 12:00；A16 從序號 3 改為 2，原本已是第 2 天 12:00。機械比對確認，除 `number`、`slug`、`publish` 的上述差異及六個 `chapters[].point` 外，其餘欄位與編譯母 row 相同，包括 `category`、`region`、`must_verify`、`sources`、`names`、`cast`、`image_notes`、`caveats`。六章 key 順序保持 `hook`、`origin`、`idea`、`engine`、`turn`、`now`。

章節重排按 [A29 treatment](../A29-lego.md) 與 [A16 treatment](../A16-costco.md) 的事件順序：A29 先呈現賣獲利樂園的矛盾，再由 1932–2003 年鋪陳危機、2004 年應對、2005 年交易與 2019 年所有權；A16 從 2024 年價目表回到 1976 年 Price Club、1983 年 Costco，再講熱狗成本解法、2025 年財報與續費。章節點不是逐字旁白稿，10 分鐘長度仍須另經腳本、配音與實際音檔確認。

## 獨立審核時的事實邊界

- **A29：** 2003 年約 14 億丹麥克朗是稅前虧損的約數，兩版年報重編口徑不同；1998／2000 年虧損、2004 年樂園稅後獲利及 KIRKBI 次順位貸款等數字，原 review 仍標示依靠年報 PDF。不得把開園與集團虧損寫成已證明的單一因果，也不能把 2019 年 KIRKBI 參與 Merlin 私有化說成樂高集團買回樂園。
- **A16：** 熱狗起始年份只寫「1980 年代中期」；Jelinek 與 Sinegal 對話的發生年份未證，2018 年是 Jelinek 轉述時間。2025 年會員費／營業利益約 51% 是兩行財報的比值，不是單品補貼或公司自己的獲利分攤說法；2024 年財務長及 2026 年執行長的價格表述均須註明時間。

新章點已分別由 [A29 review](reviews/A29.json)／[A16 review](reviews/A16.json) 核對，`reviewProblems=[]`，`build.mjs` 已用五份新審稿編成 `stories.json`。A29 的六份年報 PDF 可由審稿者閱讀，但本機 worker `--fetch` 不能轉成正文；它的每條 `must_verify` 另有至少一筆可讀 HTML，故依驗證器定義 `reviewer_only=[]`，仍須在逐字稿逐句複核 PDF 頁碼及數字。兩題的母題庫 `fixed` 只提供來源交接，五集版以本次新 review 為準。主機 live 狀態、實際腳本與媒體仍待驗。
