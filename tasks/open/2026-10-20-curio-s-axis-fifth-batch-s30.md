---
id: 2026-10-20-curio-s-axis-fifth-batch-s30
title: "Curio S axis fifth batch: S30 Xuanzang left illegally, S17 the cuckoo haiku, S24 Archimedes and Eureka"
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-history-stories
claimed_at: 2026-10-20T04:26:00Z
created_at: 2026-10-20T04:30:00Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s30
  - docs/videos/curio-s17
  - docs/videos/curio-s24
  - docs/videos/history-curiosity/topic-checks/S30.md
  - docs/videos/history-curiosity/topic-checks/S17.md
  - docs/videos/history-curiosity/topic-checks/S24.md
---

# Curio S axis fifth batch: S30 Xuanzang left illegally, S17 the cuckoo haiku, S24 Archimedes and Eureka

## Why

站主 2026-10-20：「繼續新增新集數」（延續 2026-10-19「用推薦的選擇就好不用問我，有額度就一直做下去吧」）。第四批（S28、S10、S25，票
`2026-10-20-curio-s-axis-fourth-batch-s28`）旁白已錄、插圖在畫。第五批照樣一區一集：S30「唐朝最有名的和尚，是偷渡出國的？」（中國）、
S17「三英傑的杜鵑俳句，為什麼沒有一首是他們寫的？」（日本）、S24「阿基米德真的光著身子跑上街喊 Eureka？」（歐洲）。
選題理由：原文開得到（《大慈恩寺三藏法師傳》《大唐西域記》在 CBETA；松浦靜山《甲子夜話》在國會圖書館；維特魯威《建築十書》
在 Wikisource／Gutenberg／Perseus）。

## Definition of done

- [ ] 三題各有 `topic-checks/<id>.md`（研究加獨立覆核）。
- [ ] 三集稿子 `loops` 至少 8 個、盲評全過、lint 0 錯誤、`claims.md`、`verify-1.md`，開 PR。
- [ ] 旁白、配樂、插圖做完並 `review-push` 給站主。

## Steps

- [ ] 查核先做（研究代理＋獨立覆核代理），再寫稿。
- [ ] 每完成一段就開 PR（站主：額度用完前記得開 PR）。

## How to verify

`node tools/video/cli.mjs lint --slug curio-s30`（及 s17、s24）0 錯誤；`status --slug` 看關卡。

## Notes

- 前幾批的教訓見票 `2026-10-19-curio-s-axis-third-batch-s29` 與 `2026-10-20-curio-s-axis-fourth-batch-s28` 的 Notes
  （一次只跑一集 keyframes、念錯字用 `say`、不畫小孩、招牌黑板會被畫上字、盲評最常卡 no_recap／chapters_link／no_detour）。
- 成片要先裝品牌素材包，否則沒有片頭片尾。
