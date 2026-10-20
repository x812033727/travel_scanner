# X02 達美樂｜本機概念試片交付

本機試片已輸出至 `/workspace/brand-story-preview/dominos-x02/`；二進位媒體不進 Git。此檔是**未核准概念版**，`preview-review-needed.json` 明列 14 張仍為 `needs_review` 的插畫及影片、字幕、劇本、時間軸、選圖、字卡、配樂的 SHA-256。三句旁白仍待人耳確認，見 [音訊修訂](reviews/audio-revision.md)；逐鏡缺陷見 [視覺 QA](reviews/visual-qc.md)。

| 交付檔 | SHA-256 |
| --- | --- |
| `preview-review-needed.mp4` | `ba430870cad347ccdc6275d21dc6a9cf2c52c8ae433f81b4ffd5a3eec1f4452d` |
| `preview-review-needed.zh-TW.srt` | `a954357982666723ea005866071cc264ccbb2816d6fc20e80e8b084060816b00` |
| `preview-review-needed.zh-TW.vtt` | `35a65128bea1ee757958894dba19e706417c1a6e5baa3f8c09932b92b3b0a012` |
| `preview-review-needed.json` | `8c054bf599a8aefecdbd05e574d4a6d27c740d36fa50b98065c9d5c756162567` |
| `thumbnail.jpg` | `a36b0785280c387f7d7016a443524c65435da90371ebe8c847c0ef90cb3aff57` |

另附三頁插畫接觸表 `contact-sheet-01..03.jpg` 及資訊卡總覽 `contact-sheet.png`，可先快速看整體分鏡。影片為 **9:05.43／16,363 影格**，其中 50.53 秒濃縮開場後插入 5 秒**概念**片頭，8:39.43 的正文結束後接 21 秒**概念**片尾。全片 1920×1080／30 fps、H.264 High／BT.709、48 kHz 雙聲道 AAC；完整影像與音訊解碼、連續影格時間戳、−14.0 LUFS／−1.0 dBTP、95 則繁中字幕逐位元組對稿均通過，詳見 [QA 紀錄](reviews/local-preview-qa.md)。

在此工作樹可重跑唯讀驗證：

```bash
node docs/videos/story-everyday-dominos-pizza-x02/reviews/local-preview-qa-check.mjs --workdir /workspace/.brand-video-workdir
```

若需重建概念版，先確定來源雜湊及成本仍符合 [製作紀錄](production-quote.md)，再執行：

```bash
node docs/videos/story-everyday-dominos-pizza-x02/local-preview.mjs --workdir /workspace/.brand-video-workdir --allow-review-needed --force
```

嚴格模式不加 `--allow-review-needed` 會因 14 張待審插圖拒絕。正式成片仍需解決這 14 鏡、人工複聽 3 句旁白、替換站主選定的 5 秒與 21 秒品牌動畫，並重做成片 QA。片尾框線不具可點連結；私人上傳後須在 YouTube Studio 設置最後 17 秒的兩個影片元素與訂閱元素，實際點擊驗證，才能填寫正式影片網址。詳細章節與來源口徑見 [上架交接](publishing-handoff.md)。
