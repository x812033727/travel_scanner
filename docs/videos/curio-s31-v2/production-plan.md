# S31 新規則版製作與報價（2026-10-26）

新稿：[script.md](script.md)。原標題保留，使用獨立 slug `curio-s31-v2`。原版 `curio-s31` 的成片、旁白、插圖、外語及核准仍歸原工作與 PR #1800；本次不覆寫它們。

## 當前讀回（2026-10-27）

最新 checkpoint（2026-10-27）：冷卻後的獨立續作 `dub-en-quality-retake1-after-busy1`（82113／PID57648）於15:34:08.1485986Z native4結束，仍是5次429 `video_speech_upstream_busy`。**獨立對帳及Root讀回確認212 raw未變（29目標／183其他皆0 changed），102項來源／mix／fit／timeline／cache／check／approval／state與82份journal全SHA保留，active／uncertain 0、PID已退出、無lease。plain仍0/2，0/8配音接受。** 最早 **2026-10-27T16:35:00Z（台北10/28 00:35）** 才可重新核對，已較前次延長至至少60分鐘；此前只讀觀察，不重播任一舊slot。15:26:30Z官方quota快照仍為5,157,762，涵蓋29 requests／1,251字元，但不能證明供應商當日額度可用，也無收據可宣稱零費用。下次須fresh quota／來源／lease／journal與實際剩餘句子。見[第二次限流對帳](dub-en-quality-retake1-provider-busy2.json)；兩次原始紀錄完整保留。完整包尚未完成，S15尚未開始。

窄診斷：[私有 final-diagnosis.md](C:/Users/x8120/mokaair-work/curio-s31-v2-preflight/rename-native-diagnostic-20261027/final-diagnosis.md)，SHA256 `fa648dfc294921661b21f98f795d5f3ef16002325f1358c0d8dd0948fe441f86`。本機fixture可重現EPERM，但未證實production持鎖來源或UTF8因果；沒有OS改動或上限變更。Transport observer只涵蓋synthesis，舊absolute-path配置未啟用；空檔／缺席不能證明ASR無HTTP錯誤。

**歷史快照：以下 running、最新、待核對等文字均描述當時狀態，不得用來判斷目前程序；目前狀態以上段為準。**

最新 checkpoint（2026-10-27）：97854／PID15272已於14:34:07.6598357Z native1結束，這次是**首次完整EN音訊檢查的29個品質flags，不是journal故障**。212/212＝148 exact＋13 Jev通過＋22 second解除＋29 flags；本輪22個新ASR、3次Jev及1個保存答案沿用，primary Jev累計64、second transcript共51。695b／lz514實際沿用已獨立確認，舊189筆primary／語意欄位保留，noul／second新增另列；active journal 0、82份歷史證據與舊take已凍結。**第一輪原文重錄準備，尚無producer；0/8 accepted。** 29 requests／1251官方billable字元僅離線規劃，plain 0/2、shorten 0、listener 0；14:51:49.2388142Z官方dry-run native0已讀Gemini ready／remaining 5,157,762，足夠實際29 requests／1251 billable；681次fresh checks（非unique檔數）。Root按授權準備獨立付費slot，尚未dispatch，quota只是快照並非保留額度。官方dry-run會忽略redo而報0，不能拿它代替本次實算。Second runtime獨立覆核PASS：51 subset的raw／完整實際轉寫／cache全SHA一致，nativeWhisper0／390.379s、callback396.399s，4CPU／nice19／offline／no hints；本機child close0／reaped及三PID已退出，無holds／uncertain／lease。遠端scratch刪除未證，state／runs保留未archive；無runtime阻擋另行TTS，仍非音訊核准。見[dub-en-first-check-complete.json](dub-en-first-check-complete.json)；完整包及下一集未成。

最新續作入口：2026-10-27T14:25:29.6516650Z。第八筆695b／lz514已逐筆恢復覆核，Root fresh573次SHA核對：current/private各212raw、三方cache189及原170全保留、76preserved＋3active＝79精確journal會員、21present／1absent、terms0及來源／lexicon／unused EN binding一致；原PID27636 dead且無競爭程序／lease／STOP／ASRstate。**唯一正常續檢session97854／PID15272執行中**，slot check-en-saved-answer8-resume，lease 2026-10-27T14:25:30.310Z。從起點帶同一已審source-free EN bridge，no force，20分鐘callback與30秒IO上限不變。**先等97854 nativeexit，再核695b實際沿用、完整flags、second runtime/cleanup及journal；不可啟動另一producer／JA或重播97406。** 續檢前checkpoint已push至2651b8a53；本次dispatch另存本機。見[dub-en-eighth-check-recovery.json](dub-en-eighth-check-recovery.json)。0/8外語驗收，完整包及下一集未成。

最新續作入口：2026-10-27T14:14:45.0472582Z。第七筆43f97／lz504已通過逐筆恢復覆核，Root fresh566次SHA核對：current/private各212raw、current/frozen/consumption三方cache170、原137全保留、70preserved＋3active＝73精確journal會員、21present／1absent、terms0及來源／lexicon／unused EN binding一致；原PID43140 dead且無競爭程序／lease／STOP／ASRstate。**唯一正常續檢session97406／PID27636執行中**，slot check-en-saved-answer7-resume，lease 2026-10-27T14:14:48.409Z。從起點帶同一已審source-free EN bridge，no force，20分鐘callback與30秒IO上限不變。**先等97406 nativeexit，再核43f97實際沿用、完整flags、second runtime/cleanup及journal；不可啟動另一producer／JA或重播94112。** 續檢前checkpoint已push至1b58cab781c58f0fa5495d93419619d7ff9bd5cb；本次dispatch紀錄另存本機。見[dub-en-seventh-check-recovery.json](dub-en-seventh-check-recovery.json)。0/8外語驗收，完整包及下一集未成。

最新續作入口：2026-10-27T13:53:02.6945692Z。第六筆保存回覆逐筆恢復覆核及Root fresh557次SHA核對通過：current/private各212raw、current/frozen/consumption三方cache137、原130全保留、64preserved＋3active＝67精確journal會員、terms0與來源/lexicon/unused EN binding均current，原PID53448 dead且無競爭程序/lease/STOP/ASRstate。**唯一正常續檢session94112／PID43140執行中**，slot check-en-saved-answer6-resume，lease 2026-10-27T13:53:03.335Z；同一已審EN source-free bridge從起點帶入，no force／原20分鐘callback及30秒IO上限不變。新runner僅把observer參數改成basename，helper仍只涵蓋synthesis，不拿空檔證明ASR沒有HTTP錯誤。**先等94112 nativeexit，再核0196實際沿用、完整flags、second runtime/cleanup及journal；不可啟動另一producer/JA或重播54516。** 見[dub-en-sixth-check-recovery.json](dub-en-sixth-check-recovery.json)。0/8外語驗收，完整包及下一集未成。

本輪最新：54516已於13:39:12Z native1結束，EN辨識cache137/212；第五保存答案實際沿用獨立確認，第六筆完整回覆離線恢復及逐筆覆核PASS，準備fresh核對後正常續檢。64歷史檔與3active均保留，Windows鎖來源仍未知，沒有OS／供應商／費用／上限變更。舊transport observer因absolute path未啟用，且只涵蓋synthesis，不能把缺席當作ASR未遭HTTP錯誤。見[dub-en-sixth-check-recovery.json](dub-en-sixth-check-recovery.json)。

最新續作入口：2026-10-27T13:38:05.3498942Z。第五筆保存回覆逐筆覆核及Root fresh550次SHA核對通過：current/private各212raw、current/frozen/consumption三方cache130、原126全保留、58preserved＋3active＝61精確journal會員、terms0與來源/lexicon/unused EN binding均current，原PID32176 dead且無競爭程序/lease/STOP/ASRstate。**唯一正常續檢session54516／PID53448執行中**，slot check-en-saved-answer5-resume，lease 2026-10-27T13:38:06.012Z；同一已審EN source-free bridge從起點帶入，no force／原20分鐘callback及30秒IO上限不變。**先等54516 nativeexit，再核128762實際沿用、完整flags、second runtime/cleanup及journal；不可啟動另一producer或JA，不能重播38131。** 見[dub-en-fifth-check-recovery.json](dub-en-fifth-check-recovery.json)。0/8外語驗收，完整包及下一集未成。

21:36台北最新：38131已因第五筆完整ASR回覆的Windows journal EPERM native1結束。前四筆保存回覆均實際沿用，current130/212cache、原音與中文master未變；第五筆離線恢復及逐筆獨立覆核PASS，準備fresh核對後新slot續檢。所有58歷史檔與3active保留，沒有提高重試／圖片／全域上限。EN完整品質、八語驗收與交付包仍待完成。見[dub-en-fifth-check-recovery.json](dub-en-fifth-check-recovery.json)。

21:28台北最新：29192於第四筆完整回覆confirmed rename EPERM native1停止；EN辨識cache126/212，新保存回覆已離線恢復及逐筆獨立覆核PASS，準備fresh核對後新slot續檢。52歷史檔與3active三真檔保留，未增加30秒重試上限、圖片支出或全域預算；無新語言合成、無音訊接受。見[dub-en-fourth-check-recovery.json](dub-en-fourth-check-recovery.json)。

21:22台北最新：第三筆完整保存回覆已逐筆獨立覆核，fresh536次SHA／current110cache／49journal會員與來源、hint、unused binding、製作鎖核對後，唯一正常EN續檢29192／PID45724執行中。既有已付答案循正式journal恢復，其餘不同請求仍用既有授權流程；不force或改上限。等待完整音訊結果再續JA，0/8外語驗收。見[dub-en-third-check-saved-answer-recovery.json](dub-en-third-check-saved-answer-recovery.json)。

21:18台北最新：5437已因第三筆完整回覆的Windows journal EPERM native1結束；9bd6保存答案實際沿用通過獨立核對，原103cache保留、目前110。新aa360/v2a0431三真檔與所有46歷史檔保存，離線官方恢復native0/reused1/send0/fetch0，逐筆覆核與新入口準備中。無producer／second dispatch／JA，尚無完整EN品質結果；圖片帳本及所有上限不變。見[dub-en-third-check-journal-failure.json](dub-en-third-check-journal-failure.json)。

21:12台北最新：新保存回覆已逐筆獨立覆核，Root fresh核529次SHA／103cache／212raw／43journal會員與來源、lexicon、unused binding、製作鎖後，唯一正常續檢5437／PID45204執行中。沿用既有原音與已審bridge、no force，不改費用／重試上限。等nativeexit和完整品質／實際沿用證據才處理下一步，0/8外語驗收。見[dub-en-second-check-saved-answer-recovery.json](dub-en-second-saved-answer-recovery.json)。

21:05台北最新：EN辨識進度103/212，上一筆保存回覆已由正式journal沿用，獨立實際核對通過。74735已因另一筆完整回覆的Windows EPERM native1結束；新三真檔已凍結，離線官方恢復及逐筆獨立覆核PASS，準備fresh核對後新slot正常續檢。尚無EN完整品質結果或外語驗收，不啟動JA。圖片費用／上限、212原音與中文master不變。見[dub-en-second-check-journal-failure.json](dub-en-second-check-journal-failure.json)；以下running狀態保留為歷史。

20:30台北最新：EN已付ASR answer恢復合約的獨立PRIVATE clone覆核通過，Root fresh232檔／lexicon／3journal與unused binding全部一致後，新正常首檢續作74735／PID12192執行中，仍從起點帶已審source-free bridge。不force、不動原音或OS／上限；先等nativeexit及實際journal consumption／品質與second runtime證據，不能先做JA。見[dub-en-first-check-saved-answer-recovery.json](dub-en-first-check-saved-answer-recovery.json)。

20:26台北最新：EN首檢46532在保存完整primary ASR回覆後Windows journal升格EPERM，native1／尚非完整品質結果。14筆已寫cache、新answer三真檔及22份mutable evidence已凍結，212原音及中文final全未變。30秒I/O額外wait已耗盡，沒有解除持續拒絕；不增加全域／本集上限或更動OS安全設定。獨立PRIVATE official-journal恢復核對中，Root未重送；無producer／lease／secondASR dispatch。詳見[dub-en-first-check-journal-failure.json](dub-en-first-check-journal-failure.json)，以下首檢running為歷史。

20:21台北最新：完整EN cohort與binding獨立覆核已PASS，原始212句及12個stretched實際樣本、current source/cache/voice/v4與150窗0over物理fit全部核對。當前唯一本集producer為官方EN首檢46532／PID46832，首檢即帶已審source-free bridge v3；等其nativeexit／原始flags及真runtime/cleanup結果才續做，不先啟動JA。這不是發音驗收或聆聽通過，完整上架包仍未成。見[dub-en-first-check-dispatch.json](dub-en-first-check-dispatch.json)；下段為此前履歷。

20:04台北最新：中文版完整master維持11/11QA及委託final核准。英文首次合成／混音已native0，212句／150窗fit0over，969.705秒／46,583,012B，SHA99141e431c94d33b29d9143af4259f1f083e730f968389cdd68156408ac2adc9；8窗加速≤1.15、cheng-date合法借後停頓0.1秒。兩筆已付答案成功沿用，原172片段全未變且獨立實際覆核通過。I/O限定處理已審啟用但0額外retry，不能當作OS修復證明。正在準備真212WAV cohort及首檢binding，尚無EN音訊接受／其餘七語／完整交付包，未上傳。collector v1僅mock覆核被拒、v2修補；bridge v3 generic PASS尚非實際dispatch批准。圖片／judge上限及帳本完全不變。詳見[dub-en-synthesis-complete.json](dub-en-synthesis-complete.json)與queue；以下172片段等狀態保留為履歷。

目前更新（以batch-queue.md最新時點為準）：中文master16:09.667已11/11QA及委託final核准；英文已有172個片段，尚未組成完整配音或通過fit/audioQA。Windows完整回覆journal升格曾四次更名失敗，全部已付回覆與原片段保留；當前兩筆已在PRIVATE clone證明可沿用，先等本集限定、30秒額外上限的原rename重試處理自測與獨立覆核，不改OS安全設定／全域額度或repo共享工具。ASR bridgev1/v2的缺陷在付費啟用前被覆核攔下，v3仍待審。其餘七語與完整交付包未成，沒有上傳。

中文master已完成與依委託核准，實際16:09.667／29090frames，SHA b8bc3fcfe22e73cff79422124d89da99630bbf7c7e59b0480ef9804db11d2c60；官方QA11/11、新檔原生開場／片頭／更新字幕／v4片尾及ended抽查通過。僅抽查，沒有宣稱站主觀看或任何人完整聆聽。九語CC文字綁定current，外語速度警告留待實際配音時間處理。現在英文首次dub90907執行中（dry-run171requests／10565字元／當時既有月額5508182），七語待後續；八語／上架包未成，未上傳。下段17:55來源及音訊決策保留，其render執行狀態已被本段取代。

新source SHA6e0dd44b07a5bef457438b18d75371d214acde1f3c37718d08ac4661203f3b86，speechHash fa2912daff4bd218，實際正文28310frames／30＝943.666667秒。listener修補5句、敘事round8依官方合併13/13、八語40格差分覆核及1696source hashes均current。129圖全沿用，保守圖片／評審控制總額仍US$1.578／6；既有976秒配樂SHA a00ffb8aa48c83041867c2ea319ff962b21b6510cb9e97030711ef73e9518a41沿用，不新買。音訊依有界委託品質決策核准，官方2flags及低分保留，沒有聆聽或自動全過宣稱；見audio-qa-delegated-decision.json。新render session56428執行中，舊16:11.967預覽還不是當前final，八語dubs／完整交付包未成。

現行lint0errors／0warnings，bundled Node24.19.0完整docs-video236/236、task2193通過，見validation-listener-rw1.json。下方原報價與各次驗證保留為當時紀錄，以batch-queue.md最新斷點續作。

## 已完成的準備

- 6 章、212 行、3,206 個漢字口語單位；150 景，其中 129 景為插圖，24 條伏筆。開場先說利害與場景，只有兩個預告，再接承諾句與問題；每章對觀眾說話，包含旁白自己的反應。
- 13 分鐘是製作目標；設定一秒四至五字。CLI 舊估速為 15.7 分鐘，兩者都不是音檔實測。目前約3,200字，合成後若未達約13分鐘，補有來源的實質內容並重審，不以加長空檔處理；按實測時間修正語速或實質內容，不用停頓、慢播或片頭片尾補正文長度。
- 系列畫風固定 `cute-mystery`、MiniMax `image-01`；129 景中 66 景的既有 prompt、camera、scene ID 逐字沿用，63 景另寫畫面；正文插圖占比約 87%。繁中字幕改燒錄，縮圖採 bold layout d。
- 原圖 68 張的選定檔案雜湊全部驗證通過，完整素材已另存新版工作目錄；一筆已不符合實際檔案的歷史快取索引不移入。副本不含原版核准、旁白、時間軸、付費佇列、鎖或帳本。新版插圖清單仍須經正常 keyframes 對帳，才會具有新版視覺綁定。
- 配樂沿用原版已取得的曲目（SHA-256 `a3bf978eb08fca11cf3483fb8944b5705f85cb429ff6ee56b0bb137500c48c59`），依實測旁白長度明確循環；不新買音樂。頻道 v4 片頭與 21 秒結束畫面素材在本機且已核對。
- 來源逐句覆核 212/212 通過，`speechHash=8af0af8b6fb7d1e4`，見 [claim-audit-20261026.md](claim-audit-20261026.md)。十驛不是荔枝運單；宋人產地與天數說法保留作者年代；送達鮮度、確切出發地與實際天數仍未結。

## 一集一次報價

2026-10-26 正式站唯讀 dry-run：

| 項目 | 數量／單價 | 費用或額度 |
| --- | --- | --- |
| 中文旁白 | 171 個合成請求，4,270 計費字元；Sulafat ready | 工具只報字元與配額，不報美元；當時 Gemini 月額度剩 5,951,808 字元，未送出合成 |
| 新增插圖與評審 | 63 景，每次 US$0.0035 圖片 + US$0.01 評審 | 一次全過約 US$0.85；每景最多三次約 US$2.55 |
| 保守全量插圖上界 | 若 129 景全需新畫，各最多三次 | dry-run 約 US$5.22；工具報價未扣已複製快取 |
| 既有圖、既有配樂、離線合成與字幕 | 沿用及本機處理 | 不另買圖／音樂；若判定或輸入已變，仍以正常產線判定是否需評審 |

**站主已一次核准本集插圖與圖片評審上限 US$6。** 預期沿用 66 張後費用較低；上限採工具未扣快取的保守全量計算。每景最多三次，不自動無限重畫。若新增要求或剩餘額度不足，先留下實際帳本與缺口，再處理變更。

2026-10-26 站主已明確核准新稿與US$6上限，並委託依推薦選擇持續製作；新 outline/script 核准已按新檔雜湊記錄。以下實際進度取代開工前的費用與工序狀態；上架包、上傳及公開狀態仍分開記錄。

## 製作履歷（2026-10-27；當時狀態保留，最新斷點見下段）

- 中文TTS完成：171請求、4,430計費字元；212句WAV合計12:53.440。時間軸含工具固定句間／換景間隔，共15:45.967；發聲語速在約4–5字／秒目標內。沒有為湊片長重錄、慢播或補空白。
- 第一套音訊檢查212句已完成，31句需第二意見；仍未核准音訊。第二套離線Whisper只讀原WAV、保留逐檔SHA與執行收據，不把ASR誤聽直接當成配音錯誤。
- 正常產線實際保留65張舊圖判定；consort-basket原提示三次未過，已依委託改成單人、室內、素牆的簡單畫面。僅改這景prompt，旁白、敘事盲評與script-check綁定不變。
- 圖片工作在服務502後暫停對帳；v2-add-037已生成及下載，續跑應取原快取評圖，不能重買。帳本US$0.4895已包含早期斷線工作的US$0.0035；該圖已用既有原檔及伺服器唯讀收據離線恢復cache、結清pending，沒有新增請求或重複入帳。另保留最多US$0.05未回傳judge費用不確定量，保守合計US$0.5395，仍受US$6上限管理。完整分鏡尚未交付。
- 離線版面預覽已完成：21張字卡、212段字幕strips、九語縮圖，工具無layout錯誤；九張縮圖及字卡聯絡表已逐一查看。此檢查不等於最終影片QA，詳見 [render-preview-review.json](render-preview-review.json)。
- 配樂由原版已付原始曲目離線延長至976秒，新購費用0；新檔SHA-256 `a00ffb8aa48c83041867c2ea319ff962b21b6510cb9e97030711ef73e9518a41`，官方music命令已核對並寫出本集manifest。
- 八語各212行已翻譯、逐語獨立覆核並套用修正；這是文字候選完成，實際配音、窗口fit與外語音訊檢查仍待中文版定案。
- 31句獨立轉寫已完成，原始輸出與輸入WAV驗SHA通過；離線診斷16句可依既有比對規則排除疑慮、15句仍待判讀。詳見 [audio-qa-progress-20261027.md](audio-qa-progress-20261027.md)。八語最終文字覆核均已讀回且綁定合併檔SHA，見 [i18n-review-summary.json](i18n-review-summary.json)。
- 恢復配對後官方check-audio已正式排除16句，仍15flags；局部重錄及退避37分鐘後續作均遇供應商429，音檔未變，暫緩語音。圖片續作目前91張通過，剩38張正在以每次HTTP嘗試記錄的私有費用煞車續作；既有帳本US$0.5265，另保守保留US$0.17前段重試不確定量，全段仍以工具單價US$6控制，不改全域預算。
- 實際時間軸45秒鉤子檢查0問題，最長41.033秒；24條loops均可定位。開場52.466667秒，片頭插入frame1574；音訊取樣／SHA全匹配，976秒配樂覆蓋正文且餘30.033秒。16個來源URL各GET一次均200且無redirect，最終QA仍需重查完整組合說明欄。
- 150個正文視覺states的正式pace檢查0問題。本集drama/explainer適用15秒上限，21張字卡最長13.167秒；212字幕strips與另加的品牌片尾不冒充正文畫面state。

預覽完成快照2026-10-27 08:47台北：129/129插圖與分鏡通過；中文版預覽已合成，29159frames／30fps＝16:11.967，原生播放器可播放、跳轉並正常播畢。-14LUFS／truepeak-1.9dBFS／musicbed-33.1LUFS，當前source/media綁定與原版SHA均核對。完整QA10/11只剩音訊未核准；三張外語縮圖後續實圖檢查均過（28／26／30px），八語文字review SHA最新，配音尚未生成。帳本US$1.3905、包含歷史重試不確定量的保守控制US$1.578，均低於US$6；配樂／clips新購0。該快照尚未通過音訊、final或完整交付包，詳見[production-preview-r6.json](production-preview-r6.json)。

先前09:38台北：09:30退避後已正常續試一次13句／242字元，session16091保存native_exit4，仍為Gemini忙碌／用量限制；21個凍結檔案未變，成功重錄輪數0、journal全空且lease已釋放。累計四個語音指令均未完成重錄，不把拒絕請求算成已錄完的品質重錄輪次。當時11:40台北的退避斷點已由下段12:02收據取代；沒有新WAV就不再跑ASR或重合成，不提早接下一集。見[speech-retry-20261027-0930.json](speech-retry-20261027-0930.json)及[batch-queue.md](batch-queue.md)。

先前12:02台北：11:40退避後的一次續作session21401仍native_exit4／busy-quota，21檔未變、journal全空、lease釋放，沒有成功重錄或新ASR；當時13句仍待修正。退避至**16:00台北**的斷點已由下段成功續作收據取代，不推定日額或供應商重置時間。第五個未完成語音指令的實證見[speech-retry-20261027-1140.json](speech-retry-20261027-1140.json)。音訊、final、八語配音與完整交付包仍未完成。

最新16:05台北：退避後session62156已native_exit0，完成13requests／242字元、158reused；13WAV實際改變並凍結，正文28290frames／30＝943秒，audio_evidence0問題、journal空且lease釋放。成功重錄輪數1，現在先做新WAV獨立ASR與官方音訊QA；舊13flags屬舊take，舊16:11.97預覽／10/11QA與新旁白不同，尚未重組或核准。新cohort manifest SHA `fb86a85557d67c3c1fa6f849564fc27986fb5ced4b0212a52ce485ed8c693a46`，收據[speech-retry-20261027-1600.json](speech-retry-20261027-1600.json)。先前Windows preload URL錯誤已離線查明並對帳，CLI未載入；改用file URL後才完成唯一正常provider續作。圖片／評審與配樂沒有新費用，八語配音及交付包仍待辦。

最新16:38台北：r1獨立ASR13/13及官方QA完成，疑句降至5；已保存的transcribe answer經官方journal恢復並實際reused1，沒有重買該筆。只對5句作r2原文重錄已native0（71171，5requests／88字元、166reused），正文28317frames／30＝943.9秒；5新SHA待新獨立ASR及官方QA。成功plain重錄2/2後不再無限重錄，如仍有疑句才進最多2輪受保護的措辭修正。active journal entries0但已驗證recovery/tmp證據保留，source／voice及圖片音樂費用未變；audio／final／八語配音仍未完成。收據[audio-qa-retake1-official.json](audio-qa-retake1-official.json)、[audio-retake2-20261027.json](audio-retake2-20261027.json)。

## 接續順序

1. 已完成：站主確認這份修訂稿與本集生圖上限；只對新版記錄新的 outline/script 決定，不移用原版核准。
2. 中文旁白 → check-audio → 原圖對帳與新增插圖 → 分鏡檢查。站主已委託例行推薦選擇，代理依實際QA記錄決定，不寫成站主本人已聽／已看。
3. 明確循環既有配樂，render → clips → assemble；頻道片頭在開場濃縮後、片尾 v4 end screen。量測實際正文與成片長度、燒錄字幕、章節與音量，完成 QA 後送成片審核。
4. 原版已選 en/ja/ko/es/pt/id/vi/th；新版字幕與配音須按新稿重建及逐語審查。原版六條已成配音只作保留素材，不能標為新版可用。待中文版定案後續做外語及上架包。
5. 未取得成片與上架授權前，不上傳、不改任何 YouTube ID 或公開狀態。

## 驗證記錄

- 新稿 lint：0 errors、0 warnings；來源覆核通過。敘事第6輪兩位新讀者為13/13、11/13，依既定合併規則通過13/13；原始意見及全部輪次保留在narrative-review.json與narrative-rounds.json。
- `npm run check:tasks` 通過（2190 張票；既有過期與重疊警告保留）。
- 新增斷線續作工具票後，再用bundled Node24.19.0執行check:tasks通過（2191張票）；八語修正、泰文說明欄縮短及插圖prompt修正後的lint仍為0 errors／0 warnings。
- 完整 `test:docs-videos`：235 通過、1 失敗。唯一失敗為既有 imported-long-languages runtime 測試，系統 Node 24.13.0 子程序以 Windows 原生碼 3221226505 結束；未修改該工具。改用既有 bundled Node 24.19.0 單獨重跑同一測試通過（1/1）。沒有宣稱整套測試全綠。
- 中文版未核准預覽已生成並做播放器抽查；音訊13flags仍待修正，八語音軌與完整上架包未做，沒有上傳、公開或站主本人驗收。不能把預覽當成整集已完成。
