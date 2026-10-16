# M09 音訊 QA 的一次 502：未進供應商的證據

日期：2026-10-16（UTC）。範圍只限 `check-audio` 第 21／95 句 `ta55`，本機 speech journal 請求 SHA-256 `80a7eac4f2a5a5b6d09d9d07b088fa3f434e696f56db99d35a151266ed8c4230`。第一次執行留下前 20 句轉寫快取，後 74 句未送；US$0.50 音訊 QA 估算仍留在整批帳本的 `reserved`，不宣稱實際帳單。

## 對時證據

- 本機 `audio/speech-journal/<SHA>.json`：`sent_at=2026-10-16T01:46:28.193Z`、`held_at=2026-10-16T01:46:32.580Z`、`status=held`、`video_speech_uncertain`。原 journal 檔 SHA-256 `50CC5B5799E8D58A8CEB1505E15B725918291C7459E6B1A3254CD4733623B921`。
- 主機 Nginx `/var/log/nginx/error.log` 在 `2026/10/16 01:46:32` 對 `POST /api/video/speech/transcribe` 記錄 `connect() failed (111: Connection refused) while connecting to upstream`，目標為 `http://127.0.0.1:8091/api/video/speech/transcribe`。用戶端位址不抄進此收據。
- 主機部署日誌 `/root/deploy-logs/deploy_20261016_014517.log`（wrapper 同時戳檔 `/root/deploy-logs/wrapper-20261016_014517.log`）顯示部署由 01:45:17 開始，API 與 web 新容器分別至 01:46:47.109、01:46:48.400 才啟動，01:47:11 才通過健康檢查。這筆 01:46:32 的請求在 Nginx 連 web 前已失敗，沒有進入 web/API 或 Gemini，故這一筆不會產生 Gemini 轉寫費用。
- 唯讀恢復確認（主機 UTC 01:58:53）：web `/` 回 307，web `GET /api/video/speech/transcribe` 回 405，API `/health` 回 200，API `GET /api/v1/video/speech/transcribe` 回 405。GET 僅測路由，不呼叫付費轉寫。

## 續跑界線

清除前先把 exact held journal 複製到外部 review 留存並核對 SHA。然後只對上述 request SHA 執行 `node tools/video/tts/speech-journal.mjs forget --dir <M09 audio/speech-journal> --sha <SHA>`；不能 `--force` 重買前 20 句、不能清其他 journal。再以已預留的 US$0.50 估算續跑一次 `check-audio --slug curio-m09`，讀回快取／費用／旗標。若出現新的不明結果，保留新 hold 並重新查證。

## 已執行的單筆恢復

- 已將 held JSON 複製到 `<home>/mokaair-work/videos/curio-m09/review/holds/80a7eac4f2a5a5b6d09d9d07b088fa3f434e696f56db99d35a151266ed8c4230.before-forget.json`；複本與原件 SHA-256 同為 `50CC5B5799E8D58A8CEB1505E15B725918291C7459E6B1A3254CD4733623B921`。
- 對 exact request SHA 執行一次 `speech-journal.mjs forget`，CLI 回報 `forgot ... (held)`；確認原 held JSON 已不存在、複本仍具相同 SHA。其餘 journal 未處理。下一次 `check-audio` 仍須核對快取和完整 95 句結果。

## 續跑結果

- 2026-10-16：在前 20 句快取上續跑，另轉寫 75 句；check-audio 完整讀回 95／95 句、TypeSafe Jev 判讀 1 次。70 句逐字吻合，7 句僅同音字或語助詞差異，4 句 Jev 判可接受，14 句自動旗標待離線複核。CLI 因品質旗標結束碼 1，不等同供應商失敗。
- 共用帳本 m09-audio-qa-20261016-01 由 US$0.50 預留改為保守估額結算；工具回傳呼叫數，尚無供應商最終美元帳單。後台旁白審核尚未提交或核准；不得啟動 M09 插畫。
