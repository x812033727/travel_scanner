# S31 新規則版製作與報價（2026-10-26）

新稿：[script.md](script.md)。原標題保留，使用獨立 slug `curio-s31-v2`。原版 `curio-s31` 的成片、旁白、插圖、外語及核准仍歸原工作與 PR #1800；本次不覆寫它們。

## 當前讀回（2026-10-28）

最新 checkpoint（2026-10-28 14:37Z停止／獨立對帳完成）：Root通過14:35Z退避、fresh226原件／204refs與normalized guard0，讀官方dry-run native0／ready quota4,604,093後，開唯一正常續作3（29491／official58664，dispatch14:36:16.077Z、lease14:36:17.270Z）；已於14:37:02.030Z **native4停止，5次429／video_speech_upstream_busy／retry-after10，非EPERM。** 獨立讀回確認原226 copies／current pairs、79句raw／key全部不變，**本slot新增完成take0；剩133個新請求／2,811字元、0 saved。** 這不是零費用證明；dryrun分組105／3,203也不是逐句完成／計費量。134journal exact／active與unknown0、PID退出／lease absent／normalized process0，EN source／成片／flags／completed ASR及四份封存完整。Root第二次JA busy退避延長至**不早於2026-10-28T15:40:00Z（至少60分鐘，本地決策，非provider reset）**；屆時fresh對帳並讀新dry-run quota後才可另slot正常續作，不重播resume3／212、不改provider／limits／30秒I/O或自動重試。fit／QA未知、JA成功品質重錄0，EN unchecked結案1/8、0/8 accepted，其餘6語待做；圖片預算／完整包／S15不變。見[JA續作3 busy停止收據](dub-ja-first-resume3.json)。 續作4於R4僅source審查通過，dry／paid未用且尚無quota；15:40Z後fresh核對→一次dryrun native0實讀log／quota≥4,504且20分鐘內→另slot paid綁fullSHA，見[續作4準備](dub-ja-resume4-preparation.json)。

歷史JA續作2 busy停止快照（14:02Z；已由續作3停止取代）：JA續作2／78919已於14:02:46.449Z **native4停止，5次HTTP429／video_speech_upstream_busy／retry-after10，這次不是EPERM。** 獨立226檔對帳確認原78句raw／key保留，新增lz315來自92b8保存回覆的官方trim／encode正常沿用，現79句有效；raw response326,444B與處理後clip270,764B／SHA892cb1eb…4920明確分列，原15字元與6份recovery proof／tmp保留。**剩133個新請求／2,811字元，0未消費saved；不是完成／計費量。** 134journal fullSHA／會員保留、active／unknown0，PID已退出、lease absent、fresh normalized process0；EN成片／flags／ASR與四份封存完整。Root固定退避**不早於2026-10-28T14:35:00Z**，這是本地決策不是provider reset；同樣拒絕就延長。屆時先fresh核source／cache／journal／quiet與唯一新dry-run額度讀回，再由Root決定新正常slot，不能重播212／舊slot／自動重試或改provider／limits。fit／QA未知、成功品質重錄0；EN unchecked結案1/8、0/8 accepted，其餘6語待做，圖片預算／完整包／S15狀態不變。見[JA續作2 busy停止與退避](dub-ja-first-resume2-stop.json)。

歷史prepared-only交接（續作3已使用並停止，source候選仍未啟用）：續作3 recipe與獨立靜態review已凍結，dry-run／paid兩槽未用、皆硬擋14:35Z前，尚無新quota。下次先fresh讀source／79 current／剩133新請求2,811／134journal／quiet，再由Root只跑唯一新dry-run；native0後讀原log建立綁實際證據與20分鐘內時間的quota（≥4,504保守），才可另slot一次paid。JA collector／source-free bridge port已generic獨立74 PASS／1 symlink skip／0 fail，僅source／離線fixtures，不是actual cohort、H5、binding、啟用或ASR；64句／80MiB／20分鐘門檻保留，EN completed與四份封存不動。現有normalized9003 guard只涵本次未啟用JA合成，未來JA-ASR新root須另審守衛。見[JA下一步準備收據](dub-ja-next-preparation.json)。 H5兩碼source-template獨立36/36／0 skip通過，仍不可執行，actual inventory／caller／JA guard／啟用待備；見[H5準備收據](dub-ja-handoff-source-preparation.json)。

歷史JA正常續作2 dispatch快照（14:01Z；78919現已因busy停止）：92b8／lz315保存合成回覆已由原始checker native0／private reused1 send0 fetch0與獨立actual review通過；Root222檔凍結確認**78句有效、134句／2,826字元待處理含saved15，計畫新133請求／2,811**。前筆66d6／v2a0291已獨立確認canonical正常trim／encode消費、原67句保留及新11句有效。新recipe已先靜態PASS，外部normalized process guard通過6正／6負fixture並fresh0，Root重核222原件／199refs及ready quota4,614,770後，開**唯一正常續作78919／official58296（dispatch14:01:48.202Z、lease14:01:50.157Z）執行中，等待native。** 舊predicate限制保留揭露，不回溯宣稱舊recipe全PASS；原I/O額外30秒／無redo／force／自動重試不變。92b8本筆canonical消費、實際新calls／計費、fit／QA仍未知；不釘moving log，不重播舊slot／212或開第二producer。EN unchecked結案1/8、0/8 accepted，其餘6語待做，EN ASR及四份closure保留；圖片預算不變，完整包與S15未成。見[JA正常續作2](dub-ja-first-resume2.json)。

歷史JA續作1停止快照（13:27Z；前筆66已核驗、新92已另slot續作）：JA正常續作74740／official7608於13:27:47.602Z **native1停止，新request92b8ccf3…ef486的confirmed journal rename再遭Windows EPERM，非fit／品質結果。** native與完整log已固定，partial raw／cache／實際剩餘範圍待Root凍結，前筆66d6／v2a0291雖已越過日誌，canonical正常消費仍待獨立讀回，不先宣稱成功。另披露本slot recipe在dispatch後靜態審查發現CIM路徑分隔符predicate可漏掉反斜線；沒有完整獨立recipe PASS，不把它宣稱為EPERM成因。下一次製作前Root須以fresh normalized process guard與精確journal對帳守門。原145／3,058含saved28、新144／3,030均只是dispatch時計畫，實際完成／計費與fit／QA未知；保留原slot，不重播212／full redo／自動重試／手動升格或清journal。**EN unchecked結案1/8、0/8 accepted；JA部分合成停止，其餘6語待做。** 圖片預算不變，完整包與S15未成。見[JA續作1停止收據](dub-ja-first-resume1-stop.json)。

歷史JA正常續作1 dispatch快照（13:26Z；74740現已停止待新對帳）：66d6／v2a0291的完整保存合成回覆已由原始private checker與獨立actual review通過（private reused1／send0／fetch0）；Root凍結201檔，確認67句raw／cache有效、120歷史＋4actual＝124份journal。Root fresh201原件與206refs、讀官方dry-run native0／ready quota4,642,806後，已開**唯一正常續作74740／official7608（dispatch13:26:33.205Z、lease13:26:34.444Z），等待native。** 待處理145句／3,058字元含保存答案28，故計畫新144請求／3,030；這些都不是實際完成／計費。雖log已越過v2a0291，canonical實際消費仍待native後核驗，fit／QA未知；dryrun分組114／3,492不當逐句量。沿原IO30秒、無redo／force／自動重試，不能重播舊slot／212或啟第二producer。JA-ASR僅唯讀差距方案，未啟用／建cohort，須保留EN完成state／run與四份closure。**EN unchecked結案1/8、0/8 accepted；JA執行中、其餘6語待做。** 圖片預算不變，完整包與S15未成。見[JA正常續作1](dub-ja-first-resume1.json)。

歷史JA首次停止快照（13:10Z；已覆核保存答案另slot續作，canonical消費待驗）：JA首次合成9813／official58696於13:10:31.3270782Z **native1停止，confirmed journal rename遭Windows EPERM，非fit／品質判決。** exact request66d6efe4…dd36a與.tmp .58696已由native／完整log固定；Root回報PID已退出，正核partial cache／WAV／保存答案與實際剩餘範圍。原212 requests／4,504僅離線計畫，不當實際完成／計費或剩餘量；實際fit／QA仍未知，初次部分合成不算品質重錄輪。空的synthesis observer不代表零HTTP／零費用。保留舊dispatch及所有原檔，不能重播212、full redo、手動升格／清journal或開第二producer；只待Root凍結與逐筆覆核後決定新正常continuation。**EN unchecked／skip已結案1/8、0/8 accepted；JA部分合成待對帳，其餘6語未始。** 圖片預算不變，完整包與S15未成。見[JA首次合成停止收據](dub-ja-first-stop.json)。

歷史JA首次合成dispatch快照（13:05Z；9813現已停止待對帳）：Root讀回JA fresh195項refs與英文skip證據、官方dry-run native0後，已開**唯一JA首次合成9813／official58696（dispatch13:05:20.657Z、lease13:05:21.576Z），等待native。** current JA212句有效／missing0，離線逐句計畫212 requests／4,504 billable；官方dry-run分組估計171／5,078不可當逐句實際量，monthly4,689,563只是ready快照。尚無實際合成總量、fit、品質或驗收結論；維持Gemini Sulafat／標準日語、原IOv2額外30秒與file-URL observer，無redo／force／自動重試，不為JA合成清理英文ASR state／run。**EN已unchecked／skip結案1/8、0/8 accepted；JA執行中、其餘6語未開始。** 下一heartbeat先等本slot native並核partial cache／WAV／journal，不能重播212或開第二producer；圖片預算不變，完整包與S15未成。見[JA首次合成dispatch](dub-ja-first-dispatch.json)。

歷史EN最終品質與unchecked結案快照（12:50–12:59；JA未付費僅指當時）：71837已**native1完成完整品質判定，非infra：212＝164 exact＋14 Jev通過＋29 second解除＋5 flags，207句解除。** lz213新解除；保留lz411／v2a0611／lz506／lz513／v2a0791及原分數。五句獨立覆核後，Root依DUBS已實際寫入EN skipped：**本輪英文結案為unchecked、正常配音交付略過，並非accepted；1/8嘗試已結案、0/8 accepted，其餘7語待做，下一語JA。** current en.m4a與212 raw／fit／字幕文字／metadata保留，官方pure readback為normal dubs0／unchecked EN1附5句時碼，不代表已產正式CC或自動上傳。plain2/2＋listener2/2已用盡、shorten0，不再第3輪。末段CLI5筆primary／2次Jev／0保存沿用，不推整鏈費用；runtime獨立PASS：新4＋有效cache30＝34 second，Whisper0／28.175秒、callback31.892秒，4CPU／nice19／offline／無稿／單SSH close0與local reaped，120journal active0、state／run保留，遠端scratch刪除未證。lz513同音保留不清flag／低分，沒有任何實聽或音訊核准。JA離線212／4504計畫已準備，未付費；圖片預算不變，完整包與S15未成。見[EN最終品質與unchecked結案](dub-en-listener-reword2-check-complete.json)。

歷史listener2品質檢查dispatch快照（12:49Z；71837現已完成）：H4 closure77980已native0，253副本＋11anchors＋18移動原件＋relocation＝283檔／ledger6經Root與獨立完整讀回，三份舊封存275＋6、283＋6、283＋6保留；Root activation、preinstall0及新binding排他安裝完成，新212 cohort已獨立通過。Root已開**唯一正常英文品質檢查71837（caller40824／official53496，intent12:49:19.694Z），等待native；尚無新版flags／runtime結果。** callback保持source-free、同名bridge、20分鐘總上限及原30秒I/O preload；Root為callback補bundled Node PATH，外層finally還原環境。固定slot已用不可重播／另開producer。plain2/2＋listener2/2已合成、shorten0，舊6flags不充當新take結果，lz513原scores／flag保留；0/8 accepted，圖片預算不變，完整包與S15未成。見[listener2品質檢查dispatch](dub-en-listener-reword2-check-dispatch.json)。

歷史listener2合成完成快照（12:33–12:34；後續handoff／check狀態僅指當時）：listener2合成48611已於12:33:05.2651135Z **native0完成五句新文字／raw與混音；plain2/2、listener2/2已合成完成，新品質待檢。** 官方5 requests／262 billable、166 request groups沿用；獨立actual覆核確認目標5句全部new SHA、其餘207文字／raw／metadata保留，全212 raw、177前件副本、120歷史journal active0與舊ASR state2／run15／binding全18檔不變。實測150窗0over、8窗≤1.15，cheng-date0.1秒及v2-add-0790.03秒由後停頓吸收；新軌a56fc2ea…10d45／46,585,183B／969.705秒，full decode native0／−14.1LUFS／LRA5.1／true peak−2.0dBFS，只是技術驗證。前6flags中5句對應更新前take；lz513保留同一take／文字、原0.17／0.16與flag，不是自動清除或實聽。新cohort／ASR／QA須另走實際關卡，generic PASS不是啟用；shorten0，不做第3輪原文或listener合成。**0/8 accepted**，圖片預算不變，完整包與S15未成。見[listener2合成結果](dub-en-listener-reword2-result.json)。

歷史listener2合成dispatch快照（12:28Z；48611現已完成）：listener2五句措辭已獨立語意覆核、官方merge完成（EN3b1f40f2…43501，其他207句／metadata不變）；Root已dispatch **唯一合成48611／official46588（12:28:27.467Z，lease12:28:28.592Z），等待native與實際音檔／fit對帳。** 本輪計畫5 requests／262 billable、207行沿用，尚非完成量；plain2/2、listener1已合成，listener2僅本次執行中。最新官方dry-run native0讀quota4,733,976≥262，為共享額度快照；前置alias錯誤與時區解析誤判都在CLI／paid dispatch前，原時間並未過期，舊recipe保留，並非付費重試。lz513依current兩ASR的Mount Li／Lee同音證據保留原文字／take，原0.17／0.16及flag不清，不是音訊驗收／實聽。舊6flags保留，新版品質未檢；0/8 accepted，圖片預算不變，完整包與S15未成。見[listener2合成dispatch](dub-en-listener-reword2-dispatch.json)。

歷史listener1完整品質快照（12:00–12:08；listener2尚未套用僅指當時）：listener1正常續檢76955已**native1完成完整品質判定，非infra：212＝163 exact＋14 Jev通過＋29 second解除＋6 flags，206句解除。** 實際6句為lz213／lz411／v2a0611／lz506／lz513／v2a0791；新版cache與flags已另存immutable副本，原分數／flags保留。lz513／76efd的58B保存答案已獨立確認canonical正常沿用，210筆有效primary保留、6處合法annotation更新、120份journal active0。末段CLI僅1筆新primary／2次Jev／1保存沿用，不推整鏈付費call數。Runtime獨立PASS：新8＋有效舊cache27＝35 second，Whisper native0／90.718秒、callback94.414秒，4CPU／nice19／int8／offline／無稿／單SSH close0與local reaped；lease absent、無holds，state／run保留，遠端scratch刪除未證。plain2/2＋listener1合成完成、shorten0，下一步只準備受限listener2候選與語意覆核，尚未套用／合成，不做第3輪原文重錄。**0/8 accepted**，圖片預算不變，完整包與S15未成。見[listener1完整品質結果](dub-en-listener-reword1-check-complete.json)。

歷史listener1正常續檢1 dispatch快照（11:59Z；76955現已完成）：76efd／lz513的58B完整保存答案已由原始private checker native0／reused1 send0 fetch0與逐筆actual review通過；148份凍結、212 raw、114歷史＋3actual＝117份journal及Root fresh358次原件SHA已核。Root另開新slot的**唯一正常續檢76955執行中（caller32228／official43356，intent11:58:59.322Z、lease11:59:00.092Z），等待native與保存答案canonical消費／新品質證據。** 不宣稱second已完成或零費用；closure／activation保持有效，既用slot不重播，不能開第二producer或第3輪原文重錄。plain2/2＋listener1合成完成、shorten0；舊12flags歷史，0/8 accepted，圖片預算不變，完整包與S15未成。見[listener1正常續檢1](dub-en-listener-reword1-check-resume1.json)。

歷史listener1首次check停止快照（11:51Z；已另slot正常續檢，保存答案消費待驗）：listener1 的新cohort封存／啟用已完成，H3 closure23025 native0；新283檔／ledger6及兩份前封存275＋6、283＋6均完整保留。唯一品質檢查15049（caller41372／official55244，11:49Z dispatch）於11:51:27.708Z **native1停止：primary完整保存答案的confirmed rename遭Windows EPERM，尚無新版品質結果。** request76efd856…dbea83的sent／answer／tmp為443／1286／758B，Root正凍結並安排原始private checker與逐筆覆核；不猜line、cache、second完成或費用。成功closure／activation維持有效，舊slot不重播；只能對帳後由Root另開正常continuation。plain2/2＋listener1合成完成、shorten0，**舊12flags只屬前take；0/8 accepted。** 圖片預算不變，完整包與S15未成。見[listener1品質檢查停止快照](dub-en-listener-reword1-check-dispatch.json)。

歷史listener1合成快照（11:23–11:27；後續handoff／check狀態僅指當時）：英文listener改口第1輪96080已於11:23:07.1918944Z **native0完成12句變更文字合成，plain2/2＋listener1完成；新品質仍待檢查。** v3措辭已逐句語意覆核並由官方caption merge套用，EN SHA e6e8e1c3…75ef7；僅12句文字／raw更新、其餘200與metadata保留，Chinese/source／voice/provider不變。官方12 requests／522 billable、159 request groups沿用；獨立actual稽核確認212 raw、153份前件、14 stretched、114歷史journal全保留active0、lease absent，舊ASR state2／run15／binding未改。實測fit150／0over、8窗≤1.15，cheng-date0.1秒由後停頓吸收；新軌a1814473…c729／46,583,753B，full decode native0／−14.1LUFS／LRA5.1／true peak−2.0dBFS，只是技術讀回。**原12flags對應舊take，不能稱新12fail；0/8 accepted、shorten0。** 現只準備新cohort，ASR handoff／新QA尚未執行；圖片預算不變，完整包與S15未成。見[listener1合成結果](dub-en-listener-reword1-result.json)。

歷史第2輪後品質結果（11:01Z；12flags屬listener1改口前take）：37111已native1完成完整品質判定，非infra：**212＝159 exact＋14 Jev通過＋27 second解除＋12 flags，200句通過檢查。** 相較前15句，lz221／lz427／lz520已解除，下一步只針對actual current12準備listener第1輪與語意覆核，目前0套用、0合成；plain2/2已達上限，不再第3輪原文重錄。lz213／4ba7保存答案52B已獨立確認canonical正常沿用；末段CLI為13筆新primary／2次Jev／1保存答案沿用，不推整鏈付費call數。Runtime獨立PASS：新13＋有效舊cache26＝39筆second，Whisper native0／111.381秒、callback115.241秒，4CPU／nice19／int8／offline／無稿／單SSH close0並local reaped；state／run保留，lease absent、無holds，未證遠端scratch刪除。0/8外語驗收，圖片預算不變，完整包與S15未成。見[第2輪後完整品質結果](dub-en-retake2-check-complete.json)。

歷史正常續檢1 dispatch／second-stage快照（37111現已完成）：4ba7／lz213保存答案的原始private checker native0／reused1 send0 fetch0及逐筆actual review已PASS。Root fresh352次原件SHA（已含212 raw）與111份journal後，開新slot的**唯一正常續檢37111執行中（caller51708／official18284，intent10:57:38.380Z、lease10:57:39.183Z），等待native與canonical實際消費驗證。** Root最新讀回fixed ASR state已含1511B的reservation.json，確認已進source-free second stage；native／runtime結果未出，pre-ASR-only continuation現在不可再用。成功closure／activation保持有效，既用slot／封存不重播，不啟動第二producer或第3輪原文重錄。plain2/2、0/8 accepted，新品質尚無結論；圖片預算不變，S15未始。見[正常續檢1收據](dub-en-retake2-check-resume1.json)。

歷史首次check停止快照（10:51Z；保存答案現已覆核並另slot續作）：H2舊scope封存88967已native0，253副本＋11anchors＋18移動原件＋relocation共283檔、ledger6及前次275檔封存均經Root／獨立完整讀回；Root activation、preinstall native0與新binding排他安裝完成，新的212 cohort／physical fit已獨立通過。其後check23135（caller57404／child8156）於10:51:02.478Z **native1停止：primary完整保存答案的confirmed rename遭Windows EPERM，並非音質判決。** request4ba7faf0…fa5899的三檔442／1278／751B保留，已凍結141檔／212 raw／108歷史＋3actual＝111份journal，原始private checker與actual review待完成；不猜line或cache數。兩PID已退出、lease／新ASR state absent、bridge runs empty；closure／activation保持有效，只可覆核後開新正常continuation，不能重播舊slot／封存或再做第3輪原文重錄。plain2/2、shorten0／listener0、0/8 accepted；新品質未成，前15flags屬舊take，private條件式改口草案未套用。圖片US$1.578／6不變，完整包與S15未成。見[第2輪後續檢斷點](dub-en-retake2-check-dispatch.json)。

歷史第2輪合成快照（10:22–10:24；後續handoff與check狀態僅指當時）：唯一原文重錄第2輪46368／PID45424已於10:22:11.6039455Z **native0完成合成及新混音，plain2/2已達上限；新品質尚未檢查。** 官方15 requests／643 billable、156 request groups沿用；獨立凍結讀回全212 raw中目標15句全部new SHA、其餘197未變，12 stretched、原108份journal完整保留且active0，PID已退出／lease absent；source／EN／中文master與舊ASR state2／run15／binding均未改。stored fit150窗0 over、7窗≤1.15倍，cheng-date多0.1秒由後停頓吸收；physical fit replay仍待已審collector。新音軌SHA51438e52…8c906，Root decode native0、−14.10 LUFS／−1.95 dBTP／LRA5.10，只是技術驗證。**前輪15flags屬舊take，不能稱新版仍15fail；0/8外語驗收、shorten0／listener0。** 目前只準備新cohort，新的ASR交接／啟用／品質檢查均未執行，generic PASS不等於啟用；不再重錄第三輪原文。圖片US$1.578／6不變，完整包與S15未成。見[第2輪合成結果](dub-en-quality-retake2-result.json)。

歷史第1輪後品質結果（09:49Z；15flags對應重錄第2輪前take）：正常續檢25284已於09:49:16.779Z **native1完成完整品質判定，並非journal／ASR故障**：212／212＝157 exact＋14 Jev通過＋26 second解除＋15 flags，共197句通過檢查。212 current clip與source／翻譯綁定均核對；本段CLI僅記2筆新primary、2次Jev、1筆保存答案沿用，前兩中斷段沒有完整counters，不用29新take推付費call總數。v2a0751／2a4b的canonical消費已獨立PASS。獨立runtime稽核通過：新19筆完整ASR與有效舊cache22合計41筆second，Whisper native0／219.153秒、callback223.101秒，4CPU／nice19／int8／offline／無稿／單SSH close0與local reaped；lease absent、無holds／uncertain，COMPLETE/state/run保留，未宣稱遠端scratch刪除。**plain完成1/2，下一步只準備剩15句的有界原文重錄第2輪；shorten0／listener0、0/8外語驗收。** 既用slot不重播；下一輪新WAV需新cohort與已審ASR交接。圖片US$1.578／6不變，完整包及S15未成。見[第1輪後完整品質結果](dub-en-retake1-check-complete.json)。

歷史正常續檢2 dispatch／second-stage快照（09:45–09:49；本slot已完成）：第二筆primary保存答案2a4b／v2a0751已完成135檔凍結、原始checker private native0／terms0／reused1 send0 fetch0及逐筆獨立恢復覆核；前筆53e／lz504的canonical消費已獨立PASS，原205有效cache保留。Root fresh346次原件SHA、212 raw與102歷史＋3active＝105份journal後，**只開新正常續檢session25284（caller19404／child51656，slot79b1e1c6…eb87，intent09:45:16.722Z、lease09:45:17.501Z），等待native exit，不能啟動另一producer或重播舊slot。** Root fresh讀回確認lease與fixed ASR state均已建立，已進獨立second stage；runtime結果尚待native與讀回，不能宣稱完成，pre-ASR continuation入口現在不可再用。本筆v2a0751的canonical實際消費仍待驗；209／212 cache及3舊SHA僅是09:36停止快照。成功closure／activation與同一source-free bridge／no-force／IOv2 30秒／callback20分鐘保持。plain1/2、shorten0／listener0、0/8 accepted、圖片US$1.578／6與S15未始均不變。見[正常續檢2收據](dub-en-retake1-check-resume2.json)。

歷史正常續檢1停止快照（09:36Z；目前續作以上段為準）：已審第一筆保存答案後的正常續檢session32438（caller6520／child57464）於09:36:27.713Z **native1停止，再遇下一筆primary完整答案confirmed rename Windows EPERM，並非音質判決。** 新request2a4be181…f78e259的sent443B／answer1282B／confirmed tmp756B保留，Root準備第二筆凍結對帳；上一筆53e／lz504的canonical實際消費仍待獨立核對。LEASE與新ASR state仍absent；成功封存與activation維持有效，不能重播任一舊slot、重做封存或啟動第二producer。停止後Root讀回209／212筆cache匹配現行clip，仍對舊SHA的3句為v2a0751／v2a0791／lz520；journal共105份。尚未推斷新保存答案對應哪句，也未形成新品質判決。plain1/2、shorten0／listener0、0/8外語驗收與圖片US$1.578／6不變，完整包及S15未成。見[正常續檢1結果](dub-en-retake1-check-resume1.json)。

歷史正常續檢1 dispatch快照（09:35Z；本slot現已停止）：上一check65243的primary保存答案request53e4101d…f5d389已凍結129檔／212 raw與96歷史＋3active journal；原始checker private native0／唯一lz504／terms0／reused1 send0 fetch0及逐筆獨立恢復覆核均通過。Root再核340次原件SHA、99份journal、212 raw、leasefree與state／legacy runs absent，依同一operation／catalog／activation開新slot，**唯一正常續檢session32438執行中（caller6520／child57464，intent09:35:34.444Z、lease09:35:35.393Z），等待native exit。** 不能重播舊slot、重做封存或啟動第二producer；canonical保存答案實際消費仍待驗。起點205／212 cache匹配現行SHA＝183筆沿用＋22筆新轉寫，7筆仍為舊SHA，不能稱205筆新take。plain1/2、shorten0／listener0、0/8外語驗收、圖片US$1.578／6不變；完整包與S15未成。見[正常續檢1收據](dub-en-retake1-check-resume1.json)。

歷史首次重錄檢查停止快照（09:25Z；目前續作以上段為準）：舊 EN-first ASR scope 已封存，closure session76805於09:15:39Z native0；245副本＋11anchors＋18移動原件＋relocation共275檔、ledger6份經Root及獨立完整讀回，Root activation／preinstall native0／新binding排他安裝均完成。其後唯一英文新品質check65243（caller40148／child46316，09:22 dispatch）已於09:25:12.217Z **native1停止：primary transcribe完整保存答案的confirmed rename遭Windows EPERM，並非音質判決。** request53e4101d…f5d389的sent／answer／confirmed tmp保留，Root正凍結對帳與核對PID；LEASE absent，新ASR state／legacy run尚未建立。closure成功保持有效；後續只可在逐筆恢復覆核後用新正常continuation slot，不能重播check-once或重做封存。plain完成1/2、shorten0／listener0、0/8外語驗收；205／212筆快取對應現行音檔（本輪新增22筆、沿用183筆），其餘7筆仍對應重錄前的音檔，原flags完整未改，新品質尚無結論。no-force、IOv2原30秒上限、20分鐘source-free callback及bridge.mjs快取名稱保持；圖片／評審保守控制US$1.578／6不變，完整包與S15未成。見[正式續檢斷點](dub-en-retake1-check-dispatch.json)。

歷史重錄完成快照（已由本次正式續檢取代；交接與待檢狀態僅指當時）：唯一partial21續作session46336／PID48028於08:28:25.3401679Z以native0完成。Root核對全212 raw：目標29句全部為新take、其他183句未變，先完成的8句原樣保留；96份journal歷史證據保留、active0。新混音16分9.705秒（46,584,728 bytes），decode native0，−14.10 LUFS／−1.94 dBTP；150視窗0 over、7個加速至多1.15倍，cheng-date的0.1秒由下一停頓吸收。**第一輪原文重錄完成1/2；新音訊品質尚待檢查，0/8外語驗收。** 新212音檔與實測fit已獨立覆核通過；lz403保存答案亦確認正常沿用；舊check屬歷史take，不能當新版通過。ASR交接僅準備、尚未移檔或啟動新check，完整交付包與S15仍未開始。見[第一輪重錄完成證據](dub-en-quality-retake1-complete.json)。

歷史 partial21 dispatch 快照（已由完成紀錄取代；段內running狀態僅指當時）：`dub-en-quality-retake1-partial23`（session31833／PID22012）於08:13:33.6032742Z native1結束，停止於下一筆語音 confirmation 更名 EPERM；212 raw累計8句新take、其他183句未變，93份journal＝82歷史＋上一筆orphan1／recovery6＋新四檔。上一筆076678／lz311p2已實際canonical沿用，原32字元與本次reuse 0分開保存；新79e359／lz403的exact whole-body、私有SPEECH恢復及剩餘21句binding均獨立通過。剩21句全付估938字元，saved41沿用後其餘20句為897。**Root已於08:23:03.9453180Z dispatch唯一partial21續作（session46336），目前等待native exit，不能開另一producer或重播full29／partial23。** fresh quota 5,070,852（08:21:47Z）僅為快照。原fit／mix／check仍非新take的品質證明，plain完成0/2、0/8外語接受；無ASR handoff，完整包未完成，S15未開始。見[剩餘21句與保存答案](dub-en-quality-retake1-partial21-journal.json)。

歷史 partial23 準備快照（已由本次partial21斷點取代；段內狀態僅指當時）：冷卻後的 `dub-en-quality-retake1-after-busy5`（session75617／PID20616）於07:51:15.8133662Z native1結束；本次已成功取得新語音回覆，停止原因是保存語音回覆的 confirmed temporary journal 更名 EPERM。已核對212 raw，其中目標29句有6句新take、其他183句未變；82份歷史journal與本筆四檔全部保存。請求076678…63e3精確對應lz311p2；私有SPEECH恢復測試與獨立覆核通過，reused1/send0/fetch0，尚未在canonical實際沿用。**續作只帶剩餘23句（全付費估1013字元；保存答案32沿用後，其餘22句最多981），不可重播原29句。** Root正準備fresh quota／來源／journal／lease核對後的唯一正常續作。原fit/mix/check仍屬舊take，不是新錄音通過；plain完成0/2、0/8外語接受，ASR handoff與S15未開始。見[部分重錄與保存答案](dub-en-quality-retake1-partial-journal.json)。

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
