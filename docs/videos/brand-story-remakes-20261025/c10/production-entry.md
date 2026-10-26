# C10 正式製片續做

全新slug `story-everyday-oxo-c10-remake-20261025`，來源SHA `637c8cce6426341d8612b2443089556cbfc2b67d415d1d726bc559999a2d307f`，官方劇本SHA `1fa2d25a0161b8ed0e4638fbaf8d982cc1dbf5717e9300cd2d121e43b0a29082`。來源／書面配鏡及原生敘事合併PASS，canonical lint0errors；後台企劃 `6de185a0-c301-4ad1-843f-d2cc0d4765ba` 與劇本 `1c9895e6-4de2-4ed8-b869-d315efecdba6` 已真實讀回approved並在圖像採用之後另以官方review-pull精確匯入，見approval-import-chain.json，不沿用原集或別集批准，不建立auto.json。

本機runtime `/workspace/work/brand-story-20261025/c10-submission-root`，媒體base `/workspace/work/brand-story-20261025/media`；CLI --workdir指向base，不是slug目錄。正常不可變字典已初始化，精確來源verify及原生合併narrative record已核對並搬入。不要搬別集字典／approved檔案，不自行重置原生歷史。

八語預設已授權；實際後台locales空白，需[合法管理設定](protected-admin-settings.json)並讀回。文字worksheet已備，須全部翻譯、原生合併及非譯者獨立文字校對；目前沒有TEXT_PASS、時間軸、SRT、配音或語言輪。

付費入場沿[C03主機交接](../c03/production-entry.md)，需要精確新版註冊、獨立帳戶、歷史用量與未結算、包含評審／轉寫／配樂／重試的全片最壞報價、受保護啟用。既有US$25停線及C系列hold不變；圖像預檢顯示的泛US$200上限不代表授權。沒有嘗試付費TTS或繞路。

本版免費TTS預檢118請求、3038計費字元，圖像115景、每景最多3次，US$1.55／4.66只為圖像目錄估值。正式入場後先TTS及逐句聽檢；目標13分鐘，整份unwrapped實聲正文720–840秒，包含coldopen與有聲CTA，只排額外5秒片頭及21秒正式v4片尾。2670 spokenUnits與紙上時間線不算時長PASS，不靠慢播、沉默或重述補長。

繁中燒字幕與CC的來源保留。[clean配方](variants/clean-master/derivation.json)只改燒錄旗標，共用真實驗收主素材與同一帳本；現在沒有clean影片、媒體QA或final。完成實際輸出後，每個MP4須完整解碼及精確QA，clean版另取得相符的final批准才做八語dub、行窗與CC。不沿用另一輸出或舊片批准，不重買相同素材。


## 已採用的預告共圖計畫

本次[受控採用](visual-only-runtime-adoption.json)只更新已獨立核對的prompt／camera，source SHA為`637c8cce6426341d8612b2443089556cbfc2b67d415d1d726bc559999a2d307f`。官方劇本`1fa2d25a0161b8ed0e4638fbaf8d982cc1dbf5717e9300cd2d121e43b0a29082`及原approvals.json前後SHA完全相同；原native票仍Matches，不重抽、不造批准。八語現已完整翻譯、官方合併及獨立語意校對TEXT_PASS，共944句／48章；採用時的source blanks及source欄位SHA證據保留，後續只填text。config的full source SHA已受控更新。 [source rebind收據](i18n/source-rebind-teaser-plan.json)完整保存；實際runtime0errors、2soft、0stale。

[正常report-only實讀](report-only-teaser-plan-readback.json)確認既有後台story、八語與原決定時間不變，沒有提交新審核或寫批准。官方upsert只替未分類影片設定category，不覆寫已有owner選擇；renderer category story與已核來源metadata一致。

[共圖計畫](image-reuse-plan.json)仍是planned、actual_same_asset_verified=false；runtime與媒體目錄production-handoff已保存相同計畫。原生CLI不強制pair，cache缺失會走新的付費派送；因此正式入場後，須先生成並驗收payoff，預告shot命令之前人工核live cache預期同key、實際已驗檔及SHA、完整參數均一致，缺任一項即停止，不能呼叫預告命令或啟動auto worker。任一端未驗收／seed或修正改變亦停整對；render前兩端選中及裁切後真檔bytes／SHA必須相同，兩context各驗收，帳本沒有重購。

舊clean配方／獨立收據已逐檔精確封存到`history/clean-master-before-teaser-image-plan`；新source只重新衍生純burnflag配方，variant SHA`92f8b08788006ca8386bef90364b404e9830a2abcb2a78fc5e22a64ae2cbf635`，待新的獨立metadata審查。沒有實際clean影片、完整QA、final或配音資格。新[免費預檢](preflight-inputs.json)仍不是全片報價；不嘗試真正TTS，所有付費保護維持。


## 圖像採用之後的真實批准匯入

採用守衛收據保持當時批准檔存在性／SHA前後不變；其後才依真後台決定，分別用官方review-pull匯入精確script及outline。獨立[import chain](approval-import-chain.json)保存每一步review ID、真decided時間、內容SHA、CLI輸出與批准檔前後SHA。當前兩關均已匯入，不新增owner決定、不批准圖片或媒體；字典、canonical與既有語言文字不變。後GET分類story及語言原決定仍不變，預算hold不改，沒有真正TTS。


## 正式v4素材已就緒（PR1860）

正式站current的`mokaair-brand-package-v4-endscreen`已下載、安裝到共同mediaBASE；package hash `416c8768d4d29f2e746a0c019d2d598ec367cbb66b0ff996841c523651a63e88`，5秒／150格片頭與21秒／630格片尾皆完成SHA、規格及完整影音decode PASS。12集branding preflight既有快照均通過；本集快照source 637c8cce6426341d8612b2443089556cbfc2b67d415d1d726bc559999a2d307f，與此次手交接的current source吻合。品牌素材身份與取得已解阻，這是素材驗證，不是故事成片QA或付費入場。

全批權威：[required-branding.json](../branding-pr1860/required-branding.json)、[下載與QA／執行說明](../branding-pr1860/README.md)、[逐集快照](../branding-pr1860/project-preflights.json)。合成前須以本集最新runtime及slug重跑[唯讀preflight](../branding-pr1860/preflight.mjs)，正式站無法讀取、素材缺檔、disabled或版本／hash不符即停止；不能接受警告後無片頭繼續，也不能借其他系列包。

真正正文與其他必要製片關卡齊備後，依PR1860權威文件所列原生工具執行`assemble --intro-after-condensation`：**濃縮開場 → 5秒片頭 → 正文剩餘部分（含有聲CTA）→ 21秒片尾**。實聲正文仍須720–840秒，包含coldopen與口述CTA，只排額外bookends；片頭片尾另加26秒／780格，不用來填正文長度。實際字幕／章節／八語配音依真插入點處理其後+150格，片尾不殘留正文字幕。

本次只更新手交接，未建立單集production pin／timeline，沒有呼叫assemble或生成故事媒體。正常首次合成後才產生pin並驗實際總格數body+780、片頭接點、片尾音畫與字幕，再做完整解碼QA及新final審看。帳戶／歷史費用／全片報價／admission及真正TTS／實聲／故事畫面／成片QA仍依原關卡；`generated_story_media=0`、付費請求0，沒有新增owner決定或預算授權。
