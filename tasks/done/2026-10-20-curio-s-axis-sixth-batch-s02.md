---
id: 2026-10-20-curio-s-axis-sixth-batch-s02
title: "Curio S axis sixth batch: S02 the borrowed arrows, S13 Sanada Yukimura, S27 horned Viking helmets"
status: done
priority: P2
area: docs
owner: claude-opus-5-5-history-stories
claimed_at: 2026-10-20T06:03:17Z
created_at: 2026-10-20T06:00:00Z
completed_at: 2026-10-20T20:27:51Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s02
  - docs/videos/curio-s13
  - docs/videos/curio-s27
  - docs/videos/history-curiosity/topic-checks/S02.md
  - docs/videos/history-curiosity/topic-checks/S13.md
  - docs/videos/history-curiosity/topic-checks/S27.md
---

# Curio S axis sixth batch: S02 the borrowed arrows, S13 Sanada Yukimura, S27 horned Viking helmets

## Why

站主 2026-10-20 第二次說「繼續新增新集數」（延續 2026-10-19「用推薦的選擇就好不用問我，有額度就一直做下去吧」）。第五批（S30、S24、S17，
票 `2026-10-20-curio-s-axis-fifth-batch-s30`）稿子已過盲評、旁白在錄。第六批照樣一區一集：S02「草船借箭，其實不是諸葛亮？」（中國）、
S13「真田幸村，其實從沒叫過『幸村』？」（日本）、S27「維京人的頭盔，為什麼沒有角？」（歐洲）。
選題理由：原文開得到（《三國志．吳主傳》裴注引《魏略》在殆知閣；真田信繁書狀與《難波戰記》等軍記在國會圖書館；
Gjermundbu 頭盔與 1876 年拜魯特首演服裝設計的資料在博物館與 Wikimedia）。

## Definition of done

- [x] 三題各有 `topic-checks/<id>.md`（研究加獨立覆核）。
- [x] 三集稿子 `loops` 至少 8 個、盲評全過、lint 0 錯誤、`claims.md`、`verify-1.md`，開 PR。
- [x] 旁白、配樂、插圖做完並 `review-push` 給站主。

## Steps

- [x] 查核先做（研究代理＋獨立覆核代理），再寫稿。
- [x] 每完成一段就開 PR（站主：額度用完前記得開 PR）。

## How to verify

`node tools/video/cli.mjs lint --slug curio-s02`（及 s13、s27）0 錯誤；`status --slug` 看關卡。

## Notes

- 前幾批的教訓見票 `2026-10-19-curio-s-axis-third-batch-s29`、`2026-10-20-curio-s-axis-fourth-batch-s28`、
  `2026-10-20-curio-s-axis-fifth-batch-s30` 的 Notes（一次只跑一集 keyframes、念錯字用 `say`、不畫小孩與裸體、招牌黑板會被畫上字、
  盲評最常卡 no_recap／no_detour／chapters_link，判定只講一次）。
- 成片要先裝品牌素材包，否則沒有片頭片尾。
