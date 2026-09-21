---
id: 2026-09-20-launch-korea-food-specials-1
title: Launch the Korea food and cafe specials batch 1
status: review
priority: P2
area: docs
owner: codex
claimed_at: 2026-09-20T12:09:46Z
created_at: 2026-09-20T09:06:28Z
completed_at:
branch: codex/korea-food-specials-complete
depends_on: []
scope:
  - docs/korea-food-specials
  - apps/api/app/guides/content/busan-dwaeji-gukbap-food-guide.json
  - apps/api/app/guides/content/seoul-dwaeji-gukbap-food-guide.json
  - apps/api/app/guides/content/busan-milmyeon-food-guide.json
  - apps/api/app/guides/content/seoul-naengmyeon-food-guide.json
  - apps/api/app/guides/content/seoul-samgyetang-food-guide.json
  - apps/api/app/guides/content/seoul-seolleongtang-food-guide.json
  - apps/api/app/guides/content/seoul-dak-hanmari-food-guide.json
  - apps/api/app/guides/content/seoul-kalguksu-food-guide.json
  - apps/api/app/guides/content/seoul-jokbal-food-guide.json
  - apps/api/app/guides/content/seoul-tteokbokki-food-guide.json
  - apps/api/app/guides/content/seoul-ganjang-gejang-food-guide.json
  - apps/api/app/guides/content/jeju-heukdwaeji-food-guide.json
  - apps/api/app/guides/content/jeju-gogi-guksu-food-guide.json
  - apps/api/app/guides/content/daegu-jjim-galbi-food-guide.json
  - apps/api/app/guides/content/daegu-makchang-food-guide.json
  - apps/api/app/guides/content/jeonju-bibimbap-food-guide.json
  - apps/api/app/guides/content/busan-jeonpo-yeongdo-cafe-guide.json
  - apps/api/app/guides/content/seoul-seongsu-cafe-guide.json
  - apps/api/app/guides/content/seoul-yeonnam-hongdae-cafe-guide.json
  - apps/api/app/guides/content/seoul-ikseon-bukchon-hanok-cafe-guide.json
  - apps/api/app/guides/content/jeju-aewol-cafe-guide.json
  - apps/api/app/guides/content/jeju-gujwa-sehwa-cafe-guide.json
  - apps/web/public/guides/busan-dwaeji-gukbap-food-guide
  - apps/web/public/guides/seoul-dwaeji-gukbap-food-guide
  - apps/web/public/guides/busan-milmyeon-food-guide
  - apps/web/public/guides/seoul-naengmyeon-food-guide
  - apps/web/public/guides/seoul-samgyetang-food-guide
  - apps/web/public/guides/seoul-seolleongtang-food-guide
  - apps/web/public/guides/seoul-dak-hanmari-food-guide
  - apps/web/public/guides/seoul-kalguksu-food-guide
  - apps/web/public/guides/seoul-jokbal-food-guide
  - apps/web/public/guides/seoul-tteokbokki-food-guide
  - apps/web/public/guides/seoul-ganjang-gejang-food-guide
  - apps/web/public/guides/jeju-heukdwaeji-food-guide
  - apps/web/public/guides/jeju-gogi-guksu-food-guide
  - apps/web/public/guides/daegu-jjim-galbi-food-guide
  - apps/web/public/guides/daegu-makchang-food-guide
  - apps/web/public/guides/jeonju-bibimbap-food-guide
  - apps/web/public/guides/busan-jeonpo-yeongdo-cafe-guide
  - apps/web/public/guides/seoul-seongsu-cafe-guide
  - apps/web/public/guides/seoul-yeonnam-hongdae-cafe-guide
  - apps/web/public/guides/seoul-ikseon-bukchon-hanok-cafe-guide
  - apps/web/public/guides/jeju-aewol-cafe-guide
  - apps/web/public/guides/jeju-gujwa-sehwa-cafe-guide
---

# Launch the Korea food and cafe specials batch 1

## Why

站主 2026-09-20 要的兩類韓國內容：**韓國美食攻略**以「料理 × 城市」為單位分類（豬肉湯飯｜首爾、豬肉湯飯｜釜山…），以及**商圈咖啡店**特輯。22 篇 zh-TW `howto` 內容包，每篇只掛一個旅遊子主題（料理用 `kr-*`、咖啡用 `cafe`），城市軸沿用既有的「依目的地瀏覽」。

分類機制與料理資料庫已經先落地：**PR #580**（migration 0082，15 個旅遊子主題）與 **PR #581 / #586**（7 道新料理＋代表店）都已合併。這張票只剩內容本身。

選店標準是這一批的核心：**入選只有一個條件——有官方來源點名這家店這個分店**（A1 觀光公社／市政府的店家頁或官方專題、A2 政府認證且有公開名冊）。不是排名，不是試吃心得。規則全文在 `docs/korea-food-specials/README.md`。

## Definition of done

- [x] 22 個內容包在 `apps/api/app/guides/content/`，每個都通過 `pack_cli ingest --dry-run` 零錯誤
- [x] 22 組資產在 `apps/web/public/guides/<slug>/`（hero、圖解、內文照片）
- [x] 每篇都經過兩輪獨立查核（查核者與撰稿者不同模型），逐條記錄在工作目錄的 `verify/<slug>/`
- [ ] 正式站發布後，每一篇：200、h1 等於標題、canonical 正確、無 noindex、hero 與圖解都 200
- [ ] 每個子主題 hub 列出正確的文章；麵包屑是「旅遊情報與攻略 › 旅遊攻略 › 美食 › <料理> › 標題」
- [x] `travel-zh-TW` sitemap 列出這 22 篇

## Steps

- [x] 規格 → 撰稿 → 兩輪查核 → 收件檢查（22 篇）
- [x] 開 PR-C（內容包＋資產）
- [x] 部署 → `seed-foods` → `guides-import --slug ×22 --locale zh-TW --dry-run` → `--publish`
- [x] `guides-links-rebuild` → `guides-links-check --locale zh-TW`
- [ ] 逐頁驗證（含隨機抽 Naver 連結在真實瀏覽器打開是對的店）
- [ ] 上線後處理 `docs/korea-food-specials/admin-todo.md` 的後台待辦

## How to verify

```bash
cd apps/api && python -m app.guides.pack_cli lint --kind howto
```

零錯誤。發布後：

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://mokaair.com/zh-TW/guides/topics/kr-dwaeji-gukbap
```

## Notes

- **正式站的每一步都要站主明確同意**，不要自己跑發布指令。
- **米其林全批一個字都不寫**：`guide.michelin.com` 對我們每個工具都回 403（一手來源讀不到），政府頁的轉述又互相打架（同一家店三個官方頁三個年份）。原計畫的 `kfood-michelin-2027-edition` 複查票因此取消。
- 正文字數依 `docs/korea-food-specials/README.md` 最後一次調整：**目標 3,800–4,600、硬牆 5,000**；repo 的 `howto` 建議區間是 `TEXT_RANGE = (1_500, 6_000)`，只產生 warning。
- 工作目錄（不在 repo 裡）：原研究在 `C:/Users/x8120/mokaair-work/korea-food-specials/`；最後收件稿與原始查核在 `C:/Users/x8120/mokaair-work/korea-food-specials-codex/`。44 份可審閱的查核紀錄與跨篇檢查腳本已整理進 `docs/korea-food-specials/verification/`。
- 相關票：`2026-09-20-kfood-isim-address-conflict`、`2026-09-20-kfood-maxim-plant-evidence`（研究階段撞到的正式站資料問題）。
- 2026-09-20 本機完成：22 篇 `pack_cli ingest --dry-run` 零錯誤、`pack_cli lint` 22 entries checked、逐篇 intake 零錯誤、跨篇檢查 22 packs／44 reviews、`npm run check:tasks` 與 `npm run test:tools` 通過。咖啡篇逐店類型再次覆核後移除缺乏類型依據的 Polv、477+；少數字數及 hero 品質下限提示不影響硬性門檻。正式站步驟仍待站主逐步同意。

## 2026-09-21 正式站上線（站主逐步同意）

站主在 2026-09-21 明確指示「照手冊匯入那 22 篇」，第 3、4 步照 `launch-runbook.md`
執行完畢。指令加了 `--actor-email`（手冊沒寫）：CLI 要求 actor 必須是有效管理員，
值取自 api 容器的 `ADMIN_EMAILS`，否則會以 `The actor must be an active administrator`
退出且不寫入任何資料。

已完成並實測：

- `seed-foods` 在此之前就有人跑過了。公開 facets 回報全部 127 道，正好是手冊寫的
  種完數字（基準 120），所以這一步沒有重跑。
- 匯入前 dry-run：22 篇全部 `create`、0 `update`，與手冊預期一致。
- `guides-import --slug ×22 --locale zh-TW --publish`：**created 22 / published 22 /
  updated 0**。同一組參數重跑 dry-run，22 篇全部轉為 `unchanged`。
- `guides-links-rebuild`：materialized 1790、dropped 0、unavailable 0、unresolved 0。
- `guides-links-check --locale zh-TW` 仍有兩筆 `unpublished`，都不是這批：
  `jiufen-shifen-yehliu-day-trip` 與 `intel/taiwan-entry-2026-arrival-card`。
- 手冊抽樣的三篇：全部 200、`noindex` 歸零、h1 與標題相符。
- 15 個子主題頁（`kr-*` 十四個加 `cafe`）全部 200。
- `travel-zh-TW.xml` sitemap：22/22 篇到齊。

**還沒做，留給下一個人：**

- 逐頁驗證只抽了手冊指定的三篇。其餘 19 篇的 200／h1／canonical／noindex，以及每篇
  hero 與圖解的 200，都還沒逐一跑過。
- 子主題 hub 是否列出正確的文章、麵包屑是否為「旅遊情報與攻略 › 旅遊攻略 › 美食 ›
  <料理> › 標題」、有沒有誤觸合作方案面板、文末美食目錄連結是否非空——都還沒看。
- `docs/korea-food-specials/admin-todo.md` 的後台待辦（A 組）未動。

**Naver 連結抽驗沒有完成，原因是工具而不是內容。** 內建瀏覽器把 `map.naver.com`
列為政策封鎖網域，不是機器人驗證；Claude in Chrome 擴充功能在該工作階段兩次都回報
未連線。沒有繞過封鎖，改為交給站主自行點開。手冊隨機抽中的三篇與期待值：

| 文章 | 連結 | 應為 |
|---|---|---|
| `seoul-kalguksu-food-guide` | place ID `1964656612` | 하니칼국수，`서울 중구 퇴계로 411-15` |
| `seoul-dwaeji-gukbap-food-guide` | search `광화문국밥 정동` | 광화문국밥，`중구 세종대로21길 53` |
| `seoul-dak-hanmari-food-guide` | search `명동닭한마리 종로5가` | 명동닭한마리，`종로구 종로40가길 14` |

改以機械檢查補上，範圍是全部 111 個 Naver 連結而非抽三個：

- 形式分布：**place ID 24 個、搜尋字串 87 個**。24 個 ID 全為數字，且沒有任何一個
  ID 在不同文章間重複——ID 重複正是連到隔壁家的典型徵兆。
- 87 個搜尋連結中，75 個的店名與區域都能在同一段落的內文對上。其餘 12 個逐一看過，
  11 個是比對規則太粗（內文用官方中文店名如「平安道家」「胖嘟嘟奶奶家」，查詢字串
  用韓文店名；或區域在內文寫成完整門牌），內容本身沒問題。
- **唯一實質疑慮**：`seoul-tteokbokki-food-guide` 有一個查詢是
  `허리케인박 떡볶이닭발 약속떡볶이`，三個名稱串成一個搜尋字串。內文說官方頁把現名
  與括號裡的舊名並列，所以字串是這樣拼出來的，但三詞搜尋不一定收斂到單一店家。

結構性觀察：111 個連結裡 87 個是搜尋形式。搜尋結果會隨時間漂移，place ID 不會。
要長期穩定，補 place ID 比每季複查搜尋字串有效，可併入
`2026-09-20-kfood-closure-sweep-2026-12` 一起考慮。
