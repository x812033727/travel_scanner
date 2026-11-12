# 審劇本：把劇本寫成分鏡、產生鏡位與注意事項

站主 2026-11-06 要的做法，跟《種田》r2 第 1–60 集實際跑過的一樣。站主說「審劇本」「審片」「審稿」「把劇本變分鏡」「產生鏡位跟注意事項」，而對象是**還沒拍的劇本或分鏡**時，照這份做。
已經拍好的片段要審，走製作端的審片（例如 `minimax-h3-colab` 的 lessons），不是這份。

每一鏡怎麼寫、三道檢查的細節，都在 [`storyboard-shot-spec.md`](storyboard-shot-spec.md)。這份只講**順序、分工和交辦怎麼寫**。

## 產出

每集一份 `docs/videos/<slug>/script.md`，製作端照抄就能拍：
- 劇情、這集接在哪、角色與參考圖。
- 每場的場頭：場景圖、時間與光、軸線、在場的人與進出、這場講完的事、配樂、怎麼離開。
- 六欄分鏡，也就是鏡位：`| 鏡 | 景別、運鏡 | 畫面裡有誰 | 動作 | 台詞 | 秒數 |`。台詞標「→ 答在」「← 因為」「（結尾）」「（懸念 → …）」。
- 注意事項：這版改了什麼（含哪些台詞要重錄、哪些片段要重抽）、配音、音樂與音效、剪接。
- 五張清單：造型、參考圖、長鏡、音樂與音效、時間與帳。

另外有一份系列設定，放所有集共用的帳與接點。

## 拍法：種田拍法（每一部劇都照做）

站主 2026-11-08 看了《恁祖媽今年18》第 1–3 集後說「種田那邊比較順」，要求第 1–3 集照種田的拍法重做，並說「以後應該也要都用這樣的拍法」。
審劇本、寫分鏡、審稿都照這一節。祖媽第 1 集 v2 照這樣重拍過，審片學到的事也寫在這裡。

**鏡數與節奏**
- 一鏡約 2.5–3 秒；說話的鏡照台詞長度（約每秒 4–5 字，原聲鏡至少買 6 秒）。
- 一集 2.5 分鐘約 45–50 鏡，換算約每分鐘 18–20 鏡。
- 每一鏡都有一個看得見的動作。剪點放在動作中間（起身起到一半、轉頭轉到一半），不放在動作做完之後的靜止。

**一場戲的鏡頭順序**（覆蓋）
1. 帶運鏡的全景或主觀鏡，交代場地與每個人的位置。
2. 過肩與反打，交代誰對誰說話。
3. 手與道具的插鏡。
4. 反應特寫。
- 多數鏡頭有前景，例如椅背、門框、桌角、柱子、對方的肩。
- 同一場守住軸線。要越軸就拍一鏡有人走過去。

**臉**
- 每張看得到的臉都寫具體表情：眉、眼、嘴角、下巴、呼吸，至少兩處。劇情要求木然的才寫木然。
- 定妝描述（`cast.json`）不寫笑容也不寫姿勢，姿勢由每鏡的動作決定。
- 講話的人面向聽的人，臉是側面或四分之三側臉。沒有人看鏡頭，聽的人也不看。
- 往鏡頭走、站在鏡頭軸線上的人，要寫明眼睛看畫面外哪裡，例如「看著畫面左外的門口」。
- 一鏡最多三張有名字的臉。

**每一鏡都要寫進畫面的**（祖媽第 1 集 v2 審片學到的）
- **大道具**：人物圍著的桌、床、供桌、門、椅子、鏡子，每一鏡都寫它在畫面哪裡，過肩與特寫也一樣。動作不跟道具衝突，例如坐在桌邊的人不翹腳、東西不放膝上。
- **第一格的狀態**：寫「第一格眼睛閉著一秒，然後睜開」，不寫「睜開眼」；上一鏡已經站起來，這一鏡就從站著開始。
- **光**：暗的鏡寫光從哪裡來、照亮哪些東西，不然整片黑。
- **封閉的地方**：寫門關著、沒有開著的門。夜景寫夜，點燈的窗可以亮。
- **驚嚇與尖叫**：寫臉上每一處，再加「不笑」。東西掉、飛要寫在鏡頭中間發生，不寫「最後才掉」。
- **手**：戒指只在一隻手上時，寫入鏡的是哪隻手、有沒有戒指。
- **鏡子**：倒影穿同一件衣服、看著自己。最穩的拍法是從鏡子裡往外看。
- **戲服**：換裝的定妝照要拍全身，寫明「沒有」的東西，例如沒有披肩。道具一直畫錯時，從同一集畫對的那一鏡截圖當參考圖。

**不容易拍的，寫分鏡時就避開**
- 精確的數量（三片、二十九個抽屜）、慢動作、字、正面揭露的臉、一鏡三個以上的動作。
- 承載劇情轉折的鏡不能設計成「拍不好就跳過」。開門、走出來這類鏡，用背影或插鏡設計。

**心裡話與畫外音**
- 一場的心裡話總秒數，不超過那幾鏡畫面的總長。
- 比畫面長的心裡話，剪接時延到下一鏡（`spill`），不能撞到下一句原聲。

**分鏡要先過獨立審稿再花錢**：第 5 步審稿交辦要加上「拍法」的檢查，見下面的範本。

## 步驟

### 1. 先讀

- 規格 `storyboard-shot-spec.md`，全文。
- 劇本或原版各集，以及它們的細綱。
- 上一版的審片紀錄。上次的必修要逐條避開。
- `cast.json` 與參考圖清單。
- 已經寫好的範本集，例如《種田》的 `docs/videos/zhong-tian-qu-qi-e001-r2/script.md`。

### 2. 寫系列設定（一集也要）

一個代理、一份檔，例如 `production/r2-bible-e011-e060.md`。寫完才開始寫分鏡。內容：
- **時間線**：每集第幾天、幾點、天氣、主要事件、好感加減與總值。原版自相矛盾的地方挑一邊，寫明為什麼。
- **接點表**：每一集最後一鏡誰在哪、什麼姿勢、手上拿什麼、什麼光，就是下一集的第一鏡。過了時間的，寫用什麼畫面交代，不用字卡。
- **帳**：錢、貨的數量，重要道具在誰手上，期限，路程與花費（兩地之間走路、騎馬、坐船各要多久，住一晚多少錢）。
- **場景格局**：常用場景的門在哪、井和柴堆在哪、桌子是什麼桌。
- **道具的樣子**：例如槍有沒有紅纓、玉佩是什麼形狀、箱子叫什麼名字。
- **人物與參考圖**：每個人出場的集數與外貌，同一鏡不放兩個撞臉的人；哪些圖要先畫。
- **原版必修**：每集一行。
- **伏筆與回收**、系統的任務與吐槽、每集鏡數目標。

### 3. 寫分鏡

- 一個寫稿者連續寫五集，彼此可以同時寫。頭尾照接點表，不用等鄰居。鄰居的稿已經有了，就照鄰居的寫。
- 寫稿交辦（照抄，改集數與路徑）：
  - 先讀：規格全文、系列設定、範本集、每集的原版與細綱與必修、上一集最後一場。
  - 寫 `docs/videos/<slug>/script.md`，格式照範本，頭尾照接點表；最後一集要停在下一段的接點上。
  - 規則：
    - 照上面〈拍法：種田拍法〉：一鏡約 2.5–3 秒，一集 2.5 分鐘約 45–50 鏡，兩到三場；每鏡一個看得見的動作，剪在動作中間；每場照全景→過肩反打→插鏡→反應的順序；每張臉寫表情、看著對方；大道具、第一格狀態、光每鏡都寫。
    - 台詞每句 10–24 字、一口氣說完；問了就答，轉折有看得見的原因。
    - 每場有開頭、有結尾，最後一句是鉤子。
    - 好感照帳；錢、貨、道具換地方時寫誰帶走。
  - 交稿前：跑 `storyboard-check.py`，ERROR 全清，再照規格的自檢清單對一遍；檔案用 UTF-8、LF。
  - 只動自己那幾集，不提交；回報每集的鏡數、秒數、跟設定不一樣的地方、還缺的圖。
- 寫到一半發現的通則，馬上傳給還在寫的人。例如唐小棠的立領一直漏寫、面板的百分比要寫中文。

### 4. 程式檢查

```bash
python -I docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/storyboard-check.py docs/videos/<slug>/script.md
```

有 ERROR 就退回寫稿者。warning 照系列設定寫明的例外留。

### 5. 獨立審稿

- 由沒寫這幾集的代理看，只讀不改。每段四集，相鄰兩段重疊一集，另外多讀前一集最後一場、後一集第一場。
- 審稿交辦：照規格〈第三道：獨立審稿〉的五件事與回報表。可以直接貼的範本在下面。
- 審完一段就先送去改，不用等全部審完。

### 6. 改稿

- 審稿意見交回**原本寫那幾集的寫稿者**，他們最清楚那幾集。要先讀原文確認問題是真的，再改。
- 兩段意見衝突時，例如交界的同一處兩邊都說要改，由主對話決定改哪一邊，並寫進系列設定。
- 改完：
  - 再跑一次程式。
  - 每集記「YYYY-MM-DD 審稿後的修改」，台詞改了寫要重錄。
- **掃全季**：一個設定改了，就用搜尋把每一集都找出來改，例如道具的樣子、參考圖的代號、面板的寫法。

### 7. 收尾

- 系列設定補一節「審稿後補定的事」，加上要站主決定的事。
- 提交、推上 PR，說明寫全季的鏡數與長度，以及要站主決定的事。
- 已經在拍的集數，把改動傳給製作端。

## 成本（r2 第 11–60 集實測）

| 項目 | 數量 | 每個約 |
| --- | --- | --- |
| 系列設定 | 1 個代理 | 32 萬 tokens、23 分鐘 |
| 寫稿（每人五集，含改稿） | 10 個代理 | 35–43 萬 tokens、30 分鐘 |
| 獨立審稿（每段四到五集） | 16 個代理 | 19–25 萬 tokens、5–7 分鐘 |

50 集共用掉每週額度約 7%（從 75% 到 82%）。每個代理都用 `model: "opus"`。寫稿分兩批跑，每批五個；第一批跑完先看一次額度。

## 審稿交辦範本（貼給審稿代理，換掉 SEG、PREV、NEXT）

```text
You are an independent, READ-ONLY reviewer of storyboard scripts. You did not write them.
Do NOT edit, create, commit or push any file. Report in 繁體中文 (Taiwan usage).

Scripts: docs/videos/<slug>/script.md. Your segment: episodes {SEG}. Also read the last scene of
episode {PREV} and the first scene of episode {NEXT} so every junction is checked.

Check against: storyboard-shot-spec.md (read entirely, especially 〈交給製作端之前的三道檢查〉 and its
error tables); the series notes (timeline, ledger, junction table, props, characters, 必修, and the
section 「審稿後補定的事」, which is binding); cast.json; the original episodes and the previous review.

Examine shot by shot: (1) the 11 items; (2) dialogue head and tail — every question answered, every turn
caused by something the character can see or hear, scenes open and end, speaker in frame or 畫外, names
set up before first use; (3) continuity — positions and axis, who leaves, who holds each prop, time and
light, and the last shot of N and the first shot of N+1 being the same moment; (4) numbers — money,
counts, travel time, deadlines, panels; (5) each 必修: avoided or not; (6) the 拍法 section of
script-to-storyboard.md (種田拍法): ~2.5–3 s per shot with a visible action cut mid-action, coverage order per
scene (wide → over-the-shoulder/reverse → inserts → reactions), a concrete expression on every face, speakers
facing listeners and nobody into the lens (explicit off-axis eyelines for anyone walking toward the camera), at
most three named faces, big props written into every shot of their scene, first-frame states, light sources in
dark shots, closed rooms stated, fear written per facial feature plus "not smiling", no precise counts or slow
motion, inner voice fitting the picture.

Report only what would make production guess wrong or confuse the viewer. One table:
| 集 | 鏡 | 問題 | 依據（引原文或規則） | 建議怎麼改（台詞給替換句，10–24 字） |
then 必修 per episode and a count. Under 1500 words.
```
