# S53 R36｜成年屋外驗框稿後 18 KEEP 圖單安全離線回綁

2026-10-22 UTC。[R36 不同作者史料／書面畫面紙審](r36-s53029-adult-exterior-doorway-independent-paper.md) **PASS**，SHA `20f3d8bd063b16df68c661eef41f71581e3e8262e351c516a5dc729af04aea25`。本步只在私有工作區 `STOP` 在位、jobs 空時把正式 manifest 的 `visual_hash` 從 R35 `76b75a45d888af0b` 改為 R36 `7a88c3a7a90cc951`；沒有購媒體或選入 R35 第一張退件圖。

先逐檔核 R36 `video.json` SHA `601b54f492cb38ddf046f200f6bb02097868e25b9217605d2661abc33c1aa49e`、`claims.md` SHA `0795312a9584486511f8695faeee7dda73863fd5ca64f705da99da5ccba6a745`、`script.md` SHA `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc`、可逆差分 SHA `0659203b3466efb8a0fec54eb8c1291a24030c215e60d7c48a08a09027e9f02d`、固定 Survey 原檔 SHA `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`。舊正式 manifest SHA `051f6055af0209948d665b095b1201ef37967c5c34c74cb2c3213292909dec59`，18 筆 KEEP 所選實檔 SHA 全對，沒有 `s53029`；獨占備份到私人 `rebind-backups/r35-manifest-before-r36-adult-doorway.json`，同 SHA。

只改 `visual_hash`，canonical JSON 寫暫存、fsync 後原子取代。新正式 manifest SHA **`deae00309dd2e438ad4f20252f6a8e3178432f15a6fb967350aeba0db27142a7`**，18 筆完整條目、request key、所選 SHA 前後逐項相同。contact SHA `0c1694a9150059b8656f778562ecaf925b3a4827d88b919d40464912abb0f930` 不動；`keyframeProblems` 的 94 筆僅對應 94 個未畫 `shot`，既收 18 張 **0 問題**，`s53010/s53018/s53028` 仍為卡。ledger SHA `fb92ccb3157efcb91b384f86a3f03d0d184a0e6b8a6b956cbbaced369b694878`、**US$0.6480／49 image／48 judge／0 預約**不變，低於使用者 US$4.78 上限；jobs SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3` 且空，`STOP` 在位。

後續只可在新一輪正確父工作目錄、image-01 即時額度、固定來源、18 KEEP／退件證據及上限預檢全部通過後，對 `s53029` 購**第二張實際原生圖**及一 judge，直接看未裁原尺寸與所選裁圖；若退件即停，不跳 `s53030`。本離線回綁本身不驗收任何新圖。
