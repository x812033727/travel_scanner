# 旅遊情報攻略第六批：二十篇規格與撰稿指令

第六批的二十篇 zh-TW 旅遊文章，一篇一個規格檔。這份 README 有三部分：清單、給撰稿者的通用規則、給協調者的收件步驟。
任務票是 `tasks/done/2026-09-14-launch-articles-batch-6-twenty-more.md`。二十篇 2026-09-14 已上線；規格有錯的地方列在 [ERRATA.md](ERRATA.md)，正式內容以 `apps/api/app/guides/content/<slug>.json` 為準。

規格在 2026-09-14 定稿，流程如下：
- 六個分區提出 55 個候選，三位評審打分，選出 20 篇。
- 每篇打開相近的既有文章比對，並實際讀官方頁，確認查得到核心數字。
- 對照 main 上 #468 新增的 15 篇旅遊文與第五批，修掉重疊與口徑衝突，再做三輪一致性審查。

直島因為不在目的地目錄而換掉，改寫越南上網、換錢、叫車（第 17 篇）。

## 清單

| # | 規格 | kind | destination_id | topics | display_order | valid_until |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [taiwan-long-weekends-2027-flight-planning](taiwan-long-weekends-2027-flight-planning.md) | intel | null | season, budget | 810 | 2027-12-31 |
| 2 | [power-bank-flight-rules-2026](power-bank-flight-rules-2026.md) | intel | null | packing, safety | 820 | 2027-01-31 |
| 3 | [japan-cherry-blossom-2027](japan-cherry-blossom-2027.md) | intel | null | season, nature, viewpoint | 830 | 2027-05-10 |
| 4 | [hong-kong-4-day-itinerary](hong-kong-4-day-itinerary.md) | howto | hong-kong | itinerary, viewpoint, culture | 840 | |
| 5 | [return-to-taiwan-customs-duty-free-guide](return-to-taiwan-customs-duty-free-guide.md) | howto | null | entry, shopping | 850 | |
| 6 | [hong-kong-airport-to-city](hong-kong-airport-to-city.md) | howto | hong-kong | transport, budget | 860 | |
| 7 | [singapore-4-day-itinerary](singapore-4-day-itinerary.md) | howto | singapore | itinerary, culture, nature | 870 | |
| 8 | [yokohama-day-trip-from-tokyo](yokohama-day-trip-from-tokyo.md) | howto | tokyo | itinerary, transport, viewpoint | 880 | |
| 9 | [singapore-entry-2026-sg-arrival-card](singapore-entry-2026-sg-arrival-card.md) | intel | singapore | entry | 890 | 2027-03-31 |
| 10 | [singapore-changi-airport-mrt-simplygo-guide](singapore-changi-airport-mrt-simplygo-guide.md) | howto | singapore | transport, budget | 900 | |
| 11 | [dmz-day-trip-from-seoul](dmz-day-trip-from-seoul.md) | howto | seoul | itinerary, culture | 910 | |
| 12 | [suwon-hwaseong-day-trip](suwon-hwaseong-day-trip.md) | howto | seoul | itinerary, culture, transport | 920 | |
| 13 | [hong-kong-entry-2026](hong-kong-entry-2026.md) | intel | hong-kong | entry | 930 | 2027-03-31 |
| 14 | [hanoi-4-day-itinerary](hanoi-4-day-itinerary.md) | howto | hanoi | itinerary, culture, food | 940 | |
| 15 | [taoyuan-airport-departure-guide](taoyuan-airport-departure-guide.md) | howto | null | transport, packing | 950 | |
| 16 | [phuket-airport-transport-where-to-stay](phuket-airport-transport-where-to-stay.md) | howto | phuket | transport, hotel, beach | 960 | |
| 17 | [vietnam-money-sim-grab-guide](vietnam-money-sim-grab-guide.md) | howto | null | connectivity, budget, packing | 970 | |
| 18 | [ho-chi-minh-city-4-day-itinerary](ho-chi-minh-city-4-day-itinerary.md) | howto | ho-chi-minh-city | itinerary, culture, transport | 980 | |
| 19 | [korea-naver-map-kakao-t-guide](korea-naver-map-kakao-t-guide.md) | howto | null | transport, connectivity | 990 | |
| 20 | [kanazawa-2-day-itinerary](kanazawa-2-day-itinerary.md) | howto | kanazawa | itinerary, culture, transport | 1000 | |

除了金澤 `featured: false`，其餘 19 篇都是 `featured: true`。

這批補上了七個目錄裡原本 0 篇的目的地：香港、新加坡、河內、胡志明市、普吉、金澤、橫濱（橫濱掛 `tokyo`，理由同鎌倉）。
目錄裡仍是 0 篇的有喀比、仙台、大邱、清萊、大叻、順化、全州，留給第七批，喀比優先。

## 給撰稿者：通用規則

讀者是台灣旅客。語氣像懂行、講話直接的朋友，每段都要有能照做的資訊，不寫「總之」「相信大家」「讓我們」。

每篇規格裡已經寫好這些事：
- 段落順序、每段寫什麼
- 要查的官方來源，以及規劃時讀到的數字
- offer 放哪裡
- 站內連結放哪一段
- 圖解畫什麼
- 容易寫錯的事實

規格與這份 README 衝突時，以規格為準。

### 工作區與檢查指令

用 repo 的內容包工具（`app/guides/pack_cli.py`，#467 進 repo），格式跟生活分享系列相同。每篇一個目錄 `<workdir>/<slug>/`：

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

圖解要自己渲染成 PNG，用 Read 打開看版面。機械檢查看不到文字疊字、壓線、超出方框，第五批每三張就有一張是渲染後才發現的。
Windows 上把 `CHROMIUM_BIN` 指到 Edge：

```bash
cd apps/api
CHROMIUM_BIN="C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" uv run python -c "from pathlib import Path; from app.guides.pack_ingest import render_svg; render_svg(Path('<workdir>/<slug>/diagram-1.svg'), Path('<workdir>/<slug>/diagram-1.png'))"
```

只在工作區寫檔，不改 repo 裡的檔案、不跑 git，不用共用的瀏覽器分頁。撰稿的 session 可能中途被切斷：落在磁碟上的檔案會留下來，結尾的報告不會。

**不要把任何個人資料送出去。** 用 curl 或腳本呼叫 Commons 等外部網站時，User-Agent 一律寫 repo 工具用的 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，不要放使用者或自己的 email、姓名。第六批有六篇的查核者把使用者的個人 email 放進 User-Agent 送給 Wikimedia。

### `pack.json`

```json
{
  "slug": "<slug>",
  "kind": "howto",
  "destination_id": "hong-kong",
  "topics": ["itinerary", "culture"],
  "featured": true,
  "display_order": 840,
  "valid_until": null,
  "locales": {
    "zh-TW": {
      "title": "…",
      "description": "≤500 字，一句話講清楚解決什麼問題，寫查證年月",
      "hero": { "src": "/guides/<slug>/hero.jpg", "alt": "描述照片內容", "width": 1, "height": 1 },
      "blocks": [],
      "sources": [ { "title": "網站名：頁名（查了什麼）", "url": "https://…", "checked_on": "2026-09-2x" } ]
    }
  }
}
```

slug、kind、destination_id、topics、featured、display_order、valid_until 照上面清單抄。

照片的 `width`、`height` 先填 1，`credit` 不要填，工具會從 Commons API 讀回來覆寫。自繪圖解的 image 區塊寬高也填 1。

區塊只能用下面這幾種：
- heading：level 只能是 2 或 3。
- paragraph：≤4,000 字。
- list：1–30 項。
- link：只放站內網址。
- image：照片用 `photo-1.webp`，圖解用 `diagram-1.svg`。
- table：最多 6 欄、30 列，每格 ≤300 字。
- callout：tone 只能是 tip、warning、info。
- offer：module 只能是 flight、hotel、activities、transport、connectivity。

全部純文字：不能有 HTML、Markdown、emoji，`<` 後面不能直接接字母，也不能有 `&amp;` 這類實體。

結構：
- 第一個區塊是 paragraph，不下「前言」標題。
- 至少 3 個 level 2 標題、1 張表格、1 個 callout、1 張自繪圖解，內文照片 1–2 張。
- 字數（正文，不含 sources）：howto 1,800–3,000 字，intel 800–1,500 字。規格另有字數目標的，以規格為準。

**表格最多 4 欄。** 文章表格在 375 px 手機上會把每一欄擠進螢幕寬，五欄的表每欄只剩 44–58 px，一列高到 300 px。
在票 `2026-09-14-guide-tables-squeezed-on-phones` 修好渲染器之前，第五批已經把五欄摺成四欄，這批一開始就照這個寫。

### 事實查核

- 票價、時刻、營運時間、規定都要用 WebFetch 讀官方頁確認才寫，文中寫「2026 年 9 月查證」。**查不到官方確認的數字就不寫數字**，改寫「以官網為準」。
  WebSearch 每篇最多 5 次。
- 規格裡的數字是規劃當天讀到的，撰稿時要再打開一次核對；官方頁改了就照新的寫，並在 `notes.md` 記下。
- 法規類的事實（入境、免稅額、海關、行動電源、實名登記）要回到主管機關的頁面或法規原文查，引用時寫出是哪個機關、哪一頁。
  不能拿媒體轉述當定論；只有外國使館通知的內容，也不能寫成現行規定。
- 幣別用當地幣別：日圓、韓元、港元、新加坡幣、越南盾、泰銖。日期寫完整，時效性的內容寫清楚「自 2026-10-01 起」。
- 下面這些網站在這台機器上讀不到，或讀到的內容不能直接用，規格裡已經寫了替代來源：
  - tourismthailand.org 英文站（thai.tourismthailand.org 可以讀）
  - jreast.co.jp
  - Korail
  - customs.gov.vn
  - evisa.gov.vn
  - 桃園機場官網（403）
  - 港鐵 `/customer/services/` 底下的頁面
  - 人事總處新聞稿：WebFetch 的摘要把日期寫錯了，要用 curl 讀原始 HTML。
- 第五批的教訓：**過了機械檢查的草稿，不等於查證過的文章。** 高山白川鄉、越南入境兩篇交給新的查核者後，各改掉 13 處錯誤。

### 分潤區塊（offer）

- 每篇最多 3 個，不放在第一個 level 2 標題之前，也不能兩個相鄰。位置與 module 照規格。
- 跨城市文章（destination_id 是 null）的 offer 要填 destination_id。
- heading 用通用說法，例如「香港機場交通與票券先比價」，不點名區塊不一定畫得出的商品。
- entry、packing、shopping、etiquette、safety、food、budget 主題原則上不放；入境情報文末可以放一個機場交通 offer。
- 目前正式站只有 tokyo、osaka-kyoto、seoul、busan、taipei 的 activities 與 transport 有核准方案。其他城市，以及所有 hotel、connectivity 區塊，
  上線時什麼都不會畫，要等後台核准；區塊還是照放。

### 站內連結

- 只連兩種文章：main 上已存在、而且有 zh-TW 版本的文章，以及這批 20 篇。台灣那二十篇沒有 zh-TW 版，不能連。
  網址格式：`https://mokaair.com/zh-TW/guides/<kind>/<slug>`、`…/destinations/<id>`、`…/foods?city=<id>`。
- **時效：** howto 不連會在它主要閱讀期內過期的 intel。季節段非連不可時，規格裡已寫明刪除日期；刪除日 = 該 intel 的 `valid_until` 隔天。
  連結前的那句話要寫成拿掉連結後仍然讀得通。
- 和 #468、第五批重疊的段落要縮短並連過去，口徑要一致。規格裡點名的例子：
  - 新加坡熟食中心的占位方式
  - 越南過馬路
  - 天星小輪不寫票價
  - 日本訂房的「免費取消有期限」

### 照片

- 只用 Wikimedia Commons，授權限 CC0、Public domain、CC BY、CC BY-SA；不用 NC、ND、KOGL，也不用沒標授權的。每個候選都要打開檔案頁確認。
- hero 選橫幅、寬 ≥1600 px、主體清楚。Commons 原檔很大的照片常常壓到 JPEG 品質 44 還超過 200 KB（第五批日光、南怡島都遇過），換一張比硬壓有用。
- 同一張照片不能當兩篇的 hero。紙鈔、商標、螢幕截圖、可辨識人臉的照片不用。

### 圖解

- 規格：viewBox `0 0 1600 900`，要有 `role="img"`、`<title>`、`<desc>`，所有 `font-size` ≥15，不外連。右下角放 `© Mokaair 製圖 2026`。
  配色與字型串照 `docs/life-ai-series-brief.md` 第 6 節：
  - 韓國主題加 Noto Sans KR。
  - 泰國主題加 Noto Sans Thai。
  - 香港、新加坡、越南用預設字型串。
- **圖上每個數字都要出現在正文**，工具會擋。
- 標籤用當地文字加英文。一張圖只講一件事。

## 給協調者：收件步驟

1. 撰稿者交件後，先讀 `notes.md`，抽查三個以上數字是否真的出自官方頁。報告裡的「需要注意」每一條都要追。
2. `ingest --dry-run` 通過、渲染圖看過沒問題之後，才正式 ingest（不加 `--dry-run`）。
3. 工具不檢查的四件事，要自己檢查：
   - 站內連結的 slug 與 kind 是否存在
   - offer 是否在第一個 h2 之後、是否兩個相鄰
   - 表格是否超過 4 欄
   - Commons 作者欄位是不是網址或授權說明文字（第五批有 6 張照片是這樣）
4. `uv run pytest tests/test_guides_content_pack.py -q`，然後開 PR。
5. 合併、部署後，在正式站先跑 `guides-import --dry-run`，確認只有這二十篇是 `create`，再跑 `--publish`。
6. 每個規格最後一節「上線後與交叉檢查」裡有日期的項目，都在上線 PR 開成票，例如 2027-01-10 刪掉連假篇的 2026 年那一節。
