---
id: 2026-10-19-curio-s-axis-third-batch-s29
title: Curio S axis third batch: S29 Cao Chong weighs the elephant, S14 Musashi at Ganryujima, S26 let them eat cake
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-history-stories
claimed_at: 2026-10-19T22:13:18Z
created_at: 2026-10-19T22:13:17Z
completed_at:
branch: claude/curio-s-batch2
depends_on: []
scope:
  - docs/videos/curio-s29
  - docs/videos/curio-s14
  - docs/videos/curio-s26
  - docs/videos/history-curiosity/topic-checks/S29.md
  - docs/videos/history-curiosity/topic-checks/S14.md
  - docs/videos/history-curiosity/topic-checks/S26.md
---

# Curio S axis third batch: S29 Cao Chong weighs the elephant, S14 Musashi at Ganryujima, S26 let them eat cake

## Why

站主 2026-10-19：「繼續新集數，用推薦的選擇就好不用問我，有額度就一直做下去吧」。第二批（S03、S11、S34，票
`2026-10-19-curio-s-axis-second-batch-s03`）稿子已合併、旁白與插圖已送站主。第三批照樣一區一集：S29「曹沖稱象，可能來自
一部佛經？」（中國）、S14「宮本武藏在巖流島真的故意遲到？」（日本）、S26「『沒有麵包就吃蛋糕』，瑪麗皇后真的說過嗎？」（歐洲）。
選題理由：原文開得到（《三國志》鄧哀王沖傳在殆知閣、《雜寶藏經》在 CBETA、《二天記》《五輪書》在國會圖書館或青空文庫、
盧梭《懺悔錄》在 Project Gutenberg）。

## Definition of done

- [ ] 三題各有 `topic-checks/<id>.md`（研究加獨立覆核）。
- [ ] 三集稿子選 A 案、`loops` 至少 8 個、盲評全過、lint 0 錯誤、`claims.md`、`verify-1.md`，開 PR。
- [ ] 旁白、配樂、插圖做完並 `review-push` 給站主。

## Steps

- [ ] 查核先做（研究代理＋獨立覆核代理），再寫稿。
- [ ] 每完成一段就開 PR（站主：額度用完前記得開 PR）。

## How to verify

`node tools/video/cli.mjs lint --slug curio-s29`（及 s14、s26）0 錯誤；`status --slug` 看關卡。

## Notes

- 同一集的 tts、check-audio、keyframes 不能同時跑（skill〈在雲端環境做旁白與插圖〉）。
