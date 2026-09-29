# claims — vibe-coding-first-website-2026

一行一個可查證的說法：`id｜說法｜官方來源｜查核日｜出現的場景`。方案名稱與限制以官網當天為準。

c1｜描述需求 → 產出單一 HTML → 瀏覽器打開 → 一次改一件 → 上線：做法取自站內文章，屬方法建議｜站內文章 vibe-coding-first-website｜2026-09-29｜what-is
c2｜「Artifacts are available on Free, Pro, Max, Team, and Enterprise plans」；「Artifacts require Cloud code execution and file creation to be turned on in Settings > Capabilities」；可複製或下載｜https://support.claude.com/en/articles/9487310-what-are-artifacts-and-how-do-i-use-them｜2026-09-29｜tools, open-file
c3｜Canvas 要登入 Gemini Apps；Code 檢視可直接改、旁邊是預覽、可開主控台看錯誤；可分享與匯出｜https://support.google.com/gemini/answer/16047321｜2026-09-29｜tools
c4｜ChatGPT 也有做網站的功能，方案與地區以官網為準（未給任何數字）｜https://learn.chatgpt.com/docs/sites（今日 HTTP 200；官方確認 Sites 建站與代管）｜2026-09-29｜tools
c5｜GitHub Pages：來源儲存庫建議 1 GB、網站不超過 1 GB、部署逾 10 分鐘逾時、每月頻寬軟性上限 100 GB、每小時建置軟性上限 10 次；自訂 GitHub Actions 建置及發布流程不受這個每小時限制｜https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits｜2026-09-29｜hosting
c6｜Cloudflare Pages 免費方案：同時 1 個建置、每月 500 次、每站最多 20,000 個檔案、單檔最多 25 MiB、每帳號 100 個專案；Direct Upload 的 dashboard 拖放每次最多 1,000 檔（不能泛指 GitHub 或 Wrangler 上傳）｜https://developers.cloudflare.com/pages/platform/limits/ 及 https://developers.cloudflare.com/pages/get-started/direct-upload/｜2026-09-29｜hosting, deploy-steps
c7｜「GitHub Pages is not intended for or allowed to be used as a free web-hosting service to run your online business」｜https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits｜2026-09-29｜not-for-business
c8｜四個坑（圖片版權、個資與金鑰、AI 亂補內容、廣告追蹤要守隱私法規）：方法建議，取自站內文章｜站內文章｜2026-09-29｜four-traps, check-before
c9｜CC BY 與 CC BY-SA 可商用、帶 NC 限非商業、帶 ND 不得散布改作版本、六種都要標示原作者｜https://creativecommons.org/share-your-work/cclicenses/｜2026-09-29｜cc-licenses

## 與企劃不同的地方

- brief 選項 A 的工具比較用 `compare`；腳本改成三列的 `table`，因為三家各有一個要注意的地方，並排較清楚。
- ChatGPT 的網站功能只提名稱層級，不寫方案與開放範圍：說明頁本次抓取為 403，無法當天確認。

## 我懷疑但沒動的事

- Cloudflare「直接把資料夾拖進去」依站內文章與 Cloudflare 的 Direct Upload 文件；撰稿日可再看一次 Direct Upload 頁的介面文字。
- Claude 的 artifact 儲存上限（每個 20 MB）與舊版 artifact 的差異沒有放進影片，避免過細。

## 2026-09-29 獨立複查更正

今日 OpenAI Sites 官方文件可讀，取代上方歷史 403 限制。另補正 index.html 副檔名、GitHub 軟／硬限制與自訂 Actions 例外、Cloudflare 新 Direct Upload 拖放 1,000 檔上限，以及 ND 對散布改作的限制。移除無實測支持的兩分鐘／五分鐘保證與無統計根據的「最常見」斷言。brief 保留原稿；ND 概述需依本次授權原文理解。因超過三項事實變更，另需第二位查核者覆核，不能只靠本報告當成上架通過。
