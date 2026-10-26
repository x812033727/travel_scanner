# 給有正式連線的操作方：C03 從零製作交接

站主已指示「從C03開始重製」「如果不行你就重新來吧」。Codex已把可做的來源、劇本、文字分鏡、獨立審查、canonical準備及免費送審做完；**舊素材不再需要等待，付費生成與成片尚未開始**。

## 精確輸入與關卡

- 新slug：`story-everyday-moleskine-c03-remake-20261025`；原集`story-everyday-moleskine-c03`原稿／帳本／上架包保留。
- video SHA：`9639d356ca5bdcb18e85c3631ea754a0f69888949358111f452541654ac7fdd9`；後台canonical script SHA：`4fbe37211a5beda9f309156f736a4bab1e2f52eb044d97ccfb6ffad3e3cf289f`。來源及雙讀者合併證據見 [README](README.md)、[status](../status.json)。
- [正式審稿頁](https://mokaair.com/zh-TW/admin/videos?tab=drama&video=story-everyday-moleskine-c03-remake-20261025)：outline `3b0480b5-0ca4-4337-b743-0db04dfb4106`、script `c90d3492-7efe-4385-bdcc-ccd6664205d1`，目前均已核准並匯入。只有一個實際企劃選項A，原生流程直接送人審，沒有購買Jev挑選。
- 執行根目錄（此環境）：`/workspace/work/brand-story-20261025/c03-submission-root`；媒體根目錄：`/workspace/work/brand-story-20261025/media`。新的canonical project有官方生命週期初始化的字典及獨立`verify-1.md`，無auto.json、無自行核准、無舊媒體移植。

## 尚需正式主機處理的入場條件

1. 已完成：兩筆後台企劃／劇本核准均已用官方`review-pull`匯入精確雜湊，見`backend-status.json`。其後正式TTS命令在供應商派送前以`video_budget_preproduction_hold`拒絕，exit 3、付費0；見`production-after-approval.json`。
2. 依現行`video_budget`受審啟用流程處理**僅此新slug**的帳戶：讀回供應商帳戶、模型、區域與價格、原C03歷史結案、各operation的reserved／uncertain／settled及餘額，保留原始證據。新slug本機與API hold仍有效；現有token無管理啟用能力，media/status也未暴露C03帳戶明細。
3. 讀 [pricing-and-entry.json](pricing-and-entry.json)：120個初始TTS請求／4194計費字元、100個插畫景／含首次每景最多3次，圖像目錄估價US$4.05；1首Lyria目錄價US$0.08，實際配樂報價待TTS時間線。語音、轉寫、Jev、重錄、未明費用仍須一起計入全片。檔案也列原生模型保守單次上界；它們不能當實際帳單或保證全片可在US$25完成。維持既有US$25停線，不能把US$200泛上限、字元額度或原集餘額當新版授權。未完成全片入場核對前不派付費請求。
4. 已完成：正式`mokaair-brand-package-v4-endscreen`已依PR1860下載並安裝，5秒片頭與21秒片尾的SHA／規格及完整AV decode已通過；詳見[正式品牌素材](../branding-pr1860/README.md)及[全批必要規則](../branding-pr1860/required-branding.json)。舊C03音訊、插圖仍不是從零重製的前置條件。

以上請保留可審閱讀回；不移除整個C系列保護、不刪或挪用原C03帳本、不把新slug改成舊slug借放行。原C03歷史US$25結案與10/24收尾啟用的文檔，不是新帳戶的即時餘額。

## 入場後的正式製作順序

使用本repo官方CLI與新project，先實際TTS並量正文12–14分鐘、逐句聽檢與發音覆核；不足就補有來源的新故事資訊並重新審稿，不靠停頓。聲音／劇本關卡成立後做100景新插畫與實際驗收、render、靜態運鏡、配樂、assemble、繁中燒錄字幕及CC，再完整解碼、音量／字幕／片頭片尾／插畫時間占比QA。正文插畫至少70%，卡片最多連3張，正式片頭5秒在濃縮開場後、v4片尾21秒。

真實生成與QA收據再送後台供站主看片。這份交接沒有音訊、分鏡成圖或成片核准，沒有YouTube上傳。媒體與帳本放repo外，付費素材不進Git；資料傳回需使用可讀共享路徑或暫存下載連結。

在另一台機器建立新runtime時，可依 [prepare-runtime](../prepare-runtime.mjs) 明確選`c03`；兩個根目錄都用repo外絕對路徑。不要直接將作者資料夾`c03`當canonical slug資料夾，亦不要覆寫已有媒體或核准的runtime。

## 主機唯讀檢查與八語預設

請有正式主機連線的操作方依[當前認證／唯讀交接](connection-and-budget-readback.md)執行已獨立複查PASS的`host-budget-metadata-readback.sh`。它先驗DB只讀交易，再直接讀兩個精確slug的帳戶及聚合費用；不變更主機、帳戶或啟用。現有影片權杖有效，網站管理員權杖不能取代主機；此環境尚無SSH及相應網路連線。舊`host-admission-readback.sh`與三項本機拒絕測試保留，但新slug的CLI hold發生於DB查詢前，不能證明帳戶不存在。實際主機尚未執行，檢查通過也不是製片授權。

新slug的獨立DB帳戶是否存在及實際餘額尚未取得主機讀回；合法額度註冊與API／client受審啟用也未確認；單加allowlist或新增帳戶均不足，不能把新片改成原slug。

站主已授權後續用建議設定並預設八語；正式後台也已讀回英、日、韓、西、葡、印尼、越南、泰文的metadata／CC／dub全數選取，決定時間`2026-10-25T14:09:36.202531Z`，見`backend-language-choice.json`。本次無須再套用同一選擇；`language-selection-request.json`保留同一完整payload供後續各集依授權預設。

八語1,144句文字與metadata已完成獨立校對，見`i18n/README.md`，但無實際時間軸／SRT或配音。不要手造`languages.json`的決定時間或假裝語言輪已開始。

配音仍要求實際clean核准成片。建議保留繁中燒錄輸出，再用`variants/clean-master/`從相同已驗主素材本機重新組乾淨主片，重新作真實QA及final審核；舊配方及其獨立收據已精確封存；新配方的[metadata獨立審查](variants/clean-master/review.json)已通過，原生檢查顯示劇本／旁白／圖像輸入相同，未宣稱影片已生成或關卡已通過。原生八語流程在真正乾淨主片成立後才啟動，不修改eligibility規則或借舊final核准。


## 已採用的預告共圖計畫

本次[受控採用](visual-only-runtime-adoption.json)只更新已獨立核對的prompt／camera，source SHA為`9639d356ca5bdcb18e85c3631ea754a0f69888949358111f452541654ac7fdd9`。官方劇本`4fbe37211a5beda9f309156f736a4bab1e2f52eb044d97ccfb6ffad3e3cf289f`及原approvals.json前後SHA完全相同；原native票仍Matches，不重抽、不造批准。既有八語文字、worksheets與review bytes未改，[明確source rebind](i18n/source-rebind-teaser-plan.json)保留原語意審核SHA，只承接相同旁白／metadata的既有TEXT_PASS；實際runtime0errors、32soft、0stale。

[正常report-only實讀](report-only-teaser-plan-readback.json)確認既有後台story、八語與原決定時間不變，沒有提交新審核或寫批准。官方upsert只替未分類影片設定category，不覆寫已有owner選擇；renderer category explainer用於既有合法資料卡，仍不得繞品牌故事clean/final/QA/dub要求。

[共圖計畫](image-reuse-plan.json)仍是planned、actual_same_asset_verified=false；runtime與媒體目錄production-handoff已保存相同計畫。原生CLI不強制pair，cache缺失會走新的付費派送；因此正式入場後，須先生成並驗收payoff，預告shot命令之前人工核live cache預期同key、實際已驗檔及SHA、完整參數均一致，缺任一項即停止，不能呼叫預告命令或啟動auto worker。任一端未驗收／seed或修正改變亦停整對；render前兩端選中及裁切後真檔bytes／SHA必須相同，兩context各驗收，帳本沒有重購。

舊clean配方／獨立收據已逐檔精確封存到`history/clean-master-before-teaser-image-plan`；新source只重新衍生純burnflag配方，variant SHA`4349a436af212203b79cdc0bfdc5920673cce2c0dd06442846116b37481c52c4`，[獨立metadata審查](variants/clean-master/review.json)已通過。沒有實際clean影片、完整QA、final或配音資格。新[免費預檢](preflight-inputs.json)仍不是全片報價；不嘗試真正TTS，所有付費保護維持。


## 正式v4素材已就緒（PR1860）

正式站current的`mokaair-brand-package-v4-endscreen`已下載、安裝到共同mediaBASE；package hash `416c8768d4d29f2e746a0c019d2d598ec367cbb66b0ff996841c523651a63e88`，5秒／150格片頭與21秒／630格片尾皆完成SHA、規格及完整影音decode PASS。12集branding preflight既有快照均通過；本集快照source 9639d356ca5bdcb18e85c3631ea754a0f69888949358111f452541654ac7fdd9，與此次手交接的current source吻合。品牌素材身份與取得已解阻，這是素材驗證，不是故事成片QA或付費入場。

全批權威：[required-branding.json](../branding-pr1860/required-branding.json)、[下載與QA／執行說明](../branding-pr1860/README.md)、[逐集快照](../branding-pr1860/project-preflights.json)。合成前須以本集最新runtime及slug重跑[唯讀preflight](../branding-pr1860/preflight.mjs)，正式站無法讀取、素材缺檔、disabled或版本／hash不符即停止；不能接受警告後無片頭繼續，也不能借其他系列包。

真正正文與其他必要製片關卡齊備後，依PR1860權威文件所列原生工具執行`assemble --intro-after-condensation`：**濃縮開場 → 5秒片頭 → 正文剩餘部分（含有聲CTA）→ 21秒片尾**。實聲正文仍須720–840秒，包含coldopen與口述CTA，只排額外bookends；片頭片尾另加26秒／780格，不用來填正文長度。實際字幕／章節／八語配音依真插入點處理其後+150格，片尾不殘留正文字幕。

本次只更新手交接，未建立單集production pin／timeline，沒有呼叫assemble或生成故事媒體。正常首次合成後才產生pin並驗實際總格數body+780、片頭接點、片尾音畫與字幕，再做完整解碼QA及新final審看。帳戶／歷史費用／全片報價／admission及真正TTS／實聲／故事畫面／成片QA仍依原關卡；`generated_story_media=0`、付費請求0，沒有新增owner決定或預算授權。
