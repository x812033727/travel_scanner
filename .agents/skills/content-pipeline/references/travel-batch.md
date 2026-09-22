# zh-TW 旅遊／美食批次：從規格到 PR

適用：howto／intel 旅遊攻略、料理 × 城市的美食特輯、商圈咖啡店特輯。這一頁只列「要點＋去哪裡讀」，規則全文在各批 README。規格與 README 衝突時以規格為準；規格內部衝突時以它的「撰稿時要小心」為準（第七批 ERRATA 的裁決）。

## 批次的 docs 目錄

`docs/<批次目錄>/`，例如 `docs/travel-guides-batch-8/`、`docs/korea-food-specials/`：

- `README.md`：清單表（`| # | 規格 | kind | destination_id | topics | display_order | valid_until |`）、「給撰稿者：通用規則」（只寫本批與上一批不同的地方，其餘指向上一批 README）、「給協調者：收件步驟」。
- 每篇一個 `<SLUG>.md` 規格：summary 講什麼、段落順序、要查的官方來源（規劃當天讀到的網址與原文逐字抄進去）、offer 放哪、站內連結與 `related`、圖解畫什麼、容易寫錯的事實、上線後與交叉檢查。
- `FOLLOWUPS.md`：有日期或條件觸發的複查、既有文章要補的反向連結、查過決定不處理的。
- `ERRATA.md`：規格發出後發現的錯與裁決。
- 可選 `batch.json`（給 `intake_check.py --manifest`）與 `shared-numbers.json`（給 `shared_check.py --rules`），格式寫在兩個腳本的開頭。

## 工作區（repo 外）

`<WORKDIR>/<SLUG>/`：`pack.json`（先寫）、`diagram-1.svg`（第二張叫 `diagram-2.svg`，文章裡要真的放）、`images.json`（`{"hero": {"title": "File:…"}, "photos": {"photo-1": {"title": "File:…"}}}`）、`notes.md`（一行一條 `主張｜來源網址｜查證日`，尾端三節：與規格不同的地方／我懷疑但沒動的事／進度）、`report.md`、`verify-1.md`、`verify-2.md`。helper 腳本放 `<WORKDIR>/_tools/<SLUG>/`。

旅遊文章的 hero 用 Commons 實景照，不畫 `hero.svg`。`pack.json` 裡 hero 的 `src` 寫 `/guides/<SLUG>/hero.jpg`、width 與 height 先填 1、`credit` 留空，ingest 會從 Commons 讀回來覆寫。

## `pack.json` 要點

全文與範例在 `docs/travel-guides-batch-7/README.md` §`pack.json`，欄位細節在 `docs/travel-guides-batch-6/README.md` §`pack.json`。

- 頂層：slug、kind、destination_id、topics（要在 `apps/api/app/guides/taxonomy.py` 的 `SEED_TOPICS` 裡）、featured、display_order（每批一個區段）、valid_until（intel 才有）、aliases、related（最多 4）、locales。
- 一日遊掛基地城市（芭達雅掛 bangkok、白川鄉掛 kanazawa）。目錄裡沒有的城市 → destination_id 是 null → 零 offer、最多兩個城市頁 link、不放美食目錄。
- 區塊：summary 第一（2 到 5 句，第一句是答案，數字逐字照正文，不寫後設句）→ 開頭 paragraph → 至少 3 個 level 2 標題、1 張表格（設計上限 4 欄，渲染器允許 6）、1 個 callout、恰 1 張圖解、1 到 2 張照片；FAQ 只在規格列了才放。全部純文字：無 HTML、Markdown、emoji、實體。
- 字數：`pack_ingest._body_length` 算 summary、每一格、callout、FAQ、連結句，不算標題。repo 的硬限制 howto 1,500 到 6,000、intel 700 到 3,000 是 CI 的真相；批次裁決 howto 上限 4,200（目標 3,000 到 3,600）、intel 上限 2,200（目標 1,500 到 1,900）；規格裡每個 H2 的字數是上限。刻意寫短的篇不補。
- 站內連結：文章用 `article` inline，`kind` 填對方的；城市頁 `https://mokaair.com/zh-TW/destinations/<id>`、美食目錄 `https://mokaair.com/zh-TW/foods?destination_id=<id>` 用 `link` 區塊。既有文章的 `?city=` 不是錯，不順手改。連結目標要在 `apps/api/app/guides/content/` 有 zh-TW 版，或是本批的 slug。
- offer：最多 3 個、第一個 H2 之後、不相鄰、通用標題、無品牌與金額；null destination 零 offer（後台的 `_validate_document` 會擋）。
- sources：`title`（網站名：頁名（查了什麼））、`url`（轉址後的最終網址）、`checked_on`（真的打開那頁的日期）。

## 事實

- 官方頁當天重開。兩個官方來源打架：可執行的數字擇一，預設營運者，另一邊一句話揭露，不並列成兩個選項；開放時間有疑義用較窄的時段。全文在 `docs/travel-guides-batch-8/README.md` §本批與第七批不同的地方 第 3 到 5 條。
- 讀不到的官方站與特殊讀法（Inertia 的 `data-page`、`__NEXT_DATA__`、WordPress REST、兩段 POST、掃描 PDF 用 pymupdf）：`docs/travel-guides-batch-8/README.md` §「讀不到的官方站」更新、`docs/travel-guides-batch-7/README.md` §事實查核。
- 已經不是官網的網域（賭場連結、停放頁、轉到社群平台）不得引用；規格與 README 會列，新發現的加進去。
- 地名以目的地目錄為準：`apps/api/app/destinations/catalog.py`、`apps/api/app/hotspots/areas.py`、`apps/api/app/foods/area_catalog.py`。目錄外的寫法放 `aliases`。
- 讀者看得到的地方不寫會成長的數字：標題、描述、summary 不寫家數。美食篇預設不寫價格，互相矛盾的年份一律不寫（`docs/korea-food-specials/README.md` §數字）。

## 照片與圖解

全文在 `docs/travel-guides-batch-7/README.md` §照片、§圖解。

- Commons 只收 CC0、PD、CC BY、CC BY-SA（NC、ND、KOGL 不收，程式是 `pack_ingest.ALLOWED_LICENSE`）；每個候選都開 File: 頁確認；hero 橫幅寬 ≥1600 px、壓到 200 KB 以下（硬上限 300 KB）、全站唯一；紙鈔、商標、截圖、可辨識人臉不用。正文寫完才搜 Commons；十幾個代理別同時搜，會 429。
- 圖解：viewBox `0 0 1600 900`、`role="img"`、`<title>`、`<desc>`、所有 font-size ≥15、系統字型、不外連、右下角 `© Mokaair 製圖 2026`；配色與字型在 `docs/life-ai-series-brief.md` 第 6 節。**圖上每個數字都要出現在每個語系的正文。** 渲染成 PNG 自己看過：重疊、壓線、超框機器看不到。

## 派工

- 一位代理一篇：context 小、便宜、被切斷損失小。launch 訊息只帶 IDENTITY 區塊：slug、kind、destination_id、字數區間、兩個範例包、共用數字的兄弟篇、規格與 README 路徑；提示本文用 `.agents/skills/content-pipeline/references/prompts/writer-travel.md`。
- 查核用 `.agents/skills/content-pipeline/references/prompts/verifier-travel.md`，一定換人；第一輪改超過三個事實就第二輪，再換一個人。
- 六篇以上的批次，規格的一致性審查按地區分組：每組三個視角，各組可改自己的規格，只回報跨組衝突。「一個視角讀完全部 20 篇」在 1 MB 的規格上失敗過。
- 裁決回給原審查者（context 還在）比開新代理便宜。

## 收件（協調者）

1. 讀 `notes.md`，抽查三個以上的數字真的出自官方頁；報告裡「需要注意」每一條都追。
2. `pack_cli ingest --dry-run` 過、圖解 PNG 看過，才正式 ingest。
3. `intake_check.py --slug <SLUG> --from-content`（連結目標、offer 位置、欄數、summary 數字、hero 唯一、credit、讀者優先、`lint_document`、SVG 規則）；有共用數字的批次跑 `shared_check.py`。
4. `pack_cli lint --kind howto`（或 `intel`）；`pytest tests/test_guides_content_pack.py -q`。
5. PR 帶：內容包、`apps/web/public/guides/<SLUG>/`、批次 docs、票；描述附 dry-run 摘要。
6. 合併後照 `.agents/skills/content-pipeline/references/publish-runbook.md`。
