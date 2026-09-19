---
id: 2026-09-14-answer-first-howto-descriptions
title: AIO: 68 how-to descriptions enumerate topics instead of answering
status: review
priority: P3
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-19T11:15:21Z
created_at: 2026-09-14T13:48:24Z
completed_at:
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - apps/api/app/guides/content/busan-3-day-itinerary.json
  - apps/api/app/guides/content/dmz-day-trip-from-seoul.json
  - apps/api/app/guides/content/fuji-kawaguchiko-day-trip.json
  - apps/api/app/guides/content/fukuoka-airport-to-hakata-tenjin.json
  - apps/api/app/guides/content/gimhae-airport-to-busan.json
  - apps/api/app/guides/content/hakone-day-trip-free-pass.json
  - apps/api/app/guides/content/himeji-castle-day-trip.json
  - apps/api/app/guides/content/hiroshima-miyajima-2-day.json
  - apps/api/app/guides/content/incheon-airport-to-seoul.json
  - apps/api/app/guides/content/japan-drugstore-shopping-list.json
  - apps/api/app/guides/content/japan-entry-2026-visit-japan-web.json
  - apps/api/app/guides/content/japan-esim-sim-wifi.json
  - apps/api/app/guides/content/japan-ic-card-suica-icoca-guide.json
  - apps/api/app/guides/content/japan-ski-season-2026-2027.json
  - apps/api/app/guides/content/japan-winter-illumination-2026.json
  - apps/api/app/guides/content/japan-year-end-new-year-2026-2027.json
  - apps/api/app/guides/content/jeju-3-day-itinerary.json
  - apps/api/app/guides/content/kamakura-enoshima-day-trip.json
  - apps/api/app/guides/content/kobe-arima-day-trip.json
  - apps/api/app/guides/content/korea-entry-2026-k-eta-e-arrival.json
  - apps/api/app/guides/content/korea-esim-sim-wifi.json
  - apps/api/app/guides/content/korea-money-exchange-wowpass-guide.json
  - apps/api/app/guides/content/korea-olive-young-tax-refund-shopping.json
  - apps/api/app/guides/content/nagoya-3-day-itinerary.json
  - apps/api/app/guides/content/narita-haneda-to-tokyo.json
  - apps/api/app/guides/content/new-chitose-airport-to-sapporo.json
  - apps/api/app/guides/content/okinawa-4-day-itinerary.json
  - apps/api/app/guides/content/osaka-kyoto-where-to-stay.json
  - apps/api/app/guides/content/sapporo-snow-festival-2027.json
  - apps/api/app/guides/content/seoul-4-day-itinerary.json
  - apps/api/app/guides/content/seoul-palaces-hanbok-guide.json
  - apps/api/app/guides/content/seoul-subway-t-money-guide.json
  - apps/api/app/guides/content/suwon-hwaseong-day-trip.json
  - apps/api/app/guides/content/takayama-shirakawago-day-trip.json
  - apps/api/app/guides/content/tokyo-5-day-itinerary.json
  - apps/api/app/guides/content/tokyo-disney-guide.json
  - apps/api/app/guides/content/tokyo-transit-passes.json
  - apps/api/app/guides/content/tokyo-where-to-stay.json
  - apps/api/app/guides/content/yokohama-day-trip-from-tokyo.json
---

# AIO: 68 how-to descriptions enumerate topics instead of answering

## Why

`description` is what an AI answer engine quotes when it summarizes a page, and 68 of the
site's descriptions assert nothing it can lift.

Measured across all 498 localized documents: 72 descriptions are a single sentence containing
three or more `、` separators — a noun-phrase list with no predicate — and 60 of those are
`howto`, plus 8 `intel`. `seoul-subway-t-money-guide`'s 235-character description enumerates
「計費方式、30 分鐘免費轉乘規則、T-money 在哪裡買、怎麼儲值與退款」 and states no fact.

These are the fare-and-timetable pages where the site has its highest-value numbers and its
densest citations (howto carries a median of 19 sources), so they are exactly the pages losing
the extraction. The fix is cheap because the answer is already one block below: every document
opens with a paragraph, and the howto first paragraphs are already answer-first.

## Definition of done

- [x] Each rewritten description opens with a one-sentence answer carrying the number, then the
      enumeration, then the provenance clause these descriptions already use.
- [x] No fact is introduced that the article body does not already state and source.

## Steps

- [x] Select the targets by the measured rule: splits into exactly one sentence on
      `/(?<=[。.])/` **and** contains at least three `、`. That is the 60 howto + 8 intel.
- [x] Rewrite by hand, lifting the lead from the document's own first paragraph.
- [x] Split the work by kind or destination so one task does not hold all of
      `apps/api/app/guides/content` — several models work the same queue.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_content_pack.py
```

Spot-check that the new first sentence matches a number the body states and a source backs.

## Notes

**Do not automate the rewrite.** A generated first sentence that states a fare wrongly is the
one failure mode worse than a teaser: it is the sentence an answer engine caches and repeats.

Changing `description` changes both the meta description and the JSON-LD `description`, so this
is a live SEO change on 68 pages, not a silent one. The facts being promoted — fares, minutes —
are also the most perishable content on the site.

### 2026-09-19 split (claude-fable-5-1)

Re-measured with the ticket's rule on 2026-09-19: 72 howto/intel localized documents (64 howto, 8 intel;
the 35 life ones are a different shape — mostly the short ja descriptions of the codex series — and stay
out). This ticket now holds the 39 Japan/Korea documents listed in its scope; the other 33 (Southeast
Asia, Taiwan, Hong Kong/Macau/Singapore, USJ) are `2026-09-19-aio-answer-first-descriptions-part-2`, so
two writers can work at once and neither holds the whole content directory. Per-document current
descriptions were measured into a tab-separated list at the time; re-run the rule rather than trusting it.

### 2026-09-19 done in repo (claude-fable-5-1)

All 39 documents in scope rewritten by hand, one at a time, in the working tree (not committed):
each new `description` opens with one sentence that answers the page's question with a number or
fact lifted from the document's own first paragraph or its first table, then keeps the enumeration
of what the article covers, then the provenance clause the old description already carried
(查證日期／官方來源 wording unchanged). Only `locales["zh-TW"].description` changed in each pack;
every file round-trips byte-identically through `json.dumps(obj, ensure_ascii=False, indent=2) + "\n"`,
and `git diff --numstat` shows exactly one line replaced per file. No sentence was generated: the
only automation was a checker that confirmed every numeric token of each new description appears
digit for digit in that document's blocks, that the provenance clause is still present, and the
length. Lengths went from 115–292 (median 188) to 178–200 (median 197); the 18 originals longer than
200 all came down to 200 or less.

14 old descriptions did not end with the provenance clause (it sat at the start or in the
middle: `japan-drugstore-shopping-list`, `japan-entry-2026-visit-japan-web`, `japan-esim-sim-wifi`, `japan-ski-season-2026-2027`, `japan-winter-illumination-2026`, `japan-year-end-new-year-2026-2027`, `korea-esim-sim-wifi`, `korea-olive-young-tax-refund-shopping`, `narita-haneda-to-tokyo`, `okinawa-4-day-itinerary`, `osaka-kyoto-where-to-stay`, `tokyo-disney-guide`, `tokyo-transit-passes`, `yokohama-day-trip-from-tokyo`); the same wording now closes the description. Two had no dated 查證 clause at all (`japan-drugstore-shopping-list`, `japan-esim-sim-wifi`): those now end with the
date and sources the document's own first paragraph states, nothing new. `1.5%` and `go.kr` (which the ticket's `.` split would cut) sit in the
enumeration, never in the answer sentence.

Validation, run after the edit:

```
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q   # 9 passed, 5 skipped
uv run python -m app.guides.pack_cli lint --kind howto   # 167 warnings, 29 errors before and after, identical output
uv run python -m app.guides.pack_cli lint --kind intel   # 2 warnings, 6 errors before and after, identical output
```

The lint exit code is 1 before and after because of pre-existing `diagram_number_not_in_text` and
`text_length` findings on other documents; this change adds no new warning or error.

Spot-check of five documents drawn at random (seed 20260919), first sentence against body and sources:

- `himeji-castle-day-trip`: 2,500 日圓 (2026-03-01 起) and 每小時 1,000 人 are in the opening paragraph
  and the 入城料 section, backed by 姫路城公式サイト 縦覧料 and ご利用案内; 57／1 小時 25／37 分 are in the
  transport table, backed by 姫路観光ナビ アクセス.
- `korea-olive-young-tax-refund-shopping`: 15,000 到 1,000,000 韓元 and 5,000,000 韓元 are in the
  即時退稅 section and the comparison table, backed by VisitKorea Duty Free & Tax Refunds and Visit Seoul Tax Refund.
- `incheon-airport-to-seoul`: T1 43 分／T2 51 分／13,000 韓元 are in the comparison table and 直達列車
  section (공항철도 직통열차 안내); 4,650 韓元 to 弘大入口 is in the 一般列車 section (공항철도 일반열차 운임);
  17,000 韓元 and 6001／6015／6002 are in the bus table (공항리무진 6001／6015／6002 노선).
- `korea-money-exchange-wowpass-guide`: 100,000 到 200,000 韓元 is in the tip callout and decision tree;
  發卡費 6,000 韓元 and 0 手續費 are in the comparison table and WOWPASS section (WOWPASS 官網 常見問題).
- `new-chitose-airport-to-sapporo`: 37／33 分, 1,230 日圓 and 每小時 6 班 are in the opening paragraph
  and table (JR北海道 快速エアポート); 1,500 日圓 and 65 到 80 分 are in the bus section (北都交通 時刻表).

| file | locale | old → new | new first sentence |
| --- | --- | --- | --- |
| `busan-3-day-itinerary.json` | zh-TW | 181 → 194 | 釜山三天兩夜這樣排：Day 1 海雲台與廣安里夜景，Day 2 用 1 號線串甘川文化村、札嘎其市場、南浦洞與龍頭山，Day 3 松島海上纜車或海東龍宮寺，下午 Blueline Park 天空膠囊或海岸列車再去機場；地鐵刷卡 1 區間 1,600 韓元，1 日券 6,000 韓元一天搭不到四趟不用買。 |
| `dmz-day-trip-from-seoul.json` | zh-TW | 189 → 192 | 坡州 DMZ 和平觀光自己去，一般票單軌 12,200、步行 9,200 韓元，臨津閣售票處 09:00 到 14:30 發券，週一與平日國定假日休館，板門店 JSA 目前不受理外國人見學。 |
| `fuji-kawaguchiko-day-trip.json` | zh-TW | 254 → 198 | 新宿到河口湖三種走法：高速巴士約 1 小時 45 分、2,000 到 2,200 日圓，特急富士回遊約 1 小時 54 分、4,200 日圓，中央線大月轉富士急行線 2,580 日圓。 |
| `fukuoka-airport-to-hakata-tenjin.json` | zh-TW | 164 → 187 | 福岡機場國際線進市區最便宜是搭免費連絡巴士到國內線再轉地下鐵空港線，2 站到博多、5 站到天神都是 260 日圓；不想轉車就搭西鐵直達巴士，博多站筑紫口 400 日圓、天神 500 日圓。 |
| `gimhae-airport-to-busan.json` | zh-TW | 161 → 200 | 金海機場進釜山最便宜是釜山金海輕軌到沙上轉 2 號線，交通卡 1,600 韓元起、到海雲台 1,800 韓元；利木津巴士西面線 6,000、海雲台線 9,500 韓元只收信用卡，末班 21:30 與 21:40 從機場發車。 |
| `hakone-day-trip-free-pass.json` | zh-TW | 218 → 192 | 新宿出發繞完箱根黃金路線一圈，箱根周遊券 2 日 7,100 日圓一定划算：山內五段單程票加起來 5,810 日圓，加上小田原到湯本與新宿來回車資就超過票價，浪漫特快特急券另加 1,200 日圓、約 80 分鐘。 |
| `himeji-castle-day-trip.json` | zh-TW | 221 → 196 | 姬路城 2026 年 3 月 1 日起市外訪客入城料 2,500 日圓，大天守每小時只放 1,000 人登城；從大阪搭 JR 新快速約 57 分、京都約 1 小時 25 分、三ノ宮約 37 分。 |
| `hiroshima-miyajima-2-day.json` | zh-TW | 206 → 199 | 廣島宮島兩天一夜：Day 1 和平紀念公園、原爆圓頂、資料館（200 日圓）與廣島燒，Day 2 JR 到宮島口約 28 分、420 日圓，轉 JR 宮島渡輪 200 日圓加宮島訪問稅 100 日圓看嚴島神社。 |
| `incheon-airport-to-seoul.json` | zh-TW | 150 → 198 | 仁川機場到首爾站最快是 AREX 直達列車，T1 43 分、T2 51 分、13,000 韓元；住弘大搭一般列車刷 T-money 最便宜，T1 到弘大入口 4,650 韓元；6001／6015／6002 機場巴士到明洞、首爾站、弘大 17,000 韓元。 |
| `japan-drugstore-shopping-list.json` | zh-TW | 117 → 198 | 日本藥妝免稅門檻是同一家店同一天未稅 5,000 日圓，2026 年 11 月 1 日起改成先付含稅價、出境後退款；5 月 1 日起含六種成分的感冒藥、止咳藥限購，回台灣的非處方藥每種最多 12 瓶、合計 36 瓶。 |
| `japan-entry-2026-visit-japan-web.json` | zh-TW | 164 → 193 | 台灣護照入境日本免簽 90 天、不用申請任何電子許可，用免費的 Visit Japan Web 產生一個 QR 碼就能同時辦入境審查與海關申報；JESTA 電子渡航認證目標 2028 年度才上路。 |
| `japan-esim-sim-wifi.json` | zh-TW | 131 → 192 | 去日本上網，手機支援 eSIM（iPhone XS、XR 以後）且已解鎖的 1 到 2 人選 eSIM，3 人以上或要開熱點選 WiFi 分享器，手機不支援 eSIM 才到機場買實體 SIM。 |
| `japan-ic-card-suica-icoca-guide.json` | zh-TW | 292 → 189 | 日本交通 IC 卡十張全國互通、辦一張就夠：東京進出買 28 天免押金的 Welcome Suica，iPhone 在錢包 App 加 Suica，關西進出想留卡買 ICOCA 2,000 日圓含押金 500。 |
| `japan-ski-season-2026-2027.json` | zh-TW | 269 → 198 | 2026–27 雪季 Niseko United 2026 年 11 月 28 日開放，全山券旺季一日 13,500 日圓，留壽都同日開放、正季一日券 16,700 日圓，白馬 Valley 全山一日券 11,100 日圓，GALA 湯澤尚未公告。 |
| `japan-winter-illumination-2026.json` | zh-TW | 135 → 178 | 2026 年 9 月 13 日查證時只有神戶光雕（2027 年 1 月 29 日到 2 月 7 日）與讀賣樂園（2026 年 10 月 29 日到 2027 年 4 月 4 日）公布了新檔期，東京丸之內、六本木、大阪御堂筋等都還只能先看 2025 年。 |
| `japan-year-end-new-year-2026-2027.json` | zh-TW | 230 → 199 | 2026 年 12 月 26 日到 2027 年 1 月 4 日在日本，官公廳 12 月 29 日到 1 月 3 日休、銀行 12 月 31 日到 1 月 3 日休、のぞみ 12 月 25 日到 1 月 5 日全席指定席、百貨 1 月 1 日休業、1 月 2 日初売り。 |
| `jeju-3-day-itinerary.json` | zh-TW | 154 → 197 | 濟州三天兩夜照 Day 1 濟州市區、Day 2 東線、Day 3 西歸浦或漢拿山排最順，台灣國際駕照 2022 年 2 月起在韓國能租車自駕，搭巴士間線刷卡 1,150 韓元、急行基本 2,000 韓元。 |
| `kamakura-enoshima-day-trip.json` | zh-TW | 214 → 195 | 從新宿玩鎌倉、江之島買小田急「江の島・鎌倉フリーパス」1,640 日圓，含新宿到藤澤來回與江之電全線無限搭；住東京車站、品川走 JR 橫須賀線直達北鎌倉約 1 小時，江之電一日券のりおりくん 800 日圓。 |
| `kobe-arima-day-trip.json` | zh-TW | 143 → 199 | 大阪到神戶三宮搭 JR 新快速約 20 分、阪急或阪神特急約 30 分，都不加特急費；三宮到有馬溫泉地鐵轉神戶電鐵約 30 分（谷上到有馬溫泉 440 日圓）或 JR 巴士 780 日圓，金の湯 800、銀の湯 700 日圓。 |
| `korea-entry-2026-k-eta-e-arrival.json` | zh-TW | 181 → 190 | 台灣護照入境韓國到 2026 年 12 月 31 日都免辦 K-ETA，只要在抵達前 3 天內到官網免費填好 e-Arrival Card 電子入境卡，海關只有帶申報物品的人才要用「여행자 세관신고」App 申報。 |
| `korea-esim-sim-wifi.json` | zh-TW | 208 → 196 | 去韓國上網，手機支援 eSIM 且已解鎖的 1 到 2 人選 eSIM，3 人以上選 WiFi 分享器，不能用 eSIM 就到仁川機場買實體 SIM，兩個航廈的入境層都有 24 小時電信櫃檯。 |
| `korea-money-exchange-wowpass-guide.json` | zh-TW | 206 → 195 | 去韓國吃餐廳、逛商場為主的人信用卡當主力，在台灣只換 100,000 到 200,000 韓元現鈔；待 4 天以上的人落地辦 WOWPASS，發卡費 6,000 韓元、換匯與付款 0 手續費。 |
| `korea-olive-young-tax-refund-shopping.json` | zh-TW | 216 → 188 | Olive Young 結帳出示護照就能即時退稅：單筆 15,000 到 1,000,000 韓元當場扣稅，全程累計上限 5,000,000 韓元，超過的拿退稅單到仁川機場辦。 |
| `nagoya-3-day-itinerary.json` | zh-TW | 212 → 200 | 名古屋三天兩夜：中部國際機場搭名鐵 μ-SKY 28 分鐘進城（運賃 980 日圓加 μ 票 450 日圓，特急 36 分不加價），Day 1 名古屋城、榮、大須，Day 2 熱田神宮、鰻魚飯三吃、磁浮鐵道館，Day 3 犬山或名古屋站周邊再回機場。 |
| `narita-haneda-to-tokyo.json` | zh-TW | 134 → 198 | 成田進東京，住上野搭京成 Skyliner 36 到 41 分、2,580 日圓，住新宿、東京車站搭 JR N'EX 東京最快 53 分、3,140 日圓，預算優先搭 TYO-NRT 巴士 1,500 日圓；羽田搭京急到品川 11 到 14 分、330 日圓。 |
| `new-chitose-airport-to-sapporo.json` | zh-TW | 229 → 199 | 新千歲機場到札幌站搭 JR 快速 Airport 最快 37 分、特別快速 33 分，1,230 日圓、白天每小時 6 班；住薄野、中島公園搭機場巴士 1,500 日圓直達飯店，約 65 到 80 分。 |
| `okinawa-4-day-itinerary.json` | zh-TW | 162 → 187 | 沖繩四天三夜第一天不租車，用單軌一日券 1,000 日圓走國際通與首里城，第二天起租車跑美國村、萬座毛，第三天美麗海水族館（成人 2,180 日圓、那霸機場開車約 2 小時）與古宇利大橋，第四天瀨長島再還車回那霸機場。 |
| `osaka-kyoto-where-to-stay.json` | zh-TW | 115 → 195 | 第一次去關西、行程以大阪為主住難波或梅田，帶小孩或預算有限住天王寺；京都要跑很多景點、拖大行李住京都站，想走路逛街吃東西住河原町，想住町家旅館住祇園，大阪到京都搭阪急特急 43 分鐘、京阪特急約 40 分鐘。 |
| `sapporo-snow-festival-2027.json` | zh-TW | 206 → 193 | 第 77 屆さっぽろ雪まつり官網已公告 2027 年 2 月 4 日到 11 日舉行，大通、すすきの、つどーむ三會場同一期間、入場免費。 |
| `seoul-4-day-itinerary.json` | zh-TW | 188 → 198 | 首爾四天三夜這樣排：Day 1 明洞與南山首爾塔，Day 2 景福宮（成人 3,000 韓元、穿整套韓服免門票、週二休）、北村韓屋村（觀光時段只到 17:00）、仁寺洞、廣藏市場，Day 3 南怡島加江村鐵道自行車或改水原華城，Day 4 弘大延南或聖水漢江再去機場。 |
| `seoul-palaces-hanbok-guide.json` | zh-TW | 214 → 198 | 首爾景福宮、昌德宮成人門票各 3,000 韓元，昌慶宮、德壽宮與宗廟各 1,000 韓元，綜合觀覽券 6,000 韓元比五張單票 9,000 韓元便宜，穿整套韓服全部免費；景福宮、宗廟週二休，其他三座週一休。 |
| `seoul-subway-t-money-guide.json` | zh-TW | 235 → 197 | 首爾地鐵成人刷卡基本票價 1,550 韓元，30 分鐘內轉乘免費，Climate Card 1 日券 5,000 韓元要一天搭 4 趟才回本。 |
| `suwon-hwaseong-day-trip.json` | zh-TW | 165 → 198 | 首爾到水原華城搭地鐵 1 號線到水原站轉公車，或從江南站搭 3000、蠶室站搭 1007 直行巴士；城牆周長 5,744 公尺免費全年開放，華城行宮成人 2,000 韓元、17:00 停止入場、穿韓服免費，華城御車成人 6,000 韓元、每週一休。 |
| `takayama-shirakawago-day-trip.json` | zh-TW | 241 → 200 | 名古屋到高山搭 JR 特急ひだ 約 140 分（特急券 2,730 日圓加乘車券）或高速巴士約 2 小時 45 分、3,600 日圓，高山到白川鄉只有濃飛巴士約 50 分、2,800 日圓要預約，一日來回二選一，兩天一夜才能都逛。 |
| `tokyo-5-day-itinerary.json` | zh-TW | 115 → 197 | 東京五天四夜一天一區：Day 1 新宿，Day 2 淺草、上野，Day 3 築地、豐洲 teamLab、銀座，Day 4 明治神宮、原宿、表參道，Day 5 採買去機場；住新宿從成田搭 N'EX 3,330 日圓，加買 Tokyo Subway Ticket 72 小時券 2,000 日圓。 |
| `tokyo-disney-guide.json` | zh-TW | 187 → 197 | 東京迪士尼一日護照浮動票價，2026 年 9 月平日多為 9,900 日圓、週末 10,900 日圓，官網每天 14:00 開賣兩個月後同一天的票；免費的優先通行卡已不在官網服務清單，縮短排隊只剩付費的尊享卡（每人每次 1,000 到 3,500 日圓）。 |
| `tokyo-transit-passes.json` | zh-TW | 173 → 192 | 第一次去東京每個人先有一張 IC 卡逐次刷（Welcome Suica 免押金、28 天），一天搭四趟以上地鐵再加買 Tokyo Subway Ticket 72 小時券 2,000 日圓，只玩東京不去關西 JR Pass 一定不划算。 |
| `tokyo-where-to-stay.json` | zh-TW | 140 → 197 | 東京第一次來、想去的地方分散住新宿或東京車站，從成田進出想少轉車住上野（Skyliner 41 分直達），帶小孩或長輩想安靜住淺草或上野，預算有限看池袋，購物和吃為主住銀座，年輕、行程集中西側選澀谷。 |
| `yokohama-day-trip-from-tokyo.json` | zh-TW | 212 → 194 | 從東京去橫濱，住澀谷搭東急東橫線直通元町・中華街最快約 36 分，住東京車站、品川搭 JR 京濱東北線到櫻木町；照這條路線みなとみらい線最多搭一兩段，刷 Suica 就好，東急線みなとみらいパス 920 日圓只適合跳好幾站的人。 |

Owner's host import, dry run first, then publish (same slug list):

```
python -m app.cli guides-import --actor-email <admin> --dry-run --slug busan-3-day-itinerary --slug dmz-day-trip-from-seoul --slug fuji-kawaguchiko-day-trip --slug fukuoka-airport-to-hakata-tenjin --slug gimhae-airport-to-busan --slug hakone-day-trip-free-pass --slug himeji-castle-day-trip --slug hiroshima-miyajima-2-day --slug incheon-airport-to-seoul --slug japan-drugstore-shopping-list --slug japan-entry-2026-visit-japan-web --slug japan-esim-sim-wifi --slug japan-ic-card-suica-icoca-guide --slug japan-ski-season-2026-2027 --slug japan-winter-illumination-2026 --slug japan-year-end-new-year-2026-2027 --slug jeju-3-day-itinerary --slug kamakura-enoshima-day-trip --slug kobe-arima-day-trip --slug korea-entry-2026-k-eta-e-arrival --slug korea-esim-sim-wifi --slug korea-money-exchange-wowpass-guide --slug korea-olive-young-tax-refund-shopping --slug nagoya-3-day-itinerary --slug narita-haneda-to-tokyo --slug new-chitose-airport-to-sapporo --slug okinawa-4-day-itinerary --slug osaka-kyoto-where-to-stay --slug sapporo-snow-festival-2027 --slug seoul-4-day-itinerary --slug seoul-palaces-hanbok-guide --slug seoul-subway-t-money-guide --slug suwon-hwaseong-day-trip --slug takayama-shirakawago-day-trip --slug tokyo-5-day-itinerary --slug tokyo-disney-guide --slug tokyo-transit-passes --slug tokyo-where-to-stay --slug yokohama-day-trip-from-tokyo
python -m app.cli guides-import --actor-email <admin> --publish --slug busan-3-day-itinerary --slug dmz-day-trip-from-seoul --slug fuji-kawaguchiko-day-trip --slug fukuoka-airport-to-hakata-tenjin --slug gimhae-airport-to-busan --slug hakone-day-trip-free-pass --slug himeji-castle-day-trip --slug hiroshima-miyajima-2-day --slug incheon-airport-to-seoul --slug japan-drugstore-shopping-list --slug japan-entry-2026-visit-japan-web --slug japan-esim-sim-wifi --slug japan-ic-card-suica-icoca-guide --slug japan-ski-season-2026-2027 --slug japan-winter-illumination-2026 --slug japan-year-end-new-year-2026-2027 --slug jeju-3-day-itinerary --slug kamakura-enoshima-day-trip --slug kobe-arima-day-trip --slug korea-entry-2026-k-eta-e-arrival --slug korea-esim-sim-wifi --slug korea-money-exchange-wowpass-guide --slug korea-olive-young-tax-refund-shopping --slug nagoya-3-day-itinerary --slug narita-haneda-to-tokyo --slug new-chitose-airport-to-sapporo --slug okinawa-4-day-itinerary --slug osaka-kyoto-where-to-stay --slug sapporo-snow-festival-2027 --slug seoul-4-day-itinerary --slug seoul-palaces-hanbok-guide --slug seoul-subway-t-money-guide --slug suwon-hwaseong-day-trip --slug takayama-shirakawago-day-trip --slug tokyo-5-day-itinerary --slug tokyo-disney-guide --slug tokyo-transit-passes --slug tokyo-where-to-stay --slug yokohama-day-trip-from-tokyo
```

Changing `description` changes the meta description and the JSON-LD `description` of these 39 pages
at once, so the publish is a visible SEO change; the other 33 documents are
`2026-09-19-aio-answer-first-descriptions-part-2`.
