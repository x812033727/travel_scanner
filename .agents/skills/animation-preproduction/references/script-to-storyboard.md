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
    - 每集 34–42 鏡、兩到三場；每鏡一個看得見的完整動作。
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
counts, travel time, deadlines, panels; (5) each 必修: avoided or not.

Report only what would make production guess wrong or confuse the viewer. One table:
| 集 | 鏡 | 問題 | 依據（引原文或規則） | 建議怎麼改（台詞給替換句，10–24 字） |
then 必修 per episode and a count. Under 1500 words.
```
