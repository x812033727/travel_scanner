# 第一輪查核：ai-news-google-vids-omni-free-20260924

- 查核者：獨立查核代理（第一輪，claude-opus-5-5），2026-09-26（台北）
- 規格：`FACTCHECK-48.md`、`docs/news-2026-batch-4/agents/ai/FACTCHECK.md`、DELTA-4-8（全文）、DELTA-4-7 第 3、4、10、11、14、16 條、DELTA-4-5、BRIEF 十二條錯誤型態
- 改動的檔案：內容包 `apps/api/app/guides/content/ai-news-google-vids-omni-free-20260924.json`、研究紀錄 `docs/ai-news-2026-09-late/research/ai-news-google-vids-omni-free-20260924.json`（沒跑 git）
- 自己的抓取：`_raw/ai-news-google-vids-omni-free-20260924/round1/`（fetch-log.tsv、原始 HTML、純文字、改動前的內容包與紀錄備份）；腳本：`_tools/ai-news-google-vids-omni-free-20260924/fc1_*.py`

## 摘要

- 查了 **91** 條主張：**76 條確認**、**13 條改寫**、**2 條查無依據**（改寫或刪除）。事實修改一共 **15 條主張、13 處文字替換**；另有 3 處是依讀者優先規則精簡歸因語，事實不變。內容包合計 16 處替換，研究紀錄 6 處。
- 撰稿者要求優先查的三點：
  1. **兩段免費額度**：兩個數字、各自的重設時間，以及「與 AI 虛擬化身合併計算」這個但書，都掛在正確的說明頁上（6 部＋合併計算＋點數重設在 15609411；50 部＋每月 1 日 12 AM PT＋家庭共用在 16143507）。兩頁今天重抓都是英文版。有兩處修正：一是摘要把 50 部寫成「免費額度」，但 16143507 寫的是 “Most users”，已改成「每月額度」；二是「互相矛盾」改成「不一致」，因為兩頁講的對象範圍不同。
  2. **地區**：與說明頁原句相符，沒有寫成台灣被排除。發現一處錯：「地區限制只出現在上傳影片來改」不成立，同一頁的虛擬化身素材寫明 “Google AI Pro and Google AI Ultra (USA only)”，已拿掉「只」。
  3. **Workspace 版本清單**：原本讀起來像完整清單，其實漏列了版本。已補回 Enterprise Essentials、Enterprise Essentials Plus、Nonprofits、Individual，並改成「包括……等」；教育版照指示不寫。Frontline 寫成「不包含」（依 15609411），沒列出的版本沒有寫成「被排除」。
- **研究紀錄本身有錯**，已一併更正，免得第二輪把文章改回去：
  - 紀錄寫 AI Expanded Access「沒寫高多少」，但 15609411 的表格列了 `2,000 seconds/month`。
  - 紀錄寫「付費與 Workspace 方案以秒計」，但 Workspace Individual 是付費方案，表上仍是 `6 video clips/month combined with AI avatars`。
  - 紀錄寫「其他 AI 功能用點數計」，但表上只有四項功能列點數，Background removal 與 Music generation 兩格空白。
- 第 4 點全部確認：
  - 日期行照裁定寫。
  - 推出起算日是 Google 印的 9 月 23 日。
  - 只寫電腦版（vids.new）；Flash-Lite 旁白寫 Coming soon。
  - 沒有寫 SynthID 符合任何法規，也沒有取用 AI 摘要的內容。
  - 沒有價格，沒有談 Google AI Plus。
- 自檢結果：`check_article.py`：`OK ai-news-google-vids-omni-free-20260924 zh-TW paragraphs 2968`（exit 0）。`pack_cli lint` 只剩 `image_missing` ×2 與 `raw_internal_url`（依規格屬預期）。
- 結論：**needs_second_round**。事實修改超過十處，而且第一輪新寫的句子還沒有人查過。

## 重抓結果（2026-09-26 14:37–14:39Z，`curl -sSL --max-time 30`，UA `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`，同一主機間隔 ≥1 秒）

| 來源 | HTTP | 落地檔 bytes | 正文 | 備註 |
| --- | --- | --- | --- | --- |
| blog.google `…/workspace/gemini-omni-in-google-vids/` | 200 | 380,362 | 是 | JSON-LD `datePublished` 2026-09-23T19:00:00+00:00，可見日期 Sep 23, 2026；「Read AI-generated summary」三段跳過；Learning Center 連結仍指向 `support-content-draft.corp.google.com`，沒有請求 |
| workspaceupdates.googleblog.com `…/gemini-omni-11-flash-now-in-vids-….html` | 200 | 204,686 | 是 | 印 September 23, 2026；Resources 連到 15609411 與 16143507 |
| support.google.com/docs/answer/15609411 | 200 | 1,698,237 | 是 | `var lang='en'`；另抓 `?hl=en` 1,698,705，正文相同 |
| support.google.com/docs/answer/16143507 | 200 | 1,632,847 | 是 | `var lang='en'`；另抓 `?hl=en` 1,633,304，正文相同 |

研究紀錄 58 條 `verbatim_quote`（4 條 sources、54 條 verified_facts）在今天的抓取裡都能以連續字串找到（`fc1_check_quotes.py`，bad 0）。每條 fact 的 `url` 都在內容包的 `sources[]` 裡。

## 主張表

C＝確認，改＝改寫，無＝查無依據（已改寫或刪除），風＝讀者優先的歸因精簡（事實不變）。

| # | 位置 | 主張（摘要） | 判定 | 依據 |
| --- | --- | --- | --- | --- |
| 1 | title | Google Vids 開放免費用 Gemini Omni 1.1 做影片 | C | blog “generate high-quality videos at no cost using our latest Gemini Omni 1.1 Flash model” |
| 2 | description | 日期行、任何 Google 帳號在電腦版免費生成、兩份說明頁寫法不同、年齡與中文提示未說明；以（2026 年 9 月查證）結尾 | C | blog；15609411；16143507；四頁 age／18／under／Taiwan 皆 0 次 |
| 3 | 第一段 | 台北 9/24 凌晨（美國 9/23） | C | JSON-LD 19:00Z＝台北 03:00；DELTA-4-8 第 4 條 |
| 4 | 第一段 | 任何 Google／Workspace 帳號、最新 Gemini Omni 1.1 Flash、新創作控制、免費、高畫質 | C | blog 第一段 |
| 5 | 第一段 | 在電腦開 vids.new、選 Create AI videos | C | “visiting vids.new on desktop and selecting "Create AI videos."” |
| 6 | 第一段 | 只提到電腦版，手機平板沒寫 | C／風 | 四頁 mobile／phone／tablet 0 次；歸因語精簡 |
| 7 | 第一段 | 凡能用 Workspace 帳號的國家與地區、沒有國家清單、沒點名台灣 | C／風 | 15609411 “all countries and regions where Google Workspace accounts are available”；Taiwan 0 次 |
| 8 | 第一段 | 登入後看開始畫面有沒有 Create AI videos 最準 | C | 15609411 “the associated option won’t display in the “Getting started” screen” |
| 9 | 第二段 | 查核日 2026-09-26 | C | 與 sources[].checked_on、紀錄、caption 一致 |
| 10 | 第二段 | 「免費」「最先進」是 Google 的用語 | C | “at no cost”、“Google’s most advanced AI” |
| 11 | 第二段 | 地區、額度、功能可能調整 | C | 15609411 “subject to change” |
| 12 | summary 1 | 日期、任何帳號、電腦、Omni 1.1 免費、3–10 秒、720p／1080p | C | blog；16143507 |
| 13 | summary 2 | 兩頁「對免費額度」寫法不同 | 改 | 16143507 寫 “Most users”，不是指免費額度 → 「每月額度」 |
| 14 | summary 2 | 6 部＋合併計算；多數使用者最多 50 部；截至 9/26 | C | 15609411 “^^6 video clips/month combined with AI avatars”；16143507 “Most users can generate up to 50 videos per month.” |
| 15 | summary 3 | Frontline 不含；公司學校帳號由管理員決定 | C | 15609411 |
| 16 | summary 4 | 年齡、中文提示未說明；旁白沒有日期、Coming soon | C | blog；四頁 0 次 |
| 17 | §1 | 同時發在官方部落格與 Workspace Updates | C | 兩頁都是 Sep 23 |
| 18 | §1 | Google 表示整合最先進的 AI，不需專業剪輯技能或大預算 | C | 已歸因為廠商宣稱 |
| 19 | §1 | 三個創作控制 | C | blog 三個 bullet |
| 20 | §1 | 延長場景維持脈絡、光線、角色外觀、環境；「Google 說明這一致性由模型維持」 | 無 | 前半句確認；「由模型維持」原文沒有 → 「這是 Google 的說法」 |
| 21 | §1 | 指定秒數、對上故事與旁白、3–10 秒 | C | blog；16143507 “between 3 and 10 seconds” |
| 22 | §1 | 1080p 生成新場景，或把「既有片段」升頻 | 改 | 原文 “upscale existing AI clips”／“upscaling AI videos” → 「既有的 AI 片段」 |
| 23 | §1 | 每段 Omni 1.1 片段嵌入看不到的 SynthID | C | blog |
| 24 | §1 | Google 說觀眾能驗證是 AI 生成 | C | “This allows viewers to verify…” |
| 25 | §1 | 沒寫怎麼驗證、去哪驗證 | C | 四頁都沒有 |
| 26 | §1 | SynthID 是 Google 自己的浮水印技術 | 無 | 四條來源都沒寫 → 刪掉，只留「這裡提到 SynthID，不代表……符合」 |
| 27 | §1 | 不代表符合任何 AI 標示法規 | C | 編輯但書；紀錄 must_not_write |
| 28 | §2 | 24fps | C | 16143507 |
| 29 | §2 | 720p 與 1080p | C | “720p and 1080p resolution” |
| 30 | §2 | 16:9／9:16 | C | 16143507 |
| 31 | §2 | 長度可選 3–10 秒 | C | 16143507（生成、編輯兩處） |
| 32 | §2 | 四種生成方式 | C | 16143507 第一段 |
| 33 | §2 | 最多 7 張參考圖（Ingredients） | C | “upload up to 7 images” |
| 34 | §2 | 關分頁紀錄就消失 | C | “When you close the Vids tab, the history disappears.” |
| 35 | §2 | 要插入 Vid 才能事後存取 | C | “insert it into your Vid” |
| 36 | 表 | 延長場景一致性，已上線（Google 說法） | C | blog；WSU “Users now have access” |
| 37 | 表 | 指定秒數 3–10 | C | 16143507 |
| 38 | 表 | 「既有片段可升頻到 1080p」 | 改 | 同 #22 |
| 39 | 表 | SynthID 已上線 | C | blog |
| 40 | 表 | Flash-Lite 旁白、100 多種語言、Coming soon | C | blog |
| 41 | 表 caption | 資料來源只列部落格與 Workspace Updates | 改 | 3–10 秒來自說明頁 → 加「與 Google 說明中心」 |
| 42 | §3 | 消費者：個人帳號、Google AI Pro 與 Ultra | C | WSU “Consumer: Users with personal Google accounts; Google AI Pro and Ultra” |
| 43 | §3 | Workspace 清單只列 Business／Enterprise 六種 | 改 | WSU 另有 “Enterprise Essentials and Enterprise Essentials Plus; Nonprofits; Individual”、Education Plus、兩種教育加購、AI Expanded Access → 補四種、改「包括……等」，教育版不寫 |
| 44 | §3 | AI Expanded Access 上限較高，「但官方沒有寫高多少」 | 改 | WSU 的確沒寫，但 15609411 列 “2,000 seconds/month” → 刪掉否定句 |
| 45 | §3 | Frontline 明確不含 Vids 的 Gemini 功能 | C | “Google Workspace Frontline doesn’t include access to Gemini features in Google Vids.” |
| 46 | §3 | 工作學校帳號由管理員決定 Vids 與生成式 AI | C | 15609411 |
| 47 | §3 | 這次更新沒有管理員開關 | C | “This feature does not have an admin control.” |
| 48 | §3 | Rapid／Scheduled Release、9/23 起、1–3 天 | C | WSU；「美國時間」標籤見待決事項 |
| 49 | §3 | 個人帳號推出節奏沒寫 | C | WSU 只講 Workspace 網域 |
| 50 | §3 | 許多 AI 功能目前只支援英文 | C／風 | 15609411 |
| 51 | §3 | AI 短片沒列提示語言、中文未說明 | C／風 | 15609411 只列圖片、旁白、虛擬化身、投影片轉影片四項；16143507 只連到一般語言頁（14925782 的 Vids 段也只有那四項） |
| 52 | §3 | 四份文件都沒寫年齡 | C／風 | 四頁 age／18／under／teen／older 0 次 |
| 53 | 圖 caption | 日期、適用帳號、裝置、規格、額度、查核日 | C | 同上 |
| 54 | 紀錄 diagram | 四格（誰能用／在哪裡做／能做什麼／額度多少） | C | 「列名方案」「電腦上開 vids.new」「3 到 10 秒、1080p」「兩份說明頁寫法不同」都在正文 |
| 55 | 紀錄 hero_label | 免費生成影片的條件 | C | — |
| 56 | §4 | 部落格沒寫額度數字，只請個人帳號看 Google AI 方案 | C | “For more access to AI video generation in Google Vids on your personal account, explore our Google AI plans” |
| 57 | §4 | 不寫價格、不建議訂閱 | C | 內容包沒有價格 |
| 58 | §4 | Workspace Updates 指定的「AI 用量」說明頁 | C | Resources “Google Vids AI Limits” → 15609411 |
| 59 | §4 | 個人帳號每月 6 部 AI 短片、與虛擬化身合併計算 | C | “^^6 video clips/month combined with AI avatars” |
| 60 | §4 | 「其他 AI 功能」改用點數 | 改 | 表上只有 Help me create、AI voice-over、Image generation & editing、Slides to Vids 四項列點數，Background removal、Music generation 空白 → 「另有幾項 AI 功能」 |
| 61 | §4 | 每月 50 點、每月 1 日 12:00 AM PT 重設 | C | 15609411 footnote（這個重設時間是點數的，掛在正確的頁上） |
| 62 | §4 | 不能分享、不累積、可能調整 | C | 15609411 |
| 63 | §4 | 同一份公告指定的另一份生成說明頁 | C | Resources → 16143507 |
| 64 | §4 | 「多數使用者每月最多可生成 50 部影片」 | C | 16143507 |
| 65 | §4 | 一樣是每月 1 日太平洋時間午夜 12 點重設 | C | “resets at 12 AM PT on the first day of the month” |
| 66 | §4 | AI Pro／Ultra 家庭共用時額度共用 | C | 16143507 |
| 67 | §4 | 兩頁「互相矛盾」 | 改 | 兩頁講的範圍不同（個人帳號／多數使用者），來源撐得住的是「不一致」 |
| 68 | §4 | 「付費與 Workspace 方案」以秒計 | 改 | Workspace Individual（付費）是 “6 video clips/month combined with AI avatars” → 「Workspace 的 Business、Enterprise 方案與 Google AI Pro、Ultra」 |
| 69 | §4 | 表頭預設每月最多 500 秒、各方案不同 | C | “Up to 500 video clip seconds per month” |
| 70 | §4 | AI Expanded Access「官方沒有寫高多少」 | 改 | 15609411 “2,000 seconds/month” → 「秒數同樣列在說明頁的表格裡」（依紀錄，不逐一抄各方案秒數） |
| 71 | §5 | Flash-Lite 旁白 Coming soon、100 多種語言、不是 9/23 已推出、沒有日期 | C | blog |
| 72 | §5 | 「地區限制只出現在」上傳影片來改 | 改 | 同頁虛擬化身素材 “Google AI Pro and Google AI Ultra (USA only)” → 「生成說明頁對……另有地區限制」 |
| 73 | §5 | EEA、英國、瑞士、伊利諾州、德州不能上傳來改，只能改生成紀錄 | C | 16143507 Important 方框 |
| 74 | §5 | 超過 10 秒只改最後 10 秒 | C | 16143507 |
| 75 | §5 | 不代表這些地區不能生成，也不能當台灣全功能可用的證明 | C | 範圍說明；沒有寫成台灣被排除 |
| 76 | §5 | 個人帳號只有預設虛擬化身 | C | “^Personal Google accounts only have access to preset AI avatars” |
| 77 | §5 | 虛擬化身素材限英文、列名方案；消費者只列 AI Pro／Ultra（僅限美國）；個人免費帳號不在清單 | C | 16143507 “Check Avatar availability” |
| 78 | §5 | 生成式 AI、受 Generative AI Prohibited Use Policy 約束 | C | 16143507 |
| 79 | §5 | 「只供在 Vids 內使用」、效力沒有進一步說明 | C／風 | “Generated images and videos are for use only within Vids.” |
| 80 | §5 | 可能不代表真實世界的情況 | C／風 | 16143507 |
| 81 | FAQ 1 | 台灣：原句、沒點名、自己登入看 | C | 15609411 |
| 82 | FAQ 2 | 兩個數字、截至 9/26、沒解釋差異 | C | 兩頁 |
| 83 | FAQ 3 | 「公告與說明頁都只寫在電腦上開啟 vids.new」 | 改 | 說明頁沒提 vids.new，步驟是 “Open Google Vids on your computer.” → 分開寫 |
| 84 | FAQ 4 | 中文提示未說明 | C | 同 #51 |
| 85 | FAQ 5 | 只供在 Vids 內使用、政策、可能不代表真實 | C | 16143507 |
| 86 | FAQ 6 | 旁白還不能用、Coming soon、沒有日期 | C | blog |
| 87 | callout | 說明頁寫「方案與額度隨時可能調整」 | 改 | 原文 “The limits and exact features … are subject to change” → 「額度與功能都可能調整」 |
| 88 | callout | 沒實測、不是使用或購買建議、以登入畫面為準 | C | 編輯但書 |
| 89 | 連結 1 | 2026 年 AI 新聞總整理：1 月至 9 月的重點與生活應用 | C | 與目標內容包 zh-TW title 逐字相同；目標五語齊全 |
| 90 | 連結 2 | Gemini Omni 在 I/O 亮相：用對話改影片，素材與連續性仍要自己把關 | C | 同上；DELTA-4-8 第 5 條 |
| 91 | sources[] | 四條標題、網址、checked_on 2026-09-26 | C | 今天重抓全部 200、正文 |

## 修改（改前 → 改後，來源）

1. 摘要第 2 項：「對免費額度寫法不同」→「對每月額度寫法不同」。來源：https://support.google.com/docs/answer/16143507
2. §1 延長場景：「，Google 說明這一致性由模型維持，本站沒有實測驗證；」→「，這是 Google 的說法，本站沒有實測驗證；」。來源：blog
3. §1 升頻：「或把既有片段升頻到 1080p。」→「或把既有的 AI 片段升頻到 1080p。」。來源：blog
4. §1 SynthID：「SynthID 是 Google 自己的浮水印技術，這裡不代表它符合任何國家或地區的 AI 標示法規。」→「這裡提到 SynthID，不代表它符合任何國家或地區的 AI 標示法規。」。來源：blog
5. 表格 1080p 那一格：「既有片段可升頻到 1080p」→「既有的 AI 片段可升頻到 1080p」。來源：Workspace Updates
6. 表格 caption：「資料來源：Google 官方部落格與 Google Workspace Updates 公告，…」→「資料來源：Google 官方部落格、Google Workspace Updates 公告與 Google 說明中心，…」。來源：16143507
7. §3 Workspace 段：「清單列出 Business Starter、Standard、Plus，以及 Enterprise Starter、Standard、Plus；買了 AI Expanded Access 加購授權的使用者，用量上限比較高，但官方沒有寫高多少。」→「清單列出的版本包括 Business Starter、Standard、Plus，Enterprise Starter、Standard、Plus，以及 Enterprise Essentials、Enterprise Essentials Plus、Nonprofits、Individual 等；買了 AI Expanded Access 加購授權的使用者，用量上限比較高。」。來源：Workspace Updates；15609411
8. §4 點數：「個人帳號其他 AI 功能改用點數計算」→「個人帳號另有幾項 AI 功能改用點數計算」。來源：15609411
9. §4 兩頁：「兩份官方頁截至 2026 年 9 月 26 日就是這樣互相矛盾，」→「兩份官方頁截至 2026 年 9 月 26 日的寫法就是不一致，」。來源：16143507、15609411
10. §4 秒數：「付費與 Workspace 方案的額度改用秒數計算，…買了 AI Expanded Access 加購授權能拿到更高上限，但官方沒有寫高多少。」→「Workspace 的 Business、Enterprise 方案與 Google AI Pro、Ultra，AI 短片額度改用秒數計算，…買了 AI Expanded Access 加購授權能拿到更高上限，秒數同樣列在說明頁的表格裡。」。來源：15609411
11. §5 地區：「地區限制只出現在「上傳自己的影片來改」這一項功能：」→「生成說明頁對「上傳自己的影片來改」這一項功能另有地區限制：」。來源：16143507
12. FAQ 3：「Google 的公告與說明頁都只寫在電腦上開啟 vids.new 操作，…」→「Google 部落格的公告寫的是在電腦上開啟 vids.new，說明頁的操作步驟也都從「在電腦上開啟 Google Vids」開始，…」。來源：blog；16143507
13. callout：「說明頁本身也寫明方案與額度隨時可能調整。」→「說明頁本身也寫明額度與功能都可能調整。」。來源：15609411

讀者優先的歸因精簡（事實不變，FACTCHECK-48 核准的修改）：
- 第一段原本有三個歸因語（官方部落格宣布／這次公告只提到／Google 指定的說明頁只寫），改成一個：「；手機或平板能不能用，目前沒有說明。台灣讀者最在意的地區問題：可用地區是「凡是能使用 Google Workspace 帳號的國家與地區」，沒有列出國家清單，也沒有點名台灣；」。
- §3 語言與年齡段原本有四個歸因語，改成兩個（拿掉「Google 的說明頁寫」與「同樣是官方未說明」）。
- §5 使用政策段原本有三個歸因語，改成兩個（拿掉「官方」與「頁面另外提醒」）。

研究紀錄的更正（一併改，免得第二輪把文章改回去）：
- `not_said` 與 `must_not_write`：「沒有 AI Expanded Access 高多少」→ 15609411 列 2,000 seconds/month；正文仍然不逐一抄各方案秒數。
- `verified_facts`：
  - AI Expanded Access 那條改成「這一頁沒寫多高；15609411 的表格列了數字」。
  - 「付費與 Workspace 方案以秒計」改成逐類寫明，並記下 Workspace Individual 與 Google AI Plus 是每月 6 部。
  - 「其他 AI 功能用點數計」收窄成表上的四項。
- `editorial_brief` 同步改寫。
- 已加上 `factcheck` 物件（claims_checked 91、changes 22 筆、open_questions、coordinator_rulings）。`title` 沒改。

## 讀者優先的檢查

- 內容包裡「本文」出現 0 次。description 以「（2026 年 9 月查證）」結尾，沒有查證流水帳。title、description、summary 都沒有數篇數之類的選題計數。
- 歸因語：第一段剩一個，正文每段最多兩個（改了上面三段）。FAQ 與 callout 不計。
- 仍然偏多、但屬風格而沒有動的：「Mokaair／本站沒有實測」在第二段、§1 兩段與 callout 各出現一次，共四次。這是查證紀律寫進正文，交給協調者決定要不要併成一次。

## 待協調者決定

1. Workspace Updates 印的是 “starting on September 23, 2026”，沒有時區。正文照紀錄寫「美國時間 2026 年 9 月 23 日起」，日期沒有換算，但「美國時間」這個標籤是推論。可以考慮改成「2026 年 9 月 23 日起（Google 公告的日期）」。
2. 表格「狀態」欄對三個控制與 SynthID 寫「已上線」。依據是 Google 的 “Now anyone…”／“Users now have access”；不過 Workspace 網域從 9/23 起有 1–3 天的出現期，個人帳號則沒寫節奏。正文已經交代推出節奏，所以保留。
3. 15609411 另列 Workspace Individual 與 Google AI Plus，兩者和個人帳號一樣是每月 6 部、與虛擬化身合併計算。正文照紀錄不談 Plus；Individual 現在出現在適用版本清單裡，但沒寫額度。
4. 16143507 頂端的方框仍寫 “This feature requires an eligible Google Workspace subscription.”，和部落格、Workspace Updates 矛盾。沒有採用，照紀錄維持。
5. DELTA-4-8 第 7 條：兩份說明頁是活頁面，發布當天要重讀。字數 2,968，離 3,000 的上限只剩 32 字，之後補句要先精簡別處。

## 自檢輸出（原樣）

```
OK ai-news-google-vids-omni-free-20260924 zh-TW paragraphs 2968
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
