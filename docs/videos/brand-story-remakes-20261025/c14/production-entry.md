# C14 CamelBak 正式製片續做

全新slug `story-everyday-camelbak-c14-remake-20261025`，來源SHA `5a555ee4b1ac57f4a990a251a0336376d87d293500824771fe4e1c75f70525ea`，官方劇本SHA `7aca1f854cde265715340ba0218ef891584c9148a808d63a3864dae04a7a36f7`。來源／書面配鏡及原生敘事合併PASS；後台企劃 `7c6a0b46-a59f-4f4a-8906-d17978369674`、劇本 `31bcfffc-9281-43d3-92cc-332a62165c55` 真實pending，正式決定後用官方review-pull匯入，不沿用舊集或別集批准、不建立auto.json。

本機runtime `/workspace/work/brand-story-20261025/c14-submission-root`，媒體base `/workspace/work/brand-story-20261025/media`；CLI --workdir指向base。正常不可變字典已初始化，來源verify及原生合併narrative record精確核對搬入。runtime brief是[submission/brief.md](submission/brief.md)，來源綁定作者brief保持原樣；不要重跑prepare-runtime覆寫送審brief或之後的批准輸入。

八語已授權，實際後台locales空白，需[合法管理設定](protected-admin-settings.json)並讀回。worksheet已備，須全部翻譯、原生合併及非譯者獨立校對；沒有TEXT_PASS、SRT、配音或語言輪。

付費入場沿[C03主機交接](../c03/production-entry.md)：精確新版註冊、獨立帳戶、歷史用量與未結算、包含評審／轉寫／配樂／重試的全片最壞報價、受保護啟用。既有US$25停線及C系列hold不變，泛US$200上限不是授權；未嘗試付費TTS。

免費預檢75請求、2492計費字元，74圖景最多3次，US$1.00／3.00只為圖像目錄估值。whole narration 2168 units有顯著偏短規劃風險，實聲仍未知。正式入場後先TTS與逐句聽檢，目標13分鐘、實聲正文720–840秒，含coldopen和有聲CTA，只排額外5秒片頭／21秒正式v4片尾；不能慢播、停頓或重述填長，不能把規劃字量當時長PASS。

## 實際共圖的強制人工停線

[原始共圖計畫](asset-reuse-plan.json)只有書面PASS，actual_same_asset_verified=false。runtime與媒體工作目錄production-handoff已放同一SHA計畫。只有正式付費入場後才可先生成payoff；首take須正常通過、保持選中，再以完全相同model／完整prompt／negative／seed／size／reference SHA／選圖版本／修正參數重用。原生CLI不執行pair限制，cache miss或缺檔會走新provider派送。**因此預告shot命令執行前必須人工讀取live cache，確認預期同key、真實存在且SHA吻合的已驗檔；任一條件不明就停止，不呼叫該命令，不啟動auto worker。** 任一端judge失敗、取景或seed改變亦停止整對核對，不單端另買圖。

原生同key或相同prompt不代表實際同圖，裁切還可能產生不同檔；render前須讀兩端真manifest assignment、實際選中／裁切後圖bytes與SHA完全相同，兩context各驗收且ledger沒有重購。不能手造manifest、把另一張相似圖稱共用或標actual verified。

繁中燒字幕／CC來源保留。[clean配方](variants/clean-master/derivation.json)只改燒錄旗標，須共用實際已驗素材及同一帳本。每個MP4均需完整解碼、精確QA與final批准；clean另有相符final後才做八語dub、行窗與CC，不能借另一輸出／舊片批准。


## 正式v4素材已就緒（PR1860）

正式站current的`mokaair-brand-package-v4-endscreen`已下載、安裝到共同mediaBASE；package hash `416c8768d4d29f2e746a0c019d2d598ec367cbb66b0ff996841c523651a63e88`，5秒／150格片頭與21秒／630格片尾皆完成SHA、規格及完整影音decode PASS。12集branding preflight既有快照均通過；本集快照source 5a555ee4b1ac57f4a990a251a0336376d87d293500824771fe4e1c75f70525ea，與此次手交接的current source吻合。品牌素材身份與取得已解阻，這是素材驗證，不是故事成片QA或付費入場。

全批權威：[required-branding.json](../branding-pr1860/required-branding.json)、[下載與QA／執行說明](../branding-pr1860/README.md)、[逐集快照](../branding-pr1860/project-preflights.json)。合成前須以本集最新runtime及slug重跑[唯讀preflight](../branding-pr1860/preflight.mjs)，正式站無法讀取、素材缺檔、disabled或版本／hash不符即停止；不能接受警告後無片頭繼續，也不能借其他系列包。

真正正文與其他必要製片關卡齊備後，依PR1860權威文件所列原生工具執行`assemble --intro-after-condensation`：**濃縮開場 → 5秒片頭 → 正文剩餘部分（含有聲CTA）→ 21秒片尾**。實聲正文仍須720–840秒，包含coldopen與口述CTA，只排額外bookends；片頭片尾另加26秒／780格，不用來填正文長度。實際字幕／章節／八語配音依真插入點處理其後+150格，片尾不殘留正文字幕。

本次只更新手交接，未建立單集production pin／timeline，沒有呼叫assemble或生成故事媒體。正常首次合成後才產生pin並驗實際總格數body+780、片頭接點、片尾音畫與字幕，再做完整解碼QA及新final審看。帳戶／歷史費用／全片報價／admission及真正TTS／實聲／故事畫面／成片QA仍依原關卡；`generated_story_media=0`、付費請求0，沒有新增owner決定或預算授權。
