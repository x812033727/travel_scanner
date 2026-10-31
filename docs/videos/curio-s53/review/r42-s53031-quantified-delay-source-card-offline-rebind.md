# S53 R42｜兩三個月來源卡紙審後離線圖單回綁

2026-10-22 UTC。[不同作者 R42 來源／版面紙審](r42-s53031-quantified-delay-source-card-independent-paper.md) **PASS**，收據 SHA-256 `389cda0d2d4c4b1ec3d86048b2fbb9bb438b4f7c9b18868e984daf9841b1e6f3`。本步只在私人 `STOP` 在位、jobs `{}` 下，把正式 keyframe manifest 唯一 `visual_hash` 從 R41 `cfbe5fb638b9afd6` 離線改成 R42 `bc739bdaed3b717a`；沒有呼叫付費插圖或 judge。

回綁前重核 `video.json` SHA `81d681b05d12d766e6fcf70d6c60ee78a0dace86d55e93d3401b1ab8c7528ab2`、`claims.md` SHA `eac14636b9762c539950a5c664387cd91a6512da3fcadbd2944341fdd45ee7cf`、R42 紙審、私人 STOP／jobs、正式 19-KEEP manifest SHA `4cfd50a126d5d4f65c4fba6daf1bd8c9e04ecc209aed241a20cf4266d22d4011`。19 個條目皆 `judge.passed=true`、`needs_review=false`，所選 19 個 JPEG 實檔 SHA 全對；`s53031` 與尚未開畫的 `s53049` 都不在有效圖單。舊 manifest 以獨占建立方式私人備份於 `rebind-backups/r41-manifest-before-r42-delay-card.json`，SHA 與舊正式檔相同。

僅替換 canonical JSON 中唯一視覺雜湊字串，等長原子寫入並回讀。新 manifest SHA-256 **`3046213a5cce33e4178fd3d92a5d5f9bf319a4ce3cdeff228c0a797669f7e698`**；除 `visual_hash` 外位元組完全相同，**19 個 KEEP 完整條目及實檔 SHA 不變**。正式 `keyframeProblems` 核對：19 個已收鏡頭無問題，110 個插圖鏡頭中仍有 91 個待圖，沒有其他問題。`speechHash=05c4d9a79a8708b4` 未變；lint exit 0、0 errors／0 warnings。contact sheet SHA `1b58f6e22f6cd20dd339bc8a022cf2ca4546937f5c0c2b49b1021efd83c64483`、ledger SHA `ce2d97f156a1d7d3b0079a8f1e790374013e21ea9a15bc33e4cf436fad1fec89`（US$0.7155／54 images／53 judges／0 reservations）、jobs SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3` 和 STOP 全不變。

`s53031` 現由正式來源卡承載，不購第二張插圖；下一景 `s53032` 仍須獨立核固定分配史料、提示詞及 claims，再做即時配額／US$4.78 上限及單景 dry-run。此回綁不等於下一景已准付費，也不代表長片、短片或 Studio 連結完成。
