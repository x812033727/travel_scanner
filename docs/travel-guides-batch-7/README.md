# 旅遊情報攻略第七批：二十篇規格與撰稿指令

第七批的二十篇 zh-TW 旅遊文章，一篇一個規格檔。這份 README 有三部分：清單、給撰稿者的通用規則、給協調者的收件步驟。
任務票是 `tasks/open/2026-09-14-plan-articles-batch-7.md`（規劃）；撰稿與上線另開票，見文末。

規格在 2026-09-16 定稿，流程如下：
- 六個區域（泰國、東北日本、韓國、越南、港澳星、跨區）各一個研究代理提出 24 個候選，逐一在官方頁核對核心數字，curl 與 WebFetch 各試一次，讀到的數字逐字記進 `research-<region>.md`（規劃工作區，不進 repo）。核心數字有一半以上讀不到就淘汰。
- 選出 20 篇，一篇一個規格代理：打開最接近的既有文章正文、研究檔與官方頁，照第六批的格式寫規格。
- 三輪一致性審查：連結與時效、區塊規則、事實與口徑。審查結果直接改進規格。

淘汰或延後的題目：大叻三天（12 個核心數字讀不到 8 個，留給第八批；越南國內交通篇放一段「大叻怎麼去」）、颱風季航班改退（長榮與虎航的政策頁讀不到）、香港迪士尼 vs 海洋公園（第二次淘汰，迪士尼票價頁只進得了排隊室）、釜山／香港／新加坡住哪（官方的區域描述讀不到，與既有文章重疊大）、藏王樹冰與銀山溫泉冬季文（等 11 月各度假村公布日期）。

## 清單

| # | 規格 | kind | destination_id | topics | display_order | valid_until |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [lunar-new-year-2027-asia-travel](lunar-new-year-2027-asia-travel.md) | intel | null | season, culture | 1010 | 2027-02-20 |
| 2 | [japan-golden-week-2027](japan-golden-week-2027.md) | intel | null | season, transport | 1020 | 2027-05-10 |
| 3 | [krabi-airport-transport-where-to-stay](krabi-airport-transport-where-to-stay.md) | howto | krabi | transport, hotel, beach | 1030 | |
| 4 | [krabi-ao-nang-railay-4-islands](krabi-ao-nang-railay-4-islands.md) | howto | krabi | itinerary, beach, nature | 1040 | |
| 5 | [phuket-phi-phi-james-bond-island-hopping](phuket-phi-phi-james-bond-island-hopping.md) | howto | phuket | itinerary, beach, nature | 1050 | |
| 6 | [chiang-rai-2-day-itinerary](chiang-rai-2-day-itinerary.md) | howto | chiang-rai | itinerary, culture, transport | 1060 | |
| 7 | [bangkok-where-to-stay](bangkok-where-to-stay.md) | howto | bangkok | hotel, budget, transport | 1070 | |
| 8 | [southeast-asia-seasons-when-to-go](southeast-asia-seasons-when-to-go.md) | howto | null | season, budget | 1080 | |
| 9 | [sendai-airport-access-loople-bus-guide](sendai-airport-access-loople-bus-guide.md) | howto | sendai | transport, budget | 1090 | |
| 10 | [sendai-matsushima-2-day-itinerary](sendai-matsushima-2-day-itinerary.md) | howto | sendai | itinerary, culture, transport | 1100 | |
| 11 | [yamadera-day-trip-from-sendai](yamadera-day-trip-from-sendai.md) | howto | sendai | itinerary, culture, nature | 1110 | |
| 12 | [zao-fox-village-from-sendai](zao-fox-village-from-sendai.md) | howto | sendai | itinerary, nature, family | 1120 | |
| 13 | [daegu-airport-ktx-subway-guide](daegu-airport-ktx-subway-guide.md) | howto | daegu | transport, budget | 1130 | |
| 14 | [daegu-2-day-itinerary](daegu-2-day-itinerary.md) | howto | daegu | itinerary, culture, food | 1140 | |
| 15 | [jeonju-hanok-village-day-trip-from-seoul](jeonju-hanok-village-day-trip-from-seoul.md) | howto | seoul | itinerary, culture, food | 1150 | |
| 16 | [ha-long-bay-cruise-from-hanoi](ha-long-bay-cruise-from-hanoi.md) | howto | hanoi | itinerary, nature, transport | 1160 | |
| 17 | [hue-day-trip-from-da-nang](hue-day-trip-from-da-nang.md) | howto | da-nang | itinerary, culture, transport | 1170 | |
| 18 | [vietnam-domestic-flights-train-guide](vietnam-domestic-flights-train-guide.md) | howto | null | transport, budget | 1180 | |
| 19 | [macau-day-trip-from-hong-kong](macau-day-trip-from-hong-kong.md) | howto | hong-kong | itinerary, culture, transport | 1190 | |
| 20 | [sentosa-day-guide](sentosa-day-guide.md) | howto | singapore | itinerary, family, beach | 1200 | |

除了藏王狐狸村 `featured: false`，其餘 19 篇都是 `featured: true`。

歸屬原則：從基地城市出發的一日遊掛基地城市（全州掛 `seoul`、順化掛 `da-nang`、下龍灣掛 `hanoi`、澳門掛 `hong-kong`；前例是鎌倉、橫濱掛 `tokyo`，慶州掛 `busan`）。有自己機場、住在當地的掛自己。
這批補上了目錄裡原本 0 篇的喀比（primary）、仙台、大邱、清萊；全州與順化以一日遊的形式進站。目錄裡仍是 0 篇的只剩大叻，留給第八批。

## 給撰稿者：通用規則

讀者是台灣旅客。語氣像懂行、講話直接的朋友，每段都要有能照做的資訊，不寫「總之」「相信大家」「讓我們」。

每篇規格裡已經寫好這些事：
- summary 那 2 到 5 句講什麼、段落順序、每段寫什麼
- 要查的官方來源，以及規劃時讀到的數字
- offer 放哪裡
- 站內連結放哪一段，以及 `related` 要列哪四篇
- 圖解畫什麼
- 容易寫錯的事實

規格與這份 README 衝突時，以規格為準。第六批的 [README](../travel-guides-batch-6/README.md) 與 [ERRATA](../travel-guides-batch-6/ERRATA.md) 仍然適用；下面只寫本批不同或要特別提醒的地方。

### 本批與第六批不同的地方

1. **summary 區塊是第一個區塊。** `{"type": "summary", "items": [...]}`，2 到 5 句、每句 ≤300 字：第一句是答案（要做什麼、選哪個），其餘是決定條件、文章給的數字與一個注意事項。只重述正文有的事實，數字逐字照正文；不寫「本文介紹」這種後設句，不逐字重複 description。第二個區塊才是開頭 paragraph。
2. **站內文章連結用 article inline，不用 link 區塊。** 寫成
   `{"type": "rich_paragraph", "inlines": [{"type": "text", "text": "…"}, {"type": "article", "text": "連結文字", "kind": "howto", "slug": "…"}, {"type": "text", "text": "。"}]}`，
   `kind` 填對方的 kind。城市頁與美食目錄仍用 `link` 區塊：`https://mokaair.com/zh-TW/destinations/<id>`、`https://mokaair.com/zh-TW/foods?destination_id=<id>`（`?city=` 目前被忽略，票 `2026-09-14-food-links-city-param-ignored` 修好前一律用 `destination_id`）。
3. **`related` 與 `aliases`。** `pack.json` 的 `related` 最多 4 個 slug，照規格列；`aliases` 是 zh-TW 別名（喀比的「甲米」、大叻的「達叻」這類讀者真的會搜的），沒有就留空物件。
4. **表格以 4 欄為上限設計。** 渲染器 2026-09-14 已修好（每欄至少 7rem，寬表在表格內橫向捲），5 到 6 欄不會再擠爛，但讀者要橫捲；規格寫 4 欄就寫 4 欄。
5. **FAQ 區塊可選。** 只有規格列了 `faq` 的篇章才放；答案是純文字，2 到 10 組。
6. **時效規則不變。** howto 不連 valid_until 在 2027-06-30 之前的 intel；規格點名的季節段例外，刪除日 = 該 intel 的 valid_until 隔天，連結前那句話要寫成拿掉連結後仍讀得通。

### 工作區與檢查指令

用 repo 的內容包工具（`app/guides/pack_cli.py`）。每篇一個目錄 `<workdir>/<slug>/`：

| 檔案 | 內容 |
| --- | --- |
| `pack.json` | 內容包，**先寫這個**；寫完就存 |
| `diagram-1.svg` | 自繪圖解；第二張叫 `diagram-2.svg`，文章裡要真的放 |
| `images.json` | Commons 照片：`{"hero": {"title": "File:…"}, "photos": {"photo-1": {"title": "File:…"}}}` |
| `notes.md` | 查證記錄，一行一條：`主張｜來源網址｜查證日` |

旅遊文章的 hero 用 Commons 實景照片，不畫 `hero.svg`。

驗證只能加 `--dry-run`，這個模式什麼都不寫：

```bash
cd apps/api
uv run python -m app.guides.pack_cli ingest --from <workdir> --slug <slug> --dry-run
```

圖解要自己渲染成 PNG，用 Read 打開看版面。機械檢查看不到文字疊字、壓線、超出方框。渲染指令與 Windows 的 `CHROMIUM_BIN` 寫法見第六批 README。

只在工作區寫檔，不改 repo 裡的檔案、不跑 git，不用共用的瀏覽器分頁。撰稿的 session 可能中途被切斷：落在磁碟上的檔案會留下來，結尾的報告不會。

**不要把任何個人資料送出去。** 用 curl 或腳本呼叫 Commons 等外部網站時，User-Agent 一律寫 repo 工具用的 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，不要放使用者或自己的 email、姓名。

### `pack.json`

```json
{
  "slug": "<slug>",
  "kind": "howto",
  "destination_id": "krabi",
  "topics": ["transport", "hotel", "beach"],
  "featured": true,
  "display_order": 1030,
  "valid_until": null,
  "aliases": {"zh-TW": ["甲米"]},
  "related": ["krabi-ao-nang-railay-4-islands", "phuket-airport-transport-where-to-stay"],
  "locales": {
    "zh-TW": {
      "title": "…",
      "description": "≤500 字，一句話講清楚解決什麼問題，寫查證年月",
      "hero": { "src": "/guides/<slug>/hero.jpg", "alt": "描述照片內容", "width": 1, "height": 1 },
      "blocks": [
        { "type": "summary", "items": ["…", "…"] },
        { "type": "paragraph", "text": "…" }
      ],
      "sources": [ { "title": "網站名：頁名（查了什麼）", "url": "https://…", "checked_on": "2026-09-2x" } ]
    }
  }
}
```

slug、kind、destination_id、topics、featured、display_order、valid_until、related 照清單與規格抄。照片的 `width`、`height` 先填 1，`credit` 不要填，工具會從 Commons API 讀回來覆寫。

區塊只能用：heading（level 2 或 3）、paragraph、rich_paragraph（含 text／link／article inline）、list、link（只放站內網址）、image、table（最多 6 欄、30 列，每格 ≤300 字）、callout（tip／warning／info）、offer（flight／hotel／activities／transport／connectivity）、summary、faq。全部純文字：不能有 HTML、Markdown、emoji，`<` 後面不能直接接字母，也不能有 `&amp;` 這類實體。

結構：summary 在最前面，接開頭 paragraph，不下「前言」標題。至少 3 個 level 2 標題、1 張表格、1 個 callout、1 張自繪圖解，內文照片 1 到 2 張。字數（正文，含 summary 與 FAQ，不含 sources）：howto 1,800 到 3,000 字，intel 800 到 1,500 字。

### 事實查核

- 票價、時刻、營運時間、規定都要用 WebFetch 或 curl 讀官方頁確認才寫，文中寫「2026 年 X 月查證」。**查不到官方確認的數字就不寫數字**，改寫「以官網為準」。WebSearch 每篇最多 5 次。
- 規格裡的數字是規劃當天（2026-09-16）讀到的，撰稿時要再打開一次核對；官方頁改了就照新的寫，並在 `notes.md` 記下。
- 法規類的事實回到主管機關的頁面或法規原文；媒體轉述不當定論。
- 幣別用當地幣別：日圓、韓元、港元、澳門元、新加坡幣、越南盾、泰銖。日期寫完整。
- 規劃時這台機器讀不到、或讀到的內容不能直接用的站，規格裡都已寫了替代來源或「以官網為準」：
  - 泰國：喀比機場（DOA 的三個網域）、transport.co.th、Greenbus、BEM 的 MRT 首末班（Incapsula）、nps.dnp.go.th、watrongkhun.org、doitung.org、thawan-duchanee.com、singhapark.com、chiangraicity.go.th、tourismthailand.org（含 thai.）、air4thai、pcd.go.th、tmd.go.th。portal.dnp.go.th 只有 WebFetch 讀得到；news.dnp.go.th 下午常回 503。泰國的季節月份用泰國觀光局東京辦事處的天氣頁 thailandtravel.or.jp/about/weather/，它有 8 個地區乘 12 個月的官方月份表，比各城市頁完整。
  - 日本：jreast.co.jp、jr-odekake.net、jr-central.co.jp 都 403，但 JR 東海的訂票網站 smart-ex.jp 讀得到（トピックス頁有黃金週、盂蘭盆節、年末年始三大尖峰期 のぞみ 全席指定席的通則）。內閣府祝日頁除了網頁還有 syukujitsu.csv 可以直接讀；法令用 e-Gov 的 API。仙台空港鉄道的真正網域是 senat.co.jp；city.sendai.jp 只有 WebFetch 讀得到；zao-fox-village.com 只有 http。
  - 韓國：korail.com（letskorail 轉過去後只剩載入頁）、kobus.co.kr、twayair.com、donghwasa.net 讀不到；korea.kr 用 curl 讀不到，改讀發布機關 kasa.go.kr；tour.daegu.go.kr 只能 curl；dtro.or.kr 要帶 cookie；tour.jeonju.go.kr 的 /eng/ 深層頁用 WebFetch 讀得到。
  - 越南：futabus.vn 全站 403；dalat.gov.vn、thuathienhue.gov.vn、acv.vn 讀不到；hueworldheritage.org.vn 主站讀不到但 eticket 子站的 API 讀得到；halongbay.com.vn 首頁不穩、文章頁讀得到；dsvn.vn 的時刻票價要用 giotaugiave.dsvn.vn 的表單；vietjetair.com 只有 WebFetch 讀得到；chinhphu.vn 只有 WebFetch 讀得到。
  - 港澳星：discoverhongkong.com 403、港鐵 customer 頁維護中、迪士尼票務頁是排隊室、環球影城票價讀不到；TurboJET 用 WebFetch 回 503，要用 curl；海洋公園票價頁 curl 可讀、開放時間讀不到。
  - 航空：evaair.com 全站 403、tigerairtw.com 是 SPA 殼；華航、星宇（latestnews 子網域）讀得到。
- **過了機械檢查的草稿，不等於查證過的文章。** 第五批與第六批交給獨立查核者後，每篇平均改掉 10 處以上。

### 分潤區塊（offer）

規則同第六批：每篇最多 3 個，不放在第一個 level 2 標題之前，不相鄰；位置與 module 照規格；跨城市文章（destination_id 是 null）的 offer 要填 destination_id；heading 用通用說法；entry、packing、shopping、etiquette、safety、food、budget 主題原則上不放。哪些城市已核准合作方案以後台為準，區塊照放。

### 站內連結

- 只連兩種文章：main 上已存在、而且有 zh-TW 版本的文章，以及這批 20 篇。台灣那二十篇沒有 zh-TW 版，不能連。文章連結用 article inline（見上），城市頁與美食目錄用 link 區塊。
- 本批互連（喀比兩篇與普吉篇、喀比跳島與普吉跳島、河內與下龍灣、峴港與順化、清邁與清萊、KTX 篇與大邱／全州、香港篇與澳門、連假篇與農曆新年篇、黃金週篇）都寫在各規格裡；兩篇對同一件事的說法必須一字不差（皮皮島門票、瑪雅灣封閉期、韓國설날 2 月 7 日、台灣春節 2 月 4 日到 10 日）。
- **地名以目的地目錄為準**（`app/destinations/catalog.py`、`app/hotspots/areas.py`、`app/foods/area_catalog.py`）：Railay 寫「萊雷」不寫「萊利」，Karon 寫「卡隆」不寫「卡倫」。目錄以外的常見寫法放進 `aliases`，不寫進正文。
- **農曆新年篇 2027-02-20 就到期**，比連它的黃金週篇（2027-05-10）與連假篇（2027-12-31）都早。連它的那兩篇要在 2027-02-21 同時拿掉連結與 `related` 裡的它，連結前那句話要寫成拿掉連結後仍讀得通。

### 照片

同第六批：只用 Wikimedia Commons，授權限 CC0、Public domain、CC BY、CC BY-SA；每個候選都要打開檔案頁確認；hero 橫幅、寬 ≥1600 px、壓到 200 KB 以下；同一張照片不能當兩篇的 hero；紙鈔、商標、螢幕截圖、可辨識人臉的照片不用。Commons API 對同一出口的密集請求會回 429，工具會依 Retry-After 退避重試；不要十幾個撰稿代理同時搜 Commons。

### 圖解

同第六批：viewBox `0 0 1600 900`、`role="img"`、`<title>`、`<desc>`、所有 `font-size` ≥15、不外連、右下角 `© Mokaair 製圖 2026`；配色與字型串照 `docs/life-ai-series-brief.md` 第 6 節；韓國主題加 Noto Sans KR、泰國主題加 Noto Sans Thai，港澳星越用預設字型串。**圖上每個數字都要出現在正文**，規格的「圖解」一節已列出可以畫的數字。

## 給協調者：收件步驟

1. 撰稿者交件後，先讀 `notes.md`，抽查三個以上數字是否真的出自官方頁。報告裡的「需要注意」每一條都要追。
2. `ingest --dry-run` 通過、渲染圖看過沒問題之後，才正式 ingest（不加 `--dry-run`）。
3. 工具不檢查的幾件事，要自己檢查：
   - article inline 的 slug 與 kind 是否存在（`uv run python -m app.cli guides-links-check --locale zh-TW` 在上線後跑一次）
   - offer 是否在第一個 h2 之後、是否兩個相鄰
   - 表格是否超過 4 欄
   - summary 的數字是否逐字出現在正文
   - Commons 作者欄位是不是網址或授權說明文字
4. `uv run pytest tests/test_guides_content_pack.py -q`、`uv run python -m app.guides.pack_cli lint --kind howto`、`--kind intel`，然後開 PR。
5. 合併、部署後，在正式站先跑 `guides-import --dry-run`，確認只有這二十篇是 `create`，再跑 `--publish`，然後 `guides-links-rebuild` 與 `guides-links-check`。
6. 每個規格最後一節「上線後與交叉檢查」裡有日期的項目，都在上線 PR 開成票（例如 2027-05-11 刪櫻花情報連結、2028-01-01 刪連假篇連結、越南 Tết 定案後改農曆新年篇、JR 東海公布黃金週全席指定期間後補日期）；反向連結彙整成一張「既有文章補連第七批」的票。
