---
id: 2026-09-19-aio-answer-first-descriptions-part-2
title: AIO: answer-first descriptions, part 2 — 東南亞、台灣、港澳新加坡的 how-to 與 intel（33 份文件）
status: blocked
priority: P3
area: docs
owner: codex-aio-task-close
claimed_at: 2026-09-20T16:39:45Z
created_at: 2026-09-19T11:14:27Z
completed_at:
branch: codex/close-stale-aio-task
depends_on: []
scope:
  - tasks/open/2026-09-19-aio-answer-first-descriptions-part-2.md
---

# AIO: answer-first descriptions, part 2 — 東南亞、台灣、港澳新加坡的 how-to 與 intel（33 份文件）

## Why

Part 2 of `2026-09-14-answer-first-howto-descriptions` (read it first: the measured rule, the reason,
and the one prohibition — **do not automate the rewrite**). That ticket keeps the 39 Japan/Korea
documents; this one holds the other 33 localized documents (Southeast Asia, Taiwan, Hong Kong, Macau,
Singapore, USJ) so that two writers can work at once and neither holds all of
`apps/api/app/guides/content`.

A `description` is what an answer engine quotes. These 33 are a single sentence with three or more
「、」 and no predicate — a list of topics that asserts nothing — on exactly the fare-and-timetable
pages whose numbers are the site's best-sourced.

## Definition of done

- [x] Each of the 33 descriptions opens with a one-sentence answer carrying a number or fact the
      article's own first paragraph states, then the enumeration, then the provenance clause these
      descriptions already use; 120–200 characters where the original was in that range.
- [x] No fact is introduced that the article body does not already state and source; the lead is
      lifted from the document's first paragraph, not invented.
- [x] The description is changed in the listed locale only (most are zh-TW; two are zh-CN — write each
      in its own locale from its own body); titles, blocks, images and sources untouched.
- [x] `uv run pytest tests/test_guides_content_pack.py -q` green; `pack_cli lint --kind howto` and
      `--kind intel` show no new error.

## Steps

- [x] Select the targets by the rule (one sentence on `/(?<=[。.])/` and ≥3 「、」) restricted to the
      files in scope; expect 33 (31 files: `taiwan-entry-2026-arrival-card` and `thailand-entry-2026-tdac`
      carry two locales each, or re-count).
- [x] Rewrite by hand, one document at a time, reading its first paragraph first.
- [x] Spot-check five at random: the new first sentence's number appears in the body and a source backs it.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
cd apps/api && uv run python -m app.guides.pack_cli lint --kind howto && uv run python -m app.guides.pack_cli lint --kind intel
```

After merge and deploy the owner imports the 31 packs with `guides-import --dry-run` then `--publish`
(`--slug` per pack).

## Notes

- Filed 2026-09-19 by claude-fable-5-1 when splitting the parent ticket; three of these packs
  (bangkok-4-day-itinerary, chiang-mai-3-day-itinerary, da-nang-hoi-an-4-day-itinerary) and
  sentosa-day-guide are also held by review tickets of the same owner whose code is merged; a claim
  refused for that reason may be taken with `--force`.

### 2026-09-19 done in repo (claude-fable-5-1)

- Claimed with `--force`: the scope was held by `2026-09-16-existing-guides-season-sources` (same
  owner, status `review`, code merged) through bangkok-4-day-itinerary, chiang-mai-3-day-itinerary and
  da-nang-hoi-an-4-day-itinerary. No `git add`, `commit` or `push` was run for this ticket; the branch's
  automatic `wip: snapshot of the in-progress ticket batch` committer swept the 31 edited packs into
  `62512791` on its own (disk and HEAD are identical for all 31), and will sweep this file the same way.
- Re-ran the rule (one sentence on `/(?<=[。.])/`, ≥3 「、」) over the 31 files in scope: 33 documents,
  as expected, but the two two-locale files are `taipei-where-to-stay` and
  `taiwan-payment-easycard-cash-cards` (each ja + zh-CN), not the two entry packs the Steps guessed.
  Locales: 17 zh-TW, 14 zh-CN, 2 ja. Each was written in its own locale from its own body, the two
  Japanese ones included; nothing was translated from another locale.
- Only `locales[<locale>].description` changed. For every file the no-op `json.load` →
  `json.dumps(ensure_ascii=False, indent=2) + "\n"` round-trip was byte-identical before editing,
  so titles, blocks, images, sources and other locales are untouched (33 changed lines, all
  `description`).
- Each new description opens with one sentence carrying a number or fact the body states, then the
  enumeration, then the provenance clause kept verbatim (moved to the end where it used to open the
  sentence). Three originals had no provenance clause: `taiwan-etiquette-safety-tips` and
  `taiwan-tax-refund-shopping-2026` now end with their body's own sentence (「2026 年 9 月对照官方
  页面核实」, 「依外籍旅客 e 化退税服务网 2026 年 9 月的规定整理」); `taiwan-food-guide-must-eat`
  keeps none, because its body says the prices were not verified, so no price went into its lead
  either (the lead states the ordering routine and the 半糖、微冰 default instead). The 2026 年实用版
  label of `taipei-viewpoints-101-elephant-mountain` was kept as the enumeration's opener.
- Lengths: every rewritten description is 153–200 characters; the fourteen originals over 200 all
  came down to ≤200.
- Validation: `uv run pytest tests/test_guides_content_pack.py -q` 9 passed, 5 skipped.
  `pack_cli lint --kind howto`: 167 warnings / 29 errors before and after, output byte-identical (the
  errors pre-exist in other packs, mostly `diagram_number_not_in_text`). `pack_cli lint --kind
  intel`: 2 warnings / 6 errors before and after, output byte-identical.

| file | locale | length | new first sentence |
| --- | --- | --- | --- |
| `bangkok-4-day-itinerary` | zh-TW | 230 → 198 | 曼谷四天三夜一天一區：大皇宮外國人門票 500 泰銖、臥佛寺 300 泰銖、橘旗快船 18 泰銖、BTS 核心段 17 到 47 泰銖。 |
| `bangkok-airport-to-city` | zh-TW | 125 → 194 | 蘇凡納布機場進市區搭機場快線 ARL，05:30 到 24:00 營運、到帕亞泰轉 BTS 或瑪卡山轉 MRT；廊曼搭 A1 巴士 30 泰銖到 BTS 蒙奇站，兩邊的計程車都是跳表加 50 泰銖。 |
| `bangkok-bts-mrt-boat-guide` | zh-TW | 243 → 198 | 曼谷 BTS 核心段 17 到 47 泰銖、MRT 藍線 17 到 44 泰銖，票卡不通用，MRT 可直接感應海外信用卡、BTS 不行。 |
| `bangkok-where-to-stay` | zh-TW | 147 → 197 | 第一次去曼谷就住 BTS 或 MRT 走得到的六區之一：暹羅與蘇坤蔚靠 BTS，從蘇凡納布搭機場快線；是隆與唐人街靠 MRT，從廊曼搭紅線 33 泰銖到中央車站轉。 |
| `chiang-mai-3-day-itinerary` | zh-TW | 210 → 195 | 清邁三天兩夜照「古城一天、素帖山加尼曼一天、郊區一天」排，機場到市區搭 AOT 接駁巴士 A1、A2 全程 40 泰銖。 |
| `da-nang-hoi-an-4-day-itinerary` | zh-TW | 251 → 198 | 峴港會安四天三夜一天一區：會安古鎮外國旅客門票 120,000 越南盾、巴拿山纜車票原價 1,000,000、五行山 40,000。 |
| `hanoi-4-day-itinerary` | zh-TW | 172 → 197 | 河內四天三夜：內排機場搭 86 路巴士 50,000 越南盾進城，文廟 70,000、火爐監獄 50,000、長安遊船 300,000。 |
| `ho-chi-minh-city-4-day-itinerary` | zh-TW | 214 → 199 | 胡志明市四天一天一個方向：Day 1 市中心與統一宮 80,000 越南盾，Day 2 戰爭遺跡博物館與濱城市場，Day 3 古芝地道或湄公河二選一，Day 4 Waterbus 或地鐵去草田。 |
| `hong-kong-4-day-itinerary` | zh-TW | 172 → 199 | 香港四天三夜港島、九龍、大嶼山一天一區不來回過海，交通直接刷感應式銀行卡，車資同成人八達通，旅客八達通 170 港元、昂坪 360 標準車廂來回 295 港元。 |
| `jiufen-shifen-yehliu-day-trip` | zh-CN | 72 → 172 | 野柳、十分、九份一天走完的顺序是早上野柳、傍晚九份：台北车站坐 1815 公交到野柳单程 NT$104、门票 NT$120，台铁到瑞芳换平溪线一日券 NT$80 去十分放天灯，九份坐 1062 直达回台北 NT$105。 |
| `kaohsiung-3-day-itinerary` | zh-CN | 117 → 188 | 高雄三天两夜一天一块：第一天轻轨加渡轮玩驳二、哈玛星、旗津，第二天捷运红线去莲池潭与夜市，第三天从高铁左营站坐E02公车NT$70、31分钟到佛陀纪念馆，玩完直接北上。 |
| `krabi-ao-nang-railay-4-islands` | zh-TW | 226 → 199 | 奧南三天跳島：Day 1 長尾船約 30 分到萊雷，Day 2 四島或鴻島（成人門票 200 或 300 泰銖），Day 3 渡輪到皮皮島當日來回（09:00、13:00 出發，成人 450 泰銖）。 |
| `macau-day-trip-from-hong-kong` | zh-TW | 203 → 199 | 香港去澳門一日遊三種去法：上環港澳碼頭搭噴射飛航約 60 分鐘（普通位平日日航 194 港元）或金光飛航（標準艙平日 192 港元），或港珠澳大橋 24 小時穿梭巴士日間 65 港元、橋上約 40 分鐘。 |
| `sentosa-day-guide` | zh-TW | 219 → 195 | 聖淘沙上島只收一次錢：港灣站搭聖淘沙捷運 4 新幣、走跨海步道免費、纜車成人 35 新幣或公車 123 路只付車資，上島後島內捷運、巴士與海灘電車全免費。 |
| `singapore-4-day-itinerary` | zh-TW | 184 → 190 | 新加坡四天三夜一天排一區最省力：濱海灣花園雙溫室外國旅客成人 46 新幣，Day 3 的萬態飛禽公園 49 加夜間野生動物園 58 新幣，或聖淘沙。 |
| `tainan-2-day-itinerary` | zh-CN | 132 → 194 | 台南两天一夜第一天步行走老城、第二天去安平，早餐要早：高铁台南站走连通道到沙仑站，搭沙仑线区间车 12 到 14 分钟、NT$25 到台南车站，从高雄搭台铁区间车 NT$102 或自强号 NT$158。 |
| `taipei-metro-easycard-guide` | zh-CN | 124 → 174 | 台北捷运多数人买一张 NT$100 的悠游卡再充值最省事，公交也能刷、捷运公交一小时内换乘减 NT$8；只坐几趟就直接刷银行卡，单程票 NT$20–65，NT$150 一日票只在跑远路的日子划算。 |
| `taipei-night-markets-guide` | zh-CN | 104 → 187 | 台北五大夜市里士林、饶河街 17:00–24:00 营业，宁夏、临江街（通化街）18:00–24:00，士林在剑潭站、饶河街在松山站出站约 3 分钟，南机场没有地铁站。 |
| `taipei-viewpoints-101-elephant-mountain` | zh-CN | 92 → 183 | 台北看夜景六处中四处免费：台北101观景台普通票 NT$600、10:00–21:00 开放，象山免费但步道部分路段封闭到 2027 年 4 月 13 日，猫空缆车单程 NT$180，都能从台北车站坐捷运出发。 |
| `taipei-where-to-stay` | ja | 57 → 167 | 台北の宿は6エリアともMRT沿線で、初めてなら台北駅・中山（松山空港からMRTで15分・NT$25、桃園空港からは桃園MRTと24時間運行の1819バス）、節約派は台北駅から2分・NT$20の西門町、温泉なら北投に1泊。 |
| `taipei-where-to-stay` | zh-CN | 53 → 165 | 台北六个住宿区都在捷运沿线，初访住台北车站／中山最稳：机场捷运 A1 与 24 小时的 1819 巴士都在这里，从松山机场捷运 15 分钟、NT$25；省钱住台北车站一站之隔、2 分钟 NT$20 的西门町，泡温泉去北投住一晚。 |
| `taiwan-entry-2026-arrival-card` | zh-CN | 158 → 195 | 入境台湾 2025 年 10 月 1 日起改为抵达前 7 天内在线免费填 TWAC；大陆护照要办入台证、每次停留 15 天以内，港澳居民可在线申请网签（30 天）或入出境许可证，新马护照免签 30 天。 |
| `taiwan-esim-sim-wifi` | zh-CN | 108 → 187 | 台湾上网在桃园机场买中华电信、台湾大哥大、远传电信的旅客卡最省事，上网吃到饱4G 3天NT$300起、5G 3天NT$500起，也能办eSIM；要注意柜台最晚21:30关门、要带两种证件、旅客卡不能延长天数。 |
| `taiwan-etiquette-safety-tips` | zh-CN | 85 → 195 | 游客在台湾真的会被罚的几条：捷运黄线内连白开水都不能喝，罚 NT$1,500 至 7,500，禁烟场所吸烟或用电子烟罚 NT$2,000 至 10,000，家户垃圾丢进台北街边垃圾桶罚 NT$3,600 起；报警 110、救护 119。 |
| `taiwan-food-guide-must-eat` | zh-CN | 96 → 154 | 台湾小店点餐的规矩是自己拿纸菜单勾选、柜台付款、自助茶水、不用小费，饭店餐厅可能在账单上加10%服务费；奶茶店会问甜度和冰块，多数本地人答半糖、微冰。 |
| `taiwan-payment-easycard-cash-cards` | ja | 93 → 196 | 台湾の支払いは、夜市・屋台・伝統市場は現金のみが多く、MRT・バス・コンビニはNT$100で買える悠遊カード、デパートやチェーン店、セブン-イレブンはJCBを含むタッチ決済のクレジットカードという使い分け。 |
| `taiwan-payment-easycard-cash-cards` | zh-CN | 62 → 195 | 在台湾付钱，夜市、小吃摊、传统市场常常只收现金，捷运、公交和便利店小额用 NT$100 一张的悠游卡，百货和 7-ELEVEN 可感应刷银联卡，邮局 ATM 能用银联卡取新台币，支付宝、微信支付只在 7-ELEVEN 和全家能确认。 |
| `taiwan-tax-refund-shopping-2026` | zh-CN | 113 → 200 | 台湾标价已含 5% 营业税，外籍旅客（含持入出境许可证的港澳读者）同一天同一家店满 NT$2,000 就能退，税额再扣 20% 手续费，含税 NT$10,000 到手约 NT$380，商品 90 天内未拆封带出境、出境前办完。 |
| `taoyuan-airport-to-taipei` | zh-CN | 148 → 197 | 桃园机场进台北默认坐机场捷运直达车，NT$160、35 到 39 分钟到台北车站，05:55 到 22:58 有车；23:00 之后落地或想省钱坐 24 小时的 1819 巴士 NT$133 到 164，人多行李多坐排班出租车约 NT$1,200 到 1,900。 |
| `thailand-entry-2026-tdac` | zh-TW | 194 → 197 | 台灣護照入境泰國 2026 年 9 月 15 日起觀光免簽從 60 天改為 30 天，TDAC 泰國數位入境卡抵達前 3 天內在官網免費填好，電子菸連菸油都別帶。 |
| `thailand-esim-sim-wifi` | zh-TW | 187 → 197 | 泰國上網：手機支援 eSIM 就出發前買旅客 eSIM（AIS 399 泰銖起），只待 5 天以內開台灣電信漫遊最省事，待 8 天以上到 24 小時的機場櫃台買實體 SIM（True 8 天 449 泰銖），3 人以上租分享器。 |
| `usj-guide` | zh-TW | 150 → 199 | 日本環球影城一日入場券成人 8,400 日圓起、2026 年 9 月 1 日起都要指定入園日期，一定要進超級任天堂世界就買含瑪利歐賽車的環球特快入場券（附區域入場保證），不買就開園前一小時到、入園後先在 APP 領區域入場號碼券。 |
| `vietnam-money-sim-grab-guide` | zh-TW | 216 → 200 | 越南落地先做三件事：拿護照到機場電信櫃台買預付 SIM（純上網約 100,000 到 200,000 越南盾），美金到機場銀行櫃台換越南盾或 ATM 提款，Grab、Xanh SM、Be 叫車或跳表計程車。 |

Spot-check (five picked with `random.seed(20260919)`; every number in the new first sentence was
searched in the body text and matched to a source in `sources`):

- `hanoi-4-day-itinerary` zh-TW — 86 路 50,000、文廟 70,000、火爐監獄 50,000、長安遊船 300,000 all in
  the fare tables; backed by 內排國際機場 Phương tiện vận chuyển công cộng, 文廟—國子監 Visitor
  information, 火爐監獄遺址 Ticket, 長安名勝群管理委員會 Giá vé.
- `taiwan-esim-sim-wifi` zh-CN — 4G 3天NT$300、5G 3天NT$500 in the 旅客卡资费 table, 21:30 in the
  桃园机场柜台 table and the callout; backed by 中华电信 观光预付卡资费, 台湾大哥大 4G/5G旅客卡, 远传
  旅客上网卡 and 桃园国际机场 设施介绍.
- `hong-kong-4-day-itinerary` zh-TW — 旅客八達通 170 港元 (交通 section and 一覽 table), 昂坪 360
  標準車廂來回 295 港元 (一覽 table), 感應式銀行卡車資同成人八達通 (交通 section); backed by 港鐵
  車票種類及車費, 昂坪 360 Cable Car Tickets, 港鐵 About Contactless Bank Card.
- `taiwan-entry-2026-arrival-card` zh-CN — 2025 年 10 月 1 日, 抵达前 7 天内, 每次 15 天以内, 网签 30
  天, 新马免签 30 天 all in the 行前 section and its table; backed by 移民署新闻 TWAC, 移民署 大陆地区
  人民来台个人旅游须知 (15 天), 移民署问答 港澳人士 (30 天), BOCA 免签入境.
- `taiwan-payment-easycard-cash-cards` ja — 悠遊カード NT$100 (結論 list), 夜市・屋台・伝統市場は現金の
  み (table and 現金 section), セブン-イレブンはタッチ決済・JCB (table); backed by 悠遊卡公司 普通卡,
  대만관광청 서울사무소 FAQ, 7-ELEVEN 支付工具.

After merge and deploy, the owner imports the 31 packs on the host (dry run first, then publish):

```bash
python -m app.cli guides-import --actor-email <admin> --dry-run --slug bangkok-4-day-itinerary --slug bangkok-airport-to-city --slug bangkok-bts-mrt-boat-guide --slug bangkok-where-to-stay --slug chiang-mai-3-day-itinerary --slug da-nang-hoi-an-4-day-itinerary --slug hanoi-4-day-itinerary --slug ho-chi-minh-city-4-day-itinerary --slug hong-kong-4-day-itinerary --slug jiufen-shifen-yehliu-day-trip --slug kaohsiung-3-day-itinerary --slug krabi-ao-nang-railay-4-islands --slug macau-day-trip-from-hong-kong --slug sentosa-day-guide --slug singapore-4-day-itinerary --slug tainan-2-day-itinerary --slug taipei-metro-easycard-guide --slug taipei-night-markets-guide --slug taipei-viewpoints-101-elephant-mountain --slug taipei-where-to-stay --slug taiwan-entry-2026-arrival-card --slug taiwan-esim-sim-wifi --slug taiwan-etiquette-safety-tips --slug taiwan-food-guide-must-eat --slug taiwan-payment-easycard-cash-cards --slug taiwan-tax-refund-shopping-2026 --slug taoyuan-airport-to-taipei --slug thailand-entry-2026-tdac --slug thailand-esim-sim-wifi --slug usj-guide --slug vietnam-money-sim-grab-guide
python -m app.cli guides-import --actor-email <admin> --publish --slug bangkok-4-day-itinerary --slug bangkok-airport-to-city --slug bangkok-bts-mrt-boat-guide --slug bangkok-where-to-stay --slug chiang-mai-3-day-itinerary --slug da-nang-hoi-an-4-day-itinerary --slug hanoi-4-day-itinerary --slug ho-chi-minh-city-4-day-itinerary --slug hong-kong-4-day-itinerary --slug jiufen-shifen-yehliu-day-trip --slug kaohsiung-3-day-itinerary --slug krabi-ao-nang-railay-4-islands --slug macau-day-trip-from-hong-kong --slug sentosa-day-guide --slug singapore-4-day-itinerary --slug tainan-2-day-itinerary --slug taipei-metro-easycard-guide --slug taipei-night-markets-guide --slug taipei-viewpoints-101-elephant-mountain --slug taipei-where-to-stay --slug taiwan-entry-2026-arrival-card --slug taiwan-esim-sim-wifi --slug taiwan-etiquette-safety-tips --slug taiwan-food-guide-must-eat --slug taiwan-payment-easycard-cash-cards --slug taiwan-tax-refund-shopping-2026 --slug taoyuan-airport-to-taipei --slug thailand-entry-2026-tdac --slug thailand-esim-sim-wifi --slug usj-guide --slug vietnam-money-sim-grab-guide
```

### 2026-09-21 stale-claim handoff

- The 31 pack edits for this task were merged in PR #565 (`d11178863d1a2a35ddfff17be65bcc2a63514194`) on 2026-09-19. Its checklist and repository checks are complete. The original `review` claim exceeded the documented 24-hour takeover period, so `codex-aio-task-close` claimed it through the task CLI without `--force`.
- The task remains open as `blocked`: its own handoff still requires a production import dry run and publication audit, and no verified import receipt has been attached here. Recheck live versions and preserve later edits before any import. Do not treat the merged pack changes as proof that production descriptions were republished.
- The repository editing scope is now only this task file. The merged pack paths are released for separately claimed localization work; future production import must compare the current published revisions to the exact reviewed descriptions and stop on drift. No article pack or production data was changed in this handoff.
