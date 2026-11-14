# 大阪／京都與台北住宿區決策卡來源紀錄

checked_on：2026-11-14。五語文案在 `apps/web/lib/destination-decisions.json` 的 `destinations["osaka-kyoto"]` 與 `destinations.taipei`，
與東京（[adsense-tokyo-sources.md](adsense-tokyo-sources.md)）、首爾（[adsense-seoul-sources.md](adsense-seoul-sources.md)）使用同一套欄位與版面。
固定順序對應 `apps/api/app/destinations/catalog.py`：

- `osaka-kyoto`：`難波／心齋橋`、`梅田`、`京都站`、`四條河原町`
- `taipei`：`台北車站`、`西門町`、`信義區`、`中山`

每列包含 `suitable`、`tradeoff`、`check`。「適合情境」與「入住前檢查」是根據官方觀光與鐵道／捷運資料整理的編輯建議，
不是官方飯店評等或住宿實測。刻意不寫房價、票價、班距、精確車程分鐘數、保證安靜或「最方便」等說法，避免隨票價與時刻表異動而失真。

## 大阪／京都（`osaka-kyoto`）來源與依據

本輪於 2026-11-14 UTC 以公開 HTML 讀取下列頁面，皆回 200。

### nambaShinsaibashi | 難波／心齋橋 / Namba / Shinsaibashi / 難波／心斎橋 / 난바 / 신사이바시

- source: OSAKA-INFO — Dotonbori | https://osaka-info.jp/en/spot/dotonbori/
- source: OSAKA-INFO — Shinsaibashi-Suji Shopping Street | https://osaka-info.jp/en/spot/shinsaibashi-suji-shopping-street/
- source: Nankai Electric Railway — Limited Express Rapi:t | https://www.nankai.co.jp/en_railway/traffic/express/rapit.html
- evidence: OSAKA-INFO 道頓堀頁說明道頓堀為大阪南區（Minami）代表餐飲與夜間娛樂街區，交通列 Namba Station（南海、近鐵、Osaka Metro 御堂筋線／千日前線／四橋線）步行即達；心齋橋筋商店街頁說明拱廊商店街自心齋橋站（Osaka Metro 御堂筋線、長堀鶴見綠地線）南北延伸至宗右衛門町通，平日與週末人潮皆多。南海電鐵 Rapi:t 官方頁確認關西機場站與南海難波站間有特急列車直通。各「難波」車站與心齋橋站分屬不同站體、拖行李與臨街安靜度檢查屬編輯建議。

### umeda | 梅田 / Umeda / 우메다

- source: OSAKA-INFO — Tourist Information OSAKA (JR Osaka Station) | https://osaka-info.jp/en/spot/tourist-information-osaka/
- source: OSAKA-INFO — Shin-Umeda City General Information Center | https://osaka-info.jp/en/spot/tourist-information-shin-umeda/
- source: JR-WEST — Kansai-Airport Express HARUKA | https://www.westjr.co.jp/travel-information/en/tickets-passes/oneway/haruka/
- source: Kyoto City Official Travel Guide — Getting to Kyoto | https://kyoto.travel/en/getting-to/
- evidence: OSAKA-INFO JR 大阪站旅服頁與新梅田城（梅田藍天大廈）頁分別列出 JR 大阪站、Osaka Metro 梅田站、阪急大阪梅田站等不同步行起點，反映北區（Kita）多站體結構。JR 西日本 HARUKA 官方頁列出關西機場直通大阪站、新大阪站與京都站；Kyoto Travel 交通頁列出 JR 大阪站至京都站的新快速與阪急大阪梅田站至京都河原町站路線。多樓層與地下街轉乘距離及電梯核對屬編輯建議。

### kyotoStation | 京都站 / Kyoto Station / 京都駅 / 교토역

- source: Kyoto City Official Travel Guide — Getting to Kyoto | https://kyoto.travel/en/getting-to/
- source: Kyoto City Official Travel Guide — Getting Around Kyoto by Subway & Train | https://kyoto.travel/en/getting-around/getting-around-kyoto-by-subway-train/
- source: Kyoto City Official Travel Guide — Access to Higashiyama and Shijo Kawaramachi | https://kyoto.travel/en/getting-around/comfortable-access-to-higashiyama-kiyomizu-dera-temple/
- evidence: Kyoto Travel 兩篇交通總覽確認京都站匯集東海道新幹線、JR 關空特急 HARUKA、JR 各線（往伏見、嵐山、宇治、大阪、奈良）、近鐵與地下鐵烏丸線。東山交通專頁明確指出由京都站直接搭市巴士前往東山／五條坂方向經常擁擠，建議改搭鐵道轉地下鐵或京阪電車。烏丸口與八條口南北兩側出口確認為編輯提醒。

### shijoKawaramachi | 四條河原町 / Shijo Kawaramachi / 四条河原町 / 시조 가와라마치

- source: Kyoto City Official Travel Guide — Access to Higashiyama and Shijo Kawaramachi | https://kyoto.travel/en/getting-around/comfortable-access-to-higashiyama-kiyomizu-dera-temple/
- source: Kyoto City Official Travel Guide — Getting to Kyoto | https://kyoto.travel/en/getting-to/
- source: Kyoto City Official Travel Guide — Getting Around Kyoto by Subway & Train | https://kyoto.travel/en/getting-around/getting-around-kyoto-by-subway-train/
- evidence: Kyoto Travel 東山與市內鐵道頁記載四條河原町（阪急京都河原町站、鴨川對岸京阪祇園四條站）步行可達花見小路、八坂神社與東山一帶；阪急連通大阪梅田，京阪連通大阪（淀屋橋／京橋）及伏見、宇治，西側烏丸通則有地下鐵烏丸線四條站。新幹線與 HARUKA 均停靠京都站而非四條河原町，故卡片提醒攜帶行李時需轉乘。

## 台北（`taipei`）來源與依據

本輪於 2026-11-14 UTC 以公開 HTML 讀取下列頁面，皆回 200。

### taipeiMainStation | 台北車站 / Taipei Main Station / 台北駅 / 타이베이역

- source: Taipei Travel — Taiwan Railways (Taipei Main Station) | https://www.travel.taipei/en/attraction/details/1727
- source: Taipei Travel — Taipei City Mall | https://www.travel.taipei/en/attraction/details/2145
- source: Taoyuan Metro — Route Map | https://www.tymetro.com.tw/tymetro-new/en/_pages/travel-guide/road.html
- evidence: 臺北旅遊網台北車站頁確認此站為台鐵、高鐵與台北捷運（淡水信義線、板南線）共構之北台灣交通樞紐；台北地下街頁與桃園捷運路線圖確認地下通道連通桃園機場捷運 A1 台北車站、捷運北門站及周邊地下街出口。站區地下街跨度大、應核對具體出口區號與電梯屬編輯建議。

### ximending | 西門町 / Ximending / 시먼딩

- source: Taipei Travel — Ximending Shopping District | https://www.travel.taipei/en/pictorial/article/53989
- source: Taipei Travel — The Red House | https://www.travel.taipei/en/attraction/details/503
- source: Taoyuan Metro — Route Map | https://www.tymetro.com.tw/tymetro-new/en/_pages/travel-guide/road.html
- evidence: 臺北旅遊網西門町商圈專文與西門紅樓頁確認西門町以徒步商店街、電影街、街頭文化與西門紅樓為核心，交通為捷運西門站（板南線與松山新店線交會，6 號出口往商圈、1 號出口往紅樓）。桃園捷運路線圖確認機場捷運終點為 A1 台北車站，不停靠西門站，故需於台北車站或北門站轉乘。

### xinyi | 信義區 / Xinyi District / 信義区 / 신이구

- source: Taipei Travel — Xinyi Shopping District | https://www.travel.taipei/en/attraction/details/1695
- source: Taipei Travel — Taipei 101 Mall | https://www.travel.taipei/en/attraction/details/540
- source: Taoyuan Metro — Route Map | https://www.tymetro.com.tw/tymetro-new/en/_pages/travel-guide/road.html
- evidence: 臺北旅遊網信義商圈頁與台北 101 商場頁記載百貨群空橋連通、書店、影城、餐飲與夜景特色，交通分別對應板南線市政府站（北側）與淡水信義線台北 101／世貿站、象山站（南側）。對照桃園捷運路線圖，由機場捷運 A1 台北車站前往信義區需轉乘台北捷運。

### zhongshan | 中山 / Zhongshan / 중산

- source: Taipei Travel — MRT Green Corridor | https://www.travel.taipei/en/attraction/details/3692
- source: Taipei Travel — MRT Zhongshan Underground Book Street | https://www.travel.taipei/en/attraction/details/2100
- source: Taoyuan Metro — Route Map | https://www.tymetro.com.tw/tymetro-new/en/_pages/travel-guide/road.html
- evidence: 臺北旅遊網心中山線形公園頁與中山地下書街頁記載捷運中山站至雙連站間的綠廊公園、地下書街及周邊巷弄特色店鋪與咖啡館，捷運中山站為淡水信義線與松山新店線交會站。桃園捷運路線圖確認機場捷運止於 A1 台北車站；提醒區分「捷運中山站周邊」與行政區「中山區」其他捷運站屬編輯建議。

## 界線

- 本輪未逐間核對個別旅館、未實地量測各出口步行秒數，亦未抄錄隨時可能調整的票價或班距；卡片僅引導讀者在訂房前核對實際車站、出口與電梯動線。
- 這是重點目的地頁的實質決策內容補強，不代表 AdSense 審核必然通過；部署後仍應依 [adsense-review-readiness.md](adsense-review-readiness.md) 覆核正式站公開頁。
