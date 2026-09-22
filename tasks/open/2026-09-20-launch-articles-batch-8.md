---
id: 2026-09-20-launch-articles-batch-8
title: 撰寫並上線第八批旅遊文章：二十篇 zh-TW 攻略與情報
status: in-progress
priority: P2
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-22T13:07:55Z
created_at: 2026-09-20T02:32:43Z
completed_at:
branch: claude/launch-articles-batch-8
depends_on:
  - 2026-09-19-plan-articles-batch-8
scope:
  - apps/api/app/guides/content/okinawa-lodging-tax-2027.json
  - apps/api/app/guides/content/japan-public-holidays-2027.json
  - apps/api/app/guides/content/ghibli-park-tickets-and-access.json
  - apps/api/app/guides/content/kanazawa-shirakawago-day-trip.json
  - apps/api/app/guides/content/onomichi-shimanami-kaido-cycling.json
  - apps/api/app/guides/content/kerama-islands-ferry-from-naha.json
  - apps/api/app/guides/content/okinawa-without-a-car.json
  - apps/api/app/guides/content/hallasan-hiking-reservation-guide.json
  - apps/api/app/guides/content/marado-gapado-ferry-day-trip.json
  - apps/api/app/guides/content/chiang-mai-airport-transport-where-to-stay.json
  - apps/api/app/guides/content/chiang-mai-night-markets-walking-streets.json
  - apps/api/app/guides/content/phuket-old-town-big-buddha-viewpoints.json
  - apps/api/app/guides/content/pattaya-koh-larn-day-trip-from-bangkok.json
  - apps/api/app/guides/content/thailand-temple-etiquette-dress-code.json
  - apps/api/app/guides/content/da-lat-3-day-itinerary.json
  - apps/api/app/guides/content/ninh-binh-day-trip-from-hanoi.json
  - apps/api/app/guides/content/my-son-sanctuary-day-trip-from-da-nang.json
  - apps/api/app/guides/content/vung-tau-day-trip-from-ho-chi-minh.json
  - apps/api/app/guides/content/ngong-ping-360-lantau-day.json
  - apps/api/app/guides/content/kuala-lumpur-3-day-itinerary.json
  - apps/web/public/guides/okinawa-lodging-tax-2027
  - apps/web/public/guides/japan-public-holidays-2027
  - apps/web/public/guides/ghibli-park-tickets-and-access
  - apps/web/public/guides/kanazawa-shirakawago-day-trip
  - apps/web/public/guides/onomichi-shimanami-kaido-cycling
  - apps/web/public/guides/kerama-islands-ferry-from-naha
  - apps/web/public/guides/okinawa-without-a-car
  - apps/web/public/guides/hallasan-hiking-reservation-guide
  - apps/web/public/guides/marado-gapado-ferry-day-trip
  - apps/web/public/guides/chiang-mai-airport-transport-where-to-stay
  - apps/web/public/guides/chiang-mai-night-markets-walking-streets
  - apps/web/public/guides/phuket-old-town-big-buddha-viewpoints
  - apps/web/public/guides/pattaya-koh-larn-day-trip-from-bangkok
  - apps/web/public/guides/thailand-temple-etiquette-dress-code
  - apps/web/public/guides/da-lat-3-day-itinerary
  - apps/web/public/guides/ninh-binh-day-trip-from-hanoi
  - apps/web/public/guides/my-son-sanctuary-day-trip-from-da-nang
  - apps/web/public/guides/vung-tau-day-trip-from-ho-chi-minh
  - apps/web/public/guides/ngong-ping-360-lantau-day
  - apps/web/public/guides/kuala-lumpur-3-day-itinerary
  - docs/travel-guides-batch-8/ERRATA.md
---

# 撰寫並上線第八批旅遊文章：二十篇 zh-TW 攻略與情報

## Why

第八批的二十份規格 2026-09-20 定稿，在 [`docs/travel-guides-batch-8/`](../../docs/travel-guides-batch-8)，
規劃票是 `2026-09-19-plan-articles-batch-8`。規格經過六組一致性審查（事實與口徑、區塊規則、連結與時效），
六份審查記錄合計改了 155 處。這張票是照規格把文章寫出來、查證、畫圖、上線。

這批先補只有一兩篇文章的城市：大叻是目的地目錄裡最後一個 0 篇的城市；廣島、金澤、胡志明市原本各只有一篇行程文；
沖繩、濟州、清邁、普吉、峴港各只有兩篇。另有兩篇 2027 年的時效情報（沖繩住宿稅、日本國定假日）。

## Definition of done

- [ ] 二十個內容包在 `apps/api/app/guides/content/`，zh-TW。slug、kind、destination、topics、display order、
      valid_until 與 `docs/travel-guides-batch-8/README.md` 的清單一致。每篇有 Commons hero、內文照片 1 到 2 張、
      自繪 SVG 圖解、表格、callout、summary 區塊、`related` 與 `aliases`、帶 `checked_on` 的 sources，以及規格指定的 offer
      （吉隆坡篇與泰國寺廟禮儀篇是零 offer）。
- [ ] 每個數字撰稿當天在官方頁重新核對過；官方頁沒寫的一律「以官網為準」。每篇留 `notes.md`。
      README「撰稿當天必須重查的時效事實」那張表逐列處理過（寧平長安停業、渡嘉敷 2026-10-01 調價等）。
- [ ] 每篇經過一位獨立查核者（不是撰稿者）逐條對官方頁；第一輪改超過三處事實的再查一輪。
- [ ] 站內文章連結用 `article` inline，城市頁與美食目錄用 `link` 區塊、網址用 `foods?destination_id=`；
      destination_id 是 null 的三篇照 README 的結尾 link 通則。
- [ ] `uv run pytest tests/test_guides_content_pack.py -q` 綠、`pack_cli lint --kind howto` 與 `--kind intel`
      對這二十篇沒有 error。
- [ ] （站主同意後）合併、部署，正式站 `guides-import --slug` ×20 先 `--dry-run` 確認只有這二十篇是 create，再 `--publish`，
      然後 `guides-links-rebuild` 與 `guides-links-check --locale zh-TW`。
- [ ] 上線 PR 照 [`docs/travel-guides-batch-8/FOLLOWUPS.md`](../../docs/travel-guides-batch-8/FOLLOWUPS.md)
      第 1 節開日期票、第 2 節開「既有文章補連第八批」票。

## Steps

- [ ] 一篇一位撰稿代理，照規格與兩批 README 寫；工作區在 repo 外。**同時在跑的代理不要超過 7 位。**
- [ ] 獨立查核：每篇一位新的代理，拿到的是「未查證的草稿」，逐條對官方頁並回報改掉的每一條。
- [ ] 收件：讀 `notes.md` 抽查數字、跑 `ingest --dry-run`、渲染圖解看過，再正式 ingest。
- [ ] 工具檢查不到、要另外看的：article inline 的 slug 與 kind、offer 位置與相鄰、表格欄數、
      summary 的數字是否逐字出現在正文、Commons 作者欄位、同一張 Commons 照片不得當兩篇的 hero
      （沖繩兩篇既有文章共用的那張黑潮之海照片不要再用）。
- [ ] **共用同一組數字的地方逐字對**：沖繩三篇（住宿稅一句、泊港交通只在慶良間篇、村稅金額只在慶良間篇）、
      濟州兩篇（巴士車種與票價、「漢拏山」）、清邁兩篇（八條共用事實、住宿四區名稱）、
      泰國四篇（寺廟服裝句、查龍寺 08:00–17:00、格蘭島）、越南四篇（統一線「到站（發車）」雙時刻、越南盾寫法）、
      昂坪篇與香港四天篇的七個共用事實。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
uv run python -m app.guides.pack_cli lint --kind howto
uv run python -m app.guides.pack_cli lint --kind intel
```

正式站上每個 `/zh-TW/guides/<kind>/<slug>` 回 200、沒有 noindex，hero 與 `diagram-1.svg` 載得到，
`sitemaps/sitemap/travel-zh-TW.xml` 有這二十篇。

## Notes

- 規格裡標「以官網為準」的地方是官方頁真的查不到，不要找第三方補數字。
- 這台機器讀不到或要特殊讀法的官方站列在兩批 README 的「事實查核」一節。
- 撰稿與查核代理呼叫外部站時，User-Agent 一律用 repo 工具的
  `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，不得帶任何人的 email 或個人資料。
- 研究檔與抓下來的原始頁不在 repo（規劃工作區）；規格的「官方來源」一節已把要用的網址與 2026-09-20 讀到的原文抄進去。
- 第七批的教訓（`tasks/done/2026-09-16-launch-articles-batch-7.md`）：二十個代理同時跑會撞模型限額；
  過了 `ingest --dry-run` 的草稿不等於查證過的文章；hero 壓不進 200 KB 時在 ingest 之後補壓。

## 進度（2026-09-22，第一波）

- 第一波七篇（寧平、頭頓、美山、慶良間、不開車玩沖繩、沖繩住宿稅、大叻）由七位 opus 撰稿代理各寫一篇（同時 ≤7），
  再各派一位新的 opus 查核代理逐條對官方頁。查核結果：美山 112 條／0 事實改動、頭頓 61／0、大叻 75／1、沖繩住宿稅 48／1、
  寧平 90／2、不開車玩沖繩 76／2、慶良間 80／6（→ 第二輪：六筆全部確認，另一筆改動＝座間味泊位編號 No.6／No.7A 在官方頁與港區地圖都查不到，整篇移除；復原步驟在工作區 verify-2.md）。七篇全部 `pack_cli ingest` 進 repo，hero 全部 ≤200 KB。第一波完成 2026-09-23。
- 讀者優先規則的裁決（描述只留一個查證戳記、開頭段最多一個出處語、標題與 summary 不寫自選數量）與規格差異都記在
  `docs/travel-guides-batch-8/ERRATA.md`（本票 scope 新增）。
- 協調者工具在持久目錄 `C:\Users\x8120\mokaair-work\_tools\`（WRITER.md、VERIFIER.md、intake_check.py、shared_check.py、shrink_hero.py），
  狀態檔 `C:\Users\x8120\mokaair-work\STATE.md`。
