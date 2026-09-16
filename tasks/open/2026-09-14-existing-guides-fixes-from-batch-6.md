---
id: 2026-09-14-existing-guides-fixes-from-batch-6
title: "Existing guides: facts corrected and back-links to batch 6 found while writing batch 6"
status: review
priority: P2
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-16T03:39:51Z
created_at: 2026-09-14T10:30:00Z
completed_at:
branch: claude/travel-article-structure-search-sr9jiq
depends_on:
  - 2026-09-14-launch-articles-batch-6-twenty-more
scope:
  - apps/api/app/guides/content/japan-drugstore-shopping-list.json
  - apps/api/app/guides/content/seoul-subway-t-money-guide.json
  - apps/api/app/guides/content/japan-shinkansen-ticket-guide.json
  - apps/api/app/guides/content/korea-ktx-srt-ticket-guide.json
  - apps/api/app/guides/content/da-nang-hoi-an-4-day-itinerary.json
  - apps/api/app/guides/content/seoul-4-day-itinerary.json
  - apps/api/app/guides/content/vietnam-entry-2026-evisa.json
  - apps/api/app/guides/content/thailand-esim-sim-wifi.json
  - apps/api/app/guides/content/jeju-car-rental-guide.json
  - apps/api/app/guides/content/korea-olive-young-tax-refund-shopping.json
  - apps/api/app/guides/content/korea-money-exchange-wowpass-guide.json
  - apps/api/app/guides/content/nami-island-petite-france-day-trip.json
  - apps/api/app/guides/content/korea-esim-sim-wifi.json
  - apps/api/app/guides/content/incheon-airport-to-seoul.json
  - apps/api/app/guides/content/takayama-shirakawago-day-trip.json
  - apps/api/app/guides/content/kansai-rail-passes-guide.json
  - apps/api/app/guides/content/tokyo-5-day-itinerary.json
  - apps/api/app/guides/content/kamakura-enoshima-day-trip.json
  - apps/api/app/guides/content/hong-kong-ferry-tram-day.json
  - apps/api/app/guides/content/cheung-chau-walking-day.json
  - apps/api/app/guides/content/singapore-gardens-indoor-outdoor.json
  - apps/api/app/guides/content/singapore-hawker-first-visit.json
  - apps/api/app/guides/content/hanoi-old-quarter-walking-guide.json
---

# Existing guides: facts corrected and back-links to batch 6 found while writing batch 6

## Why

The batch-6 writers and fact-checkers re-read many existing articles and the official pages
behind them. Some of those articles are now wrong or unsourced. Others should point at the new
batch-6 articles, which cover in depth what they mention in passing. Nothing here blocked the
batch-6 launch.

Block numbers are `locales.zh-TW.blocks` indexes on 2026-09-14. Re-find each block by the
quoted text if it has moved.

## Definition of done

- [x] Every correction below is checked against the evidence page on the day of the edit, then
      applied or dismissed with a reason in Notes.
- [x] The back-links below are added. Link text says what the target actually covers. No
      how-to links an intel notice that expires within its reading period.
- [ ] `uv run pytest tests/test_guides_content_pack.py -q` passes, and the host import shows only
      the edited articles as `update`.

## Steps

### Corrections

- [x] `japan-drugstore-shopping-list` block 28 says 「生理用品 120 片」 and 「（每半年一次）」.
  - The customs page says 「衛生棉條合計不超過 120 個」.
  - The once-per-six-months limit applies only to post and express shipments, not to
    travellers' own luggage (特定醫療器材專案核准製造及輸入辦法第 6 條).
  - Evidence: https://web.customs.gov.tw/taipei/singlehtml/3392?cntId=cus2_3392_3392_1347
    and https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=L0030119
- [x] `seoul-subway-t-money-guide` block 19 says the Climate Card covers 「京義中央線…首爾市內區段」.
  - The official range for the Gyeongui–Jungang Line is 탄현~양원/서울역.
  - The page also carries a notice that the 30-day pass is ending; block 18 quotes the 30-day
    price.
  - Evidence: https://news.seoul.go.kr/traffic/archives/510651
- [x] `japan-shinkansen-ticket-guide` block 5 attributes the list of all-reserved Nozomi periods
  to JR Central's timetable page. That page only says "major peak periods".
  - The periods come from the JR Central / JR West PDF of 2026-05-21.
  - The same PDF adds four three-day weekends: 2026/10/10–12, 11/21–23, 2027/1/9–11 and 3/20–22.
  - Evidence: https://jr-central.co.jp/news/release/_pdf/000045592.pdf
- [x] `korea-ktx-srt-ticket-guide` block 12, 「春節、中秋前後韓國人會在開放預訂當天搶票」, has no source.
  - Korail's 2026-08-14 release gives a separate holiday booking window on a dedicated page.
  - The same release says only integrated rail members can book and SR members must convert
    first. Re-check the SRT app and membership advice in block 10.
  - Evidence: https://info.korail.com/info/selectBbsNttView.do?bbsNo=199&key=911&nttNo=27180
- [x] `da-nang-hoi-an-4-day-itinerary` block 24 says 「帶美金到市區換錢所換」 and 「可綁信用卡或付現」.
  - Decree 340/2025/NĐ-CP (effective 2026-02-09) fines exchange at unauthorised points and
    between individuals. Write 「到銀行或合法兌換處換」; do not write "gold shops are illegal".
  - Grab Vietnam's Pay page lists only Moca, saved bank cards and international cards. Write
    「現金以 App 為準」.
  - Wording must match `vietnam-money-sim-grab-guide`.
  - Evidence: https://baochinhphu.vn/ca-nhan-mua-ban-vang-mieng-voi-to-chuc-khong-co-giay-phep-se-bi-phat-toi-20-trieu-dong-102251229162503718.htm
    and https://www.grab.com/vn/en/pay/
- [x] `seoul-4-day-itinerary` block 21 says the Hwaseong Eocha saves walking the whole wall and
  goes via the palace.
  - The Eocha starts at Yeonmudae and runs via Hwahongmun, Janganmun, Hwaseomun and Maehyanggyo,
    not the palace or Paldalmun.
  - Buses 60 and 7-2 leave from Suwon Station exit 7.
  - Delete the 「2026 年 9 月官網有路線縮短與暫停營運的公告」 sentence after 2026-10-14.
  - Evidence: https://www.swcf.or.kr/?p=68
- [x] `vietnam-entry-2026-evisa` block 15 gives Tan Son Nhat international flights at T2, but
  its only source is a pre-T3 page.
  - Add the government portal report of 2025-04-17: T3 opened for domestic flights, and T2
    stays international.
  - Evidence: https://tphcm.chinhphu.vn/nha-ga-t3-hien-dai-nhat-ca-nuoc-khai-thac-chuyen-bay-thuong-mai-dau-tien-101250417091116059.htm
- [x] `thailand-esim-sim-wifi` block 19, 「Grab 用台灣門號註冊就能叫車」, has no official page.
  Soften to 「台灣門號能否註冊以 App 當下為準」, or cite one.
- [x] `jeju-car-rental-guide` says Google Maps cannot navigate driving routes in Korea.
  - The government gave conditional approval on 2026-02-27 to export 1:5000 map data, with
    verification still pending.
  - Write 「不完整、以 App 當下為準」.
  - Evidence: https://www.korea.kr/news/policyNewsView.do?newsId=148960107
- [x] `korea-olive-young-tax-refund-shopping` block 16 says 「看的是容器標示的容量」. The CAA
  wording is container volume, not the label. Low priority.
  - Evidence: https://www.caa.gov.tw/Article.aspx?a=1398&lang=1
- [x] `korea-money-exchange-wowpass-guide` block 25, 「不用小費」, has no source. VisitKorea's taxi
  page supports it; cite that page for tipping and payment only, not for fares.
  - Evidence: https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=140661

### Back-links (target first, then where it goes and suggested link text)

- [x] `suwon-hwaseong-day-trip` ← `seoul-4-day-itinerary`, after block 21 (plan B); do it with
  the correction above. Link text 「水原華城一日遊：怎麼去、行宮門票、城牆與華城御車」.
- [x] `dmz-day-trip-from-seoul` ← `seoul-4-day-itinerary`, in the Day 3 day-trip section.
  - Add 「也可以換成 DMZ（週一休館）」 first.
- [x] `dmz-day-trip-from-seoul` ← `nami-island-petite-france-day-trip`, in the closing links;
  optionally also link `suwon-hwaseong-day-trip`.
- [x] `korea-naver-map-kakao-t-guide` ← four articles:
  - `seoul-subway-t-money-guide`, the map app section around block 26
  - `korea-esim-sim-wifi`, the "which apps need a Korean number" section around block 23
  - `korea-money-exchange-wowpass-guide`, after the taxi sentence in block 25
  - `incheon-airport-to-seoul`, the taxi section around blocks 23–24
- [x] `kanazawa-2-day-itinerary` ← three articles:
  - `takayama-shirakawago-day-trip`, after block 8. Also fix the block-28 link text 「從金澤搭北陸新幹線的票怎麼買」, which oversells the target.
  - `kansai-rail-passes-guide`, in the JR pass section (blocks 5–8)
  - `japan-shinkansen-ticket-guide`, after block 4, item 3
- [x] `yokohama-day-trip-from-tokyo` ← two articles:
  - `tokyo-5-day-itinerary`, after 「橫濱的中華街與港未來」 in block 14
  - `kamakura-enoshima-day-trip`, after block 3
- [x] `hong-kong-4-day-itinerary` ← `hong-kong-ferry-tram-day` and `cheung-chau-walking-day`, at
  the end of each.
- [x] `singapore-4-day-itinerary` and `singapore-changi-airport-mrt-simplygo-guide` ←
  `singapore-gardens-indoor-outdoor` and `singapore-hawker-first-visit`.
- [x] `hanoi-4-day-itinerary` ← `hanoi-old-quarter-walking-guide`, at the end.
- [x] `hanoi-4-day-itinerary`, `ho-chi-minh-city-4-day-itinerary` and `vietnam-money-sim-grab-guide` ←
  `da-nang-hoi-an-4-day-itinerary`, block 24 list and closing links.
- [x] `hanoi-4-day-itinerary`, `ho-chi-minh-city-4-day-itinerary` and `vietnam-money-sim-grab-guide` ←
  `vietnam-entry-2026-evisa`, blocks 15–16.
- [x] `hong-kong-entry-2026` and `singapore-entry-2026-sg-arrival-card` ← `vietnam-entry-2026-evisa`,
  the closing entry-rules links. All three expire 2027-03-31.
- [x] `phuket-airport-transport-where-to-stay` ← `thailand-esim-sim-wifi`, after the last item of
  block 27.
- [x] `return-to-taiwan-customs-duty-free-guide` ← `korea-olive-young-tax-refund-shopping`
  (blocks 15–17) and `japan-drugstore-shopping-list` (blocks 27–30).

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
uv run python -m app.guides.pack_cli lint --kind howto
```

## Notes

- Consolidated on 2026-09-14 from the batch-6 writing workflow: writer notes, two fact-check
  rounds and the cross-article reconciliation.
- Deliberately not included:
  - Tobacco Act penalty wording in `taiwan-etiquette-safety-tips` / `taiwan-entry-2026-arrival-card`.
    It only changes after the amendment's third reading, and is tracked in
    `2026-09-14-batch-6-guides-dated-maintenance`.
  - An optional 「21:30 閉門」 addition to `osaka-kyoto-nara-4-day-itinerary`, which is not wrong today.
- 2026-09-16 全部套用（分支 `claude/travel-article-structure-search-sr9jiq`），證據頁當天用 WebFetch 重查；
  `jr-central.co.jp` 對 WebFetch 回 403，新聞稿 PDF 改用 curl 下載後以 pypdf 讀。逐條：
  - `japan-drugstore-shopping-list`：applied。關務署頁寫「衛生棉條合計不超過120個」；法規第 6 條第 5 項
    「除入境旅客自行攜入者外，其經便捷通關方式輸入之次數，以每半年一次為限」。block 28 改成衛生棉條 120 個、
    說明每半年一次只管郵寄快遞；加法規來源（18 筆）。
  - `seoul-subway-t-money-guide`：applied。官網寫 경의중앙선 탄현~양원/서울역、4호선 정부과천청사~진접、
    7호선 온수~장암、공항철도 김포공항~서울역；頁上有「기후동행카드 30일권 운영 종료 안내」，結束日期在
    連結裡沒抓到，block 18 只寫「掛著結束營運的公告，日期以公告為準」。
  - `japan-shinkansen-ticket-guide`：applied。2026-05-21 新聞稿列的期間：黃金週 4/24–5/6、盂蘭盆 8/7–16、
    白銀週 9/18–23、年末年始 12/25–1/5，新增三連休 10/10–12、11/21–23、2027/1/9–11、3/20–22；block 5
    改引新聞稿並列出全部日期，時刻表頁來源改題「沒有列日期」，PDF 加進來源（19 筆）。
  - `korea-ktx-srt-ticket-guide`：applied。Korail 2026-08-14 公告：9/23–27 車票、交通弱勢 9/3–4、一般
    9/7–11、專用網頁、「이번 추석 예매는 코레일 '통합 회원'만 가능」、SR 會員要先轉換。block 12 以 2026
    中秋為例改寫，block 10 末尾補一句整合會員；來源加公告（12 筆）。
  - `da-nang-hoi-an-4-day-itinerary`：applied。措辭對齊 `vietnam-money-sim-grab-guide`：「銀行或獲准的兌換處」、
    「罰的是在未獲准的地方換錢與個人之間換錢」，沒寫金店違法；Grab 付款頁只列 Moca、已存銀行卡、國際信用卡
    或金融卡（頁上「cash」只出現在推無現金的文案），寫「現金以 App 為準」。加兩筆來源（19 筆）。
  - `seoul-4-day-itinerary`：applied。御車頁：연무대 → 화홍문 → 장안문 → 화서문 → 매향교 → 연무대，
    「2024년 3월 11일부터 관광형 노선(화성행궁 출발) 폐지」，매주 월요일 휴무；p=68 頁寫 수원역 7번 출구
    AK플라자 정류장 60、7-2번。來源已滿 20 筆：拿掉 서울시 내 손안에 서울 那筆（與 종로문화플랫폼 同樣只撐
    北村 10:00–17:00 這條）換成御車頁；公車出口那句沒寫進正文（沒有第二個來源位子），改寫「哪個出口搭哪班
    公車看下面那篇」並緊接水原一日遊連結。「2026 年 9 月官網有路線縮短與暫停營運的公告」留到 2026-10-14
    再刪（水原篇 block 22 有日期：9/16–10/3 縮短、10/4–11 停駛、10/13 恢復）。
  - `vietnam-entry-2026-evisa`：applied。政府入口網 2025-04-17：「ga hành khách quốc nội T3 … chuyến bay
    thương mại đầu tiên mang số hiệu VN1286」、「Nhà ga T2 tiếp tục đảm nhiệm chức năng phục vụ các chuyến
    bay quốc tế như trước」。加來源（16 筆）。
  - `thailand-esim-sim-wifi`：applied，改成「能不能用台灣門號註冊以 App 當下為準」，沒有可引的官方頁。
  - `jeju-car-rental-guide`：applied。정책브리핑 2026-02-27：「엄격한 보안 조건 준수를 전제로 반출 허가 결정」、
    「간행 심사 등 정부 검토·확인을 거친 데이터만 반출」、「조건 불이행 등 경우 허가를 중단·회수」。加來源（8 筆）。
  - `korea-olive-young-tax-refund-shopping`：applied 措辭（「看的是容器的容量」）。民航局頁對 WebFetch 只列出
    下載檔、抓不到條文字句，沒加來源；100 毫升那條本來就引仁川機場頁。
  - `korea-money-exchange-wowpass-guide`：applied。VisitKorea Taxi 頁：「don't require tips」、「cash, credit
    card, or transportation card」；來源標題改成只涵蓋小費與付款（頁上雖有 4,800 起跳，照票的要求不拿它引票價）。
    起跳價留在正文，緊接的回連 `korea-naver-map-kakao-t-guide` 那篇引首爾市頁。
  - 回連 14 組全部加上，都是 `rich_paragraph` 的 `article` inline，文字寫目標實際涵蓋的內容，兩篇入境情報
    用 `kind: intel`（效期都到 2027-03-31）：`seoul-4-day`（水原、DMZ）、`nami`（DMZ、水原）、
    `korea-naver-map` ← `seoul-subway`／`korea-esim`／`korea-money-exchange`／`incheon`、`kanazawa` ←
    `takayama`（並把 block 28 連結文字改成新幹線篇實際內容）／`kansai-rail-passes`／`japan-shinkansen`、
    `yokohama` ← `tokyo-5-day`／`kamakura`、`hong-kong-4-day` ← 兩篇香港、`singapore-4-day`＋`changi` ←
    兩篇新加坡、`hanoi-4-day` ← `hanoi-old-quarter`、三篇越南 ← `da-nang`、`vietnam-entry`、兩篇入境 ←
    `vietnam-entry`、`phuket` ← `thailand-esim`、`return-to-taiwan` ← `olive-young`、`japan-drugstore`。
  - 驗證：`pack_cli lint --slug` ×23 只剩 7 篇本來就有的 `diagram_number_not_in_text`／`svg_small_label`
    error，沒有新的 error code；`test_guides_content_pack.py`、`test_guides_content_links.py` 通過。
    主機 `guides-import --dry-run` 應只列這 23 篇 zh-TW `update`，部署時再確認。
