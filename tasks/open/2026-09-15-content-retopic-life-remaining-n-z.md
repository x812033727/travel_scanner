---
id: 2026-09-15-content-retopic-life-remaining-n-z
title: 生活分享無前綴文章重新分類（slug n–z）：審閱 retopic 提案並套用
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

# 生活分享無前綴文章重新分類（slug n–z）：審閱 retopic 提案並套用

## Why

同 `content-retopic-life-remaining-a-m`，這張處理 slug 首字 n–z。

## Definition of done

- [ ] 每篇 n–z 的無前綴 life pack 都掛上至少一個子主題，或在 Notes 記下為何維持父主題。
- [ ] lint 與內容包測試通過。

## Steps

- [ ] `pack_cli retopic --kind life --dry-run` 匯出表，篩 slug n–z。
- [ ] 逐篇審閱後套用。
- [ ] 部署後匯入。

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
```

## Notes

與 a–m 那張不可同時 in-progress（scope 相同）。
