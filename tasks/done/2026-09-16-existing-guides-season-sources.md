---
id: 2026-09-16-existing-guides-season-sources
title: 既有文章依第七批規劃修正：沒有出處的季節月份與霧霾說法
status: done
priority: P3
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-19T09:34:17Z
created_at: 2026-09-16T23:06:29Z
completed_at: 2026-09-19T11:00:37Z
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - apps/api/app/guides/content/bangkok-4-day-itinerary.json
  - apps/api/app/guides/content/chiang-mai-3-day-itinerary.json
  - apps/api/app/guides/content/da-nang-hoi-an-4-day-itinerary.json
---

# 既有文章依第七批規劃修正：沒有出處的季節月份與霧霾說法

## Why

規劃第七批時，季節篇的研究代理讀到泰國觀光局東京辦事處的天氣頁
（`thailandtravel.or.jp/about/weather/`）有 8 個地區乘 12 個月的官方月份表，
比各城市頁完整。對照之下，三篇既有文章寫的月份沒有出處，而且會和第七批的
季節篇（`southeast-asia-seasons-when-to-go`）互相矛盾——兩篇在季節段互連，
讀者點過去就會看到同一件事兩套說法。

## Definition of done

- [x] `bangkok-4-day-itinerary` 的「5 到 10 月雨季」改成 TAT 月份表的口徑
      （多雨 7 月到 10 月、少雨 1 月到 4 月與 12 月），sources 補上月份表那一頁。
- [x] `chiang-mai-3-day-itinerary` 的「PM2.5 常在 3 月最嚴重」拿掉哪一個月最嚴重的說法，
      改成「2 月到 4 月前後是燒田季，出發前查 Air4Thai 即時數據」。
      Air4Thai 與污染管制廳的頁面在這台機器上讀不到，不要補數值。
      同篇的雨季月份（6 到 10 月）若也沒有出處，一併改成以 TAT 月份表為準。
- [x] `da-nang-hoi-an-4-day-itinerary` 的季節月份取自 vietnam.travel 的城市頁，
      與同站的氣候總頁差一個月。確認要以哪一頁為準，兩處寫法一致，並在 sources 標明。
- [x] 改完之後，三篇與 `southeast-asia-seasons-when-to-go` 的說法一致。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
uv run python -m app.guides.pack_cli lint --kind howto
```

## Notes

- 這三篇已經上線，改的是既有內容包，`modified_at` 會動，屬預期。
- 第七批的季節篇規格（`docs/travel-guides-batch-7/southeast-asia-seasons-when-to-go.md`）
  的「官方來源」一節有月份表的網址與逐字讀到的月份，直接照它寫。
- 最好等第七批上線後和它一起改，兩邊同一個口徑；先改也可以，只要以月份表為準。

### 2026-09-19 done in repo (claude-fable-5-1)

口徑：以 `southeast-asia-seasons-when-to-go`（第七批季節篇，已在 `content/`）的字句為唯一基準。
兩個新來源的網址照規格「官方來源」抄，這台機器沒有再打開那兩頁；`checked_on` 依交辦填 2026-09-19，
主機匯入前若有人重開頁面核對，把日期改成實際打開那天。改法：`json.load` 走結構、只改指定 block 的字串、
用 `pack_ingest` 同一組設定寫回（改前確認三檔 round-trip 逐位元相同），diff 只有下面列的幾行。

- `bangkok-4-day-itinerary`（block 19 的 rich_paragraph，2026-09-19 補反向連結時轉成的那段）：
  「11 月到 2 月最涼最舒服也最貴；…5 月到 10 月雨季午後常有雷陣雨」→「泰國觀光局東京辦事處（TAT 東京）的
  月份表把曼谷的少雨月標在 1 月到 4 月與 12 月、多雨月在 7 月到 10 月，5、6、11 月居中；…多雨月的雨 TAT 寫
  多半像陣雨、一天分幾次下、很少整天下」。「最涼最舒服也最貴」和月份同一句、同樣沒有出處，季節篇也沒這樣寫，
  一併拿掉。sources 加 TAT 東京「タイの天気について」（月份表），排在 TAT Newsroom 潑水節那筆之後；15 → 16 筆。
- `chiang-mai-3-day-itinerary`（block 22）：「6 月到 10 月是雨季」→「TAT 清邁頁沒寫雨季月份，月份表把多雨期
  標在 5 月到 9 月」；「2 月到 4 月是燒田季，山區焚燒的 PM2.5 常在 3 月最嚴重…出發前看」→「每年 2 月到 4 月前後
  是泰北燒田季，霧霾重的日子素帖山看不到景，出發前查泰國污染管制廳的 Air4Thai 即時數據」（沒有數值、沒有哪一個月
  最嚴重）；「最舒服的是 11 月到 2 月的涼季，也是旺季、房價最高」→ TAT 清邁頁的說法（氣候涼、花開、適合健行賞鳥、
  乾季 11 月到 1 月平均約 25 度），「旺季、房價最高」沒有出處，拿掉。sources 加月份表頁與 TAT 東京清邁頁，排在
  TAT 東京清萊那筆之後；15 → 17 筆。清單裡「2 月到 4 月出發的人先查 Air4Thai 的 PM2.5」本來就沒有月份高低，沒動。
- `da-nang-hoi-an-4-day-itinerary`：以越南國家旅遊局的氣候總頁（季節篇用的那一頁）為準，城市頁只補總頁沒有的峴港。
  block 2：會安改成總頁的「2 月到 8 月晴熱，9 月到隔年 1 月多雨，9 月到 11 月是颱風與水患高峰」（原本是城市頁的
  「3 到 5 月最好，10 月到隔年 1 月多雨多風暴」）；峴港保留城市頁的「3 到 5 月最舒服、6 到 8 月雨少海水清澈但很熱、
  11 月到隔年 2 月是雨季」並寫明是城市頁。城市頁另一句「9 到 10 月最舒服」和總頁的 9 到 11 月颱風水患高峰對不上，
  依「總頁有寫就以總頁為準」的規則不再重複（沒有說哪一頁錯）。block 5 callout：「10 月到 12 月要留彈性」→
  「9 月到 11 月要留彈性」，內文改成總頁的 9 月起熱帶風暴、會安 9 到 11 月多雨偶有小淹水、雨季到隔年 1 月，
  峴港城市頁的雨季 11 月到隔年 2 月。sources：Da Nang、Hoi An 兩筆城市頁的 title 標明是城市頁、哪些內容取自它們；
  加「Weather and climate in Vietnam」（英文原文）；19 → 20 筆（schema 上限 20，之後再加要先併一筆）。
- 三篇與季節篇對照後字面一致：曼谷 1 月到 4 月與 12 月／7 月到 10 月／5、6、11 月居中；清邁 11 月到 2 月、
  5 月到 9 月多雨、2 月到 4 月前後燒田季、查 Air4Thai；越南中部 會安 2 月到 8 月、9 月到隔年 1 月多雨、
  9 月到 11 月颱風水患高峰、峴港城市頁 11 月到隔年 2 月。規格 `docs/travel-guides-batch-7/southeast-asia-seasons-when-to-go.md`
  「撰稿時要小心」(3)(4)(5)(8) 與「口徑不一致要一起修的三處」描述的差異改完即消失；那份規格與季節篇 pack 不在本票
  scope，沒動。

驗證（2026-09-19，本機）：
- `cd apps/api && uv run python -m app.guides.pack_cli lint --kind howto`：124 entries checked；三篇底下只有原本就有的
  `no_summary` warning、沒有 error（整份報告 exit 1 是其他 howto 既有的 `diagram_number_not_in_text`，不在本票 scope）。
- `uv run pytest tests/test_guides_content_pack.py tests/test_guides_content_links.py -q`：12 passed, 5 skipped。
- `grep` 三篇：「5 月到 10 月雨季」「6 月到 10 月是雨季」「3 月最嚴重」「10 月到隔年 1 月」「10 月到 12 月」都沒有了。

主機步驟（部署後，`--slug` 可重複）：

```bash
python -m app.cli guides-import --actor-email <admin> --dry-run \
  --slug bangkok-4-day-itinerary --slug chiang-mai-3-day-itinerary --slug da-nang-hoi-an-4-day-itinerary
# 應列 3 篇 zh-TW 的更新（modified_at 會動，屬預期）；確認後同一串參數把 --dry-run 換成 --publish，
# 再打開三篇的季節段與季節篇對一次，之後 done。
```

### 2026-09-19 主機匯入（claude-opus-5，站主同意；部署 `14ce467d` 之後）

- #563 改到的 571 個內容包先 dry-run：402 篇只有 `update`／`unchanged`、169 篇含 `create`（未發布的 AI coding、Claude Code、Codex 等，屬 `2026-09-15-publish-held-ai-coding-content` 的發布決定，全數排除，包括 zh-TW 更新、其他語系新建、分類會變的 `codex-beginner-guide`）。站主選「發布 402 篇更新」：發布前重跑計畫 402 篇、分類全 `unchanged`、無 `create`，`--publish` 結果 `updated 467`、`unchanged 51`、`published 467`、`created 0`、`failed null`；重跑 518 個語系全 `unchanged`。`guides-links-check --locale zh-TW` 仍是原本 32 筆（27 `missing` 指向待發布內容、5 `raw_url`），沒有新增。
- 三篇（`bangkok-4-day-itinerary`、`chiang-mai-3-day-itinerary`、`da-nang-hoi-an-4-day-itinerary`）都在已發布的 402 篇裡；公開頁 `/zh-TW/guides/howto/bangkok-4-day-itinerary` 已引用泰國觀光局（TAT）的月份資料。
