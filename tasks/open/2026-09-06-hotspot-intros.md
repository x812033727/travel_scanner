---
id: 2026-09-06-hotspot-intros
title: 景點的第一手介紹：儲存、審核與呈現
status: in-progress
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T17:48:40Z
created_at: 2026-09-06T17:48:17Z
completed_at:
branch: claude/hotspot-intros
depends_on: []
scope:
  - apps/api/app/hotspots/intros.py
  - apps/api/app/hotspots/service.py
  - apps/api/app/hotspots/router.py
  - apps/api/app/hotspots/admin_router.py
  - apps/api/app/i18n.py
  - apps/api/tests/test_hotspot_intros.py
  - apps/web/components/hotspot-intro.tsx
  - apps/web/components/hotspot-intro.test.tsx
  - apps/web/components/hotspot-explorer.tsx
  - apps/web/components/hotspot-explorer.test.tsx
  - apps/web/messages/en/hotspots.json
  - apps/web/messages/ja/hotspots.json
  - apps/web/messages/ko/hotspots.json
  - apps/web/messages/zh-TW/hotspots.json
  - apps/web/messages/zh-CN/hotspots.json
  - docs/hotspot-themes.md
---
# 景點的第一手介紹：儲存、審核與呈現

## Why

熱門景點頁上的「介紹」一直是別人寫的——連到 YouTube 影片或旅遊部落格的外部連結。使用者要的是另一種：Mokaair 自己寫的一段話，說明這是什麼地方、什麼時候去。購物景點尤其需要（該買什麼、免稅怎麼算、什麼時段人少），季節景點也是（花期大概什麼時候、怎麼看最好）。

`hotspot_intros` 的表在主題那個 PR（#245）就一起建好了，但一直沒有程式碼用它。

## Definition of done

- [x] 一段介紹以 `pending` 進來，核准後才會出現在讀者眼前。
- [x] **AI 產生的草稿永遠不會默默覆蓋已核准的段落**——有人讀過那段文字並說了可以。
- [x] 讀者看到自己語言的版本；只有簡繁互相遞補，英文讀者不會拿到日文。
- [x] 後台可以列出待審、批次核准／拒絕、直接改寫內容、手動新增一段。
- [x] 卡片與詳情面板顯示介紹，長文可展開。

## Steps

- [x] `intros.py`：`upsert_hotspot_intro_draft`（AI 工作寫入的接縫）、`load_public_intros`、`intro_coverage`、`intro_targets`、`clean_intro_body`。
- [x] `service.py` 的 ranking item 加 `intro`；`router.py` 加 `GET /hotspots/{id}/intro`。
- [x] `admin_router.py`：列表、批次審核、改寫、五語覆蓋率、手動新增。
- [x] `i18n.py` 兩個錯誤碼 ×5 語系。
- [x] 前端 `hotspot-intro.tsx`＋卡片與面板接線＋三個語言鍵。
- [x] 測試：API 16 個、前端 5＋3 個。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest        # 1118 passed
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
```

```
GET    /hotspots/{id}/intro                      # 讀者視角
GET    /admin/hotspots/intros?status=pending&locale=zh-TW
POST   /admin/hotspots/intros/review             {ids, action, reason?}
PATCH  /admin/hotspots/intros/{id}               {body?, review_status?, reason?}
GET    /admin/hotspots/{hotspot_id}/intros       # 五語覆蓋，缺的那格是 null
POST   /admin/hotspots/{hotspot_id}/intros       {locale, body, approve=true}
```

## Notes

- **不覆蓋已核准內容**是這張任務的核心。`upsert_hotspot_intro_draft` 碰到 `approved` 的列會原封不動回傳 `written=False`；只有明確傳 `replace_approved=True` 才會換掉，而且舊文會存進 `metadata_json["previous_body"]`，並把狀態退回 `pending`——換過的段落也還沒有人審過。
- `intro_targets()` 是給之後的 AI 產生工作用的：它問「哪些景點還缺哪些語言」，而不是給它一串景點。中斷後重跑不會重畫已經落地的。
- 簡繁互相遞補是唯一的跨語系 fallback（和 `area_name()` 同政策）。payload 會帶 `locale` 說明讀者實際拿到的是哪一種，前端要顯示語言標記時用得到。
- `intros.py` 裡 `from app.hotspots.service import PUBLIC_REVIEW_STATUSES` 是函式內 import：`service` 為了 ranking payload 會 import 這個模組，寫在頂層就成環了。
- 前端的展開門檻用「欄寬」而不是字數：一個中日韓字約等於兩個拉丁字母，90 個英文字和 90 個漢字不是同一段文章。`approximateColumns()` 有直接的測試。
- `apps/web/components/hotspot-explorer.tsx` 在 `2026-09-06-readable-foundation` 的 scope 裡，所以 claim 用了 `--force`：那張任務的 PR #229 已經合進 main（`df19535`），只是沒有跑 `tasks done`，檔案實際上沒有人在動。沒有去改別人的任務檔（board 規則一）。
