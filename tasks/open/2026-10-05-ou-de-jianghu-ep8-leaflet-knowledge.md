---
id: 2026-10-05-ou-de-jianghu-ep8-leaflet-knowledge
title: 《偶的江湖》第 8 集交接：寫傳單的人怎麼比玄門先知道《裂山秘錄》不見了
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-05T12:19:43Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/series-plans/ou-de-jianghu
---

# 《偶的江湖》第 8 集交接：寫傳單的人怎麼比玄門先知道《裂山秘錄》不見了

## Why

第 4 集〈裂山秘錄〉a01 的經閣戲裡，沈歸鶴點出一個破綻：玄門經閣第 15 日上午才第一次打開、才發現秘錄不見，傳單卻在第 14 日夜裡就寫了「盜《裂山秘錄》西逃」。本集照分場表只讓他問一次、沒有人答（書院長老一句「紙是誰的，不要緊。秘錄不見了，是真的。」帶過）。企劃包 `season-01.json` 第 8 集〈鬼燈〉要在那一集揭開傳單是誰的筆（state.evidence 有「傳單紙的筆跡比對」與「兩名被收買的客院盟兵」），但沒有寫寫傳單的人**怎麼先知道**秘錄不見了。這個答案決定第 6–8 集要埋什麼（例如第 1 集當夜玄門長老身上那把經閣鑰匙的下落、或竹虛西行前有人見過他帶著秘錄函），不先定下來，第 6、7 集的分場表寫不準。

## Definition of done

- [ ] `season-01.json` 第 8 集（或它之前揭露的那一集）的 beats／state 寫明寫傳單的人是從哪裡、什麼時候知道秘錄不見的，並與第 1 集（長老身上的鑰匙、閉關之謊）、第 4 集（三把鑰匙：長老一把、竹虛一把、執事一把；經閣第 15 日才開）、第 5 集（盟兵被收買）的成品不矛盾。
- [ ] 要在第 6、7 集埋的伏筆列進那兩集的 beats（`season-01.json`），並寫進 `continuity.csv`／`continuity.md`。
- [ ] `node docs/videos/series-plans/ou-de-jianghu/build.mjs --check`、`validate.mjs`、`node --test validate.test.mjs` 通過；名字掃描 0 筆。

## Steps

- [ ] 1. 讀第 4 集成品 `docs/videos/ou-de-jianghu-e004/script.md` 的經閣戲（a01 第 42 鏡起）與 `production/ep4/beats.md` 第八節、第十一節「請主控確認」那一條。
- [ ] 2. 向站主提兩三個可選的答案（例：鑰匙在長老死的當夜被取走；竹虛出發前在經閣待了一夜被人看見；執事那一把鑰匙早就不在他手上），請站主選。
- [ ] 3. 照選定的答案改 `season-01.json` 第 6–8 集的 beats／state 與連戲表，重建並驗證企劃包。

## How to verify

```bash
D=docs/videos/series-plans/ou-de-jianghu
node $D/build.mjs --check && node $D/validate.mjs && node --test $D/validate.test.mjs
npm run check:tasks
```

## Notes

- 由票 `2026-10-04-ou-de-jianghu-e002-e005-scripts`（已關）拆出；第 4 集 `review.md`「已知問題」也記了這一條。
- 第 4 集成品已定：沈歸鶴只問一次、無人答；第 5 集執事把射寂聞的箭叫「第二支」，三宗認定長老死於無歸箭。答案不能讓第 4、5 集的任何一句台詞變成錯的。
