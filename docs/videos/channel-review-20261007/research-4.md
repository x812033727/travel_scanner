# 聲音與人味：合成旁白頻道的成敗差異、觀眾對 TTS 的接受條件、說書式口吻的寫法、單一聲音的單調解法

> **事實查核後的修正（2026-10-07 下午）**
> - Crowd React Media 揭露後的數字不是 33／47／21：原文是 AI 組揭露後 25% 更喜歡、20% 更不喜歡、多數無差；人聲組 48% 更喜歡、4% 更不喜歡；整體對 AI 聲 44% 正面／26% 負面／30% 中立（radioink 2026-07-07）。
> - Adobe Express 調查是 2026-02-18 發布，原頁寫 AI 聲在新聞 9%、podcast 8% 可接受（遊戲 51%、客服 45%）；77% 最信任人聲與 48% 行銷人的「情感真實度」可留。
> - Markluce AI 與 Mokaair「同一合成聲」沒有依據（兩邊都無音檔），改「同為 AI 合成旁白（依說明欄自述）」；最近 8 支觀看 20～164。
> - 「這裡是 Mokaair，專講 AI 工具」在 zxHRm5jnELc 的 0:48，不是 1:12。
> - 「surface-level, automated drek」是 404 Media 作者 Jason Koebler 的話；真人歷史頻道 Pete Kelly 說的是「historically inaccurate／I absolutely hate it」。
> - YouTube 官方頁 1311392 沒有逐字寫「合成聲音」，官方例子是「image slideshows, templated storylines, or scrolling text with minimal or no narrative」與「AI-generated content made with generic or unoriginal templates」；supertone 網址已轉到 antinodeaudio.com；TechNews 06-16 是媒體引 Kapwing 研究，非官方。
> - Kapwing 案例 60 支裡 58 支是 Shorts，不能當長片觀眾對 AI 聲的證據；ElevenLabs Creator US$22／月請引官方 pricing 頁（costbench 寫 $11）；貓貓研究所只有 195 訂閱，只能當「有自稱」的例子。
> - 小數字：黑貓訂閱 55,200；「官網」52 次；「不代表／不等於」26 次；cc09kA17Xsw 的「以官網為準」還有 6:36 一處。


# Mokaair「聲音與人味」診斷（2026-10-07）

## 一句話結論

Mokaair 的問題不是「AI 聲音被識破」，而是旁白裡沒有一個人：沒有名字、沒有自稱、沒有固定的開場收尾、沒有互動句，而查核層的免責用語（「以官網為準」「公告沒寫」「不代表」）直接寫進旁白，每個數字要落地的時候都被截斷；合成方式又把每句切成獨立的完整句再用固定靜音拼回去，表演計畫與配樂音效都做好了卻沒接上。同一條賽道上已經有一個結構幾乎一樣的失敗樣本（Markluce AI，486 訂閱、每支觀看 16～164），而成功的無真人中文頻道（黑貓研究院、十萬個品牌故事、Delfino雕雕、品牌简史）共同點是「旁白是一個在場的人」，不是聲音是真是假。

**證據限制**：沒有任何音檔可聽，所有關於「聲音平不平」的判斷都是從逐字稿、`tools/video/tts` 的程式與 `docs/videos` 的設定推出來的，下面每一條都標了。黑貓研究院與品牌简史是否用 AI 聲音，說明欄與 metadata 都沒寫，判定不了。

---

## 1. 無真人解說頻道：成功的和失敗的差在哪

### 1.1 中文同賽道的對照（yt-dlp 2026-10-07 抓）

| 頻道 | 訂閱 | 最近 8 支觀看 | 旁白人設的證據 | AI 聲音？ |
|---|---|---|---|---|
| 黑貓研究院 @qiqiqushi0 | 5.51 萬 | 7.5k～22.8 萬 | coA8iBMMLY4：「我們」22 次、「錯了」一字句、「你想想看」、結尾「謝謝你藤本弘先生…歡迎在下面留言告訴我…我們下支影片見」；全片一隻貓、一個人、一張畫桌講到底 | 不明 |
| 十萬個品牌故事 | 17.9 萬 | 85～1.4 萬 | 「第249期」系列編號；說明欄「歡迎來到我的頻道」 | 不明 |
| Delfino雕雕 | 14.5 萬 | 3.3k～12.5 萬 | 標題帶署名「\| Delfino雕雕」、「訂閱雕雕~」 | 不明 |
| 品牌简史 Brand Chronicles | 3.7 萬 | 3.1k～24.7 萬 | 4KZmdADz1eM 0:18「今天就帶你了解…」0:30「點個讚訂閱我們，一起進入潘通的奇幻世界」 | 不明 |
| 直擊科技新聞 | 1.41 萬 | 392～8.2k | 聳動標題（「OpenAI 正式開殺！」）、27 分鐘長片 | 不明 |
| 貓貓研究所（黑貓的仿作） | 195 | 289～1.5k | 「大家好，我是阿貓！」、EP 編號 | 不明 |
| **Markluce AI**（繁中 AI 導讀） | **486** | **16～164** | 說明欄自述「腳本、配音與畫面皆由 AI 產生，腳本由 Claude 協助撰寫」；開場 0:00–0:39 全是免責與來源說明 | **是（自述）** |
| **Mokaair** | **3** | **1～251** | 18 支「我們」合計 25 次、沒有自稱、只有 zxHRm5jnELc 1:12 說過一次「這裡是 Mokaair」 | 是 |

讀法：Markluce AI 跟 Mokaair 的結構幾乎相同（AI 撰稿、單一合成聲、繁中、以免責開場、五語字幕），結果也在同一量級。成功組不管聲音真假，旁白都是「我／我們」在跟「你」說話，有名字、有系列、有固定收尾。

### 1.2 英文的對照

- **Sleepless Historian**（71.5 萬訂閱）：AI 聲音、每支 2 小時以上、觀看 9 千～3.4 萬。它能成立是因為格式是「睡前歷史」，聽眾要的就是平的聲音；404 Media 與真人歷史頻道點名這類頻道是「surface-level, automated drek」，配音曾出現「FEEEEE」故障，真人創作者觀看掉 50–60%。這條路對「要人清醒看完的 AI 新聞解說」不適用。
- **AI 新聞解說賽道的前段都是真人聲音**：yt-dlp 搜「this week in AI news explained」前 20 筆，AI Explained 24.7 萬、Tina Huang 16.4 萬、The AI Advantage 2.2 萬；同一頁裡用 AI 聲音做新聞整理的（IBI、KYC AI LABS、Robert Gharibian）觀看 40～95。
- **創作者實測**：Kapwing 用 ElevenLabs「Adam」做無真人體操頻道，157 天 60 支 110 萬觀看才到 1,000 訂閱；結論「觀眾似乎不介意 AI 聲音」（幾乎沒批評留言），但「AI 聲音缺少抑揚，讓人很難長時間聽下去」。
- **平台逆風**：YouTube 2025-07-15 把「重複性內容」改名「不真實內容」，點名「合成聲音、自動切格、模板化小變化」的量產；但明說用 AI 不會自動失格，看的是創作者觀點。2026-06 technews 報導推薦演算法對所有不露臉影片處理更嚴格。

### 1.3 成功組的共同做法（從上面的頻道歸納）

1. **一個在場的敘事者**：固定自稱、固定開場（「今天我們來講一隻貓」）、固定收尾（「我們下支影片見」）、一個留言問題。
2. **一支影片一個世界**：黑貓 coA8 全片只有一隻貓、一個人、一張畫桌；數字都回到這個場景。
3. **懸念不是公式**：黑貓開場 0:00–0:53 一路堆到「現在這隻藍色機器貓，還是當年那一隻嗎？」才進正題，中間沒有「你以為…其實」的標記詞（整支「其實」5 次，「你以為」0 次）。
4. **系列化與署名**：「第249期」「EP 15」「\| Delfino雕雕」。
5. **配樂與音效**：站主在 ILLUSTRATED.md 點名黑貓的就是「每 4–6 秒換圖加運鏡、配樂與音效」（無音檔，這條是站主自己的觀察）。

---

## 2. 觀眾對合成聲音的接受度

| 來源 | 類型 | 結果 |
|---|---|---|
| Crowd React Media，2026-05/06，1,326 名 18–45 歲電台聽眾 | 實驗 | 55% 把 AI 聲誤認為真人；人聲／AI 聲在專業、可信、活力、好感上差距不顯著（只有幽默感 33% vs 26%）；**揭露是 AI 之後**：33% 較不喜歡、47% 無差、21% 更喜歡 |
| Adobe Express，850 消費者＋205 行銷人 | 調查 | 77% 最信任人聲；AI 聲音最不被接受的情境：**新聞 19%、podcast 9%**；48% 行銷人認為「情感真實度」是最大限制 |
| AIR Media-Tech 三個頻道 | 配音實測 | AI 配音軌 vs 真人配音軌的平均觀看時長：1:22 vs 5:19、0:54 vs 5–6 分、0:43 vs 7:13（配音不是旁白，但量出「平的合成聲」對留存的傷害） |
| Kapwing | 創作者實測 | 觀眾不介意 AI 聲，但缺抑揚難久聽 |
| NarrationBox（供應商部落格，數字無法驗證） | 供應商 | 聲稱平板旁白讓觀看時間掉 15–40%、約 90 秒處出現可量的流失；列的原因是「沒有起伏、重點後沒停頓、稿子是寫給眼睛的」 |

接受條件可以歸納成：聽不出來就沒事；聽出來之後，新聞類最吃虧；留下來的關鍵不是「像不像真人」而是「有沒有起伏、有沒有一個人在講」。Mokaair 是新聞解說，又在 18 支裡用同一個聲音平唸，正好落在最吃虧的格子。

**TTS 的自然度與成本（官方頁，2026-10-07）**

| 供應商 | 自然度資料 | 價格 | 控制手段 |
|---|---|---|---|
| Gemini 3.8 Flash TTS | 第三方部落格引用的 MOS／ELO 排名（bottalk、techstackups）把 Gemini 放在前兩名，但頁面抓不到方法論，只能當參考 | 音訊輸出 US$9／百萬 token（2026 年底前，之後 18），有免費層 | `speech_metadata.style` 自然語言；句內 `<short pause>`／`<long pause>`；單請求最多 2 個預設聲音的說話者；支援 Chinese (Hant script)；文件強調 3.8 TTS「把輸入當逐字稿」 |
| ElevenLabs | 同上部落格把 v3 放第一或第二 | Creator US$22／月；超額 US$0.30／1,000 字（costbench 2026-06-14）；一支 1,900 字的 Mokaair 旁白約 US$0.6 | 標籤式情緒 |
| Azure | — | 價格頁動態載入，這次抓不到 | SSML |

---

## 3. 說書式口吻在中文解說頻道怎麼寫才不像文章朗讀

**量得到的差異**（zh-TW 字幕，黑貓一支 vs Mokaair 三支）

| | 黑貓 coA8 | S88lbAsLz2E | cc09kA17Xsw | vxv8KrNual8 |
|---|---|---|---|---|
| 字／分 | 283 | 293 | 266 | 233 |
| 我們 | 22 | 0 | 0 | 1 |
| 我 | 7 | 10 | 3 | 2 |
| 問句 | 13 | 13 | 17 | 8 |
| 為準／官網／說明頁／公告 | 0 | 2／0／17／3 | 5／6／0／1 | 0 |
| 不代表／不等於 | 0 | 4 | 1 | 4 |

語速一樣，短句一樣，「你」也一樣多；差的是「我們」和那一排免責詞。

**具體寫法**（youmind 轉口播稿規則、youtubescriptwriter substack，加上黑貓的樣本）：

1. 一句不超過 20 字（Mokaair 已達標，平均一格 9～11 字）。
2. 書面語換口語：因此→所以、此外→另外、具有→有、採用→用、提供→給；主動語態；第二人稱。
3. **宣告式開場**：「今天我們來講一隻貓」（黑貓 0:00）、「今天就帶你了解…」（品牌简史 0:18），不是抽象反問。
4. **一字句當節拍**：「錯了」（黑貓 1:13）接「偉大的作品往往誕生於極度的焦慮與走投無路之中」——短後長。
5. **把聽眾拉進房間**：「你想想看這有多不可思議」「你現在去電影院看的…你在書店買到的…你家小孩看的…」（黑貓 0:27–0:36，三個並列具體場景）。
6. **免責不唸**：數字給「大約」「幾成」，精確值與來源放字卡與說明欄（產線的 script-writing.md 本來就這樣寫）。
7. **固定收尾**：回答開場問題 → 一個留言問題 → 署名下支見。

---

## 4. 一個聲音跨 18 支的單調問題有沒有解法

| 解法 | 證據 | 在 Mokaair 產線的狀態 |
|---|---|---|
| 配樂床＋音效 | 站主點名黑貓的做法；ILLUSTRATED §配樂與音效已做到側鏈壓低、−14 LUFS、第 2 版量過響度的音效組與 cue 表 | **設定是空的**：2026-10-03 讀站上設定 `no slides_music_track and no slides_sfx_set`；README 又說純投影片不放配樂。所以 18 支很可能全無配樂（無音檔，推論） |
| 每句表演提示 | ILLUSTRATED §聲音表演：`voice.performance` 全片計畫＋ `lines[].emotion`，lint 要求三分之一句子帶提示 | **工人路線丟掉**：`settle()` 把 voice 換成設定分頁的聲音，計畫被丟 |
| 雙聲道對話 | Gemini 文件：單請求最多 2 個說話者；NotebookLM 兩主持人 2024 年底爆紅、「第一次聽分不出不是真人」，但 2026 年中評論：「同樣兩個聲音同樣節奏，幾集之後套路就露出來」 | 漫劇路線已有多角色 `voice` 與 `emotion`（`core/drama.mjs voiceFor`），投影片路線沒用 |
| 角色／人設 | 貓貓研究所「我是阿貓」、黑貓的黑貓、Delfino 的署名 | 沒有 |
| 整景合成而不是逐句切 | `split.mjs` 檔頭自己寫：「separately synthesized sentences each start their intonation afresh and sound like a list being read」；站主在 Shorts 記「逐句合成加固定 0.18 秒間隔：口吻改了節奏還是平」 | 長片已是整景一次送，但句間塞 800 ms `<long pause>` 再切、再用固定 0.3 s 拼回；節拍只有 900／600／1200 三種 |

---

## 5. 三支逐字的人味診斷（無音檔，從文字與產線設定推）

**S88lbAsLz2E（09-30，舊口吻，251 觀看，頻道最高）**
- 0:00 用問句開場，但 0:15–0:30 立刻報目錄「第一…第二…第三…最後」，正是 register 規則禁的；它反而是觀看最高的一支，說明觀看數是題目（「Google Vids 免費」）帶的，不是口吻。
- 「說明頁」一支 17 次、2:43「數字我就不放在畫面上了，因為說明頁也寫了額度可能調整」——把最想知道的數字拿掉。
- 結尾 7:55「下一步，打開說明欄的文章」：沒有名字、沒有問題、沒有下支見。

**cc09kA17Xsw（10-07，新口吻，2 觀看）**
- 0:05 開場句不錯（「讓 AI 自己挑模型，帳單就會變便宜？這句話，只對一半」），但 9 分鐘換了至少 8 個互不相關的比喻：0:11 帳單拖地、0:31 主廚泡麵、1:16 硬幣、2:32 郵局分揀台、3:22 機車／卡車、4:38 鞋盒收據、6:19 鷹架橋、6:36 試吃——每個都是「寫出來的聰明」，沒有一個場景讓人住進去。
- 數字落點全被截斷：1:08「成本最多能省下一截；確切比例以官網為準」、1:52「矮多少，以官網為準」、2:03「確切的金額，以官網為準」、6:30、6:53。說書規則說「數字一次一個，每個都接著它在觀眾生活裡的意思」，這裡一個都沒給。
- 「你以為…其實」只在 0:54–0:59 出現一次，像填表；「我」3 次、「我們」0 次；結尾 8:48 直接以答案收，沒有人、沒有互動。

**vxv8KrNual8（10-05，843 秒最長，21 觀看）**
- 0:05 與 0:28 連兩次「你以為…其實」，公式露出來。
- 查核免責寫進旁白：2:11「這裡只用麵團做比喻，沒有真的在替文字計數」、2:44「不要把這種機制，說成所有語言模型完全一模一樣」、3:16「比喻像配料分量，卻不是模型裡真的住了一位麵包師」——旁白在替自己的比喻道歉。
- 比喻每 30 秒換：雨傘→麵團→麵包師→陶藝→黏土→攤主；定義句是書面語（1:19「三欄是核對依據和執行紀錄，不是把能力分成互斥的三種」）。
- 「我」2 次、「我們」1 次，14 分鐘只有 8 個問句。

---

## 6. 五個缺失與改法

| # | 缺失 | 證據 | 改法 | 類別 | 可自動化 |
|---|---|---|---|---|---|
| 1 | 旁白沒有「人」：沒名字、沒自稱、沒固定開收尾、沒互動句 | 18 支 我們=25、大家=3、謝謝=0、留言=5；只有 zxHRm5jnELc 1:12 說過「這裡是 Mokaair」；黑貓一支 我們=22 | 給旁白固定人設（名字、固定開場句、固定收尾句、口頭禪）寫進頻道立場與 REGISTER_RULES；每章至少一句「我們」或「你想想看」；結尾固定一個留言問題；放寬 GREETING 正則讓自稱過 | 改稿子 | 部分（人設要站主定） |
| 2 | 免責用語唸出來，數字落點被截斷 | 公告 65／官網 53／為準 31／說明頁 17／沒寫 31／不代表 27；cc09 1:08、1:52、2:03、6:30、6:53；vxv8 2:11、2:44、3:16 | 免責移到字卡與說明欄；旁白每支最多一次「以官網為準」；lint 加詞頻警告；查核 NOT FOUND 改成刪句不是加免責句；數字用「大約／幾成」 | 改稿子＋改產線 | 是 |
| 3 | 合成方式壓平語氣：句間 `<long pause>` 切開再用固定 0.3 s 拼回；表演合約在工人路線被丟掉 | requests.mjs 14–16、92 行；split.mjs 檔頭；PAUSE_BEATS；ILLUSTRATED §聲音表演「settle()…計畫會被丟掉」；站主自記「口吻改了節奏還是平」 | 讓 settle() 保留 `voice.performance`、撰稿三分之一句帶 `emotion`；句間改靠標點、只在章末與「其實」前用 `<long pause>`，對位改用強制對齊；照 voice-audition.md 用「最吃表演的一段」讓站主 A/B 選 style；同段跑 ElevenLabs 試聽（約 US$0.6／支） | 改 TTS 設定 | 部分（站主試聽選一次） |
| 4 | 同一聲音、無配樂無音效、無第二聲音 | 2026-10-03 設定 `no slides_music_track／no slides_sfx_set`；README 純投影片不放配樂；Gemini 單請求可 2 說話者；drama 路線已有多角色 | 站主放一首授權床＋一組音效到 `_music`／`_sfx`、後台填兩個欄位（之後每支自動有床與 stamp／pop）；用第二個 Gemini 聲音唸每章末的問句與觀眾反問（句子本來就在稿裡）；系列固定編號 | 改產線加音效配樂 | 部分（素材要站主給） |
| 5 | 比喻太多太換、開場靠公式，沒有一個人要講一件事的衝動 | cc09 8 個比喻、vxv8 6 個比喻；黑貓全片一貓一人一桌；黑貓開場 0:00「今天我們來講一隻貓」 | REGISTER_RULES 加「一支一個世界」「你以為…其實每支最多一次」「開場用宣告或具體的人」；站主錄 3～5 分鐘自己講某支影片給撰稿代理當口頭禪與自稱的樣本（script-writing.md 本來就要求記進 brief.md）；若願意，5 秒片頭錄一句真人招呼 | 需要站主自己錄音 | 否 |

優先順序：#2 與 #1 是純文字規則、一天內能改、對人味影響最大；#4 只缺站主丟兩個檔案進資料夾；#3 要動 TTS 切句與對位，風險最高但是「聲音平」的根；#5 要站主出聲。

---

## 來源

- 頻道與影片（yt-dlp 2026-10-07）：https://www.youtube.com/@qiqiqushi0/videos ；https://www.youtube.com/watch?v=coA8iBMMLY4 ；https://www.youtube.com/channel/UCzYxev5q9HTv3LvBUMEv87g/videos ；https://www.youtube.com/watch?v=JJGR9qkF0qo ；https://www.youtube.com/watch?v=4KZmdADz1eM ；https://www.youtube.com/channel/UCXjk9RSGtUWbll5iN_Fgmqw/videos ；https://www.youtube.com/channel/UCDSqIYkBjaIijvbniU8RSqg/videos ；https://www.youtube.com/channel/UCUMIaN7_23XZdTToxdZjHrw/videos ；https://www.youtube.com/channel/UChmOSkJUGQkNnyCybYgv7cw/videos ；https://www.youtube.com/@SleeplessHistorian/videos ；https://www.youtube.com/@garychenai/videos
- 觀眾接受度：https://radioink.com/2026/07/07/radio-listeners-cant-detect-ai-voice-but-dont-trust-it-either/ ；https://www.contentgrip.com/ai-voices-in-marketing-adobe/ ；https://air.io/en/creators-spotlight/ai-dubbing-retention-3-youtube-case-studies ；https://kapwing.com/resources/we-grew-a-faceless-youtube-channel-to-1000-subscribers ；https://narrationbox.com/blog/why-ai-voice-sounds-robotic-on-youtube（供應商）；https://cognitivefuture.ai/elevenlabs-for-youtube-creators/（供應商相關）
- 失敗案例與政策：https://www.404media.co/ai-generated-boring-history-videos-are-flooding-youtube-and-drowning-out-real-history/ ；https://www.supertone.ai/en/work/youtube-ai-monetization-policy-2025-eng ；https://technews.tw/2026/06/16/faceless-creators-are-becoming-collateral-damage-in-youtubes-ai-cleanup/ ；https://technews.tw/2026/08/06/youtube-explains-its-ai-slop-policy-and-why-some-creators-wont-get-paid/
- TTS：https://ai.google.dev/gemini-api/docs/speech-generation ；https://ai.google.dev/gemini-api/docs/pricing ；https://costbench.com/software/voice-apis/elevenlabs-api/ ；https://clickup.com/blog/how-to-make-a-podcast-with-notebook-lm/
- 口播寫法：https://youmind.com/zh-TW/skills/script-to-speech-converter-AxqimiY87VajoS ；https://youtubescriptwriter.substack.com/p/your-youtube-script-is-not-an-article
- 產線（唯讀）：/home/user/travel_scanner/tools/video/tts/requests.mjs ；/home/user/travel_scanner/tools/video/tts/split.mjs ；/home/user/travel_scanner/tools/video/automation/register.mjs ；/home/user/travel_scanner/docs/videos/README.md ；/home/user/travel_scanner/docs/videos/ILLUSTRATED.md ；/home/user/travel_scanner/docs/videos/HANDS-OFF.md ；/home/user/travel_scanner/.agents/skills/youtube-video/references/script-writing.md ；/home/user/travel_scanner/tasks/open/2026-10-03-produce-video-openai-devday-2026-recap.md
- 資料包與逐字：<分析暫存區>/data/channel_pack.md ；<分析暫存區>/subs/{S88lbAsLz2E,cc09kA17Xsw,vxv8KrNual8}.zh-TW.vtt ；比對用的字幕與頻道 JSON 在 <分析暫存區>/work/voice/