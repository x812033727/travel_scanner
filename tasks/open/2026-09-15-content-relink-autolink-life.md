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
branch:
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
