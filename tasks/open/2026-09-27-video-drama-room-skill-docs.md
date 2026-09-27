---
id: 2026-09-27-video-drama-room-skill-docs
title: Video drama room skill docs: one drama route in the skill, and DRAMA, SERIES and AUTOMATION follow DRAMA-FLOW
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-27T06:16:03Z
completed_at:
branch:
depends_on:
  - 2026-09-27-video-drama-room-worker
  - 2026-09-27-video-drama-room-web
scope:
  - .agents/skills/youtube-video
  - .claude/skills/youtube-video
  - docs/videos/DRAMA.md
  - docs/videos/SERIES.md
  - docs/videos/AUTOMATION.md
---

# Video drama room skill docs: one drama route in the skill, and DRAMA, SERIES and AUTOMATION follow DRAMA-FLOW

## Why

流程改了（`docs/videos/DRAMA-FLOW.md`）：漫劇只有一條路，關卡是文件與劇本加四個自動關卡，站主可以討論。skill `youtube-video` 與三份設計文件要跟上，否則下一個代理照舊文件做。

## Definition of done

- [ ] `SKILL.md` 的路線表：「AI 漫劇」與「長篇漫劇」合成一列，關卡寫成「文件（故事聖經／設定集、總綱、細綱）、劇本」加自動的設定圖、旁白、分鏡、成片；`.claude/skills/youtube-video/SKILL.md` 同步（`tools/skills.test.mjs`）。
- [ ] `references/drama.md`：關卡清單、主幹表第 1 步改成故事聖經、第 3 步後加劇本關卡、拿掉單集的選大綱、指令加 `review-push --gate script`；`references/series.md`：流程每個核准點加「討論」。
- [ ] `DRAMA.md`、`SERIES.md`、`AUTOMATION.md` 照 DRAMA-FLOW.md §與既有文件的關係改（不重寫，各加一段並改關卡表）。

## Steps

- [ ] skill 兩份 reference 與 SKILL.md。
- [ ] 三份設計文件。

## How to verify

```bash
npm run test:tools
```

## Notes

- 等 worker 與 web 落地再寫，才寫得出實際的指令與頁面名稱。
