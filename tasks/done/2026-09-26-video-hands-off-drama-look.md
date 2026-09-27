---
id: 2026-09-26-video-hands-off-drama-look
title: 影片交給 AI 決定：漫劇設定圖依 judge 分數自動選
status: done
priority: P3
area: tools
owner: claude-fable-5-1-video-drama
claimed_at: 2026-09-26T22:49:41Z
created_at: 2026-09-26T16:18:48Z
completed_at: 2026-09-26T22:53:06Z
branch: claude/video-hands-off-drama-look
depends_on:
  - 2026-09-26-video-hands-off-settings
scope:
  - apps/api/app/video_automation/settings.py
  - apps/api/app/video_reviews/admin_service.py
  - tools/video/review/sync.mjs
---

# 影片交給 AI 決定：漫劇設定圖依 judge 分數自動選

## Why

漫劇每個角色都要站主挑一張設定圖（`look` 關卡）。`look` 階段已經用 judge 評分，並標出分數最高的 `suggested`。站主希望所有決定都交給 AI（`docs/videos/HANDS-OFF.md` §漫劇的設定圖），所以這一關也可以依分數自動選。

## Definition of done

- [x] 規則 `look_pick_passed(payload, min_score)`：`suggested` 那張的分數達到 `judge_min_score`，而且沒有列出問題，就核准這個角色的 `look` 審核，`choice` 用 `suggested`。
- [x] 只有 `auto_pick_look`（settings 票加的開關，預設關）開著時才生效。
- [x] 備註寫出分數，並寫稽核紀錄。
- [x] 加上測試。

## Steps

- [x] 開工前用 `node .agents/skills/task-board/scripts/who-is-on-it.mjs --scope tools/video/media` 查漫劇那條線誰在做，先協調。
- [x] 規則與 `submit_review` 接上；送審的 payload 如果少了分數，在 `tools/video/review/sync.mjs` 補上。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_reviews.py -q
npm run test:tools
```

## Notes

- 預設關閉，理由和 `auto_approve_storyboard` 一樣：第一支漫劇要由站主看過。
- 2026-09-27（claude-fable-5-1-video-drama）：做完。漫劇那條線就是這個 session 自己（#795–#824），不用另外協調。`tools/video/review/sync.mjs` 不用改：`lookSubmissions` 送的 payload 本來就有每張的 `judge.overall`／`problems` 與 `suggested`，`recordLook` 拉回時用 `choice` 的字母算出張數，伺服器填 `choice = suggested` 就接得上。規則 `look_pick_passed(payload, min_score)` 與 `auto_picks_look` 在 `settings.py`，`submit_review` 的接點在 `admin_service.py`，備註像「judge 給 B 8/10、沒有列出問題，依設定自動選」。疊在 judge（#832）與 settings（#830）之上。
