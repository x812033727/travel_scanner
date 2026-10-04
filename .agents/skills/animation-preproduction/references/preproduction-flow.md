# 前期各步的範本與一個做完的例子

`SKILL.md` 的 P0–P7 與鎖定後的變更單，每一步要交的東西長什麼樣。範本放進這一集的回報或票的 Notes（repo 是公開的：檔案、收據、帳號資訊留在 repo 外的工作目錄）。後半是用 `animation-camera/references/budaimiao-example.json`（布袋喵參考風格的原創八鏡）實際跑三支腳本的結果。

## P0 製作條件卡

```text
作品／集：                 slug：
路線：伺服器 | Hailuo 網頁（H3 2K／768P、2.3） | Kling 網頁（3.0 1080p）；一集鎖一條（小樣想比另一家，最多一鏡另列一行）
production profile：有（只能走伺服器）／沒有
交片：1920×1080、16:9、30 fps；CC；配音：已錄／未錄
方案與餘額：               本月剩餘：
預算：期望 ___ 點（US$___）、上限 ___ 點、預留一成；花到期望就停下來問
take 上限：clip ___（預設 2）、關鍵影格 ___（預設 3）
AI 潤飾（Hailuo AI Polish／Kling AI Prompter）：開／關
期限：
參考風格：例如「真一隻布袋喵」（docs/videos/drama-craft/reference-study-20261004-budaimiao.md）
```

## P2 分場與節拍表

每場一列；「新知道什麼」寫不出來的場，先合併或刪掉，不要進分鏡。

| 場 | 一句話：觀眾在這場新知道什麼 | 轉折 | 地點與時間 | 光與色（整集的色彩腳本） | 出場角色與道具 |
| --- | --- | --- | --- | --- | --- |
| 1 斷橋前的一步 | 沈守橋、陸試探，第一擊後陸退半步 | 陸以為能過，沈一擊讓他退 | 斷橋南側橋台、黃昏 | 冷天光＋右側暖輪廓光；只屬這場 | 沈（單劍、銀袖扣、玉髮繩）、陸（單杖、銅環、銅肩扣） |

光寫在每一鏡的 `prompt`，不寫進 `look.style`（試拍：倉庫火光漏進婚禮）。

## P3 鏡位表

每場先畫軸線、定鏡位，再把台詞分到鏡位上（`scene-coverage.md` 第一節）。`shot_plan.mjs` 依 `camera` 整行＋`prompt` 第一個子句給代號，同一個代號就是同一個鏡位。

| 鏡位 | 景別與角度 | 拍誰 | 用途 | 母鏡頭？ | 第幾鏡用 |
| --- | --- | --- | --- | --- | --- |
| A | 雙人、平視、鎖定 | 沈左、陸右 | 開場空間 | 否 | s01（s08 是另一個鏡位的全景） |
| … | | | | | |

規則：攝影機整場留在軸線同一側；全景約每 6–8 鏡回來一次（`drama-craft.md` 的參考片，目視）；回到同一鏡位的第二、三次寫 `data.source`，第一次買長一點當母鏡頭。對話場 4–6 個鏡位；打鬥場插鏡與反應多，鏡位數不設目標。

## P4 分鏡表欄位

`shot_plan.mjs --markdown` 印的就是分鏡表，欄位是：

| 欄 | 意思 | 從哪來 |
| --- | --- | --- |
| 鏡 | 場景 id | `video.json` |
| 場／鏡位 | chapter 與鏡位代號 | chapter、`setupKey` |
| 景別、運鏡 | `camera` 原文 | `video.json` |
| 角色 | 畫面裡的人（畫外說話者不列） | `data.characters` |
| 台詞 | speaker：文字；或「動作 N s」 | `lines`、`action_seconds` |
| 秒 | 這一鏡在時間軸上的長度 | 錄好的 `timeline.json`，沒有就 lint 估 |
| 類型 | clip／still／切自哪一鏡；母鏡頭標它的切鏡 | `visual`、`source` |
| 買 | 這條路線買幾秒 | `route-decisions.md` 第三節 |
| 首格／末格 | 已畫／要看／過期／待畫 | `keyframes/manifest.json` |
| 風險 | A／B／C 與原因 | `shot-risk.md` |
| 一次／期望／上限 | 點數或 US$ | 一次的價 × 1、× 預期 take（不超過上限）、× take 上限 |

另外每個要買的鏡頭印一段「定稿正文」（照貼、附 SHA-256）、整集的負面欄（網頁真的有負面欄才貼）、批次順序、槓桿與問題。`--csv` 給試算表，`--json` 給別的工具。`--strict` 把 lint 會擋的鏡頭（切素材的來源、鏡長、profile 規則）、不在八組裡的運鏡字、不在小樣裡的 C 級都算成問題。

## P7 開拍鎖定包

```text
開拍鎖定包：<slug>，<日期>
1 條件卡：（P0），AI 潤飾：開／關
2 分鏡表：shot_plan.mjs --route ___ 的輸出（附件），共 ___ 鏡；clip ___、still ___、切 ___；風險 A ___、B ___、C ___
  負面欄：網頁真的有才貼 look.negative，不寫進正文
3 文字卡動態分鏡：animatic.html；冷看意見：___
4 小樣計畫：___、___、___ 三鏡（同一條路線）；要驗的：___；失敗條件：___；take 上限 ___；點數上限 ___
  另一家比較（要的話）：___ 一鏡，路線 ___，___ 點，take 1，正文 SHA-256 ___
5 預算：伺服器端（設定圖、配音、關鍵影格與 judge、音樂）US$___；片段期望 ___ 點、上限 ___ 點、預留 ___；本月方案額度占 ___%
6 批次：小樣（檢查點）→ 第 1 場（檢查點）→ …；停損：同一缺陷兩次、到 take 上限、結果不明、花到期望值
7 plan_lock.mjs --ready：製作中要完成的 ___（關卡、配音、關鍵影格）；送第一支之前的人工項 ___
8 未驗：___
請站主在花錢之前確認一次；確認後照包做（設定圖、配音、關鍵影格、小樣、批量），包外的事（超預算、改鎖定的東西、重大缺陷）才再問。
```

站主點頭後：`plan_lock.mjs --write --note "<站主的原話>" --assist on|off`，加上跟 `shot_plan.mjs` 同一組規劃旗標。

## 變更單

`plan_lock.mjs --check` 印的就是變更單；送給站主之前補上「誰要改、為什麼」：

```text
變更單：對照 <鎖定時間> 的開拍鎖定（<站主當時的話>）
要求：<誰、為什麼>
動到的雜湊：（--check）
改了什麼：（--check 的列表）
會重畫、重買或重做：（--check 的列表，含 judge 次數與要重匯的外部片段）
失效的核准：（--check，只列已經核准過的）
估計多花：___ 點／US$___
決定：站主 ___（日期）
```

決定之後一次改完、`--write --force --note "<決定>"`（沒給規劃旗標就沿用鎖定的設定）；舊鎖留在 `plan/`，這筆變更記進 `plan/changes.jsonl`。

## 例子：布袋喵參考風格的八鏡（2026-10-04 實跑）

`budaimiao-example.json` 是《斷橋前的一步》一場戲，八鏡、約 21.6 秒（lint 估；沒錄配音）。

### 1. 先出表

```bash
node .agents/skills/animation-preproduction/scripts/shot_plan.mjs .agents/skills/animation-camera/references/budaimiao-example.json --route kling
```

八鏡都是 clip、八個鏡位（這場沒有回到同一鏡位，所以沒有切鏡可省）。風險：A 4、B 3、C 1：

- s06 過肩「青弧打中陸的杖、濺出火花」：`contact.two-person`（C）。兩個角色同框、接觸點在兩人之間。
- s04 插鏡「右手把劍柄抬高 20 厘米」：`hands.weapon`（B）。握法與手指數最容易在中途變。
- s02、s07 是說話的人在臉的景別裡（`speech.visible-mouth`，B）：產線沒有對嘴。

三條路線的片段錢（一次／期望／上限；Kling 與 Hailuo 是點數與月費攤的美元）：

| 路線 | 買的秒數 | 一次 | 期望 | 上限 |
| --- | --- | --- | --- | --- |
| Kling 3.0 1080p | 28 | 224 點（US$2.76） | 322 點（US$3.98） | 448 點（US$5.53） |
| Hailuo H3 2K | 33 | 396 點（US$4.84） | 566 點（US$6.92） | 792 點（US$9.68） |
| 伺服器 Omni | 32 | US$4.80 | US$6.78 | US$9.60 |

伺服器端的設定圖、關鍵影格與 judge 另外約 US$2.10（上限 US$5.26），三條路線都一樣要付。小樣選到 s05 → s06 → s07（出招、接觸、受力反應）：那個 C 在裡面，最難的先驗。

### 2. 重設計那個 C

導演的判斷：s06 的接觸是這場戲的重點，但不必讓兩個人同框接觸。照 `shot-risk.md` 的招式（也是參考頻道的做法）：

- s06 改成接觸點的插鏡：`camera: "Insert of the staff band, locked"`，`prompt` 只有杖的銅環與從左邊進來的青弧，`characters: []`，`motion` 是「青弧打中銅環一次、碎成一陣琥珀色火花」。兩人的關係由前一鏡（s05 沈出招）與後一鏡（s07 陸受力後退）交代：動作切在兩端。

重跑（改過的檔在工作目錄，不進 repo）：

| 路線 | 買的秒數 | 一次 | 期望 | 上限 |
| --- | --- | --- | --- | --- |
| Kling 3.0 1080p | 28 | 224 點（US$2.76） | 290 點（US$3.58） | 448 點（US$5.53） |
| Hailuo H3 2K | 33 | 396 點（US$4.84） | 518 點（US$6.33） | 792 點（US$9.68） |
| 伺服器 Omni | 32 | US$4.80 | US$6.30 | US$9.60 |

風險變成 A 5、B 3、C 0；期望值少 7–10%，上限不變（take 上限一樣）。更重要的是唯一一個不會收斂的鏡頭不見了：它是最可能燒光 take、拖住整批的地方。`shot_reading.mjs --strict` 讀改過的八鏡仍然零陷阱。

沒有 C 之後，自動挑的小樣變成 s02 → s04（台詞與蓄勢）；這場戲最該先驗的仍是出招、接觸、受力那條剪接鏈，所以鎖定時用 `--pilot s05,s06,s07` 指定。s02、s07 的 B 留著：台詞已鎖（P1），把它們搬到聽者臉上要改分鏡結構。在鎖定包裡寫「這兩鏡說話者入鏡，嘴型不對嘴，接受」，或在 P3 就把這兩句放到反應鏡上。

### 3. 動態分鏡與鎖定

```bash
node .agents/skills/animation-preproduction/scripts/animatic.mjs --file <改過的 video.json> --workdir <這集的工作目錄> --route kling --pilot s05,s06,s07
node .agents/skills/animation-preproduction/scripts/plan_lock.mjs --file <改過的 video.json> --workdir <這集的工作目錄> --ready --route kling --pilot s05,s06,s07
node .agents/skills/animation-preproduction/scripts/plan_lock.mjs --file <改過的 video.json> --workdir <這集的工作目錄> --write --route kling --pilot s05,s06,s07 --assist off --note "<站主的話>"
```

文字卡版的動態分鏡在這一步就能看節奏：八鏡中位數約 2.5 秒、最長 4 秒、前 10 秒開始 5 鏡（對話戲的目標是前 10 秒至少 4 鏡；整集的前 30 秒至少 10 鏡這一列，單場戲不評）。鎖定前的 `--ready` 列出還沒有的關卡、配音與關鍵影格，放進鎖定包第 7 項。鎖定之後有人把 s05 的 `motion` 加了一個字，`--check` 立刻印出變更單：s05 的畫面欄位與定稿正文變了；關鍵影格不用重畫（`motion` 不在畫面請求裡），但 storyboard 核准過的話會失效，伺服器買過的素材要再 judge、匯入過的外部片段要重匯。
