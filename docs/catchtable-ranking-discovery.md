# CatchTable 排行榜反推新店家：設計、邊界與操作

> 2026-09-22 claude-fable-5-1 應站主要求規劃；同日依站主「省 token 才做 skill、Jev 要真的更好才用」
> 的原則收斂：**不做 skill、不接 Jev**，理由在文末兩節。工作排在票
> `2026-09-22-catchtable-ranking-discovery-batch-1`；候選檔的欄位在
> `apps/api/app/foods/data/catchtable/README.md`；轉檔腳本是 `tools/catchtable_build_batches.py`。

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
4. **「菜單連結」沒有欄位。** CatchTable 店頁本身就有菜單，公開的訂位按鈕就是菜單入口；官網若有
   菜單頁，就當 `merchant_official` 來源存。要一顆獨立的「菜單」按鈕是 schema 決策（migration、
   後台、卡片、五語系），不在本計畫，列在下面的待決事項。
5. **不做 skill、不接 Jev。** skill 量出來是每個 session 多付約 280 token、批次 session 內容讀兩遍；
   Jev 做不了貴的那一步（開頁面），能做的判斷研究代理開著頁面就順手做完了。兩節理由在文末，
   也寫了什麼時候重看。

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
| 0 | 認領票、決定這批的範圍（哪個榜、哪個城市、幾家）、建 `apps/api/app/foods/data/catchtable/<batch-id>/` | 任何 session | 票的 Notes | 站主點頭家數 |
| 1 | 收集：打開榜頁，用下面「本機瀏覽器」一節的片段把 `/shop/<alias>` 清單存成 `rankings.json` | **本機瀏覽器** | alias、顯示名、名次、頁面網址、擷取時間 | 每頁的 alias 數與畫面上的家數一致 |
| 2 | 去重：對正式站目錄（worklist 匯出，含 approved）與 repo 內既有 platform_reviews 的 CatchTable 網址比對 | 任何 session | 每個 alias 標 `new` 或 `duplicate_of=<slug>` | 疑似同店的列出來給人判 |
| 3 | 逐店查證：開 `/zh-TW/shop/<alias>`，抄店名、地址、區域、料理、hreflang；判斷訂位控制項；找官方來源 | **本機瀏覽器** | `candidates.json`（欄位見資料目錄的 README） | 每筆 `import` 都有 https 的官方來源與逐字引文 |
| 4 | 轉檔：`tools/catchtable_build_batches.py` 產 `merchants.json`；匯入後拿 worklist 的 merchant_id 再產 `platform-reviews.json` | 任何 session | 兩個匯入檔加一份報告 | 腳本零錯誤；dry-run 計畫與報告一致 |
| 5 | PR：候選檔、兩個匯入檔、報告、票 | 任何 session | 合併 | CI 綠 |
| 6 | 正式站匯入：兩支指令各自先 dry-run | 主機，站主同意後 | 新 pending 店家、平台列 | 計畫與實際一致 |
| 7 | 站主給 Naver 精準頁網址；session 在站主登入的後台逐筆填入、補座標、核准（2026-09-23 起） | 後台 | 公開店家 | 公開 API 查得到 |
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

**第一批量到的（2026-09-23，30 家，報告 `docs/catalog-content-reviews/catchtable-seoul-batch-1.md`）：**

| 比例 | 值 | 意思 |
| --- | ---: | --- |
| 有官方來源 | 14/29 | 一半的店只有 Instagram；觀光局頁靠 Visit Seoul、KTO、江南區廳 Visit Gangnam、Taste of Seoul，官網靠母公司門市清單 |
| 能線上訂位 | 22/30 | 最佳榜 20/20；候位榜 2/10——候位榜不是全候位 |
| 與既有目錄重複 | 1/30 | 榜單找到的幾乎都是目錄沒有的店 |

結論：**值得跑第二批**，切法建議「首爾最佳榜第 21–40 名 ＋ 釜山最佳榜前 20」（候位榜的來源命中率與訂位率都低，第二批不再從它取）；
第二批開跑時把「操作步驟與指令」那一節升成 skill（判定規則在第一批已經改了三次，第二批之前不會再大改）。
第一批 14 家建成 pending 之後全部卡在 Naver 精準頁，這一步不解決，第二批只是把佇列拉長。
（2026-09-23 更新：Naver 這一步用「站主在自己的 Naver 地圖挑選並貼短網址、session 讀轉址取 id 並填後台」的分工，14 家裡 12 家當天公開；
剩兩家分別卡座標與 Naver 條目重複。）

## 操作步驟與指令

| 步驟 | 雲端 session | 本機（站主的瀏覽器，或本機的 Claude Code／Codex） |
| --- | --- | --- |
| 開榜頁、開店頁、判斷訂位控制項、找官方頁 | 不行（見「環境發現」） | 可以 |
| 去重、轉檔、PR、票、文件 | 可以 | 可以 |
| 正式站 dry-run 與套用 | 站主同意後在主機 | 同左 |

給代理的硬規則（提示裡要帶，來源與指示衝突時來源贏並回報）：

1. CatchTable、Naver、Google、Instagram 只當發現與定位，永不當來源。
2. 只有渲染後看到店家自己的控制項才是可訂位（有 `service-tab-DINING` 且點開有日期選擇）；只有候位分頁或「登記遠端候位」是候位，存 `disabled`。
3. 不逆向 API、不繞過封鎖、不解驗證碼、不登入、不送任何訂位表單。
4. 名次不寫進資料庫、不公開。
5. 地址只從官方頁抄；座標、Naver 網址、審核狀態批次一律不寫。
6. 語言網址照 `hreflang`；沒有 `/ko/`，不要生一個。
7. 漢字店名不猜；英文名要是拉丁字母。
8. 抓官方頁用固定 UA，`curl -sSL`，先剝 `<!-- -->` 再讀，200 的殼頁不是來源。
9. 先 `--dry-run` 再寫；動正式站之前要站主明確同意。

主機上的指令都在 `docker compose -f docker-compose.prod.yml exec -T api python -m app.cli …` 後面；
本機檢查用 repo 的 venv python（`<PY>`），從 `apps/api` 跑。`<BATCH>` 是
`app/foods/data/catchtable/<batch-id>`。

```bash
# 去重用的目錄快照（主機；含 approved，因為重複最常發生在已公開的店；--include-researched 讓 enrichment
# 已結案的店也留在清單裡，否則去重會漏）。不帶 --out：它把 JSON 寫到 stdout，一次 SSH 直接接回本機。
# 帶 --out 的話檔案落在 api 容器裡的 /tmp，主機上 cat 不到，要再 exec 一次 cat。
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli \
  export-food-merchant-worklist --status all --destination seoul --include-researched > seoul-all.json

# 候選檔檢查與轉檔（任何機器，只用標準函式庫）
<PY> ../../tools/catchtable_build_batches.py --candidates <BATCH>/candidates.json --check
<PY> ../../tools/catchtable_build_batches.py --candidates <BATCH>/candidates.json --merchants-out <BATCH>/merchants.json
# 店家套用後，用 worklist 補 merchant_id，再產平台列
<PY> ../../tools/catchtable_build_batches.py --candidates <BATCH>/candidates.json \
  --worklist seoul-all.json --platform-out <BATCH>/platform-reviews.json

# 本機用 repo 的解析器再驗一次匯入檔（不碰資料庫）
<PY> -c "from pathlib import Path; from app.foods.trend_import import load_trend_merchants; print(len(load_trend_merchants(Path('<BATCH>/merchants.json'))))"
<PY> -c "from pathlib import Path; from app.foods.platform_review_import import load_review_file; print(len(load_review_file(Path('<BATCH>/platform-reviews.json')).records))"

# 正式站：店家（先 dry-run，看 would_create 與 skipped 的理由；同意後加 --apply）
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli \
  import-trend-merchants --file <BATCH>/merchants.json
# 正式站：平台列（同樣先 dry-run；同意後加 --apply）
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli \
  apply-food-platform-reviews --file <BATCH>/platform-reviews.json
```

三個會踩到的點：`import-trend-merchants` 的稽核來源會標成 `trend-merchant-sweep`（它是為潮流街區寫的，
檔案格式通用；要改就是票 `2026-09-22-catchtable-one-pass-importer`）；平台列的 `verified` 與 `disabled`
都**強制要有 `evidence`**，一筆壞掉整個檔案被拒；管理員在後台審過的列會被跳過，除非帶精確的
`expected_checked_at`。

## 本機瀏覽器：收集榜單、看店頁、找官方來源

**榜頁抄清單。** 兩個榜都是**虛擬化清單**（2026-09-23 實測）：DOM 只保留視窗附近的十幾張
`<article>`，捲到底之後榜首就從 DOM 消失，所以「先捲到底再一次抓所有連結」會漏掉前面的店。而且被回收再利用
的卡片有時候只更新了名次徽章、內容（連結與圖片）還是舊的，用 `window.scrollTo`／`scrollBy` 跳著捲會撞到這種
半更新狀態，同一個 alias 會出現在兩個名次。可靠的做法是**重新載入頁面、只用滾輪（真實 wheel 事件）每步捲三格、
等一秒、掃一次 DOM 累積**，名次讀卡片左上角的徽章而不是 DOM 順序，任何一步出現「同名次不同 alias」或
「同 alias 不同名次」就整份作廢重抓。首爾最佳榜的網址段是 `location-seoul`（從 `location-all` 點 SEOUL 分頁得到），
候位榜第 1–4 名的卡片第一次渲染時是只有 onclick、沒有 `href` 的 `<a>`，再渲染一次就有了。

在 DevTools Console 先貼這段定義累積器，然後**用滑鼠滾輪**往下捲，每捲三格就再執行一次 `__scan()`，
直到你要的名次都齊、連續三步沒有新 alias 為止，最後印出結果：

```js
window.__r = { byRank: {}, byAlias: {}, conflicts: [] };
window.__scan = () => {
  for (const art of document.querySelectorAll("article")) {
    // 最佳榜的徽章是 div.absolute.top-0.left-0 > span，候位榜是 div[class*="top-[0px]"][class*="left-[0px]"]
    const badge = art.querySelector("div.absolute.top-0.left-0 span")
      || art.querySelector('div[class*="top-[0px]"][class*="left-[0px]"]');
    const a = art.querySelector('a[href*="/shop/"]');
    const m = a ? (a.getAttribute("href") || "").match(/\/shop\/([^/?#]+)/) : null;
    const alias = m ? decodeURIComponent(m[1]) : null;
    const rank = badge && /^\d{1,3}$/.test(badge.textContent.trim()) ? Number(badge.textContent.trim()) : null;
    if (rank == null || !alias) continue;
    const label = (a.innerText || "").replace(/\s+/g, " ").trim().slice(0, 120);
    if (window.__r.byRank[rank] && window.__r.byRank[rank].alias !== alias) window.__r.conflicts.push({ rank, was: window.__r.byRank[rank].alias, now: alias });
    if (window.__r.byAlias[alias] != null && window.__r.byAlias[alias] !== rank) window.__r.conflicts.push({ alias, wasRank: window.__r.byAlias[alias], nowRank: rank });
    if (!window.__r.byRank[rank]) window.__r.byRank[rank] = { rank, alias, label };
    if (window.__r.byAlias[alias] == null) window.__r.byAlias[alias] = rank;
  }
  const ranks = Object.keys(window.__r.byRank).map(Number).sort((x, y) => x - y);
  return { n: ranks.length, max: ranks[ranks.length - 1], conflicts: window.__r.conflicts.length };
};
window.__scan();
// 捲完之後：
// JSON.stringify({ page: location.href, captured_at: new Date().toISOString(),
//   entries: Object.values(window.__r.byRank).sort((x, y) => x.rank - y.rank), conflicts: window.__r.conflicts }, null, 2)
```

貼進 `rankings.json` 之前對三件事：`conflicts` 是空的；名次從 1 連續到你要的家數沒有缺；`label` 只是幫你認店，
店名、料理、區域以店頁為準。榜單會隨時間變（2026-09-23 前後 20 分鐘的兩次擷取，第 17–19 名順序就不同），
`captured_at` 就是證據，用擷取當下的名次，不補位、不事後對齊。換城市或料理就是換路徑段，先在畫面上切一次再抄網址，不要猜。

**店頁怎麼看。** 開 `https://www.catchtable.net/zh-TW/shop/<alias>`，等它渲染完（空殼對不存在的
alias 也回 200，真正的 404 是渲染後才出現）。

| 東西 | 在哪裡 | Console 幫手 |
| --- | --- | --- |
| 韓文店名（含分店名） | 標題底下的原文 | — |
| 道路名地址、電話、營業時間、「網站」連結 | 資訊分頁，網址就是 `/zh-TW/shop/<alias>/info`；地址預設是翻譯過的，點「原文語言」才是韓文道路名地址 | `document.body.innerText.slice(document.body.innerText.indexOf("位置"), …)` |
| 料理類型、區域 | 標題附近的標籤 | — |
| 四語網址 | `hreflang` | `[...document.querySelectorAll('link[rel="alternate"]')].map(l => l.hreflang + " " + l.href)` |
| 訂位控制項 | 「首頁」分頁裡的服務區塊：同時提供訂位與候位的店有 `service-tab-toggle`，底下是 `service-tab-DINING`（預訂）與 `service-tab-WAITING_REMOTE`（候位）兩個分頁；點開 DINING 才會出現「日期 • 時間 • 人」、日期列與「尋找可用時間」 | `document.querySelector('[data-testid="service-tab-DINING"]')?.click()` 之後看 `document.body.innerText` 有沒有「日期 • 時間 • 人」與「尋找可用時間」；`document.querySelector('[data-testid="dock-waiting-btn"]')?.innerText` |

判定：有 `service-tab-DINING`，點開後出現「日期 • 時間 • 人」與「尋找可用時間」（或沒有分頁切換、頁面直接就是
這組控制項）→ `reservation`；沒有 DINING 分頁，只有 `service-tab-WAITING_REMOTE`／`waiting-remote-content`／
`dock-waiting-btn` → `waiting_only`；什麼控制項都沒有 → `none`；頁面渲染後是 404 或身分對不上 → `unclear`。
**2026-09-21 那條「有『預訂』且沒有候位鈕才算可訂位」的規則在雙服務的店會誤判**（熟成到 乙支路店兩個分頁都有，
dock 按鈕也在），2026-09-23 起以 DINING 分頁為準。dock 按鈕上的「今日公休」只是現在不在營業時段（開店前也會
顯示），不是公休日、也不是判定依據。平台 API 的 `serviceTypes` 單獨看會誤判（효뜨那筆含 `DINING_GLOBAL` 卻只能候位），
一律以渲染後的控制項為準。

**服務區塊是 lazy section，不捲到它就永遠不會渲染**（2026-09-23 三個代理都在這裡誤判成「被擋」）：初始畫面常常只有底部橘色
「預訂」鈕或 `dock-waiting-btn`，要**逐步往下捲**（每步 500px、等 1 秒，最多 14 步）直到 `service-section-title`、`service-tab-toggle`
或 `waiting-remote-content` 之一出現，區塊出現時頁面才會呼叫 `dayslot-enc`／`timeslot-enc`／`online-reservation-open-schedule`
（訂位）這類 API。真實點一下底部「預訂」鈕也會捲到區塊，JS 的 `click()` 不會。候位制的店捲完可能還是只有 dock（區塊根本不掛載），
那就是 `waiting_only`；區塊裡的 `service-tab-RESERVED_ENTRY`（優先入場）與 `waiting-onsite-content`（現場候位）都不是訂位。
**而且只有前景分頁會掛載**：背景分頁裡 `IntersectionObserver` 的回呼不會觸發（複核者實測 1.5 秒 0 次），捲動也沒用，連訂位的 API 都不會發，
任何店都只剩底部「預訂」鈕或 dock。`tabs_select` 也救不了：**整個瀏覽器面板收起來時，前景分頁的 `document.visibilityState` 一樣是 `hidden`**
（`tabs_context` 會說 The Browser pane is currently hidden），所以只要沒有人正在看面板，任何分頁得到的「只有候位鈕」都不能算證據。
可行的做法（2026-09-23 用已知可訂位的 산청숯불가든 을지로2호점 當對照組驗過）：在 Console 把 `window.IntersectionObserver` 包一層，
讓新建立的觀察器在 `observe()` 後立刻收到一筆 `isIntersecting: true`，再點店頁自己的「菜單」→「首頁」分頁讓 LazySection 重新掛載，
區塊就會照常渲染並向 CatchTable 取真實的服務資料（`dayslot-enc` 等）。這只是讓頁面自己的元件在隱藏面板裡照常渲染，不是繞過封鎖、
不是逆向 API，做了要在報告揭露；`document.visibilityState` 要跟判定一起記，事後才分得清哪一次觀察可信。同一家店同一天兩種畫面（熟成到 乙支路店早上有雙分頁、
兩小時後只剩 dock）多半就是這個原因，分不清就記 `unclear`，不硬判。

**官方來源去哪找（依序）。** 來源要是講這家分店的頁，文字看得到、當天讀到，等級照
`docs/korea-food-specials/README.md`：觀光局店家頁（Visit Seoul 的 `KOP…` 店家頁、VisitKorea 繁中站
`big5chinese.visitkorea.or.kr` 與英文站、Visit Busan、Visit Jeju、`tour.daegu.go.kr`、`tour.jeonju.go.kr`、
區廳美食名錄）→ 政府認證名冊（백년가게、서울미래유산）→ 店家官網（店頁資訊分頁常有「홈페이지」連結；
Instagram、Naver 部落格、smartstore 不算）。米其林官網對我們每個工具都 403，不當來源也不繞。
找不到就 `no_official_source`，把搜過的關鍵字寫進 `notes`，下一批不用重找。

**每家店做完就存。** 一家寫完就存 `candidates.json`；代理被切斷時留下的是檔案，不是報告。十家一組
交回，換人抽三分之一重開店頁與官方頁。

## 環境發現（2026-09-22 實測，別再試一次）

| 試了什麼 | 結果 |
| --- | --- |
| `curl` 兩個榜頁 | 200，7,056 bytes 的 SPA 空殼，沒有店家 |
| `curl` `api.catchtable.net/api/v6/search/keyword` 與 `api/v5/shop/detail` | Cloudflare「Sorry, you have been blocked」，403；帶 Origin／Referer／sec-ch-ua 等完整瀏覽器標頭同樣 403 |
| 雲端容器的 headless Chromium 開榜頁 | `ERR_CERT_AUTHORITY_INVALID`：代理重簽的憑證不在 Chromium 的信任庫；規則是不可關驗證 |
| 2026-09-21 本機瀏覽器 | 店頁與搜尋都正常，9 筆查完並套用 |

結論：收集與逐店查證在本機做（站主的瀏覽器，或本機的 Claude Code／Codex session）；雲端 session
負責去重、轉檔、PR、票與文件。

## 為什麼現在不做 skill

量過：skill 的 description 約 280 token，Claude Code 與 Codex 都會把它塞進**每一個** session 的 skill
清單，不管那個 session 在做什麼；SKILL.md 本體約 3,100 token，內容就是這份文件的管線表與規矩，被觸發時
和這份文件一起載入等於讀兩遍。一批只跑幾次（首爾、釜山、濟州、大邱各一兩批），省不到 token，反而每個
session 都多付。等第一批跑完、確定要接著跑第二批以上，再把「操作步驟與指令」那一節升成 skill——到時
只搬指令與關卡，規則留在這裡。

## 為什麼現在不接 Jev，什麼時候重看

Jev（`apps/api/app/ai/jev.py`）只做判斷：選一個、放量表、回真偽機率。這條管線裡看起來像它的活有四件：
去重（這筆是不是目錄裡那家）、分類、商圈、官方頁是不是講本店。逐一對照後，現在接它不會比較好：

- **貴的那一步它做不了。** 成本在本機瀏覽器開店頁、找官方頁；判斷是開著頁面的那個代理順手做的。
- **多一個分類器不會少做事。** `JEV_CJK_AUTOPILOT_ENABLED` 關著，非英文 state 的 act 一律降 confirm，
  它的答案全部要人再看一次：一批 30 家，人本來就要看 30 筆，接了 Jev 還是 30 筆加一份報告。
- **沒有規模。** 一批 30 家，去重靠正規化店名加地址就剩個位數的疑似配對；商圈靠 `area_catalog` 的
  `terms` 對地址；分類是 18 選 1，研究代理讀官方頁時已經選了。
- **要先付的工不小。** 兩支指令、測試、影子量測、門檻討論，換來的是第二意見。

重看的條件（任一成立就值得開票）：出現**批次的清單來源**——例如哪天拿得到 CatchTable 或 Naver 的搜尋
結果匯出，要把幾百筆清單對到目錄，「這筆是不是那家店」的配對數才會多到人看不完；或者
`JEV_CJK_AUTOPILOT_ENABLED` 因為別的功能量出數字而打開，Jev 可以真的 act。到那時的設計從這一段重建
就夠，不必留程式：同店 `noul`、分類 `choice`（criteria 用英文寫，選項是 `category_catalog.py` 的 slug）、
商圈 `choice`（該城市的 area key，附韓文與英文）、本店 `noul`；state 只放店名、地址、料理、官方頁摘錄；
問題名以 alias 為前綴、一批一個 state、`JevRequestTooLarge` 對半切；先照 `app/hotspots/ai_search.py`
的影子模式量 agreement（整體與分語言），門檻用全站的 `jev_act_confidence`／`jev_flag_confidence`；
不問名次、價格、營業時間、日期。

## 站主要決定的事

1. **第一批範圍**：建議最佳餐廳榜首爾前 20 加候位榜前 10；或只做其中一個榜。
2. **Naver 精準頁怎麼進來**：A）站主在後台逐筆貼（第一批，不改程式）；B）候選檔多一欄
   `naver_map_url` 由站主填、匯入器寫進 `naver_map_url` 但 `map_match_status` 仍是 `unverified`
   （要改匯入器，違反「批次不寫地圖身分」的字面，需站主明確同意）。建議 A。
   **2026-09-23 站主改成 A′**：Naver 精準頁的**查找**仍是站主（`map.naver.com` 在內建瀏覽器被安全政策拒絕，
   2026-09-23 再確認，而且不繞道 Chrome 或 curl），站主把 14 條網址貼進對話；**後台的逐筆填入、座標、核准**
   改由 session 在站主登入的內建瀏覽器面板裡代操作，每一步照後台既有的驗證走，核准前把要公開的清單給站主看過。
   座標優先從官方頁自己印的座標來（Visit Gangnam、VisitKorea 頁面帶經緯度，`coordinate_source_type=official_tourism`），
   其餘用 OpenStreetMap 上店家本身的節點（`admin_verified`，來源網址是節點永久連結）；座標佇列自 2026-09-19 起只寫 Google Place ID、不寫座標，幫不上忙。
3. **只有官網、沒有觀光局頁的店要不要進目錄**：目錄本來就收 `merchant_official`（潮流街區 99 家
   多數如此），建議收；文章引用維持 A 級規則不變。
4. **菜單按鈕**：建議不開欄位；要開就是獨立的 schema 票。

## 與既有票的關係

- `2026-09-21-catchtable-apply-and-daerim`：大林倉庫餐酒館（`daelimchanggobar`）就是這條管線的第一筆
  候選，卡在 Naver 網址；第一批把它收進候選檔，不另開票。
- `2026-09-22-catchtable-one-pass-importer`（P3，依賴第一批）：店家與平台列一次寫、稽核記 alias；
  第一批證明會再跑才做。
- `2026-09-12-food-merchant-enrichment`：同一條研究路線（worklist 匯出、瀏覽器研究、JSON 匯入）。
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
