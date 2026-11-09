---
id: 2026-11-09-western-till-the-verdict
title: Western adaptation of Till the Verdict Do Us Part (2025-15)
status: review
priority: P2
area: docs
owner: claude-opus-5-5
claimed_at: 2026-11-09T00:14:33Z
created_at: 2026-11-09T00:14:32Z
completed_at:
branch: claude/exciting-pascal-u7qk3g
depends_on: []
scope:
  - docs/videos/series-plans/top40-2025-2026/2025-15-xingde-xiangyu/western
---

# Western adaptation of Till the Verdict Do Us Part (2025-15)

## Why

站主 2026-11-09 從 repo 的企劃裡選定《婚約到他判刑那天為止》（`2025-15-xingde-xiangyu`）做歐美版、走歐美市場。
中文版的五季三百集已經寫完，但人名、城市、法律程序、文化細節和規格都是華語市場的；直接翻譯配音，美國觀眾會在
「同一天離婚又再婚」「私人偷拍的照片被法院排除」這類地方出戲。

## Definition of done

- [x] 改編規格：劇名、Port Merrow 的世界、人物對照、法律程序修正、文化調整、規格差異、第一季篇章對照（`western/README.md`）。
- [ ] 站主決定畫面比例（9:16／16:9）與先做幾集。
- [ ] 英文 `cast.json` 與第一季 60 集英文逐集細綱，通過 `lib/validate.mjs` 的同一套規則。
- [ ] 前三集英文劇本與分鏡，照 animation-preproduction 鎖定，三鏡小樣報價。

## Steps

- [x] 讀中文版 setting、outline 與 plan.json，列出要改的地方。
- [x] 寫 `western/README.md`。
- [ ] 等站主回覆兩個決定。
- [ ] 英文 cast 與第一季細綱。
- [ ] 前三集劇本、分鏡、小樣。

## How to verify

讀 `docs/videos/series-plans/top40-2025-2026/2025-15-xingde-xiangyu/western/README.md`；英文細綱寫好後，
跑 `node docs/videos/series-plans/top40-2025-2026/lib/validate.mjs <英文版目錄>`。

## Notes

- 中文版的劇情骨架、十二條謎團和鉤子全部沿用；改編只動名字、場景、程序和規格。
- 法律修正：華盛頓州離婚有 90 天等待期，所以第 20 集改成判決生效那天，中間跳三個月（對上何醫師的熱爐禁令）；
  非法證據排除法則主要約束政府，所以第二季偷拍改成無法驗證來源加非法侵入與制裁；死後再審改成定罪審查小組加撤銷原判。
- 真人電影感能不能撐住，先看 `2026-11-06-tai-nainai-screen-test` 的試鏡結果。
