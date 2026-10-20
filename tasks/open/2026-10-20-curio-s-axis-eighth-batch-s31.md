---
id: 2026-10-20-curio-s-axis-eighth-batch-s31
title: "Curio S axis eighth batch: S31 Yang Guifei's lychees, S16 Sunomata one-night castle, S21 tulip mania"
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-history-stories
claimed_at: 2026-10-20T08:35:16Z
created_at: 2026-10-20T08:40:00Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s31
  - docs/videos/curio-s16
  - docs/videos/curio-s21
  - docs/videos/history-curiosity/topic-checks/S31.md
  - docs/videos/history-curiosity/topic-checks/S16.md
  - docs/videos/history-curiosity/topic-checks/S21.md
---

# Curio S axis eighth batch: S31 Yang Guifei's lychees, S16 Sunomata one-night castle, S21 tulip mania

## Why

站主 2026-10-20 第四次說「繼續新增新集數」（延續 2026-10-19「用推薦的選擇就好不用問我，有額度就一直做下去吧」）。第七批（S06、S12、S20，
票 `2026-10-20-curio-s-axis-seventh-batch-s06`）查核進行中。第八批照樣一區一集：S31「楊貴妃的荔枝，怎麼送到長安？」（中國）、
S16「墨俁一夜城，一夜蓋得起來嗎？」（日本）、S21「鬱金香狂熱，其實沒那麼瘋？」（歐洲）。
選題理由：原文開得到（《新唐書．楊貴妃傳》、《唐國史補》、杜牧詩與蘇軾等宋人的爭論在維基文庫；墨俁築城的《武功夜話》與《太閤記》在國會圖書館；
1637 年的鬱金香小冊子與 Anne Goldgar 的研究摘要可在網上讀到）。

## Definition of done

- [x] 三題各有 `topic-checks/<id>.md`（研究加獨立覆核）。
- [x] 三集稿子 `loops` 至少 8 個、盲評全過、lint 0 錯誤、`claims.md`、`verify-1.md`，開 PR。
- [ ] 旁白、配樂、插圖做完並 `review-push` 給站主。

## Steps

- [x] 查核先做（研究代理＋獨立覆核代理），再寫稿。
- [x] 盲評照前幾批的教訓：結論只講一次，第二次提到一律點名回呼並補新事實。

## 進度（2026-10-20）

- 三題查核（研究＋獨立覆核）、三集稿子（盲評全過、lint 0／0）、旁白、插圖都做完，旁白與分鏡已 `review-push`。
- 剩下：S20、S16、S31 沒有配樂。本月 music 預算（60 tracks）用完，`music --slug` 回「本月的music預算不夠」。
  站主在 `/admin/videos` 設定分頁調高預算，或下個月，再對這幾集跑 `node tools/video/cli.mjs music --slug curio-<id>`，然後重送 `review-push --gate audio`。
