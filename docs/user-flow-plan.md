# Mokaair 使用流程規劃：從兩扇門到一條主線

**日期：** 2026-09-05 · **基準：** `main@2858c74`，open PR #150（行程編輯器四大痛點）尚未合併
**與 `docs/planning-flow-spec.md` 的關係：** 那份規格談的是「旅程畫布裡面」（描述 → 草稿 → 想改什麼 → 貼上 → Day Health）。這份談的是「畫布外面」：使用者從第一次進站到旅途中，各介面之間怎麼交接、哪裡登入、哪裡扣次、做完一件事之後下一步在哪。兩份互補，§7 說明合併後的順序。

---

## 0. 先講結論

**現況一句話：** 產品有兩扇門（首頁比價、`/trips/new` 排程）、三個探索面（熱門景點、美食、餐廳）、四個出發前工具（價格通知、LINE、航班動態、票價實驗室），彼此幾乎不交接。使用者每做完一件事，就得自己找下一件事在哪。

**目標一句話：** **旅程（`TripPlan`）是唯一的容器**。每個介面不是建立旅程，就是掛到旅程上；每個扣次動作都從旅程出發、結果回到旅程。登入牆放在「要儲存」那一刻，扣次牆放在「要真實報價」那一刻，而且兩道牆過了之後動作自動續跑。

**三條原則：**

1. **先給再要。** 訪客能免費走到「看見草案」；帳號在要儲存時才要；點數在要真實報價時才扣。過牆之後不重來。
2. **交接物明確。** 每個階段輸出一個物件（草案 → 旅程 → 報價 → 提醒 → 分享），下一階段只吃這個物件，不重問一次。
3. **看得見再按。** 每個扣次按鈕標價、每個上限在碰到前顯示、每次失敗都說「未扣次」（這三點程式碼裡已經做到七成，本文補剩下的三成）。

**先做的三件事（都不需要 migration，不碰 PR #150 正在改的檔案）：**

| | 做什麼 | 為什麼先做 |
|---|---|---|
| PR A | 主線不斷線：登入後自動續跑、`/trips/new` 登入帶 `next`、加入行程後連回旅程、底欄尊重旗標、訪客看不到可按的扣次按鈕 | 全是前端小修，直接修掉 §2 的 A、C、F、G 四個斷點 |
| PR B | 從搜尋儲存的旅程立刻擁有系統卡、真實報價的航班錨點與主要飯店（保留 `offer_id`） | 讓兩扇門進來的旅程長得一樣，是後面所有「從旅程出發」的前提 |
| PR E | 扣次與上限看得見：`GET /usage` 回傳已用數、旅程選單回傳上限、最佳化前先算可移動數、餘額不足不再導到買不了的頁面 | 把 402/403/422 從「事後打臉」改成「事前告知」 |

---

## 1. 事實核對：會改變規劃方向的十件事

每一項都是本次讀碼確認過的，不是從文件或提案推論的。

| 以為 | 實際 | 出處 |
|---|---|---|
| 首頁的自由文字會送給 AI 解析 | **`POST /ai/parse-trip` 在 UI 打不到。** `search-experience.tsx:425-434` 只在 `structuredParsed` 為 null 時呼叫；而 `/search` 唯一的來源 `search-workbench.tsx:115-120` 永遠帶 `origin`、`destination`、`departure_date`，所以 `structuredParsed`（`:293-296`）永遠非 null。`694e0f8` 換成真模型的解析器，目前只有手打 `/search?q=…` 才會用到 | `search-experience.tsx:293-296, 425-434`；`search-workbench.tsx:113-121` |
| 登入後會接著搜尋 | 登入後回到 `/search`，條件都在，但**要再按一次「確認條件並開始搜尋」**。`auth-form.tsx:36` 只做 `router.push(next)`，沒有人呼叫 `begin()` | `search-experience.tsx:918-945`；`e2e/full-stack.spec.ts:23-24` 明確按了第二次 |
| `/trips/new` 的登入會回來 | **不會。** 閘門連到裸的 `/login`，沒有 `next`；登入後落在首頁 | `new-trip-auth-gate.tsx:35`（其他九個登入入口都用 `loginPath()`） |
| 從搜尋存下來的旅程和 `/trips/new` 建的一樣 | **不一樣，但差異比第一眼小。** 搜尋路徑把最佳化方案原樣寫進 `data`、不跑 AI；系統卡與帶 `offer_id` 的去回程錨點其實已由 `build_itinerary` 產生（`trips/itinerary.py:232-254, 551-573`），`serialize_trip` 在建立回應時就會補齊其餘系統卡。真正缺的是：`data` 沒有 `travelers`／`preferences`／`origin_airport` 這些空白旅程才有的鍵，錨點與主要飯店**沒有價格快照**，序列化也沒有「已報價／估算」的分列。空白路徑則跑 AI 草稿（免費）、有系統卡但**沒有任何報價** | `trips/router.py:1582-1647`（搜尋）、`:1461-1484`（AI 免費）、`:542-561`（`hydrate_legacy_items`） |
| 搜到的機票可以放進**既有**旅程 | **不能。** 航班錨點只有手打一種：`apply_flight_anchor_details` 把 `offer_id` 清成 `None`、`flight_selection_source` 寫死 `manual`。住宿是唯一例外（住宿熱區 `select` 會保留 `offer_id` 與價格快照） | `trips/router.py:741-784`（`:751`、`:778`）；`stay_router.py:494-548` |
| 可以從旅程發起搜尋 | **只有住宿可以。** `SearchCreate` 沒有 `trip_id`，`POST /searches` 從不讀旅程；`stay_search_query` 已經會從旅程推導住宿查詢，這個模式存在但沒有推廣到機票 | `search/schemas.py:105-120`；`stay_areas.py:419`；`stay_router.py:131-134` |
| 旅程可以設價格通知 | 可以建，但**永遠是 `manual_only`**：`automatic_monitoring_supported` 對 `trip` 一律回 `False`，快照只讀 `trip.total_price`（空白旅程是 0）。提醒卡也**不連回旅程** | `alerts/router.py:97-113`；`alerts/monitoring.py:10-15`；`account-list.tsx:220-281` |
| 上限會提前告知 | **20 筆旅程、20 筆提醒、12 個可移動景點都是撞到才知道。** `GET /trips/options` 沒有數量與上限，`GET /usage` 有 `limits` 沒有已用數，`OPTIMIZATION_MOVABLE_LIMIT` 在 `optimize/preview` 裡面才丟 422 | `trips/router.py:1664-1689, 1449-1453, 3566-3571`；`usage/router.py:127-135`；`usage/service.py:108` |
| 點數不夠會有出路 | `insufficient_uses` 直接 `router.push("/pricing")`，而 `/pricing` 的購買按鈕是 `disabled`（購買即將開放）。註冊送 `TRIAL_3`（預設 3 次，後台可調），之後只有 CLI 能加點 | `search-experience.tsx:613-615`；`pricing/page.tsx:48`；`usage/service.py:46-60, 341` |
| `planning-flow-spec.md` 的 migration 編號可用 | **`0037` 已被 `0037_user_preferred_currency` 用掉。** 規格裡的 `0037/0038/0039` 全部要重編 | `apps/api/migrations/versions/`（head = `0037_user_preferred_currency`） |
| 漏斗看得到 | **後端零事件。** 五個事件名（`page_view`、`registration_completed`、`search_completed`、`trip_created`、`outbound_click`）全由瀏覽器送；首頁推薦、加入行程、AI 套用、最佳化套用、提醒建立、分享、扣次、402 全都沒有事件。事件名還是 DB `CHECK` | `models.py:244-262`；`analytics-provider.tsx:121-147`；`analytics/service.py:313-317` |

另外兩個影響工程方式的事實：`search-experience.tsx`（1,548 行）、`search-workbench.tsx`、`account-list.tsx`、`price-alert-button.tsx` **沒有走 i18n catalog**，靠 `legacy-ui-localizer.tsx` 的 54 條 DOM 置換；`search-experience.tsx` **沒有元件測試**，是全站最大的無測試面。任何動到這幾個檔案的 PR，都要把新字串放進 `messages/*`（`tools/check-i18n.mjs` 會擋新增的中文字），並補上該檔案的第一批測試。

---

## 2. 現況流程與斷點

```text
                    首頁 /                                    /trips
   ┌──────────────────────────────────┐          ┌──────────────────────────┐
   │ 5 步選項（日期/目的地/旅伴/住宿/偏好） │          │ 建立新行程 → 4 步精靈      │
   │ 請 AI 推薦 3 組（免費、估算）          │          │ （基本/旅伴/住宿/確認）     │
   │ 用這組條件搜尋                       │          │ 登入閘門（沒有 next）  ✗C   │
   └───────────────┬──────────────────┘          └────────────┬─────────────┘
                   ▼                                          ▼
   /search（登入牆 → 回來要再按一次 ✗A）              POST /trips source=blank
   POST /searches 扣次 → SSE → 三個推薦組合            AI 草稿免費、有系統卡、無報價 ✗B
   儲存並編輯行程（無 Idempotency-Key ✗A）
                   ▼                                          ▼
   POST /trips source=search                          /trips/[id] 行程編輯器
   方案原樣存入、無 AI、無系統卡 ✗B      ──────────▶   航班錨點只能手打 ✗B
                                                      住宿：住宿熱區（唯一保留 offer_id 的路）
                                                      沒有「查機票」入口 ✗B
                                                      md–lg 寬度沒有出口 ✗G

   /hotspots  /foods  附近餐廳                         /alerts  /flights/status  /labs/airlines
   加入行程 → 2.2 秒 toast，沒有連結 ✗D               提醒不連回旅程 ✗E
   沒有旅程 → 「請先建立旅程」沒有連結 ✗D             旅程型提醒 manual_only 等於無效 ✗E
   餐廳只能覆蓋午/晚餐槽 ✗D                          航班動態訪客可按扣次按鈕 ✗F、結果進不了旅程 ✗E
   沒有「從這裡開始規劃」✗D
                                                      /share/[token]：唯讀、沒有任何 CTA、data 整包外洩 ✗H
```

### 斷點清單

- **A. 登入牆打斷主線。** `/search` 登入回來要再按一次（`search-experience.tsx:918-945`）；`/trips/new` 登入不帶 `next`（`new-trip-auth-gate.tsx:35`）；儲存方案沒有 `Idempotency-Key`，重試會建兩筆旅程並吃掉上限（`search-experience.tsx:625`，對照 `new-trip-form.tsx:220-224` 有帶）。
- **B. 兩扇門進來的旅程不一樣，而且互相到不了。** 見 §1 第 4–6 列。結果是：比價來的旅程沒有可編輯的每日草稿與系統卡；排程來的旅程沒有價格；使用者要嘛重打航班資料，要嘛回首頁重新走一次 5 步。
- **C. 兩個規劃器重複蒐集偏好。** `search-workbench.tsx:10` 五步與 `new-trip-form.tsx:18` 四步蒐集幾乎相同的欄位（目的地、日期、人數、預算、住宿偏好、興趣、步調、備註），沒有共用狀態，也沒有互連。完成其中一個對另一個毫無幫助。
- **D. 探索面是死路。** `travel-card-actions.tsx:178-203` 加入成功只有 toast；`:36` 沒有旅程時只有一句話；餐廳只能覆蓋當天午/晚餐（`restaurants/user_router.py:171-180`、`foods/selection.py:48-53`），沒有第三餐、咖啡、點心；卡片上沒有「從這裡開始規劃」。附近餐廳還有一套平行的收藏與加入實作（`hotspot-restaurants-panel.tsx:231, 311, 330`），`/account` 只看得到 `/saved-items` 那一套。
- **E. 出發前工具不連旅程。** 提醒卡沒有連結（`account-list.tsx:220-281`）；`manual_only` 的提示叫使用者「在搜尋頁手動查看」但 `/search` 全站沒有任何 `<Link>` 指向它（只有 `search-workbench.tsx:120` 的 `router.push`）；航班動態的結果進不了旅程，頁面用文字叫使用者「票價請回旅遊搜尋比較」也沒有連結（`flight-status-search.tsx:119`）。
- **F. 訪客看得到可按的扣次按鈕。** `/flights/status` 與 `/labs/airlines` 沒有登入檢查，按鈕顯示「· 消耗 1 次」（`flight-status-search.tsx:126`、`airline-fare-lab.tsx:267-269`）；只有 `/search` 有正確的閘門（`search-experience.tsx:929-935`）。「比較更多來源」是搜尋頁唯一沒有標價的動作（`:1204-1221`）。
- **G. 導覽不一致。** 底欄不讀 site-visibility（`app-bottom-nav.tsx:7-28`），旗標關掉時桌機導覽會藏、手機底欄還是把人送進「已暫停」頁；`/foods` 沒有 layout 旗標也沒有底欄入口，手機只能從首頁快捷卡進去。（旅程頁的返回鍵是 `flex lg:hidden`，`md`–`lg` 之間仍有出口，這點核對後不算斷點。）
- **H. 分享頁是死路，而且給太多。** `shared-trip-view.tsx:17` 沒有 CTA，底欄在 `/share/` 被隱藏；`GET /shared-trips/{token}` 回傳整包 `data`（`trips/router.py:4000`），空白旅程的 `notes`、`preferences`、主要飯店的價格快照都在裡面。
- **I. 點數與上限看不見。** 見 §1 第 8–9 列。加上兩條獨立的 AI 扣次路徑（`/itinerary/generate` 與 `preview`+`apply`，`trips/router.py:2459, 2702`），以及 `restaurant-searches` 宣告了 `Idempotency-Key` 卻沒有重放（`restaurants/router.py:45-79`），重試會重複花 Google 配額。

---

## 3. 目標流程：一條主線、六個階段

```text
  免費 · 可訪客                          免費 · 需登入                        扣次 · 需登入
 ┌────────────────────────┐   草案    ┌────────────────────────┐   旅程    ┌──────────────────────────┐
 │ ① 靈感與草案             │ ───────▶ │ ② 建立旅程               │ ───────▶ │ ④ 在旅程裡比價與預訂        │
 │ 首頁：一句話／選條件      │          │ 免費 AI 草稿＋系統卡       │          │ 從旅程查機票／查住宿         │
 │ 熱門景點／美食：從這裡開始 │          │ 登入牆在這，過牆自動續跑    │          │ 報價帶回錨點（保留 offer_id）│
 │ 推薦 3 組（估算，標明）    │          │                          │          │ 聯盟 clickout 帶 trip_id     │
 └────────────────────────┘          └───────────┬────────────┘          └────────────┬─────────────┘
                                                 │ ③ 排程（畫布）                        │ 報價
                                                 │ 想改什麼／貼上／Day Health            │
                                                 │ （planning-flow-spec）                ▼
                                     ┌───────────┴──────────────────────────────────────────┐
                                     │ ⑤ 出發前（免費）                                        │
                                     │ 價格通知 ↔ 錨點、航班動態 ↔ 錨點、天氣、LINE、上限提醒     │
                                     └───────────┬──────────────────────────────────────────┘
                                                 ▼
                                     ┌──────────────────────────────────────────────────────┐
                                     │ ⑥ 旅途中與旅途後（免費）                                  │
                                     │ 今日模式、列印／ICS、分享 → 複製到我的旅程                 │
                                     └──────────────────────────────────────────────────────┘
```

每一階段的交接物：

| 階段 | 輸入 | 輸出（交接物） | 存放處 | 費用 | 登入 |
|---|---|---|---|---|---|
| ① 靈感與草案 | 一句話、選項、或一個景點 | `TripBrief`（目的地、日期或視窗、人數、預算、住宿偏好、興趣、步調、出發地、備註） | URL + `sessionStorage` | 免費 | 否 |
| ② 建立旅程 | `TripBrief` | `TripPlan`（AI 草稿、系統卡、`origin_airport`） | PostgreSQL | 免費（首次草稿本來就免費，`trips/router.py:1461-1484`） | 是，在這裡 |
| ③ 排程 | `TripPlan` | 更新後的 `TripPlan`（版本 +1） | PostgreSQL | 預覽免費，套用扣次（現況） | 是 |
| ④ 比價與預訂 | `TripPlan` → 推導搜尋條件 | `SearchRequest`（記 `trip_id`）→ 報價回寫錨點／主要飯店 | PostgreSQL + Redis | 搜尋扣次（現況規則），帶入旅程免費 | 是 |
| ⑤ 出發前 | 錨點上的 `offer_id` | `PriceAlert`（掛在 offer 上）、航班狀態快照 | PostgreSQL | 提醒免費，航班動態沿用現況（快取命中不扣） | 是 |
| ⑥ 旅途中／後 | `TripPlan` | 列印頁、ICS、分享 token、複製出來的新 `TripPlan` | — | 免費 | 分享頁否，複製要 |

### 3.1 靈感與草案（首頁、熱門景點、美食）

**使用者看到：** 首頁一個入口、三種說法。「用一句話描述」（planning-flow-spec 步驟 1 的 composer）、「選條件」（現有 5 步）、或從熱門景點／美食卡片的「從這裡開始規劃」進來。三種說法都寫進同一個 `TripBrief`。

**系統做什麼：**

- 三種入口收斂成一個型別 `apps/web/lib/trip-brief.ts`，`search-workbench.tsx` 與 `new-trip-form.tsx` 都讀寫它（`sessionStorage` 鍵 `mokaair-trip-brief`）。`new-trip-form.tsx:117-124` 已經有 `sessionStorage` 草稿還原，改成讀共用鍵即可。
- 一句話入口呼叫**現有的** `POST /ai/parse-trip`（`ai/router.py:15`，真模型、有規則備援、訪客可用、不扣次），把 `ParsedTripRequest` 回填到選項式表單，每個推測值標「推測」。這一步讓 `694e0f8` 投入的解析器第一次真的被打到。
- 「請 AI 推薦 3 組」維持現有 `POST /destinations/discover`（`places/router.py:378`，確定性估算、訪客、免費），回應裡的 `assumptions` 已經寫明「推薦階段使用估算資料，不是即時最低價」（`:504-507`），畫面照抄，不另編。
- 選定推薦後，畫面給**兩個**出口而不是一個：「先建立旅程」（→ ②，免費）與「直接比價」（→ ④，扣次）。今天只有後者（`search-workbench.tsx:113-121`）。
- 熱門景點／美食卡片新增「從這裡開始規劃」：把 `destination_id` 與該景點寫進 `TripBrief.seed_places`，導到首頁草案；建立旅程時這些景點進入待安排（planning-flow-spec 步驟 6 的 inbox，未建成前先落到第一天）。

**目的地不在目錄時：** `_load_ai_planner_candidates` 在 `match_destination` 失敗時直接回 `[]`（`trips/router.py:896-898`），AI 草稿會退成空殼。這個閘門要在草案階段就講（planning-flow-spec 步驟 1 的 `destination_supported`），不能等建完旅程才發現。

### 3.2 建立旅程（登入牆在這，過牆自動續跑）

**使用者看到：** 從草案按「建立旅程」。未登入 → 登入／註冊 → **回到同一頁、自動送出**。已登入 → 直接落在 `/trips/[id]`，草稿已在。

**系統做什麼：**

- `POST /trips`（`trips/router.py:1428`）維持 `source=blank`，新增 `origin_airport`（寫進 `data`），因為 ④ 需要出發地，而今天空白旅程沒有這個欄位。
- 20 筆上限**在按鈕上**顯示（「已建立 18／20」），不是 403 之後。資料來源見 §4.2。
- 從搜尋儲存的旅程（`source=search`）在儲存當下就補齊：立即 `ensure_system_slots`、把方案的機票寫成去回程錨點（保留 `offer_id`、價格快照、`flight_selection_source: "offer"`）、方案的飯店寫成主要飯店（沿用 `stay_router.py:521-543` 的 `lodging` 結構）、寫入與空白旅程相同的共用鍵（`travelers`、`preferences`、`origin_airport`、`destination` 經目錄正規化）。這樣 ③④⑤ 對兩種來源的旅程一視同仁。
- 儲存方案帶 `Idempotency-Key`（`search-experience.tsx:625` 補上；後端 `:1433-1448` 已支援重放）。

**登入續跑規則（全站通用，見 §4.1）：** `next` 帶回原頁，並帶 `resume=<intent>`；頁面在 `authState` 變成 `signed_in` 時執行一次該 intent，然後 `router.replace` 清掉參數。`/trips/new` 用精靈本來就有的 `sessionStorage` 還原，只需把閘門改成 `loginPath("/trips/new")`。

### 3.3 排程（畫布）

沿用 `docs/planning-flow-spec.md`：鎖定已上線（`models.py:1249`、`trip-editor.tsx:1481`），想改什麼、貼上、Day Health、列印、複製都在那份規格的 PR 序列裡。本文只加兩條介面規則：

- **加入行程要落地，不能只有 toast。** `travel-card-actions.tsx:195-197` 成功後顯示「已加入行程 · 查看旅程」連到 `/trips/{id}`（跳到指定日期的 `?day=` 深連結要動 `trip-editor.tsx`，等 PR #150 合併後再加）；沒有旅程時顯示「建立旅程」連到 `/trips/new`（PR H 之後帶 `destination_id` 進草案）。
- **餐廳與美食可以「新增一餐」。** 現在只能覆蓋午／晚餐槽（`restaurants/user_router.py:171-180`）。`trip-selections` 加 `mode: "replace_meal" | "append"`，`append` 建一般 `activity` 項目（`item_type="meal"`，不佔 `system_role`），走 `persist_system_schedule_change` 同一條寫入路徑。

### 3.4 在旅程裡比價與預訂（扣次牆在這）

**使用者看到：** 旅程頁的去程／回程錨點卡上有「查機票 · 消耗 N 次」，飯店卡有「查住宿」（住宿熱區，已存在）。按下去進 `/search?trip_id=…`，標題是「為〈京都五天〉找機票」，條件已從旅程帶入、可改。每張機票卡有「帶入去程／帶入回程」，每張住宿卡有「設為主要飯店」。帶入後回到旅程，錨點顯示價格快照與「建立價格通知」。

**系統做什麼：**

- `POST /searches` 接受 `trip_id`（`search/schemas.py:105-120` 加欄位）。伺服器從旅程推導條件：`origin_airport`、目的地經 `match_destination(...).primary_gateway`（`search-workbench.tsx:116` 已用同一欄位）、`start_date/end_date`、`data.travelers`、`data.preferences`；把 `stay_areas.py:419` 的 `stay_search_query` 抽成 `trip_search_criteria(trip, modules)` 讓機票與住宿共用。`request_json` 記 `trip_id`，結果頁據此決定顯示「帶入旅程」而非「儲存並編輯行程」。扣次規則不變（`search_operation()`，`usage/service.py:111-119`）。
- 新增 `POST /trips/{id}/flight-anchors/{direction}/from-offer {version, offer_id}`：驗證 offer 屬於該使用者的搜尋（同 `alerts/router.py:115-125` 的查法），由 offer 資料填 `FlightAnchorDetails`，**保留 `offer_id`**、寫 `price_snapshot`、`flight_selection_source: "offer"`。`apply_flight_anchor_details`（`trips/router.py:741`）加一個 offer 分支，手打分支不動。
- 旅程總價分兩欄：「已報價」（錨點與主要飯店的快照合計）與「估算」（其餘），呼應首頁承諾的「即時與估算費用分開」（`messages/zh-TW/search.json` `costBenefit`）。空白旅程今天 `total_price=0`，提醒按鈕因此被藏起來（`account-list.tsx:358`）；改用「已報價」合計。
- 聯盟：在旅程頁重新渲染 `<AffiliatePartnerOptions tripId={trip.id} />`（元件已收 `tripId`，`affiliate-partner-options.tsx:19`；後端 `affiliates/router.py:109-119` 已支援 `trip_id`）。`a5d7417` 曾把它從旅程頁拿掉，理由是無關的分頁裡佔位；這次只放在「已有主要飯店／錨點」的卡片下方，不再是獨立分頁。
- 活動與接送先不做「帶入」（結果是 offer 不是景點，需要新的項目寫入路徑）；列在 §8。

### 3.5 出發前（提醒、航班動態、天氣、LINE）

- **提醒掛在錨點上，不掛在旅程上。** 帶入報價的錨點卡直接「建立價格通知」（`resource_type=flight`，`resource_id=public_offer_id`，走現有 `POST /alerts`）。旅程型提醒（`manual_only`）在 UI 改名為「追蹤這趟旅程的已報價項目」，實作是對錨點 offer 各建一筆；沒有任何報價時按鈕說明「先查機票或住宿才能追蹤價格」。
- **提醒連回來源。** `GET /alerts` 序列化加 `links: {trip_id?, search_id?}`：`trip` 型直接給 `trip_id`；`flight/hotel` 型查 `TripPlanItem.offer_id` 是否掛在任一旅程錨點上。`account-list.tsx:220-281` 的提醒分支改成連結。`manual_only` 的提示改成「到旅程頁重新查價」並給連結，取代今天那句沒有連結的「在搜尋頁手動查看」。
- **航班動態從錨點出發。** 錨點卡「查航班動態 · 消耗 1 次（快取命中不扣）」預填班號與日期進 `/flights/status?flight_number=…&date=…`（`flight-status-search.tsx` 接受 query 參數），結果卡有「寫回旅程」把狀態快照存進錨點 `data.flight_status`（免費，`PUT /trips/{id}/flight-anchors/{direction}` 加可選 `status_snapshot`）。訪客在此頁只看到「登入後查詢」連結（§4.1）。
- **天氣**沿用 `GET /trips/{id}/weather`（`trips/router.py:1698`），不動。
- **LINE：** `line-link-panel.tsx:27` 吞掉 401 沒有訊息、`:34` 連結失效沒有出路，補上「重新登入」與「回價格通知」兩個連結。

### 3.6 旅途中與旅途後

- **分享頁有出口。** `shared-trip-view.tsx` 加兩個 CTA：「複製到我的旅程」（planning-flow-spec PR 12 的 fork；未登入走 `loginPath` 續跑）與「用 Mokaair 規劃你的旅行」（→ 首頁草案，帶 `destination_id`）。
- **分享頁少給。** `GET /shared-trips/{token}`（`trips/router.py:3975-4011`）把 `data` 改成白名單：保留 `destination_city/country`、`routing`、`planning.provider`；**剔除** `notes`、`preferences`、`travelers`、`primary_lodging.price_snapshot`。飯店名稱與地址保留（同行者需要）。
- **今日模式、列印、ICS**：沿用 planning-flow-spec PR 11、13。本文只補一條：列印頁與 ICS 的入口放在旅程頁「旅程工具」裡（`trip-editor.tsx:1430-1458`），不另開分頁。

---

## 4. 橫切規則

### 4.1 登入與續跑

- 所有登入入口一律 `loginPath(returnPath)`（`lib/navigation.ts:13-15`）。今天的例外只有 `new-trip-auth-gate.tsx:35` 與 `header-auth.tsx:15`（裸 `/login`）；後者維持（從 header 登入本來就沒有 intent）。
- `returnPath` 可帶 `resume=<intent>`：`search`（`/search` 執行 `begin()`）、`create-trip`（`/trips/new` 在還原草稿後停在確認步驟並聚焦送出鈕，不自動送出：建立旅程會吃 20 筆上限，讓使用者看一眼再按）、`fork`（分享頁執行複製）。頁面只執行一次，執行後 `router.replace` 移除參數，避免重新整理時重跑。
- **訪客看不到可按的扣次按鈕。** 規則：`useOperationCharge` 的按鈕在 `authState !== "signed_in"` 時渲染成 `loginPath(current)` 連結，文案「登入後查詢 · 消耗 N 次」。套用到 `/flights/status`、`/labs/airlines`；`/search` 已是這樣。
- 三個頁面各自打 `/auth/me`（`search-experience.tsx:399`、`new-trip-auth-gate.tsx:18`、`header-session.tsx:42`）加上 `/saved-items`（`saved-items-provider.tsx:35`），各有自己的 loading 與失敗文案。收斂成 `HeaderSessionProvider` 一份 context；`travel-card-actions.tsx:148-158` 那個「auth 還在 loading 就不彈登入」的規則照搬到所有閘門。

### 4.2 扣次與上限：送出前看得到、失敗不扣、餘額不足有出路

| 今天 | 改成 | 哪裡 |
|---|---|---|
| `GET /usage` 只有 `limits` | 加 `counts: {saved_trips, price_alerts}` | `usage/router.py:127-135` |
| `GET /trips/options` 只有 `items`，且默默丟掉沒日期的旅程 | 加 `limit`、`count`、`can_create`；沒日期的旅程改為回傳並標 `needs_dates`，選單解釋「先設定日期」而不是消失 | `trips/router.py:1664-1689` |
| 12 個可移動景點上限在 `preview` 裡才 422 | 旅程序列化加每日 `movable_count` 與 `movable_limit`；UI 在按鈕上顯示「鎖定 N 個再最佳化」（planning-flow-spec PR 9） | `trips/router.py:3559-3571, 3497` |
| 「比較更多來源」沒標價 | 免費就寫「不扣次」 | `search-experience.tsx:1204-1221` |
| `insufficient_uses` → `/pricing`（買不了） | 頁內 sheet：目前餘額、這個動作要幾次、「購買即將開放」、連到 `/account` 的使用紀錄；不離開搜尋頁 | `search-experience.tsx:613-615` |
| 兩條 AI 扣次路徑 | UI 已只用 `preview`+`apply`（`e2e/navigation.spec.ts:117` 驗證），`/itinerary/generate` 標記 deprecated、下一版移除；規則同 planning-flow-spec：「只產生 `_itinerary_preview_key` 信封，不寫第二條 apply」 | `trips/router.py:2444` |
| `restaurant-searches` 的 `Idempotency-Key` 沒用到 | 補 Redis 重放（照 `search/router.py:243` 的寫法） | `restaurants/router.py:45-79` |
| 提醒 20 筆上限撞到才 403 | 建立按鈕上顯示「18／20」 | `alerts/router.py:233`；`price-alert-button.tsx` |

不變的承諾（已在文案裡，程式碼要繼續守住）：「成功取得可用結果才扣次，失敗不扣」（`pricing.json`）、「每個計次操作會在送出前顯示消耗次數」（`pricing.json` `promises.sameHelp`）、catalog 備援不扣（`trips/router.py:2604, 2787`）、快取命中不扣（`flights/router.py:99-102`）。

### 4.3 導覽

- 底欄讀 `useSiteVisibility`，關掉的旗標不顯示（對齊 `site-navigation.tsx:36`）。
- 「探索」是一個 hub：`/hotspots` 與 `/foods` 頂端共用一條分段控制「熱門景點｜城市美食」，底欄的探索同時涵蓋兩者（`app-bottom-nav.tsx:12` 的 `matches` 已含 `/foods`，缺的是入口）。`/foods` 維持不加旗標：景點暫停時，底欄的探索改指向 `/foods`，分段控制只剩美食時不顯示。不改後台「熱門景點」開關的語意；要不要獨立的美食開關列在 §8。
- `/search` 不再是無入口頁：主要入口變成旅程頁的「查機票／查住宿」（§3.4），首頁「直接比價」是次要入口。

### 4.4 手機優先與五語系

- 每個 PR 的驗證都包含 Pixel 7 視口（`playwright.config.ts` 已有），觸控目標 ≥ 44px（`e2e/navigation.spec.ts:117` 的規則）。
- 新字串一律進 `messages/*/`，五語系同步（`tools/check-i18n.mjs` 會擋）。動到 `search-experience.tsx` 的 PR，順手把該區塊的字串搬進 catalog，逐步淘汰 `legacy.json` 的 DOM 置換；不要求一次搬完。
- `search-experience.tsx` 每個 PR 至少補一個 vitest：先補「登入回來自動續跑」與「儲存帶 Idempotency-Key」兩條。

### 4.5 觀測

事件名目前是 DB `CHECK`（`models.py:257-262`），planning-flow-spec §3 已經說過不要重複這個模式。做法：一支 migration 拿掉 `ck_analytics_event_name`，改由 `analytics/service.py:37-43` 的 `EVENT_NAMES` 驗證；然後加事件：

| 事件 | 從哪送 | 意義 |
|---|---|---|
| `discover_requested` | 瀏覽器 | 首頁入口步驟，今天完全看不到 |
| `search_started` | 伺服器（`search/router.py:56` 成功建立 job 時） | 對照 `search_completed` 得出失敗率 |
| `trip_created` | **改由伺服器**送（`trips/router.py:1643, 1559`），瀏覽器那兩處移除 | 伺服器真相，含 `source` |
| `place_added_to_trip` | 伺服器（三條 `trip-selections`） | 探索 → 旅程的轉換 |
| `ai_applied`、`optimize_applied` | 伺服器（`trips/router.py:2790, 3741`） | 畫布的核心動作 |
| `offer_attached` | 伺服器（`from-offer`、住宿 `select`） | ④ 的成功指標 |
| `alert_created`、`share_created`、`share_forked` | 伺服器 | ⑤⑥ |
| `usage_charged`、`usage_insufficient` | 伺服器（`usage/service.py:278, 243`） | 錢的真相與流失點 |
| `login_resumed` | 瀏覽器 | §4.1 是否真的省掉那一次點擊 |

伺服器端直接寫 `analytics_events`，不經過訪客 ingest（`analytics/router.py:27` 有 IP／session 速率限制，伺服器不該被它擋）。管理後台漏斗（`analytics/service.py:313-317`）從四步改成：`discover_requested → trip_created → offer_attached → outbound_click`。

---

## 5. 介面與 API 變更清單

### 介面

| 介面 | 現況 | 變更 | PR |
|---|---|---|---|
| 首頁工作台 `search-workbench.tsx` | 5 步、只有「用這組條件搜尋」、字串硬編 | 讀寫 `TripBrief`；推薦卡雙出口「先建立旅程／直接比價」；一句話入口；字串進 catalog | H（雙出口可提前到 A） |
| `/trips/new` | 4 步、閘門無 `next` | 閘門 `loginPath`；讀 `TripBrief`；新增 `origin_airport` | A（閘門）、H（其餘） |
| `/search` | 登入回來要再按；儲存無冪等；「比較更多來源」無標價；402 導到 `/pricing` | `resume=search`；`Idempotency-Key`；標價；402 頁內 sheet；`trip_id` 模式的「帶入旅程」 | A、E、D |
| 旅程頁 `trip-editor.tsx` | 錨點手打；無查機票入口；總價單一數字；`md`–`lg` 無出口 | 錨點卡：報價快照、查機票、建立提醒、查航班動態；已報價／估算兩欄；聯盟區塊；出口 | B、D、F（等 #150 合併後） |
| `/hotspots`、`/foods`、附近餐廳 | toast 死路；無「從這裡開始」；餐廳只能覆蓋 | 成功連回旅程；沒有旅程 → 建立；「從這裡開始規劃」；新增一餐；探索分段（不動旗標） | A（連結、分段）、H（從這裡開始）、F（新增一餐） |
| `/alerts` | 不連回來源；`manual_only` 提示無連結 | `links`；文案與連結 | F |
| `/flights/status`、`/labs/airlines` | 訪客可按扣次按鈕 | 登入後查詢連結；接受 query 預填；「寫回旅程」 | A（閘門）、F（預填與寫回） |
| `/share/[token]` | 無 CTA | 複製到我的旅程、用 Mokaair 規劃 | G |
| 底欄 | 不讀旗標 | 讀旗標；探索含美食 | A |
| `/pricing` | 402 的終點但買不了 | 不再作為 402 終點；保留為方案說明頁 | E |

### API

| 方法 | 路徑 | 新／改 | 重點 | 扣次 | PR |
|---|---|---|---|---|---|
| POST | `/trips` | 改 | `source=search` 寫入共用 `data` 鍵、主要飯店與錨點帶價格快照；`origin_airport` | 無 | B |
| PATCH | `/trips/{id}` | 新 | 名稱、日期、`origin_airport`、`status`、封面（= planning-flow-spec PR 1；含兩階段日期位移） | 無 | C |
| GET | `/trips/options` | 改 | `limit`、`count`、`can_create`、`needs_dates` | — | E |
| GET | `/usage` | 改 | `counts` | — | E |
| GET | `/trips/{id}` | 改 | 每日 `movable_count`／`movable_limit`；`pricing: {quoted, estimated}` | — | E、B |
| POST | `/searches` | 改 | `trip_id` + `modules` 子集；伺服器推導條件；`request_json.trip_id` | 現況規則 | D |
| POST | `/trips/{id}/flight-anchors/{direction}/from-offer` | 新 | `{version, offer_id}`；保留 `offer_id`、價格快照 | 無 | D |
| PUT | `/trips/{id}/flight-anchors/{direction}` | 改 | 可選 `status_snapshot` | 無 | F |
| POST | `/hotspots/{id}/trip-selections`、`/foods/.../trip-selections`、`/restaurants/{place_id}/trip-selections` | 改 | `mode: replace_meal \| append`；回應含 `trip_id`、`day_date`、`item_id` | 無 | A（回應）、F（append） |
| GET | `/alerts` | 改 | `links` | — | F |
| GET | `/shared-trips/{token}` | 改 | `data` 白名單 | — | G |
| POST | `/shared-trips/{token}/fork` | 新 | = planning-flow-spec PR 12 | 無 | G |
| POST | `/hotspots/{id}/restaurant-searches` | 改 | 真的重放 `Idempotency-Key` | 無 | E |
| POST | `/trips/{id}/itinerary/generate` | 棄用 | 一版後移除 | — | E |
| POST | `/analytics/events` | 不改 | 伺服器端事件直接寫表 | — | I |

### 資料模型

**migration 從 `0038` 起編號，以合併順序為準**（`0037` 已被 `0037_user_preferred_currency` 使用；planning-flow-spec 的 `0037_trip_metadata → 0038`、`0038_trip_place_candidates → 0039`、`0039_trip_item_hours_cache → 0040`，本文的 `drop ck_analytics_event_name` 視合併時間插入）。

本文需要 migration 的只有兩處：`PATCH /trips/{id}` 的 `status`／`cover_image_url`（PR C，沿用規格）與 analytics `CHECK` 移除（PR I）。其餘全部走既有欄位與 `data` JSON：`origin_airport`、`price_snapshot`、`flight_status`、`flight_selection_source` 都是 JSON 鍵；`TripPlanItem.offer_id` 欄位本來就在（`trips/router.py:457` 的 `item_record` 會寫）。

---

## 6. 交付順序與驗證

每個 PR 獨立可上線；標「等 #150」的表示會動到 `trip-editor.tsx`，排在 PR #150 合併之後以免衝突。

**PR A — 主線不斷線（前端，無 migration，不碰 `trip-editor.tsx`）— 已在本分支實作**
範圍：§2 的 A、D（連結部分）、F、G。含 `new-trip-auth-gate.tsx` 登入帶 `next`、`search-experience.tsx` 的 `resume=search` 與儲存方案的 `Idempotency-Key`、加入行程成功後「查看旅程」連結與沒有旅程時的「建立旅程」連結、底欄讀旗標與探索分段（`explore-switch.tsx`）、航班動態與票價實驗室對訪客改成登入連結、「比較更多來源 · 不扣次」、旅程型提醒卡「查看旅程」連結、分享頁「用 Mokaair 規劃你的旅行」出口、README「規則解析器」那句改掉。
驗證：vitest 新增 `search-experience.test.tsx`（登入連結帶標記、回來只跑一次並清掉標記、沒有標記不自動跑、儲存重試沿用同一把 key、比較更多來源標價）、`flight-status-search.test.tsx`、`explore-switch.test.tsx`、`shared-trip-view.test.tsx`，並補 `app-bottom-nav`、`travel-card-actions`、`account-list`、`airline-fare-lab`、`new-trip-auth-gate` 的案例；e2e：`full-stack.spec.ts` 主旅程改為「註冊回來自動開始搜尋」，`navigation.spec.ts` 加三條（登入回來自動續跑、票價實驗室訪客閘門、探索分段），`flight-status.spec.ts` 加訪客閘門。
留到後面：`?day=` 深連結（動 `trip-editor.tsx`，等 #150）、提醒卡對機票／住宿的回連（要後端 `links`，PR F）。
風險：`resume` 只在 `authState`、供應商狀態與扣次資訊三者都就緒時觸發一次，之後立刻 `router.replace` 清掉標記；重新整理或分享連結不會自己扣次。

**PR B — 旅程是容器（後端為主）— 已在本分支實作**
範圍：新模組 `apps/api/app/trips/pricing.py`（`offer_price_snapshot`、`lodging_from_offer`、`trip_pricing`）；`POST /trips` 搜尋路徑在 `data` 加上 `source`、`origin_airport`、`destination_code`、`travelers`、`preferences`、`search_criteria`，主要飯店用住宿熱區同一種結構寫入（含價格快照），去回程錨點帶 `price_snapshot`；空白旅程接受 `origin_airport`；序列化新增 `pricing`（`quoted_total`、`estimated_total`、逐項 `counted`，來回票同一個 `offer_id` 只計一次，外幣列出但不換算）；手打航班會移除快照；重新查價時錨點與主要飯店的快照跟著更新；`flight-anchor-card.tsx` 顯示「報價 NT$… · 來源 …」。
驗證：`tests/test_trip_pricing.py`（快照欄位、來回票只計一次、外幣不換算、手打無快照）；整合測試 `test_search_trip_keeps_quotes_and_the_keys_a_blank_trip_has`（本機 Postgres／Redis 跑過）；`flight-anchor-card.test.tsx`。
留到後面：`apply_flight_anchor_details` 的 offer 分支與 `from-offer` 端點（PR D），旅程頁 hero 的「已報價／估算」兩欄（等 #150）。

**PR C — `PATCH /trips/{id}`**
= planning-flow-spec PR 1，加 `origin_airport`。它的「兩階段日期位移」與 `uq_trip_plan_item_system_role` 地雷照規格處理。C 與 B 無依賴，可並行。

**PR D — 從旅程出發比價（後端＋前端，等 #150）**
範圍：`POST /searches` 的 `trip_id`；`trip_search_criteria`；`from-offer`；`/search` 的 `trip_id` 模式；旅程頁「查機票」入口；聯盟區塊回旅程頁。依賴 B（錨點要能收 offer）與 C（`origin_airport` 可改）。
驗證：新的 e2e 主旅程（見下）；`test_search_from_trip`（條件推導、他人旅程 404、沒有 `origin_airport` 時 422 並帶可用出發地）。
風險：`destination_name` 不在目錄（搜尋來的旅程存的是 `destination_city`，可能是機場代碼），推導失敗要回 422 `trip_destination_unsupported`，UI 讓使用者選機場，不猜。

**PR E — 扣次與上限看得見（前後端，小）— 已在本分支實作**
範圍：`GET /usage` 回傳 `counts`（旅程數、追蹤中的提醒數，與建立端點同一套判斷）；`GET /trips/options` 回傳 `count`、`limit`、`can_create`、`undated_count`；旅程序列化新增 `optimization`（每日 `movable_count` 與 `movable_limit`，與最佳化預覽共用同一個 `movable_slots`）；`restaurant-searches` 真的重放 `Idempotency-Key`（Redis 十分鐘）；`/itinerary/generate` 標記 deprecated；前端 `usage-insufficient-notice.tsx` 取代導到 `/pricing`（搜尋頁與票價實驗室），旅程與通知清單顯示「已建立 N／20」並在達上限時說明。
驗證：`test_restaurant_search_replay.py`、`test_trip_optimization_preview.py` 新增 `optimization_summary` 案例、整合測試的 `/usage` 與 `/trips/options` 斷言；前端 `usage-insufficient-notice.test.tsx`、`account-list.test.tsx`、`airline-fare-lab.test.tsx`。
留到後面：旅程頁最佳化按鈕上的「鎖定 N 個再最佳化」（等 #150）；`travel-card-actions` 對 `undated_count` 的提示（要先有 PATCH 才能設定日期，PR C 之後）。

**PR F — 出發前閉環（等 #150）**
範圍：提醒 `links` 與文案、錨點建提醒、旅程型提醒改義、航班動態預填與寫回、LINE 兩個訊息、新增一餐。依賴 B。

**PR G — 分享與旅途中**
範圍：分享頁 CTA、`data` 白名單、fork（= 規格 PR 12）；列印／ICS／今日入口（= 規格 PR 11、13）。

**PR H — 一個入口**
範圍：`TripBrief`、工作台雙出口、一句話入口（= 規格 PR 3、5）、「從這裡開始規劃」、工作台字串進 catalog。最大的一包，最後做；此時 A–F 已讓兩扇門進來的旅程一致，合併入口才不會把差異搬進來。

**PR I — 觀測**
範圍：§4.5。任何時間可做；建議在 A 之後立刻做，之後每個 PR 都有數據可看。

### 新的 e2e 主旅程（取代 `full-stack.spec.ts:3` 的路徑）

1. 訪客首頁 → 下一步 ×4 → 請 AI 推薦 3 組 → 「先建立旅程」
2. 登入牆 → 免費註冊（`next=/trips/new?resume=create-trip`）→ 回到確認步驟，草稿已還原 → 交給 AI 排好行程（免費）
3. `/trips/{id}`：系統卡（去回程航班、飯店、每日午晚餐）、AI 草稿、「已建立 1／20」
4. 去程錨點「查機票 · 消耗 1 次」→ `/search?trip_id=…` → 確認條件並開始搜尋 → 分析完成 → 「帶入去程」
5. 回到旅程：錨點有價格快照、總價分「已報價／估算」→ 建立價格通知 → 確認建立
6. `/alerts`：提醒卡連回旅程 → 點回旅程
7. 建立唯讀連結 → 另一個帳號開 `/share/{token}` → 「複製到我的旅程」→ 登入續跑 → 新旅程頁

手機（Pixel 7）與桌機各跑一次，與現有 e2e 相同。

---

## 7. 與 `planning-flow-spec.md` 的合併順序

| 規格 PR | 內容 | 本文對應 | 順序 |
|---|---|---|---|
| 1 | `PATCH /trips/{id}`（原 `0037`） | PR C（編號改 `0038`） | 與 A、B 並行 |
| 2 | 鎖定 | 已上線 | — |
| 3 | 解析器欄位擴充 | PR H 一併做 | H |
| 4 | 想改什麼（intents） | 畫布內，本文不重複 | B 之後（錨點與報價項目要進 preserved set） |
| 5 | 草稿優先前門 | PR H | H |
| 6 | Day Health | 畫布內 | 任意 |
| 7、8 | 貼上與 inbox 作為候選集 | 畫布內；本文「從這裡開始規劃」的 `seed_places` 在 inbox 建成後改落到 inbox | H 之後 |
| 9 | 最佳化前算可移動數 | PR E 做後端與按鈕 | E |
| 10 | 誠實路段 | 畫布內 | 任意 |
| 11、13 | 列印／ICS、PWA／今日 | PR G 只做入口與白名單，實作照規格 | G |
| 12 | fork | PR G | G |
| 14 | 聯盟帶 `trip_id` | PR D 做在錨點與飯店卡下方 | D |

規格 §7 的六個未決問題本文不重開；Q1（精修定價）在本文的框架下更容易回答：既然扣次牆放在「真實報價」，畫布內的精修保持免費是一致的。

---

## 8. 未決問題

**Q1 — 訪客能不能看到 AI 草稿？** 本文把 LLM 草稿放在登入之後（免費但要帳號），訪客只有確定性的推薦 3 組。理由是 LLM 成本與濫用；代價是「先給再要」少給了一步。選項：(a) 維持；(b) 訪客可預覽一次（IP 限流，同 `ai-trip-parse-ip` 的做法），儲存才要帳號；(c) 訪客看目錄備援草稿（免費、確定性），登入後才換真模型。**建議 (c)**：不花模型錢、能展示畫布長什麼樣、也誠實標示「依精選資料排序」。

**Q2 — 出發地。** 空白旅程沒有出發地，而搜尋一定要。選項：(a) 建立旅程時問（草案多一格，預設 TPE）；(b) 查機票時才問並存回；(c) 會員偏好（像 `preferred_currency`）。**建議 (a)+(c)**：草案有一格，預設值來自會員偏好。

**Q3 — 活動與接送要不要「帶入旅程」？** 這兩類結果是 offer 不是景點，帶入需要新的項目寫入路徑（不能走 `trip-selections`）。本文先不做；等 ④ 的機票／住宿數據出來再決定。

**Q4 — `/foods` 要不要獨立旗標？** 本文維持不加旗標（PR A 只讓探索入口在景點暫停時改指向美食）。如果營運上需要單獨關掉美食，要加第七個布林到 `site-visibility`（`lib/site-features.ts`）與後台版面設定，成本不高但要一起改五語系文案。

**Q5 — 餘額不足的真正出路。** 購買未開放前，402 的 sheet 只能說「即將開放」。要不要在後台加「申請試用加點」的自助流程（寫入 `usage_ledger` 的 adjustment，需管理員核准）？這是產品決定，不是工程問題。

**Q6 — `/labs/airlines` 與 `/flights/status` 在主線上的位置。** 兩者都不連旅程。本文只修閘門（A）與航班動態的預填／寫回（F）；票價實驗室維持研究面，不進主線。

---

## 附錄：不做、延後

- 即時協作編輯、App 內訂票、原生 App、插畫小書：沿用 planning-flow-spec §5 的取捨。
- 把 `search-experience.tsx` 一次搬進 catalog 與拆檔：只隨 PR 逐步做，不獨立成一個大 PR。
- 對舊旅程回填錨點 `offer_id`：不做；舊搜尋的 offer 早已過期，回填只會製造看似有效的價格。
- 提醒的背景監控擴到 Skyscanner：`AUTOMATIC_FLIGHT_PROVIDERS` 只有 `amadeus/duffel/mock`（`alerts/monitoring.py:6`），是供應商條款問題，不在本文範圍。
