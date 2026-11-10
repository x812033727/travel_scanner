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
- [x] 站主決定畫面比例與集數：第一季 60 集（2026-11-09）；畫面 **9:16 直式**（2026-11-10 改定，原 16:9）。
- [ ] 直式小樣：H3 Ref2VA 544×960 → 736×1312 還沒在 repo 試過（試鏡是 16:9）。
- [x] 英文設定集、第一季總綱與 60 集英文逐集細綱（`western/setting.json`、`outline.json`、`season-01.json`），`validate.mjs --season 1` 通過。
- [x] 英文 `production/cast.json`（外貌、換裝、聲音候選、路人、場景、道具提示詞）。
- [x] 定妝照試鏡（2026-11-10，約 9 CU，`production/screen-test/README.md`）。
- [x] 站主定案（2026-11-10「照內建的」）：聲音用 cast.json 預設、定妝照用試鏡預設，存 `production/assets/refs/`、填 `portrait`；台詞照內建、不對嘴。
- [ ] 前三集英文劇本與分鏡，照 animation-preproduction 鎖定，三鏡小樣報價。

## Steps

- [x] 讀中文版 setting、outline 與 plan.json，列出要改的地方。
- [x] 寫 `western/README.md`。
- [x] 站主回覆兩個決定。
- [x] 改編對照表 `western/GLOSSARY.md`。
- [x] 英文設定集、總綱與第一季 60 集細綱（七個代理平行改寫，合併後統一天數與進度條）。
- [x] 英文 cast.json。
- [x] 定妝照試鏡與四個主角的聲音試聽（樣本已交站主）。
- [ ] 依試鏡結果改 cast.json：Nora 拿掉手腕燙痕、Elias 的疤改獨立插鏡、陰天寫進每鏡正文。
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
- cast.json 的聲音都是 Gemini TTS 的候選（名字已對過 `apps/api/app/video_speech/gemini.py`），還沒試聽：Nora Despina、Elias Charon、Grant Algieba、Peg Gacrux。
- 生成時不放任何可讀文字（文件、招牌、帳本、瓶底的氣泡名字），要讓觀眾讀的字一律後製加。
- Nora 第 19 集剪成齊肩；Sienna 一律用左手寫字、翻頁（第 50 集的伏筆）；Elias 左手背的疤到第 60 集才露。
- 2026-11-10 試鏡：選 Nora b、Elias a、Grant a、Peg a；四支片段臉都守住、三支說話鏡嘴有動；細小傷痕會被畫成紅點或紅色傷口（見 screen-test README〈學到的〉）。
