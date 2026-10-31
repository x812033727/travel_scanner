# S49 R22｜首章尾端三張首試原圖驗收與停畫

2026-10-22 UTC。[R22 三景獨立書審](r22-first-chapter-tail-prompt-independent.md)按精確檔 **PASS** 後，只對 `moon028/030/031` 執行 MiniMax `image-01 --takes 1`。命令在 EXIT trap 暫移私有 `STOP`，結束時恢復。三張均生成，沒有第二次嘗試或啟動下一章。我直接打開三張 **1280×720 原生 JPEG** 與裁後選圖，對照旁白、來源層級、動作、年代及 judge；機器三張都 PASS，不代替原圖判斷。

| 景 | 原圖 SHA-256 前 12 碼 | 選圖 SHA-256 前 12 碼 | 機器 | 直接原圖結論 |
| --- | --- | --- | --- | --- |
| `moon028` | `d24eaa7a43dc` | `48c1cf7cc044` | 9.29 PASS | **KEEP**：灰髮成年讀者、單一泛用報紙與小月亮圓圈，桌上沒有 Grant／皇家學會兩份似原件文件，也無可讀字。人物雙手靠桌而未指圓圈，是次要手勢差異；4.5% 裁邊後來源安全。 |
| `moon030` | `bf2372ee8e31` | `bc965c99c5e7` | 10 PASS | **技術 HOLD**：成年舊式學者在單張紙畫兩個分離圓圈，R21 假實體望遠鏡／三腳架已消失；但原圖頂底有黑色信箱邊，5.9% 自動裁圖仍在頂部留下約 5 像素近黑細條。依批次策略，選圖邊緣未乾淨前不計 KEEP。 |
| `moon031` | `6e297a01226b` | `c07bae3d6d80` | 9.29 PASS | **REJECT**：成人與舊式服裝取代 R21 孩童及現代燈，但應無字的報紙呈現密集擬文字列，紙上另有**實體小圓筒**，不只是扁平墨線。judge `details` 指出同一錯誤卻仍 PASS；裁圖不能修來源／物件誤導。 |

[完整清單](r22-first-chapter-tail-native-inventory.json)保存三張原圖、選圖完整 SHA-256、judge 原文、人工理由、前後帳本與圖單。`moon030` 黑邊是直接看原圖與選圖、再以**只讀像素檢查**確定：原圖頂列幾乎全黑；選圖頂列仍約 75% 近黑，約第 6 列才清乾淨。可先評估既有標準裁邊流程能否無新增付費、可追溯地修正；若仍有邊，按此圖回修提示詞及獨立書審。`moon031` 需窄修「印刷欄／浮起的鏡筒」模式，再看原圖。兩景未放行，不因 `needs_review=false` 自動送分鏡。

付費前已私有備份 manifest、ledger、此前 24 張 KEEP 選圖 SHA，及 R21 `moon030/031` 舊圖於 `/workspace/.video-work/curio-s49/review/r22-first-chapter-tail-pre/`。新 manifest SHA-256 從 `cb9f8dd0d2f4e4906f1b42a12e78efbfe69a0a25af84eec38dc62fbb2dbc7765` 變為 `29fd2d89b96cb1dc609db00263337db9a46cd06089b462151940c399d0095d06`；原有 **24 張 KEEP** 項目及選圖檔 SHA 逐一不變。帳本 **US$0.9315／69 image／69 judge** → **US$0.9720／72 image／72 judge**，三圖三評審正好 US$0.0405，0 音樂、0 預約；低於本集累計 **US$5.30** 上限，餘 US$4.3280。`STOP` 現在存在。R22 創作檔 `video.json` `26a4812f…`、`claims.md` `4e25e983…`、劇本 `82369f76…` 未被畫圖修改。

首章 `moon030/031` 仍待處理，全片 121 張插圖也尚未逐張通過。CLI 的 `next: review-push --gate storyboard` 是通用提示，不能據此送全片分鏡。網站 outline／script／audio 卡仍待站主；人耳聽審、配樂、片頭片尾、成片、Shorts 與 Studio 連結仍未完成。
