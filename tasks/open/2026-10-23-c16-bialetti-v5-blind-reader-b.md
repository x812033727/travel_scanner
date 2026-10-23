---
id: 2026-10-23-c16-bialetti-v5-blind-reader-b
title: Review C16 Bialetti v5 narration blind as reader B
status: in-progress
priority: P1
area: docs
owner: codex-c16-v5-blind-reader-b
claimed_at: 2026-10-23T06:41:54Z
created_at: 2026-10-23T06:41:48Z
completed_at:
branch: codex/c16-bialetti-v5-blind-reader-b-20261023
depends_on: []
scope:
  - docs/videos/story-everyday-bialetti-c16/reviews/narrative-blind-v5-reader-b.md
---

# Review C16 Bialetti v5 narration blind as reader B

## Why

C16 Bialetti v5 已有作者稿，但腳本核准前需要兩位互不接觸的純旁白讀者。讀者 B 只拿到 81 行 ID／旁白投影；本 task 保存固定 v5 commit 的獨立判定，不能沿用舊稿收據。

## Definition of done

- [x] 固定作者 commit、腳本 Git blob／SHA-256、旁白投影 SHA-256，證明 81 行同序同文。
- [x] 交出正式 12 個必答題與可選章名題的逐 ID PASS／HOLD 收據，區分真實 TTS 與紙上篇幅。
- [x] 草稿 PR 保存本收據，與作者檔案隔離，不合併。

## Steps

- [x] 先只讀旁白投影並鎖定整體 HOLD，之後才讀倉庫規則和作者 metadata。
- [x] 從指定作者 commit 建立獨立 sparse Git worktree，撰寫 `reviews/narrative-blind-v5-reader-b.md`。
- [ ] 推送審稿分支並建立不自動合併的草稿 PR。

## How to verify

`git show f285754f1c227b5238ef92d92d56323a95a340bc:docs/videos/story-everyday-bialetti-c16/script.md` 取固定 bytes，Python `hashlib.sha256` 與 81 列 Markdown 表格／純旁白投影逐 ID 比對；`npm run check:tasks`、`git diff --check`、`gh pr view --json isDraft,baseRefName,headRefName,autoMergeRequest`。

## Notes

投影 SHA-256 `48ABACBA12A05BA0889951ACE204B7DCCC5271F2235EEE3978A2C69B3B2D5072`；作者腳本 SHA-256 `2620912D8337CFE69BBA4EAF9F19139BF2AA9C69B1E8680560B5FADBD74E6091`。正式面板 6 PASS／6 HOLD，整體 HOLD；紙上至少八分鐘可行，真實 TTS 未測。作者的 PR #1704 會繼續修訂，這份收據只綁 v5 固定 commit。
