# C04 製片接續

精確新slug為`story-everyday-bubble-wrap-c04-remake-20261025`。正式劇本review `4b59f286-1467-4548-b0da-95b5462f682f`已核准並匯入相符SHA，獨立來源檔`verify-1.md`也已進canonical。本次唯讀確認現行企劃approved；圖像採用及report-only步驟的批准檔保持不變，其後另以正常review-pull匯入這份真實owner決定，獨立收據見`outline-approval-import.json`。企劃與原script現在都已匯入。

執行根目錄`/workspace/work/brand-story-20261025/submission-root`；媒體base為`/workspace/work/brand-story-20261025/media`。官方CLI的`--workdir`應傳base，工具會自行加slug。不要重新執行prepare-runtime覆寫已有核准的runtime。另一台新工作機才用repo外兩個根目錄明確選`c04`，由官方字典生命週期建立新執行目錄。

新slug仍受C系列付費保護；缺逐片合法註冊、獨立帳戶、API及本機受審啟用，以及供應商價格、歷史／reserved／uncertain／settled費用和餘額讀回。既有US$25停線不變，工具顯示US$200不是本片授權，也不借舊集帳戶。C03仍先做媒體；本集的免費準備不代表已獲付費放行。

現有dry-run為101個初始TTS請求、3640計費字元；92個插畫鏡頭，每景含首次最多3次，當時圖像估價最高約US$3.73。這只是圖像階段估價，非全片或八語報價；音樂仍缺真實時間線，語音／轉寫／Jev／重試／語言配音等須共同核算，未形成全片報價前不派付費。

正式v4品牌素材已由正式站取得、安裝及完成影音decode核對，品牌素材身份與取回已解阻，詳見[正式收據](../branding-pr1860/README.md)。取得合法入場後，先真實TTS量正文12–14分鐘並逐句聽檢／讀音覆核，不以停頓、慢播或警語填時長；需改旁白則重新走精確稿件關卡。

聲音關卡後，生成及驗收92景新插圖，按實際正文時間驗至少70%插畫、字卡最多連3，render／靜態運鏡／實際時長配樂／assemble／繁中燒錄及可關閉CC，5秒片頭在濃縮開場後、21秒正式v4片尾，再完整解碼及音畫／字幕／品牌QA、final審核與上傳包。

後台八語已真實選metadata／CC／dub，見`backend-language-choice.json`。文字可先備，實際CC須沿真實時間軸；clean國際主片依`variants/clean-master/`從相同已驗素材另外本機輸出，不重買整集圖像／音訊或繼承另一MP4的final核准。實際clean完整QA及目前final核准後才進八語配音、時窗擬合與聽檢。沒有SRT／配音／成片完成宣稱，也沒有YouTube上傳或排程。


## 已採用的預告共圖計畫

本次[受控採用](visual-only-runtime-adoption.json)只更新已獨立核對的prompt／camera，source SHA為`8549eb766873b65cb3453d03edfb5c2d151a3a9209578f3383cdc321c9620a75`。官方劇本`d363a2d4486549ead4e444455df4af5f9e80d72693bf34fc91f028a851b2d884`及原approvals.json前後SHA完全相同；原native票仍Matches，不重抽、不造批准。既有八語文字、worksheets與review bytes未改，[明確source rebind](i18n/source-rebind-teaser-plan.json)保留原語意審核SHA，只承接相同旁白／metadata的既有TEXT_PASS；實際runtime0errors、9soft、0stale。

[正常report-only實讀](report-only-teaser-plan-readback.json)確認既有後台story、八語與原決定時間不變，沒有提交新審核或寫批准。官方upsert只替未分類影片設定category，不覆寫已有owner選擇；renderer category explainer用於既有合法資料卡，仍不得繞品牌故事clean/final/QA/dub要求。

[共圖計畫](image-reuse-plan.json)仍是planned、actual_same_asset_verified=false；runtime與媒體目錄production-handoff已保存相同計畫。原生CLI不強制pair，cache缺失會走新的付費派送；因此正式入場後，須先生成並驗收payoff，預告shot命令之前人工核live cache預期同key、實際已驗檔及SHA、完整參數均一致，缺任一項即停止，不能呼叫預告命令或啟動auto worker。任一端未驗收／seed或修正改變亦停整對；render前兩端選中及裁切後真檔bytes／SHA必須相同，兩context各驗收，帳本沒有重購。

舊clean配方／獨立收據已逐檔精確封存到`history/clean-master-before-teaser-image-plan`；新source只重新衍生純burnflag配方，variant SHA`9d20895acdd3675c3d9df8930468ad14e00fc131388f057c210d155067c3337c`，待新的獨立metadata審查。沒有實際clean影片、完整QA、final或配音資格。新[免費預檢](preflight-inputs.json)仍不是全片報價；不嘗試真正TTS，所有付費保護維持。


## 後續獨立的真企劃批准匯入

圖像採用當時批准檔前後不變的收據保持原樣。其後，正式後台的企劃review `b82ea00f-85da-4cc9-92d8-a654e08ea09b`、brief SHA `c3eb5e30f27880ddbeb890ea9983b8c0c3d2189ccc3861ebd2f7c75dc022613c`、實際決定時間 `2026-10-26T00:07:53.166579Z` 已由官方 `review-pull --gate outline` exit0匯入；[獨立匯入收據](outline-approval-import.json)保存新動作的批准前後SHA與CLI輸出。這不是新增owner決定或圖像／媒體批准；script、字典、八語及原票不變，製片預算hold未解除，未執行真正TTS。


## 正式v4素材已就緒（PR1860）

正式站current的`mokaair-brand-package-v4-endscreen`已下載、安裝到共同mediaBASE；package hash `416c8768d4d29f2e746a0c019d2d598ec367cbb66b0ff996841c523651a63e88`，5秒／150格片頭與21秒／630格片尾皆完成SHA、規格及完整影音decode PASS。12集branding preflight既有快照均通過；本集快照source 8549eb766873b65cb3453d03edfb5c2d151a3a9209578f3383cdc321c9620a75，與此次手交接的current source吻合。品牌素材身份與取得已解阻，這是素材驗證，不是故事成片QA或付費入場。

全批權威：[required-branding.json](../branding-pr1860/required-branding.json)、[下載與QA／執行說明](../branding-pr1860/README.md)、[逐集快照](../branding-pr1860/project-preflights.json)。合成前須以本集最新runtime及slug重跑[唯讀preflight](../branding-pr1860/preflight.mjs)，正式站無法讀取、素材缺檔、disabled或版本／hash不符即停止；不能接受警告後無片頭繼續，也不能借其他系列包。

真正正文與其他必要製片關卡齊備後，依PR1860權威文件所列原生工具執行`assemble --intro-after-condensation`：**濃縮開場 → 5秒片頭 → 正文剩餘部分（含有聲CTA）→ 21秒片尾**。實聲正文仍須720–840秒，包含coldopen與口述CTA，只排額外bookends；片頭片尾另加26秒／780格，不用來填正文長度。實際字幕／章節／八語配音依真插入點處理其後+150格，片尾不殘留正文字幕。

本次只更新手交接，未建立單集production pin／timeline，沒有呼叫assemble或生成故事媒體。正常首次合成後才產生pin並驗實際總格數body+780、片頭接點、片尾音畫與字幕，再做完整解碼QA及新final審看。帳戶／歷史費用／全片報價／admission及真正TTS／實聲／故事畫面／成片QA仍依原關卡；`generated_story_media=0`、付費請求0，沒有新增owner決定或預算授權。
