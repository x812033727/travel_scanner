# 寫一季逐集細綱（season-NN.json）的交辦單

給任何要替 `top40-2025-2026/<plan>/` 寫 `season-NN.json` 的人或代理。一次只寫一季、只寫那一個檔案（暫存檔放 scratchpad）。

## 先讀

1. 該目錄的 `plan.json`、`setting.json`、`outline.json`（你的那一季：6 個篇章的 beats／threads／end／spectacle／tones；上一季的 `end_state` 讓第 1 集接得上；最後一季再讀 `outline.ending`）、`README.md`。
2. 欄位規則：`../zhong-tian-qu-qi/authoring.md`；風格範例：`../zhong-tian-qu-qi/season-0N.json` 的前 3 集（`jq '.episodes[0:3]'`）。
3. 檢查器：`lib/validate.mjs`（規則以它為準）。

## 檔案形狀

```json
{ "number": N, "title": "…", "theme": "…", "start_state": "…", "end_state": "…",
  "guest_cast": [{ "id": "sNN-xxx", "name": "", "role": "", "appearance": "真人外貌提示詞" }],
  "threads": [{ "id": "sNN-t01", "question": "", "setup_episode": 0, "payoff_episode": 0 }],
  "episodes": [ 60 集 ] }
```

`title`／`theme`／`start_state`／`end_state` 從 outline.json 那一季**逐字抄**。

每集欄位（全部必填，除了 `extra_hooks`）：`number`（全劇集數）、`season_episode`（1–60）、`chapter`（1–6，每 10 集一章）、`title`（12 字內）、`youtube_title`（≤60 字；禁字：血、屍、裸、性感、火辣、慘死、自殺、自盡、血洗、屠、斬首、凌遲、酷刑）、`duration_s`（整數 90–180；季內第 10/20/30/40/50/60 集 ≥120）、`logline`、`hook`、`hook_type`（question／danger／image／line／reversal）、`mid_hook`、`extra_hooks`（可選，0–2 句；約一半的集數用，讓多數集有 4 個鉤子）、`conflict`、`turn`、`satisfaction`（≥2 個 `{beat,type}`，第一個 beat 在 opening 或 first_half）、`cliffhanger` `{type,text,question}`（type：danger／reveal／choice／reversal／emotion；question ≤30 字，第 300 集也要）、`lead_arc`（wins／suffers／mixed）、`tension`（5 個 1–5 的整數，不能全平，最後 ≥4）、`tones`（setting.tones 的 id；每個篇章要把 outline 列的調性都用到）、`spectacle`、`glamour_shot`、`setups`、`payoffs`、`reveals`、`general_payoffs`、`characters`（setting.characters 或本季 guest_cast 的 id）、`locations`、`state` `{time, knowledge, carry_forward}`。

## 檢查器會擋的

- hook、mid_hook、cliffhanger.text、extra_hooks 全部是不同的文字。
- 相鄰兩集的 cliffhanger.type 不同；主角不連兩集 suffers。
- 任何連續四集至少一集有 payoffs。
- 季內第 1 集的 cliffhanger.type **不是** reversal；第 60 集**是** reversal 且 lead_arc 不是 suffers。
- 短線（sNN-tNN）要先 setup 再 payoff，而且每一條都要收。
- setups／payoffs／reveals 的 id 只能是 m01–m12 或本季的 sNN-tNN。
- `reveals` 只能列 `reveal_season` 等於本季的謎團，每個謎團全劇只揭一次（交辦時會告訴你本季要揭哪幾個）；只能 setup／payoff `setup_season` ≤ 本季的謎團。
- 篇章的 `end` 就是季內第 10/20/30/40/50/60 集的結尾；第 60 集收在 `end_state` 的最後一個畫面。

## 怎麼寫才好看

- 每集的 hook 在前 10 秒接住上一集的 cliffhanger；每集都切在最高點；台詞一句 ≤10 字。
- 照 setting.json 的 advertiser_safety 與 glamour；每集一個奇觀、一個顏值鏡頭。
- 該劇的進度條（燈的亮暗、食單的頁數、帳本、原稿字……）每集都要看得見。

## 怎麼交

每 10 集（一章）寫一個暫存檔，用小腳本組成 `season-NN.json`，然後：

```bash
node docs/videos/series-plans/top40-2025-2026/lib/validate.mjs docs/videos/series-plans/top40-2025-2026/<plan> --season N
```

改到印出 `ok` 為止。回報：集數、檢查器輸出、哪裡不得不彎了 outline。
