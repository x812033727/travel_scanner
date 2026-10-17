# B18 第 95 景旁白分段修正候選（2026-10-17）

**狀態：離線窄幅候選；整片仍 HOLD。** 從 [字卡與共圖意圖整合候選](../B18-visual-card-reuse-integration-candidate-20261017/README.md) 的 `sha256.json`（SHA-256 `d950454ac96598ec59c1391731e4e0c0f9eae54c702123b4d9b3b3afb1675d1f`）重建，不改舊包、正式主機、工人或媒體。這份只處理獨立審讀指出的 `now-s095/8b88e002` 單獨逗號，以及拆在兩景間的不完整口播句。

`now-s095/bb7022f4` 現在完整說明 2021 年第 112 號認定；原本只含 `，` 的 `8b88e002` 改為完整句，交代 1985 年製的機器在認定時仍於堺東店使用。`now-s096/1585ea8b` 完整交代元祿產業另外保存的早期「魚鱗板」也在同一項認定之內。第 112 號主張 `n4.scene` 隨旁白由 `now-s096` 移到 `now-s095`；其 `source: 1`、`fact: 8`、`UNCHECKED` 不變。這些事實對應[日本機械學會第 112 號原頁](https://www.jsme.or.jp/kikaiisan/heritage_112_jp.html)。畫面、卡片、其餘旁白、其他 64 項主張與原共圖意圖原樣保留。

`node build.mjs --write` 生成本包；`node build.mjs --check` 以來源與本包 SHA-256 逐位元組核對。官方合稿、`lintProject` 與 `cuteStoryVisualProblems` 在離線假資料夾重跑。輸出詳見 [delta.json](delta.json)、[verification.json](verification.json)、[sha256.json](sha256.json)。第 95 景兩句、第 96 景一句，各自完整；總數維持 93 行，沒有獨立標點行；片長仍是字數／鏡頭估算，不是 TTS 實測。

lint 零錯、可愛畫風零錯；警告由舊包的 22 增至 23，其中新類型是依**估算**鏡頭秒數產生的 `craft pace.spread`。這一點要和實際配音及整段剪輯一起重看，本窄修沒有替整片節奏背書。

原獨立全稿審讀的**後半段敘事 HOLD** 與 `turn-s072` **主張覆蓋 HOLD** 仍在；正式逐章查核、聽眾審稿、劇本收據、語音、圖片、CC、三鏡樣片、成片與站主看片尚未完成。本候選不是全片查核 PASS，也不授權 B18 付費製作、匯入或上傳。
