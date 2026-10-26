# 第四片有界研究：先審大綱，再把公共報告變成可交付簡報

研究截止：2026-10-25 UTC。新聞主窗為過去7天；外語影片參考放寬至30天。建議採用候選A，定位為「由新功能引出的原創工作流程示範」。本地已做出4頁PDF、PNG及可編輯PPTX，附逐頁來源清單；**沒有登入或執行 Gemini Notebook、Canva 生成服務**。若影片定位必須是「Notebook 新功能實測」，目前證據不足，應暫緩這個產品實測標題。

候選標題方向：「AI簡報先別急著生成：先審大綱，再交出4頁有來源的成品」。觀眾會得到一份可複用的需求格式，以及可以實際打開的簡報。70%／79% 僅是本次遇到而尚未對齊的來源觀察，不應成為「Stanford寫錯」或「AI又亂編」的標題。

## 三個近期候選

| 候選 | 官方新消息／日期 | 可以教觀眾做什麼 | 本輪判斷 |
|---|---|---|---|
| A：Gemini Notebook 共同製作簡報／影片 | [Google產品公告](https://blog.google/innovation-and-ai/products/gemini-notebook/co-create-slides-videos/)，10月19日；[Workspace公告](https://workspaceupdates.googleblog.com/2026/10/gain-more-creative-control-over-slide-Decks-and-Video-Overviews-in-Gemini-Notebook.html)，10月21日 | 在渲染之前先審來源範圍、每頁問題與敘事，集中回覆修改，再交付有來源的簡報 | 最適合。公共資料可直接實作，成品能審；新聞功能為 **CITED**，本地流程為 **RUN**。不得稱為產品操作測試。 |
| B：Gemini Customize 集中管理 skills 與連接應用 | [Workspace公告](https://workspaceupdates.googleblog.com/2026/10/an-easier-way-to-customize-how-gemini-works-for-you.html)，10月21日 | 將重複的語氣、格式和輸出要求保存成可複用規則 | 一般生產力題目成立，但本輪沒有登入執行，也沒有跨帳號連接工具；缺乏比A更有辨識度的成品。 |
| C：Canva Craft 兩階段圖像模型 | [官方介紹](https://www.canva.com/newsroom/news/canva-craft/)、[官方新聞索引](https://www.canva.com/newsroom/news/)，10月22日 | 先定構圖／文字層級，再生成不同尺寸的設計素材 | 創作題材廣，但需要實際帳號或API才能評估生成品質；本輪沒有呼叫。與已做的可編輯創作題目較接近，列備選。 |

三者的原始官方HTML、抽取文字、HTTP200、抓取UTC、UA、大小及SHA均保存在 `fourth-demo/sources/`。Canva日期可在官方頁面的 `publishedAt=2026-10-22T19:00:00.000Z` 對應到該篇標題，並非拿相鄰新聞日期代用。

A的官方設計是先選主題／形式／風格，開啟Review後審投影片大綱或影片製作筆記，一次回覆修改，再按Proceed生成；也可以不開Review。Workspace公告說10月16日起分批推出、最長15天，並列出Workspace／Individual／個人帳號；但抓取當下的[簡報說明](https://support.google.com/gemininotebook/answer/16757456?hl=en)與[影片說明](https://support.google.com/gemininotebook/answer/16454555?hl=en)均把co-create列為Google AI Ultra功能。這個公告／說明落差尚未以真實帳號解決，不能保證免費帳號此刻能用。簡報說明也寫明Proceed後不能再修改該大綱；後續投影片修訂目前不採用來源。若日後拍產品操作，應以當時帳號畫面和方案為準。

B的Customize選單公告說全方案、全球多平台推出，但多數連接應用目前限美國英語，部分擴至其他英語地區、巴西與印度；不能把選單全球推出解讀為所有應用全球可連。[10月13日rollout更新](https://workspaceupdates.googleblog.com/2026/10/an-update-on-launch-of-skills-in-gemini-app-and-workspace.html)另說Gemini app skills預計11月中完成，而Workspace skills延後、尚待新時程，兩者不能混為已全面上線。

C官方說現已在Canva／Dream Lab和公開API提供，採先構圖計畫再渲染的兩階段，最高2K、30多種比例、可生成55種語言文字。Canva MCP的具體小節仍寫Coming Soon；更快變體及後續編輯／參考圖能力亦屬未來項目。沒有重現DesignArena排名或官方速度／成本比較，因此不採用那些比較當結論。

日期排除項：[Adobe Acrobat Productivity Agent原文](https://news.adobe.com/news/2026/09/adobe-productivity-agent-in-acrobat-now-transforms-complex-documents)實為9月9日，超出30天。起初搜尋索引把它與10月22日另一則Adobe新聞並置，已回原文校正，不把它充作本週消息。

## 五個外語YouTube公開標題／觀看快照

蒐集窗：2026-10-25 19:20:47–19:26:09 UTC。直接YouTube頁面在本環境回代理403或擷取受限，以下觀看數取自**公開第三方文字中繼頁**，不是YouTube即時分析。保留YouTube原連結供人工核對。標題可能被本地化或更改；crawl age是搜尋服務標籤，不能當觀看計數時間。未下載或觀看影片、未測CTR／留存，也不能從觀看數推論剪輯節奏有效。

| 頁面顯示標題／頻道 | 顯示發布日 | 顯示觀看數 | 來源與可用參考 |
|---|---|---:|---|
| GEMINI NOTEBOOK (NotebookLM) now works inside Google DOCS, SHEETS, and SLIDES — Ernesto Ibáñez | 10月18日 | 15,090 | [YouTube](https://www.youtube.com/watch?v=hVhMxCwSEZA)／[文字快照](https://zolotube.com/watch?v=hVhMxCwSEZA)，crawl yesterday。描述依序給報告、表／圖、簡報prompt；早於10月19日新co-create公告，僅是相鄰流程參考。 |
| 98% of People Use NotebookLM Only to Summarize (Do This Instead) — Pau Rodríguez | 10月7日 | 978 | [YouTube](https://www.youtube.com/watch?v=L7ygZh8sXSo)／[文字快照](https://zolotube.com/watch?v=L7ygZh8sXSo)，crawl last week。描述為10種用途；其98%與藏錯誤測試均未重現。搜尋曾出現另一標題，記錄採開啟頁顯示版。 |
| Clase 4 - Tres formas de realizar presentaciones profesionales con IA — IA en salud desde cero | 10月12日首播 | 6,063 | [YouTube](https://www.youtube.com/watch?v=ILUGjeT5Nrw)／[文字快照](https://zolotube.com/watch?v=ILUGjeT5Nrw)，crawl today。描述比較ChatGPT／Gamma／NotebookLM及PPT／PDF交付；未評估醫療內容。 |
| Learn GEMINI NOTEBOOK from SCRATCH: Complete and Updated Guide — Karine Lago | 10月14日 | 24,488 | [YouTube](https://www.youtube.com/watch?v=HQFkyIQ4iPI)／[文字快照](https://zolotube.com/watch?v=HQFkyIQ4iPI)，crawl last week。葡語創作者，頁面標題顯示英語；章節文字由來源／引用帶到Studio成品。 |
| 발표를 위한 무료 AI 도구 TOP 3 \| (60초 만에 PPT 만들기) — Muhammad Irfan | 10月6日 | 729 | [YouTube](https://www.youtube.com/watch?v=wubrvwp71Xc)／[文字快照](https://zolotube.com/watch?v=wubrvwp71Xc)，crawl today。搜尋另索引英語「Top 3 FREE AI Tools for Presentations…」；韓語為頁面顯示版，未確認原始語言，亦未重現60秒速度。 |

五則都在30天內，只有第一則落在7天窗邊界；它們支持「公共報告→可交付簡報」是可辨認的觀眾用途，並不能證明本週新功能已被這些影片測過或題材必定熱門。描述／章節可參考的共同做法是先給可複用輸入，再交成品與匯出格式；本輪沒有觀察實際畫面或剪輯。完整快照含變體與限制存 `fourth-demo/youtube-metadata-snapshots.json`。

## 本地RUN：一份公共PDF，四頁可交付簡報

真實輸入為[Stanford 2026 AI Index經濟章PDF](https://hai.stanford.edu/assets/files/ai_index_report_2026_chapter_4_economy.pdf)，HTTP200，6,450,805 bytes、60頁，SHA256：

`6654b484b0c20213ead6ed8388f3145928c2dde9bca86e16a5b7efe9a00d8269`

這是2026報告，本例採用的投資／使用資料是2025年，沒有把它說成2026年10月調查。原始PDF、HTTP收據、所用完整頁文字及完整頁PNG均保留。PDF頁序以1起算；印刷頁碼另列。

| 採用的數字 | 正確範圍／單位 | 來源 |
|---|---|---|
| 581.69 | 2025全球企業AI投資，十億美元；包含多類融資活動 | 印刷p178／PDF第8頁，圖4.2.1 |
| 344.66 | 同年全球私人AI投資，十億美元；為前列總額中的一部分，不可相加 | 同頁同圖 |
| 285.88、12.41 | 2025美國／中國私人AI投資，十億美元；不是兩國全部公私AI支出 | 印刷p182／PDF第12頁，圖4.2.8 |
| 88% | 2025受訪者回報其組織在至少一項業務使用AI；自述調查，不能當人口普查 | 印刷p193／PDF第23頁，圖4.3.1 |

私人投資資料來自報告的Quid口徑；附註對企業／融資範圍有限定，不能把私人融資圖改叫「所有AI投資／政府AI預算」。本例只保留圖上值，不加算容易誤導的投資總和，也未用四捨五入後的數值另做精確倍數宣傳。

**70／79的查核狀態：未解。** 章摘要印刷p173／PDF第3頁，把2025生成式AI使用描述為組織在至少一項業務使用、列70%；詳細章節印刷p193／PDF第23頁，描述為受訪者回報其組織「regularly」使用生成式AI、列79%。兩處年份都指2025，但組織／受訪者分母描述與使用措辭有別，尚未確立為同一問項、同一母體。原始整頁與上下文已保存，不能僅因數字不同就判定誰錯。

另外查了[McKinsey 2025原始調查](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai-2025)，發布日2025-11-05，調查為2025-06-25至07-29、1,993位受訪者、105國，按各國GDP加權，38%受訪者來自年營收逾10億美元組織。原文支援88%敘述；[官方圖表頁](https://www.mckinsey.com/featured-insights/charts/ai-at-work-but-not-at-scale)的圖像描述列2025生成式AI79%，並列同一調查資訊，但該描述披露由Writer輔助撰寫，僅作追查線索。這不足以確立摘要70%的原始問項／分母，所以維持未解。沒有混入McKinsey後來的2026年調查。這兩頁原始HTML與HTTP200收據亦保留。

本地流程是本對話助理原創規劃＋確定性PDF抽取與排版，沒有另呼叫模型API，也不是從產品取得的大綱。`outline-before-review.json`是明示的作者初稿，尚未渲染；初稿將不同指標塞進兩頁。先一次回覆全部修改，再生成4頁：

1. 先把「投入多少錢」與「多少受訪者回報使用」分開。
2. 全球企業投資及其私人投資子集，同圖交代不可相加。
3. 用同年、同單位、同私人融資口徑比較美國／中國。
4. 88%有來源支持；70／79只顯示為兩處來源觀察，清楚標未確認，不採納為生成式AI採用率。

可複用輸入格式：

> 用指定來源做4頁、約3分鐘團隊簡報。先交大綱，不要生成成品。每頁列一個讀者問題、要用的數值、資料年、單位、受訪母體／統計範圍、印刷頁碼和PDF頁序。來源若有未對齊處，列待確認，別替我選一個數字。等我一次回覆全部修改後，再產出可編輯簡報與PDF，並附逐頁來源清單。

「約3分鐘」只是需求目標，未量測朗讀。可教的操作重點是先定每頁要回答的問題、逐項綁單位和來源、將未解資料保留為註記、最後交付可編輯檔與來源清單；不需要把影片變成Python安裝課。

## 實物、驗證與採用界線

本地產出根目錄：`/workspace/work/ai-tech-next/fourth-demo/`。

- `output/reviewed-briefing.pdf`：4頁、真正可打開的簡報PDF，依已渲染PNG製作。
- `output/reviewed-briefing-editable.pptx`：4頁原生文字方塊／形狀，可編輯；已由python-pptx重新開啟驗證結構，未在PowerPoint原生程式渲染，不能承諾各平台字型完全一致。
- `output/s1.svg`至`s4.svg`、對應PNG：原創1600×900版面；已逐頁實際檢視，無遮擋／溢出，數字、資料年、來源可見。圖中的Notebook標籤明示本地流程、非產品畫面。
- `output/page-citation-manifest.json`：每頁所用claim、印刷頁碼、PDF頁序、圖號、來源URL及PDF SHA；C6未解數字僅列annotation，不列採用claim。
- `source-economy.pdf`、`source-selected-pages.json`、`output/source-pdf-page-{03,08,12,23}.png`：完整輸入和所用整頁上下文。
- `input-brief.json`、修改前後大綱、`review-feedback.json`、`claim-ledger.json`、`results.json`、`visual-review.json`、`manifest.json`：可重查輸入、修改、輸出與SHA。生成器為`build_demo.py`，沒有安裝套件或改全域環境。

實測生成階段2026-10-25 19:35:26–19:35:27 UTC，確定性本地管線1.604秒，4頁PDF／PPTX重新開啟成功，5項數值claim有來源、1項口徑對齊未解。這不是Notebook或Canva生成時間，也不包含研究、人工規劃和視覺檢查時間；沒有量測節省多少時間／API成本、模型優劣或帳號額度。研究與追查已止於上述有界材料，不延伸成完整AI Index審計。

**採用建議：A可用，但片名／旁白應明示是新功能啟發的原創流程，不是假裝產品實測。** 若要錄Notebook產品畫面，還需有可用帳號、核對Ultra與rollout狀態，再實際走一次Review→Proceed→匯出；本輪沒有完成這件事。B與C留作備選，沒有帳號使用證據，不能補寫成已實測。未建立第四片episode、未修改task/backend/git、未安裝環境、未使用付費API、未下載YouTube影片；本輪只交研究和本地可審成品，沒有宣稱影片已製作。
