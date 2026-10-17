# H11 英／日／韓專用縮圖補件

2026-10-17。站主指出 H11 缺少語言專用縮圖。本機原四語上傳包有繁中主縮圖，卻沒有 `thumbnails/en.jpg`、`ja.jpg`、`ko.jpg`；三語文稿的 `thumbnail` 翻譯與來源雜湊均為 current。既有私人 YouTube 影片的主縮圖在後台同步紀錄為已設定，但這筆 API 回執不證明 Studio 畫面或觀眾端實際顯示。

只縮短三語 `i18n/<locale>.json` 的 `thumbnail.headline` 以配合既有版型：英文「UNREAD / HOW OLD?」、日文「未解読 / 年代は？」、韓文「못 읽어도 / 뭘 알까?」。題意仍指未解讀手稿與可查的證據；片名、說明、字幕、台詞、來源及畫面不變。執行 `render --slug curio-h11 --thumbnails-only`，最終 3／3 生成；此模式保留原卡片、繁中主縮圖與成片。

| 檔案（相對於工作媒體目錄） | 大小 | SHA-256 |
| --- | ---: | --- |
| `thumbnails/en.jpg` | 89,412 B | `951EECD6EB2CC6FAC136092876251428CD009C764837328477C2AFF264B71C42` |
| `thumbnails/ja.jpg` | 92,011 B | `35A8CD051A3FCC0DADC40A63A5C0B54A8246D9F82F732B2948E68513E3B53DD9` |
| `thumbnails/ko.jpg` | 88,657 B | `87B2E17AB429F0A3C53E6E374D3EB158B0D778F0ADE3E32D5B646A314A036851` |

三張均為 1280×720 JPEG、低於 2 MB；逐張目視無錯字、缺字、截斷或背景錯配。`review/thumbnail-en-320x180-v2-20261017.jpg`、`thumbnail-ja-320x180-20261017.jpg`、`thumbnail-ko-320x180-20261017.jpg` 的手機寬預覽均可讀主標。英文舊預覽 `thumbnail-en-320x180-20261017.jpg` 僅供修訂前比較，勿上傳。

驗證：`lint --slug curio-h11` 0 error／0 warning；`package --slug curio-h11` 4／4。新的 `upload/` 包含三張語言縮圖，三張與來源檔 SHA 相同；`upload/metadata.json` SHA-256 `301E34A22EEF16AF3EE38906FD448CAC059795D4F9ED54BA0FCB1D8AD50D2192`，`thumbnails` 列出 en／ja／ko，`skipped_thumbnail_locales` 為空。繁中 `thumbnail.jpg` SHA-256 仍是 `68D71A7067064F8AAAE2EAD9D28EB9DBDC94DACC59D5EF6142D62A0AF46398EE`；已核准 `final.mp4` SHA-256 仍是 `54EFA17859D4359B84A9266799108B3C0DE0597DDFAAA2F1B4B3F556801FF1BC`。本次無付費呼叫、重錄或重新合成。

新包已送後台，最新 `publish` 卡 `8be04d82-9f4a-43f0-b177-c082dbb7ff65`／SHA `301E34A22EEF16AF3EE38906FD448CAC059795D4F9ED54BA0FCB1D8AD50D2192`；最新 `languages` 卡 `cd3f9fe3-7f02-4df2-98e8-c928d9bd1b49`／SHA `CA1BE987B9EEC6B31C1270B4DAC132B4D59467D5C2D2375AD9A5E946E032E2FE`。原核准卡保留歷史。既有私人 YouTube 影片 ID `9Gn00ib57OA` 及三語配音的 uploaded 狀態未改。至該影片 Studio「語言」頁，分別點 en、ja、ko 的語言名稱，在「縮圖」按新增，上傳 `upload/thumbnails/en.jpg`、`upload/thumbnails/ja.jpg`、`upload/thumbnails/ko.jpg` 各自對應的檔案，按「更新」；重新整理後切換三語實際查看。這一步未由代理執行，也未排程或發布。

2026-10-17 03:14 UTC，站主回覆「OK」後，唯讀後台列確認上述兩張最新卡分別在 03:14:19／03:14:16 UTC 核准。`review-pull --gate publish` 與 `--gate languages` 將這兩份相同 SHA 的核准寫入本機 `approvals.json`。命令同時列出「approved a version that has since changed」的舊版核准提示；最新 `metadata.json` 本機 SHA 已再次核對為 `301E34A2…D2192`，最新兩筆核准均在 `approvals.json`。這只是上傳包與語言包核准，尚未證明 Studio 的三張語言縮圖已上傳或可見。

2026-10-17 03:27 UTC，站主依 H11 Studio 語言頁的逐語上傳與重新整理指引回覆「三語縮圖都已顯示」。這是站主對英／日／韓縮圖在 Studio 顯示的目視確認；代理未登入 Studio 獨立截圖，也未核對觀眾端縮圖、公開狀態或排程。同期本機重核 `upload/thumbnails/en.jpg`、`ja.jpg`、`ko.jpg` SHA-256 分別為 `951EECD6…B71C42`、`35A8CD05…13E3B53DD9`、`87B2E17A…A036851`，與上表一致；`upload/metadata.json` 仍為已核准的 `301E34A2…D2192`，`upload/final.mp4` 仍為 `54EFA178…801FF1BC`。`approvals.json` 保留最新 `publish` SHA `301E34A2…D2192` 與 `languages` SHA `CA1BE987…2FE` 的核准讀回。此回覆關閉「H11 語言縮圖未顯示」問題，不代表影片已公開或全部 YouTube 播放路徑再次驗收。
