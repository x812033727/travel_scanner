# S43 手動大綱關卡回條（2026-10-20）

本站影片工具已使用配對權杖，工作目錄 `VIDEO_WORKDIR=/workspace/.video-work`。這是本機手動前製，`curio-s43` 工作目錄沒有 `auto.json`，送審會標為 `hand_pushed`；Jev 的推薦**不等於站主核准**。

| 步驟 | 逐次結果 |
| --- | --- |
| 固定企劃檔 | `brief.md` SHA-256 `00b591b66f75f90899af6e9dd21ec5e88083c69cb7f27e85f7eec3391c178ec6`；`outlineOptions` 正確讀出 A、B 的標題、一行說明與開場鉤子；`checkBrief(..., "drama", "cute-mystery")` 為空問題清單。 |
| `review-push --report-only` | `reported to /admin/videos; nothing submitted`；只建立／更新站台專案資料。 |
| `review-push --gate outline` | Jev 建議 A（0.92；符合立場 0.87；解說類「有示範」不適用；建議違規 0.01）。同一執行明確回覆本片沒有 `auto.json`，`the owner decides at every gate`，大綱 `submitted for review (pending)`。 |
| `review-pull --gate outline` | `outline: waiting for the owner`，exit 3；尚未取得對此檔案雜湊的站主選案。 |

**下一個依賴：**先由站主在 `/admin/videos` 選定這一集的大綱，`review-pull` 確認對同一 `brief.md` 雜湊的核准後，才可送劇本關卡。即使候選 A 的本地劇本完成盲讀，待決定仍是待決定。本回條未呼叫 `approve`、`review-push --gate script`、TTS、插圖、配樂、組片或上傳。

## 後續實際選案（2026-10-20）

上述是送審當下的歷史狀態。站主後來在 `/admin/videos` **選擇 A 案**；本機 `/workspace/.video-work/curio-s43/approvals.json` 記錄 `gate=outline`、同一 `brief.md` SHA-256 `00b591b66f75f90899af6e9dd21ec5e88083c69cb7f27e85f7eec3391c178ec6`、`approved_at=2026-10-20T10:36:26.994Z`，備註指向站台 09:43:02.220891Z 的 A 案選擇。再次執行 `review-pull --gate outline` 回覆 `outline: already recorded`（exit 0），`status` 顯示 `outline approved`。新劇本的來源和盲讀仍在覆核；這份大綱選案沒有代替劇本、語音或成片核准，也沒有媒體費用。

## R3 改採企劃 B：目前僅本機選案，尚未重送站台（2026-10-20）

兩輪 A 倒敘劇本各經兩位獨立讀者判 FAIL，尤其開場問未收錄的船長原信全文卻無法回收；詳細題目與精確雜湊見 [verify-1.md](verify-1.md)。為修正敘事，R3 採原企劃的 **B：從邀請信順講**。這是依使用者已授權採編輯推薦方向所做的**本機代理選案**，不是站主在 `/admin/videos` 對 B 的選擇。站台唯一實際 outline approval 仍是舊 `brief.md` SHA `00b591b6…` 的 **A**；`review-pull` 若顯示 `outline approved`，也僅能解讀為該版 A 已批准。

R3 的兩位新盲讀及獨立來源／文字畫面審核尚在排隊。下一節記錄後來實際提交的 B 大綱；在 B 的 exact brief 獲站台選案前不提交劇本關卡，更不合成語音、購圖或組片。

## B 新版企劃已真實送站台，結果待站主決定（2026-10-20）

將 `brief.md` 的 B 標為推薦並把方案表調成順時序走法後，固定檔案 SHA-256 為 `d590fc04c78c754f9c1c024ce43a4666ecb5aecbd9443e4622d90e6233ccf87f`；解析器讀出 A、B 兩個選項，`checkBrief(..., "drama", "cute-mystery")` 回空問題清單。以 `NODE_USE_ENV_PROXY=1 VIDEO_WORKDIR=/workspace/.video-work` 執行 `review-push --gate outline`：Jev **推薦 B（1.00；符合立場 0.86；建議 0.01）**，工具同時明確指出本片沒有 `auto.json`，仍由站主逐關決定；回覆 `outline submitted for review (pending)`。接著 `review-pull --gate outline` 回覆舊 A approval 對此新版已失效、`waiting for the owner`，exit 3。這是**站台 B pending，不是站台 B approved**；沒有劇本關卡或付費媒體。

2026-10-20 R7 前製核對：`review-pull --gate outline` 再次回覆「approved a version that has since changed；waiting for the owner」（exit 3），對應 B `brief.md` SHA `d590fc04…` 仍無站台選案。`review-pull --gate script` 未取得任何核准，`status` 仍顯示 `script approved: not approved yet`。R6/R7 的本地敘事與政策回條只屬前製，**未**執行 `review-push --gate script`，也沒有把舊 A 選案移用到 B。網站對手動推送影片不自動核准；本地代理的版本決策須另記而不能冒稱站台選案。

2026-10-20 R8 前製核對：兩名新讀者共同退回 R7 敘事後，現行 R8 雜湊見 `verify-1.md`。本輪**未**呼叫任何站台審核或付費工具；B 大綱仍以最近一次 `review-pull` 的 `hand_pushed pending` 為準，劇本沒有站台核准。本地 R8 亦尚未作代理選案／劇本核准，須先等兩位新讀者、獨立來源／文字畫面與新政策判讀。
