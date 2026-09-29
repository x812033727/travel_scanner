# 2026-09-29 第二輪獨立事實查核

查核者：codex-p1-product-review（不是原撰稿者，也不是第一輪查核者）。範圍為第一輪全部 14 個更正位置，加上從第一輪 9 項 CONFIRMED 主張隨機抽出的 3 項；另補核對三家工具及 GitHub 商業用途限制。這是文字事實查核，不是配音、成片或上架驗收。

先將 video.json 的全部 line.text、say、slide.data、thumbnail、YouTube title/description/tags 抽為 228 個編號文字位置，才開始逐項判斷。抽樣用 crypto.randomInt 的 Fisher–Yates shuffle，結果為第一輪表格 #4、#5、#9，沒有重抽。原始清單、抽樣結果、今日重新抓取的來源及 HTTP/redirect 收據存於本次外部 evidence 的 vibe-coding-first-website-2026 子目錄。沒有把 claims.md 或第一輪結論當成證據。

2026-09-29 重新取得 11 個官方頁面，全部 HTTP 200；使用 Mokaair-editorial/1.0 識別、跟隨 redirect、讀取前移除 HTML comments，同 host 至少間隔 1 秒。Claude 舊址轉到新文章，CC 舊址轉到 /cc-licenses/。OpenAI 另依 OpenAI Docs 技能搜尋並開啟官方文件；本輪共 1 次網頁搜尋。

## 全部 14 個更正位置

「之前 → 之後」描述本輪收到的內容及本輪處理；第一輪原句仍保存在 verify-p1-20260929.md，不覆寫其歷史。

| # | 主張 | 位置 | 官方 URL | HTTP | 判定 | 之前 → 之後 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 此單頁 HTML 使用 index.html | `scenes.4.data.sub` | [GitHub 入口檔](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)、[Cloudflare 靜態 HTML](https://developers.cloudflare.com/pages/framework-guides/deploy-anything/) | 200 / 200 | CONFIRMED | index.html → 保留；GitHub 也接受 index.md、README.md，影片沒有宣稱所有網站只能用此檔名 |
| 2 | 同上，旁白檔名及 say 一致 | `tech-bounds:dv87` text/say | 同 #1 | 200 / 200 | CONFIRMED | index.html / index 點 H T M L → 保留；say_for 為 38121ecc2e44 |
| 3 | GitHub 已發布網站不得超過 1 GB | `hosting:knvi`，依賴 `hosting:hvjf`、`scenes.11.data.rows.0.1` | [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits) | 200 | CONFIRMED | 硬上限 1 GB → 保留；不能再把所有限制稱為軟限 |
| 4 | 每小時 10 builds 軟限的例外是自訂 GitHub Actions 建置及發布流程 | `hosting:4raw` text/say、`claims.md:c5` | [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits) | 200 | CHANGED | 泛稱「自訂的部署工作流程」→「自訂 GitHub Actions 流程」；新增對應 say 與 say_for 22f9d14a8d4d |
| 5 | 上線步驟的 HTML 首頁檔名 | `scenes.12.data.steps.0.title` | 同 #1 | 200 / 200 | CONFIRMED | 首頁叫 index.html → 保留 |
| 6 | 1,000 檔限制只適用 Cloudflare dashboard 拖放 | `scenes.12.data.steps.2`、`claims.md:c6` | [Cloudflare Direct Upload](https://developers.cloudflare.com/pages/get-started/direct-upload/) | 200 | CHANGED | 泛稱「上傳或拖放（最多 1,000 檔）」→ 標題「上傳或拖放」，detail「Cloudflare 拖放：最多 1,000 檔」；Wrangler 的表列上限是 20,000，不能把 1,000 套到所有上傳方式 |
| 7 | 此單頁 HTML 的入口檔名與 say 一致 | `deploy-steps:5ymd` text/say | 同 #1 | 200 / 200 | CONFIRMED | index.html / index 點 H T M L → 保留；say_for 為 0d4d7ff86889 |
| 8 | 新建 Direct Upload 專案可拖放資料夾，每次最多 1,000 檔 | `deploy-steps:7g2d` | [Cloudflare Direct Upload](https://developers.cloudflare.com/pages/get-started/direct-upload/) | 200 | CONFIRMED | 「直接上傳」是 Direct Upload 的中文表述 → 保留；既有 Git integration 專案不能從 dashboard 拖放，影片沒有教人切換既有專案 |
| 9 | 檔名或路徑不符可能造成公開頁打不開 | `deploy-steps:z4ax` | [GitHub 入口檔位置](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)、[Cloudflare 404 說明](https://developers.cloudflare.com/pages/framework-guides/deploy-anything/) | 200 / 200 | CONFIRMED | 「可能」的條件性敘述 → 保留；沒有把它推成最多見的原因 |
| 10 | 仔細檢查，不只依賴 AI | `check-before:ykf6` | 不適用（方法建議；只查刪除保證是否完整） | — | OUT OF SCOPE | 兩分鐘保證已刪除 → 保留建議；不聲稱新的實測時間 |
| 11 | 搜尋到圖片不等於已有使用授權 | `four-traps:rqt9` | [Google Search 圖片使用權說明](https://support.google.com/websearch/answer/29508?hl=en) | 200 | CONFIRMED | 條件性提醒 → 保留；Google 要求使用前查驗實際授權及其條款，搜尋篩選不是使用許可 |
| 12 | 公開前逐項檢查，疑問先處理 | `four-traps:9vp8` | 不適用（方法建議；只查刪除保證是否完整） | — | OUT OF SCOPE | 每項不到五分鐘保證已刪除 → 保留建議；不聲稱新的實測時間 |
| 13 | ND 禁止散布改作版本 | `scenes.16.data.right.points.1` | [CC BY-ND 4.0 deed](https://creativecommons.org/licenses/by-nd/4.0/deed.en) | 200 | CONFIRMED | 不得散布改作版本 → 保留；不能簡化成一概禁止私下改作 |
| 14 | NC 與 ND 的旁白範圍 | `cc-licenses:3r9q` | [CC 授權總覽](https://creativecommons.org/cc-licenses/)、[CC BY-ND 4.0 deed](https://creativecommons.org/licenses/by-nd/4.0/deed.en) | 200 / 200 | CONFIRMED | NC 限非商業、ND 不得散布改作版本 → 保留 |

14 是修改位置數，不是 14 個獨立新事實；檔名、拖放限制、ND 各有重複依賴。以上 10 CONFIRMED、2 CHANGED、2 OUT OF SCOPE。

## 隨機抽查及額外複核

| # | 主張 | 位置 | 官方 URL | HTTP | 判定 | 之前 → 之後 |
| --- | --- | --- | --- | --- | --- | --- |
| S1（原 #4） | GitHub Free 支援公開 repo 的 Pages；網站 1 GB、每月頻寬 100 GB 軟限、每小時 10 builds 軟限與 Actions 例外 | `hosting`、`claims.md:c5` | [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits) | 200 | CONFIRMED | 數值保留；Actions 名稱範圍修正見 #4，不重算一次事實變更 |
| S2（原 #5） | Cloudflare Free 同時 1 build、每月 500、每站 20,000 檔、單檔 25 MiB、每帳號 100 專案 | `hosting`、`claims.md:c6` | [Cloudflare Pages limits](https://developers.cloudflare.com/pages/platform/limits/) | 200 | CONFIRMED | video/claims 的數值保留。第一輪報告把 100 專案稱「軟限」沒有當日來源支持：官方寫 limit 且非例行提高，本輪不沿用該標籤；不是把另一份報告的措辭當產品證據 |
| S3（原 #9） | BY/BY-SA 可商用；NC 限非商業；ND 不得散布改作；六種授權均要求署名 | `cc-licenses`、`claims.md:c9` | [CC 授權總覽](https://creativecommons.org/cc-licenses/)、[CC BY-ND 4.0 deed](https://creativecommons.org/licenses/by-nd/4.0/deed.en) | 200 / 200 | CONFIRMED | 保留。BY-SA 的相同條件、其他人格／隱私權等仍須依實際授權閱讀；沒有聲稱署名就是所有條件 |
| E1 | Claude Artifacts 免費可用；需程式執行與檔案建立；legacy artifact 可複製／下載 | `tools:25fx/ciyv`、`open-file` | [Claude 官方文件](https://support.claude.com/en/articles/17153992-what-are-artifacts-and-how-do-i-use-them) | 200 | CONFIRMED | 保留。免費一般 artifact 不等同所有付費 template；團隊／企業的開關在組織設定。影片沒有逐一聲稱 template 免費 |
| E2 | Gemini Canvas 需登入，具有程式碼、預覽、console 與分享／匯出功能 | `tools:ducf/kbcx`、`claims.md:c3` | [Gemini Canvas 官方說明](https://support.google.com/gemini/answer/16047321) | 200 | CONFIRMED | 保留功能層級敘述；不把文件／簡報的匯出選項推論成任何 app 均能一鍵下載完整獨立 HTML |
| E3 | ChatGPT Sites 可以建立、代管、修改及分享網站 | `tools:8u87`、`claims.md:c4` | [OpenAI 官方 Sites 文件](https://learn.chatgpt.com/docs/sites) | 200 | CONFIRMED | 保留功能敘述與方案／地區須再查的限制。官方列有資格的付費方案，本報告不把影片的免費上線承諾擴張成 Sites 免費 |
| E4 | GitHub Pages 不得充當經營線上事業／電商或以商業交易、商業 SaaS 為主的免費主機 | `not-for-business`、`claims.md:c7` | [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits) | 200 | CONFIRMED | 保留。這不等於所有含商業資訊的個人作品集都被禁止；影片未作這項擴張 |

## 聽眾、企劃與剩餘驗收

- index.html 兩處 say 與 text hash 都有效；Actions 的本輪 say 用「艾克申斯」，沒有改共用 lexicon。Lint 只證明格式與 hash 一致，真人仍須聽讀法。
- 全部旁白 text 沒有超過 40 字的句子；有效 say 沒有未知英文字。旁白沒有 URL 或括號。尚未渲染，不宣告 reveals 的畫面時序通過；例如 what-is 首句先顯示步驟再逐項講解，可由聽眾審稿判斷節奏。
- 第一輪列的查證口吻 `not-for-business:3ggy/ntu6`、`cta:dt7n` 保留。`tech-bounds:j8r3` 的「省掉一半麻煩」、`four-parts:d7wu` 的「幾乎完全」、`tech-bounds:razt` 的「搬到哪裡都不會壞」、`vague-words:wtvb` 的「唯一原則」屬未清楚標示的編輯判斷／絕對表述；brief 支持方法方向，但不是這些效果的量測證據。依 facts-only 與意見 mismatch 規則記錄，未自行重寫語氣，仍需站主與聽眾審稿。
- brief 的 ND「不可改作」仍與更精確的授權原文不同；按授權原文採「不得散布改作版本」，不改 brief。brief 的工具方案及持續儲存細節未全部搬入腳本，不能把本輪檢查當成整份 brief 都已確認。
- CTA 宣稱第一行有文章連結，但目前 youtube.description 還不是最終上架包，首行沒有該連結；source_guide 的發布狀態、文章是否包含所述範本及後續維護承諾仍未驗證。上架包必須補實際連結並驗內容，不能只因 source_guide 字串存在而勾選。
- 未試用三家工具完整走過單頁匯出流程；未生成或核對配音、字幕、翻譯、成片及 YouTube 播放。尤其「挑有帳號的那家」必須在真人試用確認該帳號權限與可匯出結果，不能由功能文件推論每個帳號都可走同一路徑。

## 結果

- 本輪表格覆核 21 列（含重複依賴）：17 CONFIRMED、2 CHANGED、2 OUT OF SCOPE。需要查證的本輪修改與抽樣主張無未解來源；第一輪「100 專案軟限」標籤為 NOT FOUND，未出現在影片或 claims 的原文，因此不另改腳本。
- 本輪只有 2 個事實適用範圍更正，均已同步相關 text/say/data/claims；沒有新增場景、改 brief、改 lexicon 或製作媒體。本輪未超過 3 個新事實更正，依門檻不強制第三位 reviewer。第一輪所要求的獨立第二輪已完成，但整支影片仍未通過上架驗收。
- 易過期事實：工具資格、設定位置、主機配額。查核日為 2026-09-29；Cloudflare limits 頁標記更新日 2026-09-05，Direct Upload／Static HTML 頁為 2026-04-21。到製作或上架時仍需重查。
- `node tools/video/cli.mjs lint --slug vibe-coding-first-website-2026`：exit 0，**0 errors / 0 warnings**。以 bundled Node 24.21.0 執行。102 句，估時 8.2 分鐘，這是估算而非實際音訊時長。
- 此收據綁定 video.json SHA-256 `ca43ab77d9914a38240bef5eea45fd9cec9ac63218ab7cb12904142dca34d425`；claims.md SHA-256 `38f6f45d4d66f97a04894a3d669998715a4400ad28f28ddb216204337a66d90f`。

## Commit-byte receipt

Final `video.json` SHA-256 with repository LF line endings: `930e925a17c84b8b507e2e36065c1f8ad741bd75a61eb7b5ec27ca99605bcc55`. Before line-ending normalization: `ca43ab77d9914a38240bef5eea45fd9cec9ac63218ab7cb12904142dca34d425`. Only CRLF-to-LF changed; JSON values, facts and say hashes are unchanged. Use this final hash for handoff and invalidate any older media/approval bound to a different script.
