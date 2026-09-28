# 不會寫程式，也能在 2026 年做出第一個網站：用對話 vibe coding，免費上線

<!-- 百萬點閱批次第 5 支（docs/videos/MILLION-VIEWS.md）。企劃日 2026-09-28；「套用立場」條號依 docs/videos/HANDS-OFF.md §頻道立場的草稿編號。 -->

## 觀眾

完全不會寫程式、但想要一頁自己的網站的人。搜尋「vibe coding」「how to build a website with AI」「build a website without coding 2026」「free website AI」。英文市場為主。這是常青教學題，也是 2026 年 YouTube 上「vibe coding」持續有大量搜尋的題目。

## 觀眾看完能做到的事

1. 把需求寫成一段話（目的、內容、風格、不要什麼，加一段技術邊界），用 Claude、ChatGPT 或 Gemini 產出一個單一 index.html，下載後在瀏覽器打開來看。
2. 用「一次只改一件事」的方式改配色、加內容、修手機版，最後用 GitHub Pages 或 Cloudflare Pages 的免費方案上線，並在上線前檢查沒有把電話、地址或金鑰寫進原始碼。

## 站主觀點

套用立場：4、5、3
不會寫程式不是門檻，把需求講清楚才是。我的做法是三件事：需求寫滿四個面向再加技術邊界（只要一個檔、檔名 index.html、樣式同檔、不連外部資源），一次只改一件事、每改一次就下載重看，上線前用純文字編輯器搜自己的電話、地址與像金鑰的字串。安全靠這個檢查動作，不靠「應該不會有人看原始碼」的僥倖：GitHub Pages 的網站本來就是公開的。方案名稱與限制 2026 年變動很快，影片一律講「以官網當天為準」，不把今天的數字講死。

## 示範或實算

第 4 章的 `steps` 是可以照做的三組修改提示（來自站內文章的示範）：只換配色、加一段內容、改手機版排版，每組都是「指到具體位置、給具體結果」，不用「好看一點」這種沒標準的說法。第 5 章的 `table` 是兩個免費上線服務 2026-09-28 的官方限制，讓觀眾照著選：

| 服務 | 免費方案關鍵限制 | 網址形式 |
| --- | --- | --- |
| GitHub Pages | 免費方案只能公開儲存庫；儲存庫與網站各建議／上限 1 GB；每月頻寬軟性上限 100 GB；部署逾 10 分鐘逾時 | 帳號名.github.io |
| Cloudflare Pages | 每月 500 次建置、同時 1 個；每站最多 20,000 個檔案、單檔最多 25 MiB；每帳號最多 100 個專案；拖放一次最多 1,000 檔 | 專案名.pages.dev |

第 3 章的 `chat` 用一個爛需求（「幫我做個網站」）對照一個好需求（目的、內容、風格、不要什麼、技術邊界都寫齊），示範描述品質怎麼決定產出品質。

## 大綱

### 選項 A：需求、產出、上線，走完一整圈（推薦）
一行說明：從「怎麼描述需求」到「怎麼上線」走完一次完整流程，中間穿插三家工具的差別；和 B 的差別是不逐一比較工具、以流程為主，和 C 的差別是不聚焦在安全。
開場鉤子：「不用學 HTML，也能今天就有一頁自己的網站。祕訣不是哪個工具最強，是你怎麼把需求講清楚——講不清楚，換再貴的工具都做不好。」
章節（估計秒數，合計約 570 秒）：
1. vibe coding 是什麼（60 秒）
   - title: 「不會寫程式，也能做出第一個網站」，副標「用對話，一次改一件事」
   - bullets: 描述需求 → 產出 → 看檔案 → 修改 → 上線
2. 把需求寫成一段話（120 秒）
   - steps: 目的 → 內容 → 風格 → 不要什麼 → 技術邊界
   - chat: 爛需求 vs 好需求
   - big: 「index.html」，sub「只要一個檔、樣式同檔、不連外部資源」
3. 選一個能直接預覽的工具（110 秒）
   - compare: 左「Claude Artifacts（免費可預覽下載，20 MB 持續儲存限付費）」「Gemini Canvas（需登入，方案以官網為準）」，右「ChatGPT Sites（Plus、Pro、工作區，Free 與 Go 沒有）」
   - bullets: 三家名稱與方案 2026 年變動快，以官網當天為準
4. 一次只改一件事（130 秒）
   - steps: 只換配色 → 加一段內容 → 改手機版排版
   - bullets: 每改一次就下載、重開來看；預覽面板不等於檔案本身
   - cta: 說明欄第一行的站內文章
5. 免費上線＋上線前檢查（100 秒）
   - table: GitHub Pages 與 Cloudflare Pages 的免費限制
   - steps: 首頁檔名 index.html → 上傳或拖放 → 拿到網址
   - big: 「搜自己的電話、地址、金鑰」，sub「原始碼所有人都看得到」
6. 做完第一頁之後（50 秒）
   - outro: 「換任何題目都適用」；下一步：站內文章
實算（修改提示與上線限制表）放第 4、5 章，好壞需求對照放第 3 章。結尾的下一步：站內文章〈Vibe coding：不會寫程式也能做出第一個網站〉。

### 選項 B：Claude、ChatGPT、Gemini 哪個最適合做你的第一個網站
一行說明：以三家工具的差別為主線（誰免費能預覽下載、誰要付費、誰要開設定），用同一個需求在三家各做一次；和 A 的差別是比較先於流程。
開場鉤子：「Claude、ChatGPT、Gemini 都能用對話做網站。但只有一家，免費就能預覽又下載。」
章節（估計秒數，合計約 560 秒）：
1. 三家都能做網站，差在哪（70 秒）：title；table 三家 × 免費預覽、下載、需開設定
2. 同一個需求怎麼寫（100 秒）：steps 四面向加技術邊界；chat
3. 在三家各做一次（150 秒）：steps 各家的入口（Artifacts、Sites、Canvas）；bullets 各家的取捨
4. 改與看檔案（110 秒）：steps 一次改一件事；big 下載重看
5. 免費上線（80 秒）：table 兩個服務
6. 答案（50 秒）：outro
比較放第 1、3 章。結尾的下一步：站內文章同上。

### 選項 C：AI 幫你做的網站，上線前一定要檢查的四件事
一行說明：以「最常踩的坑」為主線：圖片版權、個資與金鑰、AI 幻覺內容、廣告與追蹤法規；把做網站流程當背景，重點在上線前檢查；和 A、B 的差別是安全與合規優先。
開場鉤子：「AI 幫你做網站很快。但這四個坑，每一個都可能讓你上線後才後悔——尤其是第二個。」
章節（估計秒數，合計約 555 秒）：
1. 先快速做出一頁（80 秒）：title；steps 最短流程
2. 坑一：圖片版權（100 秒）：bullets CC 六種授權、NC 與 ND 的差別；big 自己拍最安全
3. 坑二：個資與金鑰（120 秒）：big 搜自己的電話地址金鑰；bullets 公開儲存庫、外洩就當作廢重發
4. 坑三：AI 幻覺內容（100 秒）：bullets 沒得過的獎、不存在的連結；chat 自己讀過再上線
5. 坑四：廣告與追蹤（95 秒）：bullets 蒐集訪客資訊要遵守隱私法規；table 免費方案軟性上限
6. 答案（60 秒）：outro
檢查清單貫穿全片，實作示範放第 1 章。結尾的下一步：站內文章同上。

## 會過期的事實

| 事實 | 撰稿日重查的官方頁 |
| --- | --- |
| Claude Artifacts 支援單頁 HTML、Free 到 Enterprise 都可預覽下載、要先開程式執行與檔案建立、20 MB 持續儲存限付費 | https://support.claude.com/en/articles/9487310-what-are-artifacts-and-how-do-i-use-them |
| ChatGPT Sites 2026-07-09 公開測試、Plus／Pro／工作區、Free 與 Go 沒有；canvas 2026-05-28 起改為寫作區塊與程式區塊 | https://help.openai.com/en/articles/20001339-creating-and-managing-chatgpt-sites |
| Gemini Canvas 做文件、簡報、程式、網頁並即時預覽；官方只寫需登入 Gemini 應用程式 | https://support.google.com/gemini/answer/16047321 |
| GitHub Pages：免費限公開儲存庫、儲存庫與網站各 1 GB、頻寬軟性上限 100 GB、部署逾 10 分鐘逾時 | https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits |
| Cloudflare Pages 免費：每月 500 次建置、同時 1 個、每站 20,000 檔、單檔 25 MiB、每帳號 100 專案、拖放一次 1,000 檔 | https://developers.cloudflare.com/pages/platform/limits/ |
| Creative Commons 六種授權（BY、BY-SA 可商用，NC 限非商業，ND 不可改作，全都要標示） | https://creativecommons.org/share-your-work/cclicenses/ |

## 素材

- 站內文章（`source_guide`）：`vibe-coding-first-website`；引用：`claude-artifacts-guide`、`ai-image-copyright-taiwan`。
- 官方頁：上表網址。
- 圖片：不用；用 `steps`、`chat`、`compare`、`table`、`big`。

## 不做的事

- 不現場錄螢幕操作（全自動路線目前不做螢幕錄影；用投影片描述流程）。
- 不推薦特定付費方案，方案與限制一律「以官網當天為準」。
- 不教 HTML 語法；教的是描述、產出、檢查、修改、上線。
- 不給任何金鑰或帳密相關的實際字串。

## 英文市場的包裝

- 英文標題（三案）：
  1. Build your first website with AI in 2026, no coding, and publish it free
  2. Vibe coding for total beginners: from one paragraph to a live website
  3. The 4 things to check before you publish an AI-built website (number 2 matters most)
- 縮圖：tag「VIBE CODING」、headline「No code.\n**First website today**」、sub「free · step by step」。
- 英文標籤：vibe coding, build a website with AI, no code website, AI website builder, GitHub Pages, Cloudflare Pages, Claude Artifacts, ChatGPT Sites。
- 配音：勾 en（ja、ko、zh-CN 可一併）。
- 上架時機：常青題，隨時可上；標題用「first website」「no coding」的長青搜尋詞。
