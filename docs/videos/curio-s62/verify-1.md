# S62 R8｜固定史料及逐句畫面查核總表

2026-10-22 UTC。**PASS**。本檔供影片 QA 的 `verify-*.md` 事實關卡讀取；完整逐句與逐景獨立查核在 [R8 來源／畫面收據](review/r8-independent-source-visual.md)，雙人敘事結果在 [R8 正式合併收據](review/r8-formal-merge-audit.md)。此檔不宣稱插圖、語音或正片已完成。

| 固定主張群 | 查核結果 | 史料及界線 |
| --- | --- | --- |
| G01–G02 鏡筒與測量限制 | CONFIRMED | 1610 年作者本文，固定英文譯本 L473–568；不稱發明第一支望遠鏡。 |
| G03–G06 1 月 7–11 日位置、雲夜、初步判斷 | CONFIRMED | 原文 L1267–1343；遮擋與環繞各依作者當時說法，不當成現代逐星辨認。 |
| G07–G10 1 月 12–24 日第四點、貼近與重疊 | CONFIRMED | 原文 L1344–1491；一夜看見的點數不等於總數。 |
| G11–G13 2 月至 3 月的遠星對照與結論 | CONFIRMED | 原文 L1588–1828；不畫成精確軌道，也不聲稱已算出各點周期或單憑此證明日心說。 |
| G14–G15 書中命名與續測邀請 | CONFIRMED | 原文 L250–377、L1258–1265；與 1880 年譯者註解分開。 |

固定來源為 Galileo 1610 年 *Sidereus Nuncius* 的 Carlos 1880 年英譯與編註，GITenberg commit `6672b6c62a0f30e9bb9b84410ef48c6698c37ea5`，raw SHA-256 `74fc9b817b64bc33415c6a44100c30f48952bc531d380682e5f4f1a26cc56fb5`，逐條行號與連結見 [research.md](research.md)。R8 獨立查核確認 **114／114** 句旁白、**110／110** 個書面插圖提示、**4／4** 張資料卡，以及 **134** 個固定來源行錨；`video.json` SHA-256 `c9f249ab7210fa4fb2cf2ac5206c57735ee19efcf0e846414bcfc06bb0745ace`，`script.md` SHA-256 `c638b0d28cfbf6b398cd3bb541160685403bf3936fcd1613bc958921623e4326`，`claims.md` SHA-256 `50f4b272576e90e3a172fd996fc27995223cd32cf0163264308109e6a3833c73`。沒有任何仍被影片引用的 `NOT FOUND` 主張。

正式雙讀者敘事逐題 OR 合併 **13／13 PASS**、CLI exit 0；A 單票的 `no_toc`、`no_recap` 疑慮保留在完整合併收據供編輯查看。正式 lint 0 error／0 warning，書面插圖占 110／114（96.49%）。上述只核已寫成的內容，不代表實際語音、圖片、片長與上傳品質已通過。
