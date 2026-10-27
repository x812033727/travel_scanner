# 奇聞檔案局新版續作順序（2026-10-26）

站主本次直接指示：

> 核准新稿與 US$6 上限，繼續製作
>
> 用你推薦的選擇就好 不用問我
>
> 做完後陸續做s15 s12 s16 s19 s20 s21

依序完成上架前的製作包，保留每集原版素材與核准；這份指示沒有要求公開發布或覆寫既有 YouTube 影片。

| 順序 | 原集 | 新版工作 | 目前狀態 |
| --- | --- | --- | --- |
| 1 | curio-s31 | curio-s31-v2 | 第1輪listener官方音訊QA已結束，只剩2個專名／同音疑句；保留低分與原始轉寫，獨立發音覆核中。八語配音尚未開始 |
| 2 | curio-s15 | 先查既有新版與持有者，再決定隔離路徑 | 等 S31 完成 |
| 3 | curio-s12 | 同上 | 等 S15 完成 |
| 4 | curio-s16 | 同上 | 等 S12 完成 |
| 5 | curio-s19 | 同上 | 等 S16 完成 |
| 6 | curio-s20 | 同上 | 等 S19 完成 |
| 7 | curio-s21 | 同上 | 等 S20 完成 |

## 續作原則

- 每集先查現有分支、任務、PR、完整媒體及實際核准，再認領窄範圍新票；原版 PR #1800 與原版工作目錄保留。
- 本機隔離版正式QA前，先用官方`review-push --report-only`登記自己的format/category，再GET核對；未登記slug在伺服器預設套教學示範規則。只報本集狀態，不因此送審、上傳或改全域設定。
- 依當前 `curio-episode`、`youtube-video` 的新規則改稿／查核／新讀者盲評，目標約13分鐘；實際正文與成片都量測。長度不足時補有來源的實質內容，不用空白、重複或慢播補時。
- 依站主推薦選擇授權，例行聲音、分鏡與成片決定可由代理依有證據的品質檢查處理，記錄為「站主委託依檢查採推薦選擇」，不得寫成站主本人已聽／已看。
- S31 的圖片及圖片評審費明確核准上限 US$6。後續採同級保守建議：每集以 US$6 為圖片／圖片評審上限，不改正式站全域預算；若報價或剩餘帳本不容納，先停該集付費部分並回報實際差額。旁白／配音用現有網站字元額度，不提高預算或開新供應商。
- 原圖、配樂及有效快取先驗雜湊再沿用；不把舊核准當新版核准。超時或 uncertain 付費請求先對帳，不能忘記記錄後盲重送。
- 中文版先定案，再按原集已選語言完成標題說明、CC、配音及逐語檢查。原版外語僅保留，不冒充新版。上架包、站主本人驗收、上傳與公開狀態分別記錄。
- 同一集一次只跑一個持有製作鎖的指令；不動其他集或其他聊天持有的鎖、STOP、正式站設定或工作。
- 完成一集即更新本表與該集任務，再接下一集。進度不變時保持安靜，只通知成品完成、真正失敗、預算超限或需要站主處理的事項。

## 當前斷點

**最新實況：2026-10-27 17:46台北。以下較早紀錄保留為履歷，以本段為續作入口。**

官方check8572已於17:31:30台北結束native1：212＝155逐字＋30同音／口語＋4Jev＋21第二轉寫＋2flags（v2a0491、v2a0722），只新增5ASR／2Jev；見[audio-qa-listener-rw1-official.json](audio-qa-listener-rw1-official.json)。當前check／flags、兩個原始WAV及timeline／approvals已凍結，source／audio仍fa2912daff4bd218、audioEvidence0、active journal0、leasefree、producer0。沒有進行第2輪listener或再次付費。離線比較器發音診斷發現吳曾被預設為ceng2、麗芝的麗被預設為li2；實際轉寫與意圖可能只是專名／多音字假陰性，正作獨立來源與發音覆核。不能改flags／低分、拼接轉寫或為了green寫錯字幕；也不能先聲稱實際音訊通過。當前lint已0錯誤／0警告。

當前唯一本集producer是**官方check-audio session8572**，log `check-audio-listener-rw1.txt`，已fresh核對source／timeline／5WAV／audio_evidence0／active journal0／敘事綁定及八語1696格source_hash全current後啟動，不帶`--locale`、不force。先等此指令結束，不啟動競爭的TTS、ASR或check；尚無audio／final核准。

當前source SHA `6e0dd44b07a5bef457438b18d75371d214acde1f3c37718d08ac4661203f3b86`、script SHA `d9056e2b5b27b1ce4c6b084a89adb76a6c723bb603349c2d72f35f9cb028c5b0`、speechHash `fa2912daff4bd218`、narrativeHash `7a931bb0c6952510`；visualHash仍`4ff8941e6473b9f4`。第一版listener裸評的no_recap低判及澄清全部保留；只在合成前修兩處確切重述（不先揭吳曾改口、刪已說過的馬接力），相對r6總5行有差分、207行不變。新bare readers C11/13、D12/13，依官方ANY-yes合併13/13、round8通過，script gate已依委託對新SHA記錄；不是站主本人讀／聽／看。`claims.md`212行對齊，八語各5格共40格已獨立覆核套用、其他207格及metadata／thumbnail不變，見[listener-rw1-i18n-review.json](listener-rw1-i18n-review.json)。

新措辭TTS16992 native0，5requests／90字元、166reused，5WAV實際改變且凍結；source與audio已對齊`fa2912daff4bd218`，正文28310frames／30＝943.666667秒。plain品質重錄2/2維持，listener合成現在1/2；沒有買新圖或配樂。見[listener-rw1-audio.json](listener-rw1-audio.json)，parent manifest SHA `4d729c2d1c6d96c3ebcd6c60e0b007f978893598ef23e2e9707581d290124edb`。獨立cached Whisper已5/5/native0/42.563秒完成，新reader SHA `114981084b5293db2d16115c63df5d7df2a073dbdeee754db2fe164ab4c8bce2`經獨立審閱；整句32聯集為新5＋r2未變1＋r1未變8＋context2＋old16。見[audio-qa-listener-rw1-asr.json](audio-qa-listener-rw1-asr.json)。原舊成片及10/11QA仍不代表當前新音訊。

R2官方check session68516已完成：212/212＝154逐字＋29同音／口語＋4Jev＋21第二轉寫＋4flags（lz318、v2a0471、v2a0491、v2a0722），5新ASR／2Jev；active journal0，已驗recovery/tmp保留。見[audio-qa-retake2-official.json](audio-qa-retake2-official.json)。plain retake2/2用完後，沒有再盲重錄原文；改走第1輪listener受保護措辭，撰寫與獨立語意覆核均PASS，4句已套用並同步script／claims及audit差分，其他208句、專名／數字、voice／shot／metadata均不變。見[listener-rewrite-r1.json](listener-rewrite-r1.json)。

17:01第一版listener source SHA `2646c3a9dbc97b65512a72eff2848319b251a9c3cda653c42dbd5c2991c0fd62`、speechHash `91814d96b978a75e`是未合成的中間稿，低判與後續兩處修補分別見[narrative-listener-rw1-initial.json](narrative-listener-rw1-initial.json)、[listener-rw1-narrative-amendment.json](listener-rw1-narrative-amendment.json)。它已由上段當前來源、round8敘事、40格翻譯與新WAV取代，不能作續作入口。

R2新5WAV的cached Whisper已完成5/5、native0、45.188秒、stderr空；獨立審閱通過的新reader `whisper-retake5-r2-verified-reader.mjs` SHA `b6af5f73f6ea1808c3ff099889d8aaa662f83499f7e1ca73857fc91df463c1d3`，raw SHA `c60b384e5a10184246bb4e2aa29f40dadd9b9dba5526221ef529d8cf9294ad73`。新／舊31整句選取與時間分域均驗證通過，見[audio-qa-retake2-asr.json](audio-qa-retake2-asr.json)。Root fresh核對source／timeline／5WAV／audio_evidence0／active journal0與lease後，已啟動唯一**官方check-audio session68516**，log `check-audio-r2.txt`；先等此指令結束，不再啟動ASR、check或TTS。這不是音訊核准。

官方音訊QA session60616已安全完成：212/212檢查，153逐字、29同音／口語差異、4Jev通過、21第二轉寫排除、5flags；只新增5個primary ASR／2Jev，明確記錄1個先前已付answer由journal讀回，沒有重買該筆。見[audio-qa-retake1-official.json](audio-qa-retake1-official.json)。active journal entries現在0；已驗證的recovery proof與原confirmed tmp仍保留，不能把保留證據誤認為待重送請求或為了清空目錄而刪除。

按現行網站drama重錄上限2（唯讀查得，未改設定），已只對剩餘5句作第2輪原文重錄：session71171 native_exit0、5requests／88字元、166reused，5WAV均變更且凍結，source／voice不變、audio_evidence0問題、active journal0且lease釋放。新正文28317frames／30＝943.9秒；新timeline SHA `1849d12c382ee222475b4a07d115a361606ba6b696f96c34cf13e777efb39cd1`、narration SHA `b819389fc2f68c26577db669fe08943e550fd20e52220f331e7e859ae25faf10`。新cohort manifest SHA `8aa3a3a9e0452d8799681aae999f1d8ece81cec9c03f943931591eb0c8cd5c3b`，收據[audio-retake2-20261027.json](audio-retake2-20261027.json)。`s31_audio_plan`／`s31_translate_ko_es`正準備與覆核唯一next5離線ASR；先查private `whisper-retake5-r2-20261027T0836/`及agent狀態，不另啟第二份。新reader應選r2新5＋r1未變8＋context2＋old16的整句真實ASR。若新QA仍有flags，走最多2輪受保護的聽眾措辭修正，不無限重錄原文；audio／final仍未核准。

R2 next5原launcher審閱PASS SHA `25fb687d73787c1968804bd0792014dc138428de9a74cb85f441b24cd1442fa3`，唯一SSH session71929現已結束；原PID2565、4CPU／nice19／offline及20分鐘硬上限，fresh RAM約27.4GiB、load0.49、worker CPU0.00%／Mem0.11%均通過。原始ASR與收據保留，不重跑此批。

private clone使用官方journal恢復實測已PASS（review SHA `0583f1810e0165ab5edfe74df7a23114786703fdc4e58d17a6a66f8ab52e59d7`）：精確request `04a11d27c3214447eb325787ecac9bc6624ef061e6ea92e6434561cb5f782b93`對應新v2a0611 WAV的16k downsample，完整sent／sidecar／tmp SHA及基底吻合；官方default processAlive確認PID55548為ESRCH，mock send／fetch均0calls，已保存回覆可讀回且reused1。原三檔保持不變，只有private clone新增recovery proof。Root核對後正常續作session60616已完成，log `check-audio-retake13-recovery-r1.txt`；不加force、不手動刪journal，實際讀回已付同request，後續不同request仍是正常已授權查核。

先前故障：官方check-audio session77188於16:26 native_exit1，Windows EPERM使已回覆的speech/transcribe confirmation無法rename到journal。sent JSON、完整answer sidecar、confirmed tmp三檔均已凍結在private `check-retake13-rename-failure-before/journal/`，保留後才作上段對帳與安全續作。這是既有`2026-10-07-preserve-speech-journal-writes-through-windows`票追蹤的類型，不在本影片票修改共用工具。沒有核准audio或final。

16:00退避後正常續作已成功：session62156於16:04:27台北native_exit=0，完成13請求／242計費字元、158請求沿用。13句WAV均實際改變，已逐檔凍結；source/script與speechHash未變，audio_evidence0問題、journal空且lease釋放。新旁白正文28290frames／30fps＝943秒（15:43），新timeline SHA `2c8ca9bcb1351ff046e2d70a4593bdb42442ea9a56172748b06a256875d602bf`、narration SHA `8aba58fcb273ab577bb7b87b380bd79babb24147a845ac89f09b044fc0874082`。成功重錄輪數現在是1；前五個provider拒絕指令沒有完成重錄。完整收據見[speech-retry-20261027-1600.json](speech-retry-20261027-1600.json)，private新cohort manifest SHA `fb86a85557d67c3c1fa6f849564fc27986fb5ced4b0212a52ce485ed8c693a46`。

成功重錄後的順序是cached Whisper獨立辨識、新SHA reader、官方check-audio。ASR與reader審閱已完成，見下段；現在先處理上段journal對帳，不競爭啟動第二份ASR或任何TTS。舊13flags只屬於舊音檔，不能沿用舊轉寫或判定到新WAV。舊16:11.97預覽與10/11QA是重錄前歷史，現在與新旁白不同，尚需音訊QA及重組；不得核准audio／final或接S15。

唯一離線ASR session32156已完成13/13、native_exit0、150.476秒、stderr空，沒有timeout或新模型下載；raw stdout SHA `92db8107dedceb5621c44a913fde3d20f26716ad4cf1f30d14c30c16bfe7246f`。獨立審閱通過的新reader v2 SHA `fa97c6bb6083f1a48a800309aafc9d61db93c871c54b70e3ceb278a65ca8f298`，按SHA選新13全句＋未變context2＋未變old16，不拼字；16anchors與完整31句重播已驗。實際server完成16:15:27台北；原verified-receipt.at被prepare物件展開覆寫，已保留原收據及raw並以timing companion說明，v2強綁旁證，不虛構精確finalize時間。完整收據[audio-qa-retake1-asr.json](audio-qa-retake1-asr.json)。原PID2401已結束，不要重跑ASR。

16:01最初的本機啟動因Windows `--import C:/...`得到`ERR_UNSUPPORTED_ESM_URL_SCHEME`，native1；helper與CLI都未載入、diagnostic檔未建立，21檔未變、journal空。已保存啟動與對帳收據，獨立無害control確認改`--import file:///C:/...`才可載入；之後使用全新`tts-after1600-fileurl`槽位完成上述唯一正常provider續試。這個local startup failure不計provider refusal或成功重錄，舊槽位不得重播。凍結helper SHA未變，實際觀測非2xx紀錄0筆；沒有為診斷額外probe。後續Windows呼叫一律使用file URL。

11:40退避後已只正常續試一次，session21401保存native_exit=4，仍為相同Gemini忙碌／用量限制；dry-run13句／242字元，站內月額度5743335。21個凍結檔案全未變、audio_evidence0問題、journal全空且lease已釋放，成功重錄輪數仍0，沒有新ASR或新集。原始dispatch／native exit／result均保留，見[speech-retry-20261027-1140.json](speech-retry-20261027-1140.json)；不要重跑`tts-after1140`的已結束槽位。**下次不得早於16:00台北（08:00Z）**，至少240分鐘退避後再正常續試一次；若仍受限繼續延長，不推定供應商重置時間，也不變更聲音、供應商或全域預算。現在五個語音指令都沒有完成重錄，不等同已做五輪音訊品質重錄。

09:30退避後已只續作一次，session16091於09:35:57派送、結束後立即保存並傳遞native_exit=4；仍為Gemini忙碌／用量限制。dry-run13句／242字元，站內月額度5743335。21個凍結檔案全未變、audio_evidence0問題、journal全空、lease已釋放、成功重錄輪數仍0。原始dispatch與native exit收據均保留，見[speech-retry-20261027-0930.json](speech-retry-20261027-0930.json)；不要重跑`tts-after0930`這個已有dispatch/exit的槽位。沒有新WAV，所以沒有啟動ASR、重合成或新集製作。**下次不得早於11:40台北（03:40Z）**，至少120分鐘退避，再只正常續試一次；仍busy/quota則繼續延長退避，不推定日額或重置時間。

已將「Gemini合成429缺少安全結構診斷」另開P2未認領票`2026-10-27-preserve-safe-gemini-tts-429-diagnostics`，只追蹤adapter/serverlog觀測資訊，不在本影片票改共用工具、設定或部署；該票記錄與pilot-budget票的scope碰撞，實作前仍須查持有者。現有accesslog不足分辨provider busy與quota，不為取得錯誤碼而另送付費probe。

已準備並在成功續作中使用的私有唯讀transport觀測：`curio-s31-v2-preflight/curio-tts-transport-diagnostic.mjs`，凍結SHA `df217e9f22be3f52220d94f7fbab84ac301d022643fa31a2f1c8238f143aace9`。獨立static及4組離線mock測試通過，165次mock皆只呼叫原fetch一次，保留原Promise／Response／例外，不新增網路或重試；只記實際本機API非2xx的HTTP碼、有限白名單problem.code與有界Retry-After秒數。見[speech-transport-observer-20261027.json](speech-transport-observer-20261027.json)（離線準備快照）及上方實際續作收據。Windows須用bundled Node `--import file:///C:/Users/x8120/mokaair-work/curio-s31-v2-preflight/curio-tts-transport-diagnostic.mjs`；`CURIO_TTS_TRANSPORT_DIAGNOSTIC_FILE`只設全新唯一JSONL basename（省略會自動產生唯一名），收據保留在preflight。不可重用舊檔或為診斷多送probe；basename無效／已存在時helper會不啟用觀測而保留原fetch，不會攔住CLI。仍須立即保存並傳遞native exit。它無法還原server丟掉的provider quota body或證明重置時間。

09:06台北站主要求「繼續」後再次唯讀核對：source/script/preview SHA、speechHash、visualHash均與驗證收據相同，audio_evidence0問題、13flags未變、journal全空、lease與本集producer皆無。尚未到09:30，不因一般「繼續」提早重送。另以本機無害退出碼對照確認PowerShell會把未明確傳遞的native非零碼包成外層1，見[speech-exit-scope-20261027.json](speech-exit-scope-20261027.json)。未呼叫provider、未改聲音或預算。今後CLI結束後立即保存並傳遞`$LASTEXITCODE`，將native碼與外層shell碼分開記錄；43490當次native碼沒有保存，不能事後追認成4。

重錄前的EN render session98057與補產CC均已exit0。[production-preview-r6.json](production-preview-r6.json)是08:46:47台北的歷史完整驗證快照：當時source/media綁定、129圖、八語文字覆核SHA、配樂與原版成片SHA核對通過；重錄後不能用它證明舊成片與新旁白相同。原版final SHA仍保留`64896215da89ee6f978d3d9e0b41600eacf9b3c21827a1462a955429637343af`。

**下一個可行動斷點是兩個剩餘疑句的獨立發音覆核**。若只是同音字，依listener規則保留原句並記錄委託品質判斷及官方原2flags；不假稱Jev自動全過或人工聽音。若證據不足，尚有第2輪受保護措辭機會，不能無限重錄。音訊獲實際可追溯決定後才render／clips／既有music驗證／assemble／captions／QA／新播放器驗證，再核准中文final、逐語製作八條dub。尚未完成完整交付包，不能勾整集完成或開始S15。

- 配對已恢復，不再要求站主重配。guarded keyframes最後session `7898` 已正常完成：129/129張judge通過，沒有needs_review；官方keyframeProblems為0，visual_hash `4ff8941e6473b9f4`、speechHash `8af0af8b6fb7d1e4`。六頁最新圖板已由代理實際檢視，依站主推薦選擇委託記錄storyboard核准，並非站主本人觀看。manifest SHA `fe9acad25cb819acd8628709e94550699a325408fc3e3e8e1982b6a2fe4dccf2`。
- 圖片／評審帳本US$1.3905、保守HTTP嘗試控制總額US$1.578（包含歷史重試不確定量US$0.17），低於US$6；無pending media jobs與保留額。原通過圖保留，只修正consort-basket、049、058、072、074、080耗盡take後的prompt，所有paid failed takes與判定已備份；稿件／聲音／敘事核准綁定未變。
- render session `78493`已exit0：233states全沿用、27秒、0layout錯誤；九語縮圖及卡片圖板與先前實際檢視的10檔SHA一致，frames已重綁current visual_hash。clips正式執行exit0：129stills、0clips、0新購。music正式驗證原track SHA通過。
- assemble session `96823`已exit0：150/150segments，1702秒；成片29159frames／30fps＝971.966667秒（16:11.967），片頭在frame1574／52.466667秒插入，intro150frames、v4outro630frames；-14LUFS／truepeak-1.9dBFS／musicbed-33.1LUFS，checks.ok=true。預覽final.mp4 SHA `023c6407ebaa7e5c928af287e31dc1bbad429d28726b33ea92e0a0d2c55f318e`，302331298bytes。獨立凍結讀回21/21檔SHA通過；原生播放器已驗開場進度、中段跳轉、片頭、v4片尾及正常ended=true／error=null，實際container972.005秒（AAC padding）。只做抽查，沒有宣稱全片連續觀看、人工聽音或站主本人觀看。九語CC已按片頭插點重產；ja2／es3閱讀速度警告留待實際配音時間修正。
- TTS session `43490`外層PowerShell觀測exit1，原native碼未保存，仍回覆「Gemini 語音暫時忙碌或達到用量上限，請稍後重試」；這輪沒有直接取得HTTP碼，不能擅自確定日額或重置時間，也不能只憑shell1推定provider錯誤類別變化。凍結21檔逐一讀回全未變、所有audio_evidence為0問題、speech-journal仍全空，成功重錄輪數仍0；private `tts-retake-context13-result.json`保留原始觀測。**下一次語音續作不得早於2026-10-27 09:30台北（01:30Z）**，且須重查當前WAV／journal與active producer，只正常續試一次；再忙碌則加長退避，不換供應商／聲音或提高全域預算。dry-run13句／242字元、月額度5743335只代表站內額度，不保證provider可用。
- 第一輪完整QA9/11：音訊未核准，另因新版尚無server project row而被預設問教學示範。已以官方`review-push --report-only`只登記本集format=drama/category=explainer，GET前404、後200且video_id=null／reviews=0，沒有送審或上傳影片。按正確分類再跑QA，policy通過（demo不適用），目前10/11只剩narration；保留前後兩份報告，不偽造原判定。
- EN/PT/ID三張外語縮圖改短標語，已逐語互審、保存後讀回，sub/title/description/212captions與voice均不變；最後render98057已exit0、233states全沿用，三張實圖已查看，同一官方縮圖檢查分別28／26／30px（320px寬），均pass、無警告。完整QA10/11報告產於最後EN備案之前，因此保留其當時EN23px警告；最新收據另列已解決的targeted follow-up，不篡改原報告，也不只為標語變動反覆消耗policy judge。CC已補產。不要為了消除未來配音時才應處理的CC速度警告刪事實。
- 獨立離線context Whisper已exit0：52個鄰句fresh無提示轉寫，再逐一辨識15個原始target WAV；提示只由固定鄰句實際聽到的轉寫組成，沒有傳原稿或先前target猜測。private `context-whisper-r6-20261027T074158/`保存原始JSONL、WAV SHA、實際prompt與verified receipt。獨立覆核PASS的新reader已接入官方check-audio：212/212檢查、18句second transcript排除疑慮、**13flags仍保留**，0新ASR／1Jev call；log `check-audio-context-r6.txt`。舊check及低分判定保留在`check-context-r6-before/`，沒有擇字拼成符合原稿的ASR。
- 三次語音指令均未完成重錄（前兩次429／exit4，最後一次busy/quota訊息／外層shell1、native未保存）；不要把拒絕請求算成成功重錄輪數。仍有13flags；不能提前核准audio／final、封完整交付包或開始下一集。

### 先前履歷（不能當作當前執行狀態）

2026-10-27早上站主重新配對並回覆「完成」，官方login session `46042` 已exit0、權杖正常寫入；連線阻塞已解除，不要再開配對。正式 `check-audio` 已吃入先前31句獨立Whisper：212句檢查完成、16句排除初輪疑慮、15句仍標記。

首次局部重錄 `tts --redo` session `75434` 已exit4，供應商回覆Gemini忙碌／額度限制；逐檔讀回15個WAV均未改變，不把這輪寫成重錄成功，也不啟動新ASR。dry-run277字元、站內月字元額度充足，仍可能是供應商忙碌／每日限制。原15個WAV、原旁白、timeline與兩輪check已先保存 `audio-retake-r1-before/`，沒有改稿或聲音設定。待語音供應商恢復再續同一個有journal的重錄清單，避免立即重送；重錄後的WAV不能用舊Whisper結果。

圖片續作session `98884` 已exit0：consort-basket新提示take1通過，v2-add-037沿用已付take1後按judge修正、take2通過；新生成2張，目前91/129張通過、剩38張，帳本US$0.5265。原89張通過圖與判定均保留。

語音首次重錄清單的退避續作session `25880`（距前次最後429約37分鐘）也已exit4，同樣供應商忙碌／額度限制；15個WAV再次驗SHA全未變。private log `tts-retake-r1-retry-after-backoff.txt`。先暫緩語音，不推測日額重置時間；下次最多一次正常續作不得早於2026-10-27 08:15台北（private `tts-backoff-state.json`），仍429則加長退避，不連續重送，不改供應商／聲音。16個來源URL已用官方相同link checker逐一GET，全部200且無redirect；私人收據 `source-links-preflight-20261027.json`，不取代最終組合說明欄QA。

剩餘圖片將使用已獨立靜態覆核的私有 `curio-media-budget-guard.mjs`，SHA `fb5e96f2f216d395daa3dda97c3092c7ff72bf5f6dd3a7f9d1be2e15f0324bf1`，Node --import在每次images／judge的實際HTTP嘗試前記錄估算費用並以US$6拒絕超額；不改全域設定、核准或judge判定。state `media-budget-guard-state-r6.json` 已初始化：baseline US$0.5265，前段未記錄重試的保守量US$0.17（原US$0.05＋B1三次邏輯judge最多額外4次各US$0.01），attempts空白。**不得重設／rebase這份state以抹掉已記錄嘗試**。這是依工具單價的保守費用控制，不冒充供應商發票實額；等當前語音程序結束及lease釋放後，再以guard續完整keyframes，不用force。

當前製作程序是guarded keyframes session `3593`，log `keyframes-guarded-r6-rest.txt`，已開始剩38景；91張通過圖均顯示kept。先等它正常結束，再讀manifest／jobs／帳本／guard state，處理三次未過景及新鮮SHA-bound完整圖板；不得與它競爭lease。音訊QA仍15flags，後續若先合成中文版，只能記為待音訊修正的預覽，不能核准成片、封完整交付包或開始下一集。

S31 本機工作目錄 `~/mokaair-work/videos/curio-s31-v2/`；外部收據與執行紀錄在 `~/mokaair-work/curio-s31-v2-preflight/`。`tts` 已完成：171請求、4,430計費字元、旁白28,379格／30fps＝15:45.967。212句語音片段合計12:53.440；其餘主要是工具預設句間與換景間隔，發聲語速約在4–5字／秒目標內。

第一輪 `check-audio`（session `73612`）已結束：212句中148逐字一致、29同音／口語差異、4句Jev判通過、31句仍標記；沒有提前核准音訊。31句的原始WAV雜湊及順序已存 `whisper-input-r6.json`。本機session `37037`／Python pid `42156` 已在原生主機首句驗證成功後，只終止本集自有程序；停止與部分輸出收據保留，不再續等該PID。

原生VPS的cached Whisper medium離線批次已完成31/31、exit0、4分42秒、stderr空白；無新模型下載／供應商請求。private `whisper-native-vps-r6-20261027T003938/verified-receipt.json` 綁31個WAV與原始輸出SHA `d402c92532b7fcac4cc7aaca7307b96b2922255ae6495691f181954d6f23e12d`。`whisper-verified-reader-r6.mjs` 只在輸入SHA相同時重播真實轉寫，給官方check-audio的second-opinion；不能對重錄後的WAV重用。離線官方比對函式診斷為11句直接吻合、5句兩轉寫錯在不同位置、15句仍需Jev／實音判讀；這份diagnostic不是音訊核准。待憑證恢復後用官方check-audio+已驗證reader，不再重跑31句ASR。

`keyframes` 初次session `29556` 因讀取回應 ECONNRESET 中止；bundled Node24.19.0 的續作session `91825` 也已結束（HTTP502），log `keyframes-resume-r6.txt`。v2-add-037 seed1已下載並快取，尚未記下judge，不能重新生成；目前先對帳再續跑。產線實際保留65張舊圖判定，consort-basket三次未過，已在程序停止後改成簡單室內單人prompt；旁白及敘事綁定未變。live全量報價仍US$5.22，總圖片／評審上限US$6。

已發現斷線後重評會改變修正字句、另立請求鍵的工具問題，另開 `2026-10-26-persist-keyframe-take-verdicts-before-network`，不修改別人持有的工具。舊orphan已用取回的原圖、官方cache helpers及新鮮伺服器唯讀ready／費用收據完成離線對帳，未新增網路、生成或評審請求；`connection-reset-r6/cache-reconcile-complete.json` 綁定恢復的cache檔案，pending已結清，帳本仍US$0.4895。保留全部原始收據。**不要再提交／評審這筆舊圖，也不重複入帳**。再次中斷先核對現有job與每次judge，不盲重跑。

2026-10-27恢復檢查發現私有下載helper把 `readCredentials()` 回傳的 `file` 一起展開，覆蓋了下載目的地，造成圖片寫入本機憑證檔；目前已改為只傳site/token，圖片已取回至原收據所記位置並驗SHA。原權杖無可用備份，官方login配對session `71830` 已逾時，需站主在新配對管理頁允許；未恢復前不重送付費指令。這是連線帳號斷點，不能以重新生圖處理。伺服器唯讀確認37張ready、1張failed、無pending媒體／stage／budget operation；成功judge帳本36次，但502處judge無逐片操作ID，確切費用無法還原，另保守保留US$0.05不確定量。當前保守總額US$0.5395，仍計入US$6上限管理。

外語沿用原集八語選擇（en/ja/ko/es/pt/id/vi/th），八份212行工作表已全填、獨立覆核、修正及merge，仍是待音畫實測的候選。**不要重跑i18n-sheet覆寫工作表**。en/ja修正12／7項、ko/es修正14／17項、pt/id修正10／8項、vi/th修正4／5項，八語最終delta均已由獨立覆核者讀回，private八份review均有SHA-bound文字ready決定。泰文description另縮至1292 bytes並獨立覆核通過；composed預期4935 bytes，current lint為0 errors/0 warnings。配音等中文版定案後才生成。

每語212行中159行新譯／改譯、53行來源相同仍完整覆核。初始每行max_chars是保守估算，極短窗口無法兼顧完整姓名與自然語言時保留忠實稿並列例外，由實際整個分鏡窗口配音量測處理，不以刪事實換取字數。原始時間軸的zh-TW.srt已由官方captions命令產生212 cues；最終加品牌片頭後須重產偏移。配樂已由原始已付曲目離線交叉淡化6遍、4秒接縫，延長至976秒，current track `curio-s31-v2-bed.m4a` SHA-256 `a00ffb8aa48c83041867c2ea319ff962b21b6510cb9e97030711ef73e9518a41`，新購費用0；收據 `music-reuse-r6.json`。

離線預覽render session `7717` 已exit0：644秒、21張字卡＋212段字幕strips＝233 states，無layout錯誤；中文及八語縮圖已逐張看過，字卡聯絡表21張也已查看。只核對預覽版面，沒有完整分鏡、成片或播放器驗收；`render-preview-review.json` 記錄實檔SHA及檢查範圍。全九語原始時間軸CC已產出，其中ja兩句、es三句閱讀速度警告留待實際配音／最終字幕重測。不要把raw CC或這份預覽當作最終上架包。

本聊天的續作 heartbeat 已建立，automation id `s31`，每20分鐘依實際斷點接續；狀態不變時不發通知。七集的完整交付包均驗證完成後停用。
