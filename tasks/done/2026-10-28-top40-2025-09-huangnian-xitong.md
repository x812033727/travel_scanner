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
- 跨季統一（2026-11-05）：改了 21 處（68 個欄位）——S1 第24集 原主閃回「說了一句『讓孩子吃飽』」→「對著灶嘴唇動了動」、knowledge 改成大丫沒說是什麼（遺言照 outline 留給 S5 第254–257集大丫說出，她才不會「明知故問」）；S2 客串二當家 外貌「約三十五六歲、中等身材」→「三十八歲、瘦長、背微駝、眼窩深」（對齊 S4/S5 王大）；S2 第61/64/71/75/80集 坡地（待統一那條）：第71集「這塊，我要了」「拿下後山坡地」→ 坡是村長在 S1 第58集給的、上回那根苗曬成枯草、「這回，整面坡」從頭開工，第61集「坡地荒著」→「只冒過一根苗」，第75集「她確定種進土裡不會消失」→「照樣不會消失」，第80集「全村第一次看見綠色」→「整面坡綠起來」，第64集補 S1 第二十格那包種子當夜跟冊子一起消失；S2 第80集「大家第一次笑出聲」→「坡上第一次有了笑聲」（S1 第38集全村已哄堂大笑）；S2 第88集「婆婆第一次站上灶／第一次下廚／第一次替她做一件事」→「搶下她的灶、熬老三最愛的粥」（S1 第51集婆婆已自己生火煮粥）；S2 第109集 戶冊「全村決定護不護一個罪將」→「替不替來路不明的獵戶擔保、沒人問他是誰」（S3 第173–175集全村才愣住、婆婆才說早知道）；S3 第128集 婆婆嚐鹽「三年了」「三年來第一次嚐到鹹味」→「三年沒見過整塊的」鹽磚（S1/S2 她早吃過醃肉、熬過醃肉粥）；S3 第164集 畫面裡大丫十四歲→十五歲（同集標題與 S4 都是十五，S5 春天滿十六）；S3 第168–169集 石頭：第168集加一句 extra_hook（大丫送飯指出石頭一整天沒走在背土）、characters 加 da-ya，第169集回井邊的人裡拿掉石頭（S4 第213集「他第八天沒走」、S4/S5 客串設定要有出處）；S4 縣丞：客串「縣丞 陸守拙」→「錢縣丞」、外貌對齊 S3（瘦長、八字鬍、袖口沾墨、眼睛總在算），第184集「一個面黃的八品官」→「是錢縣丞」，第185集「我三年沒吃飽」補「除了山口那個包子」（S3 第163/177集他吃過她的醃肉包說飽）；S4 第199、212集 刻痕與小叔偷看種田「三年」→「三季」（都從她穿來那季算，對得上『她家那季多出來的缸數』）；S4 第205集 王寡婦「說了三年來第一聲飽」→「一口沒留，說了飽」（S2 第118集、S3 第156集已說過飽）；S4 第209集「春花第二次報信」→「又一次」、第211集「當眾立下」十六歲規矩→「再說一次」（S1 第27集、S3 已報過信，S2 第83集已立規矩）；S4 第217–218集 押糧：「三年前」→「押糧那夜」，「到關口剩一百五十車」→「開袋全是沙」（對齊 S2 第102/105/106集換成沙），「三年的冤他從沒說過」→「那一夜的細節」（S2 第105集已說過案情）；S4 第222、227集「三年前」→「大半年前」；S4 第224集「倉以前給的字帖」→「娘照倉給的字帖抄成的本子」（倉的東西不過夜，r1；跟 S2 門板抄書同理）；S5 第254、294、299、300集「穿越三年／三年前」→「穿越以來／一年前」；S5 第257集 缺口碗「一直沒人動」「大丫三年沒讓人動」→「後來再沒人拿它盛飯」「守著的是原主最後一句話」、「空碗的來處」→「大丫為什麼守著空碗」（S1 那隻碗每頓盛第一碗、後來歸婆婆），同集大丫十四歲→十五歲；S5 第272–273集 刮鬍子「刮掉了三年的鬍子」「下頜線第一次露出來」「全村都認不出他」「第一次露出全臉」→「又長回來的一臉鬍子」「又露了出來」「全村看傻了眼」「又露出全臉」（S2 第110集她已替他刮過）；S5 第275集 小四「說出第二個詞」→「第一次開口叫他叔」（飽、肉在 S2，去在 S3，叫娘在 S4）；S5 第280集「他笑了——全劇第一次」→「笑開了——不再只是嘴角一彎」（S2 第105集他已第一次笑）。保留為刻意詮釋：格數的增長節奏（S1/S4 一天一格與「六百聲一格」、S2/S3 幾次一口氣跳數格、S2 與 S4 時間跳過時格數不跟日子走、S5 九十七格轉灶火色）照 outline 的總數與節點走，S2 起倉一天給好幾樣、寫過字／醃過／種下／繫上的東西留得住、紙上浮字會淡；S3 起村裡跟著霍青叫她阿滿；S4/S5 霍青鬍子長回來；狗娃、大柱、沙袋封條 S2 後不再出現；二郎三丫小四不長歲數、「荒年第三年」「你探了我三年」照 outline；石頭各季外貌提示詞不衝突；各季加的客串、支線與台詞改寫。季內未動（不屬 A/B）：S5 第270集樹皮信「走了十九天」，第244集送出到鎮北軍到村只隔十一天。
