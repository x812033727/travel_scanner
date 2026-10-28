---
id: 2026-10-28-top40-2026-05-hongtang-jiangzhi
title: Top40 drama plan 2026-05: adapt the pattern of 紅糖薑汁 into a 300-episode original
status: done
priority: P2
area: docs
owner: claude
claimed_at: 2026-10-28T22:32:00Z
created_at: 2026-10-28T14:03:14Z
completed_at: 2026-10-28T23:43:11Z
branch: claude/confident-galileo-vfq0j3
depends_on: []
scope:
  - docs/videos/series-plans/top40-2025-2026/2026-05-hongtang-jiangzhi
---

# Top40 drama plan 2026-05: adapt the pattern of 紅糖薑汁 into a 300-episode original

## Why

站主（2026-10-28）要把 2025 全年與 2026 年 1–10 月紅果熱度前 20 名的短劇各改編成一部原創漫劇，
照《種田娶妻打天下》（`docs/videos/series-plans/zhong-tian-qu-qi/`）的規格：5 季 × 60 集 = 300 集、
每季 6 篇章 × 10 集、每集 90–180 秒、每集 3–5 個彼此不同的鉤子（前 3 秒、中段、結尾，可加 0–2 個）。
這張票是 2026 年第 5 名《紅糖薑汁》（紅果，峰值熱度(萬)，3 月上線 11840）。
**保留這部劇自己的題材**，只學它的套路結構；人名、世界、劇情、台詞全部原創。總表在
`docs/videos/series-plans/top40-2025-2026/README.md` 與 `rankings.json`。

## Definition of done

- [x] `docs/videos/series-plans/top40-2025-2026/2026-05-hongtang-jiangzhi/` 有 README.md（一句話、類型、規模、參考劇與原創聲明、季表、等站主決定）、reference.md、plan.json、
  setting.json、outline.json、season-01.json … season-05.json。
- [x] `node docs/videos/series-plans/top40-2025-2026/lib/validate.mjs docs/videos/series-plans/top40-2025-2026/2026-05-hongtang-jiangzhi` 零錯誤（300 集）。
- [x] `node docs/videos/series-plans/top40-2025-2026/lib/build.mjs docs/videos/series-plans/top40-2025-2026/2026-05-hongtang-jiangzhi --check` 乾淨（setting.md、outline.md、season-NN.md、episodes.csv 由它產生，不手改）。
- [x] `rankings.json` 這筆的 `original_title` 與 `status` 更新到 `done`；README 進度表同步。

## Steps

- [x] reference.md：原劇套路拆解（已由研究代理寫好的話，核對一次）。
- [x] 取 3 個原創劇名候選寫進 README，先用第一個；把它填進 rankings.json 的 original_title。
- [x] plan.json：抄 zhong-tian-qu-qi/plan.json 的形狀，episode_seconds 改 90–180（篇章末 ≥120），hooks_per_episode min 3 max 5，reference 改成這部。
- [x] setting.json：世界、金手指規則與代價（world.rules）、15–20 位人物（含真人外貌提示詞）、12 條謎團（setup_season／reveal_season）、依題材的調性、不黃標、顏值、畫面。
- [x] outline.json：5 季 × 6 篇章，每篇章 beats／threads／end／spectacle／tones，每季的 start_state／end_state 與季末停點。
- [x] season-01.json … season-05.json：照 zhong-tian-qu-qi/authoring.md 的欄位逐集寫；每寫完一季跑 `validate.mjs docs/videos/series-plans/top40-2025-2026/2026-05-hongtang-jiangzhi --season N`，再 build、commit、push。一個 session 約寫 1–2 季，在〈Notes〉記下寫到哪。
- [x] 全部五季齊後跑整體 validate 與 build --check，更新 rankings.json 與總 README。

## How to verify

```bash
node docs/videos/series-plans/top40-2025-2026/lib/validate.mjs docs/videos/series-plans/top40-2025-2026/2026-05-hongtang-jiangzhi
node docs/videos/series-plans/top40-2025-2026/lib/build.mjs docs/videos/series-plans/top40-2025-2026/2026-05-hongtang-jiangzhi --check
node --test docs/videos/series-plans/top40-2025-2026/lib/validate.test.mjs
npm run check:tasks
```

## Notes

- 規則說明在 `docs/videos/series-plans/zhong-tian-qu-qi/authoring.md`（欄位）與 `README.md`（讓人停不下來的規則）；這套票唯二的差異是秒數 90–180 與可選的 `extra_hooks`。
- 進度：五季 300 集齊，整體 validate 零錯誤，build --check 乾淨。
- 季代理的彎折：S1 第一篇章在一夜內（21:40–05:30）；班下 04:00；m02 揭在 57 不是 60；m10 未用（setup_season 3）。S2 第 100 集只給地址（中正路 12 號），救的是誰留 S4；林致遠整季未還；江父用掉一通電話（全劇上限三通）。S3 收購改律師信；m06 只以 setup 露一半；許以寧來鹿川在 156–157；賣禮物 12 萬、婚禮定存 10 萬補數字。S4 債從 200 萬降到 50 萬是許以寧自付 150 萬；阿公 232 集髖骨骨折（S5 輪椅）；開幕 239–240。S5 弟弟「趁熱」做了兩次（258、260）；信在 267 讀 268 燒；m08 的錢記作「他欠」；加唐護理長的台北工作邀約（她不上車）；王阿嬤若與 S4 院民重複請合併。
