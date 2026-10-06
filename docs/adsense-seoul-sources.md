# 首爾住宿區決策卡來源紀錄

checked_on：2026-10-05。五語文案在 `apps/web/lib/destination-decisions.json` 的 `destinations.seoul`，
與東京卡片（[adsense-tokyo-sources.md](adsense-tokyo-sources.md)）同一套欄位與版面。固定順序：明洞、弘大、東大門、江南，
即目錄 `apps/api/app/destinations/catalog.py` 首爾的四個 areas。

每列包含 suitable、tradeoff、check。「適合情境」與入住前檢查是根據官方地區／交通資料做的編輯建議，
不是官方飯店評等或住宿實測。沒有加入房價、票價、精確車程、保證安靜或「最方便」之類的說法；
官方頁上的票價與班距（例如 AREX 普通車與直達車）刻意不抄進卡片，避免過期。

## 每列來源與依據

本輪於 2026-10-05 UTC 以公開 HTML 讀取下列頁面，皆回 200。

### myeongdong | 明洞 / Myeongdong / 명동

- source: Visit Seoul — Myeongdong Shopping Street | https://english.visitseoul.net/shopping/Myeong-dong/ENP000067
- source: Incheon Airport — Airport Railroad route | https://www.airport.kr/ap_en/1512/subview.do
- source: Visit Seoul — Getting to Seoul from the airport | https://english.visitseoul.net/airport-to-seoul
- evidence: Visit Seoul 寫明洞是購物重鎮，有街頭攤位、服飾與韓國美妝店，也是商業與金融中心，白天人口 150–200 萬；交通欄為「Subway Line 4, Myeongdong Station, Exits 5-10」。仁川機場的 AREX 路線圖普通車停站止於首爾站（可轉 KTX、京義中央線、1 號線、4 號線），沿線沒有明洞。Visit Seoul 機場頁另列機場巴士。拖行李穿越商街不一定省事、房間是否臨商街是編輯建議。

### hongdae | 弘大 / Hongdae / 홍대

- source: Visit Seoul — Hongdae Red Road R1 | https://english.visitseoul.net/attractions/HONGDAE-R1/ENPidz0r2
- source: Visit Seoul — Hongdae Mural Street | https://english.visitseoul.net/entertainment/HongdaeMuralStreet/ENP2ts0gq
- source: Incheon Airport — Airport Railroad route | https://www.airport.kr/ap_en/1512/subview.do
- source: Visit Seoul — Getting to Seoul from the airport | https://english.visitseoul.net/airport-to-seoul
- evidence: Red Road R1 頁列跳蚤市場、街頭表演等活動，交通為「Subway Line 2 / Gyeongui–Jungang Line / Airport Railroad, Hongik Univ. Station」。壁畫街頁寫作品散布在上坡路與住宅區，交通為 6 號線上水站 2 號出口 545m，所以弘大不只對應一個站。AREX 路線圖普通車經金浦機場、弘大入口到首爾站；Visit Seoul 機場頁寫直達車為仁川機場到首爾站不停站。「夜間熱鬧街道」對應目錄的夜生活項目，與旅館距離為編輯建議。

### dongdaemun | 東大門 / Dongdaemun / 동대문

- source: Visit Seoul — Dongdaemun Design Plaza (DDP) | https://english.visitseoul.net/dongdaemunarea/Dongdaemun%20Design%20Plaza_/24680
- source: Visit Seoul — Dongdaemun Market | https://english.visitseoul.net/shopping/Dongdaemun%20Shopping%20Complex%20and%20Shopping%20Town_/171
- evidence: DDP 頁寫展覽、時裝秀等活動與季節性的 Seoul Light，交通為「Subway Lines 2/4/5, Dongdaemun History & Culture Park Station Exit 1」。市場頁寫布料、服飾等批發零售，各區營業時間不同，布料服飾與飾品區週日休息，最近的站是「Dongdaemun Station (Subway Line 1,4 Exit 8, 9)」。兩頁的站名不同，故卡片強調是兩座站。4 號線可到明洞與首爾站，是由上面明洞頁與 AREX 路線圖都列 4 號線推得。

### gangnam | 江南 / Gangnam / 강남

- source: Visit Seoul — Gangnam Station Underground Shopping Center | https://english.visitseoul.net/shopping/Gangnam-Station-Underground-Shopping-Center/ENP017740
- source: Visit Seoul — COEX | https://english.visitseoul.net/attractions/COEX_/24664
- source: Incheon Airport — Airport Railroad route | https://www.airport.kr/ap_en/1512/subview.do
- source: Visit Seoul — Getting to Seoul from the airport | https://english.visitseoul.net/airport-to-seoul
- evidence: 江南站地下街頁寫江南大路下方的街邊店與韓國知名美妝品牌，交通為「Subway Line 2/Sinbundang Gangnam Station」。COEX 頁寫大型展覽與國際會議，人流介於三成站與奉恩寺站之間。AREX 路線圖只到首爾站，沿線沒有江南一帶的站；機場巴士見 Visit Seoul 機場頁。行程集中江北時每天跨區往返是編輯推論，沒有寫車程分鐘數。

## 界線

- AREX 官網（arex.or.kr）本輪從工作環境被防火牆頁擋下，沒有直接讀取；路線停站改以仁川機場官方路線圖核對。
- 沒有逐間核對旅館、沒有實地走過出口路線，也沒有查機場巴士各路線停靠站。卡片只要求讀者自行核對。
- 這是城市頁內容改善，不是 Google 指出的退件原因，也不代表 AdSense 已通過。上線前需部署，上線後再依
  [adsense-review-readiness.md](adsense-review-readiness.md) 的流程做公開頁覆核。
