# H11 繁中基礎上傳包收據

日期：2026-10-16（Asia/Taipei）。站主已在 `/admin/videos` 核准繁中成片；`review-pull --gate final` 現場讀回 `final: approval recorded`。此收據只涵蓋目前的繁中基礎包，語言面板 `decided_at: null`，尚未代表站主選擇只出繁中或任何外語部件。

`package --slug curio-h11` exit 0，檢查 **4／4**：成片檔與已核准最終雜湊一致、繁中說明欄、繁中字幕、合成內容揭露。`upload/` 目前有 `final.mp4`、`thumbnail.jpg`、`metadata.json`、`description.zh-TW.txt`、`captions/zh-TW.srt`、`UPLOAD.md`；沒有外語文稿、字幕或配音。

| `<home>/mokaair-work/videos/curio-h11/upload/` 檔案 | SHA-256 |
| --- | --- |
| `final.mp4` | `060B86C335008868EA93CC1977417A64EBE0A63D7F2994762671D7BBF27D3A15` |
| `thumbnail.jpg` | `68D71A7067064F8AAAE2EAD9D28EB9DBDC94DACC59D5EF6142D62A0AF46398EE` |
| `metadata.json` | `B297BCAD35B6957E5A20DA9F4F4CABA368AB60BB2880DFAC07D2C1F3AF4A0AF6` |
| `captions/zh-TW.srt` | `17A4BA0D7993D20501120C5A5AE6571CABBFFD8A95BCFF0C9219D8D02DA92A62` |

`review-push --gate publish` 已送出；隨即 `review-pull --gate publish` 讀回 **waiting for the owner**。站主回覆有意加做語言，但後台尚未保存語種與部件；讀回 `languages.json` 仍為 `{"locales":{},"decided_at":null}`。選擇更新後需按實際勾選製作、重跑 `package` 並核對新雜湊。未上傳 YouTube、未排程或公開。
