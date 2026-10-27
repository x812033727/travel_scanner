# S31 v2 音訊檢查進度

狀態：**中文master已11/11QA、原生抽查及委託final核准；EN saved answer恢復合約獨立PASS，fresh232檔一致後正常續檢74735執行中，尚非品質結果**。

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
