# verify-1: PR #1335 (claude/batch-8-wave-2), batch 8 wave 2

Verifier: independent round 1. Date: 2026-10-06. I am not the writer.
Every page was fetched with `curl -sSL --compressed -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`, waiting at least 1 s per host. No personal data was sent. `<!-- -->` comments, scripts and styles were stripped before reading, and the HTTP status was checked each time.
Special read methods:
- TTD: the embedded `"data":{…}` JSON.
- AOT: the Next.js `times` arrays for service hours.
- Royal Office 2567 PDF: a scan with no text layer, so I rendered all 7 pages with `pdftoppm` and read them.
- Visit Jeju: removed the `__SEARCH_DATA__` block and confirmed each quoted paragraph sits in the visible `p fr-view > .real` body, not only in `sbstseo`.
- Smart Bus timetables: all four JPGs plus the Dragon Line map, viewed as images.

**Scope:** the seven zh-TW packs added by the PR, all eight diagram SVG texts, the batch-wide shared numbers, and (FOLLOWUPS row 7) the live `phuket-airport-transport-where-to-stay` blocks [18]/[19]/[25]/[28].

**Mechanical checks:** I ran `intake_check.py --from-content --manifest docs/travel-guides-batch-8/batch.json` on an exported copy of the PR tree with a fresh `uv sync --frozen`. All 7 slugs: **PASS (0 failures)**. I could not render SVGs because there is no Chromium or rsvg on this host, so I read the diagram geometry from the SVG source.

## Summary

| Article | Claims | Confirmed | Problems found | Unverifiable |
|---|---|---|---|---|
| phuket-old-town-big-buddha-viewpoints | 48 | 45 | 1 fact (diagram), 1 style | 1 (TAT HQ 06:30–18:30) |
| phuket-airport-transport-where-to-stay [18]/[19]/[25]/[28] (FOLLOWUPS 7) | 18 | 18 | 0 | 0 |
| pattaya-koh-larn-day-trip-from-bangkok | 52 | 51 | 0 | 1 (Sanctuary of Truth) |
| chiang-mai-airport-transport-where-to-stay | 54 | 51 | 2 fact, 1 style | 0 |
| chiang-mai-night-markets-walking-streets | 42 | 31 | 0 | 11 (cmcity.go.th 403) |
| thailand-temple-etiquette-dress-code | 58 | 58 | 0 | 0 |
| hallasan-hiking-reservation-guide | 62 | 60 | 0 | 2 (bus fares) |
| marado-gapado-ferry-day-trip | 64 | 55 | 0 | 9 (Songak Ferry 403, bus.jeju.go.kr) |
| **Total** | **398** | **369** | **3 fact + 2 style** | **24** |

There are 3 fact findings across all seven articles, and no single article has more than 3. By the >3-per-article rule, no article strictly needs round 2 on my findings. The coordinator may still want round 2 for the Phuket diagram fix, because it means redrawing the SVG.

## Findings (ranked)

1. **FACT: Phuket diagram-1 and blocks[7].description.** The solid blue Route 1 line runs **卡隆觀景台 → 神仙半島** (SVG line x=800, y=640→740), and the leg before it, 普吉大佛 → 卡隆觀景台, is dashed as 「沒有公車，要包車」. A reader would charter to Karon View Point and then catch Route 1. The 2026-01-16 Route 1 timetable has no Karon View Point stop: after Karon Circle come Kata Night Plaza, Kata Palm, Sai Yuan and Rawai Beach. The extensions are boxed 「Rawai >> Phromthep Cape 17:22 / 17:47 / 19:02」. The article's own blocks[5] and [33] already say 「沒有卡隆觀景台這一站」.
   - Fix: make Karon VP → Phromthep a dashed charter leg. If Route 1 is drawn, start it at 拉威.
   - Sync the `<desc>` and blocks[7].description, then re-render.
2. **FACT: CNX blocks[9].** It says 「接駁巴士的班距與首末班沒有公布」, but AOT detail page 145 (Airport Shuttle Bus, International, Floor 1, Arrival) lists service hours of **07:00–00:00 daily**. That is the same widget the paragraph uses for the taxis (125: 07:00–00:00, 126: 07:00–23:00, 138: 24 h). The headway is still unpublished, so [27] stays correct.
3. **FACT (minor, wrong subject): CNX blocks[22].** It says TAT Tokyo calls November to February the best time to travel. TAT Tokyo actually says November to February is recommended for **trekking and bird-watching** (「トレッキングやバード・ウォッチングなどは…11月〜2月頃がおすすめ」), and that temples and crafts can be enjoyed all year. The spec makes this a word-for-word shared sentence with `chiang-mai-3-day-itinerary` blocks[22], so change both or file it with ticket `2026-10-06-chiang-mai-3-day-itinerary-airport`.
4. STYLE: CNX blocks[8] row 5 / [9]. AOT 126 says the metered taxi adds **50 baht** (Ministry of Transport gratuity). It is omitted, though the open 3-day-itinerary ticket lists the same gap.
5. STYLE: Phuket blocks[6] budgets 查龍寺 40 min to 1 h. The temple's official FAQ says 「A typical visit lasts between 1 to 2 hours」.

## FOLLOWUPS row 7: existing phuket-airport-transport-where-to-stay vs the official Smart Bus timetable

The `/timetable` page fetched today still serves the same two Route 1 images: `rawai/cyNL6…jpg` (airport → Rawai, from 16 Jan 2026) and `rawai/uxwoQ…jpg` (Rawai → airport, from 16 Jan 2026). It also serves the Route 2 image `patong/QW294…jpg` (from 15 Jan 2026). **No correction is needed** in any of the four blocks:

- **[18]** Last bus 23:30 ✓. After 22:00 only the 22:40 and 23:30 run ✓. The 22:00 reaches PEA Patong at 23:30 ✓. The 23:30 reaches Patong at 01:00 and Rawai at 01:50 ✓. First bus 08:15 ✓.
- **[19]** First northbound bus is 05:20 from Kata Palm, at Bangla Police Box Patong 06:00 and the airport 07:32 ✓. Rawai's first bus is 06:45, at the airport 09:17 ✓. Last bus is 19:30 from Rawai, at Bangla 20:20 and the airport 21:52 ✓. Patong → airport is 92 min both times ✓. Rawai → airport is 2 h 22 to 2 h 32 ✓.
- **[25]** Some runs extend from Rawai to Phromthep, marked yellow ✓. The legend says 「ไปแหลมพรหมเทพ Go To Phromthep Cape」. The yellow rows are the 14:00, 15:00 and 16:00 airport departures (Rawai 16:20 / 17:20 / 18:20). The box says 17:22 / 17:47 / 19:02 Rawai → Phromthep and 17:23 / 17:48 / 19:03 back. ERRATA wave 2 is right that the yellow rows and the box do not line up. [25] does not quote times, so it is not wrong.
- **[28]** Route 2 runs from Phuket Bus Terminal 1 via town to Patong for 50 baht flat ✓ (image says Terminal 1, the tab text says "Bus Terminal 2"). Dragon Line runs 07:00–19:00 every 30 min ✓ (map: 「รถออกทุก 30 นาที เริ่มตั้งแต่ 07.00 - 19.00 น.」).

Also checked: [5] and [6] stop times (08:15 → Big C Kamala 09:13, PEA Patong 09:35, Karon Circle 09:47, Kata Night Plaza 09:57, Rawai 10:25) ✓, and [24] (Cherngtalay 30–40 min, Surin 45 min) ✓.

Outside the four blocks, for the coordinator only (not in the errors list):
- [14] says 「未滿 6 歲…免費」. The operator's Payment page still says "Children under 6 ride free with a paying adult". The operator's blog of 2026-06-25 says "Children under 90 cm … free … Height is the determining factor, regardless of age" (https://www.phuketsmartbus.com/blog/children-under-90-cm-ride-for-free). Two operator pages disagree.
- [24] spells Promthep Cape, while the new article and the timetable use Phromthep Cape.

The new Phuket article's [29] (yellow 14:00/15:00/16:00, box 17:22/17:47/19:02, return 17:23/17:48/19:03) is confirmed word for word against the image.

## Per-article claim results

### phuket-old-town-big-buddha-viewpoints (48)
**Smart Bus pages:**
- `/timetable` (200): Route 1 100 ฿, Route 2 50 ฿ flat, Dragon Line free; "Central Festival, Old Town and OTOP Market"; times approximate; tab text "Bus Terminal 2" vs image Terminal 1 ✓.
- Route 2 image (200): Terminal 1 departures 06:00–20:00, Patong departures 06:00–21:00, 1 h to 1 h 10 ✓.
- Dragon map (200): every 30 min 07:00–19:00, stops Thaihua Museum and บขส.1 ✓.
- Old-town blog (200): Thalang Rd, Soi Romanee pink and blue houses, Standard Chartered 1907, 20+ murals, free map at cafés, 10 min walk north, 50 ฿ ✓.

**TAT Tokyo pages (all 200):**
- Big Buddha: 08:00–19:00, 45 m tall, 25.454 m wide, 10,000+ marble pieces, Chalong Bay and Rawai, sunset, 20–30 min from town and 30–40 from Patong; URL field mingmongkolphuket.com returns 301 to facebook.com/mingmongkolphuket ✓.
- Wat Chalong: Wat Chaithararam, about 8 km SW, 08:00–17:00, 参拝自由, 15–20 and 30 min, 1876 monks ✓.
- Phuket Town: 16th–18th century tin and trade, Portuguese, Dutch and Hokkien merchants ✓.
- Lard Yai: Sundays 16:00–22:00, opened 2013-09-29 ✓.
- Thaihua Museum: 200 ฿, 09:00–17:00, closed Mondays, built 1934, school until 2001, red bat, "visit first" ✓.
- Chui Tui: Dou Mu, 1907, vegetarian festival around October for 9 days, 10–15 min walk ✓.
- Put Cho and Sang Tham spellings ✓.
- Rang Hill: NW of town, only 「無休」 ✓.
- Karon View Point: former name Kata VP, three beaches ✓.
- Laem Phromthep: sunset, Kanchanaphisek lighthouse, Brahma shrine, elephant offerings, 40 min by tuk-tuk and 30 min from Patong ✓.
- areainfo/phuket: dry Nov–Mar, hot Apr–May, green Jun–Oct; songthaew 07:00–18:00 every 30 min; tuk-tuk fares negotiated ✓.

**Wat Chalong official site (200):**
- Index: Wat Chaiyathararam, 60 m chedi, three floors, top terrace, relic behind glass ✓.
- FAQ: 07:00–17:00, no fee ✓.

**Result:** the diagram finding (#1), the style note (#5), and TAT HQ 06:30–18:30 unverifiable (Cloudflare).

### pattaya-koh-larn-day-trip-from-bangkok (52)
**RRC airportpattayabus.com, Bangkok Terminal page (200):**
- Mo Chit 2: 155 ฿, motorway, departs 05:00–18:00 hourly; return 05:00, 07:30, then 09:00–18:00; window 34, platform 42 ✓.
- Ekkamai: 144 ฿, departs 05:00, 06:00, then 09:00–22:00; return 04:30, 08:00–20:00, 22:00; floor 1 window 13, platform 1 ✓.
- Bang Na: 144 ฿, 06:30 then 09:30–21:30, counter sale only ✓.
- About 2 h, arrive 15 min early; North Pattaya terminal on North Pattaya Rd near Sukhumvit ✓.

**Other RRC pages:**
- Airport → North Pattaya (200): 135 ฿; 07:30, 09:30, 11:30, 13:30, 15:30, 17:30, 18:30 (7 trips); return 08:00–18:00 every 2 h plus 21:00; Floor 1 Gate 8 ✓.
- Airport → Jomtien (200): 158 ฿, 06:00–22:00 hourly; the 22:00 goes to the North terminal; return 06:00–22:00 ✓.
- pattayabus.com returns 301 to airportpattayabus.com ✓.
- rrcticket.com: Ekkamai, Mor Chit, Suvarnabhumi ✓.

**TTD embedded JSON (all 200):**
- 1689: ferry 30 ฿ about 45 min, speedboat 200–250 ฿ 15–20 min; English lists 08:00, 09:00, 11:00, 13:00 and 13:00–16:00, Thai adds 17:00; 750 m; busiest 09:00–16:00; History 「…หมู่เกาะปะการัง」 = 「珊瑚島」 ✓.
- 5009: 7 km, 5.6 km², Pattaya City / Bang Lamung; speedboats dock at Tawaen ✓.
- 754: run by เมืองพัทยา, South Pattaya ✓.
- 1690: Nual is south, 250 m, private land, intact coral, beds and bar, straight from ท่าหน้าบ้าน, 3.2 km by songthaew ✓.
- 1694: Samae is west, about 800 m, stingray building, pavilion, boardwalk to rocks, via police-station road, Thian at the end ✓.
- 21500: Thian is quiet, small bridge, about half a km, few facilities, songthaew and motorbikes at the entrance ✓.

**TAT Tokyo pages:**
- Bali Hai: 06:00–21:00, boats about 08:00–17:00, 10 min from the centre, PATTAYA city sign ✓.
- Wat Phra Yai: 1977, about 10 × 18 m, 10:00–20:00, 10 min by songthaew ✓.
- areainfo/pattaya: seasons; songthaew, motorbike taxi, meter taxi and 3 bus lines ✓.

**Arithmetic:** 16:45 landing gives 5 h 15, 4 h 15 and 1 h 15 before the last buses ✓. FAQ 09:45 ✓.

**Unverifiable:** Sanctuary of Truth (captcha).

### chiang-mai-airport-transport-where-to-stay (54)
**AOT CNX:**
- Home (200): A1 40 ฿ Nimman → Huay Kaew → moat; A2 40 ฿ Mahidol → Night Bazaar → Chang Klan hotels; A3 60 ฿ ring road 2 → 700th stadium; International Gate 12; city bus 06:00–23:30; yellow and red stop lists exactly as in table row 4; รถแดง; car rental on Floor 1; arrive 2 h early ✓.
- 125: Entrance 1, Main Terminal, Floor 1, flat-rate, 07:00–00:00 ✓.
- 126: Entrance 1, 07:00–23:00, +50 ฿ ✓.
- 138: Car park, Domestic, Floor 1, call from anywhere but use designated points, 24 h ✓.
- 139: 30 ฿ per trip, colours swapped versus the home page, yellow lists Waroros ✓, so the caption caveat is justified.
- 145: shuttle 07:00–00:00, which leads to finding #2.

**Grab:**
- TH transport page (200): GrabCar and JustGrab in all regions incl. Chiang Mai; GPS pickup; upfront fare excl. tolls and surcharges; cash, card, GrabPay; advance booking 90 days to 75 min; SUV and Van "available in specific cities" ✓.
- Global airport index lists CNX with an empty href; the CNX page is 404 ✓.

**rtc-citybus.com:** 200 but a Hawk Host placeholder ✓.

**TAT Tokyo pages:**
- areainfo/chiangmai: 720 km, about 50 flights a day, 1 h 20; Mo Chit 9.5–11 h; red songthaew in town; yellow to Mae Rim and Chom Thong, blue to Lamphun, from Chang Phuak and Warorot; 24A and 24B 06:30–19:30 hourly as of Nov 2024, 24C 8 a day, all from the airport ✓. The November–February sentence is finding #3.
- Terminal 2: largest; Bangkok, Khon Kaen, Nakhon Ratchasima; Chiang Rai, Mae Hong Son (Pai), Lampang; about 3 km; tuk-tuk or songthaew ✓.
- Tha Phae: east wall, 15 min from the airport ✓.
- Nimman: about 1 km, Soi 1, 15 min ✓.
- Night Bazaar: Chang Khlan, hotels and malls, lively till late, 10 min ✓.
- Warorot: 20 min from the station ✓.
- Wat Ket Karam: east bank was an economic district, now residential and cultural tourism, 10–15 min ✓.
- trafficthai: since Jan 2023 rapid, express and special express trains use Aphiwat; ordinary, commuter and tourist trains stay at Hua Lamphong; Chiang Mai about 10 h 30, 5 a day, as of 2023-04-03 ✓.
- Chiang Rai: from Chiang Mai Terminal 1, about 3 h 20 ✓.

**Result:** findings #2, #3 and #4.

### chiang-mai-night-markets-walking-streets (42)
**TAT Tokyo pages:**
- Wualai: Saturday 17:00–22:00, silver village, hill-tribe textiles, steps from Chiang Mai Gate ✓.
- Night Bazaar: 17:00–24:00, open all year, Anusarn, Kalare about 100 m away with a free dance stage ✓.
- Warorot: three opening schedules, Rama V era 1868–1910, Kad Luang, B1 plus 3 floors, about 500 shops, Wichayanon, Chang Moi, 20 and 10 min ✓.
- Jing Jai: 08:00–22:00, farmers' market Sat–Sun, time may change, 6 zones, sausage and 3-colour sticky rice, good goods (Central Group), Tops Green daily, NO PLASTIC BAGS, 20 min from the airport, Atsadathon Rd ✓.
- Sunday Market: massage tents and goods ✓.

**AOT home:** yellow and red stops; transfer at Tha Phae Gate and Kad Suan Kaew; 06:00–23:30 ✓. **AOT 139:** lists Warorot, Jing Jai on no page ✓. Tokyo 06:30–19:30 ✓.

**Sunday Market conflict, not an error:** TAT Tokyo says 「毎週日曜日17:00頃～24:00頃」 and 「約1km」. The spec (§撰稿時要小心 (1)) explicitly rules: use the municipality's 17:00–22:00 and do not write 24:00. The spec overrides README rule 3.

**Unverifiable:** all cmcity.go.th claims (403).

### thailand-temple-etiquette-dress-code (58)
**Grand Palace site (all 200):**
- Practical information: 500 ฿ incl. Wat Phra Kaew and the Queen Sirikit Museum; the 11 banned items map 1:1 to the zh list; no-drone zone; footer 8:30 AM–4:30 PM, tickets until 3:30 PM; the "open daily 8:30 AM–3:30 PM" lines are the second and third places ✓.
- FAQ: Mani Noppharat gate from 2024-01-10; online tickets up to 1 month ahead, no refund or change; under 120 cm free; audio guide 200 ฿ in 8 languages incl. Mandarin ✓.
- Schedules: on 6 Oct 2026 all three items "Open all day" ✓.

**Royal Office 2567 PDF (200, 7 pages read as images):**
- 6(1): 08:30–16:30, sales stop 15:30. 6(2): closed on ceremony and official days.
- 7(2): free up to 120 cm.
- 7(5): dress; also bans tight tops (เสื้อรัดรูป) and three-quarter trousers (ขาสามส่วน); long sleeves under a สไบ; polite dress or correct national costume.
- 10(2): do not touch, take or scribble on decorations, murals, coloured glass, statues.
- 10(3): laser pointers may not be **used**. 10(4): no shots featuring commercial signage. 10(6): weapons. 10(7): pets.
- 11(1): general cameras allowed; no lights, crane, dolly, wireless mic or camera drone. 11(3): no pre-wedding shoots.
- 12(1)/(2): Wat Phra Kaew grounds except inside the ubosot, and outside the throne halls ✓.

**Wat Pho, plan and tips (200):** 08:00–19:30, 300 ฿, under 120 cm free, no shorts but trousers allowed; shorts above the knee banned for women; shoes off onto shelves; women barred from monks' areas; photos allowed but never step on the image; no physical contact between women and monks or novices ✓.

**TAT Tokyo pages:**
- visiting-temples: clothing, waist-cloth rental "場所によっては", hand-holding, laughing, running; women and monks incl. the yellow cloth; 4-piece set about 20 ฿; ベンチャーンカプラディット ×3; gold leaf; soles; every temple non-smoking with fines ✓.
- etiquette: anthem at 08:00 and 18:00; cinema; royal family; head (children OK); soles; stepping over feet ✓.
- Wat Arun 200 ฿ 08:00–18:00; Wat Pho 08:30–20:00, last entry 19:30; White Temple 200 ฿ 08:00–17:00, 14 km; Doi Suthep 30 ฿, cable car 50 ฿, 05:00–21:00, cable 06:00–18:00頃, 40 min ✓.

**Wat Chalong:** dress, shoes, statues, photo and video, donations, 07:00 ✓.

**Bang Pa-In callout:** matches the live ayutthaya-day-trip-from-bangkok [21] word for word ✓.

### hallasan-hiking-reservation-guide (62)
**visithalla reservation info, id=49 (200):**
- Opens on the first business day at 09:00; a local holiday does not delay it; QR sent to the phone; incomplete bookings auto-cancel after 1 day; no waitlist; cancel with the same verification method; penalties 3 months then 1 year.
- Control table (winter Oct–Mar / summer Apr–Sep): entry 11:30/12:30; Dongneung 13:30/14:30; Jindallaebat and Samgakbong descent 15:30/16:30. The old 3-season table still hangs below it.
- Warnings for 주의보 and 경보; gear list; bans with 자연공원법 §27(1); gimbap and burgers allowed ✓.

**Trail pages:**
- id=61 Seongpanak: 9.6 km (7.3 + 2.3), 3 h / 4 h 30 / 9 h, 19.2 km round trip, 156 spaces, overflow lot 199 free, bus 281 06:00–22:00 every 10–14 min (11–17 the other way) 45 and 50 min, bus 181 06:10–22:29 every 30–45 min 35 min, no shop, 1,950 m, 1,700 m advice ✓.
- id=62 Gwaneumsa: 8.7 km (6 + 2.7), 3 h 20 / 5 h / 10 h, 192 spaces, bus 475 06:20–19:45 every 45–90 min, change at 산천단 한국폴리텍대학[서] ✓.
- id=62 zh_CN: shop items ✓.
- id=50: parking 1,000 + 500 per 20 min, cap 13,000; 2,000 + 800, cap 20,000; levied per trail; entry-fee amounts blank ✓.

**Notices:**
- 1284 / 1285en: sections; 5 trails need no booking; the 4/1 → 4/2 example is the notice's own wording; max 4 per booking, once a week; QR plus ID; English says passport ✓.
- 1291: 05:00–08:00 800/400 and 08:01–11:30 200/100 from 2025-12-01 ✓.
- 1297: queue, availability page hidden, 20:00–22:00 maintenance ✓.
- 1295: 1-year entry ban ✓.
- 1294: 156/199 spaces, enforcement zones 4.5 km and 2.3 km ✓.
- 1299: web certificate from 2026-09-01; every method must be applied for and issued the same day ✓.
- 1300: Gwaneumsa reopens 9/24 05:00; bookings from 9/21 09:00 ✓.
- 1270: 05:00 start on every course; effective 2024-07-01; 14 m/s wind ✓.

**Other pages:**
- FAQ: different descent trail, companions' QR, weather cancellation, paper certificate and free JEJU IoT app ✓.
- Login page (ko/en): SNS (Kakao) and non-member verification; foreigner email only without a phone number; "Send verification code" / "Confirm verification number" ✓.
- jeju.go.kr safety: rest-year closure, visibility 20 m, snow 30 cm ✓. info.htm: trail lengths and times; trailhead addresses 516로 1865 and 산록북로 588 ✓. free.htm (in force 2026-01-01): first 30 min free ✓.

**Time-sensitive check:** the newest notice is seq 1301 (trail race on 2026-10-03, now past). Nothing changes after 1300. The English board has no Gwaneumsa notice ✓.

**Unverifiable:** bus.jeju.go.kr fares.

### marado-gapado-ferry-day-trip (64)
**wonderfulis.co.kr:**
- Fares (200): Marado 10,000/20,000 + 1,000 = 21,000; Gapado 7,300/14,500 + 1,000 = 15,500; children 500 with preschoolers exempt; under 24 months free; surcharge notice for Oct 1–31 and Nov 1–30 at 3,600 and 2,600 per person ✓.
- Notice v=83 (200): round trip 3,600 / 2,600, one way 1,800 / 1,300; at least 20 days' notice; priced by booking date; no top-up or refund; exemptions ✓. Totals 24,600 and 18,100 ✓.
- Timetable (200): Marado 09:40, 11:10, 13:50, 15:10 / 10:20, 11:50, 14:30, 15:50; Gapado 09:00, 10:00, 11:00, 12:00, 14:00, 1

> Recording note: the verifier's report reached the branch cut off at this point, mid-way through the marado-gapado-ferry-day-trip timetable line. The rest of that section (the remaining Gapado times, the Songak Ferry and bus.jeju.go.kr items behind the 9 unverifiable claims, and anything after it) was not in the hand-off, so it is not reproduced here. The summary table above has the totals for that article: 64 claims, 55 confirmed, 0 problems, 9 unverifiable.

## Round-1 corrections as applied on the branch (2026-10-06)

Each source was re-opened on 2026-10-06 with the same User-Agent before the change was made.

1. Phuket diagram-1: the 卡隆觀景台 → 神仙半島 leg is now a dashed charter leg labelled 「沒有公車，要包車」. Route 1 is no longer drawn from the viewpoint. A note at the lower left reads 「Route 1｜100 泰銖」 and 「不停卡隆觀景台，只有三班從拉威延駛神仙半島」. The `<desc>` and blocks[7].description were updated to match, and the SVG was re-rendered (resvg with Noto Sans TC) and checked by eye. The Route 1 timetable JPG (200) has no Karon View Point column, and its box reads Rawai >> Phromthep Cape 17:22 / 17:47 / 19:02.
2. CNX blocks[9]: now reads 「接駁巴士的服務時間是每天 07:00 到午夜，班距沒有公布，以現場公告為準。」 The taxi sentence now gives both start times (固定價 07:00 到午夜、跳表 07:00 到 23:00). AOT 145 was added to sources. The Next.js `times` arrays on 145, 125, 126 and 138 read 07:00–00:00:59, 07:00–00:00:59, 07:00–23:00:59 and 00:00–23:59:59 for all seven weekdays.
3. CNX blocks[22]: now reads 「11 月到 2 月氣候涼、花開，是推薦的健行與賞鳥季節」. `chiang-mai-3-day-itinerary` blocks[22] already says 「這幾個月氣候涼、花開，適合健行賞鳥」, so the shared 「11 月到 2 月」 fact still agrees and that article needed no change.
4. CNX blocks[8], row 5: 「；跳表計程車另加 50 泰銖」 was appended. This comes from AOT 126: "An additional charge of 50 Baht will be collected as a gratuity for taxi drivers, in accordance with the announcement from the Ministry of Transport."
5. Phuket blocks[6]: now reads 「查龍寺 1 到 2 小時」, from the FAQ (200): "A typical visit lasts between 1 to 2 hours."

`docs/travel-guides-batch-8/shared-numbers.json` now carries shared-check rules for findings 2–4: `首末班沒有公布` must not appear, `07:00 到午夜` must appear, `最適合旅行` must not appear, and `跳表計程車另加 50 泰銖` must appear. It also checks that `沒有卡隆觀景台這一站` stays in the Phuket pack.
