# 第六批規格勘誤

二十篇文章 2026-09-14 已經寫完、查核並上線。寫作與兩輪查核時發現，規格檔本身有些句子寫錯，或和官方頁不符。**正式站以 `apps/api/app/guides/content/<slug>.json` 為準**；規格檔保留規劃當時的原樣，錯處都列在這裡，之後有人要照規格重寫或改寫時，先看這一頁。

| 規格 | 規格原本寫的 | 實際（文章已照這個寫） | 依據 |
| --- | --- | --- | --- |
| singapore-4-day-itinerary | 花穹成人 12、雲霧林成人 26 新幣的單館票 | 這是 Singapore Resident 分頁的價格。外國旅客分頁只列雙溫室成人 46、3–12 歲 32 新幣，以及套票。WebFetch 會把兩個分頁的內容攤平讀成一份，要用 curl 分開讀 | https://www.gardensbythebay.com.sg/en/things-to-do/attractions/flower-dome.html |
| singapore-4-day-itinerary | 蘇丹回教堂「現場參觀免費」 | 官網只寫 free & easy tour，沒有寫到費用 | https://sultanmosque.sg/visit/ |
| hong-kong-4-day-itinerary | 昂坪 360 纜車約 20 分鐘，標準來回網購 420 港元；天壇大佛 09:00–18:00 | 纜車約 25 分鐘。標準車廂來回 295、水晶車廂來回 365 港元；420 是 Crystal+ 去程加標準車廂回程。天壇大佛 10:00–17:30，寶蓮禪寺 09:00–18:00 | https://www.np360.com.hk/en/tickets-promotions/tickets-tours/cable-car-tickets 、https://www.plm.org.hk/eng/visitors.php |
| hong-kong-4-day-itinerary、hong-kong-airport-to-city | 「旅遊一日票」「遊客八達通」；「高鐵西九龍站客務中心」 | 港鐵中文產品名是「遊客全日通」「旅客八達通」。香港西九龍站沒有客務中心，只有八達通售賣機 | https://www.mtr.com.hk/ch/customer/tickets/tf_index.html |
| hong-kong-4-day-itinerary | 山頂纜車「平日／繁忙日」票價 | 官方用語是「普通日子／熱門日子」 | https://www.thepeak.com.hk/zh-hant/ticket-and-booking/purchase-ticket/peak-tram-sky-pass |
| hong-kong-airport-to-city | 在香港站「出閘」步行到中環站轉車 | 兩站之間是站內通道，在付費區內，不必出閘 | https://www.mtr.com.hk/archive/ch/services/layouts/hok.pdf |
| hong-kong-airport-to-city | 機場快綫同日來回優惠的條件「在去程到回程之間搭了其他機場快綫車程」 | 用同一個付款工具搭過這趟回程以外的任何車程，就沒有回程免費 | https://www.mtr.com.hk/ch/customer/tickets/tf_index.html |
| hong-kong-entry-2026 | 「煙油 5 毫升」「加熱煙枝 100 支」 | 原文是「5 毫升煙用物質」「100 支加熱煙支」 | https://www.info.gov.hk/gia/general/202604/29/P2026042900460.htm |
| hong-kong-entry-2026 | 現金超過門檻「走紅色通道，或填紙本申報表」 | 兩者不是二選一：走紅色通道，再用紙本申報表或電子表格二維碼申報 | https://www.customs.gov.hk/tc/service-enforcement-information/passenger-clearance/currency-bearer-negotiable-instruments/index.html |
| hong-kong-entry-2026、singapore-entry-2026-sg-arrival-card | 三篇長青攻略要連回入境情報 | 依 README 的時效規則不連：入境情報 2027-03-31 過期。會連回的只有另一篇入境情報，以及 power-bank-flight-rules-2026 | README「站內連結」 |
| kanazawa-2-day-itinerary | 「大阪來回可以買兩張北陸單程票，共 16,000 日圓」 | 北陸單程票每本護照只能兌換一張，不能兩張湊成來回 | https://www.westjr.co.jp/travel-information/tc/tickets-passes/oneway/hokuriku/ |
| power-bank-flight-rules-2026 | 日本罰則包含「不放置物櫃」；韓國與日本新制「國內外航空都適用」 | 國交省罰則不含置物櫃（別紙 1 第 4 點），也不含替手機充電（第 7 點）。「國內外航空都適用」是 WebFetch 摘要自己加的，原文沒有 | https://www.mlit.go.jp/report/press/content/001995959.pdf 、https://www.korea.kr/news/policyNewsView.do?newsId=148962298 |
| return-to-taiwan-customs-duty-free-guide | 「機上餐點帶下來也算」、「個人輸入電子菸罰 5 萬到 500 萬」都「不要寫」 | 兩句都有官方依據：臺北關 FAQ 的品項原文有「含肉機上餐食或餐盒」；菸害防制法第 26 條現行條文仍是罰 5 萬到 500 萬，2026-06-25 只是行政院草案 | https://web.customs.gov.tw/taipei/singlehtml/3130?cntId=cus2_177199_3130 、https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=L0070021 |
| japan-cherry-blossom-2027 | 「2027 年 2 月確認國立天文台官報的春分日」 | 內閣府頁已經列出令和 9 年 3/21 春分の日、3/22 休日，不必再等官報 | https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html |
| taiwan-long-weekends-2027-flight-planning | 「機票怎麼比」一段講價格通知、LINE 到價通知、查詢扣次 | 正式站 2026-09-14 的 site-visibility 是 alerts_enabled、pricing_enabled 都是 false，所以文章只寫彈性日期搜尋 | `https://mokaair.com/api/travel/runtime/site-visibility` |
| ho-chi-minh-city-4-day-itinerary | 地鐵 1 號線「一般日 5–23 時、班距 7–15 分鐘」；可在「售票機、櫃台」買票 | 5–23 時是耶誕、跨年、春節的延長時刻，平日時刻沒有官方來源。購票方式是自動售票機，或 HCMC Metro HURC App 的 QR 碼 | https://baochinhphu.vn/trai-nghiem-cac-cong-nghe-vuot-troi-cua-tuyen-metro-1-ben-thanh-suoi-tien-102241223115642354.htm |
| phuket-airport-transport-where-to-stay | Smart Bus Route 2「從 Bus Terminal 2」出發；Dragon Line 經 Central Festival | 班表圖（2026-01-15 起）寫的起點是 Terminal 1，和官網文字不一致，文章照班表圖寫。Dragon Line 路線圖只畫老城一圈 | https://www.phuketsmartbus.com/ |
| suwon-hwaseong-day-trip | 「1 到 3 小時三種走法」 | 這幾條步行路線寫在網頁的 HTML 註解裡，畫面上看不到，文章不引用。夜間開放到 11/1；另一則公告寫的 11/4 是誤植（11/4 是週三） | https://www.swcf.or.kr/?p=66 |
| yokohama-day-trip-from-tokyo | 「橫濱市觀光協會」說約 30 分 | 出處是橫濱官方觀光網站，由横浜観光コンベンション・ビューロー營運 | https://www.welcome.city.yokohama.jp/access/ |
