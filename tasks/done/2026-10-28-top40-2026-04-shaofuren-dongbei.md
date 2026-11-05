---
id: 2026-10-28-top40-2026-04-shaofuren-dongbei
title: Top40 drama plan 2026-04: adapt the pattern of 少夫人來自東北 into a 300-episode original
status: done
priority: P2
area: docs
owner: claude
claimed_at: 2026-10-28T15:25:44Z
created_at: 2026-10-28T14:03:14Z
completed_at: 2026-10-28T23:35:15Z
branch: claude/confident-galileo-vfq0j3
depends_on: []
scope:
  - docs/videos/series-plans/top40-2025-2026/2026-04-shaofuren-dongbei
---

# Top40 drama plan 2026-04: adapt the pattern of 少夫人來自東北 into a 300-episode original

## Why

站主（2026-10-28）要把 2025 全年與 2026 年 1–10 月紅果熱度前 20 名的短劇各改編成一部原創漫劇，
照《種田娶妻打天下》（`docs/videos/series-plans/zhong-tian-qu-qi/`）的規格：5 季 × 60 集 = 300 集、
每季 6 篇章 × 10 集、每集 90–180 秒、每集 3–5 個彼此不同的鉤子（前 3 秒、中段、結尾，可加 0–2 個）。
這張票是 2026 年第 4 名《少夫人來自東北》（紅果，峰值熱度(萬)，截至 5/12 11884）。
**保留這部劇自己的題材**，只學它的套路結構；人名、世界、劇情、台詞全部原創。總表在
`docs/videos/series-plans/top40-2025-2026/README.md` 與 `rankings.json`。

## Definition of done

- [x] `docs/videos/series-plans/top40-2025-2026/2026-04-shaofuren-dongbei/` 有 README.md（一句話、類型、規模、參考劇與原創聲明、季表、等站主決定）、reference.md、plan.json、
  setting.json、outline.json、season-01.json … season-05.json。
- [x] `node docs/videos/series-plans/top40-2025-2026/lib/validate.mjs docs/videos/series-plans/top40-2025-2026/2026-04-shaofuren-dongbei` 零錯誤（300 集）。
- [x] `node docs/videos/series-plans/top40-2025-2026/lib/build.mjs docs/videos/series-plans/top40-2025-2026/2026-04-shaofuren-dongbei --check` 乾淨（setting.md、outline.md、season-NN.md、episodes.csv 由它產生，不手改）。
- [x] `rankings.json` 這筆的 `original_title` 與 `status` 更新到 `done`；README 進度表同步。

## Steps

- [x] reference.md：原劇套路拆解（已由研究代理寫好的話，核對一次）。
- [x] 取 3 個原創劇名候選寫進 README，先用第一個；把它填進 rankings.json 的 original_title。
- [x] plan.json：抄 zhong-tian-qu-qi/plan.json 的形狀，episode_seconds 改 90–180（篇章末 ≥120），hooks_per_episode min 3 max 5，reference 改成這部。
- [x] setting.json：世界、金手指規則與代價（world.rules）、15–20 位人物（含真人外貌提示詞）、12 條謎團（setup_season／reveal_season）、依題材的調性、不黃標、顏值、畫面。
- [x] outline.json：5 季 × 6 篇章，每篇章 beats／threads／end／spectacle／tones，每季的 start_state／end_state 與季末停點。
- [x] season-01.json … season-05.json：照 zhong-tian-qu-qi/authoring.md 的欄位逐集寫；每寫完一季跑 `validate.mjs docs/videos/series-plans/top40-2025-2026/2026-04-shaofuren-dongbei --season N`，再 build、commit、push。一個 session 約寫 1–2 季，在〈Notes〉記下寫到哪。
- [x] 全部五季齊後跑整體 validate 與 build --check，更新 rankings.json 與總 README。

## How to verify

```bash
node docs/videos/series-plans/top40-2025-2026/lib/validate.mjs docs/videos/series-plans/top40-2025-2026/2026-04-shaofuren-dongbei
node docs/videos/series-plans/top40-2025-2026/lib/build.mjs docs/videos/series-plans/top40-2025-2026/2026-04-shaofuren-dongbei --check
node --test docs/videos/series-plans/top40-2025-2026/lib/validate.test.mjs
npm run check:tasks
```

## Notes

- 規則說明在 `docs/videos/series-plans/zhong-tian-qu-qi/authoring.md`（欄位）與 `README.md`（讓人停不下來的規則）；這套票唯二的差異是秒數 90–180 與可選的 `extra_hooks`。
- 進度：五季 300 集齊，整體 validate 零錯誤，build --check 乾淨。
- 季代理的彎折：S1 m10 未標（setting 給 setup_season 3）、債務走 m03；倒數到大壽（第 8 天）、契約第 9 天到期；祖母不出席第一餐；小妹第 55 集首次叫「姐」。S2 助理命名何思遠（S4 寫成何敬文——兩季名字不一，站主改稿時統一為一人）；m08 父親的話只說一半；董事會投的是餐巾紙照片、原件留 S4；「我媽走了二十年」改「她進這個家二十年」。S3 收購改為律師信退利息分 12 期；張德福受邀上桌；m01 只列 payoff；踹改夾腳拖輕踢。S4 技師江柏山、二嬸羅美鳳對齊 S5；戒指留給 S5；他第一聲「媽」留 S5 第 296 集；錄音筆設局抓二叔。S5 生日改「四十四天後」、加「回星港四週後」字卡；加二嬸、林爸林媽；他撕餐巾紙、阿嬤留半張、新契約寫在背面。
- 待統一：助理名字（S2 何思遠／S4 何敬文）。
- 跨季統一（2026-11-05）：改了 11 處（40 個欄位）——S4 助理統一為 S2 的何思遠（guest_cast 何敬文→何思遠、三十四歲→三十二歲、特助→助理、外貌提示詞改用 S2 的；第 181、183、191、199、238 集的何敬文→何思遠）；S4 第 191 集轉折「以為是外人闖進來」→「以為助理只敢在外面傳話」（S2 已知他是二叔的人）；S2 第 61 集「大壽當夜」→「續約當夜」、「她問影本是哪來的」→「她問助理為什麼把影本送來」（S1 第 60 集祖母已說是助理給的）；S1 第 16 集船名「金海春號」→「海春號」（同 S3）；S3 第 121、122、130、151、156 集她手上不再有一百萬（存摺、「在星港打工的錢」→直播賣魚的錢，「還差十八萬」→逾期先要繳的十八萬；outline 與 S1、S2、S4、S5 都是她沒拿那張支票）；S3 第 167 集拿掉老阿伯「四十年前出去的」等等於說破 m09 的句子，留給 S4 揭；S4 第 182 集繼母「二十年沒進過廚房」→「二十年沒在廚房坐下過」（S3 第 174 集她當天在廚房煮麵）；S4 第 190 集繼母「十九歲沒畢業就嫁了」→「十九歲沒畢業就出來做事了」（她二十年前、三十歲才進邵家）；S4 第 204、206 集「宋先生」→「江先生」（江柏山）；S4 第 212 集父親過世「二十年」→「十年」（同 S1、S3、S5）；S4 第 238 集助理證詞「欠誰的錢」→「開什麼店」（S3 第 150 集他是張凱丟催繳單那天才知道林家欠錢）。保留為刻意詮釋：S1 末集祖母與陳叔對 m02 的預告、S2 的打包行李與三個月再簽、S3 照 outline 先講三年前那一夜與紅繩、S4／S5 新增的客串與支線、S5 提前稱祖母九十一歲；全劇「一年」與九十一大壽需要 S4 跨半年，S4 卻只寫了約七週（五季合計約八個月），要在 S4 插時間跳躍才對得上，屬結構決定，未改，留給站主。
- 結構性重排（2026-11-05）：S4 第 3→4 章之間（第 210→211 集）加字卡「四個月後」，停職從第 26 天跳到第 160 天、董事會在停職第 183 天（滿半年），全劇從機場 Day 1 走到第 300 集 Day 365，九十一大壽距九十大壽 354 天（農曆一年），邵亦辰第 1 集剛滿三十一、S5 開季三十一歲十個月；第 209 集小報改成「審繼承權之前」登，S4 第 4–6 章與 S5 第 1–3 章的「一年」改「快一年」，指 S2／S3 的改具體月數（第 210 集五個月、第 223 集八個月前、第 266 集七個月前與這半年），第 252 集改「九十大壽那碗」，順手修第 200 集「三天內」→「週日前」（停職第 13 天是週一）；改了 20 處 34 個欄位（含 outline 2、setting 0）；另一案：斷在第 4→5 章（簡報提的），但那裡和第 5→6 章都是同一場戲接下去（同一頓晚餐、同一個董事會前夜），要拆第 221 集、讓頭版登出後空四個月才開董事會，S4 少動兩集卻打斷「頭版→麵休三天→三天後董事會」，所以不選。未動：S2 第 69 集「續約第 8 天週日」與 S4「停職第 9 天週四」按日數推不在同一個星期幾上（跨季星期幾沒對齊，觀眾看不出，留著）；S5 提前稱祖母九十一歲照上一輪的決定保留。
