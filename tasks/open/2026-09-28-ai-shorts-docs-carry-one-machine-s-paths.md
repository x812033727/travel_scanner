---
id: 2026-09-28-ai-shorts-docs-carry-one-machine-s-paths
title: The AI Shorts documents carry one machine's paths
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-09-28T04:26:00Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/ai-shorts/README.md
  - docs/videos/ai-shorts/campaign/README.md
  - docs/videos/ai-shorts/delivery-2026-09-28.md
  - docs/videos/ai-shorts/delivery-2026-09-28.json
---

# The AI Shorts documents carry one machine's paths

## Why

repo 是公開的。PR #871 的四份文件裡寫著這台開發機的絕對路徑（使用者資料夾底下的工作區）：

- `docs/videos/ai-shorts/README.md` 的指令範例（`--workdir`、`--dir`）。
- `docs/videos/ai-shorts/campaign/README.md` 的指令範例。
- `docs/videos/ai-shorts/delivery-2026-09-28.md` 的三個 MP4 連結（點了只在這台電腦上有用）。
- `docs/videos/ai-shorts/delivery-2026-09-28.json` 的成片目錄、聯絡表與日誌路徑。

skill 的檢查（`tools/skills.test.mjs`）只擋 skill 裡的本機路徑，文件沒有人擋。路徑本身不是機密，但它把本機的帳號名稱寫進公開的 repo，而且別的機器照抄指令會失敗。

2026-09-28 規劃 Shorts 區時發現的。

## Definition of done

- [ ] 兩份 README 的指令範例改用佔位的寫法（例如 `<工作區>/shorts`），並說明工作區要在 repo 外。
- [ ] 交付收據（`.md` 與 `.json`）的路徑改成相對於工作區的路徑；檔案的 SHA-256 不變。收據是歷史紀錄：只改路徑的前綴，其餘一字不動，並在檔案開頭註明改過什麼。
- [ ] `git grep -n "Users/" docs/videos/ai-shorts` 沒有結果。

## Steps

- [ ] 改四個檔。
- [ ] 跑 Shorts 的測試，確認沒有測試綁著這幾個檔的雜湊。

## How to verify

```bash
git grep -n "Users/" docs/videos/ai-shorts
node --test tools/video/shorts/*.test.mjs
```

## Notes

- `tools/video/shorts/core.test.mjs` 綁的是 `pilots/*.json` 與 `experiments/*` 的雜湊，不含這四個檔；動手前再確認一次。
- 要不要順便把「文件裡不能有本機路徑」做成檢查，另外討論；這張票只改現有的四個檔。
