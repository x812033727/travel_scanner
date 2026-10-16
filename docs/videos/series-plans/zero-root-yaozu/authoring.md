# 逐集細綱的寫法（season-NN.json）

每一季一個檔案，`node validate.mjs --season N` 要零錯誤。來源是 `setting.json`（世界、人物、規則、謎團、調性、不黃標、顏值規則）與 `outline.json`（十季、每季六個篇章的劇情）。細綱只能展開與補細節，**不能改 outline 的事件、順序、誰死誰活、謎團在哪一季揭曉**。

## 檔案形狀

```json
{
  "number": 1,
  "title": "（照抄 outline 的季名）",
  "theme": "（照抄）",
  "start_state": "（照抄 outline）",
  "end_state": "（照抄 outline）",
  "guest_cast": [{ "id": "s01-xxx", "name": "", "role": "", "appearance": "（真人外貌提示詞，美型，照 glamour）" }],
  "threads": [{ "id": "s01-t01", "question": "這一季的短線懸念", "setup_episode": 3, "payoff_episode": 7 }],
  "episodes": [ { …每集… } ]
}
```

每集：

| 欄位 | 寫什麼 |
| --- | --- |
| `number` | 全劇集數（第二季從 61 開始） |
| `season_episode`、`chapter` | 季內 1–60、篇章 1–6 |
| `title` | 集名，12 字以內 |
| `youtube_title` | 上架標題，60 字以內，短劇式爽點長標題（例：「測出零靈根被當眾羞辱，回村才發現奶奶一刀能劈開仙門」）；不劇透本集以後的答案，不用 validate.mjs 的禁字 |
| `duration_s` | 50–180；每篇章最後一集（第 10、20…集）至少 120；動作集 60–100、揭密與感情集 100–150 |
| `logline` | 一句話：誰、要什麼、被什麼擋 |
| `hook` | **前 3 秒**：第一個畫面＋第一句台詞（或第一個聲音），要讓人停下滑動 |
| `hook_type` | question / danger / image / line / reversal |
| `hooks` | **片中鉤子**（站主 2026-10-16：一集要兩三個以上）：至少三個 `{at_s, type, text, question}`，依時間排序；從開頭到第一個、相鄰兩個、最後一個到片尾都不超過 30 秒（180 秒的集就要五個以上）。每個都是新問題、新危機、反轉、揭露或怪東西，type 用 hook_type 的五種；question 是它讓觀眾想知道的事（30 字內）；不能和開頭鉤子、結尾懸念是同一件事 |
| `conflict` | 這集要解決的事 |
| `turn` | 中段翻轉：觀眾以為的事變了 |
| `satisfaction` | 至少兩個 `{beat, type}`；第一個在 opening 或 first_half；type 用 face_slap、identity_reveal、counter_kill、level_up、first_clear、betrayer_punished、villain_humbled、hidden_power、public_vindication、rescue、reversal |
| `cliffhanger` | `{type, text, question}`，type 是 danger / reveal / choice / reversal / emotion；**相鄰兩集不同類型**；text 是最後一個畫面＋最後一句；question 是觀眾帶走的問題（30 字內，例如「奶奶的尾巴是真的嗎？」；第 600 集可省略） |
| `lead_arc` | wins / suffers / mixed；**陸拾不能連兩集 suffers** |
| `tension` | 五個 1–5（開場、前半、中段、後半、結尾），不能全平，結尾至少 4（第 600 集例外：≤3） |
| `tones` | 這集用到的調性 id（goxue、henla、ganren、kongbu、kehuan、texiao）；每個篇章要把 outline 列的調性都用到 |
| `spectacle` | 這集值得截圖的海螺奇觀鏡頭，寫成一句可拍的畫面 |
| `glamour_shot` | 這集的顏值鏡頭（誰、什麼動作、什麼光），照 setting.glamour 的 do／dont |
| `setups`、`payoffs` | 謎團 id（m01…）或本季短線 id（sNN-t01…）；**任何連續四集至少一集有 payoffs**；短線要先 setup 才能 payoff，而且每條短線都要收 |
| `reveals` | 這集**完整揭曉**的謎團 id；只能在 setting.mysteries 的 reveal_season 那一季、全劇只揭一次 |
| `general_payoffs` | 這集落袋的具體成果（救下誰、拿到什麼、關係進了一步），可空 |
| `characters` | 人物 id（setting.characters、setting.beasts 或本季 guest_cast） |
| `locations` | 場景名稱 |
| `state` | `{time, knowledge, carry_forward}`：這集結束時的時間點、陸拾已知什麼、留給下一集的東西 |

## 寫的時候要守的

1. **看得懂、接得上**：每集的 hook 要接上一集的 cliffhanger（同一個場面或它的直接後果），不靠旁白回顧；新角色第一次出場用一個動作讓人記住他是誰。
2. **收在最高點（最重要）**：每集切在張力最高的那一秒：刀落下前、門打開的瞬間、答案說出口前一個字、某人轉身露出臉的那一格、一句改變一切的台詞剛說完。**絕不收在事情已經解決之後**，也不收在角色在想、在走路、在感嘆。下一集的 hook 在前 10 秒內直接接住 cliffhanger.question（同一個畫面接下去，或立刻給出代價更大的答案）。
3. **每集五個以上鉤子**：開頭 3 秒（hook）、片中至少三個（hooks，間隔不超過 30 秒）、結尾（cliffhanger），各是不同的事；觀眾每半分鐘都有一個「然後呢？」。
4. **每集都有一件事發生**：不能整集只是對話或趕路；每集至少一個爽點落地。
5. **規則有代價**：妖祖出了圖影只剩一兩成力（r2）；燭淚眼每用一次天眼就看見他（r3）；聚靈盆一天一次（r5）。不要讓長輩一出手就解決所有事。
6. **不黃標**：照 setting.advertiser_safety；死亡化光、化灰、切走；兒童遇險不受傷；不寫自殘；恐怖靠聲音與暗處。
7. **顏值**：照 setting.glamour；身材靠勁裝與動作，不拍暴露、不停在身體部位。
8. **原創**：不借任何既有作品的人名、門派、招式、台詞；山海經、莊子等古籍的神獸與國名可以用。
9. 台詞感：細綱裡引用的台詞一句 10 字以內，像人說話。
