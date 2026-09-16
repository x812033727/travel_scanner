---
id: 2026-09-15-content-relink-autolink-life
title: 生活分享全部內容包跑 relink 與 autolink（依前綴分批提交）
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-15T13:57:28Z
completed_at:
branch: claude/travel-article-structure-search-sr9jiq
depends_on:
  - 2026-09-15-pack-autolink-and-relink-cli
scope:
  - apps/api/app/guides/content
---

# 生活分享全部內容包跑 relink 與 autolink（依前綴分批提交）

## Why

把 3,634 條指向 /life 的原始 URL 轉成型別化連結，並為名詞加上第一處出現的自動連結。

## Definition of done

- [ ] 每個前綴批次：`relink --dry-run` → 審 → `--apply`；`autolink --dry-run` → 審 diff → `--apply`；lint 與連結測試綠。
- [ ] `guides-import --slug … --dry-run` 顯示 update 後再 `--publish`。

## Steps

- [ ] 依前綴分批（ai-term-、claude-code-、codex-、gemini-、其餘）各一個 commit。
- [ ] 記錄轉換數與跳過的目標。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_content_links.py tests/test_guides_content_pack.py -q
```

## Notes

claim 時整個 content 目錄會被鎖，做完立刻 release／review。

2026-09-16 第一批（claude-fable-5-1，commit「content(life): 第一批 relink＋autolink：ai-term-／ai-search- 89 篇」）：
`relink --prefix ai-term- --prefix ai-search- --apply` 轉 317 條、保留 0 條；`autolink` 同前綴 85 篇加 220 條。lint 無 error、連結 kind 測試綠。
剩餘前綴（`claude-code-`、`codex-`、`gemini-`、其餘）各自：`relink --dry-run` → 審 → `--apply`；`autolink --dry-run` → 審 diff → `--apply`；一個 commit。
全庫尚可轉 3,710 條（4,027 − 317）。部署時記得 `guides-import --slug …` 後 `guides-links-rebuild`。
