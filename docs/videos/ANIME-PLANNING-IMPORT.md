# 將長篇動漫企劃建立成後台作品

《借來的黎明》的原始內容已由 [PR #1113](https://github.com/x812033727/travel_scanner/pull/1113) 保存。這個匯入路線把同一份內容建立為可在後台閱讀的作品：**動漫分類、22 分鐘正文、30 分鐘播出時段、十季／120 集、群像與封閉結局**。

作品顯示「企劃待製作」。匯入後有一筆 `paused` 作品、十二份原文文件及一百二十筆 `planned` 集數；每集保留兩段張力、後果及連貫狀態。它們是企劃細綱，尚不是二十二分鐘完整台詞、分鏡或成片。完整製作仍由 `2026-10-02-anime-long-episode-support` 追蹤。

## 先備條件

- 已合併並部署本 PR 的 API、Web 及資料庫 migration `0121_video_series_planning`。部署遵循既有部署流程；單純拉取文件不會更新正在執行的容器。
- 有正式主機的操作權限，及資料庫內有效的管理員。預設使用後台既有唯一管理員設定；多名管理員時在主機明確選擇 `--actor-email`，不輸出帳號或金鑰。
- 來源是 [borrowed-dawn](series-plans/borrowed-dawn/README.md) 的完整企劃包。未改造為八分鐘短漫劇，也未偽填爽點或核准結果。

以下主機指令在 `/root/travel_scanner` 執行。它們不啟用工人、呼叫生成供應商或發布影片。

## 1. 離線準備匯入包

在本機有 API 開發環境時，可從儲存庫根目錄執行：

```bash
PYTHONPATH=apps/api apps/api/.venv/bin/python -m app.video_automation.planning_cli \
  --pack docs/videos/series-plans/borrowed-dawn \
  --prepare /tmp/borrowed-dawn-admin-bundle.json
```

沒有主機 Python 虛擬環境時，使用已部署的 API 映像和唯讀來源掛載。`--prepare -` 將 JSON 寫到檔案，雜湊收據寫到 stderr，兩者分開：

```bash
docker compose -f docker-compose.prod.yml run --rm --no-deps -T \
  -v "$PWD/docs/videos/series-plans/borrowed-dawn:/plans/borrowed-dawn:ro" \
  api python -m app.video_automation.planning_cli \
  --pack /plans/borrowed-dawn --prepare - > /tmp/borrowed-dawn-admin-bundle.json
```

準備階段不連資料庫。它驗證來源、文件、全部 manifest 雜湊、集數、人物與伏筆引用、張力資料及封閉結局，並重新核對 JSON／Markdown／CSV 的內容一致性。匯入包包含原文，沒有登入憑證；伺服器收到後仍會重新驗證，不只相信準備收據。

## 2. 正式資料庫預檢

```bash
docker compose -f docker-compose.prod.yml exec -T api \
  python -m app.video_automation.planning_cli --input - \
  < /tmp/borrowed-dawn-admin-bundle.json \
  > /tmp/borrowed-dawn-admin-dry-run.json

python3 -m json.tool /tmp/borrowed-dawn-admin-dry-run.json
```

確認輸出為 `applied: false`、`action: create`，以及 `category: anime`、`status: paused`、`planning_only: true`、`documents: 12`、`episodes: 120`。既有資料完全相同時為 `unchanged`；作品已修改、核准、進入製作，或影片／集數名稱有衝突時，預檢會拒絕。不要改名或覆蓋既有作品來繞過拒絕。

## 3. 套用同一份內容

從預檢報告取得這一份匯入包的 `sha256`：

```bash
anime_plan_sha=$(python3 -c 'import json; print(json.load(open("/tmp/borrowed-dawn-admin-dry-run.json"))["sha256"])')

docker compose -f docker-compose.prod.yml exec -T api \
  python -m app.video_automation.planning_cli --input - \
  --apply --expected-sha256 "$anime_plan_sha" \
  < /tmp/borrowed-dawn-admin-bundle.json
```

只有完整驗證、碰撞預檢和管理員身分都通過，才在同一個交易建立作品、文件、全部集數及稽核紀錄。任一步失敗都不回報成功；錯誤雜湊在進入資料庫模式前就被拒絕。重跑相同未修改內容不會新增第二份。

## 4. 讀回確認

再次執行步驟 2。成功建立且未被修改的作品應回報 `action: unchanged`，仍有十二份文件、一百二十集。

登入後直接開啟：[《借來的黎明》後台作品](https://mokaair.com/zh-TW/admin/videos?tab=drama&series=borrowed-dawn)。作品位於「漫劇」作品分頁，顯示「動漫／企劃待製作／群像」及原定時長；可閱讀全部文件與集數。未生成影片時，影片分類清單沒有一百二十支成片，不能把作品建立與影片完成混為一談。

這個狀態沒有製作請求、影片 slug、開始時間、核准紀錄或工人工作。API、資料庫和後台都保持待製作限制；一般漫劇的八分鐘上限與原本審核流程保留。撤回尚未製作的企劃仍沿用原有後台操作。

## 本次交付狀態

本 PR 提供建立支援、可驗證匯入包與操作方式。本機隔離資料庫的測試不代表已在正式後台建立；正式主機套用後，才以讀回報告及後台頁面確認完成。
