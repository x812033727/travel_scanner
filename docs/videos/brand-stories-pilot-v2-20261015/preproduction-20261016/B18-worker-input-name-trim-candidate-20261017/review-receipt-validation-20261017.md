# B18 新版企劃查核收據：離線驗證

2026-10-17，`/root/b18_name_delta_review`。候選 [reviews/B18.json](reviews/B18.json) 是**與新版企劃雜湊綁定的資料列查核收據**，保留在隔離目錄；沒有覆寫 `episodes/reviews/B18.json`，也沒有寫入可匯入的 `stories.json`。

- 候選 row SHA-256：`209fb773139e96afd5a56f373b6f0843eca902f81b374c19bcd9bc8a4d78e3dd`；canonical story SHA-256：`3c43dc0c0eccdb063cc1e62d756c48ce2a476c5bfe1a70b74799c8f3cfc475f1`。
- 本收據原始檔 SHA-256：`538d6614c00a102fa0a04fb0fa4e3f3ba11719dede4d8353636c37b2f46c2752`；[獨立差異審查](independent-review-20261017.md) SHA-256：`992175f98869473c0ff151c334818092542857daf3a895167b636f86794bb1a0`。這兩份審查產物不在原候選 15 檔的 `sha256.json` 清單內，避免改寫已核對的候選 manifest。
- 直接使用 `plan.mjs` 重算：`storyHash` 等於收據 `story_sha256`，`storyProblems=[]`、`reviewProblems=[]`；`notes` 425 字元，低於 800 字元上限。`build.mjs --check`、`manifest.mjs --check` 均退出 0。舊 `episodes/reviews/B18.json` 對此新版故事為過期收據。
- 今日用正式企劃讀取器重測六來源：S0 J-Net21、S1 日本機械學會、S2 發明協會、S4／S5 石野集團均 HTTP 200 且可讀；S3 法院 PDF HTTP 200，但 `not a text page (application/pdf)`。`fetchProblems=[]`，因 F4／F5 另引可讀網頁；`reviewer_only=[]` 符合現行規則，**不表示那些網頁證明法院判定的 1972 年**。收據已寫明本人對法院 PDF P8 L466–474、P10 L574–578 的人工核讀及正式 worker 的限制。
- 企劃來源與六章分鏡的名稱掃描未見未證實的 Asahi 品牌作為史實或畫面指示；`image_notes` 仍禁止酒瓶、壽司盤標籤與商標。六章的 **65 筆逐景主張仍全部 `UNCHECKED`**；本收據只核准企劃資料列，不是 worker 逐章查核、聽眾審稿、十三題敘事、TTS、畫面、CC、成片、主機匯入或站主觀看收據。
