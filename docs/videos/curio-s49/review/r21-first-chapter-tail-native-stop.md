# S49 R21｜首章尾端兩張首試退件並停畫

2026-10-22 UTC。[未畫三景獨立書審](r21-first-chapter-three-paper-independent.md)先判 `moon028` **HOLD，不得依現行提示詞畫**；只放行 `moon030/031` 各一張。受控 MiniMax `image-01 --takes 1` 命令以 EXIT trap 暫移私有 `STOP`，退出時已恢復。兩張都已生成，我直接打開 **1280×720 原生 JPEG** 及裁後選圖；沒有重試、沒有畫 `moon028`、沒有啟動下一批。CLI 因 `moon031` 評審 FAIL 以 code 1 結束。

| 景 | 原圖 SHA-256 前 12 碼 | 選圖 SHA-256 前 12 碼 | 機器 | 人工原圖結論 |
| --- | --- | --- | --- | --- |
| `moon030` | `69d3421579b1` | `6c5571225fb0` | 9.29 PASS | **REJECT**：畫面是架在三腳架上的**實體有鏡筒望遠鏡**，不是報導內「省掉鏡筒」構想的紙上草圖。人物也偏童貌。機器在 `details` 明指出主體物件錯，卻仍給 PASS；8% 裁邊沒有修正錯圖。 |
| `moon031` | `75e29ffe7303` | `c697f04689fd` | 9 FAIL | **REJECT**：明顯孩童穿現代針織衫，背景有現代檯燈；手持海報式大圖，不是 1835 年成年讀者看的無字報紙草圖。機器抓到童貌和海報，manifest `needs_review=true`；1.2% 裁邊沒有修正。 |

[完整原圖／選圖清單](r21-first-chapter-tail-native-inventory.json)保留兩張完整 SHA-256、機器問題、人工理由及前後狀態。`moon030` 的假實體器材屬來源層級風險；`moon030/031` 同時暴露成人／年代提示不夠穩。這一批兩張均退，先按實際錯誤定點改提示詞並獨立書審，再考慮受控重畫。`moon028` 仍需先撤掉似 Grant／皇家學會兩份可得原件的實體紙張構圖；不要因其他兩景已生成就跳過它。

付費前已私有備份 manifest、ledger 和既有 24 張選圖 SHA 於 `/workspace/.video-work/curio-s49/review/r21-first-chapter-tail-pre/`。新圖單 SHA-256 從 `b854c37fe4a757f36392a03af5e43f95e844f1fe6ba26f5e965af84ba9d92248` 變成 `cb9f8dd0d2f4e4906f1b42a12e78efbfe69a0a25af84eec38dc62fbb2dbc7765`；前 24 個已 KEEP 景的 manifest 項目逐一與備份相同，選圖 SHA 可逐檔核對。帳本 **US$0.9045／67 image／67 judge** → **US$0.9315／69 image／69 judge**，恰好兩圖兩評審 US$0.0270，0 音樂、0 預約；仍低於整集 US$5.30 上限，餘 US$4.3685。`STOP` 現在存在。R21 創作檔 `video.json` `e01e1d91…`、`claims.md` `87447ad8…`、`script.md` `82369f76…` 未被畫圖修改。

首章尚有三景未過（`moon028` 紙審 HOLD、`moon030/031` 原圖 REJECT），且全片 121 張插圖尚遠未全部逐張驗收；不能送 storyboard。網站 outline／script／audio 卡仍待站主，真實人耳聽審、配樂、片頭片尾、成片、Shorts 與 Studio 連結均未完成。
