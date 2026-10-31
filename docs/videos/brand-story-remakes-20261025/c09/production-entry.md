# C09 R7 正式製片續做

新稿仍使用 `story-everyday-patagonia-c09-remake-20261025`，未重綁原episode。source video `1912082c8c1ecc0d2bab399903bde0e6f2a203cc3aac7487519ec3bbc26cc222`；官方劇本 `02f091cae8f4e6179364155ef489b8ae59839efd969b695d21971d7b1ab5e3de`。canonical在隔離submission-root，不可再以全新專案準備程式覆寫已保存的審核歷史。

企劃review `5199b233-c1ee-4970-ae11-af9115cbbde9`，劇本review `6a441762-8d88-45b7-adff-78b5c3ef1260`，最新正式讀回均approved，並在圖像採用後另以普通review-pull精確匯入，見approval-import-chain.json；舊05470603劇本的批准只屬封存基底。當前source與原生兩讀者紀錄已匹配，不自行建立auto.json。

[八語選擇讀回](backend-language-choice.json)保存既有8語metadata／CC／dub=true與真實決定時間。新稿824句文字全部獨立TEXT_PASS，不表示定時字幕、配音或clean final已存在。實際配音仍要求目前核准的clean成片及完整綁檔QA，不得依選擇旗標跳關。

付費入場沿[C03主機交接](../c03/production-entry.md)：精確新slug註冊及獨立帳戶、歷史用量／未結算、包含轉寫／評審／配樂／重試的全片最壞報價、受保護啟用均須成立。既有US$25停線與C系列hold不變，圖像預檢US$4.09不是全片授權，站點US$200泛上限也不是本批預算。

正式入場後先做真實TTS與逐句聽檢，實測自然語速正文720–840秒，再鎖分鏡及配樂；目前全旁白2916 units（排開場規劃分項2737）有規劃風險，不能用估秒、額外停頓或慢播代替。若實聲不符，先補正確內容並重新走受影響審核，圖像採購須等聲音鎖定。當前免費預檢102請求／3298計費字元、101插畫景均未生成。

繁中燒錄來源保持不變。[clean配方](variants/clean-master/derivation.json)只改字幕旗標，與同一新slug共用已驗音訊、插畫及混音輸入；還沒有clean MP4。實際兩版輸出分別完整解碼／QA，clean輸出重新取得相符final後才做八語真配音、行窗與CC。正式5秒片頭與21秒v4片尾原件已取得並通過素材QA；正文實長、手機縮圖、片頭片尾實際接點及故事成片仍待實作／實測。


## 已採用的預告共圖計畫

本次[受控採用](visual-only-runtime-adoption.json)只更新已獨立核對的prompt／camera，source SHA為`1912082c8c1ecc0d2bab399903bde0e6f2a203cc3aac7487519ec3bbc26cc222`。官方劇本`02f091cae8f4e6179364155ef489b8ae59839efd969b695d21971d7b1ab5e3de`及原approvals.json前後SHA完全相同；原native票仍Matches，不重抽、不造批准。既有八語文字、worksheets與review bytes未改，明確source rebind保留原語意審核SHA，承接相同旁白／metadata的既有TEXT_PASS。 [source rebind收據](i18n/source-rebind-teaser-plan.json)完整保存；實際runtime0errors、12soft、0stale。

[正常report-only實讀](report-only-teaser-plan-readback.json)確認既有後台story、八語與原決定時間不變，沒有提交新審核或寫批准。官方upsert只替未分類影片設定category，不覆寫已有owner選擇；renderer category explainer用於既有合法資料卡，仍不得繞品牌故事clean/final/QA/dub要求。

[共圖計畫](image-reuse-plan.json)仍是planned、actual_same_asset_verified=false；runtime與媒體目錄production-handoff已保存相同計畫。原生CLI不強制pair，cache缺失會走新的付費派送；因此正式入場後，須先生成並驗收payoff，預告shot命令之前人工核live cache預期同key、實際已驗檔及SHA、完整參數均一致，缺任一項即停止，不能呼叫預告命令或啟動auto worker。任一端未驗收／seed或修正改變亦停整對；render前兩端選中及裁切後真檔bytes／SHA必須相同，兩context各驗收，帳本沒有重購。

舊clean配方／獨立收據已逐檔精確封存到`history/clean-master-before-teaser-image-plan`；新source只重新衍生純burnflag配方，variant SHA`91926eda9724e501ed92ecffe12befda9e8d2ab13b8546fdc7d300ceecd87b91`，待新的獨立metadata審查。沒有實際clean影片、完整QA、final或配音資格。新[免費預檢](preflight-inputs.json)仍不是全片報價；不嘗試真正TTS，所有付費保護維持。


## 圖像採用之後的真實批准匯入

採用守衛收據保持當時批准檔存在性／SHA前後不變；其後才依真後台決定，分別用官方review-pull匯入精確script及outline。獨立[import chain](approval-import-chain.json)保存每一步review ID、真decided時間、內容SHA、CLI輸出與批准檔前後SHA。當前兩關均已匯入，不新增owner決定、不批准圖片或媒體；字典、canonical與既有語言文字不變。後GET分類story及語言原決定仍不變，預算hold不改，沒有真正TTS。


## 正式v4素材已就緒（PR1860）

正式站current的`mokaair-brand-package-v4-endscreen`已下載、安裝到共同mediaBASE；package hash `416c8768d4d29f2e746a0c019d2d598ec367cbb66b0ff996841c523651a63e88`，5秒／150格片頭與21秒／630格片尾皆完成SHA、規格及完整影音decode PASS。12集branding preflight既有快照均通過；本集快照source 1912082c8c1ecc0d2bab399903bde0e6f2a203cc3aac7487519ec3bbc26cc222，與此次手交接的current source吻合。品牌素材身份與取得已解阻，這是素材驗證，不是故事成片QA或付費入場。

全批權威：[required-branding.json](../branding-pr1860/required-branding.json)、[下載與QA／執行說明](../branding-pr1860/README.md)、[逐集快照](../branding-pr1860/project-preflights.json)。合成前須以本集最新runtime及slug重跑[唯讀preflight](../branding-pr1860/preflight.mjs)，正式站無法讀取、素材缺檔、disabled或版本／hash不符即停止；不能接受警告後無片頭繼續，也不能借其他系列包。

真正正文與其他必要製片關卡齊備後，依PR1860權威文件所列原生工具執行`assemble --intro-after-condensation`：**濃縮開場 → 5秒片頭 → 正文剩餘部分（含有聲CTA）→ 21秒片尾**。實聲正文仍須720–840秒，包含coldopen與口述CTA，只排額外bookends；片頭片尾另加26秒／780格，不用來填正文長度。實際字幕／章節／八語配音依真插入點處理其後+150格，片尾不殘留正文字幕。

本次只更新手交接，未建立單集production pin／timeline，沒有呼叫assemble或生成故事媒體。正常首次合成後才產生pin並驗實際總格數body+780、片頭接點、片尾音畫與字幕，再做完整解碼QA及新final審看。帳戶／歷史費用／全片報價／admission及真正TTS／實聲／故事畫面／成片QA仍依原關卡；`generated_story_media=0`、付費請求0，沒有新增owner決定或預算授權。
