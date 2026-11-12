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
  - docs/videos/till-the-verdict-e001
  - docs/videos/till-the-verdict-e002
  - docs/videos/till-the-verdict-e003
  - docs/videos/till-the-verdict-e004
  - docs/videos/till-the-verdict-e005
  - docs/videos/till-the-verdict-e006
  - docs/videos/till-the-verdict-e007
  - docs/videos/till-the-verdict-e008
  - docs/videos/till-the-verdict-e009
  - docs/videos/till-the-verdict-e010
  - docs/videos/till-the-verdict-e011
  - docs/videos/till-the-verdict-e012
  - docs/videos/till-the-verdict-e013
  - docs/videos/till-the-verdict-e014
  - docs/videos/till-the-verdict-e015
  - docs/videos/till-the-verdict-e016
  - docs/videos/till-the-verdict-e017
  - docs/videos/till-the-verdict-e018
  - docs/videos/till-the-verdict-e019
  - docs/videos/till-the-verdict-e020
  - docs/videos/till-the-verdict-e021
  - docs/videos/till-the-verdict-e022
  - docs/videos/till-the-verdict-e023
  - docs/videos/till-the-verdict-e024
  - docs/videos/till-the-verdict-e025
  - docs/videos/till-the-verdict-e026
  - docs/videos/till-the-verdict-e027
  - docs/videos/till-the-verdict-e028
  - docs/videos/till-the-verdict-e029
  - docs/videos/till-the-verdict-e030
  - docs/videos/till-the-verdict-e031
  - docs/videos/till-the-verdict-e032
  - docs/videos/till-the-verdict-e033
  - docs/videos/till-the-verdict-e034
  - docs/videos/till-the-verdict-e035
  - docs/videos/till-the-verdict-e036
  - docs/videos/till-the-verdict-e037
  - docs/videos/till-the-verdict-e038
  - docs/videos/till-the-verdict-e039
  - docs/videos/till-the-verdict-e040
  - docs/videos/till-the-verdict-e041
  - docs/videos/till-the-verdict-e042
  - docs/videos/till-the-verdict-e043
  - docs/videos/till-the-verdict-e044
  - docs/videos/till-the-verdict-e045
  - docs/videos/till-the-verdict-e046
  - docs/videos/till-the-verdict-e047
  - docs/videos/till-the-verdict-e048
  - docs/videos/till-the-verdict-e049
  - docs/videos/till-the-verdict-e050
  - docs/videos/till-the-verdict-e051
  - docs/videos/till-the-verdict-e052
  - docs/videos/till-the-verdict-e053
  - docs/videos/till-the-verdict-e054
  - docs/videos/till-the-verdict-e055
  - docs/videos/till-the-verdict-e056
  - docs/videos/till-the-verdict-e057
  - docs/videos/till-the-verdict-e058
  - docs/videos/till-the-verdict-e059
  - docs/videos/till-the-verdict-e060
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
- [x] 前三集劇本與分鏡第一版、獨立審稿、改稿（2026-11-10）；直式小樣三鏡（2026-11-10）。
- [x] 前三集照 main 2026-11-12 的新規則重審重拆（種田拍法、台詞改模型原聲），二審後改完；Nora、Grant 定妝照修圖（r3）。
- [x] 第 4–10 集（篇章 1 剩下的）：系列設定 `production/s1-bible-e004-e010.md`、分鏡、程式檢查、兩段重疊的獨立審稿（`review/2026-11-12-e004-e007-storyboard.md`、`…-e007-e010-…`）、改稿（2026-11-12）。
- [x] 站主確認 `s1-bible-e004-e010.md`〈要站主決定的〉與審稿後主控先定的事（2026-11-12「照你建議」，第 21–60 集的 `s1-decisions-e021-e060.md` 與寫稿者新加的台詞一併照收）。
- [ ] 開拍前的定妝照與場景圖（兩份 bible〈人物與參考圖〉〈場景格局〉列的順序）。
- [x] 原聲小樣（2026-11-12，約 2.5 CU，screen-test README〈原聲小樣〉）；Nora 跨鏡音色等站主聽。
- [ ] 第 21–60 集（篇章 3–6）：四章系列設定並行寫、章界對齊、分鏡、審稿、改稿（站主 2026-11-12「持續擴充，可以用更多子代理」）。
- [x] 第 11–20 集（篇章 2）：系列設定 `production/s1-bible-e011-e020.md`（站主選 A：第 20 集同一個上午）、分鏡、兩段審稿（`review/2026-11-12-e011-e015-…`、`…-e015-e020-…`）、改稿（2026-11-12）。

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
- 2026-11-12 站主兩個決定：(1) 台詞改用 **H3 模型原聲**（畫面上露嘴的台詞），畫外、心裡話、電話、電視才用 Gemini，取代 11-10 的「H3 無聲＋Gemini」；
  (2) 第 1–3 集照 `script-to-storyboard.md`〈拍法：種田拍法〉重拆（一鏡約 2.5–3 秒）。都寫進 `production/s1-bible-e001-e003.md`〈全劇固定〉。
  H3 說英文的口音與跨鏡一致性還沒驗。
- 2026-11-12 製作檔備份：`AI劇/婚約到他判刑那天為止（歐美版）/_共用/製作檔/`（todrive.sh，180＋17 檔，0 differences）。之後每集的製作檔照 `docs/videos/AI-DRAMA-DRIVE.md` 放 `AI劇/婚約到他判刑那天為止（歐美版）/第NNN集/製作檔/`。 2026-11-12 的定妝照修圖 r3 另傳在 `_共用/製作檔/screen-test/`（23 檔，0 differences）。
- 2026-11-12 站主：製作時先不放大（不跑 SeedVR2），整季做完確認後再一起放大；精修檔與草稿要留著備份。

