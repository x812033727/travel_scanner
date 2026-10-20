---
id: 2026-10-20-curio-s-axis-ninth-batch-s07
title: "Curio S axis ninth batch: S07 Changban bridge, S15 Date Masamune in white, S19 Eiffel Tower in 1909"
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-history-stories
claimed_at: 2026-10-20T20:54:34Z
created_at: 2026-10-20T21:00:00Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s07
  - docs/videos/curio-s15
  - docs/videos/curio-s19
  - docs/videos/history-curiosity/topic-checks/S07.md
  - docs/videos/history-curiosity/topic-checks/S15.md
  - docs/videos/history-curiosity/topic-checks/S19.md
---

# Curio S axis ninth batch: S07 Changban bridge, S15 Date Masamune in white, S19 Eiffel Tower in 1909

## Why

延續站主 2026-10-19「用推薦的選擇就好不用問我，有額度就一直做下去吧」與 2026-10-20「繼續新增新集數」。第八批（S31、S16、S21，
票 `2026-10-20-curio-s-axis-eighth-batch-s31`）已完成稿子、旁白與插圖。第九批照樣一區一集：S07「長坂橋一聲吼，史書真的有寫？」（中國，
這次是「演義沒誇張」的反向題）、S15「伊達政宗為什麼穿著壽衣去見秀吉？」（日本）、S19「艾菲爾鐵塔差點在 1909 年被拆？」（歐洲）。
選題理由：原文開得到（《三國志．張飛傳》與毛本《三國演義》第四十二回在維基文庫；《貞山公治家記録》等在國會圖書館；1887 年〈藝術家抗議書〉
與鐵塔特許合約、無線電史料在 Gallica 與 archive.org）。

## Definition of done

- [x] 三題各有 `topic-checks/<id>.md`（研究加獨立覆核）。
- [x] 三集稿子 `loops` 至少 8 個、盲評全過、lint 0 錯誤、`claims.md`、`verify-1.md`，開 PR。
- [ ] 旁白、配樂、插圖做完並 `review-push` 給站主。

## Steps

- [x] 查核先做（研究代理＋獨立覆核代理），再寫稿。
- [x] 盲評照前幾批的教訓：結論只講一次，第二次提到一律點名回呼並補新事實。
- [ ] 本月 music 預算已用完：配樂等站主調高預算或下個月再補（同第七、八批）。

## 進度（2026-10-21）

- 三題查核（研究＋獨立覆核）都做完：S07 45 列（覆核推翻第 17 列胡三省音注的推論）、S15 43 列（找不到 1590 年白衣的記載，本次查到最早是 1934 年通俗書；YouTube 標題改問「真的穿著壽衣去見秀吉嗎？」）、S19 40 列（1909 年沒有拆塔的計畫，到期的只是經營權）。
- 三集稿子盲評全過（S07 一輪、S19 三輪、S15 三輪），lint 0／0；旁白錄好並跑過 `check-audio`（S07 10:07、S19 9:42、S15 10:06），重錄過明顯讀錯的句子，剩下的旗標多是日文人名與同音字的轉寫誤差。
- 卡住：插圖。`keyframes --slug curio-s07` 回「本月的 judge 次數預算（20000 次）用完了」。配樂也一樣沒額度（本月 music 60 tracks 用完）。
  站主在 `/admin/videos` 設定分頁調高 judge 與 music 預算後，對三集各跑
  `node tools/video/cli.mjs keyframes --slug curio-<id> --takes 3`、`music --slug curio-<id>`，再 `review-push --gate audio` 與 `--gate storyboard`。
