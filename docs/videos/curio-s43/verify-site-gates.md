# S43 手動大綱關卡回條（2026-10-20）

本站影片工具已使用配對權杖，工作目錄 `VIDEO_WORKDIR=/workspace/.video-work`。這是本機手動前製，`curio-s43` 工作目錄沒有 `auto.json`，送審會標為 `hand_pushed`；Jev 的推薦**不等於站主核准**。

| 步驟 | 逐次結果 |
| --- | --- |
| 固定企劃檔 | `brief.md` SHA-256 `00b591b66f75f90899af6e9dd21ec5e88083c69cb7f27e85f7eec3391c178ec6`；`outlineOptions` 正確讀出 A、B 的標題、一行說明與開場鉤子；`checkBrief(..., "drama", "cute-mystery")` 為空問題清單。 |
| `review-push --report-only` | `reported to /admin/videos; nothing submitted`；只建立／更新站台專案資料。 |
| `review-push --gate outline` | Jev 建議 A（0.92；符合立場 0.87；解說類「有示範」不適用；建議違規 0.01）。同一執行明確回覆本片沒有 `auto.json`，`the owner decides at every gate`，大綱 `submitted for review (pending)`。 |
| `review-pull --gate outline` | `outline: waiting for the owner`，exit 3；尚未取得對此檔案雜湊的站主選案。 |

**下一個依賴：**先由站主在 `/admin/videos` 選定這一集的大綱，`review-pull` 確認對同一 `brief.md` 雜湊的核准後，才可送劇本關卡。即使候選 A 的本地劇本完成盲讀，待決定仍是待決定。本回條未呼叫 `approve`、`review-push --gate script`、TTS、插圖、配樂、組片或上傳。
