# C19 正式製片續做

新slug `story-everyday-seven-bank-c19-remake-20261025`。本文件只同步已完成的品牌素材入場；稿件、來源、敘事、owner審核與其他製片狀態依各自收據，沒有在此宣稱通過。真正故事TTS、實聲時長、圖片、配樂、成片QA及final仍未完成；八語仍須依正式後台選擇及各語意／媒體關卡進行。

付費入場沿[C03交接](../c03/production-entry.md)：精確新slug帳戶、歷史費用與未結算、全片報價及受保護啟用仍須成立。既有US$25停線與C系列hold不變，品牌素材取得不是付費授權，不借舊slug／帳本或建立auto.json。


## 正式v4素材已就緒（PR1860）

正式站current的`mokaair-brand-package-v4-endscreen`已下載、安裝到共同mediaBASE；package hash `416c8768d4d29f2e746a0c019d2d598ec367cbb66b0ff996841c523651a63e88`，5秒／150格片頭與21秒／630格片尾皆完成SHA、規格及完整影音decode PASS。12集branding preflight既有快照均通過；本集快照source 314cafc2fbf4e06ebf4eee4ebfa1e6fb683fafffe5f002075fcbbafc6aa46dbe，與目前修訂source不同，最新稿須重新執行唯讀preflight，不能將舊快照冒充最新稿PASS。品牌素材身份與取得已解阻，這是素材驗證，不是故事成片QA或付費入場。

全批權威：[required-branding.json](../branding-pr1860/required-branding.json)、[下載與QA／執行說明](../branding-pr1860/README.md)、[逐集快照](../branding-pr1860/project-preflights.json)。合成前須以本集最新runtime及slug重跑[唯讀preflight](../branding-pr1860/preflight.mjs)，正式站無法讀取、素材缺檔、disabled或版本／hash不符即停止；不能接受警告後無片頭繼續，也不能借其他系列包。

真正正文與其他必要製片關卡齊備後，依PR1860權威文件所列原生工具執行`assemble --intro-after-condensation`：**濃縮開場 → 5秒片頭 → 正文剩餘部分（含有聲CTA）→ 21秒片尾**。實聲正文仍須720–840秒，包含coldopen與口述CTA，只排額外bookends；片頭片尾另加26秒／780格，不用來填正文長度。實際字幕／章節／八語配音依真插入點處理其後+150格，片尾不殘留正文字幕。

本次只更新手交接，未建立單集production pin／timeline，沒有呼叫assemble或生成故事媒體。正常首次合成後才產生pin並驗實際總格數body+780、片頭接點、片尾音畫與字幕，再做完整解碼QA及新final審看。帳戶／歷史費用／全片報價／admission及真正TTS／實聲／故事畫面／成片QA仍依原關卡；`generated_story_media=0`、付費請求0，沒有新增owner決定或預算授權。
