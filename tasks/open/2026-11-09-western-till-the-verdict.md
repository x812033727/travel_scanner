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
- [x] 站主決定畫面比例與集數：16:9、第一季 60 集（2026-11-09）。
- [x] 英文設定集、第一季總綱與 60 集英文逐集細綱（`western/setting.json`、`outline.json`、`season-01.json`），`validate.mjs --season 1` 通過。
- [ ] 英文 `cast.json`（外貌、聲音、場景、道具提示詞）。
- [ ] 前三集英文劇本與分鏡，照 animation-preproduction 鎖定，三鏡小樣報價。

## Steps

- [x] 讀中文版 setting、outline 與 plan.json，列出要改的地方。
- [x] 寫 `western/README.md`。
- [x] 站主回覆兩個決定。
- [x] 改編對照表 `western/GLOSSARY.md`。
- [x] 英文設定集、總綱與第一季 60 集細綱（七個代理平行改寫，合併後統一天數與進度條）。
- [ ] 英文 cast.json。
- [ ] 前三集劇本、分鏡、小樣。

## How to verify

讀 `docs/videos/series-plans/top40-2025-2026/2025-15-xingde-xiangyu/western/README.md`；英文細綱寫好後，
跑 `node docs/videos/series-plans/top40-2025-2026/lib/validate.mjs docs/videos/series-plans/top40-2025-2026/2025-15-xingde-xiangyu/western --season 1` 與同目錄的 `lib/build.mjs … --check`。

## Notes

- 中文版的劇情骨架、十二條謎團和鉤子全部沿用；改編只動名字、場景、程序和規格。
- 法律修正：華盛頓州離婚有 90 天等待期，所以第 20 集改成判決生效那天，中間跳三個月（對上何醫師的熱爐禁令）；
  非法證據排除法則主要約束政府，所以第二季偷拍改成無法驗證來源加非法侵入與制裁；死後再審改成定罪審查小組加撤銷原判。
- 真人電影感能不能撐住，先看 `2026-11-06-tai-nainai-screen-test` 的試鏡結果。
- 第一季時間軸：第 20 集是第 99 天（婚禮當天），之後的 state.time 一律用絕對天數（第 50 集第 151 天、第 60 集第 165 天）。
- 案件進度條有六格（Report → Charges → Investigation → Arraignment → Trial → Sentencing）：停在 Report 時是 5 stages to sentencing，Charges 時是 4。
- 角色族裔：Nora 與母親為愛爾蘭裔白人；Pell 一家與 Moretti 祖孫為義大利裔；Sienna 印度裔；Dana 奈及利亞裔；Theo 韓裔；Reyes 墨西哥裔；Judith Hale 非裔。Elias 隨母姓的設定改成「自己改姓 Ashford」，因為 Rosa 仍姓 Pell。
- 「撤告」：美國的刑事案被害人不能自己撤，Grant 的條件寫成 "Drop the case and the house is yours"，指民事訴訟。
