# S42 前製站台大綱送審回條（2026-10-20）

使用官方 `tools/video/cli.mjs`，設定 `VIDEO_WORKDIR=/workspace/.video-work`、`NODE_USE_ENV_PROXY=1`、`NODE_NO_WARNINGS=1`。本集是手動製作，工作目錄沒有 `auto.json`；工具標成 `hand_pushed: true`，站台不會因 Jev 建議而直接核准。

| 步驟 | 精確結果 |
| --- | --- |
| 本地預查 | `status`：brief 存在、script lint 通過、outline 尚未核准；`lint --json`：0 errors／0 warnings，預估 9.635 分鐘。 |
| `review-push --report-only` | 首次及格式修正後各通過一次：`reported to /admin/videos; nothing submitted`。這是站台專案資料回報，不是站主審核。 |
| 第一次 `review-push --gate outline` | 舊 brief SHA `534587fdc0320c4ef630b20ca46087d3ebfbb6ba82b9515eb60f2a040243c89e`；回覆 `brief has 0 options`、`outline submitted for review (pending)`。原因是站台只辨識 `### 選項 A：`／`### 選項 B：`，舊標題未使用該格式。 |
| 修正後的大綱 | 只補兩個選項的站台可辨識標題、一行說明與開場鉤子，既有 A/B 內容與推薦方向未改。`outlineOptions` 本地檢查得到 A、B 各自的標題、摘要與鉤子；新 brief SHA `29beb1e0307a117470445b2aa23a120073e27f101ec6fa2a32dfdb9f58ba4bb7`。 |
| 第二次 `review-push --gate outline` | 站台以新 SHA 覆蓋舊 pending 版本；Jev 建議 A（0.98），工具仍回覆 `outline submitted for review (pending); the owner decides`。 |
| `review-pull --gate outline` | `outline: waiting for the owner`，exit 3。這是待決定，不是通過或失敗。 |

送審後 `script.md` SHA 仍是 `b70b82c4eb73fc997d2eb5e3ca55b1766a66a218d6c4d093406fb789905e284d`、`video.json` `80c7865f09c7c9f64fc21788770f27df1f432ae025d4a2464f382f8db1e47414`、`claims.md` `b25ef409a2c2bfd9e3662d43eb7001e52337464c888759bd32cfafd1b8d745a9`，與兩位 13／13 盲讀及獨立來源／畫面覆核所綁定的版本相符。尚未送 `script` 關卡；先由站主選定大綱，避免 A 案劇本與其選擇不一致。`review-push --gate script` 也會重新產生 `script.md`，屆時須重算雜湊並核對原稿／盲讀證據。

沒有呼叫 `approve`、語音合成、插圖、配樂、組片或上傳。正式組片時才套用已安裝的系列 5 秒片頭及 21 秒片尾；私人片的最後 16 秒留給 YouTube Studio 可點結束畫面，現階段沒有渲染這些動畫。長片及 [Short 草稿](shorts.json)的來源／頻道網址已備好。
