# 台灣、越南、泰國、新加坡訂位平台查核紀錄（2026-09-13）

日本第二輪（[`2026-09-12-japan-platforms-second.md`](2026-09-12-japan-platforms-second.md)）證明了
一件事：2026-09-11 那輪留下的候選頁很稀，不是因為店家沒有平台頁，而是因為當時的查法沒掃到。
這一輪把同樣的懷疑套到其他四個國家——**105 間還沒有訂位連結的公開店家**，每一國都改用
**該平台自己的搜尋介面**重查一次。

| 國家 | 公開店家 | 這輪查的（沒有訂位連結） | 查完新增可訂位 |
| --- | ---: | ---: | ---: |
| 台灣 | 55 | 50 | 0 |
| 越南 | 24 | 24 | 0 |
| 泰國 | 25 | 20 | 0 |
| 新加坡 | 24 | 11 | 0 |

## 做法：先證明搜尋管道有效，再用它當「查無」的依據

2026-09-12 韓國那一輪的教訓是，一個回得出結果的搜尋介面不等於一個有用的索引——DuckDuckGo 對
`booking.naver.com` 每一查都回同一批無關商家。所以這一輪每個管道都先拿該平台上**已知存在**的
店家試過，確定會回傳正確結果，才拿它的空結果當證據。

| 平台 | 管道 | 驗證方式 |
| --- | --- | --- |
| EZTABLE（台灣） | `api-evo.eztable.com/search/autocomplete?keyword=` | 網站自己的「餐廳名稱搜尋」用的就是這一支 |
| inline（台灣） | 限定 `inline.app` 網域的網路檢索 | 查得到春水堂、舊振南、第四信用合作社、SIDOLI RADIO 的店頁 |
| Chope（新加坡、泰國） | 官方 `sitemap.xml` 全量比對（22,631 個店家頁） | 內含新加坡 3,982、曼谷 625、普吉 126 家 |
| Hungry Hub（泰國） | `puma.hungryhub.com/graphql` 的 `SearchSuggestions` | 「Copper Beyond Buffet」兩家分店都查得到 |
| PasGo（越南） | `pasgo.vn/Search/SearchHeader`（`keySearch`） | 峴港的 Cá Voi、Cây Dừa 都查得到，含變音字比對 |
| SevenRooms | 限定 `sevenrooms.com` 網域的網路檢索 | 查得到新加坡既有的 gu-um、nomada 等訂位頁 |

候選頁一律**實際打開**再判斷能不能訂位，判斷依據只看頁面上本店自己的訂位控制項：

- **Chope**：可訂位的頁標題是 `… - Book and Save On Chope` 且有 `id="time-field"` 訂位框；
  不可訂位的頁標題是 `… - Discover On Chope`，版面上寫
  `Sorry, this restaurant is not accepting reservations on Chope.`。
  （頁面 JavaScript 裡另有一句 `The restaurant is not accepting any more reservations for the
  selected date.`，那是 **每一頁都有** 的 alert 字串，拿它當關鍵字會把可訂位的頁也判成不能訂位。）
- **inline**：不開放時頁面寫「抱歉，目前尚不開放線上訂位」，只留電話；可訂位時是日期與人數的表單。
- **Hungry Hub**：搜尋回傳的 `searchScore` 高分才是真的同名店，低分是平台自己的推薦補位。
- **EZTABLE**：`/restaurant/{id}` 頁的 `__NEXT_DATA__` 帶 `info.active` 與 `info.hide`。

## 結果：四國全數查無，可訂位的店家沒有增加

寫入 **104 筆**：`not_found` 102、`disabled` 2。這一輪**沒有**任何一家變成可訂位。

| 國家 | 平台 | 查無 | 有店頁但不能訂位 |
| --- | --- | ---: | ---: |
| 台灣 | EZTABLE + inline | 49 | 1（春水堂 信義店） |
| 越南 | PasGo | 24 | 0 |
| 泰國 | Hungry Hub + Chope | 20 | 0 |
| 新加坡 | Chope + SevenRooms | 9 | 1（The Blue Ginger 丹戎巴葛） |

這不是查核失敗，是這份清單的本質：四國這 105 間裡，路邊攤、老字號小吃、甜品店與書店咖啡佔絕大多數，
而這些平台服務的是會簽約付費的餐廳。可訂位的店家數維持 59 / 331。

## 解掉的三個 2026-09-11 懸案

2026-09-11 有三間店因為 inline 的「按壓不放」驗證一直沒能確認，這次打開了兩間，兩間都是
**確認是本店、確認不開放線上訂位**：

| 店家 | inline 店頁上的地址 | 頁面結論 |
| --- | --- | --- |
| 春水堂 信義店 | 台北信義新天地A9店-B1F | 「抱歉，目前尚不開放線上訂位」，只留 02-2723-9913 |
| SIDOLI RADIO 小島裡 | 台北市大同區長安西路245號1樓 | 「抱歉，目前尚不開放線上訂位」 |

兩筆維持停用，但理由從「沒能確認」變成「確認過不能訂位」。

## 同品牌不同分店：三個沒有採用的候選頁

平台上找得到品牌，不代表找得到清單這一家。這三個候選頁都是本輪找到、而且**刻意不採用**的：

| 清單店家 | 平台上的候選頁 | 為什麼不是同一家 |
| --- | --- | --- |
| Krua Apsorn（曼谷，13.7259/100.5467） | Hungry Hub `kruaapsorn-samsen-bangkok`、`krua-apsorn-at-shinawatr-3-building-bangkok` | 兩頁的座標是 13.7749/100.5107 與 13.8247/100.5582，相距 6.5 km 與 11 km |
| 富錦樹咖啡 富錦店（富錦街 353 號） | inline「富錦樹台菜香檳 敦北店」 | 同集團的另一個品牌、另一個地址 |
| The Blue Ginger（97 Tanjong Pagar Road） | Chope `the-blue-ginger-great-world` | 另一家分店，而且同樣不能訂位 |

鼎泰豐 信義店也屬於這一類的變形：inline 上鼎泰豐有八個分店頁，**全部都是 `/order/` 線上訂餐**，
沒有任何 `/booking/` 訂位頁。

## Chope sitemap 上還在、頁面已經沒了

新加坡有三間店的 Chope 店家頁還留在官方 sitemap 裡，但網址現在都回 404：

- `samy-s-curry-sg-793095`（Samy's Curry）
- `chye-seng-huat-hardware-sg-3540914`（Chye Seng Huat Hardware）
- `the-banana-leaf-apolo-little-india-sg-739223`（The Banana Leaf Apolo）

這三筆記成 `not_found` 並在 `review_note` 寫明「sitemap 還在、頁面已移除」，免得下一輪又從
sitemap 撿到同樣的網址。

## 搜尋介面的兩個陷阱（下一輪別再踩）

1. **EZTABLE 的 `hide` 旗標**：`圓環邊蚵仔煎`（id 16654）在 EZTABLE 上是 `active: 1` 的可訂位店家，
   但 `hide: 1`，於是**它自己的搜尋（不論是網頁還是 autocomplete）都找不到它**。所以 EZTABLE 的
   空結果只能當成「搜尋索引裡沒有」，不能單獨當成「這家店不在 EZTABLE 上」——這一輪因此把
   inline 的網路檢索當成第二個管道，兩邊都空才記 `not_found`。
2. **PasGo 與 Hungry Hub 的預設清單**：`pasgo.vn/tim-kiem?keyword=` 這個網址不管關鍵字是什麼，
   伺服器都回同一批 20 家餐廳（真正的搜尋在 `Search/SearchHeader`）；Hungry Hub 的
   `enableFallback` 會在查無時補一批推薦。兩者都會讓「有結果」看起來像命中。

## inline 的按壓驗證

`inline.app` 對一般抓取一律回 403，內建瀏覽器則是**開一頁就會被「按壓不放以確認您是人類」擋住**，
要等幾分鐘才能再開下一頁（403 與按壓牆對 WebFetch 一樣有效）。這一輪靠的是「檢索找頁、
隔開時間逐頁開」的節奏。inline 的 Firebase（`inline-live-*.firebaseio.com`）回 `Permission denied`，
沒有繞過去的資料路徑。

## 還沒做完的

- `kaohsiung-jiu-zhen-nan`（舊振南餅店 高雄）的 inline 列仍是 `ambiguous`：品牌在 inline 上有
  `-NADjl6fHKgbU-9W6laz:inline-live-1`，檢索也看得到「舊振南餅店 高雄中正店」
  （`/-NAJO8JVP2S8P6_wsanZ`）與台南新光三越店，但這一輪被按壓牆擋住，沒能確認中正店就是清單這一家、
  也沒能確認它開不開放線上訂位。**這一筆這次不寫入**，維持原狀。
- `taipei-cafe-acme-fine-arts-museum`（CAFE ACME 北美館）：inline 上有品牌頁
  `-MYne3QpFTXQSW31f8Kt:inline-live-2`，但品牌頁沒有分店代碼、不能存；北美館分店的分店頁還沒拿到。
- 這一輪只查了四國的支援平台。台灣還有 FunNow、饗訂位等平台，泰國還有 Eatigo、TableCheck，
  都不在白名單上，也沒有證據顯示清單上的店家在用。
