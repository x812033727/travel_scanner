# CatchTable 排行榜反推新店家：設計與邊界

> 2026-09-22 claude-fable-5-1 應站主要求規劃。這一份是**規則與設計**；操作步驟在 skill
> `.agents/skills/catchtable-discovery/SKILL.md`（Claude Code 讀 `.claude/skills/` 的逐字複本）；
> 工作排在兩張票：`2026-09-22-catchtable-ranking-discovery-batch-1`（第一批，本機瀏覽器路線，
> 不改程式）與 `2026-09-22-catchtable-import-and-jev`（匯入指令與 Jev 判斷）。

站主給的兩個入口：

| 頁 | 網址 | 是什麼 |
| --- | --- | --- |
| 候位榜 | `https://www.catchtable.net/zh-TW/top-list/waiting/seoul/all` | 首爾候位人數排行；路徑最後兩段是城市與料理類型 |
| 最佳餐廳榜 | `https://www.catchtable.net/zh-TW/ranking/location/location-all` | 全韓國的「最佳餐廳」榜；路徑最後一段是地區 |

## 結論先講

1. **做得到，而且第一批不用寫程式。** 排行榜只當「發現清單」；每家店仍然要找到官方來源
   （店家官網或觀光局的店家頁）才進目錄，用現有的 `import-trend-merchants --file`；訂位連結
   走現有的 `apply-food-platform-reviews --file`。兩支指令都先 dry-run，站主同意後才 `--apply`。
2. **收集與逐店查證只能在本機瀏覽器做。** 2026-09-22 從雲端容器實測：`api.catchtable.net`
   被 Cloudflare 擋（403 封鎖頁，帶完整瀏覽器標頭也一樣）；headless Chromium 又卡在代理憑證
   不受信任，而且不可以關掉憑證驗證。2026-09-21 那批 9 筆就是本機做的，方法可以照抄。
3. **新店家落地後是 pending／inactive／unverified，不會自動公開。** 韓國店家公開的守門是
   Naver 精準地點頁（`publishable_merchant_filters()`，見 `2026-09-06-naver-maps-key`），
   目前只有站主能在後台逐筆貼。沒有這一步，這條管線產出的是**審核佇列**，不是公開店家。
4. **Jev 的位置是四個判斷題**（同一家店？哪個分類？哪個商圈？官方頁講的是本店？），先影子量測
   再決定哪一題可以放手。`JEV_CJK_AUTOPILOT_ENABLED` 關著，所以現階段所有「act」都會降成
   「confirm」：Jev 負責排序與標旗，人負責最後一下。
5. **「菜單連結」沒有欄位。** CatchTable 店頁本身就有菜單，公開的訂位按鈕就是菜單入口；官網若有
   菜單頁，就當 `merchant_official` 來源存。要一顆獨立的「菜單」按鈕是 schema 決策（migration、
   後台、卡片、五語系），不在本計畫，列在下面的待決事項。

## 排行榜能給什麼、不能給什麼

從渲染後的頁面看得到：名次、店名（榜頁語言的顯示名）、料理類型、區域、店頁連結
`/zh-TW/shop/<alias>`。alias 是唯一可靠的識別碼（`koreahouse`、`hieutu_yongsan`、`hani._.noodle`
沒有規律），也是我們平台連結規則認的東西。

不做的事，2026-09-21 已經定了（票 `2026-09-21-catchtable-apply-and-daerim`）：

- **不逆向 API。** 站是 SPA，原始 HTML 是空殼，不存在的 slug 也回 200，API 回應有加密。
  只讀瀏覽器渲染出來的畫面。
- **名次不落地、不公開。** 理由同 `docs/hotspot-intelligence.md` 對 Google Places 的政策：
  平台內容不能變成我們的耐久排名資料。名次只寫在批次檔的 `ranking_evidence`，當本批的處理
  順序與「為什麼看這家」的證據。
- **不捏造韓文網址。** 店頁的 `hreflang` 只有 `/zh-TW/`、`/zh-CN/`、`/ja-JP/` 與無前綴的
  x-default；沒有 `/ko/`。`ko` 讀者拿到的是無前綴網址，這是既有行為。

## 邊界（站主已定，不重開）

| 規則 | 定於 | 對這條管線的意思 |
| --- | --- | --- |
| Google／Naver／米其林與訂位平台只當定位與發現，永不當來源 | 2026-09-12，`apps/api/app/foods/enrichment.py` 的 `PLATFORM_HOSTS` | CatchTable 找到的店，仍要有官網或觀光局頁才能建店家；沒有就停在候選檔的 `no_official_source` |
| 只有真的能訂位的平台頁才公開；只能候位存 `disabled` | 2026-09-11，`docs/food-reservation-platforms.md` | 判斷看店家自己的控制項（「預訂」、日期人數、「尋找可用時間」），不整頁搜關鍵字；頁尾「如果您喜歡」會列別家店 |
| 批次與 AI 永不寫座標、地圖身分、審核狀態 | 2026-09-12，`docs/catalog-review.md` | 匯入器只建 pending 列；Naver 精準頁與核准是後台的事 |
| 韓國的精準地圖身分只認 Naver 地點頁 | `apps/api/app/foods/publication.py` | 每家新店都欠站主一次貼網址 |
| 地址只從官方頁抄 | 2026-09-12 enrichment 規則 | CatchTable 的地址只用來核對「是不是同一家」與找官方頁 |
| 對外 UA 固定為 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，不帶任何人的個資 | content-pipeline skill | 抓官方頁時適用；瀏覽器逐頁看不套用 UA |
| 內建瀏覽器被擋的站（Naver 地圖）不可改用 Chrome 或 curl 繞過 | 2026-09-21 | Naver 網址由站主提供 |

## 管線

| # | 階段 | 在哪裡跑 | 產出 | 關卡 |
| --- | --- | --- | --- | --- |
| 0 | 認領票、決定這批的範圍（哪個榜、哪個城市、幾家） | 任何 session | 票的 Notes | 站主點頭家數 |
| 1 | 收集：打開榜頁，用 DevTools 片段把 `/shop/<alias>` 清單存成 JSON | **本機瀏覽器** | `rankings[]`（alias、顯示名、名次、頁面網址、擷取時間） | 每頁的 alias 數與畫面上的家數一致 |
| 2 | 去重：對正式站目錄（worklist 匯出，含 approved）與 repo 內既有 platform_reviews 的 CatchTable 網址比對 | 任何 session | 每個 alias 標 `new` 或 `duplicate_of=<slug>` | 疑似同店的列出來給人（第二階段給 Jev）判 |
| 3 | 逐店查證：開 `/zh-TW/shop/<alias>`，抄店名、地址、區域、料理、hreflang；判斷訂位控制項；找官方來源（VisitSeoul 店家頁、VisitKorea、區廳名錄、店家官網） | **本機瀏覽器** | `records[]`（見 `references/candidate-file.md`） | 每筆 `import` 都有 https 的官方來源與逐字引文 |
| 4 | 產檔：`build_batches.py` 把候選檔轉成 `merchants.json`（trend 匯入格式）；匯入後拿 worklist 的 merchant_id 再轉出 `platform-reviews.json` | 任何 session | 兩個匯入檔加一份報告 | 腳本零錯誤；dry-run 計畫與報告一致 |
| 5 | PR：候選檔、兩個匯入檔、報告、票 | 任何 session | 合併 | CI 綠 |
| 6 | 正式站匯入：`import-trend-merchants --file … `、`apply-food-platform-reviews --file …`，各自先 dry-run | 主機，站主同意後 | 新 pending 店家、平台列 | 計畫與實際一致 |
| 7 | 站主動作：後台貼 Naver 精準頁、座標佇列驗證、核准 | 後台 | 公開店家 | 公開 API 查得到 |
| 8 | 驗證與交接：公開 API 抽查、報告補數字、開後續票 | 任何 session | 票 done | 前後計數寫進報告 |

第一批只做到第 6 步就算完成（第 7 步是站主的），報告要寫清楚：幾家進了 pending、幾家有訂位、
幾家等 Naver。

## 每家店要收的東西與去向

| 欄位 | 從哪來 | 寫到哪 | 規則 |
| --- | --- | --- | --- |
| alias、店頁四語網址 | 店頁 `hreflang` | `food_merchant_platform_links`（`catchtable_global`） | 網址規則在 `apps/api/app/foods/platform_links.py`；`ko` 不存 |
| 能不能訂位 | 渲染後店頁的控制項 | 平台列的 `status`（verified／disabled） | 只有本店控制項算數；「今日公休」看不到控制項就改天再看，不硬判 |
| 韓文店名、中文名、英文名 | 店頁與官方頁 | `food_merchants.local_name`／`names_json`／`name` | 漢字店名不猜（`docs/korea-food-specials/README.md`）；英文名要是拉丁字母 |
| 道路名地址 | **官方頁**（官網或觀光局） | `food_merchants.address` | CatchTable 的地址只用來核對同店 |
| 商圈 | 地址對 `apps/api/app/foods/area_catalog.py` 的 `terms` | `area_id`（`area_source=admin`） | 對不到就留空，不硬塞 |
| 分類（至多 3） | 官方頁的菜色描述；CatchTable 的料理類型只當提示 | `food_merchant_categories` | slug 見 `apps/api/app/foods/category_catalog.py`；韓式家常大多是 `home-style`、`hotpot-soup`、`bbq-grill` |
| 來源 | 官網（`merchant_official`）或觀光局店家頁（`official_tourism`） | `food_merchant_sources` | 必須是講**這家分店**的頁；品牌總站要有分店資訊才算 |
| 座標 | 不從 CatchTable 來 | 之後由 `fill-food-merchant-coordinates` 讀官方頁 JSON-LD，或座標佇列 | `DURABLE_COORDINATE_SOURCES` 不含平台 |
| Naver 精準頁 | 站主 | 後台 | 批次不寫 |
| 名次 | 榜頁 | 只在候選檔的 `ranking_evidence` | 不落地、不公開 |

## 漏斗會長什麼樣（先講清楚，免得期待錯）

2026-09-11 從目錄往 CatchTable 查，80 家公開韓國店家只有 7 家能在 CatchTable 訂位，
60 家根本不在上面，11 家只能候位。反過來從榜單出發，店家一定在 CatchTable 上，但：

- **候位榜**的店，顧名思義多半是候位制，平台列會大量落在 `disabled`；它的價值是「發現熱門店」，
  而候位制的店往往用 Naver 예약，接得上 `2026-09-12-naver-booking-ids`。
- **最佳餐廳榜**比較可能有線上訂位，是「訂位連結」目標的主力。
- 兩個榜都會有一部分店只有 Instagram，沒有官網也沒有觀光局頁——這些**進不了目錄**（來源規則），
  只留在候選檔的 `no_official_source`，等有來源再復活。

所以第一批建議：**最佳餐廳榜的首爾區前 20 家加候位榜前 10 家**，量一次三個比例（有官方來源、
能訂位、與既有目錄重複），再決定下一批怎麼切。這是建議，家數由站主定。

## Jev 放哪裡、怎麼放

Jev（`apps/api/app/ai/jev.py`）只回答選擇、量表、真偽三種問題，帶校準過的信心；README 明寫它
的位置之一就是「把店家對到平台清單」。這條管線裡有四個純文字判斷題適合它，也只有這四個：

| 題 | 型別 | state | 回答怎麼用 |
| --- | --- | --- | --- |
| 同一家店：CatchTable 這筆與目錄的 `<slug>` 是不是同一家分店 | `noul` | 兩邊的韓文名、地址、區域 | 只問名稱相似的配對；≥ act 才當重複，其餘進人工清單 |
| 分類：這家店最像哪個 `category` | `choice`（18 個 slug，附英文名） | 韓文名、CatchTable 料理類型、官方頁一句描述 | 主分類的建議；人確認 |
| 商圈：地址落在哪個 `area` | `choice`（該城市的 area，附韓文與英文） | 道路名地址 | 對不到 `terms` 時才問；人確認 |
| 本店：找到的官方頁講的是不是這家分店 | `noul` | 官方頁標題與前幾百字、店名、地址 | 低於 flag 直接退回重找 |

不問的：名次、價格、營業時間、日期（TypeSafe 自己公布的弱點），還有「這家店紅不紅」（那是
榜單的事，我們不做排名）。

怎麼放手：照 `jev_shadow_guide_assessment` 的先例，**先影子**——第一批由人判完，再把同一批
餵給 Jev，用 `route_answer` 分 act／confirm／hold，算每一題的 agreement（整體與分語言）；
門檻 `jev_act_confidence`（0.9）與 `jev_flag_confidence`（0.5）是全站設定，不另開一套。
分類與商圈是低風險欄位（分類只增、商圈是瀏覽提示），agreement 夠高才值得為它們打開
`JEV_CJK_AUTOPILOT_ENABLED`；同店與本店這兩題關係到「寫錯一家店」，維持 confirm。
每日預算 `jev_daily_call_budget`（200）：一批 30 家把候選放進同一個 state、問題以 alias 為前綴
批次送，是個位數的呼叫。

程式落點寫在票 `2026-09-22-catchtable-import-and-jev`：一個讀候選檔、問 Jev、把答案與人的判定
並排印成報告的指令，什麼都不寫；以及一個把候選檔直接匯入（店家加平台列一次寫、CatchTable alias
當證據記進稽核）的匯入器，取代第一批用的兩段式轉檔。

## 環境發現（2026-09-22 實測，別再試一次）

| 試了什麼 | 結果 |
| --- | --- |
| `curl` 兩個榜頁 | 200，7,056 bytes 的 SPA 空殼，沒有店家 |
| `curl` `api.catchtable.net/api/v6/search/keyword` 與 `api/v5/shop/detail` | Cloudflare「Sorry, you have been blocked」，403；帶 Origin／Referer／sec-ch-ua 等完整瀏覽器標頭同樣 403 |
| 雲端容器的 headless Chromium 開榜頁 | `ERR_CERT_AUTHORITY_INVALID`：代理重簽的憑證不在 Chromium 的信任庫；規則是不可關驗證 |
| 2026-09-21 本機瀏覽器 | 店頁與搜尋都正常，9 筆查完並套用 |

結論：收集與逐店查證在本機做（站主的瀏覽器，或本機的 Claude Code／Codex session）；雲端 session
負責去重、轉檔、PR、票與文件。

## 站主要決定的事

1. **第一批範圍**：建議最佳餐廳榜首爾前 20 加候位榜前 10；或只做其中一個榜。
2. **Naver 精準頁怎麼進來**：A）站主在後台逐筆貼（第一批，不改程式）；B）候選檔多一欄
   `naver_map_url` 由站主填、匯入器寫進 `naver_map_url` 但 `map_match_status` 仍是 `unverified`
   （要改匯入器，違反「批次不寫地圖身分」的字面，需站主明確同意）。建議 A。
3. **只有官網、沒有觀光局頁的店要不要進目錄**：目錄本來就收 `merchant_official`（潮流街區 99 家
   多數如此），建議收；文章引用維持 A 級規則不變。
4. **菜單按鈕**：建議不開欄位；要開就是獨立的 schema 票。
5. **Jev 何時上**：第一批用人判，同時留下 Jev 影子報告；第二批起看 agreement 決定分類與商圈要不要放手。

## 與既有票的關係

- `2026-09-21-catchtable-apply-and-daerim`：大林倉庫餐酒館（`daelimchanggobar`）就是這條管線的第一筆
  候選，卡在 Naver 網址；第一批把它收進候選檔，不另開票。
- `2026-09-12-food-merchant-enrichment`：同一條研究路線（worklist 匯出、瀏覽器研究、JSON 匯入）；
  票二的 `apps/api/app/cli.py` 與它的 scope 重疊，兩張不要同時認領。
- `2026-09-12-naver-booking-ids`：候位制的店改查 Naver 예약，是這條管線的下游。
- `2026-09-06-naver-maps-key`：公開的守門；金鑰到手後，第一批的 pending 列可以批次對 Naver。
- `2026-09-20-launch-korea-food-specials-1` 與後續特輯：候選檔裡有 A 級來源的店，可以當下一批特輯的店。

## 驗證

正式站套用後（第 6 步）：

```bash
# 新店家進了 pending（家數要等於 merchants.json 的 would_create 數）
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli \
  export-food-merchant-worklist --status pending --destination seoul --out /tmp/seoul-pending.json
# 平台列（verified 的才會出現在公開 API，而且要等店家核准；pending 店家看後台）
curl -s -H 'X-Travel-Locale: zh-TW' "https://mokaair.com/api/travel/foods/merchants?destination_id=seoul&limit=50" \
  | python -m json.tool | grep -A3 catchtable_global
```

`X-Travel-Locale` 只吃 `en / ja / ko / zh-TW / zh-CN`，送 `ja-JP` 會安靜回退成 zh-TW；
`limit` 上限低於 100（2026-09-21 實測）。
