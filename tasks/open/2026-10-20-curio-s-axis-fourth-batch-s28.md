---
id: 2026-10-20-curio-s-axis-fourth-batch-s28
title: "Curio S axis fourth batch: S28 Sima Guang and the vat, S10 the enemy is at Honno-ji, S25 Newton's apple"
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-history-stories
claimed_at: 2026-10-20T02:12:53Z
created_at: 2026-10-20T02:12:32Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s28
  - docs/videos/curio-s10
  - docs/videos/curio-s25
  - docs/videos/history-curiosity/topic-checks/S28.md
  - docs/videos/history-curiosity/topic-checks/S10.md
  - docs/videos/history-curiosity/topic-checks/S25.md
---

# Curio S axis fourth batch: S28 Sima Guang and the vat, S10 the enemy is at Honno-ji, S25 Newton's apple

## Why

站主 2026-10-19：「繼續新集數，用推薦的選擇就好不用問我，有額度就一直做下去吧」。第三批（S29、S26、S14，票
`2026-10-19-curio-s-axis-third-batch-s29`）旁白與分鏡已送站主。第四批照樣一區一集：S28「司馬光砸的，真的是缸嗎？」（中國）、
S10「『敵在本能寺』這句話，是誰寫的？」（日本）、S25「牛頓的蘋果是真的，那它有打到頭嗎？」（歐洲）。
選題理由：原文開得到（《宋史．司馬光傳》與宋人筆記在殆知閣；賴山陽《日本外史》、《信長公記》、《明智軍記》在國會圖書館；
Stukeley 的《牛頓爵士生平回憶》手稿與 Conduitt 筆記在英國皇家學會與 Newton Project）。

## Definition of done

- [ ] 三題各有 `topic-checks/<id>.md`（研究加獨立覆核）。
- [ ] 三集稿子 `loops` 至少 8 個、盲評全過、lint 0 錯誤、`claims.md`、`verify-1.md`，開 PR。
- [ ] 旁白、配樂、插圖做完並 `review-push` 給站主。

## Steps

- [ ] 查核先做（研究代理＋獨立覆核代理），再寫稿。
- [ ] 每完成一段就開 PR（站主：額度用完前記得開 PR）。

## How to verify

`node tools/video/cli.mjs lint --slug curio-s28`（及 s10、s25）0 錯誤；`status --slug` 看關卡。

## Notes

- 第三批的教訓見票 `2026-10-19-curio-s-axis-third-batch-s29` 的 Notes（一次只跑一集 keyframes、念錯字用 `say`、
  不畫小孩、招牌黑板會被畫上字）。
- 成片要先裝品牌素材包，否則沒有片頭片尾（同一張票的 Notes）。
