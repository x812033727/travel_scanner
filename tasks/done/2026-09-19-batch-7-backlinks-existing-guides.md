---
id: 2026-09-19-batch-7-backlinks-existing-guides
title: 既有文章補連第七批：25 篇既有文章加 article inline 連到第七批
status: done
priority: P2
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-19T06:50:21Z
created_at: 2026-09-19T06:50:21Z
completed_at: 2026-09-19T08:00:16Z
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - apps/api/app/guides/content/bangkok-airport-to-city.json
  - apps/api/app/guides/content/bangkok-bts-mrt-boat-guide.json
  - apps/api/app/guides/content/bangkok-4-day-itinerary.json
  - apps/api/app/guides/content/chiang-mai-3-day-itinerary.json
  - apps/api/app/guides/content/korea-food-guide-must-eat.json
  - apps/api/app/guides/content/korea-ktx-srt-ticket-guide.json
  - apps/api/app/guides/content/korea-naver-map-kakao-t-guide.json
  - apps/api/app/guides/content/gimhae-airport-to-busan.json
  - apps/api/app/guides/content/busan-3-day-itinerary.json
  - apps/api/app/guides/content/seoul-4-day-itinerary.json
  - apps/api/app/guides/content/hanoi-4-day-itinerary.json
  - apps/api/app/guides/content/da-nang-hoi-an-4-day-itinerary.json
  - apps/api/app/guides/content/ho-chi-minh-city-4-day-itinerary.json
  - apps/api/app/guides/content/vietnam-money-sim-grab-guide.json
  - apps/api/app/guides/content/taiwan-long-weekends-2027-flight-planning.json
  - apps/api/app/guides/content/japan-cherry-blossom-2027.json
  - apps/api/app/guides/content/japan-ic-card-suica-icoca-guide.json
  - apps/api/app/guides/content/japan-shinkansen-ticket-guide.json
  - apps/api/app/guides/content/japan-train-disruption-plan.json
  - apps/api/app/guides/content/phuket-airport-transport-where-to-stay.json
  - apps/api/app/guides/content/thailand-esim-sim-wifi.json
  - apps/api/app/guides/content/hong-kong-4-day-itinerary.json
  - apps/api/app/guides/content/hong-kong-airport-to-city.json
  - apps/api/app/guides/content/cheung-chau-walking-day.json
  - apps/api/app/guides/content/singapore-4-day-itinerary.json
---

# 既有文章補連第七批：25 篇既有文章加 article inline 連到第七批

## Why

第七批二十篇 2026-09-17 上線（PR #543）。每篇規格 `docs/travel-guides-batch-7/<slug>.md` 的
「上線後與交叉檢查」都寫了要在 main 上既有文章裡加的反向連結（哪一篇、哪一個區塊、連結文字講什麼），
README 的收件步驟第 6 條要求彙整成一張「既有文章補連第七批」的票。沒有反向連結，第七批只有連出去、
沒有連進來，城市頁以外的讀者找不到它們。

## Definition of done

- [x] 20 份規格的反向連結指令全部收齊，分成「要做」「規格說不要做」「可選」三類（見 Notes）。
- [x] 25 篇既有內容包依規格加上 article inline（共 39 個）；`paragraph` 整塊改 `rich_paragraph` 時
      原文一個字不改；規格給的 block 索引都對過現在的檔案內容。
- [x] `pack_cli lint --kind howto`／`--kind intel` 對這 25 篇沒有新的 error；`tests/test_guides_content_pack.py` 綠。
- [x] 合併部署後在正式站 `guides-import` 這 25 個 slug、`guides-links-rebuild`、
      `guides-links-check --locale zh-TW` 都通過（站主在主機上跑，見 How to verify）。

## Steps

- [x] 收集 20 份規格的反向連結與「既有文章待修」項目。
- [x] 開票、認領（scope 只列真的會改的 25 個內容包）。
- [x] 照規格逐篇改（做法與位置見 Notes）。
- [x] 自檢：新加的每個 inline 的 slug 都有內容包、kind 一致；被改的段落原文只有插入、沒有刪改；
      沒有兩個 offer 相鄰、沒有兩個 article inline 相鄰（一次性腳本，不進 repo）。
- [x] 合併後由站主在主機上匯入、重建連結圖、跑連結檢查。

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --kind howto
uv run python -m app.guides.pack_cli lint --kind intel
uv run pytest tests/test_guides_content_pack.py -q
```

2026-09-19 的結果：howto 124 entries、intel 21 entries，這 25 篇只有原本就有的 `no_summary` warning；
`cheung-chau-walking-day`、`japan-train-disruption-plan` 的 `diagram_number_not_in_text` 與
`seoul-4-day-itinerary` 的 `svg_small_label` 三個 error 在 HEAD 就有（拿 HEAD 版本單獨 lint 過），
不是這張票造成的。pytest 9 passed、5 skipped。`pack_cli` 沒有連結檢查子命令，連結檢查是
`app.cli guides-links-check`，要資料庫，本機跑不了。

合併部署後在主機上：

```bash
uv run python -m app.cli guides-import --dry-run \
  --slug bangkok-airport-to-city --slug bangkok-bts-mrt-boat-guide --slug bangkok-4-day-itinerary \
  --slug chiang-mai-3-day-itinerary --slug korea-food-guide-must-eat --slug korea-ktx-srt-ticket-guide \
  --slug korea-naver-map-kakao-t-guide --slug gimhae-airport-to-busan --slug busan-3-day-itinerary \
  --slug seoul-4-day-itinerary --slug hanoi-4-day-itinerary --slug da-nang-hoi-an-4-day-itinerary \
  --slug ho-chi-minh-city-4-day-itinerary --slug vietnam-money-sim-grab-guide \
  --slug taiwan-long-weekends-2027-flight-planning --slug japan-cherry-blossom-2027 \
  --slug japan-ic-card-suica-icoca-guide --slug japan-shinkansen-ticket-guide --slug japan-train-disruption-plan \
  --slug phuket-airport-transport-where-to-stay --slug thailand-esim-sim-wifi --slug hong-kong-4-day-itinerary \
  --slug hong-kong-airport-to-city --slug cheung-chau-walking-day --slug singapore-4-day-itinerary
# 計畫應該只有這 25 篇的 zh-TW 有變動；確認後拿掉 --dry-run、加 --publish 再跑一次
uv run python -m app.cli guides-links-rebuild
uv run python -m app.cli guides-links-check --locale zh-TW
```

## Notes

### 做了什麼（內容包、位置、連到哪）

區塊索引是改完後的索引。「新增」＝插入一個新的 `rich_paragraph`；「改」＝把該 `paragraph` 整塊改成
`rich_paragraph`，原文一個字不動，只在指定位置插入 inline 與必要的連接句。

泰國
- `bangkok-airport-to-city`：新增 blocks[16]（H2「住蘇坤蔚、暹羅、考山路，各選哪一種」與清單之間，
  文字照規格）→ `bangkok-where-to-stay`。
- `bangkok-bts-mrt-boat-guide`：新增 blocks[27]（「尖峰與常用路線」的 tip callout 之後）→ `bangkok-where-to-stay`。
- `bangkok-4-day-itinerary`：改 blocks[0]，「住在暹羅到蘇坤蔚一帶」後面用括號接 inline → `bangkok-where-to-stay`；
  改 blocks[19]（預算、季節那段）段末 → `southeast-asia-seasons-when-to-go`。
- `chiang-mai-3-day-itinerary`：新增 blocks[15]（Day 3 清單之後、照片之前，文字照規格）→ `chiang-rai-2-day-itinerary`；
  改 blocks[22]（季節段）段末 → `southeast-asia-seasons-when-to-go`。
- `phuket-airport-transport-where-to-stay`：改 blocks[31]（季節段）段末 → `southeast-asia-seasons-when-to-go`；
  新增 blocks[34] → `phuket-phi-phi-james-bond-island-hopping`、blocks[35] → `krabi-airport-transport-where-to-stay`
  （結尾，曼谷四天連結之後；「不放 activities」的規則沒動）。
- `thailand-esim-sim-wifi`：新增 blocks[29]（普吉那一句之後，同一個寫法）→ `krabi-airport-transport-where-to-stay`。

韓國
- `korea-ktx-srt-ticket-guide`：改 blocks[25]，第 13、15 篇合併成同一次編輯：慶州純文字 → 東大邱那句＋inline
  → `daegu-airport-ktx-subway-guide` → 全州那句＋inline → `jeonju-hanok-village-day-trip-from-seoul`；
  數字一個都沒動，兩個 inline 中間隔著文字。
- `korea-food-guide-must-eat`：新增 blocks[31]（濟州段之後、三個行程連結之前），一句大邱
  （따로국밥、막창구이，只用大邱篇已寫的「大邱 10 味」說法，不寫店家與價格）→ `daegu-2-day-itinerary`。
- `korea-naver-map-kakao-t-guide`：改 blocks[40] 段末加一句大邱（機場官網沒有估價、沒有夜間加成，出自大邱交通篇）
  → `daegu-airport-ktx-subway-guide`。
- `gimhae-airport-to-busan`：新增 blocks[21]（行前檢查之後、城市頁連結之前）「從釜山接大邱」→ `daegu-airport-ktx-subway-guide`。
- `busan-3-day-itinerary`：新增 blocks[28]（行前檢查之後）「往北到大邱住一晚」→ `daegu-2-day-itinerary`
  （規格列為可選；釜山到東大邱的車程數字沒寫進去，由第 13 篇負責）。
- `seoul-4-day-itinerary`：新增 blocks[24]（DMZ 的 rich_paragraph 之後、activities offer 之前）
  「想跑更遠可以換成全州」→ `jeonju-hanok-village-day-trip-from-seoul`。

越南
- `hanoi-4-day-itinerary`：改 blocks[25]（Day 3 下龍灣那段），「本篇不列。」之後接 inline＋「另有專篇」
  → `ha-long-bay-cruise-from-hanoi`，比較表與三個 offer 沒動；新增 blocks[13]（內排機場段末）
  → `vietnam-domestic-flights-train-guide`；改 blocks[2] 季節句之後、簽證那行之前 → `southeast-asia-seasons-when-to-go`。
- `da-nang-hoi-an-4-day-itinerary`：改 blocks[22]（Day 4 段）句尾「想看皇城與陵墓就往北去順化」
  → `hue-day-trip-from-da-nang`；改 blocks[7]（機場段）段末 → `vietnam-domestic-flights-train-guide`；
  改 blocks[2] 季節句之後 → `southeast-asia-seasons-when-to-go`。`foods?city=da-nang` 沒動。
- `ho-chi-minh-city-4-day-itinerary`：改 blocks[8]（T3 那段）段末 → `vietnam-domestic-flights-train-guide`；
  改 blocks[2] 季節段段末 → `southeast-asia-seasons-when-to-go`。
- `vietnam-money-sim-grab-guide`：新增 blocks[40]（「河內、峴港、胡志明市」段末、callout 之前）
  → `vietnam-domestic-flights-train-guide`。

日本與台灣連假
- `taiwan-long-weekends-2027-flight-planning`：改 blocks[10]（撞期段第一段）段末接 inline → `japan-golden-week-2027`
  （inline 是該區塊最後一個 inline、後面沒有標點，和同篇其他獨立連結一樣；季節段例外，**2027-05-11 要刪**：
  只拿掉那個 article inline，原段落就完整保留，票 `2026-09-19-gw-sakura-links-expire-2027-05`）；新增 blocks[17]（札幌雪祭 inline 之後、清明那句之前，文字照規格）
  → `lunar-new-year-2027-asia-travel`（**2027-02-21 整個區塊刪掉、不留純文字**，票 `2026-09-19-lny-links-expire-2027-02-21`）；
  blocks[5] 表格春節列的「日韓同期」格照農曆新年篇規格改成「韓國설 연휴 2/6–2/9（설날 2/7）」，
  與 `lunar-new-year-2027-asia-travel`、`dmz-day-trip-from-seoul` 的口徑一致。
- `japan-cherry-blossom-2027`：新增 blocks[18]（撞期段末）→ `japan-golden-week-2027`（兩篇同一天 2027-05-10 到期，
  不用刪除票）；新增 blocks[35]（「仙台、札幌與北陸」照片之後、札幌連結之前）→ `sendai-matsushima-2-day-itinerary`。
- `japan-shinkansen-ticket-guide`：新增 blocks[7]（旺季 callout 之後、H2「怎麼買」之前；第 9、10 篇擇一，
  只加這一個區塊）→ `sendai-airport-access-loople-bus-guide`。
- `japan-ic-card-suica-icoca-guide`：改 blocks[2]（十卡互通那段）加一行 icsca（只在仙台圈、不能當便利商店電子錢包，
  出自仙台交通篇）→ `sendai-airport-access-loople-bus-guide`。
- `japan-train-disruption-plan`：新增 blocks[4]（第一個 H2 段末、圖解之前）仙山線一條線進出的例子
  → `yamadera-day-trip-from-sendai`，拿掉連結仍讀得通。

港澳星
- `hong-kong-4-day-itinerary`：改 blocks[29]，「想去就多留一天。」之後接 inline → `macau-day-trip-from-hong-kong`，
  blocks[30] 原樣；改 blocks[36]（颱風段）段末 → `southeast-asia-seasons-when-to-go`。
  **沒有連 `lunar-new-year-2027-asia-travel`**（規格明講長青 howto 不連 2027-02-20 到期的 intel）。
- `hong-kong-airport-to-city`：新增 blocks[42]（「依住宿區選路線」段末、「回程去機場」之前），
  住上環、中環的人往澳門（港澳碼頭在上環站上面，出自澳門篇）→ `macau-day-trip-from-hong-kong`。
- `cheung-chau-walking-day`：新增 blocks[23]（最後）「另一個從碼頭出發的一日」→ `macau-day-trip-from-hong-kong`（規格列為可選）。
- `singapore-4-day-itinerary`：改 blocks[30]，「費用以聖淘沙官網為準。」之後接 inline → `sentosa-day-guide`
  （只做這一處，blocks[39] 的清單沒動）；改 blocks[2] 季節段段末 → `southeast-asia-seasons-when-to-go`。

連進來的數量：`southeast-asia-seasons-when-to-go` 8、`vietnam-domestic-flights-train-guide` 4、
`bangkok-where-to-stay` 3、`daegu-airport-ktx-subway-guide` 3、`macau-day-trip-from-hong-kong` 3、
`daegu-2-day-itinerary` 2、`jeonju-hanok-village-day-trip-from-seoul` 2、`japan-golden-week-2027` 2、
`sendai-airport-access-loople-bus-guide` 2、`krabi-airport-transport-where-to-stay` 2，其餘
（`chiang-rai-2-day-itinerary`、`hue-day-trip-from-da-nang`、`ha-long-bay-cruise-from-hanoi`、
`sendai-matsushima-2-day-itinerary`、`yamadera-day-trip-from-sendai`、`phuket-phi-phi-james-bond-island-hopping`、
`sentosa-day-guide`、`lunar-new-year-2027-asia-travel`）各 1，共 39 個。
`zao-fox-village-from-sendai` 與 `krabi-ao-nang-railay-4-islands` 照規格不列反向連結（入口由第 9、10 篇與第 3、5 篇提供）。

### 規格說明「不要做」的，都沒做

- `hong-kong-4-day-itinerary` 不連農曆新年篇（時效規則）。
- `korea-olive-young-tax-refund-shopping` 不必改（大邱篇規格）。
- `zao-fox-village-from-sendai` 不去搶 `japan-shinkansen-ticket-guide` 那一段；第 9、10 篇擇一，只加一個區塊。
- `list` 項目是純字串、放不了 inline：清邁 Day 3 清單、新幹線篇 blocks[4]、新加坡 blocks[39]、
  曼谷機場篇的分區清單都沒碰，照規格改用相鄰的新區塊。
- 三篇曼谷文、清邁、峴港、香港三篇的 `foods?city=` 都沒順手改，等 `2026-09-14-food-links-city-param-ignored`。

### 規格列為可選、這張票沒做的（要做另開票或併入下次修訂）

- `seoul-palaces-hanbok-guide`（block 6、7 之後）與 `suwon-hwaseong-day-trip` 韓服段加
  「首爾以外不一定有這條規定，例如全州慶基殿」連全州篇：這會在那兩篇加入一個需要出處的新主張
  （慶基殿穿韓服不免票），規格自己也寫了改完要重跑 ingest 並更新 `checked_on`，不是純加連結，留給另一張票。
- `gyeongju-day-trip-from-busan`「往北到大邱」：規格是釜山三天或慶州擇一，做了釜山三天。
- `singapore-gardens-indoor-outdoor` 文末第四個 inline 連聖淘沙：規格寫「不是必要」。
- `vietnam-money-sim-grab-guide` 加連下龍灣篇：規格寫「可選（另開票）」。

### 既有文章待修（不在這張票）

規格點名的三處沒有出處的季節說法——`bangkok-4-day-itinerary` 的「5 月到 10 月雨季」、
`chiang-mai-3-day-itinerary` 的「6 月到 10 月是雨季」與「PM2.5 常在 3 月最嚴重」——已經有專票
`2026-09-16-existing-guides-season-sources`（寫明了正確口徑與月份表來源），這張票不重做；
只把那兩段改成了 `rich_paragraph`，那張票改字時改 `inlines[0].text` 即可。
那張票的 scope 與本票重疊，要等本票合併後才認領得到。

### 給日期票的資訊

- `2026-09-19-lny-links-expire-2027-02-21`：`taiwan-long-weekends-2027-flight-planning` 要刪的是 blocks[17]
  （唯一一個含 `lunar-new-year-2027-asia-travel` inline 的 rich_paragraph），整塊刪。
- `2026-09-19-gw-sakura-links-expire-2027-05`：`taiwan-long-weekends-2027-flight-planning` blocks[10]
  只拿掉 `japan-golden-week-2027` 的 article inline（它是最後一個 inline，後面沒有 text）；`japan-cherry-blossom-2027`
  連黃金週的 blocks[18] 同一天到期，不用動。

### 其他

- 這 25 篇已經上線，改的是既有內容包，匯入後 `modified_at` 會動，屬預期。
- 沒有碰第七批的 20 個內容包，也沒碰規格沒點名的內容包。
- BEM 首末班、AOT S1 末班、Greenbus、SR 改點這類「兩篇要一起改」的事項是各篇日期票的範圍，不在這裡。

### 2026-09-19 主機執行（claude-opus-5，站主逐項同意；部署 `6a254971` 之後）

- 站主同意後在主機執行：dry-run 25 篇皆 `zh-TW update`、taxonomy `unchanged`；與發布前重跑的 dry-run 逐位元組相同後 `--publish`：`updated 25`、`published 25`、`failed null`；重跑 dry-run 25 篇皆 `unchanged`。
- `guides-links-rebuild`：materialized 1,270、dropped 0。`guides-links-check --locale zh-TW`：32 筆，`missing` 27 筆全是指向待發布的 AI coding 內容（`2026-09-15-publish-held-ai-coding-content` 記的那 27 條），`raw_url` 5 筆在 `codex-beginner-guide`（4）與 `gemini-guide`（1）；**來源是這 25 篇的問題 0 筆**。
