# 部署後：驗證與稽核

## 每次都做

| 檢查 | 怎麼看 | 正常 |
| --- | --- | --- |
| 部署腳本 | `DEPLOY_EXIT=0`，log 尾端「3/3 健康」 | 失敗會自動回滾，log 會寫 |
| migration | `docker compose -f docker-compose.prod.yml exec -T api alembic current` | 等於 repo 最新的 revision |
| 內部健康 | `curl 127.0.0.1:8090/health`、`/ready`；web `curl -sI 127.0.0.1:8091/` | 200；公開的 `/api/travel/health` 是 404，不是故障 |
| 公開站 | `curl -s -o /dev/null -w '%{http_code} %{time_total}s' https://mokaair.com/zh-TW` | 200、小於 1 秒；`/` 回 307 到 `/zh-TW` 是正常的語系導向 |
| 容器 | `docker compose -f docker-compose.prod.yml ps` | 七個應用容器 Up，映像標籤 `:local`（分階段驅動部署的會是 `:<sha>`） |
| 新程式真的在跑 | 抓一個這次 diff 加進的字串：`curl -s <頁面> \| grep -c '<字串>'` | 有；內容包的改動要等匯入才會出現 |

抓公開頁面要慢慢來：邊緣層對頁面有 5 r/s 的限流，自己的驗證迴圈跑太快會拿到 429，那是自己的節奏，不是站台壞了。腳本一律循序、每次至少 1 秒。

## 大功能上線後的三個問題

CI 綠、部署成功、首頁 200，功能仍可能一半是啞的。2026-09-07 那批景點主題上線後找到三類本機測試看不見的缺陷：

1. **新資料真的進 DB 了嗎？** 只有 seed 對真 DB 跑過才看得見的推導錯誤（例如座標來源的 type 有、URL 是 NULL，排行榜照列但加入行程 404）。
2. **新的背景工作有沒有人聽？** endpoint、佇列、worker 訂閱、額度守衛、設定卡全都在，前端卻沒有任何一處呼叫它。
3. **順序對嗎？** 例如先扣額度才檢查供應商有沒有金鑰，按二十次沒設定的按鈕就把當天額度花光。

查證用唯讀 SQL：`docker compose -f docker-compose.prod.yml exec -T postgres psql -U travel -d travel_scanner -Atc "select …"`，一個呼叫一句簡單的 select；帶 jsonb 運算子與複雜引號的會被分類器擋，JSON 欄位改從後台或公開 API 讀。

## 部署的副作用

- 每次部署重建全部應用容器，約 8 秒 502；AdSense 爬蟲曾撞到。
- hotspot-collector 重啟的第一輪會重算當天排行：部署前核准的景點幾分鐘內就公開，部署後核准的等最多 6 小時，所以重新部署也是讓新核准提早上線的方法。代價是那一輪也跑 guide backfill，吃 YouTube 與 Brave 額度；一天六次部署曾把兩個供應商都打到 quota_exhausted。
- 內容包沒匯入就不上線：未發布的 slug 回 200 的 noindex「這篇文章目前看不到」頁，不是 404。

## 邊緣層的假陽性

`ops/nginx/README.md` 的驗證步驟裡，這些在這台主機上會「通過但什麼都沒證明」：

- 偽造來源位址的 Redis 檢查在 api 沒有 `PUBLIC_READ_RATE_LIMIT_MODE` 時永遠回 0。
- `limit_req_log_level warn` 需要 server block 自己的 `error_log … warn`，否則事件全部被丟掉；看 `/var/log/nginx/mokaair-limit.log`，不是 `error.log`。
- `429` 的數量與 `grep -c 'limiting requests'` 不是同一個母體：`limit_conn` 也回 429 但記成 `limiting connections`，兩個字串都要抓。
- 用 `xargs -P 8` 打 80 次看不到限流，因為 8 個併發對 1.5 秒的頁面約等於 5 r/s，`burst=20` 吸收得掉；要證明限流有效用 40 個並行請求。
- `ss -tn` 看不到 TIME-WAIT，判斷哪一邊關連線要 `ss -tan`。
- 用 User-Agent 數爬蟲的 429 會被自己的稽核與冒名的掃描器騙；按來源位址分開、對照公布的網段再下結論。
- server 層級的 `access_log` 會**取代**繼承的那一條，加了條件式 log 之後正常請求可能整整幾天沒有任何紀錄（2026-09-19 到 22 就發生過）；`ops/nginx/README.md` 現在要求同層放兩條。

## 已知的主控台雜訊

每頁一個跨來源的 `Failed to load resource: 400`（Travelpayouts 腳本之後），以及 `/zh-TW/foods` 的 React #418 hydration 警告，都不是部署造成的。
