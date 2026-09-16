---
id: 2026-09-15-content-relink-autolink-life
title: 生活分享全部內容包跑 relink 與 autolink（依前綴分批提交）
status: done
priority: P2
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-16T02:17:43Z
created_at: 2026-09-15T13:57:28Z
completed_at: 2026-09-16T06:08:56Z
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

- [x] 每個前綴批次：`relink --dry-run` → 審 → `--apply`；`autolink --dry-run` → 審 diff → `--apply`；lint 與連結測試綠。
- [x] `guides-import --slug … --dry-run` 顯示 update 後再 `--publish`。

## Steps

- [x] 依前綴分批（ai-term-、claude-code-、codex-、gemini-、其餘）各一個 commit。
- [x] 記錄轉換數與跳過的目標。

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

2026-09-16 第二、三批（claude-fable-5-1）：`gemini-` 73 篇：relink 轉 670 條、保留 60 條（教材 .zip 與 /guides 專區首頁，`not_an_article`）與 1 條自連（`gemini-guide`）；
autolink 52 篇加 81 條。其餘生活文章（`--kind life`，已做過的前綴為 no-op）：relink 498 篇轉 2,650 條、保留 230 條（全是 `not_an_article` 的 .zip／專區首頁）；
autolink 385 篇加 780 條。`claude-code-`／`codex-` 的站內連結本來就是型別化的（relink 0 條），只多了名詞連結。
三批合計：relink 3,637 條、autolink 1,081 條，`raw_internal_url` 警告清零。lint 0 error；`test_guides_content_links`／`content_pack`／`pack_ingest` 綠。
部署：`guides-import --dry-run` 應全列為 update → `--publish` → `guides-links-rebuild` → `guides-links-check --locale zh-TW`。
