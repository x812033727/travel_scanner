# S31 新規則版製作與報價（2026-10-26）

新稿：[script.md](script.md)。原標題保留，使用獨立 slug `curio-s31-v2`。原版 `curio-s31` 的成片、旁白、插圖、外語及核准仍歸原工作與 PR #1800；本次不覆寫它們。

## 當前讀回（2026-10-27）

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
