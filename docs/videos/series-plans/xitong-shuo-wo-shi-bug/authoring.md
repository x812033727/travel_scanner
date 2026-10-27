# 逐集細綱的寫法（season-NN.json）

一季一個檔案，`node validate.mjs --season N` 要零錯誤，改完 `node build.mjs`。來源是 `setting.json`（世界、規則、人物與 image-01 外貌提示詞、謎團、調性、不黃標、顏值、貼圖規則）與 `outline.json`（每季六個篇章的劇情）。細綱只能展開與補細節，**不能改 outline 的事件、順序、誰拿回什麼、謎團在哪一季揭曉**。

這是**貼圖漫劇**（docs/videos/BINGE.md §畫面等級的 `manga`）：旁白說書帶故事，角色只講短句，每 2–3.5 秒一張靜圖、一鏡一句（2026-10-24 起；超過 4 秒 lint 會警告）、一張圖一個人，**每 30 秒一個鉤子**。動畫漫劇（種田娶妻打天下）的規格不適用。

## 檔案形狀

```json
{
  "number": 1,
  "title": "（照抄 outline 的季名）",
  "theme": "（照抄）",
  "start_state": "（照抄 outline）",
  "end_state": "（照抄 outline）",
  "guest_cast": [{ "id": "s01-xxx", "name": "", "role": "", "appearance": "（英文 image-01 提示詞，2D anime manhua style，一個人）" }],
  "threads": [{ "id": "s01-t01", "question": "這一季的短線懸念", "setup_episode": 3, "payoff_episode": 7 }],
  "episodes": [ { …每集… } ]
}
```

每集：

| 欄位 | 寫什麼 |
| --- | --- |
| `number` | 全劇集數 |
| `season_episode`、`chapter` | 季內 1–50、篇章 1–10（每篇章 5 集） |
| `title` | 集名，12 字以內 |
| `youtube_title` | 上架標題，60 字以內，爽文長標題（例：「加班猝死醒來只有撿垃圾技能，當晚我撿起全鎮丟掉的廢技」）；不劇透本集以後的答案，不用 validate.mjs 的禁字 |
| `duration_s` | 120–180；每篇章最後一集（第 5、10…集）至少 150 |
| `logline` | 一句話：誰、要什麼、被什麼擋 |
| `hook` | **前 3 秒**：第一個畫面＋第一句旁白或聲音（常常是一聲「叮」） |
| `hook_type` | question / danger / image / line / reversal |
| `mid_hook` | **中段鉤子**：片長一半左右丟出的新問題、新危機或新身份 |
| `hooks` | **每 30 秒的鉤子**：至少四個 `{at_s, text}`，第一個在 20 秒內、相鄰不超過 30 秒、最後一個離結尾不超過 30 秒，每個是不同的事（可以包含 hook 與 mid_hook 的那兩個）。寫成旁白會念出來的話：一個問題、一句「等一下它會回來」、一句「但這還不是最糟的」、一個揭露或反轉 |
| `conflict` | 這集要解決的事 |
| `turn` | 中段翻轉：觀眾以為的事變了 |
| `satisfaction` | 至少兩個 `{beat, type}`；第一個在 opening 或 first_half；type 用 face_slap、identity_reveal、counter_kill、level_up、first_clear、betrayer_punished、villain_humbled、hidden_power、public_vindication、rescue、reversal |
| `cliffhanger` | `{type, text, question}`，type 是 danger / reveal / choice / reversal / emotion；**相鄰兩集不同類型**；text 是最後一張圖＋最後一句；question 是觀眾帶走的問題（30 字內） |
| `lead_arc` | wins / suffers / mixed；江河不能連兩集 suffers |
| `tension` | 五個 1–5（開場、前半、中段、後半、結尾），不能全平，結尾至少 4 |
| `tones` | 這集用到的調性 id（shuang、xitong、xiju、xuanyi、ganren、zhandou）；每個篇章要把 outline 列的調性都用到 |
| `spectacle` | 這集值得截圖的一張圖，寫成一句可畫的畫面（一個人、一個發光的面板、一個地點） |
| `glamour_shot` | 顏值鏡頭：千凜或江河的一張臉 |
| `characters`、`locations` | 出場的 id（setting 或本季 guest_cast）與地點 |
| `setups`、`payoffs`、`reveals`、`general_payoffs` | 埋與收的 id（謎團 m01…、短線 s01-t01…）；`reveals` 只列本季揭曉的謎團，每條謎團全劇只揭一次；任何連續四集至少收一個 |
| `state` | `{time, knowledge, carry_forward}`：這集結束時的時間、觀眾知道了什麼、下一集要接的東西 |

## 貼圖漫劇寫法

- **旁白說書**：事件由旁白講，角色台詞一句一句短；面板的內容全由旁白念（「叮。是否安裝？」），圖裡的面板不寫字。2026-10-24 起留兩拍（參考片 37–45% 的時間沒人說話，句內講得快）：每個「叮」自成一句（`"text": "叮。"`、`"pause_after_ms": 500`），面板的字在下一句；揭曉或反轉前的那一句 `"pause_after_ms": 800`。旁白的聲音指示照說書人（節奏快、尾音乾脆、關鍵字加重）直接進 TTS，不再退回教學片的聲音。
- **旁白＝江河第一人稱吐槽**（2026-10-27 起，站主看完第 1–2 集說旁白不搭、慢、口氣怪）：照沙雕動畫的講法，旁白用「我」講、每句帶一個態度（吐槽、工程師梗比喻、反問、預告），一句 10–20 字、兩三句連著講；不寫「江河醒在垃圾坑裡」這種第三人稱純描述。參考片量到句內 5.8–7.6 字/秒、有聲 84–88%、幾乎不停頓；我們舊版 3.5 字/秒、每句後停 1 秒。「叮」接在句首不自成一句，只有揭曉前 pause_after_ms 600，其餘 0。
- **一圖一人**：每個 hook、spectacle、glamour_shot 都寫成一個人的畫面；兩人同框只在結尾一鏡。
- **面板不進外貌**：角色的 `appearance` 只寫人；面板只在那一鏡的 prompt 要它時才畫，英文寫成「a blank pane of pale-blue light, completely empty」，不用 system／screen／interface／UI／window／menu（image-01 會在上面畫字，judge 的 `text` 題就擋）。2026-10-24 第 1 集 s05 就是因為江河的外貌帶著「身旁浮著系統面板」，連「還沒有面板」的鏡頭也畫出帶字的面板，兩輪修提示詞都過不了。
- **沒有人形的角色給 `sheet_prompt`**：設定圖的提示詞預設是「character design sheet：正面、四分之三、全身、站姿」，系統這種沒有人形的角色不管外貌怎麼寫都會畫出人（2026-10-25 第 1 集重做六張全畫了人，退件也沒用）。2026-10-25 起（#1855）角色可以給 `sheet_prompt` 覆寫整句：系統寫成「one single blank rectangular pane of pale-blue light … no people, no silhouettes, no text」，設定集改了就會帶進每一集；單集 video.json 手改沒用，作品的 `settle()` 會把角色換回設定集。
- **外貌不寫細小記號**：疤、痣、雀斑、耳洞這種小記號 image-01 畫不穩，設定圖常常沒有，manga 等級的 judge 身分題卻會問「記號少了或多了」，就一直重畫。2026-10-24 第 1 集 16 鏡卡住，13 鏡是江河左眉那道疤（設定圖五張都沒畫出來）；外貌只寫大的、遠看認得出的特徵（髮型、髮色、衣服、配件）。
- **系統的聲音**：`xitong` 是角色 id，它的台詞是面板的字；它第一季只在第 30 集說一句人話。
- **數字不灌水**：等級、技能都到兩位數；爽在「合併出什麼」。
- 不黃標與顏值規則照 `setting.json`。
