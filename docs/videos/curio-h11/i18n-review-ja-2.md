# H11 日文翻譯獨立審稿（第 2 輪）

日期：2026-10-16（Asia/Taipei）。審核對象為 `C:/Users/x8120/mokaair-work/videos/curio-h11/i18n/ja.todo.json`，SHA-256 `B91761B8D207E7FF383168BC0AA3F713B5B62A06DFF10AD30929D08085521D22`；對照繁中 `video.json` SHA-256 `4D2AE2A2C3D12D634A1333317FD25A816785B8A44DC6BB6E68C1E27A305532DF`。此結論僅評日文翻譯，不代替更正後繁中劇本的站主核准、補錄旁白、音訊 QA 或語言送審。審稿員未修改工作表、來源或媒體。

**結論：HOLD，1 句必修。** 上一輪 [日文審稿](i18n-review-ja-1.md)的必修項已修正；`v173f6fc` 仍應明說是背面綠葉透出、遮住首頁余白的筆畫，並保持です／ます語體。修後重新計算工作表雜湊與 `cuePieces`，再獨立複核此句。

| ID | 問題 | 現文 | 建議的最小修法 |
| --- | --- | --- | --- |
| `v173f6fc` | `緑の葉が透けて見えにくい` 容易讀成「綠葉本身不清楚」，沒有明白指出被遮住的是首頁余白筆畫；`見えにくい。` 也轉成普通體。 | `最初のページの余白は、裏面に描かれた緑の葉が透けて見えにくい。彼女が専門家に処理を頼むと、筆跡がさらに見えました。` | `裏の緑の葉が透け、最初のページの余白の字は見えにくくなりました。専門家の画像処理で筆跡がさらに見えました。`（53／60 字；本機 `cuePieces` 在兩句之間切開）。同義短句亦可。 |

## 複核範圍與已解決項

- `parts = metadata,captions`；75／75 句 ID、場景、繁中來源文字和順序對應新版 `video.json`，7／7 章名及標題、說明、標籤的來源欄也一致。所有譯文都有值；75／75 句低於各自 `max_chars`，其中 9 句超過約 40 字建議值但已分 cue，最長是待修的 `v173f6fc` 57／60 字。這是文字預算檢查，不證明配音已符合時槽。
- 前輪 `v0e564e3` 已同步「四葉」，譯成 `4葉の羊皮紙から…計4本`；日文標籤已刪頻道名。`v8949601`、`v14ba199`、`v404103f` 以本機 `cuePieces` 再跑，已無助詞獨立起頭或切斷「手稿／まで」的問題。
- `v965353b`、`v173f6fc` 已以 `最初のページ` 區分頁與葉；`v37a7ba4` 明寫拉丁語或義大利語的已知文章是模型輸入；`v6911d5a` 改回羊皮紙；`v9e503a3` 不再承諾解開全文；`v7cc1054` 已把先前公開的範圍限為部分細節。2019 年撤下的是大學新聞，沒有說論文撤稿；Marci 比對仍屬初步；Naibbe 沒有被說成解出原稿。
- 標題 23 字、7 個章名各 13 字以內，標籤譯文合計 48 字；縮圖三欄均有譯文，保留 `\n` 與 `**`。說明欄保留 2026-10-16 查核日、Naibbe 作者 README 的範圍，以及 AI 插畫揭露。

史料界線參照 [羊皮紙原始定年報告](https://www.voynich.nu/papers/Carbon_GH_2009.pdf)、[Beinecke MS 408 目錄](https://pre1600ms.beinecke.library.yale.edu/docs/pre1600.ms408.htm)、[布里斯托大學聲明](https://www.bristol.ac.uk/news/2019/may/voynich-manuscript.html)、[Davis 多光譜研究紀錄](https://manuscriptroadtrip.wordpress.com/2024/09/08/multispectral-imaging-and-the-voynich-manuscript/)及 [Naibbe 作者 README](https://raw.githubusercontent.com/greshko/naibbe-cipher/main/README.md)；本輪核心是對已審的翻譯逐欄再核，沒有替來源重新做獨立史料查核。
