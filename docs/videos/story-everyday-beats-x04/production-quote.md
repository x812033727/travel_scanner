# X04 Beats｜零付費前製估算與乾跑

`video.json` SHA-256：`77bd76e62f280b16e5dd5f33f72cc0723ddba5176fad76373c3c3335c08c9a39`。2026-10-20 在獨立 X04 worktree 本機執行；本文件只報已跑過的命令，沒有生成或購買媒體。本集累計實花 **US$0.00**，正式全片硬上限 **US$25**，該上限仍須涵蓋圖片重試與評審、語音、配樂、轉錄、複查及稅費。

| 項目 | 本機結果 | 實花 |
| --- | --- | ---: |
| `lint --slug story-everyday-beats-x04` | 0 errors／0 warnings；67 句、54 張插圖、13 張資料卡、14 個回收鉤子；估正文 8.2 分鐘、濃縮開場 00:54；Azure 計費字元估 5,727 | US$0.00 |
| `keyframes --dry-run --takes 3` | MiniMax `image-01` ready，1K；54 張插圖一輪工具估約 US$0.73，三輪最多約 US$2.19；只是圖片請求估算，尚未加其他服務及稅費 | US$0.00 |
| `tts --dry-run` | `STORY_LEXICON_MIGRATION_REQUIRED`，尚未進入任何合成請求；上列字元數來自 lint，**不是** TTS 報價 | US$0.00 |
| `story-lexicon-migrate --json` | 唯讀 refused：`STORY_LEXICON_MIGRATION_WORKDIR_UNPROVEN`，本機沒有已開始的正式 story 工作區，不可 `--apply` | US$0.00 |
| `music --dry-run` | 缺少與現稿綁定的 `timeline.json`；須在 TTS 後以實際長度乾跑 | US$0.00 |

估時只計 `video.json` 正文，**未**把概念 5 秒片頭與 21 秒片尾灌入 8 分鐘門檻。8.2 分鐘是文字模型估值，距最低要求不遠；正式 TTS 後須以量測的旁白時間軸確認至少 8 分鐘。若不足，先補有 SEC 原件支持的新內容並重新做來源及敘事審查，不能靠延長停頓、空鏡或動畫補時。

正式工人工作區與原頻道動畫目前不可用，因此沒有可驗收的旁白、插畫、音樂、SRT、MP4 或 YouTube 可點連結。動畫及連結的具體交接見 [publishing-handoff.md](publishing-handoff.md)。
