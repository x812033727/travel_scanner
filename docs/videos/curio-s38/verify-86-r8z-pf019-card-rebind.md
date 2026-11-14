# S38 R8z｜PF019 來源卡後的私人圖單重綁

2026-10-22 UTC。PF019 [作者可逆差分](verify-84-r8z-pf019-source-card-structured-diff.json)及[非作者書面審查](verify-85-r8z-pf019-source-card-independent.md) PASS 後，在 `STOP` 存在、jobs 為空且沒有媒體請求的狀態，把私人圖單由 R8y `visual_hash=099da572e40ba916` 重綁至 R8z `7f589efde612587a`。這不是全片分鏡或網站核准。

精確前置斷言：`video.json` SHA-256 `4f30f598c40dcdb9a6cc3d9edd0fa2bb2117d7f455609c4dd4f2730c9f119022`；舊 manifest SHA `112d8b480d189080c7babc59b0fbfacf937cb501858f0ceb9eac42a805848b56`；ledger SHA `74dcfa1eb94fd57f80c6b3faf2688f384001ab05b20ac7329952c62449bcf237`。舊 manifest 已逐位元備份至私人 `rebind-backups/r8y-manifest-before-r8z-pf019-card.json`。只替換圖單版本雜湊，聯絡表原本就為空；PF019 在舊、新圖單均無選圖。

重綁後 manifest SHA-256 `4620087b58255decbb15060b07061a59ea7eab33592ea5e1855b83fcdb4852ba`。先前 11 個人工 KEEP 的完整條目 canonical SHA-256 前後均為 `59cb354fcf4a4d38d746e4fc49e7dd39742d248ce1094d7de4d80a95f8a6e301`；每張選定 JPEG 的 SHA 與圖單相等。[逐張清冊](verify-86-r8z-pf019-card-rebind-inventory.json) SHA `07edc55cde86d3e2612fc7c1d4db094ae4fd121c68e407c5a4999647da9198e4`。ledger 前後同 SHA、US$0.7685／51 image／51 judge／1 music，另有舊 US$0.0035 reservation；STOP 與 jobs 狀態前後不變。

重綁只放行既有獨立紙審下的 PF018 單景首張原生圖；需再查原圖與裁圖，不能以評審分數代替人工內容驗收。
