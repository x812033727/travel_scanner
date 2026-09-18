# 審稿分組與各組要特別注意的事（協調者給 12 位審稿代理的補充；規格在 REVIEW-AI.md）

對照檔目錄：`<SCRATCH>\agents\review-ai\src\`，檔名 `<slug>.<語言>.txt`。修正清單寫到 `<SCRATCH>\agents\review-ai\corrections-<語言>-<組別>.json`。

## A 組（OpenAI 的企業動作）：astral、funding、s1、broadcom
slug：`ai-news-openai-astral-20260319`、`ai-news-openai-funding-20260331`、`ai-news-openai-s1-20260608`、`ai-news-openai-broadcom-chip-20260624`
- 四篇都不可比原稿多出利多、看好、搶進語氣；估值、募資金額、上市時程只能出現在原稿有的地方。
- astral：OpenAI 說「acquire」、Astral 說「join」兩個英文原詞要並存；「打算支援（plans to）」與「會繼續支援（will continue）」分開；「約六個月」「將近六個月」限定詞。
- funding：「承諾資本（committed capital）」不是入帳；「基石（anchored by）」不是領投；三批 4/1、7/1、10/1（日本時間）與「計畫」；Amazon 150 億＋350 億「符合特定條件時」；量詞 nearly tripled／5x／4x 的主詞與比較對象；數量級（1,220 億＝122 billion、9 億＝900 million、5,000 萬＝50 million…）。
- s1：「保密遞交 S-1 草稿」不可變成「申請上市」；EGC 與非 EGC 兩句都在（「委員會沒有權限延伸保密…」＋「非 EGC 仍可用既有保密處理程序」）；Form D 五處都用「本文引用的來源沒有解釋這份表單」的寫法，不可補定義；46／41／40＋6 每處一致。
- broadcom：tape-out 不是量產；「what may be」與「what we believe to be」分開並附英文；「大半是同一份文稿」的「大半」；前瞻性陳述與「不宜過度倚賴」；「打造成本更低」不是售價；「兩篇 6 月 24 日的官方文章沒有寫出貨或上市時間」範圍不可擴到 2025-10-13 那份。
- 譯者刻意的選擇（不要當錯誤退回，除非你有官方頁依據）：anchored by→ja「基盤となり」／ko「기반이 되었고」；zh-CN 通路→渠道、監理→监管、時程→时间表、查核→核查／核实；ja「探索」→「模索する」；「公司財務組」ja／ko 保留英文＋描述；ja／ko「路演（road show）」括注；sources 標題四語保留英文。
- en 的「本站」有些地方譯成 Mokaair、有些譯成 this site／we：以統一用語表為準（this site／we），Mokaair 出現在句首當主詞時可保留一次。

## B 組（OpenAI 的產品與治理）：gpt-55-instant、chatgpt-ads、frontier-governance、financial-services
slug：`ai-news-gpt-55-instant-20260505`、`ai-news-chatgpt-ads-20260505`、`ai-news-frontier-governance-20260528`、`ai-news-chatgpt-financial-services-20260910`
- gpt-55-instant：「將取代（will replace）」不可變成已取代；「本文不寫它已經停用，也不寫它現在仍是預設模型」整句在；xhigh 只綁 Cybersecurity；「在沒有系統層防護的基礎模型上」「不代表日常出錯率」每處在；分數方向（越高越少違規／越低越好）；方案名英文。
- chatgpt-ads：不是投放教學；「需要的金額」「預算與出價範例是示範用途」「總覽頁的更新紀錄」三個限定語；點擊與轉換都按點擊計費；「除了預算與帳戶花費上限之外」；「廣義平台分組」；2,500 個地點代碼與額外限制；台灣兩個方向都不推定。
- frontier-governance：哪些義務只落在「大型前沿開發者」、哪些是所有前沿開發者；「公開不等於全部看得到」那一題每項理由與「以遮蔽的理由所允許的範圍為限」；「本站把兩份 PDF 抽成全文比對」是本站動作；不可替 OpenAI 歸類；「未見台灣、日本、韓國字樣」照原文不改成讀者所在地。
- financial-services：三張評測各自的主詞與註記（OfficeQA Pro 沒註明誰做的、BoxBench 外部夥伴、簡報內部評測）；「合資格的金融機構」譯者用來源原文 eligible（不是 qualified，這是對的）；「逐格溯源」en 用來源的 granular citations；「正在與…合作開發」「將能」未來式；「超過 50 個以上（over 50+）」註記。
- 譯者刻意的選擇：zh-CN 簡報→演示文稿、鎖定→定向、轉換→转化、個人化→个性化；ja 查核→確認；en 單一登入／佈建還原成 SAML SSO／SCIM provisioning（來源原詞）；System Card／API Changelog 四語保留英文；gore／violence 保留英文附語意。
- 要判斷的：ja「災難性風險」譯「破局的リスク」、「遮蔽」譯「レダクション」；ko「가림 처리」——譯者自擬，若你有更通行的法律用語（附依據）就交修正。
- en 的「本站」以統一用語表為準（this site／we）。

## C 組（九月的技術與基礎設施）：nvidia-hf、gpt-live-1-api、storage-scale、gemini-38-live
slug：`ai-news-nvidia-hugging-face-20260903`、`ai-news-gpt-live-1-api-20260910`、`ai-news-chatgpt-storage-scale-20260911`、`ai-news-gemini-38-live-20260915`
- nvidia-hf：12,930,300,000 美元照數字；「已同意收購（has agreed to acquire）」不是已完成；四項承諾都是「NVIDIA 表示」；資安段落只寫影響範圍與鑑識流程，不可多出攻擊細節；「這是本文自己整理的背景對照」在；平台數字（1800 萬＝18 million、300 萬、50 萬、100 萬、20 萬、500＋、250＋）。
- gpt-live-1-api：「正式提供（generally available）」不是首次推出；「在來電者開口前用應用程式指定的語言」；「處理的是打進來的電話，不支援…對外撥出」；「沒有列出支援的口說語言」不可譯成「不支援中文」；每分鐘 0.05 美元、三分鐘 0.15 美元是本文換算；Tier 1–5：25／50／200／300／500；128,000／8,192／90%／30 天；語音名與業者名照原文。
- storage-scale：逾 7000 萬／秒、逾 2000 萬、22M、逾 500 PB、近 40 個地區、每週逾 10 億人、逾 10 倍、6 倍／15 倍／95%；「沒有把任何國家或城市寫成資料存放地點」是刻意限縮，不可譯回「沒有任何國家名稱」；「摘要／中繼資料」與「正文」的區分；metastable failure 附英文。
- gemini-38-live：四個成績（82.6／68.6%／35.1%／97.7%）主詞都是 Extended Thinking、3.8 Live 是 Speech Agent Arena 第二名；`τ` 照原樣；「即日起推出（rolling out starting today）」≠ 現在就能用；「發表文那張清單」與「模型卡的通路清單不同、本文照原樣並列」；價格表每格；「沒有一句寫出開放的國家、地區或市場」是限縮寫法；97 種與 97 種以上並列。**en 特別查**：Extended Thinking 的定位句英文（"built for high-complexity tasks, with more intelligence and multi-step reasoning capabilities"）是譯者依 fact 改寫，不是逐字引文——請回 Google 發表文（研究紀錄 `verified_facts` 或來源頁）對出原句，對不上就改成原句或改成轉述（不加引號）。
- 譯者刻意的選擇：「擁抱表情符號品牌」四語用文字描述；zh-CN 監理→监管；Enterprise Hub／Inference Endpoints 保留英文；亞穩態故障 ja「準安定故障」／ko「준안정 장애」、尾端延遲 ja「テールレイテンシ」（附英文）；private preview ja「非公開プレビュー」／ko「비공개 프리뷰」／zh-CN「私有预览」；ja 圖解企業格用「限定」對應正文「非公開」（字數）；zh-CN「SIP 请求头」譯者自認略窄、可改「SIP 头部」——zh-CN 審稿請判斷。
- en 的「本站」以統一用語表為準（this site／we）。
