# 8. `yokohama-day-trip-from-tokyo`

東京出發橫濱一日遊攻略：東急東橫線還是 JR、みなとみらい線一日券要不要買、港未來・紅磚倉庫・杯麵博物館到中華街怎麼排

| 欄位 | 值 |
| --- | --- |
| kind | `howto` |
| destination_id | `tokyo` |
| topics | `itinerary`, `transport`, `viewpoint` |
| valid_until | `null` |
| featured | `true` |
| display_order | `880` |

規格 2026-09-14 定稿：兩輪查核加三輪一致性審查，已對照 main 上 #468 與第五批的文章。官方來源的數字是規劃時讀到的，
撰稿當天要再打開一次核對，`checked_on` 填實際打開那天。通用規則見 [README](README.md)。

## 切角與段落

回答「住東京，去橫濱半天或一天，從哪條線進去、買不買票、怎麼走才不走回頭路」。字數 1,800–3,000，機場、季節、兩天走法各只留一兩句加連結，篇幅留給進入線、票券算術與步行路線。
(1) 開頭 paragraph：橫濱離東京三十分鐘上下（橫濱市觀光協會的說法是「約 30 分前後」），真正要決定的是從哪個車站進去、要不要買企畫票。先講結論：照本文的步行路線走，港未來到中華街全程用走的，多數人刷 Suica／PASMO 就好；企畫票只適合住東急沿線、或一天要在みなとみらい線上跳好幾站的人。
(2) H2 依住宿地選進入線：一張表（住哪裡／搭哪條線／在哪站下車／從哪個起點開始走），列法沿用 tokyo-where-to-stay 的區名，不重寫各區優缺點：
- 澀谷（含中目黑、代官山）：東急東橫線直通みなとみらい線，直達みなとみらい站或元町・中華街站；從みなとみらい站開始走。
- 新宿三丁目、池袋：東京メトロ副都心線直通東橫線的班次可直達；班次種別與是否直通要用東京メトロ或東急官網確認才寫。新宿站是 JR，別寫成「新宿直達」。
- 新宿（JR）：湘南新宿ライン到橫濱站轉乘。
- 東京車站、品川：JR 京濱東北・根岸線直達櫻木町、關內、石川町，從櫻木町開始走；或東海道線到橫濱轉乘。上野、銀座一帶先到東京車站或品川換 JR。
- 淺草、品川一帶（都營淺草線、京急沿線）：京急到橫濱；直通班次以京急官網為準。
表後一句加 link 到 tokyo-where-to-stay。分鐘數只寫官網查得到的，查不到就不寫。
(3) H2 票券算術（2026 年 9 月查證，みなとみらい線運賃為 2023 年 3 月 18 日改定版）：
- みなとみらい線一日乗車券：大人 460、小兒 230 日圓，當天在各站售票機買，也有 Q SKIP 數位版。
- みなとみらい線普通運賃（大人）：車票 橫濱到新高島、みなとみらい、馬車道 200 日圓，到日本大通り、元町・中華街 230 日圓；IC 卡 橫濱到みなとみらい 193 日圓、橫濱到元町・中華街 224 日圓、みなとみらい到元町・中華街 193 日圓。
- 算術（用 IC 價，讀者多半刷卡）：搭兩段最多 448 日圓（橫濱與元町・中華街來回），不到 460 日圓，不回本；搭第三段才划算，例如橫濱→みなとみらい 193＋みなとみらい→元町・中華街 193＋元町・中華街→橫濱 224＝610 日圓。用紙本車票來回 230×2＝460 日圓只是打平。照本文步行路線走的人，みなとみらい線最多只搭一兩段，不必買一日券。
- 東急線みなとみらいパス：澀谷出發大人 920、兒童 470 日圓（中目黑、代官山同價，自由が丘 910、武藏小杉 860、日吉 830、菊名 750 日圓），含東急各站到橫濱往返＋みなとみらい線一日自由搭乘，只在東急線各站售票機賣（首班車到 22:30），當日有效。比法寫成方法：「澀谷到橫濱東急 IC 運賃 ×2＋你當天要搭的みなとみらい線段數」跟 920 比。東急運賃要用東急官網運賃檢索確認才寫數字，確認前不寫。
- 東急線みなとみらい線ワンデーパス：Q SKIP 價 1,190 日圓，東急全線＋みなとみらい線，適合同一天還要去自由が丘、二子玉川的人，一句帶過。
- 京急横浜1DAYきっぷ：品川出發 1,350 日圓，含京急往返與自由區間（京急橫濱～上大岡、みなとみらい線全線等），一句帶過。
- JR 的ヨコハマ・みなとみらいパス：價格以 JR 東日本官網為準（讀不到，不寫數字）。
- 一句對齊既有口徑：Tokyo Subway Ticket 只含東京メトロ與都營地下鐵，東急、JR、みなとみらい線都要另外付（與 tokyo-transit-passes 一致）。
- 結論 paragraph：只搭兩三趟就刷 Suica／PASMO，後接 link 到 tokyo-transit-passes。
- warning callout：東急線みなとみらいパス只在東急站售票機賣，東京メトロ站、JR 站買不到，只限購買當天。
- 然後放 transport offer（見 offers）。
(4) H2 一日路線（依時序，H3 分上午、下午、傍晚；每站寫 2026 年 9 月查證的時間與票價）：
- H3 上午：JR 組從櫻木町站搭 YOKOHAMA AIR CABIN 到運河パーク（大人〔國中生以上〕單程 1,000、來回 1,800 日圓；兒童〔3 歲到小學生〕單程 500、來回 900 日圓；未滿 3 歲免費；營業 10:00–21:00，擁擠時提早停止受理，停駛日依營業日曆）；東急組從みなとみらい站出發，想搭 AIR CABIN 就來回搭一趟。→ 杯麵博物館（カップヌードルミュージアム 橫濱：大人〔大學生以上〕500 日圓、高中生以下免費；10:00–18:00，17:00 最後入館；みなとみらい站、馬車道站步行 8 分、JR 櫻木町站步行 12 分）。MY CUPNOODLES Factory 每份 500 日圓、完成約 45 分鐘，當天入館後領先到先得的整理券，或在前一天 24:00 前線上買附利用券的入館券（額滿為止）。
- 放 activities offer（見 offers），offer 前後都要有正文。
- warning callout：杯麵博物館週二休館（遇國定假日改隔天休），年末年始也休；週二去橫濱的人把路線改成紅磚倉庫、大さん橋、中華街為主。
- H3 下午：紅磚倉庫（1 號館 10:00–19:00、2 號館 11:00–20:00，店家各自不同，除法定檢查日外每天營業）→ 大さん橋（屋頂廣場 24 小時開放；みなとみらい線日本大通り站 3 或 4 號出口步行 7 分，JR 關內站南口步行 15 分）→ 山下公園（冰川丸只當地標提，門票查 NYK 官網讀得到才寫）。
- H3 傍晚：中華街晚餐（橫濱中華街發展會 chinatown.or.jp 當入口，不點名店家與價格，請讀者用文末 foods?city=yokohama 目錄挑）→ 元町商店街 → 元町・中華街站回程（東橫線直通回澀谷）。
- 表格：路線總表（時段／地點／大人票價／時間／最近車站步行分鐘），只填上面查證過的數字。
- tip callout：週末中華街吃午餐要早點進場，或把中華街排在平日；寫成建議，不寫成官方數字。
(5) H2 夜景：Cosmo Clock 21 大觀覽車 1 人 1,000 日圓，售票只收現金；與 AIR CABIN 的套票大人單程 1,700、來回 2,500 日圓，比分開買（1,000＋1,000、1,800＋1,000）各省 300 日圓；兒童套票單程 1,300、來回 1,600 日圓。大さん橋屋頂看港未來天際線，24 小時開放。AIR CABIN 營業到 21:00。步行時間只寫官網有的（例如日本大通り站到大さん橋 7 分）。
(6) H2 換個走法：一張「情境 → 路線」表，四列：
- 反向：中華街早午餐 → 山下公園 → 大さん橋 → 紅磚倉庫 → 杯麵博物館 → 傍晚在港未來搭 AIR CABIN、看夜景，櫻木町搭 JR 回東京。
- 親子：杯麵博物館（高中生以下免費、MY CUPNOODLES Factory 先預約）＋よこはまコスモワールド（入園免費，設施逐項付費）；Cosmo World 以外的價格查得到才寫。
- 雨天：杯麵博物館＋紅磚倉庫室內＋港未來室內商場，其他景點不硬走；想整天都在室內，改看東京的上野或六本木博物館，表後 link 到 tokyo-rainy-day-museum-plan（本文不重寫博物館排法）。
- 退房日帶行李：先把行李寄放在回程車站（東京方向）或橫濱站，再進港未來；置物櫃的尺寸、付款與取件細節不在本文展開，放到行前檢查連過去。
(7) 季節，一兩句：紅磚倉庫冬季有聖誕市集，日期每年公布，以官網為準；不寫年份、不寫往年日期，也不連任何會過期的 intel。
(8) 兩天走法，一段：住橫濱一晚，隔天搭 JR 橫須賀線到北鎌倉、鎌倉，時間與票價的口徑照 kamakura-enoshima-day-trip（鎌倉市觀光協會「橫濱出發約 30 分鐘」、JR 票價以官網為準），不另寫分鐘數；後接 link。
(9) H2 行前檢查（list）：避開週二（杯麵博物館休館）／想做杯麵前一天線上訂／住東急沿線才買東急線みなとみらいパス，而且要在東急站買／Cosmo Clock 21 帶現金／從成田機場搭 N'EX 可直達橫濱：看成田羽田機場交通篇（本文不寫機場票價，後接 link 到 narita-haneda-to-tokyo；羽田出發的走法那篇沒寫，本文也不提羽田，不寫「羽田、成田直接到橫濱」）／帶行李的人先看 japan-station-locker-guide（後接 link）。
(10) 結尾 link：tokyo-5-day-itinerary、destinations/yokohama、foods?city=yokohama。

## 官方來源

2026-09-14 WebFetch 重新確認（本輪有改或新增數字的都在這裡）：
- 橫濱高速鐵道 みなとみらい線 運賃頁 www.mm21railway.co.jp/info/ticket.html：WebFetch 摘要又回報「IC 全線 193 日圓」，所以另外下載原始 HTML 對照矩陣。表格是三角矩陣，右上是車票價、左下是 IC 價（2023 年 3 月 18 日改定）：橫濱到新高島、みなとみらい、馬車道 車票 200、IC 193；橫濱到日本大通り、元町・中華街 車票 230、IC 224；新高島到元町・中華街 IC 224；みなとみらい、馬車道、日本大通り之間與到元町・中華街 IC 193。第一輪的 193 疑點已解決：近距離 193，遠距離 224。
- 同網站 /info/oneday.html：一日乗車券 460／230 日圓、各站售票機、Q SKIP（第一輪已確認）。
- YOKOHAMA AIR CABIN yokohama-air-cabin.jp：大人＝國中生以上，兒童＝3 歲到小學生，未滿 3 歲免費；單程 1,000／500、來回 1,800／900 日圓；Cosmo Clock 21 套票單程 1,700／1,300、來回 2,500／1,600 日圓；10:00–21:00，擁擠時提早停止受理；所需時間沒寫，停駛日看營業日曆。
- 杯麵博物館 www.cupnoodles-museum.jp/ja/yokohama/guide/admission/：週二休館（遇國定假日改隔天休）、年末年始休；10:00–18:00，17:00 最後入館；大人（大學生以上）500 日圓、高中生以下免費。首頁 /ja/yokohama/：みなとみらい站、馬車道站步行 8 分，JR 櫻木町站步行 12 分。
- 同館 /ja/yokohama/attractions/mc-factory/：MY CUPNOODLES Factory 每份 500 日圓（含稅），完成約 45 分鐘，受理 10:00–18:00（最後 17:30）；當天入館後領先到先得的整理券，或前一天 24:00 前線上買附利用券的入館券，額滿為止。
- よこはまコスモワールド cosmoworld.jp/ticket/：大觀覽車 Cosmo Clock 21 1 人 1,000 日圓（頁面沒有年齡區分），售票只收現金；入園免費，設施逐項付費，用預付票券。
- 大さん橋 osanbashi.jp/floorguide/rooftop：屋頂廣場 24 小時開放。/access：みなとみらい線日本大通り站 3 或 4 號出口步行 7 分，市營地下鐵關內站 1 號出口與 JR 關內站南口步行 15 分；總合服務台 9:00–17:30。
第一輪已確認、本輪沒改：東急電鐵 /railway/ticket/value-ticket/minatomirai/（東急線みなとみらいパス的內容、東急各站售票機、首班車到 22:30、當日有效）；價目 PDF minatomirai_ticket_pricelist.pdf（2023-03-18 版，本輪用 pdftotext 再抽一次：澀谷 920／470 日圓，其他站價格同第一輪）；/railway/ticket/value-ticket/（ワンデーパス Q SKIP 1,190 日圓）；京急 www.keikyu.co.jp/visit/otoku/otoku_yokohama.html（橫浜1DAYきっぷ 品川 1,350 日圓）；紅磚倉庫 www.yokohama-akarenga.jp（兩館時間）；橫濱市觀光協會 www.welcome.city.yokohama.jp/access/（進入路線、約 30 分前後），英文版 www.yokohamajapan.com。
機場段不另查官網：成田搭 N'EX 直達橫濱這件事沿用 main 上 narita-haneda-to-tokyo 的內容（該篇寫 N'EX 往大船方向經橫濱、到橫濱普通車指定席 4,480 日圓），本文不引票價；該篇沒有羽田到橫濱的走法，本文不提羽田。
讀不到或無法確認：東急普通運賃。/railway/ticket/fares/ 的運賃表 PDF（1 圓單位）沒有站名文字層。依東橫線站序讀，第一列末格澀谷到橫濱是 309 日圓，但沒有站名可對，不算確認；撰稿時要用東急官網運賃檢索或各站頁確認才寫。另外，jreast.co.jp 回 403（JR 運賃與ヨコハマ・みなとみらいパス寫以官網為準）；www.yokohama.travel 憑證錯誤；あかいくつ巴士沒有官方頁，本輪從文章拿掉。撰稿時要讀：東京メトロ副都心線直通東橫線的班次、橫濱中華街發展會 www.chinatown.or.jp（只當入口，不引數字）。

## 合作區塊（offer）

放兩個，彼此不相鄰。文章 destination_id 是 tokyo，offer 的 destination_id 留 null（沿用文章值），實際畫出的是東京的方案，所以 heading 不點名橫濱的特定商品（遊船、摩天輪、AIR CABIN 都不寫）。
(1) module transport，放在「票券算術」一節的 warning callout 之後、下一個 H2 之前。heading：「東京與近郊交通票券，出發前先比價」。
(2) module activities，放在一日路線 H3 上午段杯麵博物館那段 paragraph 之後、週二休館 warning callout 之前。heading：「東京近郊一日遊與體驗先比價」。
不放 hotel（兩天走法只有一段）；topics 是 itinerary、transport、viewpoint，不在禁放清單。

## 站內連結

文中 link 區塊共 7 個站內文章＋2 個結尾頁，全部指向 main 上有 zh-TW 版的長青 howto，沒有 intel：
1. guides/howto/tokyo-where-to-stay：「依住宿地選進入線」表格之後。
2. guides/howto/tokyo-transit-passes：「票券算術」結論 paragraph（Suica 逐次扣款、Tokyo Subway Ticket 不含東急與 JR）之後，warning callout 之前。
3. guides/howto/tokyo-rainy-day-museum-plan（#468）：「換個走法」情境表之後，對應雨天那一列。
4. guides/howto/kamakura-enoshima-day-trip：兩天走法那一段之後。
5. guides/howto/narita-haneda-to-tokyo：行前檢查清單之後，對應「從成田機場搭 N'EX 可直達橫濱：看成田羽田機場交通篇」那一項。連結文字只講成田 N'EX，不寫「羽田、成田直接到橫濱」：main 上那篇只有 N'EX 經橫濱（4,480 日圓），沒有羽田到橫濱的走法，讀者點過去會找不到。
6. guides/howto/japan-station-locker-guide（#468）：緊接在第 5 個之後，對應清單裡帶行李那一項。
7. guides/howto/tokyo-5-day-itinerary：結尾第一個（Day 4 換成近郊一日遊）。
8. destinations/yokohama：結尾（https://mokaair.com/zh-TW/destinations/yokohama；yokohama 在 PUBLIC_DESTINATIONS 與 API 目錄內，是 tokyo 的延伸目的地）。
9. foods?city=yokohama：結尾（https://mokaair.com/zh-TW/foods?city=yokohama），中華街段正文提一句「店家看文末美食目錄」。
拿掉的連結：intel/japan-winter-illumination-2026（2027-01-15 到期，內容也完全沒寫到橫濱）；destinations/tokyo（結尾只放 1–2 個，橫濱城市頁本身會帶出上層的東京）；第五批 nikko-day-trip-from-tokyo、fuji-kawaguchiko-day-trip（選填項刪除，控制連結數）；japan-ic-card-suica-icoca-guide（IC 卡的說明由 tokyo-transit-passes 帶到，避免同段兩個連結）。
第六批互連：其他 19 篇沒有東京近郊或橫濱主題（櫻花 2027 是 intel、會在閱讀期內到期，金澤與本篇不同路線），本篇不連第六批；反向連結列在後續事項。

## 圖解

港灣路線圖（1600×900），圖上每個數字都要出現在正文：
- 左側：三條從東京方向進來的線，用不同顏色。澀谷 Shibuya 東急東横線 Tokyu Toyoko Line（直通みなとみらい線，teal 實線）；東京 Tokyo／品川 Shinagawa JR 京浜東北・根岸線（直達桜木町 Sakuragicho，mocha 實線）；新宿 Shinjuku 湘南新宿ライン（到横浜轉乘，虛線）。不畫分鐘數（東急、JR 的所需時間都沒查到官方數字）。
- 右上：みなとみらい線 teal，横浜 Yokohama → 新高島 → みなとみらい Minatomirai → 馬車道 Bashamichi → 日本大通り Nihon-odori → 元町・中華街 Motomachi-Chukagai。旁邊方框寫「一日乗車券 460 日圓｜IC 193／224 日圓」。
- 下方：coral 步行弧線，桜木町 → YOKOHAMA AIR CABIN（單程 1,000 日圓）→ 運河パーク → カップヌードルミュージアム Cup Noodles Museum（500 日圓，みなとみらい站步行 8 分）→ 赤レンガ倉庫 Red Brick Warehouse → 大さん橋 Osanbashi（日本大通り站步行 7 分）→ 山下公園 Yamashita Park → 中華街 Chinatown。
- 角落小方框：東急線みなとみらいパス 澀谷 920 日圓、週二杯麵博物館休館。
右下角「© Mokaair 製圖 2026」，所有字級 ≥15。

## 撰稿時要小心

(1) destination_id 定為 tokyo（與 kamakura-enoshima-day-trip 的做法一致，讀者住東京，offer 才畫得出來），結尾一定要連 destinations/yokohama 與 foods?city=yokohama。
(2) みなとみらい線 IC 運賃：WebFetch 摘要兩次都誤報「全線 193」，原始 HTML 其實是三角矩陣，橫濱到元町・中華街、日本大通り是 224。寫算術時用 193／224，不要寫成全線同價；一日券的「來回就回本」只對紙本車票成立（打平），對 IC 卡不成立。
(3) 東急普通運賃沒有確認：運賃表 PDF 依站序讀出來澀谷到橫濱 309 日圓，但表上沒有站名，不能引用。沒用東急官網運賃檢索確認就只寫比法，圖上也不畫東急分鐘數與運賃。澀谷搭直通列車進みなとみらい線時，一日乗車券能不能和 IC 卡併用、要不要出站精算，查到官網說明才寫；查不到就建議住東急沿線的人直接比東急線みなとみらいパス。
(4) JR 運賃、所需時間與ヨコハマ・みなとみらいパス價格在 jreast.co.jp（403）：寫「刷 Suica 逐次扣款，票價以 JR 東日本官網為準」，不抄部落格。
(5) 東急線みなとみらいパス價格出自 2023-03-18 版價目 PDF（澀谷 920 日圓），只在東急站售票機賣（首班車到 22:30），東京メトロ站買不到，限當日。
(6) AIR CABIN 兒童是 3 歲到小學生，國中生以上算大人；營業時間依營業日曆，擁擠時提早停止受理，不寫所需分鐘數。
(7) 杯麵博物館週二休館（遇國定假日改隔天休）、年末年始休；「最後入館 17:00」與「工廠最後受理 17:30」兩個時間不要混寫，正文只寫入館 17:00。
(8) Cosmo Clock 21 官網只寫 1 人 1,000 日圓、只收現金，沒有年齡區分，不要自己補兒童價；兒童只寫 AIR CABIN 套票價。
(9) 紅磚倉庫聖誕市集：長青文不寫年份、不寫往年日期，只寫以官網為準。
(10) 與既有文章口徑一致：鎌倉段照 kamakura-enoshima-day-trip（橫濱出發約 30 分鐘、JR 票價以官網為準）；機場段只寫「從成田機場搭 N'EX 可直達橫濱」並連 narita-haneda-to-tokyo，不寫票價（那篇寫的是 N'EX 到橫濱 4,480 日圓，本文若提及只能用這個數字）；narita-haneda-to-tokyo 沒有羽田到橫濱的走法，本文不提羽田，連結文字不能寫成「羽田、成田直接到橫濱看這篇」；Tokyo Subway Ticket 不含東急、JR，照 tokyo-transit-passes；雨天段不重寫博物館排法。
(11) 副都心線直通：新宿三丁目、池袋才是地下鐵站，新宿站是 JR，不寫「新宿直達」；直通班次種別查東京メトロ或東急官網。
(12) 中華街店家不點名、不寫價格，用 foods?city=yokohama 帶。冰川丸門票、橫濱地標塔 Sky Garden、あかいくつ巴士都沒查證，不寫數字（あかいくつ已從規格拿掉）。
(13) www.yokohama.travel 憑證錯誤，官方觀光資訊改引 welcome.city.yokohama.jp／yokohamajapan.com。

## 上線後與交叉檢查

- 反向連結（上線 PR 另開一張票，scope 為 apps/api/app/guides/content 的三個檔）：tokyo-5-day-itinerary 第 14 個區塊（Day 4「橫濱的中華街與港未來」那段）後加 link 到 guides/howto/yokohama-day-trip-from-tokyo；kamakura-enoshima-day-trip 第 3 個區塊（橫須賀線從橫濱直達鎌倉那段）後加連本篇；nikko-day-trip-from-tokyo 結尾「另一個東京近郊一日遊」可視字數加一條連本篇。
- 站內 foods 連結疑似全站無效：/[locale]/foods/page.tsx 與 apps/web/lib/foods.ts 的 readFoodBrowserFilters 只讀 destination_id，不讀 city。所有攻略文的 foods?city=<id> 連結（本篇的 foods?city=yokohama 也是）可能都打開未篩選的美食頁。先到正式站點一條確認，再用 npm run tasks -- new 開票（area web，scope apps/web/lib/foods.ts）：讓 foods 頁接受 city 當作 destination_id 的別名，或全批改寫連結並同步更新 ingest 腳本的 LINK 正則。
- 第六批 ingest 腳本的 KNOWN 白名單要包含本篇連到的 #468 slug（tokyo-rainy-day-museum-plan、japan-station-locker-guide），並確認 destination_for_id('yokohama') 能過 destinations 與 foods 連結檢查。
- 上線前在正式站確認 https://mokaair.com/zh-TW/destinations/yokohama 回 200（yokohama 是延伸目的地，要同時在 PUBLIC_DESTINATIONS 與 API 目錄內）。
- 撰稿時用東急官網運賃檢索確認澀谷到橫濱、到元町・中華街的 IC 運賃，並確認直通列車上一日券與 IC 卡能不能併用；確認到就把東急線みなとみらいパス的回本算術補成數字，同時更新 sources。
- 年度複查（建議 2027 年 9 月，或任一家宣布改運賃時）：みなとみらい線運賃（現行為 2023-03-18 改定）、東急線みなとみらいパス價目、AIR CABIN 與 Cosmo Clock 21 票價、杯麵博物館入館料與休館日。本篇是長青 howto，沒有到期日會提醒，這張複查票要放進 tasks/open。
- japan-cherry-blossom-2027 撰稿時若有東京段，可從 intel 單向連到本篇（intel 連長青 howto 不受到期規則限制）；本篇不要反向連過去。
- narita-haneda-to-tokyo 沒有羽田到橫濱的走法（只有京急到品川、單軌電車到濱松町、利木津到新宿與東京車站）。之後如果要補，另開一張票（scope 為 apps/api/app/guides/content/narita-haneda-to-tokyo.json），先用 WebFetch 查京急官網的羽田到橫濱票價與時間再寫。補上之後，本篇行前檢查那一項才能加回羽田。
