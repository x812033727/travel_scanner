---
id: 2026-09-12-guides-visibility-and-admin-list
title: 情報攻略文章的隱藏／恢復上架（單篇與批次）與後台清單、狀態篩選、分頁
status: done
priority: P1
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-12T13:25:11Z
created_at: 2026-09-12T13:25:10Z
completed_at: 2026-09-12T14:01:52Z
branch: claude/article-publish-hide-settings-a87b8d
depends_on: []
scope:
  - apps/api/app/guides/publication.py
  - apps/api/app/guides/schemas.py
  - apps/api/app/guides/admin_service.py
  - apps/api/app/guides/router.py
  - apps/api/app/guides/service.py
  - apps/api/tests/test_guides.py
  - apps/web/components/admin-guides-panel.tsx
  - apps/web/components/admin-guides-panel.test.tsx
  - apps/web/components/admin-guides-list.tsx
  - apps/web/components/admin-guides-list.test.tsx
  - apps/web/lib/guides-admin.ts
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - docs/travel-guides.md
---

# 情報攻略文章的隱藏／恢復上架（單篇與批次）與後台清單、狀態篩選、分頁

## Why

站主要能「設定文章要不要發布或隱藏」，並且有一個管得動的後台。PR #398 的機制其實都在：每語系
publish／unpublish（原因＋確認＋版本鎖）、文章層級 `is_active`、`valid_until`。缺的是：

- `is_active` 藏在「儲存分類」的 PUT 裡，沒原因、沒確認、稽核記成 `guide_article_updated`，和撤下的規矩不一致。
- `GET /admin/guides` 只回 `articles`，沒有狀態、搜尋、分頁、總數；前端是一個 `<select>` 下拉，看不出哪篇已發布、
  哪篇被隱藏、哪些語言有版本。
- 沒有批次。

## Definition of done

- [x] `POST /admin/guides/{id}/hide|unhide` 與 `POST /admin/guides/batch`：要 `expected_version`（文章版本）、
      `confirmed`、`reason`；隱藏保留各語系 `published_version`，恢復時原本公開的語言一次回來；
      每篇一筆 `guide_article_hidden|unhidden` 稽核（批次帶 `batch_id`）；批次任一版本過期就整批不寫。
- [x] `ArticleUpdate` 不再接受 `is_active`；`ArticleSummary.status` 由 `publication.article_status` 算，
      SQL 端 `admin_status_expression` 同一套規則。
- [x] `GET /admin/guides` 支援 `status`／`q`／`page`／`limit`，回 `total`／`pages`／`facets`。
- [x] `/admin/guides` 變成清單（狀態 pill＋計數、型態／目的地／主題篩選、搜尋、分頁、五語系徽章、
      單篇與多選隱藏／恢復）→ 點列進編輯器（`?article=`），編輯器有返回清單與隱藏／恢復按鈕，
      分類表單不再有 `is_active` 勾選。
- [x] 五語系 `admin.json` 的 `guides` 新鍵齊全；`docs/travel-guides.md` 更新。

## Steps

- [x] API：`publication.py`（狀態）、`schemas.py`、`admin_service.py`（`set_visibility`／`batch_visibility`／
      `list_articles`）、`router.py`；`test_guides.py` 補齊（9 個新測試）。
- [x] Web：`lib/guides-admin.ts`、`admin-guides-list.tsx`（＋6 個測試）、`admin-guides-panel.tsx` 改成清單→編輯器
      （＋4 個測試）、五語系訊息目錄（新增 40 個鍵、移除 `active`／`archived`）。
- [x] 文件：`docs/travel-guides.md` 的 Publication／Endpoints／The reader's side／Still open。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_guides.py -q
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web -- admin-guides
```

手動：建立文章 → 發布 zh-TW → 清單「隱藏」（填原因勾確認）→ 前台文章頁變未提供、sitemap 沒它 →
「恢復上架」三處都回來、不用重新發布 → 勾兩篇批次隱藏 → 稽核各一筆同一 `batch_id`。

## Notes

- 不加 migration：「隱藏」就是 `guide_articles.is_active = false`，三個公開讀取面已經在讀它。
- 後台錯誤碼（`guide_article_already_hidden`、`guide_article_not_hidden`）不用進 `app/i18n.py`：
  `test_error_localization` 把路徑含 `admin` 的模組視為 operator surface。
- `docs/travel-guides.md` 當時在 `2026-09-12-affiliate-cta-guides-and-city-pages` 的 scope 裡（PR #431 收掉），claim 用了 `--force`。
