# verify-r2-20260930 — vibe-coding-first-website-2026

第二輪獨立事實查核（2026-09-30），查核者不是撰稿者，也不是第一輪。範圍：第一輪改過的 7 項（#3、#5、#10、#11、#13、#25、#26）全部重查；第一輪 CONFIRMED 的 21 項用固定種子 20260930 抽三分之一，抽到 #4、#8、#14、#15、#17、#18、#22；外加第一輪留下的四個疑點。編號沿用 verify-r1-20260930.md。

方法：重抽 `video.json` 全文（`<VIDEO_WORKDIR>/vibe-coding-first-website-2026/_tools/verify-r2/claims-list-before.txt`，改完後的是 `claims-list-after.txt`），官方頁用 `Mokaair-editorial/1.0` 識別抓取、跟隨轉址、同主機間隔 1 秒以上、去掉 HTML 註解再讀。沒用網頁搜尋。OpenAI 兩頁今天都回 200。

## 官方頁（2026-09-30 抓取）

| 代號 | URL（最終網址） | HTTP | 頁面日期 |
| --- | --- | --- | --- |
| CL | https://support.claude.com/en/articles/17153992-what-are-artifacts-and-how-do-i-use-them | 200 | Updated this week |
| CF | https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude | 200 | — |
| GH1 | https://support.google.com/gemini/answer/16047321 | 200 | — |
| GC | https://gemini.google/overview/canvas/（今天回台灣版中文頁） | 200 | — |
| GS | https://gemini.google/subscriptions/（台灣版，NT$） | 200 | — |
| OH | https://help.openai.com/en/articles/20001339-creating-and-using-chatgpt-sites | 200 | Updated 11 hours ago |
| OL | https://learn.chatgpt.com/docs/sites | 200 | — |
| GL | https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits | 200 | — |
| GCR | https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site | 200 | — |
| GAB | https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages（轉到 what-is-github-pages） | 200 | — |
| CFL | https://developers.cloudflare.com/pages/platform/limits/ | 200 | Last updated Sep 5, 2026 |
| CFD | https://developers.cloudflare.com/pages/get-started/direct-upload/ | 200 | Last updated Apr 21, 2026 |
| CFS | https://developers.cloudflare.com/pages/framework-guides/deploy-anything/ | 200 | Last updated Apr 21, 2026 |

## 逐項判定

| # | 說法 | 位置 | 來源 | HTTP | 判定 | before → after |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | Gemini Canvas「所有 Gemini 使用者都能用」 | three-tools.rows.1.2、3rhn | GC 常見問題「所有 Gemini 使用者都能使用 Canvas」；GS 免費（每月 NT$0）列出 Canvas；GH1 只要求登入 | 200 | CONFIRMED | 第一輪更正成立 |
| 5 | 寫明免費可用：Claude、Gemini；免費用不到：ChatGPT | who-is-free、sbwf、7up6 | CL、GC、GS、OH | 200 | CONFIRMED | — |
| 10 | Claude 只要確認一個設定「雲端程式執行與檔案建立」，免費方案預設開 | claude-setup、wpkd、j3xg | CL「Artifacts require Cloud code execution and file creation to be turned on in Settings > Capabilities (Free, Pro, Max)」；CF「Free, Pro, and Max plans: Code execution and file creation is enabled by default」 | 200 | CONFIRMED | — |
| 11 | Claude 的代價是確認一個設定有開 | tradeoffs.rows.0.2、39ct | CF | 200 | CONFIRMED | — |
| 13 | Gemini 官方沒寫下載網頁檔 | tradeoffs.rows.1.2 | GH1 匯出只列 Export to Docs、Export to Slides（可存 PDF）、Copy contents、Export to Colab | 200 | CONFIRMED | — |
| 25 | GitHub Pages 免費只能用公開儲存庫 | check-list:7f5w | GL、GCR「available in public repositories with GitHub Free … If the account … uses GitHub Free … the repository must be public」 | 200 | CHANGED（措辭） | Pages 沒有自己的免費方案，限制綁在 GitHub Free 帳號。「GitHub Pages 免費方案只能用公開儲存庫，…」→「用 GitHub 免費方案，Pages 只能開在公開儲存庫，放上去的東西誰都看得到。」 |
| 26 | 只有免費帳號：Claude 或 Gemini | answer.items.0、k26g | CL、GC、GS | 200 | CONFIRMED | — |
| 4 | ChatGPT Sites：Plus、Pro、工作區；免費與 Go 沒有 | three-tools.rows.2、swky | OH「available in public beta for ChatGPT workspaces, Plus, and Pro accounts」；OH FAQ「Sites is not available on Free or Go.」；OL | 200 | CONFIRMED | — |
| 8 | ChatGPT 網頁版的觸發方式 | entrances.steps.2、8jfe | OH「On web, select Work … Include the word "website" in your prompt, or mention @Sites」；OL 同 | 200 | CHANGED | 8jfe「ChatGPT 在網頁版描述網站，提示裡要有網站兩個字，或提到 Sites。」→「ChatGPT 網頁版先選 Work，提示裡寫 website，或提到 Sites。」；steps.2.detail「提示寫「網站」或 @Sites」→「先選 Work，提示寫 website 或 @Sites」；lexicon 新增 Work、website |
| 14 | Gemini 匯出列表沒寫下載網頁檔 | tradeoffs:6x9c | GH1 | 200 | CONFIRMED | — |
| 15 | ChatGPT 描述、預覽、發布在同一處；公開測試 | tradeoffs.rows.2、i6k9 | OH「create, preview, publish, and share」「public beta」 | 200 | CONFIRMED | — |
| 17 | index.html 當入口，兩家都認 | tech-bounds、3aaf、y8wd、deploy-steps、5ymd | GCR「index.html, index.md, or README.md as the entry file」；CFS「top-level file for index.html」 | 200 | CONFIRMED | — |
| 18 | GitHub Pages：公開儲存庫；網站 1 GB；頻寬軟性 100 GB/月 | hosting.rows.0.1、hvjf | GL | 200 | CONFIRMED | — |
| 22 | 每小時建置軟限 10 次，自訂 GitHub Actions 例外 | actions-exception、4raw | GL | 200 | CONFIRMED | — |
| 19 | 網址 帳號名.github.io（第一輪疑點） | hosting.rows.0.2 | GAB 表格：使用者站 `<owner>.github.io`，專案站 `<owner>.github.io/<repositoryname>` | 200 | CHANGED | 「帳號名.github.io」→「帳號名.github.io 開頭」（新手多半建專案站） |
| 29 | 個人介紹、作品集沒問題，賣東西另找服務（第一輪疑點） | not-for-business:5azv | GAB「You can use GitHub Pages to host a website about yourself, your organization, or your project」；GL 不得用於線上生意、電商 | 200 | CONFIRMED | 不再是推論；GAB 加入 `sources` 與 claims.md c7 |
| 30a | 「有下載鍵就下載，沒有就複製全部程式碼」（第一輪疑點） | get-file:x9y8、fi98 | CL 只寫模板 artifact 用 Export、舊版 artifact 可檢視程式碼、複製、下載；對話裡做的新版 artifact 沒寫。GH1 的 Copy contents 寫「copy the text」，另有 Code 檢視可看與改程式碼 | 200 | NOT SETTLED | 官方頁無法定論，沒動；片中「找不到就用複製的」保底 |

## 總結

- 查核 16 項（第一輪改過的 7 項、抽樣 7 項、疑點 3 項另計 #19、#29、#30a；#8 同時是抽樣與疑點）：CONFIRMED 11、CHANGED 3（#8、#19、#25）、NOT FOUND 0、未定論 1（#30a）。第一輪七項更正今天全部成立。
- 事實更正 3 件：ChatGPT 入口是先選 Work、提示寫英文 website（不是中文「網站」）；GitHub 公開儲存庫限制綁 GitHub Free 帳號（措辭）；github.io 網址只對使用者站成立。沒有數字改動，縮圖、標題、說明、標籤不用動。
- `sources` 新增 GitHub Docs「What is GitHub Pages?」，全部 `checked_on` 2026-09-30；claims.md c5、c7 補來源，文末加第二輪更正段。lexicon 新增 `Work`、`website`（null，請真人試聽發音）。
- 會很快過期：ChatGPT Sites 公開測試，OH 今天 11 小時前更新、限制「may change during the public beta」；Claude CL 本週更新，2026-09-16 起分新舊版 artifact；Cloudflare limits 2026-09-05 更新。
- 意見：pjat「我的看法是」、wvvw「我的做法是」有標示，與 brief §站主觀點一致；沒有不符。
- 聽稿（只報告）：8jfe 新句含四個英文詞（ChatGPT、Work、website、Sites），聽感偏擠，lint 沒有超長警告；沒有查證口吻、括號或網址；reveal 順序沒變。
- lint：`node tools/video/cli.mjs lint --slug vibe-coding-first-website-2026` → 0 errors、0 warnings（估 8.2 分鐘、94 句）。

## 懷疑但沒動的事

- get-file「有下載鍵就下載，沒有就複製全部程式碼」：Claude 新版對話 artifact 的下載／複製控制與 Gemini Canvas Copy contents 能否拿到整份 HTML，官方頁都沒寫，要真人各試一次。
- cta「說明欄第一行就是文章連結」：`youtube.description` 第一行目前不是連結，要靠上架包補。
- 「Work」在繁中介面可能是在地化名稱，官方英文頁寫 Work；站主若看到中文介面名稱，可換成介面上的字。
- brief「會過期的事實」仍寫 Gemini Canvas「官方只寫需登入」，與官方頁不符（第一輪已報告，brief 由站主改）。

## 需要第三輪嗎

不需要。本輪事實更正 3 件，沒有超過三件的門檻；三件都沒有動到數字或鉤子。
