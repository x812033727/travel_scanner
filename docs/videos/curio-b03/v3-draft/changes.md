# B03 Lonely Planet v2 草稿：改了什麼

依據：`scratchpad/redo/RULES.md`（含 2026-11-06 補充）、`scratchpad/heimao/STRUCTURE.md`、W03 v3 範例。原資料夾 `wt-backup/docs/videos/curio-b03/` 沒有動。
這一版沒有畫圖，沒有跑 keyframes 或 tts，也沒有 commit。產生這一版的腳本在 `scratchpad/redo/tools-b03/`（`scenes.py` 是資料，`build.py` 產生 `video.json`，`gen_docs.py` 產生 `script.md` 與對照表）。

## 數字

| | 原片 | 這一版 |
|---|---|---|
| 景數 | 125（116 插圖、9 卡片） | 130（全是插圖） |
| 旁白句數 | 137 | 136 |
| 發音單位（lint） | 2619 | 2822 |
| lint 估計總長 | 12.7 分（12.66） | 13.5 分（13:31） |
| 用原片的速度估（2619 單位／12.66 分，每分鐘約 207 單位） | — | 約 13.6 分（13.64） |
| Ada 景 | 0（原檔沒有 characters） | 26（20%） |
| 無人景（`nobody: true`） | — | 90 |
| 一般人物景 | — | 14 |
| loops | 15 | 28 |

每景 4.1–8.5 秒，平均 6.2 秒（lint 的估計時間軸）。lint 沒有鉤子間隔的警告：正文每 45 秒內都有句尾問號、升級句或章節轉折。

## 結構

- 拿掉開場的濃縮劇情（1972 雪梨、二十七分錢、1973 廚房桌上釘書）。起源全部移到承諾句之後，從「故事要回到一九七二年的倫敦」講起。
- 鉤子改成：一套很厚的背包客旅遊書，叫 Lonely Planet → BBC 前後付了大約一億三千萬英鎊 → 電視台買旅遊書出版社已經夠怪 → 可是你想不到，六年後整家賣掉，拿回不到一半 → 兩個停在結果之前的高潮標籤（最後四分之一的價錢、BBC 自家網站的決定）。
- 承諾句改成黑貓句型：「今天我們就來聊聊：……最後換回了什麼？」
- **時間不再倒走**：
  - 原片在 2013 年 3 月賣出之前，就講完 2013 年 11 月才發表的檢討報告結論（TripAdvisor、三成利潤率、沖昏頭、外在因素）。這一版把它們放到 9 月的美聯社訪問之後，和 11 月副主席那句話放在一起。
  - 「另外投了兩千萬」與「推算接近一億」也是報告裡的數字，從賣出那章移到報告那章。
  - 只有兩處用「後來的檢討報告說」先引報告：2011 年的賣權（「設計得很糟」）和 bbc.com 的延誤。兩處講的都是當年發生的事，報告只是出處。
- 澳幣的回呼方向改了：先在 Wheeler 9 月的訪問出現，報告列外在因素時再回呼「還記得 Tony Wheeler 說的澳幣嗎？」。
- 片尾加「倒帶」：回到 1973 年的廚房桌，對比兩個問題（「你們怎麼去的？」與「能不能讓 BBC 的品牌更值錢？」），最後一句標明是旁白的看法；之後接留言題與訂閱。
- 完整的段落對照、10 步秒數與 loops 見 `structure-map.md`。

## 稿子

**補回的事實**（都已查核，只是早先幾輪為了長度或盲評刪掉，或當時沒用）：

- 「據一份雜誌專訪，兩個人離開英國的時候，身上一共大約四百英鎊。」#2，金額 CONFIRMED（Big Issue 2023）；車價有爭議，不講。verify-1 把 #2 列在「旁白不用的列」，原因是當時沒用到，不是因為內容錯。
- 店名的由來（era-name-q → era-kept）：#11、#12，第一輪查核 t021–t025 逐句 OK，第二輪盲評刪掉。歌名〈太空船長〉和歌手都不念，只說「一首英文歌」，避開「不能說」清單裡的「喬·庫克寫了〈太空船長〉」。
- 「一九九二年的一篇報導，就是這麼寫的」（黃色聖經的出處）：#14，CS Monitor 1992。
- 「出版社自己在書前頁，就是這麼寫的」（1,500 本的出處）：#8；原片這句寫在卡片的 sub 上。
- 鉤子的「六年後……拿回來的錢不到一半」：#41、#43；第一輪查核 t003 OK，後來是舊的盲評 no_spoiler 要求刪掉。

**改寫但意思不變的**：

- t038 執行長的話：「要在網路上壯大內容品牌，也擴大澳洲和美國的生意。」（#29 原文 grow our portfolio of content brands online and increase our operations in Australia and America）
- t041–t042 信託會：原本「開了四個條件，還要證明……」，這一版拆成兩景，只說「它要 BBC 先證明：這筆買賣，能讓 BBC 的節目和品牌更值錢」，不提四個條件（#31）。
- t107 Wheeler：「他說，傷到這家公司的不只是景氣；他們賣掉的時候，正好碰上澳幣起飛。」（#59 原文 It wasn't just the recession that hurt Lonely Planet – we also sold out just as the Australian dollar took off）
- t114 「紙本書市會掉得多快，也沒有好好細算。」（#55 Not enough downside analysis was done of the potential impact of a faster decline in books）
- t132 「一九七三年那張廚房桌子上，這本書是為了回答一個問題：你們怎麼去的？」（#5 People kept asking us … So we made a book out of it）
- t133 「三十多年後，BBC 買下它，問的是另一個問題：能不能讓 BBC 的品牌更值錢？」1973 → 2007 是 34 年；後半句對應 #31 信託會的條件（leverage extra value from the BBC's intellectual property）。
- 人名改念原文（RULES §敘事 5）：惠勒 → Wheeler、東尼·惠勒 → Tony Wheeler，新出現 Maureen。報社與通訊社（《衛報》《金融時報》、美聯社、路透社、法新社）沿用通行的中文譯名。

**刪掉的**（為了總長；事實都還是對的，要加回來不用重查）：

- 「說實話，被國會這樣點名，我大概會想找個洞鑽進去。」
- 「這句話很誠實，也有一點殘忍。」
- 「我覺得，廚房裡起家的小出版社長成這樣，難怪有人想買。」
- 「下次你在書店翻到它，可以想想它背後這本帳。」
- 賣價「分兩次付：六千萬澳幣先付、一千五百萬一年後」
- 信託會的「四個條件」

**【待查】**：0 條。這一版沒有新事實，每句帶事實的旁白都對到 `verify-1.md`〈逐項查核〉的列號，列號標在 `script.md` 每句後面。

## 畫面

- 每一景照 RULES.md §畫面 重寫提示詞：
  - 長度 102–189 字元，一個主體一個動作。
  - 白天的光：早晨、午後、陰天、窗光，沒有夜晚、檯燈、黃昏、發光。
  - 沒有負面句，沒有字，也沒有數字。
- Ada 的 `characters` 定義照 W03 的 `characters[0]` 抄過來（原檔 `characters` 是空的）。26 景都以規定句開頭，並寫 `data.characters: ["researcher"]`。
- 9 張卡片（big 7、stats 1、outro 1）全部改成插圖。
- 在世的人一律用固定的物件代表：
  - Wheeler 夫婦：兩個舊帆布背包、一台淡藍色的 1970 年代小廂型車。
  - Lonely Planet：一本素色亮黃封面的厚書。
  - 信託會：黃銅天平。
  - 檢討報告：深綠素色封面的厚檔案夾。
  - 委員會報告：深紅封面。
  - 大股東：柵欄上的白色牛仔帽。
  - 副主席：打翻的茶杯。
  - 公司股份：一個金黃色的派，四分之一那片單獨放。
- 數字都改成質性比喻：鼓起或扁掉的錢包、升起或洩氣的氣球、射偏或正中的飛鏢靶、融化的冰塊、漏水的桶子、Ada 倒抽一口氣。
- 螢幕只用安全圖案：筆電是一條藍色路線或純天藍色，手機是一個紅色定位釘，電視是黑螢幕。
- 原檔 NOTES.md 第三輪的規則（在世人物的景只畫物件）照舊；路人（會計、店員、服務生、鄰居、遊客）只出現在旁白不是在講某個真人的景。
- 縮圖 `thumbnail.data.shot` 還是 `open-stakes`，這一景仍是看著帳本張嘴的會計，沒有變。
- `voice.performance` 照新結構改寫。`youtube.description` 改了三處：
  - 段落順序照新結構。
  - 插圖那句改成「解說員 Ada 是虛構角色……在世的人物只用物件代表」。
  - 加上「本頻道跟 BBC 與 Lonely Planet 沒有授權或合作關係」。
- 其他欄位（title、tags、sources、look、music、theme、still_motion）沒有動。

## 自檢結果

- **提示詞掃描**：用 `tools-b03/scan.py`（B02 那支的副本）跑，130 景的結果如下，全部是 0：
  - 禁用字
  - 長度不在 100–190
  - Ada 開頭句不符
  - 非 shot
  - Ada 出現在沒寫 characters 的景
  - 另外確認提示詞裡沒有 `cartoon`，也沒有 lint 的畫風字。
- **lint**：在 `scratchpad/redo/lintbox/docs/videos/curio-b03/` 用 `--file` 跑，這個目錄放了 video.json、原 brief.md，lexicon 用上一層的 `lintbox/docs/videos/lexicon.json`。
  - 照 repo 現在的 lexicon：**20 個 error**，全是 Wheeler、Tony、Maureen、lovely、lonely、planet 不在 `docs/videos/lexicon.json`。
  - lintbox 的 lexicon 副本補上這六個詞（值為 null）之後：**0 error、0 warning**，估計 13.5 分鐘。
- **正式放進 repo 時要加進 lexicon 的詞**（值先填 null，試聽後再定）：`Wheeler`、`Tony`、`Maureen`、`lovely`、`lonely`、`planet`。小寫的 lonely／planet 是歌詞那兩句用的；大寫的 `Lonely`、`Planet` 已經在 lexicon 裡。

## 要站主決定的事

1. **總長**：lint 估 13.5 分；用原片的速度估是 13.64 分，在 12.66 ± 1 分的上限內，只差 0.02 分。要更保險，可以先刪這幾景（合計約 36 秒）：
   - era-zero（多打一個零，約 5 秒）
   - deal-fair（《衛報》也是對手，約 7 秒）
   - put-deal（最划算的合約，約 6 秒）
   - web-books2（比 2010 年少 27%，約 4 秒）
   - ap-italy（義大利文市場，約 7 秒）
   - web-phone（翻書還是看手機，約 7 秒）
2. **店名的由來要不要放回來？** 舊的盲評（no_detour）刪過它。這一版放在起源，是因為黑貓的起源段會交代主角的怪癖。不要的話，刪 era-name-q 到 era-kept 共五景（約 27 秒），時間也比較寬鬆。
3. **鉤子要不要說「拿回來的錢不到一半」？** 舊的盲評（no_spoiler）不准。新規則要求鉤子讓人聽得懂為什麼怪，所以這一版放回來，不講確切賣價。
4. **人名念法**：Tony Wheeler、Maureen、Wheeler 夫婦照 RULES §敘事 5 改念原文，要先試聽。歌詞的 lovely planet／lonely planet 也是念英文。
5. **10 步比例**：
   - 步 4 是 19.9%，步 5 是 18.2%；把國會那章改算成步 5，兩步就都在模板範圍內，目前的分法見 `structure-map.md`。
   - 步 8 是 5.9%，步 9 是 4.4%，都偏短。要補的話，可以用 #63（NC2 接手四個月就裁員）和 #64（2020 年墨爾本、倫敦辦公室幾乎全關、停掉雜誌）。這兩列已查核，但 #63 只讀到導言（△）。
6. **破車入畫**：RULES 畫面 8 說玩具車容易被畫上臉。這一版的破車都是真車，從背後的遠景拍（era-van、era-route、late-van、late-fuel），標成無人景。要更保險，可以改成兩個背包放在路邊。
7. **舊資料**：原資料夾的這些檔案都還是舊版，定稿後要一起更新：
   - `i18n/`
   - `claims.md` 的行號
   - `NOTES.md` 的人物表
   - `brief.md` 的「開場五步」與「畫面」兩節
   - `score.md`
8. **Ada 的髮型描述**：提示詞開頭句寫 wavy black bob with a side fringe，抄過來的 W03 角色設定寫 short loose black bob。兩者並存，跟 W03、B02 一樣，這一版沒有改。
9. **盲評**：如果還要跑舊的盲評題（no_spoiler、opening_hooks 的舊定義），鉤子的「不到一半」和起源移位都會被判不合，那些題目要照新規則改。
