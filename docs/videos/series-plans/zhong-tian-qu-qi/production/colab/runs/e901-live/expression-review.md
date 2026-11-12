# e901 真人版：逐鏡表情審查（2026-11-08）

站主：「我發現有些角色都沒表情，應該每個都要有表情，除非是劇情要求要沒表情，你再幫我審核一下看看」。

## 怎麼審的

- 素材：`picks.json` 選定的 39 支 draft（960×544），只看 trim 內的片段。`runpod/a/st2/refined/sNN.mp4` 是 11/06 的 3D CG 路線 A 成品，不是真人版，所以這次沒有用；真人版精修會保留同一段表演，判斷以 draft 為準。
- 每鏡每 0.5 秒抽一格，看得到臉但臉太小的鏡頭（全景、雙人鏡、過肩）再裁臉放大看。下面的時間是**該鏡 draft 內的秒數**（有 start trim 的從 trim 起算，例如 s08 從 0.75 秒開始）；「成片起點」是 `cut/final.log` 裡該鏡在成片中的開始時間。
- 對照：`video.json` 每句台詞的 emotion、每鏡 prompt／motion，以及實際送出的 prompt（`runpod/live/{d1,fix1..fix4}/prompts/ref-sNN-<選中的 seed>.txt`），還有 `assets/refs-live/` 的定妝照。
- 評等：**OK**／**偏平**（有一點但太淡，情緒讀不出來）／**沒表情**（像假人、像定妝照）／**錯**（演成別的情緒）。劇本本來就要冷臉或低頭的（秦霜冷眼、阿令低頭、背影鏡）算 OK，表中註明「劇本要求」。

## 總表

| 鏡 | 成片起點 | 角色 | 劇本要的 | 畫面上（draft 秒數） | 評等 |
|---|---|---|---|---|---|
| s01 | 0:00 | 面試官（只有手） | 畫外，冷淡 | 桌面插入鏡，沒有臉 | 不適用 |
| s02 | 0:08 | 許硯 | 壓著火，很穩：禮貌的笑收掉→咬牙、眉壓低、眼神硬 | 0–2.5 一直笑得很開朗；3–4.5 眉毛平、嘴在講話，沒有咬牙，也沒有硬起來的眼神；5–6.5 平靜，像普通面試 | 偏平（怒氣幾乎沒出來） |
| s03 | 0:14 | 許硯 | 低聲自嘲（背影） | 背影＋閃電，臉看不到 | OK（劇本要求背影） |
| s04 | 0:20 | 許硯 | 水下驚醒 | 0–2.5 閉眼；3.0 猛睜眼、眼睛瞪大；3.5–6 嘴張成 O 吐氣泡，驚慌 | OK |
| s05 | 0:27 | 二牛、許硯 | 又急又喘；許硯昏迷 | 全景，臉小；1.5–3.5 二牛咬牙使力、張嘴喘；許硯軟癱 | OK |
| s06 | 0:34 | 許硯 | 嗆咳，迷糊 | 0 半昏張嘴（有）；1–5 嘴在講話但表情很平，沒有咳也沒有迷糊；6 皺眉瞇眼看人（有） | 偏平 |
| s07 | 0:40 | 二牛 | 憨笑，鬆一口氣 | 0–3 講話表情生動；3.5 抹臉；4.5–6 大大鬆口氣的笑 | OK |
| s08 | 0:47 | 許硯（眼睛特寫） | 聽到聲音，找來源、皺眉 | 1.75–3.75 眼睛左右找；3.75 起眉頭微皺 | OK |
| s08b | 0:52 | 許硯 | 困惑（心裡話） | 0–7.5 低頭看手，眉頭平順、臉很平靜，看不出「誰在說話？」的困惑 | 偏平 |
| s09 | 1:00 | 許硯 | 試探 | 0–6.5 講話時臉平平的，眉毛沒動 | 偏平 |
| s10 | 1:06 | 二牛（許硯是背影） | 壓低聲音報壞消息（笑容收起） | 0–2 一邊說欠錢一邊笑；3 回頭看村子；4.5–6 轉回來，眉毛上揚、還帶著笑意，不是擔心 | 錯（笑著報壞消息） |
| s11 | 1:13 | 許硯、二牛 | 吸一口氣，打起精神 | 全景；1 許硯有一點笑意，其餘時間兩人都平 | 偏平（可接受） |
| s12 | 1:19 | 小禾（許硯、二牛） | 愣住，然後哭出來 | 1.0 臉皺了一下；2–5 側臉發呆；5.5–6 喊「哥哥」，嘴張成 O，是吃驚，沒有要哭 | 偏平 |
| s13 | 1:24 | 小禾、許硯 | 哭腔撲上去；許硯愣住 | 0–1 小禾**咧嘴笑**著轉身；2–6 抱腰時臉皺起來在哭（有）；許硯低頭，表情平 | OK（0–1 秒小禾在笑，見下文） |
| s14 | 1:31 | 許硯 | 愣住（心裡話）→放軟安慰 | 0–4 低頭（愣住，可）；5–9 低頭說話，眼神柔和；9 有一點微笑 | OK（偏淡） |
| s15 | 1:41 | 小禾 | 害怕 | 0–5.5 紅眼、眉頭往上皺、快哭；3.5–4 用袖子擦眼睛 | OK |
| s16 | 1:48 | （手） | 米缸插入鏡 | 沒有臉 | 不適用 |
| s17 | 1:54 | 許硯 | 苦笑、嘆氣 | 0–3 有笑意；4–5 **開心大笑**；6 開朗講話；看不到嘆氣、無奈 | 錯（苦笑演成開心） |
| s18 | 2:01 | 小禾、許硯 | 小禾懂事（說自己不餓）；許硯看碗再看她（心疼） | 小禾 1–6 平平地講話，看不出逞強或心疼；許硯 0–6 瞪著前方發呆，5–6 甚至有點兇 | 沒表情 |
| s19 | 2:08 | 許硯 | 認真發誓：「從今天起，哥不會再讓你餓肚子」 | 1.5–2 低頭倒粥時微笑；3–6 講話表情平順、略帶客氣，沒有決心、沒有溫柔 | 偏平（這場的情緒高點沒出來） |
| s20 | 2:14 | 趙捕頭（只有腳） | 粗聲喊門 | 踹門插入鏡，沒有臉 | 不適用 |
| s21 | 2:21 | 趙捕頭 | 念告示（官腔、斜眼） | 0–3 念得平平的；4–5 有斜眼 | 偏平（可接受） |
| s22 | 2:28 | 趙捕頭（許硯是背影） | 許硯慌；趙大步逼近 | 許硯背影（劇本要求）；趙 2–6 走近停下，臉完全中性，沒有不耐煩或盛氣凌人 | 沒表情（趙） |
| s23 | 2:34 | 趙捕頭、秦霜、阿令 | 趙冷笑；秦霜抬下巴；阿令低頭 | 趙 0–1 **咧嘴大笑**，很親切，1.0 才有一點斜笑；秦霜 1.5–6 平視、表情穩（抬下巴不明顯）；阿令全程低頭 | 錯（趙）；秦霜偏平；阿令 OK（劇本要求） |
| s24 | 2:41 | 秦霜（許硯） | 不屑：「就這身板？」 | 0–2 雙手抱胸、表情平靜；3–6 對著許硯講話，臉中性，沒有撇嘴、沒有斜眼、沒有冷笑；許硯半邊臉，平 | 沒表情（她第一句台詞） |
| s25 | 2:48 | 許硯 | 自嘲，乾笑 | 0–3 講話；3.5 甩袖；4.5–6 笑出來（稍嫌開心，但算乾笑） | OK |
| s26 | 2:54 | 阿令（手腕） | 插入鏡 | 沒有臉 | 不適用 |
| s27 | 3:01 | 許硯 | 皺眉，低聲 | 2–3.5 眉頭稍壓，其餘時間是正常講話的臉 | 偏平（可接受） |
| s28 | 3:07 | 趙捕頭 | 冷笑 | 0–6 瞇眼斜看、嘴角往下、往前壓過來，兇 | OK |
| s29 | 3:14 | 許硯 | 不疾不徐，有把握的微笑 | 0–6 眉毛上揚、帶笑講話，比較像熱情而不是沉穩，但有自信 | OK |
| s30 | 3:21 | 趙捕頭、秦霜 | 趙語塞；秦霜有點意外、挑眉 | 趙 0–1 張嘴愣住、之後洩氣；秦霜 0.5–4.5 表情生動，5–5.5 嘴角一勾 | OK |
| s31 | 3:27 | 趙捕頭、許硯 | 找台階下（悻悻然）→不耐煩一指 | 趙 0.5–1、7–7.5 **咧嘴笑得很和氣**；許硯側臉平靜 | 錯（趙） |
| s32 | 3:39 | 唐小棠 | 甜，輕快 | 0.5–6 一路開心笑著揮手 | OK |
| s33 | 3:46 | 秦霜 | 嗤笑 | 1–4 斜眼上下打量；5–6 一邊嘴角冷笑 | OK |
| s34 | 3:52 | 唐小棠、秦霜 | 唐甜甜頂回去；秦霜冷眼 | 唐全程甜笑、轉頭；秦霜抱胸冷臉 | OK（秦霜冷臉是劇本要求） |
| s35 | 4:04 | 許硯、二牛 | 許硯愣住；二牛樂 | 許硯全程平視、不笑（劇本寫愣住、發呆），但眉毛沒抬、嘴沒鬆，比較像沒表情而不是嚇呆；二牛 3–12 一直咧嘴笑 | 偏平（許硯；劇本本來就要呆，可接受） |
| s36 | 4:16 | 許硯 | 聽到「三日內與三人成婚」，瞳孔一縮、眼睛瞪大 | 選中的這支不是眼睛特寫，是整張臉；0–4.5 陰沉地直視鏡頭，沒有瞪大、沒有吃驚 | 偏平 |
| s37 | 4:21 | 許硯 | 臉色發白，「抹……殺？」 | 5.5–7 平；7.5–9.5 眼睛瞪大、嘴張開，驚嚇 | OK |
| s38 | 4:31 | 秦霜、唐小棠、阿令 | 秦霜冷、平；唐好奇；阿令低頭，最後抬眼看鏡頭 | 秦霜冷臉；唐微笑歪頭；阿令 0–7 低頭，7.5 抬眼，臉平 | OK（劇本要求；阿令最後一眼可以更有戲，見下文） |

### 統計（39 鏡）

- 看不到臉、不適用：5 鏡（s01、s16、s20、s26 是插入鏡；s03 是背影）。
- 看得到臉的 34 鏡：**OK 16**、**偏平 11**、**沒表情 3**、**錯 4**。
  - 偏平：s02、s06、s08b、s09、s11、s12、s19、s21、s27、s35、s36
  - 沒表情：s18、s22、s24
  - 錯：s10、s17、s23、s31
- 主角許硯是最大宗：他的對白鏡多半是「嘴有對上，臉是定妝照」（s02、s06、s08b、s09、s18、s19、s36）。

## 值得重拍的鏡

### 嚴重：這場戲的情緒重點不見了

1. **s02（壓著火）**：全集的開場鉤子，觀眾要在這裡感覺到主角的骨氣。現在前 2.5 秒在開心地笑，後面是平的。（成片審查第 18 項已經記過。）
2. **s19（「從今天起，哥不會再讓你餓肚子」）**：屋內這場的情緒高點，許硯的承諾。畫面上是一張客氣的平臉，送出的 prompt 裡沒有任何情緒字。
3. **s24（秦霜：「就這身板？」）**：秦霜第一次開口，角色個性靠這一句的不屑建立。prompt 寫了 "her face scornful"，畫面是中性的臉。
4. **s18（半碗粥）**：小禾說「我不餓」、許硯心疼，是 s19 承諾的動機。兩人都沒表情，prompt 裡也沒有情緒字。

### 中等：情緒不對，觀眾會覺得怪（有預算再重拍）

5. **s17（苦笑）**：演成開心的笑，跟「米缸都快見底了」的台詞衝突。
6. **s10（二牛報壞消息）**：笑著說「就拿你家的地抵」。
7. **s31（趙捕頭找台階下、不耐煩）**：咧嘴笑得很和氣，等於把反派演成好人。
8. **s23（趙捕頭冷笑）**：開頭 1 秒是親切的大笑。成片也可以從 1.0 秒開始剪，先避開最明顯的那段。
9. **s12（小禾愣住→哭）**：沒有要哭，只有吃驚。哭在 s13 才出來，所以還能接受。
10. **s22（趙捕頭逼近）**：臉是空的。全景＋過肩，影響比較小。
11. **s36（系統宣布任務）**：選中的那支不是眼睛特寫，臉也沒有吃驚，接下來的 s37 才補上驚嚇。

### 可接受（不重拍，或只修剪）

- **s13**：0–1 秒小禾咧嘴笑著轉身，之後哭得很好。可以考慮從 0.75–1.0 秒開始剪；不剪也只是一閃而過。
- s06、s08b、s09、s11、s21、s27、s35：偏淡，但不是這場的重點，或劇本本來就要呆、要平。
- s38 阿令最後抬眼：劇本只寫「看向鏡頭」，所以中性的臉不算錯。這是片尾鉤子，之後的集數可以寫成有戲的一眼（見下文的寫法）。

## 原因：送出的 prompt 怎麼寫的

### 1. 中文的情緒標註根本沒有進 prompt

`video.json` 每句台詞的 `emotion`（認真、懂事、不屑、壓低聲音、不耐煩、困惑、試探……）只用在配音。送出的 prompt 只有 `Xu Yan speaks a short Mandarin line, 「…」, his lips, jaw and cheeks moving clearly with every syllable in natural talking mouth shapes`，也就是說嘴巴怎麼動寫得很仔細，臉上什麼情緒一個字都沒有。
英文 motion 沒寫情緒的鏡頭，畫出來全是平臉：**s18、s19、s22、s31**（用關鍵字掃過，這幾支選中的 prompt 裡沒有任何表情字；出現的 "blank" 指的是紅紙背面）。s08b、s09 也一樣：「困惑」「試探」只出現在中文。

### 2. 定妝照全是中性的棚拍臉，而且收尾句又把臉鎖回定妝照

`refs-live/` 的定妝照七個角色都是面無表情的證件照式棚拍。每支 prompt 的最後一句都是（`live-action/pilot.py` 的 `STYLE_NEW[1]`）：

> Natural, realistic human motion of real actors; **faces, hair and costumes stay as in their reference pictures.**

前面雖然有 `ref2manifest.mjs` 加的 "Facial expressions follow the action and lines described below, not the reference pictures: the pictures fix the face, hair and costume only, never the mood."，但最後一句又說「臉跟定妝照一樣」，兩句互相矛盾，排在最後的那句贏。「臉」對模型來說同時是長相和表情。只要文字沒寫情緒，就回到定妝照那張平臉。

CG 版的情況剛好相反：定妝照在笑，所以系列規則寫成「沒寫就是嚴肅，不笑」（`storyboard-brief-for-planners.md` 第 5 項、`r2-bible-e001-e010.md` 第 6 條、`r2.py` 檔頭的 "default face is serious"）。換成中性的真人定妝照以後，這條規則就變成「沒寫就沒表情」。

### 3. 只寫形容詞、不寫臉怎麼動，模型會丟掉修飾、只留主詞

| 鏡 | 寫的 | 畫出來 |
|---|---|---|
| s24 | "her face scornful"、"with a cool tilt of her head" | 中性臉（"cool" 反而把臉拉平） |
| s17 | "turns his head with a rueful smile" | 開心的笑（"rueful" 丟了，只剩 smile） |
| s23 | "Zhao gives a cold smirk" | 親切的大笑（"cold" 丟了，只剩笑） |
| s10 | "Erniu's grin fades"（之後沒寫換成什麼臉） | 一直帶著笑（模型只讀到 grin） |
| s02 | "he opens with a small polite smile that fades…"，生氣寫在後面 | 前 2.5 秒在笑，生氣很淡（先寫的笑占了上風） |

### 4. 有成功的鏡，都是把臉的部位一個一個寫出來

| 鏡 | 寫法 | 結果 |
|---|---|---|
| s15 | "frightened: her eyes red and wet, her brows drawn up in the middle, her lower lip trembling, no smile the whole shot" | 害怕、快哭，OK |
| s28 | "his narrow eyes sliding sideways…, the corners of his mouth turned down"，加上往前壓過去 | 兇、冷笑，OK |
| s33 | "her eyes running from the silk sleeves down to the shoes, … a short scornful snort through her nose, one corner of her mouth lifting" | 嗤笑，OK |
| s37 | "his lips tremble, his throat bobs as he swallows hard, … half a step back as if struck" | 驚嚇，OK |
| s07 | 用動作帶出情緒："wipes the water off his face…, slaps his own chest…, lets out a big breath and breaks into a relieved grin" | 鬆一口氣，OK |
| s13 | "her shoulders shaking as she sobs" | 哭，OK |

結論：要寫**看得見的部位**（眉、眼、嘴角、下巴、喉嚨、呼吸），再加一個**動作上的情緒節拍**（嘆氣、哼一聲、吞口水）。要不笑的地方，明寫「不是開心的笑」。

### 5. 其他小因素

- 河邊每一鏡結尾都有 "the cool grey dawn mist stays unchanged"，辦公室是 "cold white lights"。這些字本來是講光，但跟 "cool tilt of her head"（s24）這種寫法放在一起，冷調的字會更多。真人版的情緒字要避開 cool、calm、steady、level 這類字，除非這鏡真的要冷臉。
- 對白鏡的鏡位常是全景、雙人或過肩（s05、s11、s12、s18、s22、s23）。臉在畫面裡只有幾十像素，就算有表情也很難讀。情緒重點的台詞，鏡位至少要到中近景。

## 給工具的改寫建議（讓之後的集數不再發生）

以下只是提案，這次沒有改任何工具檔。

### A. `live-action/pilot.py` 的收尾句

把「臉跟定妝照一樣」拆成「長相跟定妝照一樣，表情照文字演」，而且不要再出現 "faces … stay as in their reference pictures"：

```python
STYLE_NEW = ["[Shot 1] Photorealistic live-action film footage of real actors in an ancient Chinese (Song-dynasty) period drama, shot on a cinema camera.",
             "Natural, realistic human motion and acting of real actors: each person keeps the identity, hair and costume of their "
             "reference pictures, while every visible face acts the emotion written above and changes with it; the pictures are "
             "neutral studio portraits, never copy their blank expression."]
SOAKED_LOCK = ("Natural, realistic human motion and acting of real actors: each person keeps the identity of their reference "
               "pictures while every visible face acts the emotion written above, and hair and costumes keep the cut and colour "
               "of their pictures, soaked and dripping wet the whole shot as described above.")
```

（`STYLE_OLD` 不用改。`if SOAKED_MARK in text: text.replace(STYLE_NEW[1], SOAKED_LOCK)` 這段照舊可以用。）

`colab/ref2manifest.mjs` 的 faces 句也建議改成同樣的意思，並讓它排在 prompt 後段，靠近收尾：

> "Every visible face acts: its expression follows the emotion written for it below and changes with the action; the reference pictures fix identity, hair and costume only, never the expression."

### B. `writer-tools/eNNN-r2/r2.py`：每鏡每個露臉的人都要有 `face`

1. 檔頭規則改掉：`default face is serious, smiling only where the script says so` → `live action: every visible face gets an expression written as physical cues (brows, eyes, mouth, jaw, breath); "serious" is written out as a face too; no smile where the script does not ask for one`。
2. `SHOTS` 每鏡加一個欄位 `face={"xuyan": "...", "xiaohe": "..."}`，`build-r2.py` 把它接在說話句的後面，用一個固定句型：

   ```
   {Name} speaks a short Mandarin line, 「…」, {face[name]}, his lips, jaw and cheeks moving clearly with every syllable
   ```

   不說話但露臉的人，把 face 接在他的動作後面。
3. `build-r2.py` 加一個檢查（或放進 shot_reading）：
   - 露臉的角色（不在 `nospeak` 背影、不是插入鏡）沒有 `face` → 失敗。
   - `face` 裡至少要有一個部位字（brow／eye／mouth／lip／jaw／chin／tear／nostril／throat／breath）。只有形容詞（scornful、rueful、cold、warm、earnest）→ 失敗。
   - 寫了 smile／grin，但台詞的 emotion 是苦笑、冷笑、壓低聲音、不耐煩、害怕、哭腔 → 要求同一句裡出現 `not a happy smile` 或 `no teeth` 這類限定。
   - 出現 `grin fades`／`smile fades`，後面卻沒寫換成什麼臉 → 失敗。
   - 真人版的 face 不准出現 cool／calm／steady／level／neutral，除非該角色是劇本要冷臉（秦霜、阿令）。
4. 台詞 emotion 對英文的備用表：作者忘了寫 face 時，`build-r2.py` 至少把 emotion 翻成臉放進去，不讓它空白（之後由作者覆寫）。例如：

   | emotion | 英文的臉 |
   |---|---|
   | 壓著火 | jaw clenched, brows pulled down hard, eyes narrowed and fixed, lips pressed thin between words, no smile |
   | 認真 | brows level and set, eyes steady and warm on her, jaw firm, a small resolute nod, no grin |
   | 懂事 | a small brave smile that trembles at the corners, eyes shining, pretending not to be hungry |
   | 苦笑 | a crooked tired smile that does not reach his eyes, brows drawn up in the middle, a long sigh, not a happy smile |
   | 不屑 | chin raised, eyes half-lidded looking down her nose at him, one corner of her mouth curled up, one eyebrow cocked |
   | 冷笑 | one corner of the mouth curling up in a thin sneer, lips closed, eyes narrowed and sliding sideways, no teeth, not a friendly smile |
   | 壓低聲音（報壞消息） | no smile at all, brows knotted with worry, eyes darting toward the path, mouth tight |
   | 不耐煩 | an impatient scowl, brows clamped down, a sharp breath through the nose, no smile |
   | 困惑 | brows pinched together, eyes darting, a puzzled frown |
   | 試探 | head tilted, brows slightly raised, eyes wary and searching |
   | 愣住 | eyes wide and fixed, brows raised, mouth slightly open, frozen |
   | 慌 | eyes wide, brows shot up, mouth open, breathing fast |
   | 嗆咳，迷糊 | eyes half-lidded and unfocused, face screwed up as he coughs |

### C. 重拍這幾鏡的改寫範例（`r2.py` 的 comp／motion）

- **s02**：拿掉開場的笑，或限縮成「最多第一秒」。comp 結尾改成："…his eyes on the interviewer off screen right; from his first word his face is held-back anger: jaw clenched, brows pulled down hard and low, eyes narrowed and fixed on the interviewer, nostrils flared, lips pressed thin between words; at most a brief tight polite smile in the first second, gone before he speaks, never again"
- **s18**：小禾 "…pushes the bowl across the low table to Xu Yan with both hands, with a small brave smile that trembles at the corners, her eyes shining, pretending she is not hungry"；許硯 "Xu Yan looks from the bowl up to her, his brows drawing up in the middle and his eyes glistening, his throat tightening, moved and pained, his lips closed, no smile"
- **s19**：說話句後接 "his jaw firm, his brows level and set, his eyes steady and warm on her, a quiet determined look, a small resolute nod on 「從今天起」, no grin"
- **s24**：comp 的 "her face scornful" 改成 "chin raised, eyes half-lidded looking down her nose at him, one corner of her mouth curled up in a contemptuous half-smile"；motion 把 "with a cool tilt of her head" 改成 "with one eyebrow cocked, and on 「吹回河裡」 she gives a short snort through her nose"
- **s17**："lets out a long sigh that drops his shoulders, shakes his head once, and turns to Xiaohe off screen right with a crooked, tired smile that does not reach his eyes, his brows drawn up in the middle — a bitter, helpless smile, not a happy one"
- **s10**："Erniu's grin vanishes completely; his brows knot with worry, … he hunches lower and speaks low and urgent, his mouth tight, no smile again to the end"
- **s23**："Zhao's mouth curls up at one corner in a thin cold sneer, lips closed, his eyes narrowed and sliding sideways at Xu Yan, no teeth, not a friendly smile"
- **s31**："for the first line a sour, grudging face, lips pursed, brows lowered, a sharp breath through his nose as he gives in; for the second line, looking back over his shoulder, an impatient scowl as he jerks his thumb at the gate; he never smiles"
- **s22**：趙 "his brows clamped down in an impatient scowl, jaw thrust forward, eyes hard and looking down on Xu Yan"
- **s12**：小禾 "freezes, eyes wide, her chin starts to wobble, her face crumples and tears well up as she cries out 「哥哥！」"
- **s36**：眼睛特寫保留，motion 改成 "his eyes go wide in shock, the whites showing around the irises, his brows shoot up, he blinks once, slowly"
- （之後的集數）**s38 阿令最後一眼**："she slowly raises her eyes and looks straight into the lens, a guarded, wary look, her lips pressed together, a flicker of defiance"

### D. 規則文件（建議同步改，這次沒改）

- `storyboard-brief-for-planners.md` 第 5 項「沒寫就是嚴肅，不笑」→ 真人版：「每個露臉的人每鏡都寫表情，寫部位（眉、眼、嘴角、下巴、呼吸），嚴肅也要寫成一張具體的臉；不笑的地方寫『不是開心的笑』」。檢查清單第 212 行同步改。
- `r2-bible-e001-e010.md` 第 6 條同上。
- 鏡位：情緒重點那句台詞（s19、s24、s02 這種）至少要中近景，不要用全景或過肩去拍。
