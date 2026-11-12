---
id: 2026-11-12-p04-microgravity-flame
title: 原來如此事務所 P04：太空人一直在掉，火焰為什麼也變了？
status: in-progress
priority: P2
area: docs
owner: claude-opus-5.5-p06-p18-handoff
claimed_at: 2026-11-12T11:27:45Z
created_at: 2026-11-12T11:27:29Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/sothatswhy-p04-microgravity-flame
---

# 原來如此事務所 P04：太空人一直在掉，火焰為什麼也變了？

## Why

站主 2026-11-12「繼續做新的」。P04 是素材池第二輪（`docs/videos/so-thats-why/pool/reviews/material-20261111-round2.md`，P52-008～010）補到來源、非作者覆核判可成題的一集。企劃 `docs/videos/so-thats-why/refresh-20261101/EPISODES.md#p04`：先建立共同自由落體，再把同一條件套到氣體與火焰，約 11 分（10–12）。缺：「為什麼冷焰只在微重力下看得到」的來源；不能說所有微重力火焰都同一形狀或顏色；插畫標示意，不假造太空實驗。

照 P13／P29 的流程與 2026-11-12 的規則：對話版、偏快語速（≥ 4.3）、8 分鐘下限不硬寫、亮底縮圖選半身鏡頭且九語字量過不碰人、空間不足先完全備份再刪；**八語配音照 PR #2085 改用 MiniMax 各語言聲音**（站主「P29 之後參考 PR2085」，zh-TW 旁白維持 Gemini）。

## Definition of done

- [ ] 稿子：獨立查核、盲評必過題全過、lint 0 錯誤，依站主授權核准。
- [ ] 旁白、check-audio（語速 ≥ 4.3），核准；設定圖沿用系列。
- [ ] 插圖、放大檢查、分鏡評分 ≥ 49／70，核准。
- [ ] 合成、qa 11 項、`silent_share` ≤ 3%、成片送站主。
- [ ] 八語（MiniMax 配音、縮圖字不碰人）、上架包，站主核准；YouTube 網址記下後結案。
- [ ] 每關傳雲端硬碟 `videobackup:AI劇/原來如此事務所/P04/製作檔/sothatswhy-p04-microgravity-flame`（0 differences）。

## 站主的常設指示（2026-11-12）

- 「你就這樣一直做吧，不用問我，用你推薦的決定就好；新的集數你就自己挑不錯的題目來做」：除了站主保留的成片、上架、語言三關，其餘決定由 Claude 依建議自行做，做完一集接著挑下一集。
- 「記得備份好就好」：每集收工照 todrive.sh 全量備份並用 `rclone check --one-way` 驗證 0 差異；空間不足時只刪驗證過的工作檔。
- 2026-11-12 清理：刪掉 /home/user/mokaair-video-backup-sothatswhy（舊 transfer 分支的 P18 副本，4941 個路徑在 Drive 都有）；P13、P21 補傳 approvals.json 後 0 差異（4505、5514），P29 0 差異（4518）。

## 進度

- [x] 稿子：verify-1（177/4/0）、盲評四輪到 14/14、verify-2（18/0/0）、核准
- [x] 旁白：8:06，check-audio 21→0，核准
- [ ] 關鍵畫面（--takes 3，背景跑中）
