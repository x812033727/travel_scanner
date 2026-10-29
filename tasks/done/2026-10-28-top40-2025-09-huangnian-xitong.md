---
id: 2026-10-28-top40-2025-09-huangnian-xitong
title: Top40 drama plan 2025-09: adapt the pattern of 荒年全村啃樹皮，我有系統滿倉肉 into a 300-episode original
status: done
priority: P3
area: docs
owner: claude
claimed_at: 2026-10-29T00:34:05Z
created_at: 2026-10-28T14:03:04Z
completed_at: 2026-10-29T01:23:46Z
branch:
depends_on: []
scope:
  - docs/videos/series-plans/top40-2025-2026/2025-09-huangnian-xitong
---

# Top40 drama plan 2025-09: adapt the pattern of 荒年全村啃樹皮，我有系統滿倉肉 into a 300-episode original

## Why

站主（2026-10-28）要把 2025 全年與 2026 年 1–10 月紅果熱度前 20 名的短劇各改編成一部原創漫劇，
照《種田娶妻打天下》（`docs/videos/series-plans/zhong-tian-qu-qi/`）的規格：5 季 × 60 集 = 300 集、
每季 6 篇章 × 10 集、每集 90–180 秒、每集 3–5 個彼此不同的鉤子（前 3 秒、中段、結尾，可加 0–2 個）。
這張票是 2025 年第 9 名《荒年全村啃樹皮，我有系統滿倉肉》（紅果，峰值熱度(萬) 9893）。
**保留這部劇自己的題材**，只學它的套路結構；人名、世界、劇情、台詞全部原創。總表在
`docs/videos/series-plans/top40-2025-2026/README.md` 與 `rankings.json`。

## Definition of done

- [x] `docs/videos/series-plans/top40-2025-2026/2025-09-huangnian-xitong/` 有 README.md（一句話、類型、規模、參考劇與原創聲明、季表、等站主決定）、reference.md、plan.json、
  setting.json、outline.json、season-01.json … season-05.json。
- [x] `node docs/videos/series-plans/top40-2025-2026/lib/validate.mjs docs/videos/series-plans/top40-2025-2026/2025-09-huangnian-xitong` 零錯誤（300 集）。
- [x] `node docs/videos/series-plans/top40-2025-2026/lib/build.mjs docs/videos/series-plans/top40-2025-2026/2025-09-huangnian-xitong --check` 乾淨（setting.md、outline.md、season-NN.md、episodes.csv 由它產生，不手改）。
- [x] `rankings.json` 這筆的 `original_title` 與 `status` 更新到 `done`；README 進度表同步。

## Steps

- [x] reference.md：原劇套路拆解（已由研究代理寫好的話，核對一次）。
- [x] 取 3 個原創劇名候選寫進 README，先用第一個；把它填進 rankings.json 的 original_title。
- [x] plan.json：抄 zhong-tian-qu-qi/plan.json 的形狀，episode_seconds 改 90–180（篇章末 ≥120），hooks_per_episode min 3 max 5，reference 改成這部。
- [x] setting.json：世界、金手指規則與代價（world.rules）、15–20 位人物（含真人外貌提示詞）、12 條謎團（setup_season／reveal_season）、依題材的調性、不黃標、顏值、畫面。
- [x] outline.json：5 季 × 6 篇章，每篇章 beats／threads／end／spectacle／tones，每季的 start_state／end_state 與季末停點。
- [x] season-01.json … season-05.json：照 zhong-tian-qu-qi/authoring.md 的欄位逐集寫；每寫完一季跑 `validate.mjs docs/videos/series-plans/top40-2025-2026/2025-09-huangnian-xitong --season N`，再 build、commit、push。一個 session 約寫 1–2 季，在〈Notes〉記下寫到哪。
- [x] 全部五季齊後跑整體 validate 與 build --check，更新 rankings.json 與總 README。

## How to verify

```bash
node docs/videos/series-plans/top40-2025-2026/lib/validate.mjs docs/videos/series-plans/top40-2025-2026/2025-09-huangnian-xitong
node docs/videos/series-plans/top40-2025-2026/lib/build.mjs docs/videos/series-plans/top40-2025-2026/2025-09-huangnian-xitong --check
node --test docs/videos/series-plans/top40-2025-2026/lib/validate.test.mjs
npm run check:tasks
```

## Notes

- 規則說明在 `docs/videos/series-plans/zhong-tian-qu-qi/authoring.md`（欄位）與 `README.md`（讓人停不下來的規則）；這套票唯二的差異是秒數 90–180 與可選的 `extra_hooks`。
- 進度：五季 300 集齊，整體 validate 零錯誤，build --check 乾淨。
- 季代理的彎折：S1 一天最多多一格、假的「飽了」不算；冊子第 54 集先給目錄頁、60 集給全本；真野豬用倉給的鹽醃不消失（沒用「醃漬」漏洞）；霍青只說兩句。S2 交給趙四的糧在路上消失、她讓趙四簽「回繳已收」；書抄在廚房門板上；「第三句話」改成當天的第三句；小叔偷醃肉給黑風寨；霍青登記為周阿青。S3 入獄改清晨、倉黑在第二個清晨；寫過字的紙不消失（新規則）；井圖提前到 159；婆婆用拐杖攔不打。S4 一天一格、「六百聲一格」成笑點與 m01 暗示；空白紙每天給新的、字會淡；四十戶→七十戶；官差住半個月；加偽婚書、糧批號、分三成給鄰縣。S5 97/98/99 格亮且不滅的機制（原主的碗亮 99）；加州牧三天期限、柳嫂的「已發」單、樺皮信、小四第二個字「叔，地」。
- 待統一：S1 說「石老爹給坡地」在 58 集，S2 若另寫她去要坡地要對一下。
