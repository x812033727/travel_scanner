# 給有正式連線的操作方：C03 從零製作交接

站主已指示「從C03開始重製」「如果不行你就重新來吧」。Codex已把可做的來源、劇本、文字分鏡、獨立審查、canonical準備及免費送審做完；**舊素材不再需要等待，付費生成與成片尚未開始**。

## 精確輸入與關卡

- 新slug：`story-everyday-moleskine-c03-remake-20261025`；原集`story-everyday-moleskine-c03`原稿／帳本／上架包保留。
- video SHA：`65ca1b602a5048e4f6af7c721bf1bd15abf152616c07d179f6ff5b6350c02005`；後台canonical script SHA：`4fbe37211a5beda9f309156f736a4bab1e2f52eb044d97ccfb6ffad3e3cf289f`。來源及雙讀者合併證據見 [README](README.md)、[status](../status.json)。
- [正式審稿頁](https://mokaair.com/zh-TW/admin/videos?tab=drama&video=story-everyday-moleskine-c03-remake-20261025)：outline `3b0480b5-0ca4-4337-b743-0db04dfb4106`、script `c90d3492-7efe-4385-bdcc-ccd6664205d1`，目前pending。只有一個實際企劃選項A，原生流程直接送人審，沒有購買Jev挑選。
- 執行根目錄（此環境）：`/workspace/work/brand-story-20261025/c03-submission-root`；媒體根目錄：`/workspace/work/brand-story-20261025/media`。新的canonical project有官方生命週期初始化的字典及獨立`verify-1.md`，無auto.json、無自行核准、無舊媒體移植。

## 尚需正式主機處理的入場條件

1. 讀回同一筆後台企劃／劇本的實際決定，以官方`review-pull`匯入精確雜湊；不可把新稿的來源PASS當站主核准。
2. 依現行`video_budget`受審啟用流程處理**僅此新slug**的帳戶：讀回供應商帳戶、模型、區域與價格、原C03歷史結案、各operation的reserved／uncertain／settled及餘額，保留原始證據。新slug本機與API hold仍有效；現有token無管理啟用能力，media/status也未暴露C03帳戶明細。
3. 讀 [pricing-and-entry.json](pricing-and-entry.json)：120個初始TTS請求／4194計費字元、100個插畫景／含首次每景最多3次，圖像目錄估價US$4.05；1首Lyria目錄價US$0.08，實際配樂報價待TTS時間線。語音、轉寫、Jev、重錄、未明費用仍須一起計入全片。檔案也列原生模型保守單次上界；它們不能當實際帳單或保證全片可在US$25完成。維持既有US$25停線，不能把US$200泛上限、字元額度或原集餘額當新版授權。未完成全片入場核對前不派付費請求。
4. 核對並提供正式v4片頭／片尾與manifest及完整SHA-256。舊文件指向`mokaair-brand-package-v4-endscreen`；本環境只有`curio-archive-original-candidate-20261020-v1`候選，5／21秒相同不代表是正式v4。這項頻道素材需要取回，C03舊音訊、插圖則不再是前置條件。

以上請保留可審閱讀回；不移除整個C系列保護、不刪或挪用原C03帳本、不把新slug改成舊slug借放行。原C03歷史US$25結案與10/24收尾啟用的文檔，不是新帳戶的即時餘額。

## 入場後的正式製作順序

使用本repo官方CLI與新project，先實際TTS並量正文12–14分鐘、逐句聽檢與發音覆核；不足就補有來源的新故事資訊並重新審稿，不靠停頓。聲音／劇本關卡成立後做100景新插畫與實際驗收、render、靜態運鏡、配樂、assemble、繁中燒錄字幕及CC，再完整解碼、音量／字幕／片頭片尾／插畫時間占比QA。正文插畫至少70%，卡片最多連3張，正式片頭5秒在濃縮開場後、v4片尾21秒。

真實生成與QA收據再送後台供站主看片。這份交接沒有音訊、分鏡成圖或成片核准，沒有YouTube上傳。媒體與帳本放repo外，付費素材不進Git；資料傳回需使用可讀共享路徑或暫存下載連結。

在另一台機器建立新runtime時，可依 [prepare-runtime](../prepare-runtime.mjs) 明確選`c03`；兩個根目錄都用repo外絕對路徑。不要直接將作者資料夾`c03`當canonical slug資料夾，亦不要覆寫已有媒體或核准的runtime。
