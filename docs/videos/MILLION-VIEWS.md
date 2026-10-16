# 百萬點閱批次：六支英文為主的 AI 影片規劃

2026-09-28 規劃。目標是做一批英文市場為主、題目本身就有大量搜尋量的 AI 影片，衝高點閱。走 `youtube-video` skill 的全自動路線（投影片＋合成旁白＋四語 CC），每支都勾英文配音音軌。設計與關卡見 `DESIGN.md`、`AUTOMATION.md`、`HANDS-OFF.md`；頻道規格見 `README.md`。

## 為什麼是這六支、為什麼是英文

先講清楚一件事：單支影片衝到一百萬，靠的是**題目的搜尋量**與**留存率**，不是我們能保證的數字。這份規劃能控制的是「把票押在真的有人搜的題目上，而且每支都留得住人」。三個依據：

- **英文市場的量體大得多。** 2026 年 YouTube 上 AI 題目的高點閱幾乎都是英文：Claude Code 的長教學單支破兩百萬（Nick Saraev），Fireship 這類開發者頻道平均每支破百萬，Matt Wolfe、AI Explained、Two Minute Papers 都是英文。頻道聲音同一個 Gemini 聲音就能唸英文配音（`DUBS.md`），所以我們用同一支影片的英文音軌打英文市場，中文旁白服務台灣觀眾。
- **多語言音軌是點閱的乘數。** YouTube 官方資料：加多語言音軌的頻道，超過 25% 觀看時間來自非主要語言；Jamie Oliver 的頻道加了之後觀看數變三倍。每支都出 en、ja、ko 三條配音，等於一支影片打四個語言市場（zh-CN 在 2026-10-09 拿掉）。
- **時效題＋常青題各半。** 時效題（價格戰、Siri、Google Vids）趁新聞熱度；常青題（AI 代理、vibe coding、免費 vs 付費）靠長尾搜尋，熱度過了還有量。六支平衡押注，不把全部賭在一則新聞上。

留存率是演算法最看重的東西，所以每支都照 skill 的規矩：一支只回答一個問題、前 30 秒給出承諾、至少一段觀眾能照做的實算或流程。

## YouTube 政策的底線（會影響能不能長期營利）

YouTube 2026 年在收緊「非原創內容」政策：2 月一次就下架 11 個頻道、清掉 6 個的內容，被點名的是「AI 旁白配圖片幻燈片、沒有創作者觀點、套模板量產」。**AI 旁白本身不會被砍，低成本量產才會。** 這批影片對這條政策的答案，正是 skill 已經內建的關卡：

- 每支 `brief.md` 都有非空的「站主觀點」（第一行寫套用了頻道立場的哪幾條），這是 YouTube 要的「創作者觀點」。
- 每支都有一段實際的實算或可照做的流程（價格實算、申請流程、五輪代理帳單、上線步驟）。
- 版型順序各支不同（lint 會警告雷同），不套同一個模板。

也就是說：衝點閱和守政策是同一件事——有觀點、有實料、不量產。

## 六支影片

| # | slug（`docs/videos/<slug>/`） | 一句話 | 類型 | 站內來源文章 | 時效／常青 |
| --- | --- | --- | --- | --- | --- |
| 1 | `ai-price-war-gpt-6-sol-vs-opus-5-5` | 三個「便宜 X%」比的不是同一件事，用你的用量算帳單 | 更新彙整＋實算 | `ai-news-gpt-6-sol-luna-20260923` | 時效（9/22 新聞） |
| 2 | `siri-ai-ios-27-how-to-get-it` | 新 Siri 能做什麼、誰用得到、怎麼開、讀你什麼 | 觀點解說＋操作 | `ai-news-siri-ai-ios-27-20260914` | 時效（10 月多語言上線前） |
| 3 | `ai-agents-explained-what-they-cost` | 代理是什麼、為什麼貴 16 倍、哪個設定擋住費用 | 觀點解說＋實算 | `ai-agents-explained` | 常青 |
| 4 | `google-vids-free-ai-video-omni-1-1` | 免費做 AI 影片的四個界線與一個會讓片段消失的坑 | 操作教學 | `ai-news-google-vids-omni-free-20260924` | 時效（9/23 新聞） |
| 5 | `vibe-coding-first-website-2026` | 不會寫程式，用對話做出第一個網站並免費上線 | 操作教學 | `vibe-coding-first-website` | 常青 |
| 6 | `free-vs-paid-ai-plans-2026` | 20 美元值不值得，用你撞到的額度決定 | 觀點解說＋實算 | `ai-free-vs-paid-plans-2026` | 常青 |

每支的完整企劃在各自資料夾的 `brief.md`：觀眾、觀眾看完能做到的事、站主觀點、示範或實算、三個大綱選項、會過期的事實、素材、不做的事，最後一節是英文市場的標題三案、縮圖、標籤與配音設定。

## 每支的英文標題與角度（衝點閱的鉤子）

- **1 價格戰**：OpenAI and Anthropic cut prices on the same day. Here's what your AI bill actually looks like now。鉤子是「兩個數字比的不是同一件事，對你的帳單可能一毛都沒差」。
- **2 Siri**：Siri finally runs on Gemini. Who gets it, how to turn it on, and what it reads。鉤子是「你的 iPhone 可能還排在等候名單裡」。
- **3 代理**：What an AI agent actually is, what one costs to run, and the setting that stops it burning your money。鉤子是「同一件事，做成代理可能貴 16 倍」。
- **4 Google Vids**：Google makes AI video free. Here are the 4 limits before you start。鉤子是「一個坑會讓你辛苦生成的片段直接消失」。
- **5 vibe coding**：Build your first website with AI in 2026, no coding, publish it free。鉤子是「祕訣不是哪個工具最強，是你怎麼把需求講清楚」。
- **6 免費 vs 付費**：Is $20 a month for AI worth it? Find your usage, and I'll do the math。鉤子是「先別看哪家最強，先看你每天卡在哪」。

## 流程與關卡（照 skill 全自動路線）

每支的 12 步在 `AUTOMATION.md`；重點：

1. 企劃已寫好（這批的 `brief.md`）。站主在 `/admin/videos` 設定分頁存好「頻道立場」後，Jev 依立場挑大綱；立場空白時大綱等站主選。各 brief 的站主觀點第一行寫的「套用立場：N、M」用的是 `HANDS-OFF.md` 草稿的條號，站主存的立場若條號不同，只改那一行。
2. 撰稿 → 換人查核 → 聽眾審稿 → tts → 旁白檢查 → render → assemble → 四語 CC → `qa` 11 項 → 成片核准 → package → 上架確認。
3. **配音**：成片完成後，站主在每支的影片頁勾 en（ja、ko 建議一併勾），工人才做那幾條音軌（`DUBS.md`）。英文音軌是這批打英文市場的關鍵，別漏勾。
4. **縮圖**：各 brief 的縮圖文字以英文為主。等本地化縮圖的票（`2026-09-28-video-localized-thumbnails`）做好，才能一支影片對不同語言掛不同縮圖；在那之前先出英文縮圖。
5. 上架永遠是站主的動作。

## 排程建議

- 先做時效題：1（價格戰）、4（Google Vids）、2（Siri，趕在 10 月多語言上線前）。
- 常青題 3、5、6 接著做，做好放著，搜尋長尾會持續帶量。
- 一週 1 到 2 支，站主看完才上架（`DESIGN.md` 的營利對策）。

## 誠實的話

沒有人能保證單支破百萬，這是搜尋量、時機與留存共同決定的。這份規劃做的是把資源押在「英文市場＋高搜尋題目＋多語言音軌＋有觀點有實料」這組已知會拉高點閱的條件上，並用 skill 內建的關卡守住 YouTube 的原創內容政策，讓做出來的影片有資格長期累積觀看，而不是上架就被限流。六支一起上、各打不同市場與搜尋詞，是把中百萬的機率拉到最高的做法。
