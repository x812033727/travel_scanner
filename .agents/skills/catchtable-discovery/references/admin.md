# 後台：把 pending 的韓國店家變成公開

匯入器建的店家是 `pending`／`is_active=False`／`map_match_status=unverified`、沒有座標、沒有 Naver 網址。公開的守門
（`apps/api/app/foods/publication.py` 的 `publishable_merchant_filters()`）要：approved、active、verified、經緯度在範圍內且
`coordinate_source_type` 是耐久來源、`coordinate_source_url` 是 https、韓國要 `naver_map_url` 以 `https://map.naver.com/p/entry/place/` 開頭、
至少一筆 `is_current` 來源。分類、來源、商圈匯入器已經寫好，後台不用再動。

## 每家的順序（`/zh-TW/admin/foods`，「編輯地點與來源」）

1. 先確認站主已在內建瀏覽器面板登入後台（帳密只能由站主輸入）。清單用「待審」＋目的地篩選；輸入 slug 也可以搜。
2. **座標**：緯度、經度、座標來源類型、座標來源網址（https）。來源優先序見下一節。來源是官方頁自己的座標時，把「來源 1」的「座標」claim 勾起來。
3. **Naver 精準地點頁**：貼 `https://map.naver.com/p/entry/place/<id>`（去掉查詢字串；`naver.me` 會退 422）。同一個 id 不能給第二家店（園區內的另一間餐飲要有自己的條目，否則維持 pending）。
4. **地圖比對狀態**設「已驗證」——這一下才會跑發布檢查（Naver 網址、座標、來源）；沒座標的店只能存網址、狀態留「待驗證」。
5. **審核狀態**設「核准」、勾「啟用」，和第 4 步一起按一次「儲存店家地點」。成功會出現「已儲存店家地點與來源資料。」，錯誤是視窗裡的紅字。
6. 訂位平台列由 `apply-food-platform-reviews` 寫入，不在這裡動；店家公開後 verified 的那一列才會出現在公開 API 的 `reservation_links`。

- 剛匯入的店家要重新載入後台清單才看得到；待審清單一次只顯示一個目的地，跨城市的批次要切換篩選。
- 驗證寫入時比對「當地店名」輸入框的 value，不是視窗的 innerText（輸入框的值不在 innerText 裡）。
- 整批的座標＋Naver＋已驗證＋核准＋啟用可以在一個 `doAll` 迴圈裡一家一家寫完。

React 表單的寫法：文字欄與下拉用原生 value setter 加 `input`／`change` 事件，勾選框用真實 click；關舊視窗與開新視窗之間等一秒，
否則 React 會把兩下合併成「關閉」。auto 模式下連續儲存與核准會被分類器擋成 Modify Shared Resources：用有選項的提問列出要做的動作，
站主同意後同一動作放行，或先切 Manual。

## 座標來源怎麼找（依序）

1. 官方頁 JSON-LD：Visit Gangnam（`visitgangnam.net/places/<slug>`）、VisitKorea 英文站（`contentsView.do?vcontsId=`）的 `"geo": {"@type": "GeoCoordinates", …}`。
   `curl -sSL -A "Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)" <頁面>` 後 grep `"latitude"`。類型 `official_tourism`，來源網址就是那一頁。
2. OpenStreetMap：Nominatim `https://nominatim.openstreetmap.org/search?q=<路名 門牌>&format=jsonv2&countrycodes=kr&addressdetails=1`（帶固定 UA、每秒一次），
   要的是店家本身或同門牌建物的 `node`／`way`（`addresstype` 是 `amenity`／`building`），不是 `road` 的中心。類型 `admin_verified`，來源網址 `https://www.openstreetmap.org/<type>/<id>`。
   查不到就把建物名或路名門牌拆開再查一次；還是只有路段中心就留給站主，不要硬填。同門牌的鄰居節點可以當 `admin_verified`，但要在 notes 寫明。
   - 沒有 JSON-LD 的 KTO 韓文頁：用頁面地圖呼叫的內容 API 回傳的 `mapX`／`mapY`。
   - Visit Busan 同一家店常有好幾個條目：挑地址對得上的那個 `uc_seq`。
3. Naver、Google、Kakao 的座標不能當耐久來源；座標佇列不寫座標。

## Naver 精準頁的分工

- Naver 地圖與搜尋在內建瀏覽器和 Chrome 都被 Anthropic 端安全政策拒絕，站主的授權與手動開頁都改變不了，也不用 curl 繞。
- 給站主一張「編號｜店名｜地址」的表請站主自己在 Naver 地圖搜，依**地址**挑店、按「分享→複製連結」回貼 `naver.me` 短網址，一行一家寫「編號 短網址」。
  不要給 percent-encoded 的 `map.naver.com/p/search/…` 連結：第二批的 MD 檔裡這種連結在站主那邊打不開，站主最後還是自己搜。
  同園區的另一間餐飲（例如 한국의집 的 고호재）要請站主搜那間的名字，搜主體名字只會得到主頁、與既有店家撞號。
- session 只讀短網址的轉址標頭：`curl -sS -I -A "<UA>" https://naver.me/<code>` 的 `location:` 就是 `map.naver.com/p/entry/place/<id>?…`，去掉查詢字串。
- 經營者官網自己放的 Naver 短網址（例如品牌頁分店旁）可以直接用，身分由官網背書。
- CatchTable `/info` 的「網站」欄如果就是這家店自己的 Naver 地點頁，也可以直接用，不必請站主貼。
- 解出來的 id 要對照目錄裡既有的 `naver_map_url`（worklist 有），撞到就是同一個地點，不能再建一家。

## 驗證

```bash
curl -s -H 'X-Travel-Locale: zh-TW' "https://mokaair.com/api/travel/foods/merchants?destination_id=<city>&limit=50" | python -m json.tool
```

看 `total` 的前後差、每家的 `map_links` 有 Naver、`coordinate_source.type`、`reservation_links` 只在 verified 的店出現；
換 `X-Travel-Locale: zh-CN / ja / ko` 各查一次，CatchTable 網址應分別是 `/zh-CN/`、`/ja-JP/`、無前綴。前後計數與每家的 Naver id、座標來源、核准時間寫進報告的「後台操作紀錄」。
