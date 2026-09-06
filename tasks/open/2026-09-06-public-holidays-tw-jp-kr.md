---
id: 2026-09-06-public-holidays-tw-jp-kr
title: 國定假日資料：台日韓 2026-2027 進版控，日曆看得見連假與補班
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-06T13:17:37Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/holidays
  - apps/api/app/main.py
  - apps/api/app/cli.py
  - apps/api/tests/test_public_holidays.py
  - apps/web/lib/holidays.ts
  - apps/web/components/date-range-picker.tsx
  - docs/public-holidays.md
---

# 國定假日資料：台日韓 2026–2027 進版控，日曆看得見連假與補班

## Why

產品目前完全沒有假日資料：`grep -rn "holiday\|假日\|連假" apps/api/app apps/web/{app,components,lib} docs tasks` 只命中 `apps/api/app/destinations/localized.py:190` 的英文文案、以及 `apps/api/app/foods/data/trend_merchants.json` 商家備註裡的「假日」字樣。零筆真正的日曆資料。

價值不對稱，寫規格時請以**目的地側**為主：台灣使用者早就知道春節在幾月，台灣資料的價值是**機械性**的——讓日曆知道哪個星期六是補班日、讓連假長度算對。真正買方不知道的資訊是：5/3 抵達關西代表新幹線與商務旅館全滿、お盆整週房價翻倍、추석 讓首爾一半餐廳拉下鐵門。這些今天在 `/trips/new` 的月曆與 `/search` 的彈性日期上完全不可見。

### 這是「把兩份政府檔案進版控」，不是「接一家 provider」

假日一年變一次、且提前數月公告。跑 runtime API 只會換來一筆 `PROVIDER_DEFINITIONS`、一把 Fernet 金鑰、一個 `providerCategoryOf` 對應、一組 TTL、以及一條原本不會失敗的頁面新增的 503 路徑。天氣值得那套機器是因為它每小時變；這個不值得。倉庫已經有現成做法：`apps/api/app/foods/data/trend_merchants.json` 的委任 JSON + CLI（`apps/api/app/cli.py:642` 的 `fill-hotspot-labels`、dispatch 在 `:815`），一年跑一次、用 PR diff 審。**本任務不新增 provider、不新增 migration、不進 admin 面板、不需要任何 API key。若範圍長出這些，就是寫錯了。**

### 已驗證的來源事實（不要重做這段研究）

**🇹🇼 DGPA 辦公日曆表 — 權威且唯一可用**
- 目錄 API：`GET https://data.gov.tw/api/v2/rest/dataset/14718` → HTTP 200，`license: "1"`（政府資料開放授權條款第1版），`cost: 免費`，`modifiedDate 2026-07-15 11:29:25`，`coverageStartedDate 2017-01-01`、`coverageEndedDate 2027-12-31`。
- **欄位名易寫錯**：陣列在 `result.distribution[]`，欄位是 `resourceDescription` / `resourceFormat` / `resourceDownloadUrl`（**不是** `resources[]` 的 `description`/`format`/`url`）。CSV 實體網址是 `www.dgpa.gov.tw/FileConversion?...` 底下的 opaque GUID，**必須從目錄 JSON 解析，不可寫死**。
- CSV schema：`西元日期,星期,是否放假,備註`，每年 365 列。`是否放假`：`2`=放假、`0`=上班。`備註` 空白代表純週末。2026 年共 120 個放假日、22 列具名假日，與官方逐字相符（含 `02-15 小年夜`、`02-16 農曆除夕`、`09-28 孔子誕辰紀念日/教師節`、`10-25 臺灣光復暨金門古寧頭大捷紀念日`、`12-25 行憲紀念日`），春節連假 02-14→02-22 共 9 天。
- **編碼要嗅探，且不可依年份判斷**：115/116 年為 UTF-8 with BOM（2027 檔名結尾即 `_utf8bom.csv`），114 年原始檔為 UTF-8 BOM 而**同年的 (1141020更新) 修正檔卻是 cp950**。順序 `utf-8-sig → utf-8 → cp950`。
- **政府會回頭改已公告的日曆**：diff 114年原始檔 vs (1141020更新) 有三天由上班翻成放假（2025-09-29 補假、2025-10-24 補假、2025-12-25 行憲紀念日）。一次性匯入會把 2025 聖誕節顯示成上班日。所以必須是「排程重抓 + diff」，不是 one-shot import。

**🇯🇵 内閣府 syukujitsu.csv — 權威**
- **唯一可用網址是 `https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv`**（HTTP 200、21,538 bytes、`text/csv`）。常被引用的 `https://www.cao.go.jp/syukujitsu.csv` **是 404**（回傳内閣府 HTML 錯誤頁）。若把後者寫成 fallback，只會在主來源已經壞掉時才被觸發，變成無聲雙重失效。
- 編碼 **Shift_JIS + CRLF**，表頭 `国民の祝日・休日月日,国民の祝日・休日名称`，日期不補零（`2026/5/6`），1,067 列，涵蓋 1955 → **2027-11-23**（日本 12 月已無假日）。
- 2026 年 18 列，**含 `2026/5/6,休日`（振替休日）與 `2026/9/22,休日`（国民の休日）**——這兩天正是黃金週從 4 天變 5 天、白銀週成立的關鍵。所有泛用 API 都漏掉其中至少一天。
- 前瞻上限：`gaiyou.html` 明載「令和10年（2028年）の国民の祝日は、前年（令和9年（2027年））の２月に掲載します」。所以 2026-12 起，12 個月機票視窗會頂到 2027-02 才補上的日本資料——這是本資料集唯一的硬期限。

**🇰🇷 관공서의 공휴일에 관한 규정（대통령령 제36290호，공포 2026-04-30）— 條文已讀，規則可直接列舉**
- 제3조제1항 第1款：국경일 與 부처님오신날・노동절・어린이날・기독탄신일 逢**星期六或星期日**給대체공휴일。第2款：**설날・추석 연휴只在逢星期日時**才給。第3款：兩個公휴일 撞在同一非週末日時另給一天。
- 因此 **추석 2026（週四 9/24–週六 9/26）沒有대체공휴일**，현충일 6/6（週六，제8호，不在第1款清單內）也沒有。任何「韓國週六重疊也補假」的說法是錯的，照做會在韓國全年最貴的一週憑空發明 2026-09-28 這個假日。
- 2026 新增為公휴일 的 제헌절 7/17 與 노동절 5/1 已由 법률 제21338호、제21543호 修正確立。

### 三個不可以進來的來源（licence，不是資料品質）

- **Nager.Date：整條刪掉，連 KR stopgap 與 JP/KR fallback 都不行。** `https://nagerholidays.com/legal/termsofservice`（HTTP 200，Last Updated 2023-09-15）逐字寫著 "The Web API can be used for private or non-profit projects. For commercial purposes we require active sponsorship."。mokaair 有 Travelpayouts 聯盟收入，是商業產品。「自架 MIT Docker image」不是出路：Docker Hub `nager/nager-date` 說明 `LICENSE_KEY ... Required: Yes`，NuGet 亦同，金鑰來自 GitHub Sponsors。原始碼 MIT 不等於發你金鑰。（順帶：它本來就沒有台灣——`/api/v3/PublicHolidays/2026/TW` 回 **HTTP 204 空 body**，TW 不在 `/AvailableCountries`，官方 coverage 頁把 Taiwan 列在 Asia 的 "Missing"，issue #657 自 2024-07-04 開著。）
- **Calendarific：不列為 fallback。** ToS §4.3(c) 規定 API 資料快取不得超過 30 天，到期必須刪除或重新請求；§4.2(e) 禁止再散布。本任務的兩種可能架構（資料表、或進版控的 JSON）都直接違反。免費層另有 500 calls/月、單一語言、要求顯名。
- **caldays：資料本身就錯，且鎖死 2026。** `/api/holidays/tw?year=2027` 回 HTTP 200 但 payload `"year": 2026`——**無聲**降級。台灣只有 13 列（官方 22 列），缺 09-28、10-25、12-25 與全部 6 個補假，並把清明節放在 04-06（官方 04-05 清明節 + 04-06 補假）。
- **Festivo：`/v2/holidays` 已 HTTP 410 Gone，免費 1,000 calls/day 是 "Developer Sandbox" 且明載 no commercial integrations，最低可商用方案 $34.90/月，台灣涵蓋未驗證。**

### 落地位置（本任務只做最小可見面）

`apps/api/app/crawlers/fx.py` 是最接近的先例（無金鑰、多來源、非 provider row），但它連 fx 都還做了 runtime 抓取；本任務連那都不需要。UI 端 `apps/web/components/date-range-picker.tsx:42` 的 `monthGrid` 已經逐格 render，`cellClass`（`:15`）已有 `data-range` / `aria-current` 的 per-cell class 系統，加一顆假日圓點是收斂的改動。五語系名稱沒有任何來源提供（DGPA 只有 zh-TW、内閣府只有 ja、KASI 只有 ko），必須比照 `apps/api/app/weather/met_norway.py:30` 的 `_FAMILIES` 手寫，這也是「委任 JSON 而非 runtime provider」的第二個理由：名稱本來就要人工寫。

## Definition of done

- [ ] `GET /api/v1/holidays?country=TW&from=2026-09-01&to=2027-12-31&locale=zh-TW` 回傳台日韓各自 2026 與 2027 的完整假日列，每列帶 `date`、`kind`、`name`（依 locale）、`is_working_day`；不需登入、不打任何外部網路。
- [ ] 台灣 2026 回傳的 22 列具名假日與 DGPA 官方逐字相同（含 02-15 小年夜、09-28 教師節、10-25 光復節、12-25 行憲紀念日與 6 個補假）；日本 2026 回傳 18 列，含 2026-05-06 與 2026-09-22；韓國 2026 回傳 22 個放假日，且 2026-09-28 **不是**假日。
- [ ] 五個語系（zh-TW / zh-CN / en / ja / ko）都拿得到該假日的名稱，沒有任何一列 fallback 成空字串或英文代碼。
- [ ] 補班日是可前瞻的一級資料：`is_working_day=false` 的週六不會被當成假日，而 `kind=makeup_workday` 的週六即使 2026/2027 目前為零筆，schema 與查詢仍支援未來出現的補班日。
- [ ] `/trips/new` 月曆的每一格：落在假日的日子有可辨識的標記，且該格 `aria-label` 讀得到假日名稱；沒有假日資料的日子外觀與行為完全不變。
- [ ] `refresh-holidays` CLI 預設只印 diff 不寫檔；加 `--apply` 才更新 `apps/api/app/holidays/data/*.json`，重跑同一年不產生 diff。CLI 只會更新日期與旗標，**不會覆寫人工翻譯的 `names`**，遇到沒有翻譯的新 key 會列出來要人補。
- [ ] `docs/public-holidays.md` 存在，內含每個來源的 API contract、授權條款與逐字顯名字串、更新節奏與前瞻上限，並寫明哪些來源因授權被排除。
- [ ] 三段顯名字串出現在產品可見處（沿用既有 attribution 慣例，如 `apps/web/components/hotel-offer-card.tsx:117`）。

## Steps

- [ ] 新增 `apps/api/app/holidays/__init__.py` 與 `apps/api/app/holidays/data/{tw,jp,kr}_{2026,2027}.json`。每列 `{"date": "2026-05-06", "key": "jp_kenpo_kinenbi_substitute", "kind": "substitute", "is_working_day": false, "names": {"zh-TW": ..., "zh-CN": ..., "en": ..., "ja": ..., "ko": ...}, "source": "cao_go_jp"}`。`kind` 取值：`public_holiday` / `substitute` / `makeup_workday` / `bridge_holiday`。`names` 全部人工撰寫，比照 `apps/api/app/weather/met_norway.py:30` 的 `_FAMILIES`。
- [ ] 新增 `apps/api/app/holidays/service.py`：純記憶體查詢，開機時載入 JSON。提供 `holidays_between(country, start, end, locale)` 與 `is_working_day(country, date)`。日期一律 ISO `YYYY-MM-DD` 字串比較，不建 `date` 物件、不碰時區（比照 `apps/web/lib/calendar.ts` 的既有作法）。國碼沿用 `apps/api/app/foods/service.py:91` 的 `destination_country_code()`，不要再造第二套國別對應。
- [ ] 新增 `apps/api/app/holidays/router.py`：`GET /holidays`，公開、不需 `CurrentUser`（與 `apps/api/app/fx/router.py:25` 不同，因為這是靜態資料），回應加長效 `Cache-Control`。在 `apps/api/app/main.py:90` 附近 `app.include_router(holidays_router, prefix="/api/v1")`。
- [ ] 新增 `apps/api/app/holidays/refresh.py`：TW 先 `GET https://data.gov.tw/api/v2/rest/dataset/14718`，從 `result.distribution[]` 依 `resourceDescription` 找當年檔、取 `resourceDownloadUrl`，依 `utf-8-sig → utf-8 → cp950` 順序嗅探解碼，`是否放假==2` 為放假、`備註` 非空為具名假日、`備註=='補假'` → `substitute`、`備註=='補行上班'` 且 `是否放假==0` → `makeup_workday`。JP 抓 `https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv`（Shift_JIS、CRLF、日期不補零），名稱為 `休日` 的列依前後文標成 `substitute` 或 `bridge_holiday`。KR 不抓網路，由人工依 관공서의 공휴일에 관한 규정 제2조/제3조 撰寫並在每列 `note` 註明依據款次。
- [ ] 在 `apps/api/app/cli.py` 新增 `refresh-holidays` subparser（比照 `:642` 的 `fill-hotspot-labels`，含 `--country`、`--year`、`--apply`）與 `:815` 附近的 dispatch。預設 dry-run 印出「新增 / 消失 / 放假旗標翻轉 / 缺翻譯」四類 diff。
- [ ] 新增 `apps/api/tests/test_public_holidays.py`：以 `httpx.MockTransport` 餵 DGPA 與内閣府的真實片段（含 cp950 與 Shift_JIS bytes、含 `20250208,六,0,補行上班`），斷言解析結果；以 `ASGITransport(app=app)` 打 `/api/v1/holidays` 斷言上面 Definition of done 列出的三國實際日期；另加一條斷言 `2026-09-28` 不在 KR 結果中。
- [ ] 新增 `apps/web/lib/holidays.ts`：呼叫既有 catch-all proxy `apps/web/app/api/travel/[...path]/route.ts`（不需新增 BFF route），回傳 `Record<string, {kind, name}>`。
- [ ] 改 `apps/web/components/date-range-picker.tsx`：以可見月份區間查一次，於 `:120` 的 button 加上 `data-holiday` 與併入假日名稱的 `aria-label`，並在 `cellClass`（`:15`）加對應的圓點樣式。**不得新增任何中文字面量**——`tools/check-i18n.mjs` 會擋掉 `apps/web/{app,components,lib}/**/*.tsx` 新增的漢字串；名稱一律是 API 回傳的變數。
- [ ] 寫 `docs/public-holidays.md`：比照 `docs/hotspot-intelligence.md:7-13` 的來源政策表格，一列一個來源（含被排除的 Nager / Calendarific / caldays / Festivo 與排除理由），並逐字寫下三段顯名字串與各來源的前瞻上限。

## How to verify

```bash
cd apps/api && ./.venv/Scripts/python.exe -m pytest tests/test_public_holidays.py -q
cd apps/api && uv run ruff check . && uv run mypy app
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
npm run check:tasks
```

抓取器要對真實來源跑一次（**必須在真正的 VPS/容器內跑，不要只在 Windows 開發機**，見 Notes 的 TLS 註記）：

```bash
cd apps/api && ./.venv/Scripts/python.exe -m app.cli refresh-holidays --country tw --year 2026
cd apps/api && ./.venv/Scripts/python.exe -m app.cli refresh-holidays --country jp --year 2026
# 兩者都應印出「無差異」，因為進版控的 JSON 就是從同一份檔案產生的
```

端點：

```bash
curl -s 'http://localhost:8000/api/v1/holidays?country=JP&from=2026-05-01&to=2026-05-10&locale=zh-TW'
# 必須同時看到 2026-05-03、2026-05-04、2026-05-05 與 2026-05-06
curl -s 'http://localhost:8000/api/v1/holidays?country=KR&from=2026-09-20&to=2026-09-30&locale=ko'
# 必須看到 09-24/25/26，且 09-28 不在結果中
curl -s 'http://localhost:8000/api/v1/holidays?country=TW&from=2026-02-01&to=2026-03-01&locale=zh-TW'
# 必須看到 02-15 小年夜 到 02-20 補假，共 9 天連假
```

手動：開 `/zh-TW/trips/new`，把月曆翻到 2026-02 與 2026-05，確認春節與黃金週整段被標記；翻到 2026-09，確認 09-22 在日本被標記、09-28 在韓國**沒有**被標記。

## Notes

### 授權立場（已定，不要重新討論）

- **TW／DGPA**：政府資料開放授權條款第 1 版（目錄 API 回傳 `license: "1"`）。允許商業利用與改作，但顯名義務很硬：`https://data.gov.tw/license` 要求載明提供機關、年份、資料集名稱與版本、釋出聲明，並連結授權條款頁；未依規定顯名者「視為自始未取得開放資料之授權」（追溯失效）。因此 `docs/public-holidays.md` 與產品可見處要放的是**逐字字串**，不是一句「需要標示來源」。
- **JP／内閣府**：`https://www.cao.go.jp/notice/rule.html` 載明 cao.go.jp 內容適用 **公共データ利用規約（第1.0版）PDL 1.0**（與 CC BY 4.0 相容，可商用、可改作），要求 `出典：内閣府ウェブサイト（URL）、PDL1.0（規約原文ページのURL）` 形式的出典表記，改作時須註明已改作。**下一個人要讀的頁面**：`https://www.cao.go.jp/notice/rule.html`，把 PDL 1.0 規約原文頁的正確網址抄進 docs（本次未逐字確認該原文頁 URL）。
- **KR**：資料為人工依法令條文撰寫，法令本身不受著作權保護，無顯名義務。
- **holidays-jp**：只能**一年抓一次進版控**，**絕對不可在 runtime 呼叫**。兩個理由：(1) GitHub Pages 服務條款不允許把 Pages 當成營利網站的免費 hosting，而流量算在維護者個人帳號上；(2) 它自述資料由 Google Calendar 自動生成，**不是内閣府衍生物**，所以拿它的資料就不能主張内閣府的 PDL 出典。定位只有一個：CI 交叉檢查。它的 2026 檔與内閣府 18 列完全一致，且把 `休日` 明確標成 `憲法記念日 振替休日` 與 `国民の休日`，比政府檔更好讀，適合當測試 fixture。
- **ruyut/TaiwanCalendar**：`/repos/ruyut/TaiwanCalendar/license` 回 404，倉庫沒有任何 LICENSE 檔——**無授權即保留所有權利**，不可 vendored。（若看到別處寫它是 CC BY 4.0，那是錯的。）只能當一次性 spike 的對照。

### 額度與可用性

- DGPA 與内閣府都是靜態檔、無金鑰、無額度。一年抓數次。
- **DGPA 的 TLS 憑證鏈在嚴格驗證下會失敗**：curl 接受（`ssl_verify_result=0`），但 Python 3.14 / OpenSSL 3.5.7 會噴 `SSLCertVerificationError: Missing Subject Key Identifier`（缺陷在中繼鏈，不在 leaf）。倉庫用 httpx，所以**在真正的容器映像裡先證明抓得到再往下寫**，不要在 Windows 開發機驗完就收工。若容器也失敗，先把它記進 docs 並改為人工下載 + `--apply`，不要放寬憑證驗證。
- `holidays-jp` 的 2028 檔案會回 HTTP 200，但内閣府只到 2027；2028 的春分／秋分是天文推算，日本每年 2 月才正式公告。**2027 之後的任何資料都要標為暫定或直接不收**。

### 仍為 UNVERIFIED 的事項

- **KASI（한국천문연구원 특일 정보，data.go.kr `publicDataPk=15012690`）本次刻意不進範圍。** base path `https://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService` 是活的（未帶金鑰回 401 `SERVICE_KEY_IS_NULL`），授權為「이용허락범위 제한 없음」、免費、개발/운영 皆 자동승인、개발계정 10,000 calls/day（此數字以核准畫面為準，入口網一般指南另有較低描述）。**但整個 KR adapter 所依賴的 operation 名稱沒有任何一手來源可證**：同一批探測中 `getAnniversaryInfo` 回 401（存在），`getNationalHolidayInfo` 回 400 `NO_OPENAPI_SERVICE_ERROR`（不存在或已廢止），而 `getRestDeInfo` 因 TLS 握手失敗無法確認。**下一個人要讀的頁面**：`https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15012690`，並在申請到金鑰後**從 VPS**逐一呼叫候選 operation，保留回 401 而非 400 的那個。另注意該 API 規格 `수정일` 停在 2023-03-29，需確認它是否已含 2026 新增的 제헌절 與 노동절。
- **`apis.data.go.kr` 的節流發生在 TLS 層而非 HTTP 429**：約十餘次探測後同一來源 IP 被鎖住整個 session，TCP 443 連得上但握手 timeout，client 端只看得到連線錯誤、沒有 status code 可分支。天真的重試迴圈會把 VPS 的 IP 打進黑洞而毫無跡象。這是把 KR 排除在第一版之外的實質理由。
- **Calendarific 的實際 payload 未見**（無金鑰）。已知其台灣資料**不是過期的**——公開頁面 2026 台灣列有 09-28 教師節、10-25 光復節與 10-26 補假、12-25 行憲紀念日、05-01 勞動節；它真正的問題是**過度收錄**（53 列 vs 官方 22 列，混入元宵、土地公生、復活節、萬聖節），需要靠 `type`/`primary_type` 過濾。這點記在這裡只是為了不讓下一個人以「它資料太舊」為由重新評估——真正擋住它的是 30 天快取上限，那條無解。

### 兩個容易寫反的規則（照做，不要憑直覺）

1. **補行上班沒有被廢除。** 《紀念日及節日實施條例》第 8 條現行條文仍載「調整放假及補行上班日期，除其他法令另有規定者外，由目的事業主管機關調移並公告之」。只是 115／116 年公告的日曆**碰巧**零筆補班（114 年有一筆 `20250208,六,0,補行上班`）。`makeup_workday` 必須是前瞻性的一級 kind；若把它當成「歷史資料才有」，未來第一個補班星期六就會在月曆上被畫成空閒日——而那正是台灣資料唯一的價值所在。另：同條例第 6 條有條件規則「兒童節與清明節同一日時，於前一日放假。但逢星期四時，於後一日放假」，抓取器不需實作，但 diff 出現位移時不要當成錯誤。
2. **連假長度要用聯集算，不要用加總。** 連假 = {週末 ∪ 假日} − {補班日}。把「假日數」加到「週末數」上，就會在假日本來就落在週末時重複計算——韓國 2026 的 3·1절（週日）、광복절（週六）、개천절（週六）全踩這個坑。

### 刻意排除的下游消費者（各自另開任務）

`apps/api/app/ai/itinerary.py`（被 `2026-09-06-opening-hours-aware-scheduling` 與 `2026-09-06-paste-inbox-into-candidates` 兩支 P2 佔用）、`apps/web/components/day-health-strip.tsx`（同上）、`apps/api/app/search/orchestrator.py:355` 的 `FlightDateOption`、`apps/api/app/alerts/**`、`apps/web/components/trip-editor.tsx`。本任務只出**資料源**與一個最小可見面，避免卡住兩支 P2。

值得優先接上的是營業時間那支：日本週一休館的美術館在**祝日的週一會開門、改成隔天週二休（振替休館）**，所以那支任務目前的規格在假日的週一上是錯的，而它自己的硬規則是「一個誤標會毀掉整條 strip 的信任」。順序應為：假日資料先落地，營業時間後接。

### 明確不做

不做人潮或價格**預測**。彈性日期 chip 上已經有供應商的實際報價，那個數字本身就含了假日溢價；badge 只能陳述事實（「5/4 みどりの日」），不能講「這天會比較貴」——兩個會互相打架的聲音同時出現，正是 day-health strip 當初決定「寧可沉默」要避免的失敗。也不做假日審核佇列：這份資料不是 per-place，走 PR diff 審就夠。

### 這條授權標準不是新發明的

2026-09-06 選旅程天氣來源時，**Open-Meteo 就是因為免費方案僅限非商業用途而被否決**，改用
MET Norway（CC BY 4.0，條款要求可識別的 User-Agent）。mokaair 有 Travelpayouts 聯盟收入與付費
點數，是商業產品，所以「個人專案免費、商業要贊助」的來源一律不能用——Nager.Date 被排除的理由
與當時完全相同，不是新標準。同一輪還接了 Currency-api 當匯率來源。
