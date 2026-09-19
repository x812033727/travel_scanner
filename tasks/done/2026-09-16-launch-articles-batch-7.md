---
id: 2026-09-16-launch-articles-batch-7
title: 撰寫並上線第七批旅遊文章：二十篇 zh-TW 攻略與情報
status: done
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-16T23:06:26Z
completed_at: 2026-09-19T07:10:12Z
branch: claude/new-travel-guide-k2q5h3
depends_on:
  - 2026-09-14-plan-articles-batch-7
scope:
  - apps/api/app/guides/content/lunar-new-year-2027-asia-travel.json
  - apps/api/app/guides/content/japan-golden-week-2027.json
  - apps/api/app/guides/content/krabi-airport-transport-where-to-stay.json
  - apps/api/app/guides/content/krabi-ao-nang-railay-4-islands.json
  - apps/api/app/guides/content/phuket-phi-phi-james-bond-island-hopping.json
  - apps/api/app/guides/content/chiang-rai-2-day-itinerary.json
  - apps/api/app/guides/content/bangkok-where-to-stay.json
  - apps/api/app/guides/content/southeast-asia-seasons-when-to-go.json
  - apps/api/app/guides/content/sendai-airport-access-loople-bus-guide.json
  - apps/api/app/guides/content/sendai-matsushima-2-day-itinerary.json
  - apps/api/app/guides/content/yamadera-day-trip-from-sendai.json
  - apps/api/app/guides/content/zao-fox-village-from-sendai.json
  - apps/api/app/guides/content/daegu-airport-ktx-subway-guide.json
  - apps/api/app/guides/content/daegu-2-day-itinerary.json
  - apps/api/app/guides/content/jeonju-hanok-village-day-trip-from-seoul.json
  - apps/api/app/guides/content/ha-long-bay-cruise-from-hanoi.json
  - apps/api/app/guides/content/hue-day-trip-from-da-nang.json
  - apps/api/app/guides/content/vietnam-domestic-flights-train-guide.json
  - apps/api/app/guides/content/macau-day-trip-from-hong-kong.json
  - apps/api/app/guides/content/sentosa-day-guide.json
  - apps/web/public/guides/lunar-new-year-2027-asia-travel
  - apps/web/public/guides/japan-golden-week-2027
  - apps/web/public/guides/krabi-airport-transport-where-to-stay
  - apps/web/public/guides/krabi-ao-nang-railay-4-islands
  - apps/web/public/guides/phuket-phi-phi-james-bond-island-hopping
  - apps/web/public/guides/chiang-rai-2-day-itinerary
  - apps/web/public/guides/bangkok-where-to-stay
  - apps/web/public/guides/southeast-asia-seasons-when-to-go
  - apps/web/public/guides/sendai-airport-access-loople-bus-guide
  - apps/web/public/guides/sendai-matsushima-2-day-itinerary
  - apps/web/public/guides/yamadera-day-trip-from-sendai
  - apps/web/public/guides/zao-fox-village-from-sendai
  - apps/web/public/guides/daegu-airport-ktx-subway-guide
  - apps/web/public/guides/daegu-2-day-itinerary
  - apps/web/public/guides/jeonju-hanok-village-day-trip-from-seoul
  - apps/web/public/guides/ha-long-bay-cruise-from-hanoi
  - apps/web/public/guides/hue-day-trip-from-da-nang
  - apps/web/public/guides/vietnam-domestic-flights-train-guide
  - apps/web/public/guides/macau-day-trip-from-hong-kong
  - apps/web/public/guides/sentosa-day-guide
---

# 撰寫並上線第七批旅遊文章：二十篇 zh-TW 攻略與情報

## Why

第七批的二十份規格 2026-09-16 定稿，在 [`docs/travel-guides-batch-7/`](../../docs/travel-guides-batch-7)，
規劃票是 `2026-09-14-plan-articles-batch-7`。規格已經過三輪一致性審查（連結與時效、區塊規則、
事實與口徑，共 38 條發現全部處理）。這張票是照規格把文章寫出來、查證、畫圖、上線。

這批補上目錄裡原本 0 篇的喀比（primary）、仙台、大邱、清萊；全州與順化以一日遊的形式進站。
做完之後目錄裡只剩大叻是 0 篇。

## Definition of done

- [x] 二十個內容包在 `apps/api/app/guides/content/`，zh-TW。slug、kind、destination、topics、
      display order、valid_until 與 `docs/travel-guides-batch-7/README.md` 的清單一致。
      每篇有 Commons hero、內文照片 1 到 2 張、自繪 SVG 圖解、表格、callout、summary 區塊、
      `related` 與 `aliases`、帶 `checked_on` 的 sources，以及規格指定的 offer。
- [x] 每個數字撰稿當天在官方頁重新核對過；官方頁沒寫的一律「以官網為準」。每篇留 `notes.md`。
- [x] 站內文章連結用 `article` inline（不是 `link` 區塊），城市頁與美食目錄用 `link` 區塊、
      網址用 `foods?destination_id=`。
- [x] （部署後）`test_guides_content_pack` 綠、`pack_cli lint --kind howto` 與 `--kind intel` 沒有新的 error。
      部署後 `guides-import --dry-run` 只有這二十篇是 create，再 `--publish`，然後
      `guides-links-rebuild` 與 `guides-links-check`。（2026-09-19：二十篇已上線，#555 查 sitemap 20／20；
      本機 `test_guides_content_pack` 9 passed、lint 對這二十篇零 error；主機上的 `guides-links-rebuild`／
      `guides-links-check --locale zh-TW` 併入反向連結票 `2026-09-19-batch-7-backlinks-existing-guides` 的
      主機步驟，那張票 review 中。）
- [x] 上線 PR 把各規格「上線後與交叉檢查」裡有日期的事項開成票（2026-09-19 開了 24 張，見下方
      「日期票已開」）。
- [x] 既有文章的反向連結彙整成一張票：`2026-09-19-batch-7-backlinks-existing-guides`（2026-09-19）。

## Steps

- [x] 一篇一個撰稿代理，照規格與 `docs/travel-guides-batch-7/README.md` 寫；工作區在 repo 外。
      **一次不要超過 7 個代理**（20 個併發會撞到模型限額，第一次規劃就是這樣中斷的）。
- [x] 收件：讀 `notes.md` 抽查數字、跑 `ingest --dry-run`、渲染圖解看過，再正式 ingest。
- [x] 工具檢查不到、要人工看的：article inline 的 slug 與 kind、offer 位置與相鄰、
      表格欄數、summary 的數字是否逐字出現在正文、Commons 作者欄位。
- [x] **兩篇共用同一組數字的地方要逐字對**：喀比兩篇與普吉跳島篇（皮皮門票、瑪雅灣封閉期、
      渡輪班次）、仙台四篇（市內票券）、大邱兩篇、越南兩篇（SE 車次發車時刻）、
      農曆新年篇與黃金週篇。規劃時三輪審查抓到的錯，有一半以上就出在這裡。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
uv run python -m app.guides.pack_cli lint --kind howto
uv run python -m app.guides.pack_cli lint --kind intel
```

正式站上每個 `/zh-TW/guides/<kind>/<slug>` 回 200、沒有 noindex，hero 與 diagram-1.svg 載得到。

## Notes

- 規格裡標「以官網為準」的地方是官方頁真的查不到，不要自己找第三方補數字。
- 這台機器讀不到的官方站列在 `docs/travel-guides-batch-7/README.md` 的「事實查核」一節。
- 撰稿代理呼叫 Commons 等外部站時，User-Agent 一律用 repo 工具的
  `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，不要放任何個人資料。

**Scope 與 claim（2026-09-16）**：scope 列的是這二十個內容包檔與圖檔目錄，不是整個內容目錄。
`2026-09-15-content-summary-howto-and-life`（claude-fable-5-1）持有 `apps/api/app/guides/content`
整個目錄，工具把底下任何路徑都當成重疊，所以這張票用 `--force` 認領；這二十個 slug 一個都不在那張票的
工作範圍裡（那張票是替既有文章補 summary 與 FAQ，本批的檔案還不存在）。第六批遇到同樣情形、同樣處理。

## 撰稿進度（2026-09-17）

**二十篇已經寫完、ingest 進 repo，PR #543 已開。** 還沒做的只有部署與正式站發布。

- `pack_cli ingest` 二十篇全部成功，`tests/test_guides_content_pack.py` 9 passed 5 skipped，
  `lint --kind howto` 與 `--kind intel` 對這二十篇**零 error 零 warning**（站上既有文章的舊 error 不在本批範圍）。
- 這個 commit 只新增檔案，沒有修改任何既有內容包。
- 收件檢查（`scratchpad/write7/intake_check.py`）跑工具檢查不到的部分：欄位值與清單一致、offer 數量與位置、
  表格欄數、summary 的數字逐字對正文、article inline 的 slug 與 kind、link 只有站內網址且不用 `?city=`、
  sources 都有 `checked_on`、字數。最後一輪 **20/20、零發現**。
- 共 285 筆查證來源。每篇的查證記錄留在撰稿工作區的 `notes.md`。

### 編輯規則的三處放寬（都記在 ERRATA.md）

README 沿用第六批的字數上限比站上實際出貨嚴。撰稿者用 `pack_ingest._body_length` 量過 main：
88 篇 zh-TW `howto` 中位數 3,183、最長 4,178；17 篇 `intel` 區間 1,574 到 2,174。
協調者把上限定在 howto 4,200、intel 2,200，並把七篇退回壓縮（最長的澳門篇 5,097 壓到 4,200）。
hero 壓不進 200 KB 時照第六批的做法在 ingest 之後補壓，腳本留在 `scratchpad/write7/shrink_heroes.py`。

### 撰稿階段抓到的事實問題

`ERRATA.md` 有 19 條。影響最大的兩條：

- **越南鐵路的票價表單**：規格說它「忽略出發站」，兩位撰稿者各自實測推翻——表單其實有吃出發站。
  真正的坑是查完一次之後站別會跳回端點，畫面上看不出算的是哪一段（實測顯示 728,000，重選才拿到 143,000，差五倍）。
  兩篇都改寫成真正的坑。
- **仙台機場的定額計程車**：規格寫的 5,000 日圓在官網 HTML 裡被註解掉、畫面上看不到，現行費率是 6,500。

### 還沒做的

- [x] 部署，然後在正式站跑 `guides-import --dry-run`（確認只有這二十篇是 create）、`--publish`、
      `guides-links-rebuild`、`guides-links-check --locale zh-TW`。（二十篇已於 2026-09-17 上線；連結檢查併入
      反向連結票的主機步驟。）
- [x] 把各規格「上線後與交叉檢查」的日期事項開成票（2026-09-19 完成，24 張，見下方「日期票已開」）。
- [x] 既有文章的反向連結（同一張票）：票 `2026-09-19-batch-7-backlinks-existing-guides`。

## 釋出認領（由站主授權，2026-09-19）

claude-opus-5 應站主「整理目前所有工作狀態」處理，盤點見 `docs/work-status-2026-09-19.md`。

PR #543 於 2026-09-17 合併，二十篇都已上線：2026-09-19 查 `sitemaps/sitemap/travel-zh-TW.xml`，20／20 都在，網址形如 `/zh-TW/guides/howto/<slug>`。原持有者 claude-opus-5（2026-09-16 認領，review）。

剩下三件：部署後的 `test_guides_content_pack` 與 `pack_cli lint --kind howto`／`--kind intel`；把各規格「上線後與交叉檢查」的日期事項開成票（清單原本在某個 session 的 `scratchpad/plan7/followups.md`，可能已經不在，要從 `docs/travel-guides-batch-7/` 的規格重新整理）；既有文章的反向連結。

## 反向連結（2026-09-19，claude-fable-5-1）

既有文章的反向連結收進票 `2026-09-19-batch-7-backlinks-existing-guides`：20 份規格「上線後與交叉檢查」的
反向連結指令全部核對過，25 篇既有內容包加了 39 個 article inline；規格說不要連的（香港四天不連農曆新年篇、
Olive Young 不改、狐狸村不列）、可選而沒做的（首爾五大宮與水原的韓服段、濱海灣花園、越南換錢篇連下龍灣）、
以及兩個要等日期票刪掉的連結（連假篇連黃金週 2027-05-11、連農曆新年 2027-02-21）都寫在那張票的 Notes。
規格點名的既有文章待修（曼谷、清邁的季節月份與 PM2.5 說法）早已有專票 `2026-09-16-existing-guides-season-sources`，
沒有重做。lint 與 `test_guides_content_pack` 綠；合併後主機上的 `guides-import`（25 個 slug）、
`guides-links-rebuild`、`guides-links-check --locale zh-TW` 步驟寫在那張票的 How to verify。

### 2026-09-19 日期票已開（claude-fable-5-1 子代理）

從 `docs/travel-guides-batch-7/*.md` 二十份規格的「上線後與交叉檢查」重新整理（`scratchpad/plan7/followups.md` 已不在），所有有日期或條件觸發、規格要求開票的事項開成 24 張 `tasks/open` 票，都是 `area: docs`、未認領；2027-01-01 前到期的 P2，其餘 P3。每張票的 scope 是要改的內容包，規格說圖也要改的加上 `apps/web/public/guides/<slug>`；規格寫「同一個 PR 改」的另一篇一起列進 scope。反向連結在 `2026-09-19-batch-7-backlinks-existing-guides`（既有文章補連第七批），規格點名的既有文章待修在 `2026-09-16-existing-guides-season-sources`，都不在這 24 張裡。

- `2026-09-19-bangkok-stay-recheck-2027-01`（P3）：曼谷住宿篇 BEM 首末班、2027-01-05 BTS 時刻表（與 `bangkok-4-day-itinerary` 同 PR）、2027-01-15 聯合票價（與 `bangkok-bts-mrt-boat-guide` 同 PR）。
- `2026-09-19-chiang-rai-recheck-2026-11`（P2）：清萊篇每年 11 月前 TAT 東京景點頁、Greenbus 與六個官網恢復後補數字（清邁篇同 PR）。
- `2026-09-19-daegu-2-day-recheck-2026-12`（P2）：大邱兩天篇 2026-12-01／每年 6、12 月纜車、每年 3 月下旬西門夜市、前山纜車停駛、桐華寺與 E-World。
- `2026-09-19-daegu-airport-recheck-2026-q4`（P2）：大邱交通篇 2026-10-26 後 TW663／664、2026-12-31 前 DTRO 票價與一日券、businfo 公車。
- `2026-09-19-sr-korail-recheck-daegu-jeonju`（P3）：大邱交通篇與全州篇的 SR 票價表／時刻表改版、Korail 恢復，與 `korea-ktx-srt-ticket-guide` 同 PR。
- `2026-09-19-ha-long-recheck-2026-11`（P2）：下龍灣篇每年 4、11 月換季出港時段、每年 3 月廣寧省費率、NQ 原文、雲屯航線。
- `2026-09-19-hue-recheck-2027-01`（P3）：順化篇每年 1 月門票法規與電子售票、2027-03-01 前 HĐ 觀光列車、hueworldheritage 與 acv.vn 恢復。
- `2026-09-19-golden-week-nozomi-watch-2027`（P3）：黃金週篇 2027-01 起每月查 smart-ex.jp のぞみ公告（`japan-shinkansen-ticket-guide` 同 PR）。
- `2026-09-19-lny-links-expire-2027-02-21`（P3）：農曆新年篇過期後刪 `japan-golden-week-2027` 開頭句與 related、刪 `taiwan-long-weekends-2027-flight-planning` 2026-09-19 新增的春節區塊（農曆新年篇與黃金週篇兩份規格）。
- `2026-09-19-gw-sakura-links-expire-2027-05`（P3）：2027-05-11 `sendai-matsushima-2-day-itinerary` 拆櫻花篇連結、`taiwan-long-weekends-2027-flight-planning` 拆 2026-09-19 補的黃金週篇連結（松島篇與黃金週篇兩份規格）。
- `2026-09-19-jeonju-recheck-2027-spring`（P3）：全州篇每年春季慶基殿與南部市場夜市、kobus 與全州公車票價恢復。
- `2026-09-19-andaman-ferry-recheck-2026-11`（P2）：喀比交通篇 2026-12-01、喀比跳島篇（規格「和第 3 篇同一張票」）、普吉跳島篇每年 11 月的 Andaman Wave Master 班表，附 2026-10-15 斯米蘭開放日（可選）。
- `2026-09-19-krabi-airport-sites-2027-01`（P3）：喀比交通篇 2027-01-31 前重試機場官網與 บขส.、Grab 上車區、Tubkaek 目錄。
- `2026-09-19-dnp-park-closures-2027-01-15`（P3）：喀比跳島篇與普吉跳島篇 2027-01-15 封園總表（兩份規格互相「通知一起改」）、DNP 新收費規則（含 `chiang-mai-3-day-itinerary` 茵他儂）、皮皮特別費 400／200、翡翠池與虎穴寺。
- `2026-09-19-lny-2027-vietnam-tet-hk-lcsd`（P2）：農曆新年篇 2026-10-15 起每月查越南 Tết（最晚 2027-01-10）、2027-01 康文署新聞稿；scope 依規格只含本篇。
- `2026-09-19-macau-recheck-2027-04`（P3）：澳門篇 2027-04 年度複查、噴射飛航新網址、澳巴／新福利、輕軌東線、入境連結。
- `2026-09-19-sendai-airport-intl-2026-10`（P2）：仙台交通篇 2026-10-31 前國際線冬季班期。
- `2026-09-19-sendai-matsushima-recheck-2026-q4`（P2）：松島篇每年 10 月圓通院、11 月光のページェント與遊覽船／福浦橋／瑞巖寺、2027-01 前瑞鳳殿、丸文票價。
- `2026-09-19-zao-fox-winter-2026-11`（P2）：狐狸村篇每年 11 到 12 月冬季營業與山麓アクセス線、官網改 https。
- `2026-09-19-sendai-four-spring-2027`（P3）：仙台四篇的春季複查——2027-03-20 後空港線、2027-03-25 起立石寺、2027-03-31 前蔵王 GTFS／每年 4 月 takeyakotsu、2027-04-01 前るーぷる／地鐵／まるごとパス、JR 改正後仙石線、jreast 讀得到時四篇補票價（四篇共用數字，規格要求同 PR）。
- `2026-09-19-sentosa-recheck-2026-09`（P2）：聖淘沙篇 2026-09-19 後 Sentosa Line 維修公告、每季海灘電車與 Grab 接駁、每年票價與步道（`singapore-4-day-itinerary` block 30 同 PR）、環球影城票價、官網口徑統一。
- `2026-09-19-sea-seasons-recheck-2027-01`（P3）：季節篇 H2-3 補連越南兩篇、2027-01 TAT 東京行事曆與月份表、Air4Thai（含清邁篇）、常年值換版、`2026-09-16-existing-guides-season-sources` 改完後更新小心事項。
- `2026-09-19-sea-seasons-unlink-2028-01-01`（P3）：季節篇 2028-01-01 拆 `taiwan-long-weekends-2027-flight-planning` 連結。
- `2026-09-19-vietnam-rail-recheck-2027-01`（P3）：越南交通篇 2027-01-01 前後鐵路票價與退換票政策頁、SE1–SE8 時刻（順化篇同 PR）、航空行李規則、futabus／acv、大叻專篇上線後。

**沒開票的規格條目**（不是日期或條件複查）：各篇「合作方案在後台核准後確認 offer 畫得出來」、ingest 腳本 KNOWN 白名單與自檢、上線前的口徑對稿與照片規則。清萊篇與全州篇「上線後確認城市頁列得出本篇」的目錄缺口只寫進票的 Notes（全州篇在 `2026-09-19-jeonju-recheck-2027-spring`），還沒有人實際確認。

**含反向連結或既有文章待修條目的規格**：除狐狸村篇明寫「不列進那張票」外，其餘十九篇都有反向連結條目，都交給 `2026-09-19-batch-7-backlinks-existing-guides`。曼谷住宿篇、清萊篇、季節篇另有「既有文章待修」（`bangkok-4-day-itinerary` 5–10 月雨季、`chiang-mai-3-day-itinerary` 6–10 月雨季與「3 月最嚴重」），在 `2026-09-16-existing-guides-season-sources`；農曆新年篇另有설날口徑對齊（`taiwan-long-weekends-2027-flight-planning`「日韓同期」欄改成「韓國설 연휴 2/6–2/9（설날 2/7）」），規格說併進反向連結那張票，開票時沒有確認它做了沒有。黃金週篇與農曆新年篇的反向連結各要一張刪除票，就是上面的 `2026-09-19-gw-sakura-links-expire-2027-05` 與 `2026-09-19-lny-links-expire-2027-02-21`。
