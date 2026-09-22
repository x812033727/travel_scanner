# 上線 runbook：從合併到逐頁驗證

每一步動到正式站都要站主明確同意。這份清單是「同意之後不必再想指令」，不是授權。實例：`docs/korea-food-specials/launch-runbook.md`（它的 `seed-foods` 那幾步是那批專屬的）。

## 0. 出發前（本機，不碰正式站）

- PR 已合併到 main，目標 SHA 的 CI 綠。
- `cd apps/api && <PY> -m app.guides.pack_cli lint --kind <KIND>` 零 error（warning 另議）。
- 確認主機上沒有別人的分階段發布：`/root/travel-scanner-deploy.hold` 存在就停下來問站主。怎麼分辨活的發布和被遺棄的 hold，讀 `ops/release/README.md`。一般部署腳本看到 hold、或別的 session 的 `/root/mokaair-*/state.json`，會以 exit 3 拒絕。
- 寫內容前先 `pg_dump`（站主的既有做法）。

## 1. 部署

照 `ops/release/README.md`。純內容批次是一般 deploy，沒有多階段。部署會一併帶上 migration；seeding-only 的 migration 重跑不會覆蓋後台編輯過的內容。

## 2. 批次專屬的種子步驟（有才做）

例：料理資料庫 `seed-foods`（冪等，沒有 dry-run）。**先記基準再種**：`curl -s "https://mokaair.com/api/travel/foods/facets"` 數一次，種完再數一次。數字對不上就是已經有人跑過，或種子檔和正式站不一致。

## 3. 匯入

```bash
# 3a 不帶 slug：只為了看積壓。站上有大量刻意保留（未發布）的文章，
#    一個不帶 slug 的 --publish 會把它們全部推上線。
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-import --dry-run
# 3b 只看自己的：預期 N 個 create、M 個 update，其餘不該出現
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-import --slug <S1> --slug <S2> --locale zh-TW --dry-run
# 3c 計畫與站主看過的一致，才把 --dry-run 換成 --publish
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-import --slug <S1> --slug <S2> --locale zh-TW --publish --actor-email <ACTOR_EMAIL>
```

- `<ACTOR_EMAIL>` 取容器的 `ADMIN_EMAILS` 第一個。沒帶會以「The actor must be an active administrator」失敗，而且什麼都不寫。
- 在 `apps/api/app/guides/publish_holds.json` 裡的 slug 帶 `--publish` 會整批拒絕；先清 hold 或拿掉那個 slug。
- dry-run 回 `{dry_run, articles: [{slug, taxonomy, locales: [{locale, action, publish}]}]}`；publish 回 `{created, updated, unchanged, published, taxonomy_updated, failed}`。兩者形狀不同，別拿同一段程式比。
- 五語系文章的 `--locale` 要列全；更新既有文章（`update`）與新文章同一次 `--slug` 匯入。
- 匯入完再跑一次 3b 的 dry-run：應全部 `unchanged`。

## 4. 連結

```bash
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-links-rebuild
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-links-check --locale zh-TW
```

## 5. 逐頁驗證（本機，未登入）

```bash
cd apps/api && <PY> <ROOT>/.agents/skills/content-pipeline/scripts/verify_public.py --slug <S1> --slug <S2> --kind howto --locale zh-TW --sitemap
```

每篇：200、h1 等於內容包標題、canonical 正確、沒有 noindex、hero 與每張圖解 200、在 sitemap 裡。網址形狀：生活分享 `/<locale>/life/<slug>`，其餘 `/<locale>/guides/<kind>/<slug>`；分類頁 `/<locale>/guides/topics/<topic>`。

- 正式站有讀取限流：腳本循序、每次間隔 1.3 秒以上；不要多執行緒。
- `SITEMAP_LIMIT` 是 1,000 列，超過會靜默掉最舊的：上線前後各數一次。
- 麵包屑取 `topics[0]`（依 display_order）：文章掛子主題就只掛子主題，否則料理名不會出現。
- 隨機抽三篇的外部連結（Naver 等）在真實瀏覽器打開確認。遇到機器人驗證就停手，不繞過。

## 6. 之後

- `<BATCH_DOCS>/FOLLOWUPS.md` 有日期的項目開成票：刪連結的日期、季節到期、反向連結彙整成一張票。
- 票 `npm run tasks -- done <id>`；STATE 與 HANDOVER 更新；Claude 端把學到的寫進記憶，Codex 端寫進 HANDOVER。
- 後台待辦（改名、重存讓搜尋建索引、補座標）列成 handoff 檔給站主。
