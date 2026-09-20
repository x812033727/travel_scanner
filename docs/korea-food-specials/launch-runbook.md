# 上線逐步清單（韓國美食與咖啡特輯 22 篇）

**正式站的每一步都要站主明確同意才做。** 這份清單是為了「同意之後不必再想指令」，不是授權。

前提：PR-C 已合併進 `main`。分類機制（PR #580，migration 0082）與料理資料庫（PR #581／#586）**已經在 main**。

---

## 0. 出發前（本機，不碰正式站）

```bash
cd apps/api && python -m app.guides.pack_cli lint --kind howto
```

零錯誤。再確認 22 個內容包與 22 組資產都在。

**確認主機上沒有別人的分階段發布正在進行**（`/root/travel-scanner-deploy.hold`）。有的話就停下來問站主——那個 hold 是別的發布流程的鎖，硬闖會把它切斷。

## 1. 部署

照 `ops/release/README.md` 的既有流程。這一批**沒有**多階段發布，是一般的 deploy。

部署會同時帶上 **migration 0082**（旅遊子主題）——它是 seeding-only、只插入缺的 slug、導言只寫 NULL 的列，重跑不會覆蓋後台編輯過的內容。

## 2. 記下基準，再種料理

種之前先記下現況，才有辦法判斷種子有沒有種出預期的東西：

```bash
curl -s "https://mokaair.com/api/travel/foods/facets" | python -m json.tool | head -30
```

（2026-09-20 的基準：全部 120 道、韓國 25 道。）

```bash
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli seed-foods
```

**`seed-foods` 是冪等的，但沒有 dry-run。** 跑完應該是：全部 127 道、韓國 32 道（新增 7 道）。

驗證「認養」有沒有生效——這兩家是正式站早就公開的店，種子只會加料理連結、不動審核狀態：

```bash
curl -s "https://mokaair.com/api/travel/foods/merchants?q=豬肉湯飯" | python -m json.tool | head -40
```

송정3대국밥應該出現。新增的代表店則是 pending／inactive，**不會**出現在公開 API——那是正確的。

## 3. 匯入文章

先不帶 slug 跑一次，確認沒有意外的內容跟著進去：

```bash
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-import --dry-run
```

**看清楚這一份計畫再往下。** 站上有大量刻意保留（未發布）的文章，一個不帶 slug 的 `--publish` 會把它們全部推上線。

確認無誤後，只匯入這 22 篇：

```bash
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-import \
  --slug busan-dwaeji-gukbap-food-guide --slug seoul-dwaeji-gukbap-food-guide \
  --slug busan-milmyeon-food-guide --slug seoul-naengmyeon-food-guide \
  --slug seoul-samgyetang-food-guide --slug seoul-seolleongtang-food-guide \
  --slug seoul-dak-hanmari-food-guide --slug seoul-kalguksu-food-guide \
  --slug seoul-jokbal-food-guide --slug seoul-tteokbokki-food-guide \
  --slug seoul-ganjang-gejang-food-guide --slug jeju-heukdwaeji-food-guide \
  --slug jeju-gogi-guksu-food-guide --slug daegu-jjim-galbi-food-guide \
  --slug daegu-makchang-food-guide --slug jeonju-bibimbap-food-guide \
  --slug busan-jeonpo-yeongdo-cafe-guide --slug seoul-seongsu-cafe-guide \
  --slug seoul-yeonnam-hongdae-cafe-guide --slug seoul-ikseon-bukchon-hanok-cafe-guide \
  --slug jeju-aewol-cafe-guide --slug jeju-gujwa-sehwa-cafe-guide \
  --locale zh-TW --dry-run
```

應該是 **22 個 create、0 個 update**。確認之後把 `--dry-run` 換成 `--publish`。

## 4. 重建連結

```bash
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-links-rebuild
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-links-check --locale zh-TW
```

## 5. 逐頁驗證

每一篇：HTTP 200、h1 等於標題、canonical 正確、**沒有 noindex**、hero 與圖解都 200。

```bash
for s in busan-dwaeji-gukbap-food-guide seoul-seongsu-cafe-guide daegu-jjim-galbi-food-guide; do
  curl -s -o /dev/null -w "%{http_code} $s\n" "https://mokaair.com/zh-TW/guides/howto/$s"
done
```

分類頁（每道料理一個，這是站主當初要的東西）：

```bash
for t in kr-dwaeji-gukbap kr-naengmyeon kr-samgyetang kr-beef-bone-soup kr-dak-hanmari \
         kr-kalguksu kr-jokbal kr-tteokbokki kr-heukdwaeji kr-gogi-guksu kr-jjim-galbi \
         kr-makchang kr-ganjang-gejang kr-bibimbap cafe; do
  curl -s -o /dev/null -w "%{http_code} $t\n" "https://mokaair.com/zh-TW/guides/topics/$t"
done
```

還要看的：

- 麵包屑是「旅遊情報與攻略 › 旅遊攻略 › 美食 › ○○ › 標題」（本機已驗過設計成立）
- **沒有合作方案面板**（子主題不觸發，本機已驗過）
- `travel-zh-TW` sitemap 列出這 22 篇
- 每篇文末的美食目錄連結點進去**不是空清單**（上線前我實測過十組篩選全部非空，但種完料理後要再看一次）
- **隨機抽三篇、每篇抽一個 Naver 連結，在真實瀏覽器打開確認是對的店**。遇到機器人驗證就停手，不要繞過。

## 6. 上線之後

- `handoff/admin-todo.md` 的後台待辦（A 組一定要做：刀切麵改名、重存讓中文搜尋建得起來、新代表店補 Naver 與座標）
- 票 `2026-09-20-korea-food-specials-backlinks`（讓既有的韓國內容連到這 22 篇）
- 票 `2026-09-20-kfood-closure-sweep-2026-12`（每季歇業複查）
