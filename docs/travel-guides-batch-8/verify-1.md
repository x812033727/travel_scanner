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

---

# verify-2: PR #1335 (claude/batch-8-wave-2), batch 8 wave 2

Verifier: independent round 2 (not the writer, not the round-1 verifier). Date: 2026-10-06.
Branch head checked: `78b1d922` (fetched again before starting; `git log` shows it as the tip of `origin/claude/batch-8-wave-2`).
Every page was fetched with `curl -sSL --compressed -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`, waiting at least 1 s per host. No personal data was sent. Before reading I stripped `<!-- -->` comments, scripts and styles and checked the HTTP status.

Special read methods:
- AOT: the Next.js `times` arrays.
- TTD: the embedded `data` JSON.
- Visit Jeju: removed `__SEARCH_DATA__` first.
- Smart Bus: all five timetable JPGs and the Dragon map, viewed as images.
- Royal Office 2567 PDF: rendered with pymupdf and read pages 4 and 5.
- Diagram: rendered `diagram-1.svg` with resvg (WenQuanYi Zen Hei, because there is no Chromium on this host) and checked it by eye.

## Summary

| Part | Claims | Confirmed | Problems | Unverifiable |
|---|---|---|---|---|
| Round-1 corrections, re-checked | 19 | 18 | 1 consistency (left over in the edited field) | 0 |
| FOLLOWUPS row 7: live phuket-airport-transport-where-to-stay | 22 | 21 | 1 consistency ([14]) | 0 |
| phuket-old-town-big-buddha-viewpoints, random third | 40 | 37 | 0 | 3 |
| pattaya-koh-larn-day-trip-from-bangkok, random third | 46 | 45 | 1 consistency (summary) | 0 |
| chiang-mai-airport-transport-where-to-stay, random third | 37 | 37 | 0 | 0 |
| chiang-mai-night-markets-walking-streets, random third | 31 | 22 | 0 | 9 (cmcity 403) |
| thailand-temple-etiquette-dress-code, random third | 63 | 63 | 0 | 0 |
| hallasan-hiking-reservation-guide, random third | 65 | 61 | 0 | 4 (bus.jeju TLS) |
| marado-gapado-ferry-day-trip, random third | 55 | 52 | 0 | 3 (songakferry 403) |
| **Total** | **378** | **356** | **3 (all consistency, no fact errors)** | **19** |

Random third: blocks were drawn with `random.seed(1335)` from each pack's text, table, list, callout, FAQ and summary blocks:
- phuket: 1, 2, 5, 12, 17, 25, 28, 29, 34
- pattaya: 4, 5, 8, 12, 16, 19, 20, 23, 31, 36
- CNX airport: 8, 9, 14, 19, 21, 28, 29
- CNX night markets: 0, 2, 4, 6, 9, 12, 14, 24, 27
- temples: 5, 14, 18, 19, 22, 24, 27, 28, 32, 38, 41, 42
- hallasan: 0, 5, 8, 11, 15, 20, 24, 30, 31, 41, 46, 47, 48
- marado: 1, 2, 4, 5, 20, 23, 25, 28, 30, 42

**Verdict:** all five round-1 corrections are correct, and none introduced a new fact error. Round 2 found no fact errors, so no third round is needed. Three consistency items are listed below. The Phuket image-description one belongs in this PR. The Pattaya summary wording is a one-line clarification. The live Phuket-airport [14] item is for a follow-up ticket.

## 1. Round-1 corrections, re-checked on 78b1d922

| # | Correction | Source (status) | Result |
|---|---|---|---|
| 1 | Phuket diagram: 卡隆觀景台→神仙半島 is now a dashed red charter leg (`line x=800 y=640→740`, `stroke-dasharray 14 10`) labelled 「沒有公車，要包車」. The lower-left note reads 「Route 1｜100 泰銖」「不停卡隆觀景台，只有三班從拉威延駛神仙半島」. | Route 1 JPG `rawai/cyNL6…jpg` (200) | CONFIRMED. The stop columns run Airport … PEA Patong, Karon Circle, Kata Night Plaza, Kata Palm, Sai Yuan, Rawai Beach; there is no Karon View Point. The box reads 「Rawai >> Phromthep Cape 17:22 / 17:47 / 19:02」 and 「Phromthep Cape >> Kata/Karon/Patong/Airport 17:23 / 17:48 / 19:03」. Yellow rows are the 14:00, 15:00 and 16:00 airport departures, reaching Rawai at 16:20, 17:20 and 18:20. The fare is 100 ฿ (the /timetable page, 200). |
| 1a | Diagram render | resvg PNG | No overlaps. The note at x=60, y=742/768 sits below the Karon box (y≤680) and left of the island (x≥500). Font sizes are ≥16 px. intake_check: "every number on the diagram is in the text". |
| 1b | SVG `<desc>` and blocks[7].description | SVG file | `<desc>` matches the drawing. blocks[7].description matches on the legs and the note, but still says 「普吉大佛與神仙半島之間的**右側**有一個小圈標卡隆觀景台」, while the box is on the left. That is error #1 below (consistency, left over from before the fix). |
| 2 | CNX [9]: 「接駁巴士的服務時間是每天 07:00 到午夜，班距沒有公布」; 固定價 07:00 到午夜, 跳表 07:00 到 23:00, Grab 24 h | AOT detail 145, 125, 126, 138 (all 200) | CONFIRMED. `times` arrays for all 7 weekdays: 145 = 07:00:00–00:00:59, 125 = 07:00:00–00:00:59, 126 = 07:00:00–23:00:59, 138 = 00:00:00–23:59:59. Page 145 is "International, Floor: 1, Zone: Arrival", which matches the new source title, and it lists no headway. [27] 「沒有官方班距」 is still true. |
| 3 | CNX [22]: 「11 月到 2 月氣候涼、花開，是推薦的健行與賞鳥季節」 | TAT Tokyo areainfo/chiangmai (200) | CONFIRMED: 「トレッキングやバード・ウォッチングなどは、気候が涼しく花々が満開となる11月〜2月頃がおすすめ…寺院めぐりや伝統工芸品などは、年間を通じて楽しむことができます」. chiang-mai-3-day-itinerary [22] says 「這幾個月氣候涼、花開，適合健行賞鳥」, so the two agree and no change is needed there. |
| 4 | CNX [8] row 5: 「跳表計程車另加 50 泰銖」, plus the source title | AOT 126 (200) | CONFIRMED: "An additional charge of 50 Baht will be collected as a gratuity for taxi drivers, in accordance with the announcement from the Ministry of Transport." |
| 5 | Phuket [6]: 「查龍寺 1 到 2 小時」, plus the FAQ source title | wat-chalong-phuket.com/faq.html (200) | CONFIRMED: "A typical visit lasts between 1 to 2 hours." |

Guard rules in `shared-numbers.json` (最適合旅行 and 首末班沒有公布 absent; 07:00 到午夜, 跳表計程車另加 50 泰銖 and 沒有卡隆觀景台這一站 present): all hold. `shared_check.py --from-content` against the branch content dir: **RESULT PASS (0)**, all 6 groups.

## 2. FOLLOWUPS row 7: live phuket-airport-transport-where-to-stay vs the official Smart Bus timetable

`/timetable` (200) still serves `rawai/cyNL6…jpg` (Airport→Rawai, start 16 Jan 2026), `rawai/uxwoQ…jpg` (Rawai→Airport, start 16 Jan 2026) and the Route 2 images. I read both Route 1 images cell by cell.

- **[18]** CONFIRMED. Last bus 23:30. After 22:00 only 22:40 and 23:30 run. The 22:00 reaches PEA Patong at 23:30. The 23:30 reaches Patong at 01:00 and Rawai at 01:50. First bus 08:15.
- **[19]** CONFIRMED.
  - First northbound bus is 05:20 from Kata Palm (the Rawai cell is blank), at Bangla Police Box at 06:00 and the airport at 07:32.
  - Rawai's first bus is 06:45, at the airport at 09:17.
  - Last bus is 19:30 from Rawai, at Bangla at 20:20 and the airport at 21:52.
  - Patong to the airport is 92 min both times. Rawai to the airport is 2 h 32 and 2 h 22.
- **[25]** CONFIRMED. Some runs extend from Rawai to Phromthep and are marked yellow (legend 「ไปแหลมพรหมเทพ Go To Phromthep Cape」). [25] quotes no times, so the 14:00/15:00/16:00 vs 17:22/17:47/19:02 mismatch noted in ERRATA does not make it wrong.
- **[28]** CONFIRMED. Route 2 runs from Terminal 1 for 50 ฿ flat (the tab text says "Bus Terminal 2", the image says Terminal 1, as FOLLOWUPS already notes). Dragon Line runs every 30 min, 07:00–19:00 (map: 「รถออกทุก 30 นาที เริ่มตั้งแต่ 07.00 - 19.00 น.」).
- **No correction is needed in [18]/[19]/[25]/[28].**
- Outside those four blocks:
  - **[14]**: the Payment page (200) says "Children under 6 ride free with a paying adult". The operator blog of 2026-06-25 (200) says "Children under 90 cm … free … Height is the determining factor, regardless of age". That is error #3 (consistency, follow-up ticket).
  - **[24]** 「Promthep Cape」: FOLLOWUPS already rules it 「不是錯字、低優先備查」, so it is not reported.

## 3. Random third: per-claim results

### phuket-old-town-big-buddha-viewpoints

**TAT Tokyo pages (all 200):**
- Wat Chalong: 08:00～17:00, 参拝自由, about 8 km SW, 15–20 min by car from town and 30 min from Patong, 1876 ✓ ([5], [19]).
- Big Buddha: 08:00～19:00, width 25.454 m, height 45 m, 10,000+ marble pieces, Chalong Bay and Rawai, sunset, 20–30 and 30–40 min ✓ ([5], [23]).
- Chui Tui: 1907, 斗母, around October for 9 days, 10–15 min walk ✓.
- areainfo/phuket: 無病息災 (Chui Tui), 恋愛運 (Put Cho), 学問・商売 (Sang Tham) → 消災、姻緣、學業與生意 ✓ ([12]).
- Put Cho and Sang Tham spellings ✓.
- Thaihua: 200 バーツ, 09:00～17:00／月曜休館 ✓.
- Rang Hill: 無休 ✓.
- Karon VP: no hours or fee listed ✓.
- Laem Phromthep: sunset, the Rama IX 50th-year Kanchanaphisek lighthouse, Phra Phrom shrine, elephant offerings, about 40 min by chartered tuk-tuk and 30 min from Patong ✓ ([28]).

**Smart Bus:**
- Dragon map ✓ ([5]).
- Old-town blog: 10-minute walk north, 50 ฿ ✓ ([34]).
- Route 1 has no Wat Chalong or Big Buddha stop ✓ ([17]).
- [29] matches the image word for word ✓.

**Unverifiable:** TAT HQ 06:30–18:30 (403); the 2024 landslide (news only).

### pattaya-koh-larn-day-trip-from-bangkok

**RRC pages (all 200):**
- Mo Chit 2: 155 ฿, departs 5:00–18:00 hourly; return 5:00, 7:30, then 9:00–18:00; window 34, platform 42 ✓.
- Ekkamai: 144 ฿, departs 5:00, 6:00, then 9:00–22:00; return 4:30, 8:00–20:00, 22:00; floor 1 window 13, platform 1 ✓.
- Bang Na: 144 ฿, 6:30 then 9:30–21:30, counter only ✓.
- Airport → North terminal: 135 ฿, 7 trips (7:30 … 17:30, 18:30); return 8:00 … 18:00 plus 21:00; Floor 1 Gate 8 ✓.
- Jomtien: 158 ฿, 6:00–22:00; the 22:00 goes to the North terminal ✓.
- About 2 h, arrive 15 min early, North Pattaya Rd near Sukhumvit ✓ ([4], [5], [8]).

**TTD 1689 / 5009 (200):**
- Thai list: 8.00, 9.00, 11.00, 13.00 out; return 13.00–16.00, with Thai adding 17.00 ✓ ([19]).
- 7 km, 5.6 ตร.กม., Bang Lamung, หมู่เกาะปะการัง ✓ ([16]).

**TAT Bali Hai (200):** 06:00～21:00, boats 08:00頃～17:00頃, about 10 min from the centre, South Pattaya Rd ✓ ([12]).

**Arithmetic:** 16:45 landing leaves 5 h 15 / 4 h 15 / 1 h 15 before the last buses ✓ ([31]).

**Finding:** summary [0] item 2 attaches the outbound 05:00/06:00→09:00 gap to 「回程」. That is error #2.

### chiang-mai-airport-transport-where-to-stay

**AOT home (200):**
- A1/A2/A3 40/40/60 ฿, routes ✓.
- International gate 12 ✓.
- Yellow and red stop lists exactly as in [8] row 4 ✓.
- 06:00–23:30 ✓, รถแดง ✓, car rental on the first floor ✓, 2 h early ✓.

**AOT 139 (200):** colours swapped, Waroros listed ✓ ([8] caption).

**TAT Tokyo (all 200):**
- Bus Terminal 2: largest; Bangkok, Khon Kaen, Nakhon Ratchasima; Chiang Rai, Mae Hong Son (Pai), Lampang; about 3 km; tuk-tuk or songthaew ✓ ([14]).
- Warorot: 20 min from the station ✓.
- Tha Phae: east wall, 15 min from the airport ✓.
- Nimman: about 1 km, Soi 1, 15 min ✓.
- Night Bazaar: Chang Khlan, hotels, malls and restaurants, busy until late, 10 min ✓.
- Wat Ket Karam: east bank formerly the economic district, now residential and cultural tourism, 10–15 min ✓ ([19], [29]).

### chiang-mai-night-markets-walking-streets

**TAT Tokyo:**
- Jing Jai: 08:00～22:00, farmers' market Sat–Sun only, time may change, NO PLASTIC BAGS ✓ ([27]).
- Warorot: Rama V 1868–1910, Kad Luang, B1 plus 3 floors, about 500 shops, Wichayanon Rd, Chang Moi, Tue 10:30 ✓ ([24]).
- Night Bazaar: 17:00～24:00, 年中無休 ✓ ([6]).
- Wualai: Saturday 17:00～22:00 ✓.

**AOT:** home 06:00–23:30 ✓; 139 lists Waroros ✓ ([0]).

**Unverifiable:** cmcity.go.th claims in [0], [9], [12], [14] (403).

### thailand-temple-etiquette-dress-code

**Grand Palace site (200):**
- Practical information: 11-item list = [5] ✓; 500 ฿ incl. Wat Phra Kaew and the Queen Sirikit Museum ✓; no-drone ✓; footer 8:30–16:30, tickets 8:30–15:30 ✓.
- FAQ: Mani Noppharat from 10 Jan 2024 ✓; 1 month ahead ✓; no refund or change ✓; under 120 cm free ✓; audio guide 200 ฿, 8 languages incl. Mandarin ✓.
- Schedules: Oct 2026, all three "Open all day" ✓ ([27], [28]).

**Royal Office 2567 PDF (200):**
- 10(2): no touching murals, coloured glass, statues ✓ ([38]).
- 10(3): laser pointer use ✓. 10(4): commercial signage ✓. 10(6): weapons and imitation weapons ✓. 10(7): pets ✓.
- 11(1): no lights, crane, dolly, wireless mic or camera drone ✓.
- 11(3): pre-wedding ✓ ([18]).

**Wat Pho plan (200):** 08:00–19:30, 300 ฿, under 120 cm free, no shorts, shoes onto shelves, no physical contact between women and monks or novices, women barred from monks' areas ✓ ([22], [27]).

**TAT Tokyo:**
- Wat Arun: 200 ฿, 08:00～18:00 ✓.
- White Temple: 200 ฿, 08:00～17:00, 14 km ✓.
- Doi Suthep: 30 ฿, cable car 50 ฿, 05:00～21:00, cable car 06:00～18:00頃, 40 min ✓.
- Etiquette: anthem at 08:00 and 18:00, cinema, royal family, soles, stepping over feet ✓ ([14], [24]).
- Visiting-temples: no smoking with fines; hand-holding, laughing, running, jumping and dancing ✓ ([38]).

### hallasan-hiking-reservation-guide

**Reservation info, id=49 (200):**
- First business day at 09:00; local holidays do not delay ✓.
- Penalties 3 months, then 1 year ✓.
- Control table: winter (10, 11, 12, 1, 2, 3) / summer (4–9) entry 11:30/12:30; 동능정상 13:30/14:30 ✓.
- An old 3-season table still hangs below it ✓ ([24]).
- Gear: 사탕, 초코렛, 소금, 여벌옷, 방한복, 아이젠, 장갑, 따뜻한 물 ✓.
- Bans and 자연공원법 §27(1) ✓; 김밥 and 햄버거 allowed ✓ ([46]).

**Notices:**
- 1291: 800/400, 200/100 ✓.
- 1284: example 4/1 → 4/2; max 4 per booking; once a week; QR plus ID; 281/181 ✓ ([0], [11]).
- 1297: queue, availability page hidden ✓ ([20]).
- 1300: reopening 9/24 05:00 ✓.
- 1299: all certificate methods same-day; paper/kiosk, app, web ✓ ([48]).

**Trail pages:**
- id=62: 8.7 km, 3 h 20 / 5 h; 475 runs 06:20–19:45 every 45–90 min; airport/terminal have no direct service, change at 산천단 한국폴리텍대학[서] ✓ ([30]).
- jeju.go.kr info.htm: 6.8 km (2 h / 3 h), 5.8 km (1 h 30 / 2 h 30), 9.6 km (3 h / 4 h 30); 산록북로 588 ✓ ([5], [30]).
- safety.htm: visibility 20 m, snow 30 cm, 랜턴, 등산화, 식수 ✓ ([46], [47]).

**Login page:** SNS (Kakao) and non-member; foreigners use the foreign-language page's email verification, only without a phone number ✓ ([15]).

**Unverifiable:** [31] fares (bus.jeju.go.kr TLS failure).

### marado-gapado-ferry-day-trip

**wonderfulis.co.kr:**
- Timetable (200): Marado 4 runs, Gapado 6 runs (09:00, 10:00, 11:00, 12:00, 14:00, 15:50) ✓; 30 / 10 min ✓; online booking until the day before ✓; 40 min ✓; 10-minute cut-off ✓; 064-794-5490, 08:00–16:30 incl. holidays ✓; address 최남단해안로 120 ✓; festival extra runs every 30 min ✓ ([0], [4], [5], [23], [28], [42]).
- Fares (200): 10,000/20,000 + 1,000 = 21,000; 7,300/14,500 + 1,000 = 15,500 ✓.
- Notice v=83 (200): at least 20 days' notice, priced by booking date, no top-up or refund, Oct and Nov both 3,600/2,600 round trip ✓ ([0], [20]).
- Boarding procedure (200): forms in groups of 6, minors included, one representative, passport or alien registration card ✓ ([25]).
- FAQ (200): status after 08:00; rain is not a reason, wind and waves decide ✓; 유선 및 도선사업법 §25 and 해운법 §21-2 ✓; no copies, phone-stored IDs, photo-less IDs, or papers older than 3 months ✓; overnight guests get round-trip tickets, phone or counter only ✓; no direct boat between the islands ✓ ([1], [23], [25], [28]).

**PATIS (200):** 「내일의 운항예보 14시 이후 제공」 ✓ ([28]).

**Visit Jeju festival (200, visible body):** 15th festival 2026-04-17 to 05-17, 09:00–17:00, 가파리 일원 ✓ ([42]).

**Unverifiable:** Songak Ferry column (403).

## 4. Shared numbers across the batch (word for word)

`shared_check.py` PASS on all groups (okinawa, chiang-mai, thailand-temples, phuket, jeju, vietnam). Manual comparisons:
- Phuket: Route 1 100 ฿, Route 2 50 ฿, Dragon 07:00 到 19:00 每 30 分鐘 agree between the old-town article and the live airport article.
- Chiang Mai: A1/A2 全程 40 泰銖 is in all three packs. 07:00 到午夜 and 跳表計程車另加 50 泰銖 appear only in the airport article. The 3-day itinerary's gaps are already in ticket 2026-10-06-chiang-mai-3-day-itinerary-airport.
- Temples: Wat Chalong 08:00 到 17:00 and 查龍寺官方網站 … 07:00 agree between the old-town and temple articles. The Grand Palace and Wat Pho numbers match bangkok-4-day-itinerary.
- Jeju: 진달래밭 is 金達萊田 in hallasan and 杜鵑田 in jeju-3-day-itinerary. The official zh_CN trail page (id=61, 200) uses both 「杜鹃花田」 and 「金达莱田」, so this is not an error.

## 5. Mechanical checks (exported branch tree, `uv sync --frozen`)

- `intake_check.py --from-content --manifest docs/travel-guides-batch-8/batch.json`: all 7 slugs **PASS (0 failures)**. The Phuket log says "every number on the diagram is in the text". Self-reference count is 1 (the limit).
- `pack_cli lint --slug` on the two fixed slugs: exit 0.

## 6. Time-sensitive rows today

- Grand Palace schedule: open all day.
- Hallasan Gwaneumsa upper section: reopened on 2026-09-24. No newer notice changes it.
- Marado fuel surcharge: the October and November periods are the same; December is not announced.
- Smart Bus: the timetable images are still the 15/16 Jan 2026 versions.
- Big Buddha: the TAT HQ page was unreadable (403); the article still tells readers to check before going.

## 7. Suspected, not reported

CNX [8] row 5 and FAQ [29] still suggest a taxi for 深夜落地. AOT lists the taxis until 23:00 and midnight, and [9] says 「午夜後落地用 Grab」. This was there before the round-1 fix and is not wrong as written, but the coordinator may want to tighten it.

`verify-1.md` is cut off in the marado section, and the fixer marked the cut honestly.

## Errors reported

1. phuket-old-town blocks[7].description says the Karon View Point box is on the 右側; it is drawn on the left (consistency, in this PR).
2. pattaya summary [0] item 2 attaches the Ekkamai departure gap to the return trip (consistency, in this PR).
3. live phuket-airport-transport-where-to-stay [14]: two operator pages give different child rules, under 6 years vs under 90 cm (consistency, follow-up ticket).

## Round-2 corrections as applied on the branch (2026-10-06)

Before each change, its source was re-opened on 2026-10-06 with the same User-Agent and read with comments, scripts and styles stripped. All three pages returned HTTP 200. The two packs have only the zh-TW locale, so no other locale needed a change.

1. Phuket blocks[7].description: 「普吉大佛與神仙半島之間的右側有一個小圈標卡隆觀景台。」 now reads 「普吉大佛與神仙半島之間的軸線上有一個小圈，連到左側標卡隆觀景台的方框。」 In `diagram-1.svg` the small white circle is at `cx=800 cy=640` on the central line, and the 卡隆觀景台 box is `rect x=60 y=600 width=500 height=80`, joined by `line x1=560 x2=788 y=640`. A resvg render (WenQuanYi Zen Hei) shows the box on the left, the same side as 蘭山觀景台. The SVG and its `<desc>` were not changed. The spec `phuket-old-town-big-buddha-viewpoints.md` still says 「右側在第 3 站與第 4 站之間拉一個小圈」. The drawing departs from the spec there, so the description now follows the drawing.
2. Pattaya blocks[0] item 2: 「住蘇坤蔚一帶走 Ekkamai，回程末班到 22:00，但 05:00、06:00 之後直接跳到 09:00；…」 now reads 「住蘇坤蔚一帶走 Ekkamai：去程 05:00、06:00 之後直接跳到 09:00，回程末班到 22:00；…」. The RRC Bangkok Terminal page (`airportpattayabus.com/bangkok-terminal-pattaya/`, 200) lists departures from สถานีขนส่งเอกมัย as 5:00, 6:00, then 9:00 through 22:00 hourly. It lists departures from สถานีขนส่งพัทยา as 4:30, then 8:00 through 20:00 hourly, then 22:00. Every number in the item is unchanged, and the blocks[5] table already had this right. The checklist item 「早上的空檔：Ekkamai 05:00、06:00 之後直接跳到 09:00。」 in the 行前檢查 list already names the morning departures from Ekkamai, so it was left as is.
3. Live `phuket-airport-transport-where-to-stay` blocks[14]: not changed in this PR, because the article is live and outside this PR's packs. The two operator pages were re-read on 2026-10-06. `phuketsmartbus.com/payment` (200) says "Children under 6 ride free with a paying adult." `phuketsmartbus.com/blog/children-under-90-cm-ride-for-free` (200, June 25, 2026) says "Height is the determining factor, regardless of age." The follow-up is filed as `tasks/open/2026-10-06-phuket-airport-smart-bus-child-fare.md` (P2, scope: that pack only), with a suggested sentence that discloses both rules. No other pack in the content directory has a Smart Bus child-fare sentence.

# verify-3 (wave 2): Round-3 independent fact-check: PR #1335 (claude/batch-8-wave-2)

- **Head checked:** `c353c9c3bc4a39bf94db9aa05402129427ac1158` (fetched before starting and again at the end; it did not move).
- **Read-only:** no repo edits, commits, pushes or comments.

**How pages were read**
- All requests used the UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` and no personal data. TLS verification was never disabled.
- curl pages: I stripped `<!-- -->`, scripts and styles before reading.
- Browser pages: the given Playwright/Chromium script. One host needed headed Chromium under `xvfb-run`: tourismthailand.org shows a Cloudflare check to headless Chromium and passes in headed mode.
- bus.jeju.go.kr opened in Chromium (HTTP 200). curl still fails TLS there.
  - Route lists came from the page's own `POST /publicTrafficInformation/getBusRouteNum`.
  - Per-route timetables came from `/data/schedule/downScheduleExcel?gscheduleId=…`.
  - The express fare workbook came from `/publicTrafficInformation/download/fast/fee`, which is a download.
- I rendered `diagram-1.svg` with Chromium and checked it by eye.

**Result:** 61 claims checked. 53 confirmed. 1 problem, a consistency item outside the round-2 fix set. The rest are unverifiable because two hosts block every request at the origin.

## (a) Changes made by the round-2 fix commit

| # | Claim | Source (status) | Outcome |
|---|---|---|---|
| 1 | Phuket blocks[7].description: 「普吉大佛與神仙半島之間的軸線上有一個小圈，連到左側標卡隆觀景台的方框」 | `diagram-1.svg` at head, plus a Chromium render | CONFIRMED. A white circle `cx=800 cy=640 r=12` sits on the central axis between Big Buddha (y=540) and Phromthep (y=740). A grey line `x 560→788, y=640` joins it to the box `x=60–560, y=600–680` labelled 卡隆觀景台／卡塔、卡隆盡收眼底, on the left like 蘭山觀景台. |
| 2 | The rest of the description: four stations on the right with the stated sub-labels; Rang Hill small circle left of the old town; Dragon Line ring solid and labelled 免費; Route 2 solid to 芭東, 50 泰銖; four red dashed legs labelled 沒有公車，要包車 (old town → Wat Chalong → Big Buddha → Karon VP → Phromthep); lower-left note 「Route 1｜100 泰銖／不停卡隆觀景台，只有三班從拉威延駛神仙半島」; legend at lower right | same | CONFIRMED. The render has no overlaps. Not an error: the description does not mention the short dashed leg from the old town to the Rang Hill circle, though [5] also says 叫車上山. The `<desc>` has no left/right wording and agrees. |
| 3 | verify-1 notes for this fix: the geometry, and the spec line 「右側在第 3 站與第 4 站之間拉一個小圈」 still in the spec | SVG, plus `docs/travel-guides-batch-8/phuket-old-town-big-buddha-viewpoints.md:228` | CONFIRMED |
| 4 | Pattaya summary [0] item 2: 「去程 05:00、06:00 之後直接跳到 09:00，回程末班到 22:00；蒙奇 2 回程末班只有 18:00」 | RRC `airportpattayabus.com/bangkok-terminal-pattaya/` (200) | CONFIRMED. From Ekkamai: 5:00, 6:00, then 9:00–22:00 hourly. From Pattaya: 4:30, 8:00–20:00, 22:00. Mo Chit 2 return: 5:00, 7:30, 9:00–18:00. Fares 144/155 unchanged. Ekkamai has the most trips of the three lines (16 a day). |
| 5 | The same item agrees with [5], [7], [30], [32], [39], [40] | pack | CONFIRMED, no contradictions |
| 6 | Smart Bus Payment page: "Children under 6 ride free with a paying adult." | `phuketsmartbus.com/payment` (200) | CONFIRMED word for word. 100 ฿ / 50 ฿ / Dragon free also match. |
| 7 | Smart Bus blog of June 25, 2026: free under 90 cm; accompanied by a parent or guardian; staff may measure height; "Height is the determining factor, regardless of age." | `phuketsmartbus.com/blog/children-under-90-cm-ride-for-free` (200) | CONFIRMED, all four quotes and the date |
| 8 | Live `phuket-airport-transport-where-to-stay` blocks[14] ends 「未滿 6 歲由付費成人陪同免費，以官網為準。」. The Payment source title names 未滿 6 歲, `checked_on` 2026-09-14. | pack at head | CONFIRMED. The ticket `2026-10-06-phuket-airport-smart-bus-child-fare` describes the conflict accurately. Its suggested sentence is reasonable. |
| 9 | "No other pack has a Smart Bus child-fare sentence" | `git grep` across the content packs | CONFIRMED. Only the airport pack has one; old-town and thailand-esim do not. |

The round-2 fixes are correct and introduce no new error.

## (b) Sources rounds 1–2 could not open

### tourismthailand.org: Big Buddha (headed Chromium, 200)
- 06:30–18:30, Mon–Sun: CONFIRMED. These are the tooltip rows under "Openning Hours" (the button shows "Now Close" at Thai night time). The same times are in the page's Nuxt payload. This covers Phuket [5] row 4, [24], [39] and the source title.
- 「頁上的官方網址現在轉到臉書專頁」: CONFIRMED. The page's website link is `www.mingmongkolphuket.com`, which returns 301 to `facebook.com/mingmongkolphuket`.
- Observation, not reported as an error: the tooltip ends with "* Close on Holiday". This may be template text. The article already tells readers to confirm before going, so I did not file it. The source title's 「沒有封閉或重開的說明」 is still true of the landslide closure.

### sanctuaryoftruthmuseum.com/visit-us/ (Chromium; HTTP 202 with the full page rendered)
- Naklua: CONFIRMED. "Soi Naklua 12 Pattaya-Naklua rd, Bang Lamung District, Chonburi". This supports Pattaya [35] 「城市北邊的納克盧阿、和巴里海碼頭方向相反」.
- Museum: CONFIRMED. The name is "The Sanctuary of Truth Museum".
- Ticket prices and opening hours: the page lists them (day 500 ฿, night 700 ฿, day tours 8:20–18:00, night tours 18:20–20:30). The article defers them with 「以官網為準」, so nothing in it is wrong.

### cmcity.go.th: chiang-mai-night-markets-walking-streets
- **Still unverifiable.** Apache 403 at the origin on every path, homepage included. This happens for curl, headless Chromium and headed Chromium, and for both `www.` and the bare domain. The Wayback Machine is unreachable from here.

### songakferry.com /time_regular, /price: marado-gapado-ferry-day-trip
- **Still unverifiable.** The whole site serves the operator's block page (「접근이 제한되었어요」, 403) to every client tried. The Wayback snapshot of 2026-05-17 exists, but its connection was reset.

### bus.jeju.go.kr (Chromium, 200)

| Claim | Where | Outcome |
|---|---|---|
| 간/지선 (incl. 관광지순환) single fare: card 1,150, cash 1,200 | hallasan [31], marado [34] | CONFIRMED |
| 급행 base fare for 20 km: card 2,000, cash 3,000 | same | CONFIRMED |
| +200 per 5 km | marado [34] | CONFIRMED (5 km 200, 10 km 400, 15 km 600, 20 km 800, over 20 km 1,000) |
| Maximum 3,000 over 40 km | marado [34] | CONFIRMED |
| Express paid in cash always charges the maximum | both | CONFIRMED: 「급행버스는 현금 이용 시, 최대 요금 적용」 |
| Jeju Bus Terminal and airport to 운진항: 47,993 m and 45,304 m, so the express fare is 3,000 | marado [34] | CONFIRMED (fast-fee.xlsx, tab 151) |
| 102 and 151 are 급행, from 제주버스터미널 to 모슬포남항(운진항) | marado [33] | CONFIRMED (route list, plus route sheets 405002 and 405006) |
| 251, 251-1, 252, 253, 254 and 255 are 일반간선, from 제주버스터미널 to 모슬포(운진항) | marado [33] | CONFIRMED (405015 sheets, eff. 2026-03-13; 405016) |
| 500 is a 서귀포 간선 (category 「제주/서귀포 간선」) ending at 모슬포 남항 여객선 터미널(운진항) | marado [33] | CONFIRMED (406056, eff. 2026-03-03) |
| 151 alighting stop 「모슬포 남항 여객선 터미널(운진항)」 | marado [33] | CONFIRMED on Visit Jeju CNTS_000000000019004 (visible body). The BIS sheet calls it 모슬포남항(운진항)(종점); that variant is harmless. |
| 281 is 일반간선 and 475 is 지선, so both take the 간/지선 fare; 181 is 급행 | hallasan [29], [31] | CONFIRMED |
| 475: 06:20–19:45, every 45–90 min, via 산천단(한국폴리텍대학) | hallasan [30] | CONFIRMED |
| 281 and 181 both use the 5.16 road | hallasan [28] | CONFIRMED |
| **281: 06:00–22:00, every 10–14 / 11–17 min; 181: 06:10–22:29, every 30–45 min, about 35 min** | **hallasan [29]** | **CONFLICT** (see below) |

## Problem found (1)

**hallasan-hiking-reservation-guide blocks[29], consistency.**
- The 281 and 181 schedules copy visithalla `contents.do?id=61` exactly (re-read today, 200).
- Jeju's own bus information system publishes the operator's route timetables, and they differ:
  - **281** (sheet 405019, operator 동진여객, effective 2026-06-24): first bus from Jeju Bus Terminal **05:40**, first from Seogwipo Bus Terminal **05:55** (05:50 from the old terminal), last **22:00** both ways, every **10–20 min**.
  - **181** (sheet 405007, effective 2024-08-01): first bus from the airport **06:40** (an earlier 06:00 trip starts at Jeju Bus Terminal), last from the airport **22:15**, every **40–60 min**, 38–46 min from the airport to Seongpanak.
- Batch-8 README §本批與第七批不同的地方 rule 3: use one version for the numbers (the operator by default) and disclose the other in one sentence or bracket.
- Impact on readers is small: the 281 last bus agrees, and the BIS first bus is earlier. But for 181, the article's 06:10 first bus from the airport is 30 minutes earlier than the operator sheet's 06:40.
- This block was not in the round-1/2 fix set or round 2's random third. It came up only because bus.jeju.go.kr opened today.

## Still unverifiable
- cmcity.go.th:
  - Night-markets claims that cannot be checked: [0] item 3, [5] row 1, [9], [11], [12], [14], [37], and Jing Jai's registered name (page 488).
  - Cause: Apache 403 at the origin for every client.
- songakferry.com:
  - Marado claims that cannot be checked: the Songak column of [5], [8], the end of [13], the Songak half of [14], and the 30-minute Songak leg on the diagram.
  - Cause: the operator blocks every request.
- 181: which timetable is current. The BIS sheet dates from 2024-08-01.

## Verdict
- The three round-2 changes are correct.
- Of the sources rounds 1–2 could not open, three now check out: the TAT Big Buddha hours, the Sanctuary of Truth page, and every bus.jeju.go.kr fare and route claim.
- One new consistency item, hallasan [29], should be fixed or disclosed under rule 3. It is not a fact error a reader would be stranded by.
- cmcity.go.th and songakferry.com still cannot be read from this environment.

## Round-3 corrections as applied on the branch (2026-10-06)

Before the change, both versions were re-opened on 2026-10-06 in headless Chromium with the same User-Agent and no personal data; TLS verification stayed on. The pack has only the zh-TW locale, so no other locale needed a change.

**What the sources say today**
- `bus.jeju.go.kr/publicTrafficInformation/generalBusSchedule?viewtype=2` (200). The route list came from the page's own `POST /publicTrafficInformation/getBusRouteNum` (`GROUTE_TYPE=4` lists `405007 181`, `GROUTE_TYPE=3` lists `405019 281`), and the workbooks from `/data/schedule/downScheduleExcel?gscheduleId=…`, both fetched from inside the rendered page.
  - 405019 (281), two sheets, both 「배차간격 10~20분, 동진여객」「시행일 : 2026. 6. 24.」. 제주터미널→서귀포터미널: 「첫차 5:40, 막차 22:00」, first row 제주버스터미널 05:40 → 성판악 06:21. 서귀포터미널→제주터미널: 「첫차(구. 버스터미널 출발) 5:50, 막차 22:00」; row 1 starts at 서귀포시 구 버스터미널 05:50 (its 서귀포버스터미널 cell is X), row 2 leaves 서귀포버스터미널 at 05:55, and the last row leaves at 22:00.
  - 405007 (181), one sheet, 「배차간격 40~60분, 동진여객」「시행일 : 2024.8.1.」. The first row with a 공항 time is 06:40 (→ 성판악 07:26). Row 2 has 공항 X and starts at 제주버스터미널 앞 06:00 (→ 성판악 06:35). The last 공항 departure is 22:15 (→ 성판악 22:53). 공항→성판악 is 46 min on most trips and 44, 40 and 38 on the last three. The header's 「첫차(서귀포중앙R 출발) 6:05」 is the start of the loop at Seogwipo and does not serve Seongpanak.
- `visithalla.jeju.go.kr/contents/contents.do?id=61&language=ko` (200; without the language parameter the page serves the English version, which has no bus numbers). Unchanged: 「281번 … 첫차 06:00, 막차 22:00 (배차간격 10~14분) … 약 45분」「(서귀포시→제주시) 첫차 06:00, 막차 22:00 (배차간격 11~17분) … 약 50분」「181번 … 첫차 06:10, 막차 22:29 (배차간격 30~45분) … 약 35분」.

The correction is right. Under README rule 3 the numbers now follow the operator's sheets, and the park site's version is disclosed in one sentence.

**Changes in `hallasan-hiking-reservation-guide`**
1. blocks[29] item 1: 「281 號（一般間線）：首班 06:00、末班 22:00，班距 10 到 14 分（西歸浦開往濟州方向 11 到 17 分）；…」 now reads 「281 號（一般間線）：濟州巴士轉運站首班 05:40、西歸浦巴士轉運站首班 05:55（西歸浦舊巴士轉運站另有一班 05:50），末班兩頭都是 22:00，班距 10 到 20 分；從濟州巴士轉運站上車約 45 分，從西歸浦巴士轉運站上車約 50 分。」
2. blocks[29] item 2: 「181 號（急行，從濟州國際機場出發）：首班 06:10、末班 22:29，班距 30 到 45 分，約 35 分。」 now reads 「181 號（急行，從濟州國際機場出發）：機場首班 06:40、末班 22:15，班距 40 到 60 分，機場到城板岳 38 到 46 分；另有一班 06:00 從濟州巴士轉運站發車、不經機場。」
3. blocks[28]: the rule-3 disclosure is appended after 「281 與 181 都走 5.16 道路。」: 「下面的時刻照業者在濟州巴士資訊系統公布的時刻表；漢拏山探訪預約系統的城板岳介紹頁寫的是另一版（281 首班 06:00，181 首班 06:10、末班 22:29）。」 No block was added, so later block indices are unchanged.
4. blocks[36] repeated the same first buses before the hotel offer: 「281 首班 06:00、181 首班 06:10。」 now reads 「281 濟州巴士轉運站首班 05:40、西歸浦巴士轉運站首班 05:55，181 機場首班 06:40。」 Leaving it would have contradicted [29].
5. sources: the bus.jeju.go.kr title now also names 「281 與 181 的業者時刻表（2026 年 6 月 24 日、2024 年 8 月 1 日施行）」. The id=61 source stays, because the disclosure cites it.

**Kept on purpose**
- The 281 ride times 約 45 分 and 約 50 分 agree with both versions. The BIS sheets give 37 to 44 min from 제주버스터미널 to 성판악 (44 on 52 of the 72 trips, 41 to 44 on all but the 21:45 and 22:00) and 46 to 52 min from 서귀포버스터미널 (52 on 54 of the 71 trips).
- [32] still sends readers to Naver Map or Kakao Map for the day's buses. That covers the open question of which 181 timetable is current.
- The spec `docs/travel-guides-batch-8/hallasan-hiking-reservation-guide.md` (lines 120–121, 276 and its rule (11) at 335) still gives the visithalla numbers and says every bus time follows the park site. README rule 3 is the later batch-wide rule, so the article now departs from the spec on these numbers. The spec was not edited.
- No other content pack carries a 281 or 181 schedule (`git grep`; `jeju-3-day-itinerary` has none), and `shared-numbers.json` has no rule on them.

**Checks (from `apps/api`, after `uv sync --frozen`)**
- `uv run python -m app.guides.pack_cli lint --slug hallasan-hiking-reservation-guide`: exit 0.
- `intake_check.py --slug hallasan-hiking-reservation-guide --from-content --manifest docs/travel-guides-batch-8/batch.json`: PASS (0 failures). body_length 4067 in the 1800–4200 band. The five WARN lines are in the unchanged description and summary. Both diagrams pass "every number on the diagram is in the text". The slug is not on origin/main, so there is no baseline to regress against.
- `shared_check.py --rules docs/travel-guides-batch-8/shared-numbers.json --from-content`: PASS (0). Only two jeju info counts changed (濟州巴士轉運站, 漢拏山).
- `pytest tests/test_guides_content_pack.py -q`: 9 passed, 5 skipped.
- `tasks/` was not changed.

# verify-4 (wave 2): Round-4 independent fact-check: PR #1335 (claude/batch-8-wave-2)

Two independent verifiers checked head `1f8f4919c06c9cb80627ac6f3ce464c39157f098` on 2026-10-06. Verifier A re-checked the round-3 fix in `hallasan-hiking-reservation-guide`. Verifier B worked around the two hosts no earlier round could open (`cmcity.go.th`, `songakferry.com`). Both reports follow as delivered, with headings moved down one level. The corrections applied after them are at the end.

## Round-3 fix re-check: PR #1335 (claude/batch-8-wave-2)

- **Head checked:** `1f8f4919c06c9cb80627ac6f3ce464c39157f098`. I fetched it before starting and again at the end, and it did not move. The tip commit is 「content: independent fact-check round 3 for #1335」.
- **Read-only:** no edits, commits, pushes or comments. The working tree is clean.
- **Fetching:**
  - Every request used the UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` and carried no personal data. TLS verification stayed on.
  - curl still fails TLS on bus.jeju.go.kr, so that host was read in headless Chromium (HTTP 200) with the page's own `POST /publicTrafficInformation/getBusRouteNum` and `/data/schedule/downScheduleExcel?gscheduleId=…`.
  - I cross-checked the workbooks against the rendered `/schedule/viewNew/181`, `/schedule/viewNew/281` and `/schedule/view/181` pages.
  - visithalla, visitjeju and jeju.go.kr were read with `curl -sSL`, with comments, scripts and styles stripped.

### Result

22 claims checked, 22 confirmed, **0 errors**. Every number the round-3 commit changed in `hallasan-hiking-reservation-guide` is correct. The disclosure sentence is accurate and meets README rule 3. No other article in the batch now contradicts it.

### What I checked against what

| Block | Claim | Source today | Outcome |
|---|---|---|---|
| [29] 281 | Jeju Bus Terminal first bus 05:40; Seogwipo Bus Terminal first bus 05:55; extra 05:50 from the old Seogwipo terminal; last bus 22:00 both ways; every 10–20 min | BIS 405019, both sheets, 「시행일 : 2026. 6. 24.」, 동진여객 | CONFIRMED (computed gaps are 10–20 both ways) |
| [29] 281 | 約 45 分 / 約 50 分 | same | Consistent: 37–44 min (44 on 52 of 72 trips) and 46–52 min (52 on 54 of 71 trips) |
| [29] 181 | Airport first bus 06:40, last 22:15, every 40–60 min, 38–46 min to Seongpanak; a 06:00 trip starts at Jeju Bus Terminal and skips the airport | BIS 405007, 「시행일 : 2024.8.1.」 | CONFIRMED. Airport→Seongpanak is 46 min on 16 of 19 trips, then 44, 40 and 38 |
| [28] | Disclosure: visithalla has 281 first bus 06:00, 181 first bus 06:10 and last bus 22:29 | visithalla `contents.do?id=61&language=ko` (200) | CONFIRMED word for word: 281 「첫차 06:00, 막차 22:00 (10~14분 / 11~17분)」, 181 「첫차 06:10, 막차 22:29 (30~45분) 약 35분」 |
| [36] | 281 05:40 / 05:55, 181 06:40 | same sheets | CONFIRMED, agrees with [29] |
| sources | Sheets effective 2026-06-24 and 2024-08-01 | BIS notice 685 (281/282 timetable change effective 2026-06-24); notice 537 (2024-08-01 express reorganization; its 181 attachment matches 405007 cell for cell) | CONFIRMED |

**README rule 3**
- The numbers follow one version, the BIS route sheets.
- The other version is disclosed in one sentence and is not offered as a second option.
- The narrower-window clause does not apply, because the dates settle which version is current:
  - BIS notice 685 documents the 281 change of 2026-06-24.
  - The visithalla 181 figures match the **superseded 2021-09-10 sheet** (notice 360): first departure 06:10 from Jeju Bus Terminal, 35 min to Seongpanak, last bus 22:29 at Jeju Bus Terminal, header 30~65분.
  - So the park page has not been maintained ("疏於維護"), which independently supports the choice.

### Is there a newer 181 timetable than 2024-08-01?

**No.**
- **BIS:** the route list has a single 181 entry (gscheduleId 405007, scheduleId 1399). Searching notices by subject and content for 181/182/급행/시간표 shows these 181 timetable or stop notices, and none after 537:
  - 360: timetable, effective 2021-09-10
  - 437: stop designation, effective 2023-08-10
  - 537: 2024-08-01 reorganization
- **visitjeju.net:** the 181 article (CNTS_300000000013541) links to the BIS timetable instead of carrying one. Its 10:40 airport departure matches the 2024 sheet. Its 「30분~65분」 headway is the 2021 header.
- **jeju.go.kr (Hallasan park, course07.htm):** sends readers to the BIS and has no times.

### Cross-batch consistency

- **marado-gapado-ferry-day-trip:** has routes and fares but no 281/181 times.
- **jeju-3-day-itinerary:** has no 281/181 times.
- **Diagrams:** no Jeju diagram SVG carries bus times.
- **shared-numbers.json:** the `jeju` rules still hold on the branch packs (my replication of the patterns passes). It has no 281/181 rule.
- **FOLLOWUPS / ERRATA:** do not mention these times.

### Observations, not reported as errors

- **Wording of [28].** It calls the sheets 「業者在濟州巴士資訊系統公布的時刻表」. The sheets carry 동진여객's name, but the system is the province's BIS, and the notices point to 도청 대중교통과. This is accurate enough; the rule-3 choice holds either way.
- **The spec is out of date.** `docs/travel-guides-batch-8/hallasan-hiking-reservation-guide.md` (lines 120–121, 276, rule (11) at 335) still has the visithalla numbers. Round 3 already recorded this.
- **The return direction is still undocumented.** visithalla lists 182 (서귀포→5.16→공항) for the return; the article names only 281 for that direction and leaves the day's buses to Naver Map or Kakao Map [32]. This was there before round 3.

### Still unverifiable

- **The 281 attachment to notice 685.** `/notice/download/1067` returns 200 with 0 bytes. The sheet 405019 and the notice text agree on 2026-06-24, so the numbers stand.
- **A visitjeju Seongpanak transport page with times.** I could not find one on visitjeju.net.


---

## Blocked-source check: PR #1335 (claude/batch-8-wave-2)

- **Head:** `1f8f4919c06c9cb80627ac6f3ce464c39157f098`. I fetched it before starting and again at the end; it did not move.
- **Read-only:** I made no edits, commits, pushes or comments. Scripts and downloads stayed in the session scratchpad.
- **Requests:** every request used the UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)` and sent no personal data. TLS verification was never disabled.

### How I got around the 403s

Both hosts still refuse every client from here:
- `cmcity.go.th` returns Apache 403 on `www.` and on the bare domain.
- `songakferry.com` and `songakferry.imweb.me` return the imweb block page.
- `web.archive.org`, `index.commoncrawl.org` and `archive.ph` reset the connection.

Three routes worked:
1. **Common Crawl WARCs**, read through `data.commoncrawl.org`, which is reachable. I binary-searched each crawl's `cluster.idx` with HTTP Range requests, read the CDX block, then range-fetched the WARC record. These are the crawler's own copies of the official pages; I stripped comments, scripts and styles before reading.
   - `songakferry.com/time_regular` and `/price`: captured **2026-09-06** (CC-MAIN-2026-39).
   - `cmcity.go.th/list/page/496/ประวัติความเป็นมา/`: captured **2024-10-09** (CC-MAIN-2024-42), plus 2024-03, 2024-04, 2024-07 and 2023 copies with the same text. Page 488 was captured 2024-03-01.
2. **Korea Shipping Association booking system** (`island.theksa.co.kr`, 한국해운조합). Songak Ferry's own "공식예매" link points to it (`sourcesiteid=FLL7Y2TE5B9V1UBIIN9G`). I read it live through `/booking/selectPairPortList` and `/booking/selectDepartureList`.
3. **TAT head office Thai pages**, live in headed Chromium under xvfb: `thai.tourismthailand.org/Shop/ถนนคนเดินประตูท่าแพ` and `/Shop/ถนนคนเดินเชียงใหม่`. The English pages carry only an address.

### (1) chiang-mai-night-markets-walking-streets

I checked every claim that rests on cmcity against the archived official page. All of them match except one wording point:

| Claim (blocks) | Result |
|---|---|
| Sat/Sun road closures by the municipality ([0], [9]) | Confirmed |
| Wualai: near Chiang Mai Gate, Sat only, about 17:00–22:00, local vendors so smaller than Tha Phae, silver village ([0], [5], [16], [17], [37]) | Confirmed |
| Sunday: Ratchadamnoen × Phra Pokklao crossing at สี่แยกกลางเวียง, from Tha Phae Gate to Wat Phra Singh, Sunday only, about 17:00–22:00, largest and most famous ([0], [5], [12], [37], diagram) | Confirmed. TAT HQ's live page also says Sunday only, 17.00–22.00 and gives the same route |
| About 1.5 km ([0], [5], [9], [11], [37], diagram) | Confirmed (「ระยะทางประมาณ 1.50 กิโลเมตร」); TAT has a different figure, see notes |
| 2545 start on Tha Phae Rd; moved to Ratchadamnoen 31 Aug 2547; hours changed to 15:00–22:00 ([9], [37]) | Confirmed |
| Goods, food, massage booths, portraits, music and busking incl. human statues ([13]) | Confirmed |
| Five named temples incl. Chedi Luang and Phra Singh; lit up, selling allowed on the grounds ([14]) | Confirmed |
| 「市政府的頁名仍叫塔佩步行街（ถนนคนเดินท่าแพ）」 ([9]) | **Wrong (minor).** The page is titled ถนนคนเดินเชียงใหม่ ＞ ประวัติความเป็นมา; ถนนคนเดินท่าแพ is the body's name for the Sunday street. Change to 「市政府的頁面仍把週日這條叫塔佩步行街」 |
| Jing Jai registered name จริงใจ Farmers Market ([26]) | **Still unverifiable.** The 2566 PDF was never captured |

### (2) marado-gapado-ferry-day-trip: Songak column

Everything is confirmed, by the operator's own page (2026-09-06 copy) and by today's KSA data:
- **Two timetable sets** ([5], [8]):
  - 09:20-first: 09:20, 10:50, 12:40, 14:10; returns 11:30, 13:20, 14:50, 16:10; stays 1h40, 2h, 1h40, 1h30; plus 15:30 「편도(숙박)」.
  - 10:00-first: 10:00, 11:50, 13:30; returns 12:30, 14:10, 15:30; stays 2h, 1h50, 1h30; plus 14:50 「편도(숙박)」.
- **Which set runs when:** KSA has the 10:00 set on Oct 7–8 and the 09:20 set on Oct 9–31. November is not on sale yet.
- **Stays of 1h30–2h** and **the last row being 편도(숙박)** ([5], [13], [14]): confirmed.
- **30 min crossing** ([5], diagram): KSA says 「0시간 30분」.
- **Fare** ([5], [8]): 20,000 + 1,000 = 21,000, excluding the fuel surcharge. The price table's column is 왕복요금, and KSA's adult fare is 10,000 per leg.
- **Songak goes only to Marado:** KSA's port-pair list for this operator has only 송악산 산이수동 ↔ 마라도.

### Notes (not reported as errors)

- **The 1.5 km figure has a second official value.** Both TAT HQ's live Thai page (「รวมระยะทางประมาณ 1 กิโลเมตร」) and TAT Tokyo (約1km) give about 1 km. The spec's rule (3) forbids writing both, and round 1 ruled the spec overrides README rule 3 for this pack, so I left it alone. The new evidence does help on hours: TAT HQ now agrees with the municipality on 17:00–22:00, so only TAT Tokyo still says 24:00.
- **Where readers can see the day's Songak set.** The operator site posts both sets with no dates, while KSA's booking shows which one runs on a given date. [8]'s 「出發前看官網當天用的是哪一套」 could point readers to the operator's booking page. This is optional.
- **편도(숙박) sailings are not bookable online.** They do not appear in KSA online booking, which fits overnight guests booking by phone.
- **One-way prices on the Songak price page.** Besides the 왕복요금 table, the page lists 마라도주민 1,000원(편도) and a VIP-room surcharge (편도 20,000 / 왕복 30,000). 「票價頁只列來回票價」 holds for ordinary passengers.
- **`checked_on: 2026-10-06` on the cmcity and songakferry sources.** These hosts are 403 here, but the writer worked from a different machine (see the launch ticket), so this is not evidence the pages were not opened. The content matches the archive copies either way.
- **Gapado [12] (14:20 printed twice).** I did not re-check it; it was out of scope.

### Still unverifiable

- **Jing Jai's registered name** (cmcity 2566 PDF). It is in no Common Crawl index from 2023 to 2025-47. The live host is 403, the Wayback, archive.ph and CC index servers reset, data.go.th returns 403, and chiangmai.go.th serves a self-signed certificate, which I did not bypass.
- **Whether cmcity page 496 changed after 2024-10-09.** No newer capture exists; Common Crawl also got 403 on 2026-09-11. The spec's 2026-09-20 quotes match the 2024 copy word for word.

### Verdict

- **Songak column:** fully confirmed; nothing to change.
- **Night markets:** every cmcity claim except one matches the official page as archived, and the live TAT HQ page corroborates the hours and route.
- **To fix:** one minor wording error in night-markets [9] (「頁名」).
- **Still open:** Jing Jai's registered name.

## Round-4 corrections as applied on the branch (2026-10-06)

Before changing anything I re-opened the sources myself, with the same User-Agent and no personal data. TLS verification stayed on. The pack has only the zh-TW locale, so no other locale needed a change.

**1. Night markets blocks[9], 「頁名」: applied.**
- The live page `www.cmcity.go.th/list/page/496/ประวัติความเป็นมา/` still returns 403 (401 bytes) to curl.
- I range-fetched the Common Crawl record the verifier cited: CC-MAIN-2024-42, offset 33144695, length 23815. The fetch returned HTTP 206 with 23,815 bytes. The record's WARC-Date is 2024-10-09T12:52:56Z and its target URI is the page-496 URL.
- After I stripped comments, scripts and styles, the page reads as follows:
  - The `<title>` is เทศบาลนครเชียงใหม่.
  - The breadcrumb is ขณะนี้คุณอยู่ที่ > หน้าแรก > ประวัติความเป็นมา.
  - The content heading is ถนนคนเดินเชียงใหม่, then ประวัติความเป็นมา.
  - ถนนคนเดินท่าแพ appears only in the body, twice: 「จึงมีขนาดเล็กกว่าถนนคนเดินท่าแพ」 and 「ถนนคนเดินวันอาทิตย์ (ถนนคนเดินท่าแพ)อยู่บนถนนราชดำเนินและถนนพระปกเกล้า」.
- The verifier is right. 「市政府的頁名仍叫塔佩步行街（ถนนคนเดินท่าแพ），攤位卻在 Ratchadamnoen 路上。」 now reads 「市政府的頁面仍把週日這條叫塔佩步行街（ถนนคนเดินท่าแพ），攤位卻在 Ratchadamnoen 路上。」
- No number changed. The title of source 0 (「ถนนคนเดินเชียงใหม่ 沿革與一般資料」) already matched the page heading, so it stays.
- The spec has the same wording at line 50 and in rule (4) at line 167. `ERRATA.md` says spec files are not edited after the fact, so the spec stays as it is. The error is recorded in `ERRATA.md` under 第二波, in the chiang-mai section.

**2. Night markets blocks[26], Jing Jai's registered name: attribution added, value unchanged.**
- No official source I can reach confirms it.
- I extended the verifier's Common Crawl search to the ten crawls it had not covered: CC-MAIN-2025-51 and CC-MAIN-2026-04, -08, -12, -17, -21, -25, -30, -34 and -39.
  - None of them has a capture of `cmcity.go.th/Download/…`, of page 488 or of page 496.
  - The search itself works: the same crawls hold other cmcity URLs, such as the homepage, `/list/page/334/…`, `/list/page/411/…` and `/list/pdf/…`.
  - So the market PDF was never crawled. The live host is still 403.
- The sentence already named the municipality as the source. It now also gives the document's year, as [32] dates the TAT Tokyo bus hours (「泰國觀光局東京辦事處寫 2024 年 11 月當時…」).
  - 「Jing Jai 市集（Jing Jai Market，市政府登記名稱是 จริงใจ Farmers Market）」 now reads 「Jing Jai 市集（Jing Jai Market，市政府 2023 年版市場資料上的登記名稱是 จริงใจ Farmers Market）」.
  - 2023 is Thai year 2566. That year appears in the attachment name the verifier saw on the 2024-03-01 capture of page 488 (「ข้อมูลตลาดในเขตเทศบาลนครเชียงใหม่ 2566.pdf」) and in the title of source 1 (「市場資料表 2566 年版」).
  - No name or number was invented.

**Not changed**
- **Hallasan (verifier A):** 22 of 22 confirmed, so there was nothing to apply. Its two still-unverifiable items are not claims the article makes:
  - The 281 numbers rest on sheet 405019 and the notice text, not on the 0-byte attachment.
  - The article cites no visitjeju Seongpanak page.
- **Marado, Songak column:** confirmed by the 2026-09-06 operator copy and by live KSA data. The block page on the live songakferry.com does not affect any sentence.
- **Night markets, whether page 496 changed after 2024-10-09:** no attribution added, for three reasons:
  - [9] already attributes the history to the municipal page.
  - The spec's 2026-09-20 quotes match the 2024 copy word for word.
  - TAT HQ's live page corroborates the hours and the route.
- **Gapado [12], 14:20 printed twice:** no change. The article itself already says 「官網把加波島「島上出發」的 14:20 寫了兩次…上表只列一次」, so this describes the source and is not a duplication error.
- **Optional notes not applied, because they are not errors:**
  - Pointing [8] to KSA booking.
  - 편도(숙박) sailings not being bookable online.
  - The one-way prices on the Songak price page.
  - TAT's 1 km figure. The spec's rule (3) also bars it, as round 1 ruled.

**Checks (from `apps/api`, after `uv sync --frozen`)**
- `uv run python -m app.guides.pack_cli lint --slug chiang-mai-night-markets-walking-streets`: exit 0.
- `intake_check.py --slug <slug> --from-content --manifest docs/travel-guides-batch-8/batch.json`: PASS (0 failures) on all seven wave-2 slugs.
  - Night markets: body_length 3697, inside the 1800–4200 band.
  - The night-markets diagram still passes "every number on the diagram is in the text".
- `shared_check.py --rules docs/travel-guides-batch-8/shared-numbers.json --from-content`: PASS (0). Its output is identical before and after the change.
- `pytest tests/test_guides_content_pack.py -q`: 9 passed, 5 skipped.
- `tasks/` was not changed.
