# claims — vibe-coding-first-website-2026

一行一個可查證的說法：`id｜說法｜官方來源｜查核日｜出現的場景`。方案名稱與限制以官網當天為準。2026-09-30 依站主選定的大綱 B 重寫；每個網址都在 2026-09-30 重新開過（HTTP 200，最終網址如下）。

c1｜描述需求（目的、內容、風格、不要什麼、技術邊界）→ 產出單一 HTML → 瀏覽器打開 → 一次改一件 → 備份 → 上線；把同一段需求各貼一次來比較；三組修改提示（配色、加內容、手機版）：都是方法建議，取自站內文章，不宣稱實測效果｜站內文章 vibe-coding-first-website｜2026-09-30｜five-parts, bad-good, tech-bounds, prompt-template, open-file, one-change, mobile-prompt, vague-words, backup, side-by-side
c2｜Claude Artifacts：「Artifacts are available on Free, Pro, Max, Team, and Enterprise plans」，「Create artifacts in a chat」五種方案都有；Claude 能把單頁網站（single-page websites）做成 artifact，成品在對話旁邊開啟；「Artifacts require Cloud code execution and file creation to be turned on in Settings > Capabilities」，這是一個開關（Code execution and file creation），Free、Pro、Max「enabled by default」（https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude）；舊版 artifact（2026-09-16 前在對話裡做的）可以檢視程式碼、複製或下載，新版依模板匯出，介面以官網為準｜https://support.claude.com/en/articles/17153992-what-are-artifacts-and-how-do-i-use-them（舊網址 9487310 轉到這裡）｜2026-09-30｜three-tools, account-first, who-is-free, entrances, claude-setup, tradeoffs, get-file, answer
c3｜Gemini Canvas：「you must be signed in to Gemini Apps」；說明頁沒寫方案，但 Google 官方 Canvas 頁寫「Canvas is available for all Gemini users」，方案頁的 Free（$0）也列出 Canvas（https://gemini.google/overview/canvas/、https://gemini.google/subscriptions/）；文字框下方選 Canvas；Code 檢視可直接改程式、Show console 看預覽的錯誤與紀錄；分享用 g.co/gemini/share 連結；匯出項目列的是 Google 文件、簡報、Colab 與複製內容，頁面沒有寫下載網頁檔｜https://support.google.com/gemini/answer/16047321｜2026-09-30｜three-tools, who-is-free, entrances, tradeoffs, answer
c4｜ChatGPT Sites：公開測試，開放 ChatGPT 工作區、Plus、Pro 帳號；「Sites is not available on Free or Go.」；在網頁版 Work 描述網站，提示裡含 website 一字或 @Sites；可建立、預覽、發布、分享｜https://help.openai.com/en/articles/20001339-creating-and-using-chatgpt-sites 及 https://learn.chatgpt.com/docs/sites（「Sites is in public beta and is available with ChatGPT Plus, Pro, Business, Enterprise and Edu plans」）｜2026-09-30｜three-tools, account-first, who-is-free, entrances, tradeoffs, sites-free, answer
c5｜GitHub Pages：免費方案限公開儲存庫（GitHub Free 的 Pages 只能用在公開儲存庫；GitHub Free 本身可以有私人儲存庫）；已發布網站不得超過 1 GB（來源儲存庫建議 1 GB）；部署逾 10 分鐘逾時；每月頻寬軟性上限 100 GB；每小時建置軟性上限 10 次，「This limit does not apply if you build and publish your site with a custom GitHub Actions workflow」（例外只限自訂 GitHub Actions 建置及發布流程）；網址：使用者站是 帳號名.github.io，專案站是 帳號名.github.io/儲存庫名，所以投影片寫「帳號名.github.io 開頭」｜https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits 及 https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages｜2026-09-30｜hosting, soft-hard, actions-exception, check-list
c6｜Cloudflare Pages 免費方案：同時 1 個建置、每月 500 次、每站最多 20,000 個檔案、單檔最多 25 MiB、每帳號 100 個專案；Direct Upload 專案在 dashboard「Create application > Get started > Drag and drop your files」，拖放一次 1,000 檔；既有 Git 整合專案不能在 dashboard 拖放；網址是專案名.pages.dev（1,000 檔只限 dashboard 拖放，不能泛指 Wrangler 或 GitHub）｜https://developers.cloudflare.com/pages/platform/limits/（更新 2026-09-05）及 https://developers.cloudflare.com/pages/get-started/direct-upload/｜2026-09-30｜hosting, deploy-steps
c7｜「GitHub Pages is not intended for or allowed to be used as a free web-hosting service to run your online business, e-commerce site, or any other website that is primarily directed at either facilitating commercial transactions or providing commercial software as a service」；「You can use GitHub Pages to host a website about yourself, your organization, or your project」（支持「個人介紹、作品集沒問題」）｜https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits 及 https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages｜2026-09-30｜not-for-business
c8｜網頁原始碼所有人都看得到，刪掉後也可能留在別人的快取；已貼出去的金鑰要當作外洩重發；上線前搜電話、地址、身分證號與像金鑰的字串：方法建議，取自站內文章，不宣稱實測｜站內文章 vibe-coding-first-website｜2026-09-30｜check-list, source-public
c10｜單頁 HTML 的入口檔名 index.html：GitHub Pages 找 index.html、index.md 或 README.md 當入口；Cloudflare 的 404 說明寫網站要有頂層 index.html（本片只說這份單頁 HTML 用 index.html，沒有說所有網站都只能用它）｜https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site 及 https://developers.cloudflare.com/pages/framework-guides/deploy-anything/｜2026-09-30｜tech-bounds, get-file, side-by-side, deploy-steps

## 與企劃不同的地方

- 站主 2026-09-28 選了大綱 B。片子照 B 的六章走：三家比較、同一個需求怎麼寫、三家入口、改與看檔案、免費上線、答案。開場鉤子的原句是「只有一家，免費就能預覽又下載」；官方頁面只支持前半：只有 Claude 的頁面寫明免費方案可以建立 artifact，ChatGPT 頁面寫明免費與 Go 沒有，Gemini 頁面沒寫方案。「下載」也不能整個併進「只有一家」：Claude 新版 artifact 的下載／匯出方式官網頁沒有逐項寫。所以鉤子改成「免費帳號不一定用得到」，第一章用「你以為比模型，其實先比帳號」轉，答案章按官方寫得出來的資格分三種人。
- B 沒有「上線前的四個坑」章，原稿的圖片版權（CC 授權）、AI 亂補內容、廣告追蹤三個坑和對應的 `compare` 場景整段拿掉，只留站主觀點要的「上線前搜個資、金鑰」（原始碼公開）。CC 授權兩個來源因此不再列入 `sources`。這些事實留在站內文章，片內不講。
- B 的第 3 章原本是「用同一個需求在三家各做一次」；站主沒有在三家都做過，所以片中只用 `steps` 描述這個做法（各開新對話、各存資料夾、並排打開），不說「我試過」。
- ChatGPT：交辦說明寫「說明頁在這個環境回 403，只講到『以官網為準』層級」。2026-09-30 實測 help.openai.com 與 learn.chatgpt.com 都回 HTTP 200 且讀得到全文，B 的主軸又是三家方案差別，所以片中寫了官方頁面現在寫的資格（公開測試；工作區、Plus、Pro；免費與 Go 沒有），仍不寫任何價格、用量數字或地區細節。若 OpenAI 頁面之後又讀不到，這幾句要退回「以官網為準」。
- 移除了原稿沒有依據的說法：「搬到哪裡都不會壞」「幾乎完全由描述決定」「省掉一半麻煩」「唯一原則」「白紙黑字」「這條很多人不知道」「範本會跟著官方改版更新」「很多人跳過這一步」。
- 拿掉「今年」「下個月」這類會過期的字，價位與限制表的標題帶月份（2026 年 9 月）。
- `sources` 的 Claude 網址改成轉址後的最終網址（17153992），並新增 OpenAI 說明中心與 Cloudflare 靜態 HTML 兩頁。

## 我懷疑但沒動的事

- 大綱 B 的鉤子「只有一家，免費就能預覽又下載」：Gemini Canvas 的實際免費額度、能否把成品存成單一 HTML 檔，官方頁都沒寫（頁面只列匯出到文件、簡報、Colab 與複製內容）；Claude 新版 artifact 的「下載」在說明頁只出現在舊版 artifact 與模板匯出。這些要在瀏覽器用真實帳號各試一次才知道，我沒有動鉤子的意思，只是改成官方頁面支撐得起的說法。請站主決定要不要真的三家各做一次再回頭改片。
- 「有下載鍵就下載，沒有就複製全部程式碼」是方法，不是官方保證每一家都有複製鍵；片中另有一句「各家按鈕的位置會改」保底。
- Cloudflare 的 1,000 檔限制與拖放介面文字（Create application > Get started > Drag and drop your files）依 2026-09-30 的 Direct Upload 頁（更新日以頁面為準），上架前再開一次確認介面文字沒變。
- Claude 說明頁 2026-09-30 寫舊版 artifact 是 2026-09-16 前做的，「不能再做新的」，新版與舊版的匯出方式不同；片中只講「設定要開」「成品在旁邊開」，沒有把舊版的下載鍵當成新版的保證。
- 「Claude 的好處是免費方案就能建立」不等於免費額度夠用；對話額度依 Claude 方案，片中沒有談。

## 進度

全部 31 個場景完成，`lint` 0 errors、0 warnings（估計 8.2 分鐘、94 句）。尚待：真人聽稿、獨立事實查核（本次事實變動很多：鉤子、Claude 頁改版、ChatGPT 頁可讀、B 的整體結構），配音與成片。

## 第一輪獨立查核（2026-09-30）更正

詳見 verify-r1-20260930.md。

- Gemini Canvas 免費可用：Google 官方 Canvas 頁寫「Canvas is available for all Gemini users」，方案頁 Free 欄列出 Canvas。原稿「Gemini 官方沒寫方案」「官方寫明免費能用的只有 Claude」改成 Claude 和 Gemini 兩家；three-tools、who-is-free、tradeoffs、answer 跟著改。上面「與企劃不同的地方」第一段與「我懷疑但沒動的事」第一點說 Gemini 頁面沒寫方案，只對說明頁成立。
- Claude 的設定是一個開關「Code execution and file creation」，Free、Pro、Max 預設開啟；原稿「開兩個設定」「要先開設定」改成「確認一個設定有開」。
- check-list 的「GitHub 的免費方案只能用公開儲存庫」改成「GitHub Pages 免費方案」：GitHub Free 可以有私人儲存庫，只有 Pages 限公開。

## 第二輪獨立查核（2026-09-30）更正

詳見 verify-r2-20260930.md。第一輪的七項更正今天重開官方頁都成立。

- entrances 的 ChatGPT 入口：官方寫網頁版先選 Work，提示裡要有英文字「website」或提到 @Sites，沒有寫中文「網站」會觸發。8jfe 與 entrances.steps.2 改成「先選 Work，提示寫 website 或 @Sites」；lexicon 新增 Work、website（null，待真人試聽）。
- check-list 7f5w：Pages 沒有自己的「免費方案」，官方寫的是 GitHub Free 帳號的 Pages 只能用在公開儲存庫；改成「用 GitHub 免費方案，Pages 只能開在公開儲存庫」。
- hosting 網址欄：「帳號名.github.io」只適用使用者站，專案站在 /儲存庫名 底下；改成「帳號名.github.io 開頭」。
- not-for-business 5azv「個人介紹、作品集沒問題」：What is GitHub Pages? 頁寫可以放關於你自己的網站，新增此來源，不再是推論。
