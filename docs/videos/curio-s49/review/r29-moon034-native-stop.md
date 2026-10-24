# S49 R29｜`moon034` 原生圖童貌退件與停批

2026-10-22 UTC。**`moon034` 機器 10／10 PASS，但兩次獨立原生目視均 REJECT；`moon035–039` 未開畫。**上一輪 [R28 安全圖單與 `moon033` KEEP](r28-moon032-card-moon033-native-keep.md)已固定 27 張既收圖；本輪沿用 [R26 第二章八景非作者紙審](r26-next-chapter-eight-prompt-independent-pass.md)對未改的 `moon034` 來源與提示詞 PASS，只進行一張 MiniMax `image-01` 原圖及一次 judge。

## 固定版本與費用邊界

付費前 `video.json` SHA-256 `a4d00cdc41078cc016247127c5a3676bb8a8ee98699662395bd2cfdc1f4b62a2`，`claims.md` `b89b557b52bb98dd3e4d654b665e4cd874434784a5850d71044323c7543a44e3`，`script.md` `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`；`visual_hash=dfe0bece015e7458`，`look_hash=98a370ae40badbaf`。私人 manifest SHA `de46aa231b3f4c22633e93b9261fcc0a381051190530ea78b933ace70f74d87f` 含 27 個人工 KEEP，逐張選圖檔 SHA 與完整項目相符，`moon034` 尚無條目。`STOP` 在位、jobs 空、帳本 US$1.0530／78 image／78 judge／0 預約。即時 `media-status` 顯示 MiniMax `image-01` 已設定、每圖 US$0.0035，圖片／judge 尚有充足配額；定點 dry-run 將提示詞計為 308／1069 字元。連同約 US$0.01 judge 後仍低於整集 **US$5.30** 上限。

## 原圖與人工判定

受控命令只指定 `keyframes --slug curio-s49 --shot moon034 --takes 1`，CLI exit 0。原圖 `keyframes/moon034-1.jpg` SHA-256 `9d2f671659859bda7685348d55dc234ebd7ce81809ea59b6070a6b7b3af10113`、選用自動裁圖 `keyframes/moon034-1-trim.jpg` SHA-256 `ba8d5ec9f6a01b9d7d422f3c02b0c44ebbc4707805954ac250ce81f6b8b5e8ff`，均 **1280×720**。機器 10／10 PASS，沒有列問題。兩名獨立目視者都判 **REJECT**：兩個黑髮人物雖穿外套，臉部比例、圓眼、紅頰及髮型明顯偏孩童，缺乏可確認為提示詞要求「兩位成年、1830 年代高領外套人物」的年齡特徵。前一張已收 `moon033` 則可清楚辨出成熟灰髮／鬢角人物。背景兩個明暗不同、無字圓形仍可作抽象光量概念，沒有物理望遠鏡、實測數字或偽原件；**錯誤集中於反覆發生的童貌**。機器高分不能覆蓋這項人工年代／人物退件。

原圖、裁圖、機器 contact sheet、前後 manifest／ledger 和 CLI stdout／stderr 留在私人 `review/r29-next-six-native/moon034/`；[機讀庫存](r29-moon034-native-stop-inventory.json) SHA-256 `e305756cbe4672450e88063226d1f8cfe64764b7d49280b0f0eb67de4ba20ccd` 列出 27 KEEP 的完整項目與實際選圖 SHA。CLI 後 manifest SHA `b1ff0ce2685ab16a963690e7f306fa4f5c7d93b5b66fe56063644d2fe8b83cf1` 曾包含機器 PASS、人工退件的 `moon034`。停批後在 `STOP` 下，把事前 **27 KEEP manifest 逐位元恢復**，且把兩張 contact sheet 恢復為 R28 事前的私人歸檔版本；現行 manifest SHA 再為 `de46aa231b3f4c22633e93b9261fcc0a381051190530ea78b933ace70f74d87f`，無 `moon034` 退圖選用，也無退件圖頁引用。27 張 KEEP 的全部條目及實際選圖檔 SHA 不變，`keyframeProblems` 僅列 **92 張未畫**、其他問題 0。

帳本 SHA `01a0d7c5460a5afa00b208547ae50b0ea35d61311294d930e21a9e29a6cab418` → `7039c93775ece9c2bb073156b21e32b7678f9d6c830326dd867d99b1fa222c6c`，累計 **US$1.0665／79 image／79 judge／0 預約**；只增加一圖一評審 US$0.0135，低於 US$5.30。`STOP` 已恢復，jobs 空。**不再按 R26 紙審直接批量畫 `moon035–039`**；下輪先針對 `moon034` 的成年特徵做書面窄修與另一人獨立核對，再決定單張重試或合適的來源卡。整集 storyboard、網站站主卡與人耳、動畫、Short、成片及 YouTube Studio 連結仍待。
