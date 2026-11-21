# S60 R4｜Sulafat 語音上游 429 暫停回條

2026-10-22 01:38–01:39 UTC。這份回條只記錄服務狀態，不是音檔、聽審或成片驗收。

- 凍結版本：`video.json` SHA-256 `c0a474072ffa37604dfe2acb9a46f600cac37c9815da5b4b692e213f560fd8ac`；`script.md` SHA-256 `f09ce432bfdec71135e44bc9ed3ad6f48119e95e01b2acd318fda13f8bda9dd1`。本次沒有改動稿、畫面或聲音設定。
- 工作目錄 `/workspace/.video-work/curio-s60` 的雜湊綁定 outline/script 選擇仍有效；這記錄使用者已授權的推薦選擇，不代表使用者聽過旁白。`tts --dry-run` 回 109 請求、2439 計費字元，網站報 Gemini 當月餘額 7,889,326 字元、Sulafat 可用。
- 在前次約 01:32 UTC 的五次同類拒絕之後，間隔約六分鐘做**一次**正式 `tts` 重試。網站連續五次回 HTTP 429、`video_speech_upstream_busy`、`Retry-After: 10`；CLI 依回覆重試後以 exit 4 停止。檢查工作目錄只有 `approvals.json`，沒有 WAV、`timeline.json` 或旁白可用檔。這些 429 是服務先拒絕的請求；本次沒有可確認的語音費用。
- `curio-episode` skill 記載這個錯誤可能是暫時忙碌或網站 Gemini 金鑰的當日額度；當日額度在十月的太平洋午夜，即約 **07:00 UTC** 重置。不能僅憑 429 判定哪一種。下一次有意義的恢復點是 07:05 UTC 之後，再先查 dry-run 和回覆；避免在重置前手動連續重送。
- Azure 備援已設定，但本系列選定 Gemini Sulafat 的頻道聲音，且 `speechHash` 明確包含 `doc.voice`。換供應商／聲音會改變腳本關卡的 `script_hash`、使既有精確綁定的敘事回條失效，並需要對新聲音重新聽審；此處沒有逕改聲音或宣稱其等價。

下一步：07:05 UTC 後在相同凍結雜湊重試 `tts --slug curio-s60`；成功後跑 `check-audio`，逐句處理旗標並送聽審。音訊尚未通過前，先不啟動整集插圖、配樂或合片。
