---
id: 2026-09-20-launch-korea-food-specials-1
title: Launch the Korea food and cafe specials batch 1
status: in-progress
priority: P2
area: docs
owner: claude-opus-5
claimed_at: 2026-09-20T09:06:58Z
created_at: 2026-09-20T09:06:28Z
completed_at:
branch:
depends_on: []
scope:
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

- [ ] 22 個內容包在 `apps/api/app/guides/content/`，每個都通過 `pack_cli ingest --dry-run` 零錯誤
- [ ] 22 組資產在 `apps/web/public/guides/<slug>/`（hero、圖解、內文照片）
- [ ] 每篇都經過兩輪獨立查核（查核者與撰稿者不同模型），逐條記錄在工作目錄的 `verify/<slug>/`
- [ ] 正式站發布後，每一篇：200、h1 等於標題、canonical 正確、無 noindex、hero 與圖解都 200
- [ ] 每個子主題 hub 列出正確的文章；麵包屑是「旅遊情報與攻略 › 旅遊攻略 › 美食 › <料理> › 標題」
- [ ] `travel-zh-TW` sitemap 列出這 22 篇

## Steps

- [ ] 規格 → 撰稿 → 兩輪查核 → 收件檢查（22 篇）
- [ ] 開 PR-C（內容包＋資產）
- [ ] 部署 → `seed-foods` → `guides-import --slug ×22 --locale zh-TW --dry-run` → `--publish`
- [ ] `guides-links-rebuild` → `guides-links-check --locale zh-TW`
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
- 字數帶寬 2026-09-20 從 3,900／4,200 放寬到 **3,600–4,400、硬牆 4,600**：repo 自己對 `howto` 的建議區間是 `TEXT_RANGE = (1_500, 6_000)` 而且只是 warning，舊的牆逼撰稿者砍掉規格自己要的 callout 與 FAQ。
- 工作目錄（不在 repo 裡）：`C:/Users/x8120/mokaair-work/korea-food-specials/`，`STATE.md` 是進度，`prompts/` 是各階段的代理指令，`verify/` 是逐條查核記錄。
- 相關票：`2026-09-20-kfood-isim-address-conflict`、`2026-09-20-kfood-maxim-plant-evidence`（研究階段撞到的正式站資料問題）。
