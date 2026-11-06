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
- 跨季統一（2026-11-05）：改了 25 處——念慈的律師三季三人：S2 陳律師（男 34）、S5 盧律師（40）→ 一律 S1 的鄭律師（鄭若彤），名字、角色、外貌照 S1；S2 第 84 集江父來電→改成她要開那扇積灰的門、他說「別開」（S3 開季明寫江父「第一次打電話」，全劇三通＝S3 兩通＋S5 第 278 集）；S3 第 123 集「她第一次聽他提起家人」→「這是他第一次自己提起家人」，turn 改成她知道他爸在外地、第一次看見那個人打來；S2 第 82、86 集江野「十年前喪母」→「他媽走後」「十六歲喪母」（S3 第 166 集十六歲、S4 十四年）；S2 第 74 集「江野十八歲那年送的錶」→「在她十八歲那年」；S2 第 115 集「她第一次成了站在門口等的人」→「又成了」（S1 第 59–60 集已等過）；S3 第 121 集加「七個月後，十一月初」（S2 末 275 萬→S3 開季 240 萬＝七期五萬）；S3 第 125 集月繳兩萬加一句「跟銀行的協商過了，這個月起月繳降成兩萬」，第 145、153 集另兩筆「這個月的兩萬」→兼差、加班的兩萬（S2、S4 月繳五萬）；S3 第 132 集「同居了五年」→「交往了七年」、第 136 集「她挑的窗簾／管理員認得她」→陽台只在許以寧照片裡見過（S1 第 25 集公寓是瞞她的）；S3 第 153 集阿公「給我老伴」→「給我孫媳婦」（獨居，S5 只有高雄的孫子）；S3 第 170 集江父初五上車離開→到站沒上車、行李箱提回老屋（S4 開季「江父留在鎮上」、行李箱從過年立著）；S3 第 173 集「二月中」→「二月底」出發（隔天回來就是 S4 三月初動工）；S4 第 181 集阿公「那罐銅板」→「第二罐」（S3 第 172 集已入股）、請假單「兩個月前」→「她去台北那天」（S3 第 178 集才定動工日）；S4 第 193、199 集十年前那天他「從街角跑來、拎保溫瓶」→站牌後面、一袋蛋餅一個保溫瓶，照片裡那個拎紙袋的少年她早認出來了，「她知道那天他也在公車站」→「他衝到了車門口」（S3 第 142–144 集）；S4 第 201 集「她以為已經知道江野救了媽媽」→只知道地址、四十分鐘、疤，秀琴姨才說出倉庫裡的是媽媽（S2 第 100 集救誰沒人說，m09 在 205 揭）；S4 第 209 集「她第一次在消防隊門口等他」→坐在長椅上等到訓練結束；S4 第 224 集「離家十四年」→「十二年」（總綱十八歲那年父親去外地）；S4 第 235 集「她第一次替他煮薑茶」→「這次換她煮」；S5 第 242 集七點下夜班加「照護所開了，她的夜班改到七點交接」（S1、S4 都是四點下班）；S5 第 242、271 集與短線 t14「煮了一年都太辣、先學會煮」→一緊張放了一斤薑、這次煮回剛好（S2 第 117 集、S4 第 235 集早已不辣）；S5 第 260 集標題「十年前被公車蓋掉的那句話…終於聽見」→「十年前說好回來要說的那句話」（S4 第 194 集她已聽過「等妳回來，我有話說」）；S5 第 261、268、292 集帳本「林致遠欠三百萬→290→280」→「一百五十萬→140→130」（S4 第 184 集許以寧已清償自己那一百五十萬）；S5 第 274 集「十八歲的江野」→「二十歲」，十張時刻表改成她去年年底在他抽屜見過、他收進鐵盒（S3 第 158 集）；S5 第 298 集「第一次替他算回來的時間」→「第一次照他回來的時間煮」（S4 第 217–218 集她已在數分鐘）；S5 第 300 集「第一句話跟她回來那一晚一樣：薑茶呢」→「是那年天亮她在長椅旁問他的那句」（S1 第 1 集他說的是「回來了？」）。保留為刻意詮釋：S1 夜班四點下班、m02 揭在 57、m10 未用；S2 只給地址；S3 m06 半揭、許以寧 156–157 來鹿川、賣禮物與定存補數；S4 許以寧自付一百五十萬、阿公髖骨骨折、開幕 239–240；S5 哥哥兩次「趁熱」、信 267 讀 268 燒、唐護理長邀約；王阿嬤即 S2 第 78 集到府換藥的王阿嬤，與 S4 秀琴姨、吳阿嬤是不同人，不必合併；「十年」「三年前」當固定稱呼、公車班次與時刻、江父那天在樓上看、哥哥追車一百公尺、他那天站一小時又買了下一班票等補充細節不動。
