# S07 開畫前圖樂上限精算

查核日：2026-10-20。現行 `video.json` SHA-256 `07cf926883aa0d5de6f7758984afe04a4cdb5be42ec3a06f0d6b621c5143467b`，`script.md` SHA-256 `73ace39d6b07a68d59bf077b6bd6e30a565fb5d86baed910d6f774183eb169b2`，`claims.md` SHA-256 `2cf838c667f8c66b1dc117c88ca5be04cfc2b54e33c644e88f36d262f24da62f`。86 張插圖的提示詞於這版經獨立史料／年代預檢通過，見 [`../curio-art-preflight-2026-10-20.md`](../curio-art-preflight-2026-10-20.md)；這不等同生成圖片驗收。

`keyframes --dry-run --takes 2` 報 MiniMax image-01 1K 圖片，一次全畫約 US$1.16、兩次至多 US$2.32；`--takes 3` 報三次至多約 US$3.48。工具按美分顯示，但每次圖片及評審合計精確計價 US$0.0135，因此 **86 × 3 × 0.0135 = US$3.483**。加上已付 Lyria 配樂 US$0.08，最壞情況 **US$3.563**，整集圖樂硬停上限須向上取到 **US$3.57**；US$3.56 少 US$0.003，不能涵蓋全部 258 次嘗試。

`/workspace/.video-work/curio-s07/media/ledger.json` 當下 `totals`：`usd: 0.08`、`music: 1`、`images: 0`、`judge_calls: 0`、`reserved: 0`。配樂檔已產生，實際 MP3 177.633 秒；圖片可用額度上限 US$3.49，無已購圖片。若先用兩次嘗試開畫，仍須按實際帳簿控制補畫，且不超過共享供應商每小時額度。所有選定圖片需全尺寸、史料與年代複核，再進分鏡審核及組片；配樂循環接縫需於成片查聽。
