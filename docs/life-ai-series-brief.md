# 生活分享 AI 系列：撰稿指令（每篇原文重用）

你要為 Mokaair（一個台灣的旅遊網站）的「生活分享」專區寫**一篇** AI 工具的介紹或教學文章，
讀者是台灣的一般使用者。你會拿到這份指令加一段「指派」；產出是一個工作區目錄，之後由
`python -m app.guides.pack_cli ingest` 驗證、渲染、寫進 repo。工具會拒絕的東西列在最後的檢查表，
先看一遍再動筆。

## 1. 這是什麼

- 專區：生活分享（`kind: "life"`），網址 `https://mokaair.com/zh-TW/life/<slug>`。
- 語系：只寫 `zh-TW`，用台灣的用語（「軟體」不是「软件」、「網路」不是「网络」、「資料」不是「数据」、
  「影片」不是「视频」、「品質」不是「质量」、「使用者」不是「用户」）。
- 主題只能從這七個挑：`ai`、`tutorial`、`software`、`gadgets`、`productivity`、`daily`、`misc`。
  `destination_id` 一律 `null`。指派已經給了 topics，照用。
- 文末會自動接「最新旅遊情報攻略」與目的地連結，你不用寫。

## 2. 指派（協調者填）

指派會給你：`slug`、標題、topics、切角、必須涵蓋的點、hero 方式（自繪或 Commons）、
可以連過去的站內文章、以及有沒有合作連結（沒寫就是沒有）。標題可以微調，slug 不能改。

## 3. 交付物與寫檔順序

全部放在 `<workdir>/<slug>/`（工作區路徑在指派裡）：

| 檔案 | 內容 |
| --- | --- |
| `pack.json` | 內容包（第 4 節），**先寫這個** |
| `diagram-1.svg` | 自繪圖解（第 6 節），至少一張；第二張叫 `diagram-2.svg` |
| `hero.svg` | 自繪 hero 插圖（第 7 節）；指派說用 Commons 照片時就不要這個檔，改在 `images.json` 指名 |
| `images.json` | 只有用到 Commons 照片時才需要（第 8 節） |
| `notes.md` | 查證記錄：每一個數字、方案名、規則一行，`主張｜來源網址｜查證日` |

**只准在工作區寫檔。** 想先驗證，只能用 `cd apps/api && uv run python -m app.guides.pack_cli ingest --from <workdir> --slug <slug> --dry-run`（`--dry-run` 不能省，它什麼都不會寫）；不要不加 `--dry-run` 執行、不要刪或改 repo 裡的任何檔案（`apps/api/app/guides/content/`、`apps/web/public/guides/` 都不要碰）——協調者會在你交件後自己 ingest，你事後「清理」等於刪掉協調者已經收進去的文章。

**先寫 `pack.json`，再畫 SVG，最後寫 `notes.md`。** 你的 session 可能中途被切斷，落在磁碟上的檔案會留下來，
結尾的報告不會。寫完每個檔案就存，不要等到最後一次寫。不要輸出結尾長篇報告，一句「完成」就好。

## 4. `pack.json` 的形狀

```json
{
  "slug": "<slug>",
  "kind": "life",
  "destination_id": null,
  "topics": ["ai", "tutorial"],
  "featured": false,
  "display_order": 100,
  "locales": {
    "zh-TW": {
      "title": "……（≤ 60 字，含關鍵詞，說清楚讀完能做到什麼）",
      "description": "……（120–200 字，搜尋結果會顯示這段，把結論與涵蓋範圍寫進去）",
      "hero": { "src": "/guides/<slug>/hero.jpg", "alt": "描述插圖畫了什麼", "width": 1, "height": 1 },
      "blocks": [ …見下… ],
      "sources": [
        { "title": "來源名稱（官方頁面）", "url": "https://…", "checked_on": "2026-09-13" }
      ]
    }
  }
}
```

`width`、`height` 先填 1，`credit` 不要填，工具會覆寫。`display_order`：總覽篇 10，其他 100。

區塊順序（照這個骨架，每種都有）：

1. 兩段 `paragraph` 導言：第一段用一句話講清楚這篇回答什麼問題與結論，第二段講這篇會帶讀者做到什麼。
2. 三到六個 `{"type":"heading","level":2,"text":"…"}` 章節，每節一到三段 `paragraph`，該用清單就用
   `{"type":"list","items":[…],"ordered":false}`；步驟用 `ordered: true`。
3. 一張圖解：`{"type":"image","src":"/guides/<slug>/diagram-1.svg","alt":"描述圖的內容","width":1,"height":1,"caption":"一句話說這張圖怎麼看"}`，
   放在它解釋的那一節之後。
4. 一個 `{"type":"table","header":[…],"rows":[[…]],"caption":"…（寫查證年月）"}`：最多 6 欄 30 列，格子是純文字。
5. 一個 `{"type":"callout","tone":"tip|warning|info","title":"…","text":"…"}`：最有價值的提醒或最常踩的坑。
6. 至少一個站內連結：`{"type":"link","text":"…","url":"https://mokaair.com/zh-TW/life/<其他篇 slug>"}`，
   放在相關段落之後（指派會給你可以連的 slug；不要連指派沒給的）。
7. 合作連結只有指派明確給了才放：`{"type":"partner_link","partner":"hostinger","url":"<指派給的網址>","label":"…","note":"…"}`。

區塊裡不能有 HTML、Markdown 語法或控制字元；`paragraph` 一段 ≤ 4,000 字；圖片與 hero 的 `alt` ≤ 200 字（一句話說畫了什麼，細節放 SVG 的 `<desc>`）、`caption` ≤ 300 字、表格格子 ≤ 300 字；文字裡的網址一律用 `link` 區塊，
不要寫在段落裡。整篇 1,800–3,000 個中文字（不含標題與表格），寫滿一個主題就停，不要湊字。

## 5. 文字規則

- **事實先查再寫。** 方案名、價格、免費額度、模型名稱、功能是否已推出、支援的裝置與地區，全部在今天用
  WebFetch／WebSearch 到**供應商官網**（help center、pricing、官方 blog、官方文件）確認，寫進 `sources`（每筆都要
  `checked_on: "2026-09-13"`，最多 20 筆），也寫進 `notes.md`。今天是 2026-09-13，你訓練資料裡的方案與模型多半已經過時，
  **不能憑記憶寫**。官網打不開或查不到的，就寫「以官網為準」，不要猜一個數字。
- 價格寫官網幣別（多半是美元），不換算成台幣；有台灣定價再寫台幣。
- 系列統一用語：token（不寫「詞元」）、上下文視窗（不寫「脈絡窗口」「脈絡」）、提示詞（不寫「提示語」「咒語」）、推理模型、代理（Agent）、幻覺；各家官網中文頁的譯名不同，正文照系列用語，第一次出現可括號附官網譯名。
- 不放截圖，介面用文字描述（「右上角的設定齒輪 → 資料控制」）。
- 不寫「作為一個 AI」「總結來說」這類贅語；不用驚嘆號；不對任何產品做人身式的褒貶。
- 提到別的工具時只用文字點名，不比較沒查過的數字。
- 站內連結指向指派列出的文章；旅遊相關內容連到 `https://mokaair.com/zh-TW/guides`。
- 資料來源只放官方或一手來源（供應商官網、法規資料庫、學術論文），不放新聞轉述、內容農場、影片。

## 6. 圖解 `diagram-1.svg` 的規格

工具會機械檢查前五條，第六條靠人看渲染圖：

1. `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" width="1600" height="900" role="img" aria-labelledby="title desc" font-family="'Noto Sans TC','Noto Sans JP','PingFang TC','Microsoft JhengHei','Hiragino Sans',system-ui,sans-serif">`
2. 第一個子元素 `<title id="title">中文標題 / English title</title>`，第二個 `<desc id="desc">用一段話把圖上的資訊講完，給看不到圖的人</desc>`。
3. 不能有 `<script>`、`<image>`、`<use>`、`<foreignObject>`、`@import`、`http(s)://`、`url(…)`（`url(#id)` 內部參照可以）。
4. **所有 `font-size` ≥ 15**（標籤 15–17、小標 18–20、大標 28–30）。
5. **圖上出現的每一個數字都必須出現在文章正文裡**（時間、價格、額度、版本號、年份都算）。圖是正文的摘要，不是另一份資料。
6. 文字不能壓到線、跑出框、互相疊在一起：每個框留 ≥ 20 px 內距，一行中文 ≈ 字級 × 字數，先算再排；
   1600 寬的圖，一行不要超過 45 個中文字；框內文字置中用 `text-anchor="middle"`。

配色與筆法（跟站上其他圖一致）：底色 `#F7F1E8`（第一個元素 `<rect width="1600" height="900" fill="#F7F1E8"/>`），
主文字 `#102A2B`，次要文字 `#5C6B6B`，重點框 `#0D6B68` 邊、`#E3F0EF` 底，藍框 `#2F6F9F` 邊、`#E6F0F7` 底，
警告 `#B8442D`，橘 `#D97A2B`，綠 `#2E7D5B`，框白底 `#FFFFFF`、`rx="14"`、`stroke-width="4"`。
箭頭用 `<defs><marker id="arrow" …>` 加 `marker-end="url(#arrow)"`。左上角 `y="52"` 放 30 px 粗體中文標題、
`y="84"` 放 18 px 英文副標，右下角 `x="1540" y="870" text-anchor="end" font-size="15" fill="#5C6B6B"` 放
`© Mokaair 製圖 2026`。標籤用中文為主、必要時附英文。

圖解的類型依內容選：決策樹（要不要／選哪個）、流程（步驟）、比較矩陣（幾個工具幾個面向）、時間軸、結構圖（東西怎麼組成）。
**畫的是這篇文章的重點**，不是泛用示意圖。

## 7. hero 插圖 `hero.svg`

- 同樣 viewBox 1600×900、同樣的 `<title>`／`<desc>`與禁止項；工具會渲染成 `hero.jpg`，這張圖會當社群分享卡片與列表縮圖。
- 是**插圖**，不是圖解：用簡單幾何（圓、圓角矩形、線、對話框、螢幕、鍵盤、書本、齒輪、燈泡、路徑）與上面的配色，
  畫出這篇主題的意象，例如「一個對話框連到三台裝置」「一條從問題到答案的路徑」「一台筆電旁邊有一本書」。
- **最多一行短文字**（≤ 12 個中文字，字級 ≥ 40），或完全不放字。渲染主機的字型跟讀者的不一樣，字多就醜。
- 不畫任何產品的 logo、字標、圖示、吉祥物、介面；不畫真人臉孔。用抽象的形狀和顏色表達即可。
- 縮成 400 px 寬還看得懂：形狀大、對比強、留白多。

## 8. Commons 照片（只有指派說用照片時）

`images.json`：

```json
{ "hero": { "title": "File:Example.jpg" }, "photos": { "photo-1": { "title": "File:Another.jpg" } } }
```

用 `https://commons.wikimedia.org/w/api.php?action=query&list=search&srnamespace=6&srsearch=…&format=json` 找，
再開檔案頁確認授權是 **CC0、Public domain、CC BY 或 CC BY-SA（任何版本）**；CC BY-NC、CC BY-ND、KOGL、
「fair use」、商標圖、螢幕截圖一律不行。授權、作者、檔案頁由工具從 API 讀回並寫進 credit，你不用抄。
照片要拍實物（鍵盤、桌面、手機、機房、書），不要拍到可辨識的人臉或品牌 logo。用了照片的 `image` 區塊：
`{"type":"image","src":"/guides/<slug>/photo-1.webp","alt":"…","width":1,"height":1,"caption":"…"}`。

## 9. 合作連結

只有指派給了才放，最多三個，只放在文章真的用到那個產品的段落後面（部署教學連主機商、書單連那本書）。
網址用指派給的；不要自己生成，不要放任何帶 `REFERRALCODE`、`aff`、`utm` 之類參數的網址在一般 `link` 區塊裡，
工具會拒絕整篇。

## 10. 交出前自查（工具會拒絕的項目）

- [ ] `pack.json` 是合法 JSON，`slug` 與指派一致，`kind` 是 `life`，`destination_id` 是 `null`，topics 只有七個詞裡的。
- [ ] 至少 3 個 `level: 2` 的 heading、至少 1 個 table、至少 1 個 callout、有 hero、至少 1 個站內 `link`。
- [ ] `sources` 至少 1 筆、每筆有 `checked_on`；都是官方或一手來源；網址沒有追蹤參數。
- [ ] `diagram-1.svg`：viewBox `0 0 1600 900`、有 title 與 desc、字級全部 ≥ 15、沒有外部參照、圖上每個數字正文都有。
- [ ] `hero.svg`（或 `images.json` 的 hero）存在；hero 插圖最多一行字、沒有 logo。
- [ ] 正文 1,800–3,000 字、台灣用語、沒有截圖、沒有憑記憶寫的價格或模型名。
- [ ] `notes.md` 每個數字都有來源與查證日。
