---
id: 2026-10-31-b01-shimano-b02-lonely-planet-b03
title: 奇聞檔案局品牌三集：山葉 B01、Shimano B02、Lonely Planet B03（研究、稿子、查核、盲評，付費前報價）
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-curio-brand-b
claimed_at: 2026-10-31T14:58:22Z
created_at: 2026-10-31T14:58:19Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-b01
  - docs/videos/curio-b02
  - docs/videos/curio-b03
  - docs/videos/history-curiosity/topic-checks/B01.md
  - docs/videos/history-curiosity/topic-checks/B02.md
  - docs/videos/history-curiosity/topic-checks/B03.md
---

# 奇聞檔案局品牌三集：山葉 B01、Shimano B02、Lonely Planet B03（研究、稿子、查核、盲評，付費前報價）

## Why

站主 2026-10-31 要三個黑猫研究院式的品牌題目，選了：山葉（做鋼琴的公司為什麼機車也叫山葉）、Shimano（不賣整車卻收全世界腳踏車的錢）、
Lonely Planet（BBC 買下又折價賣出的旅遊書）。站主說這類現在算奇聞檔案局系列，並說「開始做吧」。
所以照 `curio-episode` skill 做成 `curio-` slug（B 是暫定的「品牌」編號，`topics.json` 的六個主軸沒有這一類，要不要正式開 B 軸由站主決定）。

## Definition of done

- [ ] 三集各有 topic-check（逐列一手來源）、`brief.md`、`claims.md`、`video.json`（13 分鐘、開場五步、loops ≥ 8、插圖 ≥ 70%、配樂）
- [ ] 另一個代理獨立查核寫 `verify-1.md`；盲評兩位讀者沒有同否的題，存 `panel/`
- [ ] `node tools/video/cli.mjs lint --slug curio-b0N` 0 錯誤
- [ ] 旁白與插圖的張數與上限金額三集一次報給站主，核准後才跑付費步驟

## Steps

- [ ] 研究：三集 topic-check
- [ ] 撰稿：brief、claims、video.json
- [ ] 獨立查核 verify-1.md
- [ ] 盲評 panel
- [ ] lint 0 錯誤、報價給站主
- [ ] （站主核准後）tts → check-audio → keyframes → music → render/clips/assemble → captions → qa → review-push

## How to verify

`node tools/video/cli.mjs lint --slug curio-b01`（b02、b03 同）；`node tools/video/cli.mjs narrative --slug ...`。

## Notes

- 人物：山葉寅楠 1916 卒可畫；島野庄三郎 1958 卒未滿 70 年、不畫本人；Wheeler 夫婦在世、不畫。商標與可讀文字一律不畫。
- 容器有 2026-10-25 配對的影音權杖（`~/.mokaair/video-tool.json`），10-31 用 GET media/status 驗過有效。
