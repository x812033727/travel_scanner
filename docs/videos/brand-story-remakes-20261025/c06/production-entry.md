# C06 正式製片續做

此交接指向全新 `story-everyday-play-doh-c06-remake-20261025`，來源video SHA `aac065fb5663fd1a75dbac064470ceaefea43eac08a162ba3be96d9130724d11`，官方劇本SHA `e00fd07d54ef284a5577327f999f4e46222aef455417f3fc878c1a91f11b124e`。

[來源／書面配鏡](reviews/source-r3-independent.json)、[雙讀者合併](reviews/narrative-final.json)及[八語文字](i18n/preparation-status.json)均通過。雙讀者各自的保留意見仍保留。劇本 `3d8ed292-ea12-4bfd-98b8-097acda4a828` 已於2026-10-25T23:42:51Z獲核准，官方review-pull已匯入精確canonical SHA；本次唯讀已確認企劃 `cf42c3a1-f54b-4295-934e-f4d6fa0ee163` 為approved；圖像採用步驟的批准檔保持不變，其後另以正常review-pull匯入這份真實owner決定，獨立收據見`outline-approval-import.json`。企劃與原script現在都已匯入。不得沿用舊集批准或自行建立auto.json。

後台分類已由外部操作改為story，八語metadata／CC／dub也已全選；[正式讀回](backend-language-choice.json)保存實際決定時間。先前待管理設定在[交接收據](protected-admin-settings.json)標記為外部套用並已讀回，本代理未取得或假造content.manage權限。server的dub_allowed欄位不是實際clean成片資格。

付費入場沿[C03正式主機交接](../c03/production-entry.md)，須精確新slug註冊、獨立帳戶、歷史用量／未結算及全片最壞報價、受保護啟用。既有US$25停線與C系列hold不變，不借舊slug或站點US$200泛上限放行。

本版免費TTS預檢150請求、4086計費字元；圖像137景、每景含首次最多3次，圖像階段約US$1.85／5.55。這些不是全片報價，未含完整轉寫、評審、配樂、重試及歷史費用，沒有實際生成。原生全旁白3428units及排開場分項3229units也不證明時長；入場後先合成與逐句聽檢，實測自然語速正文720–840秒再鎖分鏡／配樂，不能靠停頓或慢播補長。

繁中燒錄來源保留。[clean-master](variants/clean-master/derivation.json)僅是未執行配方，獨立審查只確認metadata差分及原生輸入hash。須共用真實已驗素材分別輸出、完整解碼及QA，clean輸出重新取得匹配的final批准，才開始真實八語配音、行窗調整與CC。未有媒體QA、final或YouTube上傳。

本次已用新的獨立category-delta證據，將來源圖像計畫及renderer category story受控採用到既有runtime；旁白與官方劇本完全不變，批准原檔未寫入。已核HEAD及origin/main API contract：正常report只在後台未分類時設定category，既有owner story分類會保留，無須自訂omission或呼叫protectedadmin。正常report-only後GET也確認story、八語原決定與reviews未變。


## 已採用的預告共圖計畫

本次[受控採用](visual-only-runtime-adoption.json)只更新已獨立核對的prompt／camera及renderer category metadata，source SHA為`aac065fb5663fd1a75dbac064470ceaefea43eac08a162ba3be96d9130724d11`。官方劇本`e00fd07d54ef284a5577327f999f4e46222aef455417f3fc878c1a91f11b124e`及原approvals.json前後SHA完全相同；原native票仍Matches，不重抽、不造批准。既有八語文字、worksheets與review bytes未改，[明確source rebind](i18n/source-rebind-teaser-plan.json)保留原語意審核SHA，只承接相同旁白／metadata的既有TEXT_PASS；實際runtime0errors、19soft、0stale。

[正常report-only實讀](report-only-teaser-plan-readback.json)確認既有後台story、八語與原決定時間不變，沒有提交新審核或寫批准。官方upsert只替未分類影片設定category，不覆寫已有owner選擇；renderer category story與已核來源metadata一致。

[共圖計畫](image-reuse-plan.json)仍是planned、actual_same_asset_verified=false；runtime與媒體目錄production-handoff已保存相同計畫。原生CLI不強制pair，cache缺失會走新的付費派送；因此正式入場後，須先生成並驗收payoff，預告shot命令之前人工核live cache預期同key、實際已驗檔及SHA、完整參數均一致，缺任一項即停止，不能呼叫預告命令或啟動auto worker。任一端未驗收／seed或修正改變亦停整對；render前兩端選中及裁切後真檔bytes／SHA必須相同，兩context各驗收，帳本沒有重購。

舊clean配方／獨立收據已逐檔精確封存到`history/clean-master-before-teaser-image-plan`；新source只重新衍生純burnflag配方，variant SHA`977fb6e41b11abd5ef161924f29036ea005fd4a920996a0bc0f7a6c8b47c6bdb`，待新的獨立metadata審查。沒有實際clean影片、完整QA、final或配音資格。新[免費預檢](preflight-inputs.json)仍不是全片報價；不嘗試真正TTS，所有付費保護維持。


## 後續獨立的真企劃批准匯入

圖像採用當時批准檔前後不變的收據保持原樣。其後，正式後台的企劃review `cf42c3a1-f54b-4295-934e-f4d6fa0ee163`、brief SHA `b0ce1bf0f44699cfcf68b9381bfd58813dd07a973b13ed3509348ed4944cb95d`、實際決定時間 `2026-10-25T23:55:27.437521Z` 已由官方 `review-pull --gate outline` exit0匯入；[獨立匯入收據](outline-approval-import.json)保存新動作的批准前後SHA與CLI輸出。這不是新增owner決定或圖像／媒體批准；script、字典、八語及原票不變，製片預算hold未解除，未執行真正TTS。


## 正式v4素材已就緒（PR1860）

正式站current的`mokaair-brand-package-v4-endscreen`已下載、安裝到共同mediaBASE；package hash `416c8768d4d29f2e746a0c019d2d598ec367cbb66b0ff996841c523651a63e88`，5秒／150格片頭與21秒／630格片尾皆完成SHA、規格及完整影音decode PASS。12集branding preflight既有快照均通過；本集快照source aac065fb5663fd1a75dbac064470ceaefea43eac08a162ba3be96d9130724d11，與此次手交接的current source吻合。品牌素材身份與取得已解阻，這是素材驗證，不是故事成片QA或付費入場。

全批權威：[required-branding.json](../branding-pr1860/required-branding.json)、[下載與QA／執行說明](../branding-pr1860/README.md)、[逐集快照](../branding-pr1860/project-preflights.json)。合成前須以本集最新runtime及slug重跑[唯讀preflight](../branding-pr1860/preflight.mjs)，正式站無法讀取、素材缺檔、disabled或版本／hash不符即停止；不能接受警告後無片頭繼續，也不能借其他系列包。

真正正文與其他必要製片關卡齊備後，依PR1860權威文件所列原生工具執行`assemble --intro-after-condensation`：**濃縮開場 → 5秒片頭 → 正文剩餘部分（含有聲CTA）→ 21秒片尾**。實聲正文仍須720–840秒，包含coldopen與口述CTA，只排額外bookends；片頭片尾另加26秒／780格，不用來填正文長度。實際字幕／章節／八語配音依真插入點處理其後+150格，片尾不殘留正文字幕。

本次只更新手交接，未建立單集production pin／timeline，沒有呼叫assemble或生成故事媒體。正常首次合成後才產生pin並驗實際總格數body+780、片頭接點、片尾音畫與字幕，再做完整解碼QA及新final審看。帳戶／歷史費用／全片報價／admission及真正TTS／實聲／故事畫面／成片QA仍依原關卡；`generated_story_media=0`、付費請求0，沒有新增owner決定或預算授權。
