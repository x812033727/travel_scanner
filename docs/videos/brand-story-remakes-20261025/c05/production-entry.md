# C05 R13 接續製片

現行來源SHA `773836e4a9c63770afbd6900014cbd57e6b123df44a22dca5987afaf9488d546`，官方劇本SHA `3f2f19c4989a33f0887331997e29ae505839726fb8079ceb0607511593835c80`，來源／書面配鏡／同圖計畫及actual native12合併PASS。實際immutable字典情境0errors；八語拆句每語2條delta待補與非譯者覆核，不能把舊864句宣稱新109句全current。

新劇本review `7eda9d94-62a3-4cd2-9bfe-5cdc48341126`、企劃 `3f9e948c-8a95-43de-bbb9-d06d45a4cb2a`目前真實讀回pending。R12 script67bd…的批准不適用R13；本輪approved media approvals.json ef6e1cae…逐byte不變，沒有import新批准或造auto。source brief保持1f528e…，送審format另存submission/brief.md（SHA8e7cde…）。

共用新slug `story-everyday-kincho-c05-remake-20261025` 與同一帳本身分；現有C系列hold、原US$25停線不變。正式入場須依[C03交接](../c03/production-entry.md)實際讀回精確帳戶、歷史reserved／uncertain／settled、全片價格及受保護啟用。目錄泛US$200不等於授權。現有工具token有效，沒有可操作正式主機／管理連線；不得改slug前綴或借原集帳戶繞過。

免費預檢107 TTS請求、3454計費字元；106圖景目錄估價一輪US$1.43、含首輪最多3次US$4.29，不是含歷史費用、語音／轉寫／評審／音樂／重試的全片報價。未做真實TTS、圖、配樂或影片。正式入場及新稿精確核准後，先量整份unwrapped實聲720–840秒（含冷開場、有聲CTA，只排另外5秒intro與21秒正式v4outro）與逐句聽檢，不能靠慢播、停頓或字量冒充PASS。

[同圖計畫](image-reuse-plan.json)與runtime／work production-handoff相同。原生CLI不強制pair且cache miss會派送付費請求：正式payoff先單次生成並驗收，第二teaser命令之前必須檢查完整request/key與已存在livecache實檔SHA；缺漏或不一致必停，不能讓CLI另買相似圖。兩端仍各自judge，任何retake／選圖／裁切差異須停止成對核對；render前比較最終manifest及實檔SHA完全相同。當前actual_same_asset_verified=false，沒有圖。

後台story分類、八語metadata／CC／dub全選與2026-10-25T11:29:01.252022Z原決定時間已再讀回且未變。本地render分類沿已驗原source explainer，series.kind仍story；後台既有分類由正式report契約保留。不得借render分類繞過品牌故事配音規則。clean-master只有純burn旗標未執行配方，須共用真實已驗資產另輸出、全片解碼QA及匹配當前clean final批准，才能進配音／真正timed CC與語言輪。沒有成片QA、final、實際配音或YouTube變更。


## 正式v4素材已就緒（PR1860）

正式站current的`mokaair-brand-package-v4-endscreen`已下載、安裝到共同mediaBASE；package hash `416c8768d4d29f2e746a0c019d2d598ec367cbb66b0ff996841c523651a63e88`，5秒／150格片頭與21秒／630格片尾皆完成SHA、規格及完整影音decode PASS。12集branding preflight既有快照均通過；本集快照source 773836e4a9c63770afbd6900014cbd57e6b123df44a22dca5987afaf9488d546，與此次手交接的current source吻合。品牌素材身份與取得已解阻，這是素材驗證，不是故事成片QA或付費入場。

全批權威：[required-branding.json](../branding-pr1860/required-branding.json)、[下載與QA／執行說明](../branding-pr1860/README.md)、[逐集快照](../branding-pr1860/project-preflights.json)。合成前須以本集最新runtime及slug重跑[唯讀preflight](../branding-pr1860/preflight.mjs)，正式站無法讀取、素材缺檔、disabled或版本／hash不符即停止；不能接受警告後無片頭繼續，也不能借其他系列包。

真正正文與其他必要製片關卡齊備後，依PR1860權威文件所列原生工具執行`assemble --intro-after-condensation`：**濃縮開場 → 5秒片頭 → 正文剩餘部分（含有聲CTA）→ 21秒片尾**。實聲正文仍須720–840秒，包含coldopen與口述CTA，只排額外bookends；片頭片尾另加26秒／780格，不用來填正文長度。實際字幕／章節／八語配音依真插入點處理其後+150格，片尾不殘留正文字幕。

本次只更新手交接，未建立單集production pin／timeline，沒有呼叫assemble或生成故事媒體。正常首次合成後才產生pin並驗實際總格數body+780、片頭接點、片尾音畫與字幕，再做完整解碼QA及新final審看。帳戶／歷史費用／全片報價／admission及真正TTS／實聲／故事畫面／成片QA仍依原關卡；`generated_story_media=0`、付費請求0，沒有新增owner決定或預算授權。
