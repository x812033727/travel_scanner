# verify-r1-20260930 — vibe-coding-first-website-2026

第一輪獨立事實查核（2026-09-30），對象是依站主大綱 B 重寫後的 `video.json`。查核者不是撰稿者；舊報告（verify-1.md、verify-p1-20260929*.md）查的是舊稿，這裡只當背景，不當證據。

方法：先把 `video.json` 全部可讀文字（標題、說明、標籤、縮圖、每個場景的 data、每句 text 與 say）抽成 283 筆清單（`<VIDEO_WORKDIR>/vibe-coding-first-website-2026/_tools/verify-r1/claims-list-before.tsv`），再逐項對官方頁。所有頁面用 `Mokaair-editorial/1.0` 識別抓取、跟隨轉址、同一主機間隔至少 1 秒、讀之前去掉 HTML 註解。這一輪沒用網頁搜尋。OpenAI 的兩頁今天都回 HTTP 200，讀得到全文。

## 官方頁（2026-09-30 抓取）

| 代號 | URL（最終網址） | HTTP | 頁面日期 |
| --- | --- | --- | --- |
| CL | https://support.claude.com/en/articles/17153992-what-are-artifacts-and-how-do-i-use-them（舊址 9487310 轉到這裡） | 200 | Updated this week |
| CF | https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude | 200 | — |
| GH1 | https://support.google.com/gemini/answer/16047321 | 200 | — |
| GC | https://gemini.google/overview/canvas/（轉到 /us/） | 200 | — |
| GS | https://gemini.google/subscriptions/（轉到 /us/） | 200 | — |
| OH | https://help.openai.com/en/articles/20001339-creating-and-using-chatgpt-sites | 200 | Updated 11 hours ago |
| OL | https://learn.chatgpt.com/docs/sites | 200 | — |
| GL | https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits | 200 | — |
| GCR | https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site | 200 | — |
| CFL | https://developers.cloudflare.com/pages/platform/limits/ | 200 | Last updated Sep 5, 2026 |
| CFD | https://developers.cloudflare.com/pages/get-started/direct-upload/ | 200 | Last updated Apr 21, 2026 |
| CFS | https://developers.cloudflare.com/pages/framework-guides/deploy-anything/ | 200 | Last updated Apr 21, 2026 |

## 逐項判定

| # | 說法 | 位置 | 來源 | HTTP | 判定 | before → after |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 三家都能用對話做網站，免費帳號不一定用得到 | hook:6jm7、hook.data | CL、GC、OH | 200 | CONFIRMED | ChatGPT Sites 免費與 Go 沒有，說法成立 |
| 2 | Claude Artifacts 免費方案也能在對話裡建立 | three-tools.rows.0、z52a | CL（Create artifacts in a chat：Free 打勾） | 200 | CONFIRMED | — |
| 3 | Gemini Canvas「官方只寫要登入、沒寫方案」 | three-tools.rows.1.2、3rhn | GH1、GC「Canvas is available for all Gemini users」、GS Free（$0）列出 Canvas | 200 | CHANGED | 「只寫要登入 Gemini，沒寫方案」→「所有 Gemini 使用者都能用」；3rhn 改成「官方寫所有 Gemini 使用者都能用」 |
| 4 | ChatGPT Sites：Plus、Pro、工作區；免費與 Go 沒有 | three-tools.rows.2、swky | OH「available in public beta for ChatGPT workspaces, Plus, and Pro accounts」；OL「Plus, Pro, Business, Enterprise and Edu」 | 200 | CONFIRMED | — |
| 5 | 官方寫明免費能用的只有 Claude；Gemini 沒寫方案 | who-is-free.left/right、sbwf、7up6 | GC、GS | 200 | CHANGED | 左欄加「Gemini：Canvas」；右欄標題「免費用不到或沒寫明」→「免費用不到」，只留 ChatGPT；sbwf →「官方寫明免費方案能用的，有 Claude 和 Gemini 兩家。」；7up6 →「ChatGPT 則寫明，免費和 Go 方案都沒有。」 |
| 6 | Claude 成品在對話旁邊的視窗打開 | entrances.steps.0、iret | CL「opens in its own window beside your conversation」 | 200 | CONFIRMED | — |
| 7 | Gemini 在文字框下方選 Canvas | entrances.steps.1、tyw4 | GH1「Below the text box … Canvas」；GC「Below the prompt bar, select Canvas」 | 200 | CONFIRMED | — |
| 8 | ChatGPT 在網頁版描述網站，提示含「網站」或 @Sites | entrances.steps.2、8jfe | OH「On web, select Work … Include the word "website" in your prompt, or mention @Sites」 | 200 | CONFIRMED（附註） | 官方寫的是英文字 website，且網頁版要先選 Work；見「懷疑但沒動」 |
| 9 | Claude 設定在 Settings > Capabilities | claude-setup.steps.0-1、7haj、uww9 | CL（Free、Pro、Max） | 200 | CONFIRMED | Team、Enterprise 在 Organization settings；片子講免費帳號，不動 |
| 10 | 要打開「雲端程式執行」與「檔案建立」兩個設定 | claude-setup.title、steps.2、wpkd、j3xg | CL「Cloud code execution and file creation」；CF「toggling Code execution and file creation on」「enabled by default」（Free、Pro、Max） | 200 | CHANGED | 是一個開關且預設開啟。title「Claude 先打開兩個設定」→「Claude 先確認一個設定」；steps.2「開兩個功能／雲端程式執行、檔案建立」→「確認開關開著／雲端程式執行與檔案建立」；wpkd →「確認雲端程式執行與檔案建立這個開關是開著的。」；j3xg →「官方寫明 Artifacts 需要它，免費方案預設就是開的。」 |
| 11 | Claude 的代價是要先開兩個設定 | tradeoffs.rows.0.2、39ct | CF | 200 | CHANGED | 「要先開兩個設定」→「確認一個設定有開」；39ct「代價是要先開設定」→「只要確認一個設定有開」 |
| 12 | Gemini 可直接改程式碼、有主控台 | tradeoffs.rows.1.1、yrac | GH1（Code 檢視、Show console） | 200 | CONFIRMED | — |
| 13 | Gemini 官方沒寫方案與下載 | tradeoffs.rows.1.2 | GH1、GC | 200 | CHANGED | 「官方沒寫方案與下載」→「官方沒寫下載網頁檔」 |
| 14 | Gemini 匯出列表沒寫下載網頁檔 | tradeoffs:6x9c | GH1（Export to Docs、Export to Slides／PDF、Copy contents、Export to Colab） | 200 | CONFIRMED | — |
| 15 | ChatGPT 描述、預覽、發布在同一處；公開測試 | tradeoffs.rows.2、i6k9 | OH「create, preview, publish, and share」「public beta」 | 200 | CONFIRMED | — |
| 16 | 「Sites is not available on Free or Go.」（常見問題） | sites-free.data、e4kn、epsd | OH FAQ 原文 | 200 | CONFIRMED | 逐字相符；頁名「Creating and using ChatGPT Sites」相符 |
| 17 | 單頁 HTML 用 index.html 當入口，兩家都認 | tech-bounds、side-by-side:3aaf、get-file:y8wd、deploy-steps.steps.0、5ymd | GCR「index.html, index.md, or README.md as the entry file」；CFS「top-level file for index.html」 | 200 | CONFIRMED | — |
| 18 | GitHub Pages：限公開儲存庫；網站上限 1 GB；每月頻寬軟性上限 100 GB | hosting.rows.0、hvjf | GL | 200 | CONFIRMED | — |
| 19 | 網址 帳號名.github.io | hosting.rows.0.2 | GCR `<user>.github.io` | 200 | CONFIRMED | 專案站是 帳號名.github.io/儲存庫名，片子沒細分 |
| 20 | Cloudflare Pages：每月 500 次建置、每站最多 2 萬個檔案；專案名.pages.dev | hosting.rows.1、bguq | CFL（Free：1 build at a time、500/月、20,000 檔、25 MiB、100 專案）；CFD `<PROJECT_NAME>.pages.dev` | 200 | CONFIRMED | — |
| 21 | 網站 1 GB 是硬上限；頻寬與建置次數是軟性 | soft-hard.data、knvi | GL | 200 | CONFIRMED | — |
| 22 | 每小時建置軟限 10 次，自訂 GitHub Actions 流程例外 | actions-exception.data、4raw | GL「soft limit of 10 builds per hour. This limit does not apply if you build and publish your site with a custom GitHub Actions workflow」 | 200 | CONFIRMED | — |
| 23 | Cloudflare 新建 Direct Upload 專案可拖放資料夾，最多 1,000 檔 | deploy-steps.steps.2、7g2d | CFD（Drag and drop：1,000 files、25 MiB；zip 或單一資料夾；既有 Git 整合專案不能在 dashboard 拖放；Wrangler 20,000） | 200 | CONFIRMED | 1,000 只限 dashboard 拖放，片子已限定範圍 |
| 24 | GitHub Pages 不能拿來免費經營線上生意或電商（引文） | not-for-business.data、ihai | GL 原文 | 200 | CONFIRMED | 逐字相符 |
| 25 | GitHub 的免費方案只能用公開儲存庫 | check-list:7f5w | GL、GCR「GitHub Pages is available in public repositories with GitHub Free」 | 200 | CHANGED | 「GitHub 的免費方案只能用公開儲存庫，你放上去的東西誰都看得到。」→「GitHub Pages 免費方案只能用公開儲存庫，放上去的東西誰都看得到。」（GitHub Free 可有私人儲存庫，只有 Pages 限公開） |
| 26 | 只有免費帳號：從 Claude 開始 | answer.items.0、k26g | CL、GC、GS | 200 | CHANGED | items.0 →「只有免費帳號：Claude 或 Gemini」；k26g →「只有免費帳號，官方寫明能用的是 Claude 和 Gemini。」 |
| 27 | 有 Gemini 帳號先試 Canvas；有 Plus、Pro、工作區也能試 Sites | answer.items.1-2、sbpk、6yd4 | GC、OH | 200 | CONFIRMED | — |
| 28 | 標題、說明、標籤 | youtube | 上列 | 200 | CONFIRMED | 沒有數字；「免費帳號用得到哪一家」在更正後仍成立 |
| 29 | 個人介紹、作品集沒問題 | not-for-business:5azv | GL | 200 | OUT OF SCOPE | 推論，官方沒逐項寫；見「懷疑但沒動」 |
| 30 | 需求五面向、爛／好需求、三組修改提示、備份、預覽≠檔案、搜電話地址金鑰、原始碼公開與快取 | five-parts、bad-good、tech-bounds、prompt-template、get-file、open-file、one-change、mobile-prompt、vague-words、backup、check-list、source-public | 站內文章 vibe-coding-first-website（方法建議） | — | OUT OF SCOPE | 方法，不宣稱實測；GCR「GitHub Pages sites are publicly available on the internet」支持原始碼公開 |
| 31 | 名稱與方案變動快、以官網為準；縮圖「First website today」 | names-change、thumbnail | — | — | OUT OF SCOPE | — |

## 總結

- 查核 31 項（涵蓋 283 筆文字位置中所有可查證者）：CONFIRMED 21、CHANGED 7（#3、#5、#10、#11、#13、#25、#26；事實層面是 3 件：Gemini Canvas 免費可用、Claude 是一個預設開啟的開關、公開儲存庫限制只限 Pages）、NOT FOUND 0、OUT OF SCOPE 3。
- 新增 `sources`：CF（Claude 檔案建立）與 GC（Google Gemini Canvas）；全部 `checked_on` 設為 2026-09-30。`claims.md` 的 c2、c3、c5 已改，並附更正段。沒有數字改動，所以縮圖、標題、說明不用動；沒有新增 lexicon 詞條。
- 會很快過期：ChatGPT Sites 在公開測試（OH 今天 11 小時前才更新，用量上限依方案且「may change during the public beta」）；Claude 2026-09-16 才分舊版／新版 artifact，新版在對話裡做的 artifact 怎麼下載或匯出，CL 沒寫（只寫模板用 Export、舊版 artifact 能看程式碼、複製、下載）；Cloudflare limits 2026-09-05 更新，Direct Upload 頁 2026-04-21 更新。
- 與 brief 衝突（官方頁勝，已套用，請站主決定大綱是否仍成立）：brief「會過期的事實」寫 Gemini Canvas「官方只寫需登入」，大綱 B 的鉤子是「只有一家，免費就能預覽又下載」。Google 官方 Canvas 頁與方案頁都寫免費可用，所以「只有一家免費」不成立；「下載」這半句三家都沒有官方依據（Gemini 只列匯出到文件、簡報、Colab 與複製；Claude 新版 artifact 沒寫下載）。
- 意見：pjat「我的看法是」、wvvw「我的做法是」有標示，與站主觀點一致（需求講清楚、一次改一件、上線前搜個資、以官網為準）。答案章在更正後，「只有免費帳號」與「已經有 Gemini 帳號」兩點有些重疊，屬結構，沒改。
- 聽稿（只報告）：沒有超過 40 字的句子；沒有查證口吻、括號或網址；念出的英文詞都在 lexicon（Actions 走 say「艾克申斯」）。reveal 順序：who-is-free 左欄現在有兩點，由 sbwf 一句同時帶出 Claude 與 Gemini，右欄由 7up6 帶出，順序正確。
- lint：`node tools/video/cli.mjs lint --slug vibe-coding-first-website-2026` → 0 errors、0 warnings（估 8.2 分鐘、94 句）。

## 懷疑但沒動的事

- 8jfe「提示裡要有網站兩個字」：官方寫的是英文字「website」或 @Sites，且網頁版要先選 Work。中文提示寫「網站」是否會觸發 Sites 沒有官方依據；建議站主用有 Plus 的帳號試一次，或改成「提到 website 或 Sites」。
- get-file「有下載鍵就下載，沒有就複製全部程式碼」：Claude 新版（2026-09-16 後）對話 artifact 的下載／複製控制，CL 沒寫；Gemini Canvas 的 Copy contents 是否複製整份 HTML 也沒寫。片中有「按鈕位置會改」保底，但要真人各試一次。
- cta「說明欄第一行就是文章連結」：目前 `youtube.description` 第一行不是連結，要靠上架包補上，沒驗證。
- not-for-business:5azv「個人介紹、作品集沒問題」是推論，GL 只寫不能主要用於商業交易或 SaaS。
- hosting 的「帳號名.github.io」只適用使用者站；專案站在子路徑。

## 需要第二輪嗎

需要。本輪 CHANGED 7 項（事實 3 件，但牽動鉤子前提與答案章），超過「三個事實更正」的門檻；第二輪請重查 #3、#5、#10、#11、#13、#25、#26，外加隨機三分之一的 CONFIRMED。
