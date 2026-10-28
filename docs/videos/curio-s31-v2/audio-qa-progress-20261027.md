# S31 v2 音訊檢查進度

狀態：**累計8句新take；剩21句已審並dispatch唯一session46336，等待native exit，不能開另一producer。plain0/2、0/8 accepted**。

最新 checkpoint（2026-10-28）：唯一partial21續作session46336／PID48028於08:28:25.3401679Z以native0完成。Root核對全212 raw：目標29句全部為新take、其他183句未變，先完成的8句原樣保留；96份journal歷史證據保留、active0。新混音16分9.705秒（46,584,728 bytes），decode native0，−14.10 LUFS／−1.94 dBTP；150視窗0 over、7個加速至多1.15倍，cheng-date的0.1秒由下一停頓吸收。**第一輪原文重錄完成1/2；新音訊品質尚待檢查，0/8外語驗收。** 新212音檔與實測fit已獨立覆核通過；lz403保存答案亦確認正常沿用；舊check屬歷史take，不能當新版通過。ASR交接僅準備、尚未移檔或啟動新check，完整交付包與S15仍未開始。見[第一輪重錄完成證據](dub-en-quality-retake1-complete.json)。

歷史 partial21 dispatch 快照（已由完成紀錄取代；段內running狀態僅指當時）：`dub-en-quality-retake1-partial23`（session31833／PID22012）於08:13:33.6032742Z native1結束，停止於下一筆語音 confirmation 更名 EPERM；212 raw累計8句新take、其他183句未變，93份journal＝82歷史＋上一筆orphan1／recovery6＋新四檔。上一筆076678／lz311p2已實際canonical沿用，原32字元與本次reuse 0分開保存；新79e359／lz403的exact whole-body、私有SPEECH恢復及剩餘21句binding均獨立通過。剩21句全付估938字元，saved41沿用後其餘20句為897。**Root已於08:23:03.9453180Z dispatch唯一partial21續作（session46336），目前等待native exit，不能開另一producer或重播full29／partial23。** fresh quota 5,070,852（08:21:47Z）僅為快照。原fit／mix／check仍非新take的品質證明，plain完成0/2、0/8外語接受；無ASR handoff，完整包未完成，S15未開始。見[剩餘21句與保存答案](dub-en-quality-retake1-partial21-journal.json)。

歷史 partial23 準備快照（已由本次partial21斷點取代；段內狀態僅指當時）：冷卻後的 `dub-en-quality-retake1-after-busy5`（session75617／PID20616）於07:51:15.8133662Z native1結束；本次已成功取得新語音回覆，停止原因是保存語音回覆的 confirmed temporary journal 更名 EPERM。已核對212 raw，其中目標29句有6句新take、其他183句未變；82份歷史journal與本筆四檔全部保存。請求076678…63e3精確對應lz311p2；私有SPEECH恢復測試與獨立覆核通過，reused1/send0/fetch0，尚未在canonical實際沿用。**續作只帶剩餘23句（全付費估1013字元；保存答案32沿用後，其餘22句最多981），不可重播原29句。** Root正準備fresh quota／來源／journal／lease核對後的唯一正常續作。原fit/mix/check仍屬舊take，不是新錄音通過；plain完成0/2、0/8外語接受，ASR handoff與S15未開始。見[部分重錄與保存答案](dub-en-quality-retake1-partial-journal.json)。

窄診斷：[私有 final-diagnosis.md](C:/Users/x8120/mokaair-work/curio-s31-v2-preflight/rename-native-diagnostic-20261027/final-diagnosis.md)，SHA256 `fa648dfc294921661b21f98f795d5f3ef16002325f1358c0d8dd0948fe441f86`。本機fixture可重現EPERM，但未證實production持鎖來源或UTF8因果；沒有OS改動或上限變更。Transport observer只涵蓋synthesis，舊absolute-path配置未啟用；空檔／缺席不能證明ASR無HTTP錯誤。

**歷史快照：以下 running、最新、待核對等文字均描述當時狀態，不得用來判斷目前程序；目前狀態以上段為準。**

最新 checkpoint（2026-10-27）：97854／PID15272已於14:34:07.6598357Z native1結束，這次是**首次完整EN音訊檢查的29個品質flags，不是journal故障**。212/212＝148 exact＋13 Jev通過＋22 second解除＋29 flags；本輪22個新ASR、3次Jev及1個保存答案沿用，primary Jev累計64、second transcript共51。695b／lz514實際沿用已獨立確認，舊189筆primary／語意欄位保留，noul／second新增另列；active journal 0、82份歷史證據與舊take已凍結。**第一輪原文重錄準備，尚無producer；0/8 accepted。** 29 requests／1251官方billable字元僅離線規劃，plain 0/2、shorten 0、listener 0；14:51:49.2388142Z官方dry-run native0已讀Gemini ready／remaining 5,157,762，足夠實際29 requests／1251 billable；681次fresh checks（非unique檔數）。Root按授權準備獨立付費slot，尚未dispatch，quota只是快照並非保留額度。官方dry-run會忽略redo而報0，不能拿它代替本次實算。Second runtime獨立覆核PASS：51 subset的raw／完整實際轉寫／cache全SHA一致，nativeWhisper0／390.379s、callback396.399s，4CPU／nice19／offline／no hints；本機child close0／reaped及三PID已退出，無holds／uncertain／lease。遠端scratch刪除未證，state／runs保留未archive；無runtime阻擋另行TTS，仍非音訊核准。見[dub-en-first-check-complete.json](dub-en-first-check-complete.json)；完整包及下一集未成。

最新續作入口：2026-10-27T14:25:29.6516650Z。第八筆695b／lz514已逐筆恢復覆核，Root fresh573次SHA核對：current/private各212raw、三方cache189及原170全保留、76preserved＋3active＝79精確journal會員、21present／1absent、terms0及來源／lexicon／unused EN binding一致；原PID27636 dead且無競爭程序／lease／STOP／ASRstate。**唯一正常續檢session97854／PID15272執行中**，slot check-en-saved-answer8-resume，lease 2026-10-27T14:25:30.310Z。從起點帶同一已審source-free EN bridge，no force，20分鐘callback與30秒IO上限不變。**先等97854 nativeexit，再核695b實際沿用、完整flags、second runtime/cleanup及journal；不可啟動另一producer／JA或重播97406。** 續檢前checkpoint已push至2651b8a53；本次dispatch另存本機。見[dub-en-eighth-check-recovery.json](dub-en-eighth-check-recovery.json)。0/8外語驗收，完整包及下一集未成。

最新續作入口：2026-10-27T14:14:45.0472582Z。第七筆43f97／lz504已通過逐筆恢復覆核，Root fresh566次SHA核對：current/private各212raw、current/frozen/consumption三方cache170、原137全保留、70preserved＋3active＝73精確journal會員、21present／1absent、terms0及來源／lexicon／unused EN binding一致；原PID43140 dead且無競爭程序／lease／STOP／ASRstate。**唯一正常續檢session97406／PID27636執行中**，slot check-en-saved-answer7-resume，lease 2026-10-27T14:14:48.409Z。從起點帶同一已審source-free EN bridge，no force，20分鐘callback與30秒IO上限不變。**先等97406 nativeexit，再核43f97實際沿用、完整flags、second runtime/cleanup及journal；不可啟動另一producer／JA或重播94112。** 續檢前checkpoint已push至1b58cab781c58f0fa5495d93419619d7ff9bd5cb；本次dispatch紀錄另存本機。見[dub-en-seventh-check-recovery.json](dub-en-seventh-check-recovery.json)。0/8外語驗收，完整包及下一集未成。

最新續作入口：2026-10-27T13:53:02.6945692Z。第六筆保存回覆逐筆恢復覆核及Root fresh557次SHA核對通過：current/private各212raw、current/frozen/consumption三方cache137、原130全保留、64preserved＋3active＝67精確journal會員、terms0與來源/lexicon/unused EN binding均current，原PID53448 dead且無競爭程序/lease/STOP/ASRstate。**唯一正常續檢session94112／PID43140執行中**，slot check-en-saved-answer6-resume，lease 2026-10-27T13:53:03.335Z；同一已審EN source-free bridge從起點帶入，no force／原20分鐘callback及30秒IO上限不變。新runner僅把observer參數改成basename，helper仍只涵蓋synthesis，不拿空檔證明ASR沒有HTTP錯誤。**先等94112 nativeexit，再核0196實際沿用、完整flags、second runtime/cleanup及journal；不可啟動另一producer/JA或重播54516。** 見[dub-en-sixth-check-recovery.json](dub-en-sixth-check-recovery.json)。0/8外語驗收，完整包及下一集未成。

本輪核對：第五128762實際沿用已確認，原130cache保留、current137；第六0196/lz422三真檔及64保存檔完整，離線恢復native0/reuse1send0fetch0與逐筆獨立覆核1af9f5…f6f89 PASS，尚未新dispatch或second ASR。舊observer absolute path不符basename契約，未啟用；且它只涵蓋synthesis，缺席／空檔不可當ASR無HTTP錯誤證明。見[dub-en-sixth-check-recovery.json](dub-en-sixth-check-recovery.json)。

最新續作入口：2026-10-27T13:38:05.3498942Z。第五筆保存回覆逐筆覆核及Root fresh550次SHA核對通過：current/private各212raw、current/frozen/consumption三方cache130、原126全保留、58preserved＋3active＝61精確journal會員、terms0與來源/lexicon/unused EN binding均current，原PID32176 dead且無競爭程序/lease/STOP/ASRstate。**唯一正常續檢session54516／PID53448執行中**，slot check-en-saved-answer5-resume，lease 2026-10-27T13:38:06.012Z；同一已審EN source-free bridge從起點帶入，no force／原20分鐘callback及30秒IO上限不變。**先等54516 nativeexit，再核128762實際沿用、完整flags、second runtime/cleanup及journal；不可啟動另一producer或JA，不能重播38131。** 見[dub-en-fifth-check-recovery.json](dub-en-fifth-check-recovery.json)。0/8外語驗收，完整包及下一集未成。

21:36台北：ff4b/lz418 actual沿用已獨立確認，原126cache保留、current130。第五128762/v2a0521完整保存回覆離線恢復native0及逐筆獨立review b1a577…ff129 PASS，58歷史保存檔＋3active均保留，等Root fresh核對後新slot正常續作；無producer或second dispatch，原音／中文master／上限不變。見[dub-en-fifth-check-recovery.json](dub-en-fifth-check-recovery.json)。

21:28台北：第四筆ff4b/lz418完整答案、sent、tmp與52保存檔保留；actual private恢復native0/reuse1send0fetch0及逐筆獨立覆核d44b7b…a75a9通過。29192已結束不可重播，先fresh核對再新slot續作。126筆cache是檢查進度，未代表音訊接受；原音、中文master與上限不變。見[dub-en-fourth-check-recovery.json](dub-en-fourth-check-recovery.json)。

21:22台北：逐筆獨立review f3db35…dc1f5與Root fresh536次SHA／cache三方110／49journal會員／1個實際hint／unused binding／lease與producer前提通過，正常新slot `check-en-saved-answer3-resume`已dispatch29192／PID45724。先等nativeexit及aa360實際沿用、flags和second runtime/cleanup；原音及上限未改，沒有EN音訊接受或JA合成。見[dub-en-third-check-saved-answer-recovery.json](dub-en-third-check-saved-answer-recovery.json)。

21:18台北：9bd6/lz411 canonical實際沿用獨立PASS，原103cache全部保留，目前110。5437已native1於新aa360/v2a0431完整回覆升格失敗，三真檔與46歷史保存檔都保留；離線checker native0/reused1/send0/fetch0，尚待逐筆獨立覆核與fresh核對再新slot續檢。無producer／second dispatch；原音、中文final及預算未改。見[dub-en-third-check-journal-failure.json](dub-en-third-check-journal-failure.json)。

21:12台北：529次current／private SHA核對、實讀103cache／212raw、40preserved＋3active精確journal會員及source/lexicon/unused binding／lease／producer前提全過，已啟動5437／PID45204。新slot `check-en-saved-answer2-resume`沿用已審EN source-free bridge，未force或改上限。先等nativeexit再核對實際9bd6回覆沿用、flags及second runtime；不把private recovery PASS當作音訊接受。見[dub-en-second-check-saved-answer-recovery.json](dub-en-second-saved-answer-recovery.json)。

21:05台北：上一筆lz202實際canonical沿用已獨立驗證，原14筆cache保留、212raw與中文final未變。新lz411的完整回覆、sent及confirmedtmp全保存；113次原rename在30秒deadline仍失敗。已審通用checker對新9bd6…request private replay native0/reused1/send0/fetch0，逐筆獨立覆核f98d96…19001通過；Root準備新slot前的fresh對帳。沒有手動promote、delete/forget、音訊核准或新語言合成。見[dub-en-second-check-journal-failure.json](dub-en-second-check-journal-failure.json)；下方74735執行中是歷史。

20:30台北：lz202 exact request／三真檔／官方16k downsample與hints=[]經PRIVATE replay reused1/send0/fetch0、defaultdeadPID／alive負控全PASS；Root fresh核232檔與journal一致才啟動74735／PID12192，從起點帶同一個尚未dispatch的已審EN bridge。先等nativeexit，clone合約不是canonical已消費或發音已通過。見[dub-en-first-check-saved-answer-recovery.json](dub-en-first-check-saved-answer-recovery.json)。

20:26台北：Windows confirmed升格在113attempt／28160ms排定額外wait後仍EPERM，I/Ov2已按30秒deadline封頂；不增加上限或假稱解決OS。原212音檔／混音／中文final未變，14筆EN cache與第15筆完整paidanswer三真檔已凍結；PID已dead、無lease，尚未第二SSH。先由獨立PRIVATE clone驗exact官方transcribe恢復合約及0send/fetch，再fresh核對後新slot正常續作；不能盲重送或手動promote。見[dub-en-first-check-journal-failure.json](dub-en-first-check-journal-failure.json)。下方running為已結束履歷。

20:21台北：actual212 raw／12 stretched已逐檔與物理fit覆核通過，Root正式首檢從一開始就掛正確EN的已審source-free bridge v3；單一PID46832持lease，先等nativeexit，不開另一check/ASR/TTS/JA。review僅授權實際callback exact-SHA subset及單SSH fresh gates，沒有預稱真ASR/音訊/聆聽pass。見[dub-en-first-check-dispatch.json](dub-en-first-check-dispatch.json)。

20:04台北：EN正常resume92912 native0，969.705秒branded mix SHA99141e…adc9，150窗fit0over（cheng-date0.1秒由next-slack吸收），8窗加速不超1.15。獨立actual recovery核對4aca1e…2e7b確認原172WAV全未變、兩個saved answer正常trim/encode後逐bytes等於v2a0681/v2a0682、log reuse2；不重買這兩筆。I/O preload v2已審後啟用，但實際38次均第一次rename成功、0額外retry／wait，因此不聲稱治好OS。source／中文final及核准不變，品質重錄／縮句／reword0；無active producer／lease／request，34個舊proof/tmp保留。完整212cohort collector v1在mock獨立覆核發現會員／fit一致性缺口，另存v2修補；bridge v3 generic已PASS但尚無actual binding／SSH／ASR／EN音訊接受，不能先做JA。見[dub-en-synthesis-complete.json](dub-en-synthesis-complete.json)。下段172片段及v3待審為舊履歷。

目前更新（以batch-queue.md最新時點為準）：中文master16:09.667已11/11QA及委託final核准；英文已有172個片段，尚未組成完整配音或通過fit/audioQA。Windows完整回覆journal升格曾四次更名失敗，全部已付回覆與原片段保留；當前兩筆已在PRIVATE clone證明可沿用，先等本集限定、30秒額外上限的原rename重試處理自測與獨立覆核，不改OS安全設定／全域額度或repo共享工具。ASR bridgev1/v2的缺陷在付費啟用前被覆核攔下，v3仍待審。其餘七語與完整交付包未成，沒有上傳。

18:21台北：新中文master SHA b8bc3fcfe22e73cff79422124d89da99630bbf7c7e59b0480ef9804db11d2c60，29090frames＝16:09.667，container969.705；11/11QA與實際原生抽查包括兩張更新字幕及正常ended=true／error=null。final核准僅屬此中文檔；無全片連看、人工聽音或站主觀看宣稱。英文dub90907執行中，等實際fit與新WAV才獨立ASR／QA；其餘七語與完整交付包未成。下段17:55舊render狀態已完成，其音訊裁量及兩個官方flag仍保留。

最新17:55台北：listener1的212句官方QA已完成，155逐字＋30同音／口語＋4Jev＋21第二轉寫＋2flags。獨立覆核證明比較器對吳曾／麗芝的多音預設有假陰性；依實際Whisper無憎及實際primary麗芝的語境同音證據接受兩案，同時保留吳政／立志反例與聲調未經聆聽證實的限制。官方低分與2flags原封保留；不是Jev全過，不是站主或代理聽過。詳見[audio-qa-delegated-decision.json](audio-qa-delegated-decision.json)與[audio-acceptance-listener-rw1.json](audio-acceptance-listener-rw1.json)。未執行listener2或新付費；audio gate綁current timeline461844…d8f31、speechfa2912daff4bd218。新render執行中，舊final／10of11QA仍是歷史。下方較早疑句數只屬各自take。

最新16:38台北：第一輪新13WAV已完成盲式Whisper及官方check，疑句降至5（212＝153逐字＋29同音／口語＋4Jev＋21第二轉寫＋5flags），見[audio-qa-retake1-asr.json](audio-qa-retake1-asr.json)及[audio-qa-retake1-official.json](audio-qa-retake1-official.json)。Windows journal更名故障已透過保留的完整answer安全恢復，官方明確reused1；active entries0，原tmp與recovery proof保留。第二輪只重錄5句已成功71171 native0／88字元，5新SHA已凍結，正文現在28317frames＝943.9秒；正準備新5WAV的ASR及新reader。plain drama品質重錄已2/2，後續如仍疑句才進受保護的聽眾改寫（最多2輪）。目前5flags是r1舊take判定，不能當作r2的新QA。見[audio-retake2-20261027.json](audio-retake2-20261027.json)。

最新16:05台北：session62156已native_exit0，13疑句成功重錄（13requests／242字元，158reused），13個WAV SHA全改變且已凍結；source與speechHash不變、audio_evidence0問題、journal空且lease釋放。正文現在28290frames／30＝943秒（15:43），成功重錄輪數1。正準備新13WAV的cached Whisper盲式辨識與新SHA reader；下方原13flags／轉寫是舊音檔結果，不能當作新WAV的QA，也不能沿用舊reader結果。舊預覽與QA需要在音訊通過後重組更新。見[speech-retry-20261027-1600.json](speech-retry-20261027-1600.json)。16:01另有已對帳的Windows preload本機啟動錯誤，未載CLI或送provider；已改file URL，不計provider refusal。

先前續試（11:40退避後，12:02讀回）：session21401仍為native_exit4／Gemini忙碌或用量限制，21個凍結檔案未變、journal空且lease釋放，當時成功重錄輪數仍0。當時13flags保持，沒有新ASR；16:00退避斷點已由上段成功續作收據取代。原始收據保留，見[speech-retry-20261027-1140.json](speech-retry-20261027-1140.json)。下方11:40及09:30內容是先前履歷。

先前續試（09:35:57派送，09:38讀回）：session16091已native_exit4，仍回覆忙碌／用量限制；21個凍結檔案與13句WAV未變、journal空、成功重錄輪數0。此輪已明確保存native exit，不混淆PowerShell外層碼。當時設定下一次不得早於**11:40台北**；該斷點已由上段12:02收據取代。見[speech-retry-20261027-0930.json](speech-retry-20261027-0930.json)。下方09:30文字是前一輪歷史，不能當作新重送授權。

最新正式檢查（2026-10-27 08:00台北）：212/212句檢查，148逐字一致、29同音／口語差異、4句Jev通過、18句由第二轉寫排除疑慮，**13句仍標記**。新增盲式前後文辨識先獨立轉寫52個固定鄰句，再把實際聽到的鄰句文字用作15個target的語境；沒有把原稿或先前target猜測傳給Whisper。新reader逐句驗原始輸出與當前WAV SHA，fresh15整句取代相同音檔的舊結果，其餘16句回退原獨立轉寫；不拼字或修成符合稿子的文字。所有原始結果與低分判定保留。完整來源、目前13句及音檔SHA見[audio-qa-context-r6.json](audio-qa-context-r6.json)。

08:28後的一次正常局部重錄仍回覆Gemini忙碌／用量限制，session43490已exit1；21個凍結檔案、13句WAV、timeline與旁白全未變，audio_evidence0問題、speech-journal全空。這輪沒有直接HTTP碼，不能由訊息擅自認定日額或重置時刻。成功重錄輪數仍0，**下一次不得早於09:30台北**。中文版16:11.967預覽已有片頭片尾、配樂及播放器抽查；完整QA10/11僅narration未核准，沒有把播放成功當成音訊通過，見[production-preview-r6.json](production-preview-r6.json)。

本次旁白的 `speechHash` 為 `8af0af8b6fb7d1e4`。212句WAV合計773.440秒；時間軸28,379格／30fps，為945.967秒。兩種時間分別代表語音片段合計與工具含固定句間／換景間隔的正文時間軸，不能互換。

第一輪官方 `check-audio` 檢查212句：148逐字一致、29同音／口語／拼寫差異、4句Jev判通過、31句仍標記。沒有把單一ASR的誤聽直接當作配音錯誤，也沒有先行核准。

31句獨立第二轉寫已在既有VPS的cached Whisper medium完成，CPU int8、四核affinity、nice19、全離線。先驗證第一句，再跑剩餘30句；兩個程序均exit0、stderr空白，合計282.07秒。傳入音檔與官方轉寫helper，不傳稿句；沒有模型下載或付費供應商請求。

| 證據 | SHA-256 |
| --- | --- |
| 31句輸入清單 | `38c1d1c1a62efc3412e7e788f9705c4970c7eeb690b2901236c577df08299c13` |
| 官方Whisper helper | `4b5f7918d8b2ba970bb547a66c9d25d69c969a772227ccb0b3f928740c3e5338` |
| 31句真實轉寫輸出 | `d402c92532b7fcac4cc7aaca7307b96b2922255ae6495691f181954d6f23e12d` |

原始WAV、逐句SHA與完整執行收據保留在repo外。既有Windows批次在原生主機首句證明可用後終止，部分輸出及停止理由保留；不把中途停止的本機批次寫成完成。

用官方 `matchKind`／`missedInDifferentPlaces` 函式離線比對：11句直接吻合，5句兩套轉寫錯在不同位置，15句仍須Jev或實音判讀。這只是診斷，沒有改寫官方check cache、flags或approval。

站主重新配對後，官方 `check-audio --second-opinion` 已實際執行：沿用212句初輪結果，新增一次Jev判讀並正式排除16句疑慮，15句仍標記。首次局部重錄及退避37分鐘後的一次續作均收到供應商429／忙碌或額度限制、exit4；15個WAV、timeline與旁白再次讀回均與重錄前備份一致。這兩次不算重錄成功；尚未核准音訊，沒有把舊Whisper結果套用到不同音檔。

同日以官方實際時間軸函式另核對：45秒鉤子檢查0問題，最長間隔41.033秒（`v2a0241` 04:06.100 → `lz308` 04:47.133）；24條loops均可定位，實測長度需求13條。開場52.466667秒，頻道片頭應從第1574格插入，不能使用章節字串向下取整的52秒代替。212句與旁白的SHA及取樣證據全匹配。976秒配樂比945.966667秒正文多30.033333秒。這些是時間與檔案證據檢查，沒有宣稱聽懂、觀看或核准音訊。

第一輪第二轉寫後的歷史15句：`lz204`、`v2a0281`、`lz310`、`lz318`、`v2a0461`、`v2a0471`、`v2a0491`、`lz422`、`v2a0611`、`lz505`、`lz506`、`lz511`、`v2a0722`、`v2a0731`、`lz519`。後續正式語境複查另排除`lz204`、`lz505`，目前剩13句，不能照舊15句清單盲目重錄。

下一步是對剛成功重錄的13個新WAV做獨立辨識與官方檢查；先查新cohort與當前ASR程序，不再送同一份TTS。舊reader只接受原WAV雜湊；變更後音檔必須使用新辨識，不能沿用這份歷史結果。只處理有證據的疑句，不因生僻人名、同音字或同景切句位置就重錄整集。

八語文字覆核另見 [i18n-review-summary.json](i18n-review-summary.json)。逐語配音、實際窗口fit、字幕偏移、品牌片頭片尾、成片音量與播放器檢查均尚未通過。
