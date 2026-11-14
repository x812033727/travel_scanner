# S38 R8ac｜PF020 重試前私人圖單安全重綁

2026-10-22 UTC。[非作者 PF020 提示詞紙審](verify-100-r8ac-pf020-prompt-independent.md) PASS 後，在 STOP 在位、jobs 空、ledger 不變的狀態，只把私人 active manifest 從 R8ab `visual_hash=7f7b8b8dda0faefa` 重綁至 R8ac `799a46f1c5720fec`。**沒有付費媒體請求；此步不是新圖驗收。**新 `video.json` SHA-256 `d8d169a010a7ffce93b3aec580e7c9580dc3a5393ffbe0bbc5909b72e8559688`，`look_hash=98a370ae40badbaf` 不變。

前置精確雜湊：active manifest `f666bcc1d7afe4b7e40215cb373ccf29d2a9ee8d262606c24026ee98b3914c74`、ledger `6696edf9ed0f77aa1b4f8e475f37f8121fe51cf997d65414327cbc086fcab14c`；舊 manifest 原檔按位元備份在私人 `rebind-backups/r8ac-manifest-before-pf020-retry.json`。新 active manifest SHA-256 `66b30497f3b1f7af4757716ce9d81a59f972fb3bcf5b14c8ee7086981fcc2877`。兩版 JSON 除 `visual_hash` 外完全相同；12 張原有 KEEP 的完整條目 canonical SHA 前後都是 `a2c22b903adfcca2127f264b36c83280c4a7faa840bbd7bb16f6cdc0dec040e0`，每張選用 JPEG SHA 實算吻合。[備份與重綁清冊](verify-101-r8ac-pf020-rebind-inventory.json) SHA `4413b033f835d4617e4f1a3562908ca3d11b2fbad3cadb0fe03942f94415d5c4`。

ledger 同 SHA，仍是 US$0.8225／55 image／55 judge／1 music，加舊 US$0.0035 reservation；整集硬上限 US$4.58。STOP 與空 jobs 前後不變。重綁後嘗試只讀 `media-status` 和 `keyframes --shot pf020 --takes 1 --dry-run`，兩者都因 `cannot reach https://mokaair.com: fetch failed` 以 exit 4 結束；**沒有 live 就緒證據，尚未解鎖任何付費重試**。服務恢復後重新核對 STOP／jobs、12 KEEP、圖單／帳本、單景 prompt budget、live image model 和整集費用，再只試 PF020 一張及一次 judge，逐張查看原始 1280×720。PF021／PF022 仍不在這次放行範圍。

後續診斷確認此雲端容器的 Node fetch 未自動使用既有代理：同時的 `curl` 可達站台，而 Node CLI `fetch failed`。僅在該次 CLI 前設 `NODE_USE_ENV_PROXY=1` 後，live `media-status` 顯示 MiniMax `image-01` ready、images 19962／30000、judge 21544／30000；單景 dry-run 通過，PF020 prompt **322／1072 字**，單張含評審約 US$0.0135，帳本連 reservation 的預估為 US$0.8395，低於 US$4.58。隨後才以完整精確雜湊與 STOP trap 另執行[受控單張](verify-102-r8ac-pf020-seed2-keep.md)；此重綁本身仍沒有購圖。
