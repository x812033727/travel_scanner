---
id: 2026-10-28-top40-2025-03-shengxia-fendela
title: Top40 drama plan 2025-03: adapt the pattern of 盛夏芬德拉 into a 300-episode original
status: done
priority: P2
area: docs
owner: claude
claimed_at: 2026-10-28T15:00:25Z
created_at: 2026-10-28T14:03:00Z
completed_at: 2026-10-28T22:54:42Z
branch: claude/confident-galileo-vfq0j3
depends_on: []
scope:
  - docs/videos/series-plans/top40-2025-2026/2025-03-shengxia-fendela
---

# Top40 drama plan 2025-03: adapt the pattern of 盛夏芬德拉 into a 300-episode original

## Why

站主（2026-10-28）要把 2025 全年與 2026 年 1–10 月紅果熱度前 20 名的短劇各改編成一部原創漫劇，
照《種田娶妻打天下》（`docs/videos/series-plans/zhong-tian-qu-qi/`）的規格：5 季 × 60 集 = 300 集、
每季 6 篇章 × 10 集、每集 90–180 秒、每集 3–5 個彼此不同的鉤子（前 3 秒、中段、結尾，可加 0–2 個）。
這張票是 2025 年第 3 名《盛夏芬德拉》（紅果・馬廄製片廠，峰值熱度(萬) 12347）。
**保留這部劇自己的題材**，只學它的套路結構；人名、世界、劇情、台詞全部原創。總表在
`docs/videos/series-plans/top40-2025-2026/README.md` 與 `rankings.json`。

## Definition of done

- [x] `docs/videos/series-plans/top40-2025-2026/2025-03-shengxia-fendela/` 有 README.md（一句話、類型、規模、參考劇與原創聲明、季表、等站主決定）、reference.md、plan.json、
  setting.json、outline.json、season-01.json … season-05.json。
- [x] `node docs/videos/series-plans/top40-2025-2026/lib/validate.mjs docs/videos/series-plans/top40-2025-2026/2025-03-shengxia-fendela` 零錯誤（300 集）。
- [x] `node docs/videos/series-plans/top40-2025-2026/lib/build.mjs docs/videos/series-plans/top40-2025-2026/2025-03-shengxia-fendela --check` 乾淨（setting.md、outline.md、season-NN.md、episodes.csv 由它產生，不手改）。
- [x] `rankings.json` 這筆的 `original_title` 與 `status` 更新到 `done`；README 進度表同步。

## Steps

- [ ] reference.md：原劇套路拆解（已由研究代理寫好的話，核對一次）。
- [ ] 取 3 個原創劇名候選寫進 README，先用第一個；把它填進 rankings.json 的 original_title。
- [ ] plan.json：抄 zhong-tian-qu-qi/plan.json 的形狀，episode_seconds 改 90–180（篇章末 ≥120），hooks_per_episode min 3 max 5，reference 改成這部。
- [ ] setting.json：世界、金手指規則與代價（world.rules）、15–20 位人物（含真人外貌提示詞）、12 條謎團（setup_season／reveal_season）、依題材的調性、不黃標、顏值、畫面。
- [ ] outline.json：5 季 × 6 篇章，每篇章 beats／threads／end／spectacle／tones，每季的 start_state／end_state 與季末停點。
- [ ] season-01.json … season-05.json：照 zhong-tian-qu-qi/authoring.md 的欄位逐集寫；每寫完一季跑 `validate.mjs docs/videos/series-plans/top40-2025-2026/2025-03-shengxia-fendela --season N`，再 build、commit、push。一個 session 約寫 1–2 季，在〈Notes〉記下寫到哪。
- [ ] 全部五季齊後跑整體 validate 與 build --check，更新 rankings.json 與總 README。

## How to verify

```bash
node docs/videos/series-plans/top40-2025-2026/lib/validate.mjs docs/videos/series-plans/top40-2025-2026/2025-03-shengxia-fendela
node docs/videos/series-plans/top40-2025-2026/lib/build.mjs docs/videos/series-plans/top40-2025-2026/2025-03-shengxia-fendela --check
node --test docs/videos/series-plans/top40-2025-2026/lib/validate.test.mjs
npm run check:tasks
```

## Notes

- 規則說明在 `docs/videos/series-plans/zhong-tian-qu-qi/authoring.md`（欄位）與 `README.md`（讓人停不下來的規則）；這套票唯二的差異是秒數 90–180 與可選的 `extra_hooks`。
- 進度：2026-10-28 全部完成。五季各由一個代理平行寫成（部分季因額度中斷後以 Opus 5.5 重寫），`validate.mjs` 零錯誤、`build.mjs --check` 乾淨。
- 代理回報的取捨（站主可改）：第一季年祭拉成多日、第 60 集她自己撕第一條；第二季 m06 只 payoff（setting 的 reveal_season 是 4）、第 220 集改為 reveal（本 session 手動補）；第三季時間線與 outline『剩三個月』對不上、用週數帶過；第四季把『柱子』放到對岸碼頭；第五季加外公的帳藏在潮汐表封底、懷錶要兩個人一起上發條、『十一年』與十六到三十一歲的年差未調。
- 已知小瑕疵：篇章末幾句照 outline 抄的台詞超過 10 字。
