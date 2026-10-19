---
id: 2026-10-19-curio-s-axis-second-batch-s03
title: Curio S axis second batch: S03 empty fort, S11 Nagashino volleys, S34 Endurance
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-history-stories
claimed_at: 2026-10-19T17:53:36Z
created_at: 2026-10-19T17:53:31Z
completed_at:
branch: claude/curio-s-batch2
depends_on: []
scope:
  - docs/videos/curio-s03
  - docs/videos/curio-s11
  - docs/videos/curio-s34
  - docs/videos/history-curiosity/topic-checks/S03.md
  - docs/videos/history-curiosity/topic-checks/S11.md
  - docs/videos/history-curiosity/topic-checks/S34.md
---

# Curio S axis second batch: S03 empty fort, S11 Nagashino volleys, S34 Endurance

## Why

S 軸試片三集（S01、S09、S18，票 `2026-10-18-curio-s-axis-pilot-s01-red`）成片已交站主看。站主 2026-10-19：
「繼續新集數，用推薦的選擇就好不用問我，有額度就一直做下去吧，額度用完前記得開 pr」。第二批照試片一區一集：
S03「空城計那天，司馬懿根本不在那裡？」（中國）、S11「長篠之戰的『三段擊』存在嗎？」（日本）、
S34「南極困了兩年，28 個人怎麼全部活著回來？」（歐洲探險）。選題理由：三題的原文都開得到（《三國志》裴注在
GitHub 殆知閣、《信長公記》在 ja.wikisource、甫庵《信長記》在國會圖書館、薛克頓《South》在 Project Gutenberg）。

## Definition of done

- [ ] 三題各有 `topic-checks/<id>.md`（研究加獨立覆核），通過的題目在 `topics.json` 改 `checked`。
- [ ] 三集照 `curio-episode` skill 做：大綱（選建議案）、稿子有 `loops` 表、盲評全過、lint 0 錯誤、`claims.md`、`verify-1.md`。
- [ ] 旁白、配樂、插圖（每集約 US$2）做完，`review-push` 旁白與分鏡給站主；站主核准後成片、品管、`review-push --gate final`。

## Steps

- [ ] 查核先做（研究代理＋獨立覆核代理），再寫大綱與稿子，避免像試片那樣查核後大改。
- [ ] 每一集稿子與查核完成就開 PR（站主：額度用完前記得開 PR）。
- [ ] 旁白、插圖做完再一個 PR（改過的句子與提示詞）。

## How to verify

`node tools/video/cli.mjs lint --slug curio-s03`（及 s11、s34）0 錯誤；`status --slug` 看關卡。

## Notes

- `topics.json` 的狀態改動在試片票的 scope 裡（同一個 owner）；這張票不另外宣告。
