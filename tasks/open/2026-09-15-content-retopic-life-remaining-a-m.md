---
id: 2026-09-15-content-retopic-life-remaining-a-m
title: 生活分享無前綴文章重新分類（slug a–m）：審閱 retopic 提案並套用
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-09-15T13:57:26Z
completed_at:
branch:
depends_on:
  - 2026-09-15-guide-retopic-cli
scope:
  - apps/api/app/guides/content
---

# 生活分享無前綴文章重新分類（slug a–m）：審閱 retopic 提案並套用

## Why

retopic 對有明確前綴（ai-term-、claude-code-、codex-、gemini-、ai-news-、ai-search-、wordpress-、woocommerce-、chatgpt-）的文章已在 `guide-retopic-cli` 落地時套用；其餘約 275 篇無前綴的生活文章要由編輯逐篇看規則提案是否合理，再套用。這張只處理 slug 首字 a–m。

## Definition of done

- [ ] 每篇 a–m 的無前綴 life pack 都掛上至少一個子主題，或在 Notes 記下為何維持父主題。
- [ ] `pack_cli lint --kind life` 無新錯誤；`tests/test_guides_content_pack.py` 通過。

## Steps

- [ ] `pack_cli retopic --kind life --dry-run` 匯出表，篩 slug a–m 且無子主題者。
- [ ] 逐篇審閱，必要時手改 `topics`。
- [ ] 部署後 `guides-import --dry-run` 確認為 taxonomy update，再正式匯入。

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
```

## Notes

scope 是整個 content 目錄，claim 前確認沒有其他內容批次 in-progress；做的時候只碰 a–m 的檔案。
