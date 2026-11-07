# W02 米其林 v3：改了什麼

原資料夾：`scratchpad/wt-backup/docs/videos/curio-w02-michelin-guide-stars/`（只讀，沒有改）。
這一版的四份檔案：`video.json`、`script.md`、`structure-map.md`，和這一份。
沒有畫圖，沒有跑 keyframes 和 tts，也沒有 commit。

## 總覽

| | 原片 | v3 |
|---|---|---|
| 景數 | 113（shot 102、big 9、stats 1、outro 1） | 133，全部 shot |
| 台詞 | 130 行 | 147 行（t001–t147，重新編號） |
| 旁白字數 | 2711 單位（lint） | 2947 單位（lint）；不含標點 2947 字 |
| 長度（lint 估） | 11.2 分（低於 target 12–14 分，有警告） | 12.2 分（在 target 內） |
| 長度（照原片語速估） | — | 2947 ÷ 4.03 字／秒，約 12:10，不含換景停頓 |
| Ada | 沒有（原本是另一位「檔案員」） | 30 景（23%） |
| 無人景 | — | 85 景（`nobody: true`） |
| 一般人物或只有手 | — | 18 景 |
| lint | 0 錯誤、2 警告 | 0 錯誤、0 警告（見下方「自檢」） |

每景平均約 5.5 秒。有 5 景不到 4 秒，都是短句收尾：open-promise-b、yes、door-wait、young-cook、two-ledgers。

## 敘事

- **拿掉濃縮開場**：原本開場就說了「1920 年一個男人看到書被拿去墊東西」「2017 年韓國議員追合約」，這兩個人物都沒頭沒尾。
  - 新鉤子先講這是什麼書、誰出的，再講怪在哪：星星買得到的流傳、部長站台、從免費到城市付錢。
  - 最後只留兩個高潮標籤：韓國國會、美國只撐兩年。
- **照黑貓 10 步重排**：詳見 `structure-map.md`。
- **時間不再往回跳**：
  - 泰國原本整章排在韓國後面（2017 年 10 月 → 2017 年 2 月 → 2021 年）。現在預算放在韓國之前，延約放在加州之後。
  - 韓國那章整理成合約 → 指控 → 顧問 → 兩年後 → 提告 → 否認。
- **埋的梗都收回**：共 19 條 loops，對照表在 `structure-map.md`。新埋的有：
  - 「記住這句話，等一下會很好笑」（never-paid／remember-this → two-years）
  - 自付的評審（pay-tray → answer-tray）
  - 部長的講台（open-hall → full-circle）
- **收尾**：
  - 新加倒帶句 full-circle：從工作台底下那一本，到今年部長站上的講台。
  - 新加金句 close-line：「這本書的帳一直在換人付；不換的，是你願不願意信它。」
  - CTA 問句接回步 4 的「值得繞道」。
- **原本的卡片**：九張 big、一張 stats、一張 outro，旁白都保留，畫面改成插圖。數字只留在旁白裡。
- **人名**：André 不在 `docs/videos/lexicon.json`，寫進旁白 lint 會報錯（「Andr」不在詞典）。這一版改說「兄弟其中一位」。見「要站主決定的事」第 1 條。
- **拿掉的句子**：
  - 「講到這裡你可能會想：這是亞洲的做法吧，美國總不會」（diner-grin），改由 remember-this 埋梗。
  - 韓國那章的轉場句（scooter），因為順序改了，不再需要。
  - 「一八八九年」之前的「部長站上去之前，這本書先被白送了二十年」，因為鉤子已經講了免費。
  - 書的內容那一句拿掉「地圖」，因為畫面規則不畫地圖。意思不變。
- **新寫、但不帶新事實的句子**：
  - Ada 的自我介紹
  - 「不是美食雜誌」
  - 「你今天開輪胎行，至少路上滿滿都是車」
  - 「就得回來買新的」
  - 「這就是星星值錢的起點」
  - 「我原本以為，故事就停在這裡」
  - 「查不到，就是查不到」
  - 「記住這句話，等一下會很好笑」
  - 金句與倒帶句

  這些都是轉場或看法。旁白有標成看法的，照原片標。

## 畫面

- 每景一張插圖，沒有卡片，畫面上不寫字。
- 原片的人物都換掉了，因為規則 6 不畫創辦人：
  - 安德烈與愛德華兄弟的固定外型
  - 「檔案員」
  - 匿名評審的外型句

  兄弟的景改成物件（工作台、輪胎、紅色小冊子）或 Ada。
- 匿名評審是虛構的一般人，保留成同一位普通卡通人。外型固定寫 `a calm man with short neat dark hair in a plain charcoal blazer`，出現在 anon-table、pay-tray、train-suit、arrive、travel-pay、answer-tray。
- 在世的具名人物只畫手：議員、提告的店主、台南的主廚。部長、高層、主管一律不入畫，用講台、麥克風、收音機、握手的手代替。
- 書一律寫 `small plain red booklet` 或 `thick plain-covered book`，紙張寫 blank。星星寫 `small gold paper star`。不畫地圖、招牌、報紙、菜單、月曆。
- 數字的比喻：
  - 虧損：洩氣的氣球、枯萎的幼苗、扁的錢包
  - 翻倍：升起的氣球
  - 二十億：束緊的錢袋
  - 十二本：搖搖欲墜的一疊書
  - 七萬到十萬：一排錢罐
- 光線一律是白天：
  - Ada 景照規定寫 `in soft daylight`。
  - 其他景輪流用 window／morning／overcast／afternoon light，因為 lint 會警告同一個字出現在超過三分之一的圖。
  - 法國段寫 `early 1900s France`，不寫負面句。
- 無人景不放玩具車。有車的兩景（shop-today、inside）是有人的景。

## 【待查】

**0 條。** 每句帶事實的旁白都對到原資料夾 `claims.md`／`verify-1.md` 的列，`script.md` 每句後面標了 #n。改寫過、但數字和意思沒變的幾處，記在這裡給查核者看：

- open-tags「有報導說美國城市從沒付過」：原片 t089 是「照美食媒體轉述」（#37）。鉤子裡簡化成「有報導說」，正文 never-paid 仍說「照美食媒體轉述」。
- exec-mic「同一年」：指 2017 年，接在泰國 2017 年 2 月之後。#24 是 2017 年對《華郵》說的。
- partners「二〇二五年」：#70 The Star 2025-10-23。原片沒說年份，新稿加上年份，出處的日期就是這一年。
- seedling「還說這本書值得投資」：原片 t110 是「觀光局的回答是……值得投資」（#49），主詞一樣是觀光局。

## 要站主決定的事

1. **André 要不要念出名字**：規則 5 說英文名照原文念。可是 `André` 不在 `lexicon.json`，lint 會擋。要念的話，得先在詞典加一條（共用檔，這一版沒有改）。
2. **步 8 偏長**：18.7%，模板建議 8–12%。台灣這段同時回收開場的部長梗。要縮的話，可以砍 big-balloon，再把 agree 併進 expo，大約省 10 秒。
3. **5 景短於 4 秒**：都是短句收尾（見總覽）。要硬守 5–8 秒的話，可以併進前後景，但會失去停一拍的效果。
4. **只畫手的景**：assembly-paper、contract-counter、complaint-desk、young-cook、open-rumor、partners 只畫手，沒有臉。規則 6 說用 Ada 或物件比喻，手算不算可以，請站主確認。
5. **Ada 的外型句不一致**：照簡報從 W03 抄了 `characters[0]`，它的 appearance 寫 `short loose black bob`。可是規定的提示詞開頭是 `wavy black bob with a side fringe`。W03 本身也是這樣。要不要統一，請一起決定。
6. **縮圖**：thumbnail 沿用原本的 `thumb` 模板，大字「米其林／誰付錢」，shot 指向 bench-close（工作台壓住紅色小冊子）。縮圖上的字不屬於插圖規則，但要走全球市場的話，請站主決定縮圖要不要留字。
7. **YouTube 說明**：`youtube` 欄位沒有改，裡面寫「錢換過三種人付」「二〇一六年之後」，和新稿一致。`資料截至 2026-10-31` 也沒動。

## 自檢

- **lint**：`--file` 會在同一層找 `brief.md`。直接 lint 輸出檔，只有一個錯誤：brief.md is missing。
  - 所以把 `video.json` 和原資料夾的 `brief.md` 複製到 `scratchpad/redo/lintbox/docs/videos/curio-w02-michelin-guide-stars/` 再跑。
  - 結果是 **0 errors、0 warnings**，估 12.2 分，147 行，2947 單位。
  - 章節時間：0:00、0:58、2:13、3:21、4:17、5:43、7:03、8:37、10:09、10:53。
- **提示詞掃描**：133 句逐句比對 BRIEF 列的禁字，不分大小寫、子字串比對（cat、sign、map、cap、night、lamp、glow、" no " 等），**0 命中**。所有提示詞長度都在 100–190 字元。
- **Ada 開頭**：30 句全部以 `Medium close-up of Ada with her wavy black bob with a side fringe and round red glasses` 開頭，以 `against a plain wall, in soft daylight` 結尾，都有 `characters: ["researcher"]`。非 Ada 景沒有出現 Ada。
- **其他**：無人景 85 句都寫了 `nobody: true`；所有景都是 `template: "shot"`。
