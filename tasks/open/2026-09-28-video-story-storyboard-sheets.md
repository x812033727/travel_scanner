---
id: 2026-09-28-video-story-storyboard-sheets
title: 超過 47 鏡的分鏡送審改送聯絡表
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-09-28T03:31:11Z
completed_at:
branch:
depends_on:
  - 2026-09-28-video-story-design-docs
scope:
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
---

# 超過 47 鏡的分鏡送審改送聯絡表

## Why

一支品牌故事有 85–100 個鏡頭（`docs/videos/STORY.md`）。分鏡關卡送審時，`storyboardSubmission`（`tools/video/review/sync.mjs`）每個鏡頭上傳一個檔，而一筆審核最多 48 個檔（`apps/api/app/video_reviews/schemas.py` 的 `MAX_REVIEW_FILES`）。超過 47 鏡的影片永遠送不出分鏡，整支卡住。

## Definition of done

- [ ] 鏡頭數在上限以內時，送審內容與現在完全相同。
- [ ] 超過上限時，送審改成：分頁的聯絡表（每頁最多 24 格）加上所有標成待修（`needs_review`）的鏡頭；payload 仍列出每個鏡頭的 id、judge 分數與是否待修，審核卡看得到全貌。
- [ ] 95 鏡的測試案例送得出去，檔案數不超過 48。

## Steps

- [ ] `sync.mjs`：依鏡頭數選擇送法；聯絡表分頁。
- [ ] 測試：47 鏡、48 鏡、95 鏡三個案例。
- [ ] 確認後台審核卡在缺少單鏡檔案時照常顯示（`apps/web/components/admin-video-review-card.tsx` 已容忍缺檔，這張票不改 web）。

## How to verify

```bash
node --test tools/video/review
npm run test:tools
```

## Notes

- 聯絡表由 `keyframes` 階段產生（`drawContactSheet`）；分頁如果要改 `tools/video/media`，另開票，不要擴 scope。
- PR #870 也改了 `sync.mjs`（約 90 行），合併順序誰後誰 rebase。
