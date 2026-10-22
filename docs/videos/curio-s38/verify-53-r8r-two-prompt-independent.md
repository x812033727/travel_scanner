# S38 R8r｜PF009／PF013 獨立書面覆核

2026-10-22 UTC。**書面 PASS：只放行 PF009、PF013 各一次有界原生試畫與逐張未裁切原圖驗收。** 這不是兩張圖、第一章或全片的 KEEP。R8q 兩張原生退件圖由我直接打開：PF009 的 1280×720 JPEG 有明顯上下黑寬帶及成熟寫實動畫質感；PF013 背景清楚畫出 1894 年 Tower Bridge 的兩座塔與吊索，不能作 1666 年畫面。

## 固定來源與逐字差分

固定 `/tmp/curio-s38-pepys-4200.txt` SHA-256 是 `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`，與 R8q `verify-50` 一致。日記 1666-09-02 L65795–65819 記載佩皮斯凌晨望火後**回床睡**，早晨去塔上親見橋端房屋起火；Michell 家已燒是他下塔、上船後才確認。PF009 新 prompt 的成年男子在床上拉毯、睡袍及黎明前場景是動作示意，毯色／室內光不冒充逐字史實。PF013 新 prompt 讓成年人物在倫敦塔高台看遠處河邊屋頂火，**不再要求任何橋體**，避免原圖的近代橋誤導；旁白仍交代火在橋端，沒有提早確認某戶損失。原生圖若再畫出 Tower Bridge、錯置年代或重現黑寬帶，仍要退件。

現行 `video.json` SHA-256 `f02fdd2bd769e746b2e76206152492593f66cec1ea48e40a07cd7bf236aaf015`，與 R8r 作者凍結值相同。逐一核對 `scenes[8].data.prompt`／`pf009`、`scenes[12].data.prompt`／`pf013` 的新字串與 `verify-52-r8r-two-prompt-structured-diff.json`；各只出現一次。把且只把兩個新字串在原位替回舊字串，原檔位元組 SHA-256 精確回到 R8q `087ae9c4cdbb8dea3430cd505d42624e06deca0a94b77e71c49164fbbcc2f4db`。所以 R8r 恰只改這兩個 prompt 欄位。`claims.md`、`research.md`、`script.md` SHA-256 依序仍為 `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`、`f838518cf2c4ab23de91021ae6024d9431f907866c14301466ca0a06bb3ecdfe`、`e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`。

已收 PF001–005、PF008、PF010–012、PF014 的十個現行 manifest entries 與私有 `review/r8q-six-post/keyframes--manifest.json` 各自逐項相同；現行完整 manifest 與該備份位元組相同，SHA-256 `ffd0069be9f1b368ffcea76f4b9a94b06eb7d8e1bcbc480c13f70ec90933c8fa`。十張所選圖片的現行檔案 SHA 逐張符合各 manifest entry。R8r 尚未生成新圖時，STOP 在位，私有 ledger 仍為前輪 US$0.5425／35 image／34 judge／1 music，另有舊 PF003 US$0.0035 reservation；整集硬限 US$4.58。

本輪 `lint --json` 回報 0 errors／0 warnings、112 句。`NODE_USE_ENV_PROXY=1 VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs keyframes --slug curio-s38 --shot pf009,pf013 --takes 1 --dry-run` 回報 MiniMax `image-01` ready，兩段 prompt 278／286 字，各一次含評審約 US$0.03。第一次未啟用 Node 環境代理時，Node DNS `EAI_AGAIN`，未發出圖片請求；環境代理啟用後 dry-run 成功。

**執行界線：**在私有 STOP 的 EXIT 恢復邊界中，只用 `--shot pf009,pf013 --takes 1`；執行前備份 manifest／ledger／STOP，執行後核 ledger 增量、manifest 及十張 KEEP 不變、未裁切原圖和裁邊版。若服務／帳本／檔案異常則停止，不繼續 PF015–022 或整集。
