# C07 Dr. Martens 正式製片續做

新slug `story-everyday-dr-martens-c07-remake-20261025`，source SHA `d2c90c26f028b01c3b03ee8c02368f1c35b8e31390643b7d5a71fb6fbc8a2805`，官方劇本SHA `104fd328f69068cb84d0de47284b1b08c2fa90a4f7bf94a3d4882f4372ddf112`。來源／書面配鏡與原生panel9合併PASS，企劃 `6da974aa-2b66-4e98-900c-0187b328e0c6` 與劇本 `38853f5f-8086-4493-aefd-81a772706286` 真實pending，正式批准後才以正常review-pull匯入，不沿用舊集／別集批准、不建立auto.json。

Runtime `/workspace/work/brand-story-20261025/c07-submission-root`，media base `/workspace/work/brand-story-20261025/media`；CLI --workdir傳base。自己的不可變字典正常初始化，官方screenplay、精確verify及原native票已核對搬入。runtime brief取[submission/brief.md](submission/brief.md)，來源原brief及其supporting SHA不動；送審後不可用prepare-runtime覆寫brief或之後的批准輸入。

八語意圖全metadata／CC／dub已授權；目前後台locales空白，需[合法管理設定](protected-admin-settings.json)並讀回真決定時間。八語各84句／6章與完整metadata已官方合併、獨立語意校對TEXT_PASS；共672句。仍無SRT、dub或語言輪，詳[i18n收據](i18n/preparation-status.json)。

付費入場沿[C03交接](../c03/production-entry.md)：精確新slug合法註冊、獨立帳戶、歷史用量／未結算、含評審／轉寫／配樂／重試的全片最壞報價、受保護啟用。US$25既有停線與C系列hold不變，泛US$200或catalog ready不是新授權，不借舊slug／帳本。

免費預檢84請求／2391計費字元，81圖景最多3次，US$1.09／3.28只為圖目錄估值，非全片報價。whole2123 units有明顯規劃風險，實聲未知；入場後先真TTS與逐句聽檢，目標13min、整份unwrapped narration720–840秒，含coldopen／有聲CTA，只排額外5秒片頭與21秒正式v4片尾。不慢播／加空白／重述填長，不把估算當實聲PASS。

## 共圖命令執行前的強制停線

[同圖sidecar](image-reuse-plan.json)已精確放到runtime及media production-handoff，只是planned，無actual accepted file/SHA。只有合法入場後才先產payoff首take並正常驗收、保持選中；預告命令前，操作者須讀live cache預期同key、實際存在的已驗檔bytes／SHA，及model／完整prompt／negative／seed／size／reference SHA／選圖版本／fixes全一致。**原生CLI不強制pair，cache miss會派送新付費請求；任一證據缺失或不同，必須在調用預告命令前停止，不能啟動auto worker。** 任一端judge未過、take／seed或fix改變即停整對核對，不另買相似圖冒充共圖。render前兩端真manifest選中及裁切後file SHA必須完全同，各context各正常judge；不得手造manifest或提前標actual_same_asset_verified。

[clean配方](variants/clean-master/derivation.json)只改burnflag，保持同source／新slug／ledger身分，繁中燒字幕與CC來源保留；待另一位獨立metadata審查，沒有clean影片。正式驗收素材才可共用輸出兩版，每個MP4各完整解碼／QA與相符final批准；clean版另有當前final及完整QA才可真八語dub／行窗／CC，不借另一輸出批准或重買同素材。全片QA、final、上傳與YouTube動作均未做。


## 正式v4素材已就緒（PR1860）

正式站current的`mokaair-brand-package-v4-endscreen`已下載、安裝到共同mediaBASE；package hash `416c8768d4d29f2e746a0c019d2d598ec367cbb66b0ff996841c523651a63e88`，5秒／150格片頭與21秒／630格片尾皆完成SHA、規格及完整影音decode PASS。12集branding preflight既有快照均通過；本集快照source d2c90c26f028b01c3b03ee8c02368f1c35b8e31390643b7d5a71fb6fbc8a2805，與此次手交接的current source吻合。品牌素材身份與取得已解阻，這是素材驗證，不是故事成片QA或付費入場。

全批權威：[required-branding.json](../branding-pr1860/required-branding.json)、[下載與QA／執行說明](../branding-pr1860/README.md)、[逐集快照](../branding-pr1860/project-preflights.json)。合成前須以本集最新runtime及slug重跑[唯讀preflight](../branding-pr1860/preflight.mjs)，正式站無法讀取、素材缺檔、disabled或版本／hash不符即停止；不能接受警告後無片頭繼續，也不能借其他系列包。

真正正文與其他必要製片關卡齊備後，依PR1860權威文件所列原生工具執行`assemble --intro-after-condensation`：**濃縮開場 → 5秒片頭 → 正文剩餘部分（含有聲CTA）→ 21秒片尾**。實聲正文仍須720–840秒，包含coldopen與口述CTA，只排額外bookends；片頭片尾另加26秒／780格，不用來填正文長度。實際字幕／章節／八語配音依真插入點處理其後+150格，片尾不殘留正文字幕。

本次只更新手交接，未建立單集production pin／timeline，沒有呼叫assemble或生成故事媒體。正常首次合成後才產生pin並驗實際總格數body+780、片頭接點、片尾音畫與字幕，再做完整解碼QA及新final審看。帳戶／歷史費用／全片報價／admission及真正TTS／實聲／故事畫面／成片QA仍依原關卡；`generated_story_media=0`、付費請求0，沒有新增owner決定或預算授權。
