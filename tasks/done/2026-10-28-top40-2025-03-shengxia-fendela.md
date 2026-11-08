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

- [x] reference.md：原劇套路拆解（已由研究代理寫好的話，核對一次）。
- [x] 取 3 個原創劇名候選寫進 README，先用第一個；把它填進 rankings.json 的 original_title。
- [x] plan.json：抄 zhong-tian-qu-qi/plan.json 的形狀，episode_seconds 改 90–180（篇章末 ≥120），hooks_per_episode min 3 max 5，reference 改成這部。
- [x] setting.json：世界、金手指規則與代價（world.rules）、15–20 位人物（含真人外貌提示詞）、12 條謎團（setup_season／reveal_season）、依題材的調性、不黃標、顏值、畫面。
- [x] outline.json：5 季 × 6 篇章，每篇章 beats／threads／end／spectacle／tones，每季的 start_state／end_state 與季末停點。
- [x] season-01.json … season-05.json：照 zhong-tian-qu-qi/authoring.md 的欄位逐集寫；每寫完一季跑 `validate.mjs docs/videos/series-plans/top40-2025-2026/2025-03-shengxia-fendela --season N`，再 build、commit、push。一個 session 約寫 1–2 季，在〈Notes〉記下寫到哪。
- [x] 全部五季齊後跑整體 validate 與 build --check，更新 rankings.json 與總 README。

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
- 跨季統一（2026-11-05）：改了 30 處（約一百個欄位）——S1 第49–50集 船名牌「寧安號」→船名被鑿平（S2 才知道叫望川）；S1 第29、48集 母親「十年前病逝、錶停在那年」→「十五年前病逝、錶後來停了十年」（S5 十六歲喪母）；S1 第8、17、24、27集「第五條：不過問」→「第一條」；S1 第28集 阿寧「唯一的學徒」→「第一個學徒」（S4、S5 母親是她師妹）；S1 第36集 日記「阿寧不怕海」→「阿寧怕海，更怕等」（S2 阿寧也怕海）；S1 第50集「第一天就看見」→「早就看見」（m03 的第一天、當晚留給 S2 揭）；S1 第54集「挪了五十多天」→不寫天數（S2 合約已過四個月）；S1 第59集「謝家今天回絕顏家」→「他親手退回提案」（S2 老太太週日才正式回絕）；S2 第73集「二十年的書」→「十五年」；S2 第73、75集 錶：加一個鉤子讓錶撞上欄杆停了、交給她修，「壞了十年／停了十年」→「撞停／又停了」，陸醫生「十年了」→「二十年了」（S1 第40集已修好）；S2 第108集「外公認識母親」→「外公記下母親的話」（外公是她父親）；S2 第109集「等了四個月」→「大半年」（S3 八個月）；S2 第117集 母親那頁紙→「船上的貨不對，我要——」（與 S3、S4 同一張紙）；S3 第141–142集 終止書「改成七天後生效」→照舊四個月後生效、另補「我七天後搬走」（S4 終止書日期即到期日）；S3 第161集 匿名客人從新消息→接上 S2 陸醫生送書的那位；S3 第162、165集「十六歲起…長到二十六歲」→「十六歲那年站過門口…從二十一歲長到三十一歲」；S3 第172集「三十一家」→「三十六家」（S4 三十七家含她的店）；S4 第193、222集「三週前」→「早就／兩個月前，這週才來」；S4 第195集「這三個字」→「這兩個字」；S4 第200集「阿寧走的時候」→「我上船前」（阿寧過世時母親早已失蹤）；S4 第202、207、225集「我沒坐那張桌子／二十年沒在家吃飯／二十年不敢跨進來」→「坐不起／沒好好吃過一頓飯／不敢跨進來」（S2 第110集他已坐上早餐桌）；S4 第221集「十月七日」→「十二月七日」（S1 冬季最後一航）；S5 何警官客串的名字、外貌改成 S4 同一人（對岸港警年輕男檔案員），第258集不再當成新找到報案、改為卷宗底下那張紙，第259集電話「查清」→「有紀錄為證」；S5 第241、244集 不再由母親第二次交出另一半錶（S4 第227集已扣上）→碼頭那一抱後錶停在七點二十、母親拆開發現缺齒輪，第255、268、284集「半只錶」→「那只錶」，t11 問句→「合上了卻不走」；S5 第246、269–271集 柱子：第246集改在潮嶼碼頭抱一根柱子、第269集搭渡輪帶他去對岸那根，「第一次主動回到」→「第一次帶他回到」（S4 八歲的柱子在對岸）；S5 第263–264集「你等了十一年」→「十五年」；S5 第263、298集 匿名「十五年」→「十年」（S2、S3、m11）；S5 第271、273集「整面霧面」→角落那一格已透明（S2 第107集）；S5 第291集「他走前一年」→「好幾年」（日記黏了三年）；S5 第249集「第一次先開口」→「先開了口」（S4 第209集）。保留為刻意詮釋：年祭拉成多日、她自己撕第一條、m06 第220集才 reveal、S4 把柱子放在對岸碼頭（改的是 S5）、潮汐表封底藏帳與錶要兩人上鍊、S1–S3 的日數週數與 outline 月數的落差（outline 本身矛盾，螢幕上的數字已對齊，只剩 state 標記）、八歲／十一歲（生日差容得下 27／31 歲）、第七條同時寫餐桌與不干涉工作、S2 倉庫那本書與匿名那本未明說同一本、篇章末超過 10 字的台詞。
