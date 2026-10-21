---
id: 2026-10-20-curio-s-axis-seventh-batch-s06
title: "Curio S axis seventh batch: S06 bone scraping, S12 Sekigahara's warning shot, S20 the stolen Mona Lisa"
status: done
priority: P2
area: docs
owner: claude-opus-5-5-history-stories
claimed_at: 2026-10-20T08:12:51Z
created_at: 2026-10-20T08:15:00Z
completed_at: 2026-10-21T02:19:35Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s06
  - docs/videos/curio-s12
  - docs/videos/curio-s20
  - docs/videos/history-curiosity/topic-checks/S06.md
  - docs/videos/history-curiosity/topic-checks/S12.md
  - docs/videos/history-curiosity/topic-checks/S20.md
---

# Curio S axis seventh batch: S06 bone scraping, S12 Sekigahara's warning shot, S20 the stolen Mona Lisa

## Why

站主 2026-10-20 第三次說「繼續新增新集數」（延續 2026-10-19「用推薦的選擇就好不用問我，有額度就一直做下去吧」）。第六批（S02、S13、S27，
票 `2026-10-20-curio-s-axis-sixth-batch-s02`）稿子已過盲評、旁白已錄。第七批照樣一區一集：S06「刮骨療毒是真的，醫生卻不是華佗？」（中國）、
S12「關原之戰，家康真的開槍逼小早川倒戈？」（日本）、S20「蒙娜麗莎被偷的那兩年，警察問過畢卡索？」（歐洲）。
選題理由：原文開得到（《三國志．關羽傳》與《華佗傳》在殆知閣與維基文庫；關原相關的軍記與一次史料在國會圖書館數位典藏；
1911–1913 年的法國報紙在 Gallica）。S35（寄小孩）不選：系列不畫兒童。

## Definition of done

- [x] 三題各有 `topic-checks/<id>.md`（研究加獨立覆核）。
- [x] 三集稿子 `loops` 至少 8 個、盲評全過、lint 0 錯誤、`claims.md`、`verify-1.md`，開 PR。
- [x] 旁白、配樂、插圖做完並 `review-push` 給站主。

## Steps

- [x] 查核先做（研究代理＋獨立覆核代理），再寫稿。
- [x] 盲評照 S02、S13、S27 的教訓：結論只講一次，第二次提到一律點名回呼並補新事實。

## 進度（2026-10-20）

- 三題查核（研究＋獨立覆核）、三集稿子（盲評全過、lint 0／0）、旁白、插圖都做完，旁白與分鏡已 `review-push`。
- 剩下：S20 沒有配樂（S06、S12 有）。本月 music 預算（60 tracks）用完，`music --slug` 回「本月的music預算不夠」。
  站主在 `/admin/videos` 設定分頁調高預算，或下個月，再對這幾集跑 `node tools/video/cli.mjs music --slug curio-<id>`，然後重送 `review-push --gate audio`。

## 收尾（2026-10-21）

- 站主調高 judge 與 music 預算後補齊：缺配樂的集數已跑 `music` 並重送 `review-push --gate audio`；第九批三集的插圖畫完（S07 77 張、S15 78 張、S19 68 張；S19 有三句提示詞因背景太寫實、時鐘有數字而改寫），分鏡已送審。
- 第九批每集花費：S07 US$1.25、S15 US$1.35、S19 US$1.34。
