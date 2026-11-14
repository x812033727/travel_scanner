# S38 R8n｜`pf003` 同章插圖沿用非作者獨立覆核

2026-10-21 UTC。**來源／書面畫面 PASS；PF001 圖像重用方案 PASS。**此結論只適用於 R8n `video.json` SHA-256 **`df05f4a886abfe18018a85db948623cfe96537940c5ed7cf1f71461752bb1e35`**，不是整集插圖、PF003 新 judge、網站審核或成片 PASS。本輪只讀檔、看既有原生 JPEG；未改創作檔、私有媒體與帳本，未清 `STOP` 或呼叫付費工具。

## 凍結版本與差分

我核對[作者回條](verify-35-r8n-pf003-reuse-author.md)及[結構化差分](verify-35-r8n-structured-diff.json)：目前檔 SHA-256 為上列值；在 `pf003` 區塊將兩個新字串精確換回舊值，原始位元組 SHA-256 為 R8m **`980c371a793bfe3f4d2772d6d002309026a8cbd8874187ab8cd1d8fdeba82065`**。遞迴 JSON 差分恰為 **`scenes[2].data.prompt`、`scenes[2].data.camera`** 兩葉，值及 scene ID 全與差分檔相符。R8n 的 `pf003` prompt／camera 分別**逐字等於 `pf001`**，兩者 camera 均 `push in`；其共同 `look: {"preset":"cute-mystery"}`、cast（空）、style references（空）、合成 prompt 亦相等。所有旁白、台詞 ID／章節、其餘景、R8m `pf005` 的 `pause_after_ms: 1600` 及 `pf007` 日記譯文 `big` 卡均與 R8m 相同。

`brief.md`／`research.md`／`claims.md`／`script.md` 的 SHA-256 仍依序是 `fa297d70e016d88ba1a59bd92476be22eda3eefc09f36b2d08c0c82ab114643b`、`f838518cf2c4ab23de91021ae6024d9431f907866c14301466ca0a06bb3ecdfe`、`f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`、`e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`，與[R8m 非作者回條](verify-34-r8m-independent.md)一致。現行 `visualHash=721f73508d3d3870`、`speechHash=92a6e6ad374ae77e`、`lookHash=98a370ae40badbaf`；`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s38 --json` 實測 **0 errors／0 warnings**。

## 圖像與來源

直接打開 1280×720 原生 `pf001-1.jpg`，SHA-256 **`608203b99cd453ad7218d8c773c93ca92900997d2a9a73a1be44090cba60ccb0`**：兩名成年模樣的男子持完整長柄鏟，在院中打開的土坑兩側挖土，畫面沒有虛構火勢距離或可讀字。人物頭臉入鏡，與 `pf001` prompt 要求的腰以下構圖不全相合；原 judge 已把此列為 `details=7`，整體 **9.29／10、`passed=true`、`needs_review=false`**。這項取景偏差不改土坑行動，也不構成與旁白／來源的具體矛盾。

`pf001` 旁白說 1666 年 9 月 4 日傍晚佩皮斯與 Sir W. Pen 挖第二坑；`pf002` 切到酒及起司放進坑；`pf003` 問「火追到什麼程度，才讓他選擇院子裡的泥土？」重回兩人挖坑畫面，承接選擇泥土的結果，但**不預先回答**火實際燒到何處。固定 [Pepys 日記 9 月 4 日 L65990–66009](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65990-L66009)直接記 Batten 先挖一坑、傍晚 Pepys 與 Pen「did dig another」並放酒與起司；本地全文 SHA-256 `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`。此已收插圖對 PF003 問句有內容關聯，未畫成第一坑或斷言起司確因某個明定火勢距離而埋。

## 私有快取、舊預約及停點

依工具 `composeShotPrompt`、`Stage.imageKey`、`keyframeKey` 的唯讀重算，以同一 MiniMax `image-01`、1K 記鍵尺寸 1920×1080、seed 1、空 negative／references，PF001 與 PF003 的新**圖像 request key 同為 `5127634d8744a445`**；scene ID 不在該 key。`media/cache.json` 此鍵指 `keyframes/pf001-1.jpg`，所記 SHA-256 與現存檔實算相同，且 PF001 manifest 選定的 key／SHA 亦相同。以目前模型、尺寸和未加修詞的 seed 1 條件，該圖片可預期命中本地快取；這是**圖片**重用，不是預先免費承諾。PF003 沒有既有 manifest 景目；judge 問題 context 含 `shot.id=pf003`，PF001 舊 judge stamp 不直接屬於 PF003，新判定可能另計費且須檢視結果。

PF003 舊 ledger 另有 **`key=3a06e8acfb085b26`、US$0.0035、`status=reserved`** 的原請求，沒有 `job_id`、沒有收到圖；`media/jobs.json` 的 `jobs` 為空。這個舊鍵不同於新快取鍵，不能把舊預約說成已完成，也不能藉本次沿用自動清帳。整體 ledger 實讀 **US$0.3300（含 US$0.0035 reserved）、20 image、18 judge、1 music、1 reservation**；原整集硬上限 **US$4.58** 不變。`STOP` 檔存在，私有 manifest 尚綁 R8l `visual_hash=859769ddb7cef27f`，僅有五景舊目且沒有 PF003；舊 `pf007` 圖仍是人工退件，不能因新版卡片而沿用。

**下一關：**保留 `STOP` 與舊預約紀錄，在明確的製作控制下只針對 PF003 驗證快取圖及新的 judge，逐張看實際內容與帳本；不重送舊 `3a06e8acfb085b26` 請求或把 PF001 judge PASS 當成 PF003 judge PASS。R8m 開場實測 30.20 秒仍待正式混音聽感、整集圖片、網站音訊／分鏡審核及成片 QA，故 S38 交付仍 HOLD。
