# S49 R28｜`moon032` 來源卡重綁、`moon033` 單張原圖驗收

2026-10-22 UTC。**`moon032` 來源卡重綁 PASS；`moon033` 原生圖人工 KEEP；全片 storyboard 仍 HOLD。**本輪只在[非作者 R28 來源卡紙審](r28-moon032-source-card-independent.md) PASS 後，安全重綁私人圖單，並沿用[非作者 R27 `moon033` 書面紙審](r27-moon032-033-prompt-independent-pass.md)，限界買一張 MiniMax `image-01` 原圖及一次 judge；沒有畫 `moon032` 或 `moon034–039`。

## 圖單與來源界線

固定 `video.json` SHA-256 `a4d00cdc41078cc016247127c5a3676bb8a8ee98699662395bd2cfdc1f4b62a2`，`claims.md` `b89b557b52bb98dd3e4d654b665e4cd874434784a5850d71044323c7543a44e3`，`script.md` `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`。`moon032` 的同屏「1835 年報導的虛構構想／物鏡架高處，焦像進暗室／1859 重印本所載，非實作紀錄」維持來源卡；原生退圖沒有回到所選圖單。`moon033` 旁白把反射鏡寫在報導中的 Brewster **虛構對話**，並非真實建造紀錄。

重綁前私有 manifest SHA-256 `694b319ccaaf0da0e4ed9079620945b6b95588c5a95439ec2f89d8f5d8607615`，綁 R27 `visual_hash=74c5cc0713c7766d`。先核 `STOP` 存在、jobs 為空、帳本無預約、26 個 KEEP 的選圖檔 SHA 逐張相符，再逐位元備份原圖單；只改 `visual_hash` 為工具重算的 R28 `dfe0bece015e7458`，`look_hash=98a370ae40badbaf` 不變。重綁後 SHA-256 `81fc3b828989e750f8493aa873183e4fa2f21d88ba29bf73acbf2e434795c83b`；26 個完整 shot 項目、所選檔及實際 SHA 全部不變。`moon031/032/033` 此時都無圖單項目；`keyframeProblems` 僅列 93 張未畫，既收圖無錯。

## `moon033` 原圖判定

即時 `media-status` 確認 MiniMax `image-01`、每圖 US$0.0035、圖片與 judge 供額；定點 `--dry-run` 提示詞 446／1070 字元，估單 take 約 US$0.0135，帳本當時 US$1.0395，低於整集 US$5.30 上限。受控命令只執行 `keyframes --slug curio-s49 --shot moon033 --takes 1`；CLI exit 0，原生圖及選用裁圖均為 **1280×720**，私人路徑 `keyframes/moon033-1.jpg` SHA-256 `25dc9e4e97a56da9b765ff6122ca97570ba4f5beaa2025d0c61b4d3571fca460`、`keyframes/moon033-1-trim.jpg` SHA-256 `64bdacae036eab4549c4a8e28951dfe697a14d2e631ece384449dc84a37bd7aa`。原圖、裁圖、機器 contact sheet、前後 manifest／ledger 和 CLI 紀錄均另存私人 `review/r28-moon033-native/`，防後續同名重畫覆蓋。逐項及前 26 張 KEEP 實檔清單見[機讀庫存](r28-moon032-card-moon033-native-inventory.json)，其 SHA-256 `8a290952ac5b295f8f3c52a1698ded555a08d4a4e40b9633f26a460beb6f2956`。

機器評 **9.29／10 PASS**，指出缺上唇鬍子。兩次獨立原生目視同判 **KEEP**：成熟灰髮、鬢角、深色高領外套的成年人物，用空手清楚指向普通素面橢圓牆鏡；室內有自然側光，沒有童貌、東亞式衣帽、現代頂燈、可辨文字、黑邊或真天文台器材。手中靠下的短紅頭桿可讀作手杖／指示桿，不是可辨現代儀器。鬍子與可見百葉窗缺席、光束較寬；鏡面沒有可見焦像，因此本圖只作**虛構反射鏡構想的插畫**，不能宣稱是史料中的實驗或真實月面觀測。這些落差不破壞本句核心「指出反射鏡」關係，`moon033` 可列單景 KEEP。

完成後圖單 SHA-256 `de46aa231b3f4c22633e93b9261fcc0a381051190530ea78b933ace70f74d87f`，原 26 項仍逐項相同，新圖為第 27 項；`keyframeProblems` 僅剩 **92 張未畫**，其他問題 0。帳本 SHA-256 `076a31adf1dd34d89a11ecc9a18c819bbaa7bec3164b56098fb1d5db4ebb9275` → `01a0d7c5460a5afa00b208547ae50b0ea35d61311294d930e21a9e29a6cab418`，US$1.0395／77 image／77 judge → **US$1.0530／78 image／78 judge**，0 音樂、0 預約，低於 US$5.30；`STOP` 已恢復，jobs 空。**在下一景另定有界驗收前不開畫 `moon034`。**網站卡、人耳、其餘畫面、片頭片尾、Short、成片及 Studio 連結仍待。
