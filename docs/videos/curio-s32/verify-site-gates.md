# Curio S32 R3｜站台送審回條

2026-10-20 約 07:20 UTC，使用官方 `tools/video/cli.mjs`，設定 `VIDEO_WORKDIR=/workspace/.video-work`。這是人工送審影片，工作目錄沒有 `auto.json`；工具送出的卡帶 `hand_pushed: true`，站台沒有在抵達時自動核准。

| 關卡 | 綁定檔案 SHA-256 | `review-push --gate` 回覆 | 緊接 `review-pull --gate` 回覆 |
| --- | --- | --- | --- |
| outline | `brief.md`：`8445f3277c38e8712cde24481445e1e9f0e8a199c096c220c55d164d190eab82` | `outline submitted for review (pending)`；Jev 建議 A，分數 0.98 | `outline: waiting for the owner`（exit 3） |
| script | `script.md`：`d1c91eb102319d8ec78a92e1faa8c8b3f3596e9ba8132815b2d26212b45a6731` | `script submitted for review (pending)` | `script: waiting for the owner`（exit 3） |

送審與讀回後四份前製檔雜湊維持不變：`video.json` `1e85570c510b1f14a69f0c1f7791decffc9356622071d157eef1efcbd71f251d`、`claims.md` `9532776025ac622a31a2ba033f8198eff1be230fcc757445f0f6010ab39ce53b`，`brief.md`、`script.md` 如表。沒有呼叫 `approve`、語音合成、插圖或配樂。下個製作階段須先以 `review-pull` 取得這兩個精確版本的站主決定。

R3 劇本獨立盲讀與重讀分別見 [`verify-blind-d-r3.md`](verify-blind-d-r3.md) 和 [`verify-recheck-c-r3.md`)；兩份均以表中的 `script.md` SHA 給出 13／13。後者先前看過舊稿，因此明確標示為重讀，不冒充新鮮盲讀。來源／畫面核查見 [`verify-3.md`](verify-3.md)。
