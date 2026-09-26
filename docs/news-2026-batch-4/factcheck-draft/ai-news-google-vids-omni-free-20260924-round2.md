# 第二輪查核：ai-news-google-vids-omni-free-20260924

- 查核者：獨立查核代理（第二輪，claude-opus-5-5，不是第一輪那位），2026-09-26（台北）
- 規格：`FACTCHECK-48.md`、`docs/news-2026-batch-4/agents/ai/SECOND-ROUND.md`（第一輪規格 `agents/ai/FACTCHECK.md` 全部適用）、DELTA-4-8、第一輪報告，以及協調者在派工訊息裡的四條裁定
- 改動的檔案：內容包 `apps/api/app/guides/content/ai-news-google-vids-omni-free-20260924.json`、研究紀錄 `docs/ai-news-2026-09-late/research/ai-news-google-vids-omni-free-20260924.json`（沒跑 git）
- 自己的抓取：`_raw/ai-news-google-vids-omni-free-20260924/round2/`（fetch-log.tsv、原始 HTML、全頁與 `<article>` 純文字、改動前的內容包與紀錄備份 `pack-before.json`／`record-before.json`）
- 腳本：`_tools/ai-news-google-vids-omni-free-20260924/fc2_*.py`／`fc2_fetch.sh`；改動清單 `fc2_changes.json`

## 摘要

- 查了 **71** 條主張：**58 條確認**、**12 條改寫**、**0 條查無依據**、**1 條留給協調者**。範圍如下：
  - 第一輪改過或新寫的每一句：內容包 22 條主張（16 處替換），加上研究紀錄 6 處。
  - 第一輪「確認」的主張隨機抽三分之一：純確認的 69 條抽 23 條，種子 20260926。
  - 全篇掃一次限定詞與範圍不明的否定句：20 條。
- 內容包 **18 處**替換，其中事實 13 處、協調者裁定 5 處。研究紀錄 **11 處**更正，另加 `factcheck.second_round`。
- 段落總字數從 2,968 降到 **2,895**。騰出來的字數來自拿掉三處「沒有實測」，沒有刪任何但書。
- **最重的發現：Flash-Lite 旁白的狀態，Google 兩篇官方文章寫法不一致。**
  - 本篇的 Vids 公告（9/23 19:00Z）寫 “Coming soon, Gemini 3.8 Flash-Lite text-to-speech in Google Vids will…”。
  - 同一天稍早，Google〈Gemini 3.8 text-to-speech says hello〉（9/23 15:15Z，不在 sources[]）寫 “Gemini 3.8 Flash-Lite TTS is rolling out starting today:”，下面列 “For everyone: In Google Vids”。
  - 內容包原本有四處把它寫成事實：「尚未上線」「這不是 9 月 23 日已經推出的功能」、FAQ「還不能」、「官方沒有公布日期」。
  - 這四處全部改成歸因：「Vids 公告寫 Coming soon」「公告沒有寫日期」。
  - 標題「哪些還沒上線」與第五節標題還是建立在這一項上，要**協調者決定**。
- **FAQ 6 原本的問法是錯的。** 問「把腳本變成旁白的功能現在能用嗎？」、答「還不能」，但 Vids 本來就有 AI 旁白：15609411 列了 AI voice-over、23 種語言，個人帳號每次 1 點。已把問題改成專指「Gemini 3.8 Flash-Lite 旁白」。
- **第一輪精簡歸因語時放大了一個否定句。**
  - 第一段原本寫「這次公告只提到電腦版」，被改成「手機或平板能不能用，目前沒有說明」。
  - 但 Google 的 Get started 頁（15082958，紀錄 `unverified_or_excluded`）寫手機可以看、不能編輯，所以「目前沒有說明」不成立。
  - 已改成「這次沒有說明」，把範圍限縮回這次的公告。
- **補回一個掉了的限定詞。** 15609411 的個人帳號「6 video clips/month」那一格帶 ^^ 註腳：“Personal Google accounts might have some restrictions on AI video editing.”，已補進 §4 的 6 部那一句。
- **範圍不明的否定句**（SECOND-ROUND 第 4 條）：
  - 限縮了六處「官方未說明／官方沒有」：description、summary 4、§3 語言、FAQ 2、FAQ 4、FAQ 5。
  - 另一處是 §3 的「個人帳號什麼時候看到，官方未說明」。部落格寫 “Now anyone…”，所以改成「推出節奏沒有另外寫」。
  - 部落格請讀者去看的 Learning Center 連到讀不到的內部草稿頁，所以「官方」寫不出範圍，一律改成「公告與說明頁」。
- 四條裁定都做了，細節見後面「協調者裁定」一節。
- 研究紀錄 58 條 `verbatim_quote` 在今天的抓取裡都能以連續字串找到：`fc2_quotes.py`，bad 0，沒有一條含 `...`、`…` 或 `|`。
- 自檢：`check_article.py` 顯示 `OK … zh-TW paragraphs 2895`（exit 0）。`pack_cli lint` 只剩 `image_missing` ×2 與 `raw_internal_url`，都是預期內的。
- 結論：**needs_owner**。卡在 Flash-Lite 的狀態，以及建立在它上面的標題與第五節標題；其他查過的主張都沒問題。

## 重抓結果（2026-09-26 14:53–15:01Z）

抓取方式：`curl -sSL --max-time 30`，UA 用 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`。這是站方的 support 信箱，不是個人資料。同一主機間隔 ≥1.5 秒，請求裡沒有任何人的姓名或 email。

| 來源 | HTTP | 落地檔 bytes | 正文 | 備註 |
| --- | --- | --- | --- | --- |
| blog.google `…/workspace/gemini-omni-in-google-vids/` | 200 | 380,362 | 是 | JSON-LD `datePublished` 2026-09-23T19:00:00+00:00；「Read AI-generated summary」三段跳過；`<article>` 正文和第一輪逐字相同 |
| workspaceupdates `…/gemini-omni-11-flash-now-in-vids-….html` | 200 | 204,686 | 是 | 印 September 23, 2026；HTML 裡沒有任何 2026-09-2x 的時刻或時區字串；Resources 連到 15609411（帶 `?sjid=`）與 16143507 |
| support.google.com/docs/answer/15609411 | 200 | 1,698,250 | 是 | `var lang='en'`；`?hl=en` 1,698,698；正文和第一輪相同 |
| support.google.com/docs/answer/16143507 | 200 | 1,633,274 | 是 | `var lang='en'`；`?hl=en` 1,633,308；頂端方框仍寫 “requires an eligible Google Workspace subscription”；正文和第一輪相同 |
| （只用來反駁）blog.google/rss/ | 200 | 29,574 | — | 用來找到下一列的 TTS 公告，不是猜網址 |
| （只用來反駁）blog.google `…/gemini-models/gemini-3-8-text-to-speech/` | 200 | 421,554 | 是 | 〈Gemini 3.8 text-to-speech says hello〉，JSON-LD 2026-09-23T15:15:00+00:00；不在 sources[]，已記進紀錄的 `unverified_or_excluded` |

## 主張表

C＝確認，改＝改寫，留＝留給協調者。編號 C## 沿用第一輪主張表的編號。

### A. 第一輪改過或新寫的句子（28 條）

| # | 位置 | 第一輪之後的句子（摘要） | 判定 | 依據 |
| --- | --- | --- | --- | --- |
| A1 | 第一段（C6） | 「手機或平板能不能用，目前沒有說明」 | 改 | 第一輪把原句「這次公告只提到電腦版」精簡成沒有範圍的否定句，但 Google 的 Get started 頁（15082958）寫 “You can watch processed videos on your mobile device but you can't edit…”。改成「這次沒有說明」；四頁 mobile／phone／tablet 都是 0 次 |
| A2 | 第一段（C7） | 可用地區是「凡是能使用 Google Workspace 帳號的國家與地區」、沒有國家清單、沒點名台灣 | C | 15609411 “You can use these features in all countries and regions where Google Workspace accounts are available”；Taiwan 0 次 |
| A3 | summary 2（C13） | 「對每月額度寫法不同」 | C | 16143507 “Most users can generate up to 50 videos per month.”；15609411 “^^6 video clips/month combined with AI avatars” |
| A4 | §1 第二段（C20） | 延長場景一致性，「這是 Google 的說法」 | C | blog 的 “keeping the visual context, lighting, characters’ appearance, and the environment consistent”；「本站沒有實測驗證」依裁定 4 拿掉 |
| A5 | §1 第二段（C22） | 「或把既有的 AI 片段升頻到 1080p」 | C | blog “upscale existing AI clips” |
| A6 | §1 第三段（C26） | 「這裡提到 SynthID，不代表它符合任何…AI 標示法規」 | C | 編輯但書，沒有替 Google 加任何說法 |
| A7 | 表格（C38） | 「新片段可用 1080p 生成，既有的 AI 片段可升頻到 1080p」 | C | WSU “Create brand-new AI video scenes in full 1080p HD, or upscale existing AI clips” |
| A8 | 表格 caption（C41） | 資料來源補上 Google 說明中心 | C | 3 到 10 秒來自 16143507；另依裁定 2 在 caption 補一句推出節奏 |
| A9 | §3 第二段（C43） | Workspace 版本「包括…等」，補上 Enterprise Essentials、Enterprise Essentials Plus、Nonprofits、Individual | C | WSU “Other Editions: Enterprise Essentials and Enterprise Essentials Plus; Nonprofits; Individual”；清單還有 Education Plus 與兩種加購，所以寫「等」是對的 |
| A10 | §3 第二段（C44） | AI Expanded Access「用量上限比較高」，刪掉「官方沒有寫高多少」 | C | WSU “*Users with AI Expanded Access add-on licenses have higher limits on usage of Omni in Vids.”；15609411 列 “2,000 seconds/month” |
| A11 | §3 第四段（C50） | 「Vids 的許多 AI 功能目前只支援英文」改成直述 | C | 15609411 “Many AI features in Vids are only available in English at this time.” |
| A12 | §3 第四段（C51） | 「AI 短片…提示語言沒有另外列出，中文提示能不能用，官方未說明」 | 改 | 前半句確認：15609411 只列圖片、旁白、虛擬化身、投影片轉影片四項。「官方未說明」沒有範圍，和年齡併成一句「四份官方文件都沒有寫」 |
| A13 | §3 第四段（C52） | 年齡：「四份官方文件都沒有寫」 | C | 四頁 “ age”、18、under、teen、older 都是 0 次 |
| A14 | §4 第二段（C60） | 「個人帳號另有幾項 AI 功能改用點數計算」 | C | 15609411 個人帳號表：Help me create 5 credits、AI voice-over 1 credit、Image generation & editing 1 credit、Slides to Vids 5 credits；Background removal 與 Music generation 空白 |
| A15 | §4 第三段（C67） | 「兩份官方頁…寫法就是不一致」 | C（連動補句） | 兩頁的數字與範圍都不同。為了讓 FAQ 2 的「沒有解釋差異」出現在正文，補「也沒有解釋差異」（見 C6） |
| A16 | §4 第四段（C68） | Workspace 的 Business、Enterprise 方案與 Google AI Pro、Ultra 以秒計 | C | Business 200／500／500 秒、Enterprise 200／500／500 秒、AI Pro 500 秒、Ultra 5x 2,500 秒、Ultra 20x 10,000 秒 |
| A17 | §4 第四段（C70） | 「秒數同樣列在說明頁的表格裡」 | C | 15609411 “AI Expanded Access … 2,000 seconds/month” |
| A18 | §5 第二段（C72） | 「生成說明頁對『上傳自己的影片來改』這一項功能另有地區限制」 | C | 16143507 Important 方框；同一頁另有 “Google AI Pro and Google AI Ultra (USA only)”，所以第一輪拿掉「只」是對的 |
| A19 | §5 第四段（C79） | 「這句話對匯出後影片的效力沒有進一步說明」 | C | 16143507 “Generated images and videos are for use only within Vids.” 之後沒有再說明 |
| A20 | §5 第四段（C80） | 「生成內容也可能不代表真實世界的情況」 | C | “…and may not represent real-world situations.”（保留了「可能」） |
| A21 | FAQ 3（C83） | 部落格寫 vids.new，說明頁步驟都從「在電腦上開啟 Google Vids」開始 | C | 16143507 “Open Google Vids on your computer.” 出現 4 次（生成、動畫、編輯、延長四節各一次） |
| A22 | callout（C87） | 「說明頁本身也寫明額度與功能都可能調整」 | C | 15609411 “The limits and exact features that will continue to be available are subject to change.” |
| A23 | 紀錄 `not_said` | AI Expanded Access 列在 15609411：2,000 seconds/month | C | 15609411 |
| A24 | 紀錄 `must_not_write` | 不寫「官方沒有寫 AI Expanded Access 高多少」 | C | 同上 |
| A25 | 紀錄 `verified_facts` | WSU 沒寫多高，15609411 列 2,000 秒 | C | WSU 與 15609411 |
| A26 | 紀錄 `verified_facts` | Workspace Individual 與 Google AI Plus 是每月 6 部、與虛擬化身合併；其餘列名方案以秒計（Essentials Starter、Education Fundamentals／Standard 空白） | C | 15609411 各表逐格核對 |
| A27 | 紀錄 `verified_facts` | 用點數計的是四項功能 | C | 15609411 個人帳號表 |
| A28 | 紀錄 `editorial_brief` | Business／Enterprise 與 AI Pro／Ultra 以秒計、AI Expanded Access 較高 | C | 15609411 |

### B. 第一輪確認過的主張，隨機抽三分之一（23 條，種子 20260926）

| # | 第一輪編號 | 主張 | 判定 | 依據 |
| --- | --- | --- | --- | --- |
| B1 | C3 | 台北 9/24 凌晨（美國 9/23） | C | JSON-LD 19:00Z＝台北 03:00、太平洋時間 12:00 |
| B2 | C4 | 任何 Google／Workspace 帳號、Gemini Omni 1.1 Flash、新創作控制、免費、高畫質 | C | blog 正文第一段 |
| B3 | C8 | 自己登入看開始畫面有沒有 Create AI videos 最準 | C | 15609411 “won’t display in the “Getting started” screen”；16143507 “From the start menu, select Create AI videos” |
| B4 | C10 | 「免費」「最先進」是 Google 的用語 | C | “at no cost”、“for free”、“Google’s most advanced AI” |
| B5 | C11 | 地區、額度、功能可能再調整 | C | 編輯但書；15609411 “subject to change” |
| B6 | C12 | summary 1 | C | blog；16143507 “720p and 1080p resolution”、“between 3 and 10 seconds” |
| B7 | C18 | Google 表示：最先進的 AI、不需專業剪輯技能或大預算 | C | blog；有歸因 |
| B8 | C19 | 三個創作控制 | C | blog 三個 bullet，WSU 同樣三條 |
| B9 | C25 | SynthID 沒寫怎麼驗證、去哪裡驗證 | C | 範圍是「Google 說」這一句（部落格）；四頁都沒寫 |
| B10 | C30 | 16:9／9:16 | C | 16143507 |
| B11 | C33 | 生成新片段最多 7 張參考圖（Ingredients） | C | “select Ingredients and upload up to 7 images”（編輯模式是 3 張，本句限定在生成新片段，正確） |
| B12 | C36 | 表：延長場景一致性「已上線（Google 說法）」 | C | blog “Now anyone…”；WSU “Users now have access”；裁定 2 |
| B13 | C39 | 表：SynthID「已上線」 | C | blog “Every clip generated with Omni 1.1 in Google Vids includes…” |
| B14 | C54 | 紀錄 diagram 四格 | C | 四格都在正文，數字 3、10、1080 都在正文（check_article 也通過） |
| B15 | C58 | WSU 指定的「AI 用量」說明頁 | C | WSU “Google Vids AI Limits: Learn about availability of AI features” → 15609411 |
| B16 | C61 | 每月 50 點、每月 1 日 12:00 AM PT 重設 | C | 15609411 個人帳號註腳 |
| B17 | C62 | 不能分享、不累積、可能調整 | C | 同上 |
| B18 | C64 | 「多數使用者每月最多可生成 50 部影片」 | C | 16143507 |
| B19 | C69 | 表格上方的預設值「每月最多 500 秒」、各方案不同 | C | 15609411 “unless otherwise specified in the tables below … AI video clips : Up to 500 video clip seconds per month” |
| B20 | C73 | EEA、英國、瑞士、伊利諾州、德州不能上傳來改，只能改生成紀錄 | C | 16143507 “may only use this feature to edit AI generated videos in their generation history” |
| B21 | C85 | FAQ 5：「官方沒有進一步說明」 | 改 | 內容正確，但「官方」沒有範圍 → 「頁面沒有進一步說明」（同一句前面已點名說明頁） |
| B22 | C86 | FAQ 6：「把腳本變成旁白的功能現在能用嗎？還不能。…目前沒有公布正式上線的日期。」 | 改 | 問法錯：15609411 已列 Vids 的 AI voice-over 與 23 種語言，個人帳號 “Cost: 1 credit per voiceover”。「還不能」「沒有公布日期」又與 Google〈Gemini 3.8 text-to-speech says hello〉的 “rolling out starting today … For everyone: In Google Vids” 不一致 → 問題改成專指 Flash-Lite，答案改成歸因 |
| B23 | C89 | 結尾連結 1 的文字 | C | 與 `ai-news-2026-january-september-index` 的 zh-TW title 逐字相同；目標五語齊全。連結 2 同樣逐字相同、五語齊全 |

### C. 全篇掃限定詞與否定句（20 條）

| # | 位置 | 主張 | 判定 | 依據 |
| --- | --- | --- | --- | --- |
| C1 | §4 第二段 | 個人帳號「每月最多可生成 6 部 AI 短片，與 AI 虛擬化身合併計算」 | 改（補限定詞） | 表上這一格帶 ^^ 註腳：“^^Personal Google accounts might have some restrictions on AI video editing.” → 補「AI 影片編輯也可能有一些限制」 |
| C2 | §5 第一段 | 「這不是 9 月 23 日已經推出的功能，官方也沒有公布正式上線的日期」 | 改 | TTS 公告 “Gemini 3.8 Flash-Lite TTS is rolling out starting today:” / “For everyone: In Google Vids” → 刪掉前半句，後半句改成「公告沒有寫正式上線的日期」，開頭改成「Google 在這次的 Vids 公告裡寫」 |
| C3 | 表格 Flash-Lite 那一列 | 狀態「Coming soon，尚未上線」 | 改 | 同上 → 「Vids 公告寫 Coming soon」 |
| C4 | summary 4 | 「官方目前沒有說明年齡限制、中文提示…，也沒有公布…上線時間，這項旁白功能目前是 Coming soon」 | 改 | 範圍限縮到「這次的公告與說明頁」；旁白部分歸因給 Vids 公告 |
| C5 | description | 「年齡限制與中文提示官方未說明」 | 改 | → 「公告與說明頁都沒有寫」。長度 130，仍以（2026 年 9 月查證）結尾 |
| C6 | FAQ 2 | 「官方沒有解釋兩者的差異」 | 改 | → 「兩頁都沒有解釋兩者的差異」。部落格的 Learning Center 連結是讀不到的草稿頁，「官方」無從查起；正文 §4 同步補一句 |
| C7 | FAQ 4 | 「中文提示能不能用，官方未說明」 | 改 | → 「也沒有寫」，範圍跟著句首的「Google 的說明頁」 |
| C8 | §3 第三段 | 「從美國時間 2026 年 9 月 23 日起」與「個人 Google 帳號什麼時候看到，官方未說明」 | 改 | 裁定 1：WSU 沒有時區 → 「Google 寫 9 月 23 日起」。部落格寫 “Now anyone…”，WSU 只是沒有另外寫個人帳號的節奏 → 「個人 Google 帳號的推出節奏沒有另外寫」 |
| C9 | summary 2、§4、FAQ 2 | “Most users” | C | 三處都寫「多數使用者」 |
| C10 | §2、§4 | “up to”：7 張、500 秒、50 部 | C | 三處都有「最多」 |
| C11 | 第一段、表格 | “now”：「現在都能」「已上線」 | C | blog “Now anyone…”；裁定 2 |
| C12 | 表格 caption、§3 | “1–3 days” 只講 Workspace 網域 | C | WSU “Rapid Release and Scheduled Release domains: Full rollout (1–3 days for feature visibility)” |
| C13 | 表格、summary 4、§5、FAQ 6 | “Coming soon” 四處都保留 | C | blog |
| C14 | §5 | “may”：只能改生成紀錄、可能不代表真實 | C | 16143507 |
| C15 | title、第五節標題 | 「哪些還沒上線」「還沒上線與使用前的提醒」 | 留 | 唯一對應的項目是 Flash-Lite 旁白，而兩篇 Google 公告寫法不一致。沒有自己改標題，選項見待決事項 1 |
| C16 | 全篇 | 16143507 “requires an eligible Google Workspace subscription” 方框 | C | 裁定 3：內容包兩處「訂閱」分別是「AI Pro 與 Ultra 訂閱者」「不建議該不該訂閱」，沒有寫成「要訂閱才能用」 |
| C17 | 全篇 | 「沒有實測」類句子 | C（已照裁定 4 處理） | 現在只有 callout 一處「Mokaair 沒有實際測試效果」 |
| C18 | 研究紀錄 | 58 條 `verbatim_quote` 都是連續字串 | C | `fc2_quotes.py` bad 0 |
| C19 | 全篇 | 界線 | C | topics 是 ai／software／ai-news，沒有 finance；只有一個 callout；沒有價格、訂閱建議或推定台灣可用；廠商宣稱都有歸因；不和 `ai-news-gemini-omni-20260519` 衝突（那篇沒提 Vids、SynthID、Flash-Lite） |
| C20 | 研究紀錄 | 每條 fact 的 url 都在內容包的 sources[] 裡 | C | `fc2_quotes.py` |

## 修改（改前 → 改後，來源）

### 內容包，事實修改 13 處

1. **第一段**（A1）
   - 改前：「；手機或平板能不能用，目前沒有說明。」
   - 改後：「；手機或平板能不能用，這次沒有說明。」
   - 來源：https://blog.google/products-and-platforms/products/workspace/gemini-omni-in-google-vids/
2. **表格 Flash-Lite 狀態**（C3）
   - 改前：「Coming soon，尚未上線」
   - 改後：「Vids 公告寫 Coming soon」
   - 來源：同上。反證是 https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-text-to-speech/
3. **§3 語言與年齡**（A12）
   - 改前：「…則沒有另外列出，中文提示能不能用，官方未說明；這項功能是否有年齡限制，四份官方文件都沒有寫。」
   - 改後：「…則沒有另外列出；中文提示能不能用、這項功能是否有年齡限制，四份官方文件都沒有寫。」
   - 來源：https://support.google.com/docs/answer/15609411
4. **§4 第二段**（C1）
   - 改前：「…與 AI 虛擬化身合併計算；個人帳號另有…」
   - 改後：「…與 AI 虛擬化身合併計算，AI 影片編輯也可能有一些限制；個人帳號另有…」
   - 來源：15609411
5. **§4 第三段**（A15／C6 連動）
   - 改前：「…的寫法就是不一致，這一篇兩個數字都列出來，」
   - 改後：「…的寫法就是不一致，也沒有解釋差異；這一篇兩個數字都列出來，」
   - 來源：https://support.google.com/docs/answer/16143507
6. **§5 第一段**（C2）
   - 改前：「Google 在公告裡寫，…100 多種語言的旁白；這不是 9 月 23 日已經推出的功能，官方也沒有公布正式上線的日期。」
   - 改後：「Google 在這次的 Vids 公告裡寫，…100 多種語言的旁白；公告沒有寫正式上線的日期。」
   - 來源：blog。反證是 TTS 公告
7. **summary 4**（C4）
   - 改前：「官方目前沒有說明年齡限制、中文提示能不能用，也沒有公布 Gemini 3.8 Flash-Lite 旁白的上線時間，這項旁白功能目前是 Coming soon。」
   - 改後：「這次的公告與說明頁都沒有寫年齡限制、中文提示能不能用；Gemini 3.8 Flash-Lite 旁白，Vids 的公告寫的是 Coming soon，也沒有寫上線日期。」
   - 來源：blog；15609411
8. **description**（C5）
   - 改前：「年齡限制與中文提示官方未說明（2026 年 9 月查證）。」
   - 改後：「年齡限制與中文提示，公告與說明頁都沒有寫（2026 年 9 月查證）。」
   - 來源：15609411
9. **FAQ 2**（C6）
   - 改前：「官方沒有解釋兩者的差異」
   - 改後：「兩頁都沒有解釋兩者的差異」
   - 來源：16143507
10. **FAQ 4**（C7）
    - 改前：「中文提示能不能用，官方未說明。」
    - 改後：「中文提示能不能用，也沒有寫。」
    - 來源：15609411
11. **FAQ 5**（B21）
    - 改前：「這句話對匯出後的影片有什麼效力，官方沒有進一步說明；」
    - 改後：「…有什麼效力，頁面沒有進一步說明；」
    - 這一處是分兩步改的（`fc2_edit.py` 先改成「說明頁」，`fc2_record.py` 再避開同句重複的詞）。
    - 來源：16143507
12. **FAQ 6 問題**（B22）
    - 改前：「把腳本變成旁白的功能現在能用嗎？」
    - 改後：「Gemini 3.8 Flash-Lite 旁白現在能用嗎？」
    - 來源：15609411（Vids 已有 AI voice-over）
13. **FAQ 6 答案**（B22）
    - 改前：「還不能。Google 在公告裡寫這是「Coming soon」，屆時預計能把腳本轉成 100 多種語言的旁白，但目前沒有公布正式上線的日期。」
    - 改後：「Google 在這次的 Vids 公告裡寫這是「Coming soon」，屆時預計能把腳本轉成 100 多種語言的旁白，公告沒有寫正式上線的日期；請以自己登入後看到的畫面為準。」
    - 來源：blog。最後一句與 callout 相同

### 內容包，協調者裁定 5 處

14. **裁定 4，第二段**
    - 改前：「…宣傳用語，Mokaair 沒有實際生成過影片、也沒有測試效果；這裡不提供…」
    - 改後：「…宣傳用語；這裡不提供…」
15. **裁定 4，§1 第一段**
    - 改前：「——這是 Google 自己的說法，Mokaair 沒有實際測試。」
    - 改後：「——這是 Google 自己的說法。」
16. **裁定 4，§1 第二段**
    - 改前：「這是 Google 的說法，本站沒有實測驗證；」
    - 改後：「這是 Google 的說法；」
17. **裁定 2，表格 caption**
    - 在查核日之後加：「「已上線」照 Google 的說法；Workspace 網域從 9 月 23 日起需要 1 到 3 天才會看到。」
    - 來源：WSU
18. **裁定 1，§3 第三段**
    - 改前：「推出節奏方面，Workspace Updates 寫的是 Rapid Release 與 Scheduled Release 兩種 Workspace 網域，從美國時間 2026 年 9 月 23 日起全面推出，…；這一句只講 Workspace 網域，個人 Google 帳號什麼時候看到，官方未說明。」
    - 改後：「推出節奏方面，Rapid Release 與 Scheduled Release 兩種 Workspace 網域，Google 寫 9 月 23 日起全面推出，…；這一句只講 Workspace 網域，個人 Google 帳號的推出節奏沒有另外寫。」
    - 來源：https://workspaceupdates.googleblog.com/2026/09/gemini-omni-11-flash-now-in-vids-with-improved-extension-quality-1080p-and-duration-control.html

### 研究紀錄 11 處

每一處的原文與改後文字都在 `fc2_changes.json`，也寫進了紀錄的 `factcheck.second_round.changes`。

1. **`event_date_basis`**：推出節奏的日期改成「Google 寫 9 月 23 日起」，不加「美國時間」（裁定 1），並寫明事件日那一行仍依 JSON-LD。
2. **`verified_facts`，WSU 發文日**：「美國日期，沒有時刻」改成「沒有時刻，也沒有時區」。
3. **`verified_facts`，推出節奏**：拿掉「美國時間」。
4. **`live_data_warnings`，推出節奏**：拿掉「美國時間」。
5. **`verified_facts`，Flash-Lite**：原本寫「還沒上線」「不是 9 月 23 日已推出」，第二輪更正，加上 TTS 公告的原句與寫法規則。
6. **`not_said`，Flash-Lite**：範圍限縮到「Vids 公告」。
7. **`must_not_write`，Flash-Lite**：
   - 不把「還沒上線」「不是 9 月 23 日推出」「官方沒有公布日期」寫成事實。
   - Vids 本來就有 AI 旁白，不要把「腳本轉旁白」整個寫成還不能用。
8. **`must_not_write`，一致性**：記下裁定 4（「沒有實測」這類句子只留 callout 一處）。
9. **`unverified_or_excluded`，TTS 公告**：原本寫「本紀錄沒有抓」，改成第二輪實際抓到的狀態碼、bytes、JSON-LD 時間與兩句原文，並寫明為什麼不能用、留給協調者。
10. **`live_data_warnings`，Flash-Lite**：記下兩篇不一致。
11. **`verified_facts`，^^ 註腳**：記下這個註腳掛在 6 部那一格，第二輪已補進正文。

- 另加 `factcheck.second_round`：claims_checked 71、verdicts、pack_replacements 18、record_edits 11、changes 29、open_questions、coordinator_rulings、conclusion。
- `title` 沒改。第一輪的 `factcheck` 物件沒動。

## 協調者裁定的執行

1. **Workspace Updates 的推出日沒有時區。**
   - §3 改成「Google 寫 9 月 23 日起全面推出」，表格 caption 用同一個日期。
   - 紀錄裡四處「美國時間」的推出日說法一起改掉，免得翻譯或之後的輪次加回去。
   - 事件日那一行（台北 9/24 凌晨／美國時間 9/23，依部落格 JSON-LD）在 description、第一段、summary 1、圖 caption 四處照舊。內容包現在的四個「美國時間」全是這一行。
2. **表格的「已上線」保留。**
   - caption 補「「已上線」照 Google 的說法；Workspace 網域從 9 月 23 日起需要 1 到 3 天才會看到」。
   - §3 保留 1 到 3 天，並寫個人帳號的節奏沒有另外寫。
   - Flash-Lite 那一列不屬於「已上線」，另外處理（C3）。
3. **16143507 頂端的過時方框不用。** 今天重抓仍在頁上，內容包沒有任何一句用它。
4. **「沒有實測」只留一處。**
   - 留在 callout：「Mokaair 沒有實際測試效果」，因為那一格是讀者動手前會讀的提醒。
   - 第二段、§1 兩段的三處拿掉。那三處的廠商宣稱仍然歸因：「Google 表示」「這是 Google 自己的說法」「這是 Google 的說法」。
- 字數：2,968 → 2,895，低於上限 3,000。

## 待協調者決定

1. **Flash-Lite 旁白的狀態，以及建立在它上面的標題**（needs_owner）。
   - 兩篇 Google 官方文章的說法：
     - Vids 公告（sources[] 第 1 條，9/23 19:00Z）：“Coming soon, Gemini 3.8 Flash-Lite text-to-speech in Google Vids will turn any script into a natural-sounding voiceover across 100+ languages.”
     - 〈Gemini 3.8 text-to-speech says hello〉（9/23 15:15Z，不在 sources[]）：“Gemini 3.8 Flash-Lite TTS is rolling out starting today:”，下面列 “For everyone: In Google Vids”。
   - 正文現在只寫 Vids 公告的說法並歸因，沒有一句把它寫成已上線或未上線的事實。
   - 但標題「哪些還沒上線」與第五節標題「還沒上線與使用前的提醒」唯一對應的就是這一項。選項：
     - (a) 維持：Vids 公告是事件本身的來源，正文已歸因。
     - (b) 改標題與節標題，例如「…：誰能用、額度怎麼讀、使用前的限制」、「預告中的功能與使用前的提醒」。改標題要同步紀錄的 `title`。
     - (c) 換一條來源，讓兩篇並列。但四條都沒有空位：WSU 撐著推出節奏、適用版本、管理員開關與「指定的說明頁」。
   - 候選清單（`candidates-since-0922-ai.md` 第 195 行）與紀錄原本都把它當成「還沒上線」，這一點也要一起更正。
2. **手機或平板。**
   - Google 的 Get started 頁（15082958）寫手機可以看已處理的影片、不能編輯，產品頁也寫只支援在電腦上製作。
   - 正文只寫「這次沒有說明」。要寫得更明確，就得換一條來源。
3. **活頁面。** DELTA-4-8 第 7 條的兩份說明頁，加上 TTS 公告，發布當天要重讀。

## 讀者優先的檢查

- 內容包裡「本文」出現 0 次。description 以「（2026 年 9 月查證）」結尾，長度 130。title、description、summary 都沒有選題計數。
- 歸因語數量：
  - 第一段仍然只有一個（「Google 官方部落格宣布」）。「這次沒有說明」是範圍詞，不是歸因語。
  - 正文每段最多兩個。改過的段落逐段數過：§1 第一段 2 個、§3 第三段 2 個、§3 第四段 1 個、§4 第三段 2 個、§5 第一段 2 個。
- 「這一篇」出現在第二段與 §4，屬於風格問題，沒有動。
- 第二段的「這裡不提供帳號或方案的購買建議」和 callout 的「這裡也不是使用或購買建議」重複，同樣屬於風格，沒有動。

## 自檢輸出（原樣）

```
OK ai-news-google-vids-omni-free-20260924 zh-TW paragraphs 2895
check_article exit=0
```

```
ai-news-google-vids-omni-free-20260924
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/ai-news-google-vids-omni-free-20260924/hero.jpg
  error: image_missing: zh-TW: /guides/ai-news-google-vids-omni-free-20260924/diagram-1.svg
1 entries checked
lint exit=1
```

```
items 58 bad 0
exit=0
```
