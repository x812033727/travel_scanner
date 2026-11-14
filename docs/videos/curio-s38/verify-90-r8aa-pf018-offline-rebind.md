# S38 R8aa｜PF018 單景重試前圖單離線重綁

2026-10-22 UTC。PF018 [作者窄修](verify-88-r8aa-pf018-prompt-author.md)及[非作者書面紙審](verify-89-r8aa-pf018-independent-paper.md) PASS 後，在 STOP 在位、jobs 空時只把私人 manifest 從 R8z `visual_hash=7f589efde612587a` 綁到 R8aa `819c6ff2d7c16ad0`。未呼叫任何媒體服務；這不是 PF018 新原圖或完整 storyboard 驗收。

前置檢查：R8aa `video.json` SHA-256 `e25b7163f2efa7f830c0b94e421511ceaa4662fb985b53d2290e3a715a16556b`，舊 manifest `a7c5920fd1e4c96b66bb7d9331541c36683987999617279bca9a75c21197c48d`，ledger `a753f6ef1831579858e439305677e3c4a8599b35141b9136e37099fe84d772c0`，11 個 KEEP 條目 canonical SHA `59cb354fcf4a4d38d746e4fc49e7dd39742d248ce1094d7de4d80a95f8a6e301`，逐張選圖檔 SHA 一致。舊 manifest 原樣備份至私人 `rebind-backups/r8z-manifest-before-r8aa-pf018-retry.json`。先前人工退件的 PF018 原圖及裁邊圖先原樣備份至私人 `rebind-backups/r8z-pf018-seed1-rejected/`，避免新 seed 1 同名覆寫舊證據。

新 manifest SHA-256 `d36e5c41f21f67d38b1b325b5fdaf0d1473a1d0a232273185f1c867b1c8fb548`，只有圖單版本雜湊不同；11 個 KEEP 的完整條目仍同一 canonical SHA，PF018 無入選條目，聯絡表為空。[逐張與備份清冊](verify-90-r8aa-pf018-offline-rebind-inventory.json) SHA-256 `8ccb91b62c9491eb8c507df8e273ec5709666095a69a2da92d8a90815f3da8ba`。ledger 未變，US$0.7820／52 image／52 judge／1 music，另有舊 US$0.0035 reservation；STOP 與空 jobs 未變。

先前 PF018 實際原圖已有一張。此重綁後最多試第二張實際原圖及一次 judge，須立即看未裁切原圖的成年人物、木箱入船、船型與年代；若不合格就停線，不續買 PF020–022。
