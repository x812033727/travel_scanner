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
| 1 | curio-s31 | curio-s31-v2 | 第五次續作仍429／native4；212 raw未變、plain0/2、無producer；最早07:27Z（台北15:27）fresh核對。0/8 accepted |
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

最新 checkpoint（2026-10-27）：冷卻後的獨立續作 `dub-en-quality-retake1-after-busy4`（59941／PID37224）於23:26:19.0294417Z native4結束，仍是5次429 `video_speech_upstream_busy`。**獨立對帳及Root讀回確認212 raw未變（29目標／183其他皆0 changed），102項來源／mix／fit／timeline／cache／check／approval／state與82份journal全SHA保留，active／uncertain 0、PID已退出、無lease。plain仍0/2，0/8配音接受。** 最早 **2026-10-28T07:27:00Z（台北10/28 15:27）** 才可重新核對，這次延長至至少480分鐘；此前只讀觀察，不重播任何舊slot。23:24:11Z官方quota快照為5,157,716，涵蓋29 requests／1,251字元；現有錯誤未保留供應商細節，不能區分暫時壅塞與每日額度，也無usage收據可宣稱零費用。下次須fresh quota／來源／lease／journal與實際剩餘句子。見[第五次限流對帳](dub-en-quality-retake1-provider-busy5.json)；五次原始紀錄完整保留。完整包尚未完成，S15尚未開始。

窄診斷：[私有 final-diagnosis.md](C:/Users/x8120/mokaair-work/curio-s31-v2-preflight/rename-native-diagnostic-20261027/final-diagnosis.md)，SHA256 `fa648dfc294921661b21f98f795d5f3ef16002325f1358c0d8dd0948fe441f86`。本機fixture可重現EPERM，但未證實production持鎖來源或UTF8因果；沒有OS改動或上限變更。Transport observer只涵蓋synthesis，舊absolute-path配置未啟用；空檔／缺席不能證明ASR無HTTP錯誤。

**歷史快照：以下 running、最新、待核對等文字均描述當時狀態，不得用來判斷目前程序；目前狀態以上段為準。**

最新 checkpoint（2026-10-27）：97854／PID15272已於14:34:07.6598357Z native1結束，這次是**首次完整EN音訊檢查的29個品質flags，不是journal故障**。212/212＝148 exact＋13 Jev通過＋22 second解除＋29 flags；本輪22個新ASR、3次Jev及1個保存答案沿用，primary Jev累計64、second transcript共51。695b／lz514實際沿用已獨立確認，舊189筆primary／語意欄位保留，noul／second新增另列；active journal 0、82份歷史證據與舊take已凍結。**第一輪原文重錄準備，尚無producer；0/8 accepted。** 29 requests／1251官方billable字元僅離線規劃，plain 0/2、shorten 0、listener 0；14:51:49.2388142Z官方dry-run native0已讀Gemini ready／remaining 5,157,762，足夠實際29 requests／1251 billable；681次fresh checks（非unique檔數）。Root按授權準備獨立付費slot，尚未dispatch，quota只是快照並非保留額度。官方dry-run會忽略redo而報0，不能拿它代替本次實算。Second runtime獨立覆核PASS：51 subset的raw／完整實際轉寫／cache全SHA一致，nativeWhisper0／390.379s、callback396.399s，4CPU／nice19／offline／no hints；本機child close0／reaped及三PID已退出，無holds／uncertain／lease。遠端scratch刪除未證，state／runs保留未archive；無runtime阻擋另行TTS，仍非音訊核准。見[dub-en-first-check-complete.json](dub-en-first-check-complete.json)；完整包及下一集未成。

最新續作入口：2026-10-27T14:25:29.6516650Z。第八筆695b／lz514已逐筆恢復覆核，Root fresh573次SHA核對：current/private各212raw、三方cache189及原170全保留、76preserved＋3active＝79精確journal會員、21present／1absent、terms0及來源／lexicon／unused EN binding一致；原PID27636 dead且無競爭程序／lease／STOP／ASRstate。**唯一正常續檢session97854／PID15272執行中**，slot check-en-saved-answer8-resume，lease 2026-10-27T14:25:30.310Z。從起點帶同一已審source-free EN bridge，no force，20分鐘callback與30秒IO上限不變。**先等97854 nativeexit，再核695b實際沿用、完整flags、second runtime/cleanup及journal；不可啟動另一producer／JA或重播97406。** 續檢前checkpoint已push至2651b8a53；本次dispatch另存本機。見[dub-en-eighth-check-recovery.json](dub-en-eighth-check-recovery.json)。0/8外語驗收，完整包及下一集未成。

最新續作入口：2026-10-27T14:14:45.0472582Z。第七筆43f97／lz504已通過逐筆恢復覆核，Root fresh566次SHA核對：current/private各212raw、current/frozen/consumption三方cache170、原137全保留、70preserved＋3active＝73精確journal會員、21present／1absent、terms0及來源／lexicon／unused EN binding一致；原PID43140 dead且無競爭程序／lease／STOP／ASRstate。**唯一正常續檢session97406／PID27636執行中**，slot check-en-saved-answer7-resume，lease 2026-10-27T14:14:48.409Z。從起點帶同一已審source-free EN bridge，no force，20分鐘callback與30秒IO上限不變。**先等97406 nativeexit，再核43f97實際沿用、完整flags、second runtime/cleanup及journal；不可啟動另一producer／JA或重播94112。** 續檢前checkpoint已push至1b58cab781c58f0fa5495d93419619d7ff9bd5cb；本次dispatch紀錄另存本機。見[dub-en-seventh-check-recovery.json](dub-en-seventh-check-recovery.json)。0/8外語驗收，完整包及下一集未成。

最新續作入口：2026-10-27T13:53:02.6945692Z。第六筆保存回覆逐筆恢復覆核及Root fresh557次SHA核對通過：current/private各212raw、current/frozen/consumption三方cache137、原130全保留、64preserved＋3active＝67精確journal會員、terms0與來源/lexicon/unused EN binding均current，原PID53448 dead且無競爭程序/lease/STOP/ASRstate。**唯一正常續檢session94112／PID43140執行中**，slot check-en-saved-answer6-resume，lease 2026-10-27T13:53:03.335Z；同一已審EN source-free bridge從起點帶入，no force／原20分鐘callback及30秒IO上限不變。新runner僅把observer參數改成basename，helper仍只涵蓋synthesis，不拿空檔證明ASR沒有HTTP錯誤。**先等94112 nativeexit，再核0196實際沿用、完整flags、second runtime/cleanup及journal；不可啟動另一producer/JA或重播54516。** 見[dub-en-sixth-check-recovery.json](dub-en-sixth-check-recovery.json)。0/8外語驗收，完整包及下一集未成。

**歷史核對（2026-10-27）：54516已結束；以下running紀錄均為當時履歷。**

54516／PID53448於13:39:12Z native1，第六筆lz422/request0196f77a6faa75b5cdefa6628d1008e57cb3d784da61f84a3d4943d061a915ec完整回覆confirmed rename再次Windows EPERM。第五128762/v2a0521 actual canonical沿用獨立PASS0544dfd9889796442e34e27e3c67f40c6dc83f5bc660fc370ef1f2c7115dc380，原130cache全保留、current137，212raw／source／EN翻譯／lexicon／中文master均未變。第六筆22項證據凍結manifest3e6fb429661b20b02ea5fca9b4331645c22c3d4b8947d9c0b55bae4f0bcf7fa4，64preserved＋3active全保留；approved generic native0/result39c29efff280d51ccf4e0d7d5550710d4f80d9c6ec0609b01a0cdb786263b27d，唯一lz422／terms0／reused1send0fetch0／default ESRCH／alivehold，逐筆獨立review1af9f5cfa1587162a112093f5307120b6e8e85e1e6e717dba3df705e182f6f89 PASS。

目前無producer／lease／second reservation或run。Root準備新正常slot前的fresh核對，同時以只讀及private離線fixture診斷持續Windows拒絕；原因尚未證實，不改OS／30秒上限。已確認舊transport observer只接受basename，舊runner傳absolute path使其未啟用；而該observer本來只涵蓋synthesis `/api/video/speech`，不涵蓋transcribe/judge。因此歷史observer缺席不能當作無ASR HTTP錯誤的證明。新入口僅修正basename參數，不擴張helper路由。見[dub-en-sixth-check-recovery.json](dub-en-sixth-check-recovery.json)。不得重播54516、手動promote/delete/forget或啟動JA。

最新續作入口：2026-10-27T13:38:05.3498942Z。第五筆保存回覆逐筆覆核及Root fresh550次SHA核對通過：current/private各212raw、current/frozen/consumption三方cache130、原126全保留、58preserved＋3active＝61精確journal會員、terms0與來源/lexicon/unused EN binding均current，原PID32176 dead且無競爭程序/lease/STOP/ASRstate。**唯一正常續檢session54516／PID53448執行中**，slot check-en-saved-answer5-resume，lease 2026-10-27T13:38:06.012Z；同一已審EN source-free bridge從起點帶入，no force／原20分鐘callback及30秒IO上限不變。**先等54516 nativeexit，再核128762實際沿用、完整flags、second runtime/cleanup及journal；不可啟動另一producer或JA，不能重播38131。** 見[dub-en-fifth-check-recovery.json](dub-en-fifth-check-recovery.json)。0/8外語驗收，完整包及下一集未成。

**最新實況：2026-10-27 21:36台北。以本段為續作入口，以下舊斷點保留為履歷。**

第四筆覆核後正常續檢38131／PID32176曾執行，fresh543次SHA、cache126、52preserved＋3active全符；已於21:31:25 native1停止，遇第五筆v2a0521/request12876292d88d2d5c83438502db017de44b13c8042c6670e59e9a480d4e904027完整回覆的同類Windows EPERM。上一筆ff4b/lz418 actual canonical沿用獨立PASS9b37968bee7042dc025cfe4f8335c8437769cb4c7556b4d26526daf0263e1efa，原126cache全保留、current130，212raw／source／翻譯／中文master均未變。

第五筆三真檔及22項mutable證據凍結manifest4495a9e42aed91dae9fadee5f78934bda3b577730053f12a69c5e9ac8d8863aa，58preserved＋3active保留；通用checker native0／唯一v2a0521／terms0／private reuse1send0fetch0/default ESRCH/alivehold，resultbf38f401dfb08a8bcf0b5e88e3e92e42e33c95c7c02c8c55a9b199e738dde9c2。逐筆獨立覆核b1a57763e8ed6e593e4c5e04deb9421294660093a5e156e4d151bd8ede1ff129 PASS，Root準備fresh核對後的新slot正常續檢；目前無producer／lease／second reservation或run。見[dub-en-fifth-check-recovery.json](dub-en-fifth-check-recovery.json)。不得重播38131或手動promote/delete/forget；沒有改OS、voice、provider或任何預算／重試上限，完整EN品質與八語包仍未成。

**最新實況：2026-10-27 21:28台北。以本段為續作入口，以下舊斷點保留為履歷。**

29192已21:24:12 native1結束，新的lz418/reqff4bfc70067b6bece4604236d5b506acd31d86104d5385b2dcbac3c27472d436完整回覆在Windows confirmed rename遇EPERM。current cache已126/212；22項mutable證據與212raw凍結manifest7b6bd95a21a20e6ddec4eb67207cafa3ff1571839606ed263ae67fcca19ad824，52歷史保存檔＋3active三真檔全保留。離線checker native0／exact唯一lz418／terms0／private reuse1send0fetch0/default ESRCH/alivehold及原件未改，result5320f2d136b4240b23db75a0792664d5502801beb55ef0b620e923a95ad1c7ae；逐筆獨立覆核d44b7ba1e6421c24cbf5800093314d06d1199d5f3f7c2a21f170f6be6c5a75a9 PASS。

Root準備新正常slot前的fresh核對，上一筆aa360實際沿用由獨立readback核對中。目前無producer／lease／second reservation或run，不能重播29192或手動promote/delete/forget。113次原rename／28218ms額外等待仍受原30秒上限，沒有OS或預算變更。見[dub-en-fourth-check-recovery.json](dub-en-fourth-check-recovery.json)。完整EN品質、八語驗收及交付包仍未完成。

**最新實況：2026-10-27 21:22台北。以本段為續作入口，以下舊斷點保留為履歷。**

第三筆aa360/v2a0431 actual private恢復獨立覆核PASS `f3db35c619c7cf8eeab50f2c6b9772a5ae41cc59e72e3d309d938dc8ebedc1f5`；Root讀回新runner差分，fresh536次current／private SHA核對、current/frozen/consumption三方cache110／原103全保留、current＋frozen各212raw、46preserved＋3active＝49精確journal會員及實際hint SHA/count1全通過。原producer45204 dead、無lease／STOP／另一producer／second reservation或legacy runs，來源及unused EN binding均current。

**目前唯一製作程序：正常check-audio續檢session29192／PID45724**，slot `check-en-saved-answer3-resume`，13:21:53Z dispatch／13:21:54Z lease。runner SHA `5d65d503a1794a0ea2e0b035a08a27c007d45c216c0a25c79c90fc884cf090b5`，首段即帶同一已審EN source-free bridge，no force／原20分鐘callback及30秒IO上限不變。**等29192 nativeexit，再核對aa360實際canonical沿用、完整flags、second runtime/cleanup及current journal；不可競爭啟動check/ASR/TTS/JA，或重播5437等已結束slot。** 見[dub-en-third-check-saved-answer-recovery.json](dub-en-third-check-saved-answer-recovery.json)。0/8外語配音驗收，中文master／212 EN原音／圖片帳本未變，S15等仍依序等待。

**最新實況：2026-10-27 21:18台北。以本段為續作入口，以下舊斷點保留為履歷。**

5437於21:13:42 native1結束；上一筆9bd6/lz411已由canonical正常沿用，獨立收據684f6fb800ca9313489ed71d71812498762a1193957258aa8f2608fbac695576確認原103cache逐項保留、目前110筆、212raw／中文master不變。新v2a0431回覆req `aa360da09a71fda7219f24df44bdfad53e9474cd9585f3e8da081f724014a840`同樣在confirmed rename遇EPERM；三真檔477/1338/798B與其餘來源/cache凍結manifest `ac6da18020b6281e19d8fcd41859fbaf16b9479e790880db0725ad8127cb6869`，這次另完整列46個非active保存檔，沒有刪除任何舊證據。113次原rename／28160ms額外等待後依30秒deadline停止，沒有變更上限／OS。

已審通用checker對此新actual evidence native0，唯一v2a0431、官方16k及1個實際hint重建同request；private reuse1/send0/fetch0/default PID45204 ESRCH/alive負控hold，result37bcf55b65d7b745dcfb0fbc30e80d8ec7dce76b21780cd74556706e8285f8ac。逐筆獨立覆核與新resume入口準備中；目前無producer／lease／second reservation或run。先等actual review與fresh current核對，不能重播5437或手動升格/forget。見[dub-en-third-check-journal-failure.json](dub-en-third-check-journal-failure.json)。英文尚未完整音訊驗收，JA及下一集未開始。

**最新實況：2026-10-27 21:12台北。以本段為續作入口，以下舊斷點保留為履歷。**

新lz411保存回覆已通過逐筆獨立恢復覆核，Root讀回新runner並再次fresh核對：529次SHA檢查（包含current／private副本）、20存在／2不存在的凍結證據、current及private各212raw、實讀103cache、40歷史保存檔＋3active三真檔＝43個精確journal會員；lexicon／source／unused EN binding、PID12192 dead、lease／STOP／other producer／second state／legacy runs均符合前提。40保存檔包括原34與上一筆843正常消費後的6個archive/proof/tmp，沒有修改舊manifest或刪檔。

**唯一製作程序為正常check-audio續檢session5437／PID45204**，slot `check-en-saved-answer2-resume`，13:12:34Z dispatch／13:12:35Z lease；runner SHA `e92d3344b0fbef710c3d9f9e3ba636b581ad85ec5a3fa76799b925931db552b4`。從命令起點帶同一個已審EN v3 bridge/binding、既有20分鐘callback上限及30秒IO上限，no force。**先等5437 nativeexit，再核對9bd6保存回覆的canonical實際消費、原始flags、second runtime/cleanup與current journal。不可競爭啟動check/ASR/TTS/JA或下一集；已結束74735不能重播。** 見[dub-en-second-check-saved-answer-recovery.json](dub-en-second-saved-answer-recovery.json)。中文master、EN原音及圖片帳本不變；0/8外語驗收、完整包未成。

只讀JA前置備忘保存在private `next-ja-production-preflight.md`（SHA13dac6a82d06208500beb640bb28e6e76bdaec49734bcab75202f18d3002bc0e）。Merged JA的212 source綁定當前來源，舊workdir `ja.todo.json`有5個source／4個text仍是listener前歷史，不能再merge覆蓋current版本。JA尚無timeline／fit／m4a，未啟動合成；必須EN完整音訊接受後才按備忘fresh核對。

**最新實況：2026-10-27 21:05台北。以本段為續作入口，以下舊斷點保留為履歷。**

74735已於20:39:11 native1結束，不能重播該slot。上一筆lz202的保存回覆已由正常journal流程實際消費，獨立readback `3d399bc377346f22e88eb386d4288260cea032b0f3cf52c78f90f26aa71a1622`確認原14筆cache全保留、目前103筆；212原音及中文master未變。新lz411回覆又遇相同Windows EPERM；113次同一rename／28169ms額外等待後按既定30秒停止，原因仍未確認，沒有延長預算或改OS。新request `9bd6e7e48246c0c784190123632e4456a14addcfad5fc19d9a3f26f11ede4e0a`的sent／answer／confirmedtmp三真檔完整，22項mutable證據（20存在、2不存在）及212raw核對凍結於manifest `8fe653500402e7f6e279185650556c8a57fb8e32d80661880a8edbf44fad7469`。

已審通用checker對此實際新request離線native0：唯一lz411、官方16k downsample及hints完整重建同request，default PID12192 ESRCH、alive負控hold、private replay reused1/send0/fetch0，原檔未改。逐筆獨立覆核 `f98d96e981b4982b1a519f731a668c883dcebcc35705b628392461abde519001` PASS；Root正在準備新slot的正常無force續檢，必須fresh核對current來源／212raw／103cache／三檔會員／lexicon／lease與未使用的EN bridge binding。此處尚未宣稱新回覆已由canonical消費、第二ASR已執行或音訊通過。見[dub-en-second-check-journal-failure.json](dub-en-second-check-journal-failure.json)。0/8外語配音已驗收、下一集未開始。

**最新實況：2026-10-27 20:30台北。以本段為續作入口，以下舊斷點保留為履歷。**

保存primary ASR回覆的exact官方PRIVATE clone恢復已PASS，reviewb8f3e596b9b90b1456b3495699a7bc5914b3b63ffd25a44921430847acc53f8b。唯一clip lz202的原48k WAV、官方16k downsample、EN hints=[]及完整request SHA843277…6644匹配；三真檔／generation／answer完整、default producer46832 ESRCH／alive負控hold、reused1/send0/fetch0、原檔不變。不是ASR內容正確或audio pass。

Root fresh核232current檔（含212raw與14cache）、source/translation/lexicon及3journal全SHA／active會員都一致、leasefree／三legacy空／固定ASRstate不存在後，正常續檢已啟動 **session74735／PID12192**，slot `check-en-saved-answer1-resume`、lease12:30:23Z，log private同slot-production.txt；不force、從起點帶同一個尚未dispatch的已審EN bridge/binding。**先等74735 nativeexit，再查實際saved answer consumption／官方flags／second runtime及cleanup／journal；不能啟動另一check、ASR、TTS、JA或下一集。** Clone reuse1不冒充canonical實際已完成沿用；後續不同remaining ASR/Jev仍正常已授權paid-capable。見[dub-en-first-check-saved-answer-recovery.json](dub-en-first-check-saved-answer-recovery.json)。

唯讀OS／source診斷65ed0e…1b7a確認三檔當下ReadOnly=false、未見跨rename保留target FD；原因仍是未知的持續Windows EPERM，既有30秒上限不延長、不動OS安全。中文master及EN原音／混音不變，0/8外語配音已驗收、完整包未成。46532已結束不可重播。

**最新實況：2026-10-27 20:26台北。以本段為續作入口，以下舊斷點保留為履歷。**

EN首檢46532已於20:23:20台北native1結束，原因是完整primary transcribe回覆的confirmed journal升格Windows EPERM，**不是完整品質判定**。14筆原ASR cache已寫妥；第15個已付完整answer、sent及confirmedtmp三真檔保存，req843277d2d41d2402fbb8386c85202b8ad5aba854a2a4257a9b3cdba84abb6644／producer46832已dead、leasefree。22個source/voice/cache/QA/log/journal檔已凍結manifestadd9e1b2a2c95079b4e6522e6da592628315d88b0065a56b8498703c0ee5e4ef；212 EN raw全部仍等原frozen SHA，中文master不變。見[dub-en-first-check-journal-failure.json](dub-en-first-check-journal-failure.json)。

已審I/Ov2這次確實exercise：14普通成功、失敗pair113attempt／排定額外wait28160ms，在30秒deadline封頂後sticky hold，未解除持續EPERM。不能延長上限或宣稱已治好OS，鎖來源尚未證實。ko_es正在全新PRIVATE clone用官方transcribe journal核對exact request／三真檔／defaultdeadPID／0send-fetch與alive負控；Root尚未retry。不得delete／forget／manual promote canonical，也不能拿synthesize四檔規則偽造WAV response。

當前canonical producer0，固定ASR projectstate不存在、v1/v2/v3 direct runs均空；依已審「SSH前先durable reservation」實作，此次尚未進到cachedWhisper第二辨識。當前actual EN cohort／binding仍是未dispatch的同一份；待exact recovery PASS及fresh14cache／全部raw/source/journal核對後，才用**全新slot**正常續原首檢並沿用binding，不能重播46532舊槽位。EN音訊未接受、0/8配音驗收，無JA／下一集／YouTube。

**最新實況：2026-10-27 20:21台北。以本段為續作入口，以下舊斷點保留為履歷。**

當前唯一本集producer為官方EN首檢 **session46532／PID46832**，slot `check-en-first-reviewed-v3`、lease取得12:21:33Z；實際log `C:/Users/x8120/mokaair-work/curio-s31-v2-preflight/check-en-first-reviewed-v3-production.txt`。從第一次check就帶已審source-free bridge v3／正確EN binding，沒有bare paid check、沒有force。**先等此指令native exit，再核官方flags／實際second runtime及cleanup／journal，不能啟動另一個check、ASR、TTS、JA或下一集。** 見[dub-en-first-check-dispatch.json](dub-en-first-check-dispatch.json)。

collector v2的23原測試＋5獨立控制PASS，review75c3ffa…a96僅限prepare；Root實際prepare native0於20:17台北完成。完整212 raw WAV／68,852,848B／717.12秒皆凍結，catalog577ff8…ffb18、provenance3a59c6…e73d；原始PCM1 mono48k16bit，12個stretched樣本另綁。ko_es正式actual cohort＋binding-core覆核4db14a…9bc0已逐檔驗current/frozen SHA/bytes/headers/noalias，13artifact/原native0/source/voice/cache/v4／實際樣本重播150窗0over及212placement全match。Root據此組fullbinding989984…b183／corec1cff4…118d。這只批准callback由實際args機械選exact-SHA子集、單SSH及fresh資源／cached-model gate；不預稱Whisper真跑、發音通過或有人聽過。英文check/flags在首檢前確定不存在，中文原check及兩flags已另外凍結。中文master不變，EN還未音訊接受，八語驗收0/8。

**最新實況：2026-10-27 20:04台北。以本段為續作入口，以下舊斷點保留為履歷。**

英文正式正常續作session92912已於19:50:15台北native0，212個原始WAV齊全；150窗fit0over，8窗tempo至1.15，cheng-date的3frame／0.1秒由下一停頓合法吸收。branded en.m4a為46,583,012B／969.705秒／48k stereo，SHA99141e431c94d33b29d9143af4259f1f083e730f968389cdd68156408ac2adc9；source仍6e0dd44…b86、speechfa2912daff4bd218。最後resume CLI30requests／1799billablechars、141reused、2個原paid journal answer沿用而非重買；品質重錄／縮句／reword仍0。見[dub-en-synthesis-complete.json](dub-en-synthesis-complete.json)。

限本集的I/O preload v2已經獨立PASS（review1fe346…fe1）後啟用；實際38次均為原rename第一次成功、額外retry／wait均0，transport observer空。不能說shim已證明治好Windows鎖，也沒有更動共享工具／OS安全／voice／全域預算。環境opt-in已清，當前producer0／leasefree／active journal0；34個不可變的舊recovery proof／answer／tmp仍完整保留，不刪除也不forget。

Root已建立actual completion observation90987ce91c78ca61821ded5cb7992e68a9453c734c1d13aa0956ac3557fc43b8，綁原native0收據、完整212WAV／current source／translation／timeline／fit／cache／branding／中文final及既有核准。這只是實況清冊，不是音訊驗收。private bridge v3 genericcode獨立PASS（review5dd8f5…a64b），但尚未actual cohort／binding核准或真SSH／ASR。collector v1獨立覆核拒絕（review57ce1e…c51）：postcopy會員未重查與fit一致性負控；正在另存v2修正，沒有在actual資料執行失敗版。完成修正覆核、凍結真212cohort及actual binding覆核後，才從第一次官方EN check掛已審source-free第二辨識；不可先bare paid check探句，也不可開始JA／下一集。中文master及核准維持，八語配音驗收仍0/8，完整包未成。

**最新實況：2026-10-27 19:09台北。以下較早紀錄保留為履歷，以本段為續作入口。**

77232已native1，第四次不同request的confirmed journal升格Windows EPERM。現在172個EN WAV及cache/source/gates/log／全部active journal2筆6真檔已完整凍結，manifest9b693e5a5807e82a9fbea18f139ad6b6839f928df68d785301c8cf95a6d2b891，PID43060已ESRCH、leasefree。新staged req2f2ad389067e5a6d7b65cc687ebba4f1b66ce00bfef083d24487e157cb20f062與confirmed companion0f0b8482c5e4a92624ac1d644657929dd809f25e465c43a3c878d5d5b195215f均保留。Generic已審checker對新staged實際PASS（receipt be6b21a09d75668e55ca65eb1723487753033c219c7409d7fc3e7b7fbea87f99）；root另用六真檔、官方wrap在PRIVATE clone實際joint reuse2/send0/fetch0、原檔不變（receipt8829ab51bf4cdd1446e39146a9ec4f15cceb6989e446af91908d91f298535efb）。見[dub-en-fourth-journal-failure.json](dub-en-fourth-journal-failure.json)。尚未normal resume這兩筆，不宣稱實際新clip已交付。

**當前無canonical producer。先完成／獨立審閱本集限定的confirmed-journal rename retry preload，再fresh172clips/cache/source＋兩個保存answer後才新slot正常續作。** ko_es在private confirmed-journal-retry-prep/準備可逆per-process I/O處理：只對本集、ownPID、sent→confirmed且完整bytes/SHA/generation不變的同一原rename操作多等，總額外wait30秒封頂；無copy/delete/alternate syscall、無HTTP重送、無voice/全域預算/OS安全設定或repo共享工具變更。需自測與pt_id獨立code review後才啟用；如不安全仍丟原錯誤、保存journals，不偽成功。

ASR bridgev1及v2均已正式拒絕啟用；v2的alias及kill/reap已修，但獨立負控再發現catch前程序死亡時，新binding能略過未結DISPATCH_INTENT。v2 review SHA d7dc851c85ddf7e74d3608c2f5932a7a0c62a7b99d63ec53d39a24a56d60d276。audio_plan已暫停尚未建立的cohort collector，現在另存v3，加入SSH前exclusive+fsync project-wide reservation及完整COMPLETE proof才可結案；v1/v2原code/收據保留。仍無實際EN完整cohort/binding／真SSH／ASR。完整EN native0/fitpass後才可凍結actual212 WAV、審v2／binding、掛官方首檢；其餘七語及完整交付包未成，Chinese master/QA/final gate不變。

87402已native1，第三次不同request的confirmed升格Windows EPERM；已產161EN WAV/cache/source/gates/log凍結，manifest2dd16f17b392d75d6cb24aff093dfc9c48a31e54a66d1480ca7d935b3a5b4723。新staged req0f3df992e0b4acdc31657e3d6fe044bae5b96bd77483106b3eb3f6a6184211a5/PID8488已ESRCH，用獨立code-review通過的frozen PRIVATE generic checker已做實際clone PASS（receipt9898ec61df1031193b56748941034ef096ecac465fd1387147d4776238a3f68f），reused1/send0/fetch0、原paid billable36保留。

本次active journal **2筆**：另有同一multi-line unit前句11afb86830e29b59d2e07cfad7d15b636526f2777c72da0e7fef8ffc4604c717已confirmed但尚未消費，JSON1227B與WAV203564B另凍結companion manifest e371b343dc8cdafd3f1a84bb0eee97b3698cd054daaef61d6ba31d5e16610ed2。這筆本來就confirmed，沒有偽造answer sidecar／tmp套四檔規則；ko_es在PRIVATE clone驗正常直接reuse/0send/0fetch。見[dub-en-third-journal-failure.json](dub-en-third-journal-failure.json)。**當前無producer；等兩筆實際合約皆PASS，再fresh161clips/cache/source＋兩個journal row才正常resume新slot。** 87402不能重播，不可delete/forget/手動rename。中文final不變，EN未fit/audioQA完成；bridgev2仍未啟用。

第二筆synthesize journal的PRIVATE clone恢復也已PASS（SHA69e53adebb7df1c701721e0476c40aae7ce53b163e382db26296e85f3fdaa616），exact request／4files／defaultdeadPID＋alive負控、reused1/send0/fetch0通過。Root fresh核160個凍結檔（含146個WAV）全0drift後，正常resume全新**唯一session87402／slot dub-en-saved-answer2-resume**。dry-run剩52requests／3216字元估計，當時既有月額5452289、仍0estimatedfit-over；不改voice／source／translation／全域預算。

官方canonical proof已讀回該saved raw WAV ca8834…e703，經正常trim／encode後與實際新lz426.wav逐bytes相同，clip SHA24b42cef6f0578153f3757e2880b5cfa979e629a3b7319bd52f6b8a96583a18f；原146WAV再次讀回全未變。見[dub-en-second-saved-answer-recovery.json](dub-en-second-saved-answer-recovery.json)。兩筆已付answer均非重買；其餘不同剩餘工作仍正常已授權paid-capable。**先等87402 nativeexit，再查實際fit／全212WAV／timelines／journal；現在不得啟動check、ASR或下一語。** EN仍是首次合成、品質重錄／縮句／reword均0。

12945已於18:39:02台北native1結束，第二筆不同的完整synthesize answer升格confirmed時再次Windows EPERM；前一筆確已從保存回覆重用，不能誤認為重送原request。現在已產146個EN WAV，全部與cache/source/gates/log另凍結dub-en-second-journal-failure-before，manifest SHA9fde58bfb1347fc77cd2d943a059a751ad0ab5806c4a265f7c47d35c7fcc14d9。新req1cde9891b24dd325283187fb439e5e4c344d504199e931df4d8a2b63d9d734f1、producer51568已ESRCH、leasefree、activejournal1；sent969B/answer1915B/confirmedtmp1230B/WAV387884B四檔齊全，見[dub-en-second-journal-failure.json](dub-en-second-journal-failure.json)。ko_es正在全新PRIVATE clone驗同一官方恢復合約及0send/0fetch；root未retry，禁止delete/forget/manualrename。

**此為第二筆覆核前快照，已由上段PASS與87402 resume取代。** 12945已結束不可重播；英文fit/audioQA仍未完成。已核准中文master不變。bridgev1已拒、v2仍在私人準備及後續獨立覆核；此時不能啟動ASR/check/下一語。

EN saved synthesize answer的獨立PRIVATE clone恢復PASS，receipt SHA3454b05c4cfe19fdad1ab64bb14173a89050b7b4cb5ee2420d44cda60a0da0b4：exact body／994B sent／1951B sidecar／1255B confirmed／203564B WAV／generation皆匹配，default PID47048 ESRCH、alive負控hold，reused1／send0／fetch0；returned billable0是本次沿用合約，原paid billable30留存。root再次核65個凍結檔全部0drift／leasefree，新的正常resume已啟動**當時session12945／slot dub-en-saved-answer-resume（現已native1結束）**。當前log同slot-production.txt；先等nativeexit，不啟動另一producer。resume dry-run128待產request／8068字元估計、當時既有月額5482537，估計仍0fit-over；其中這一筆從原回覆讀回，其餘不同未完成request仍正常已授權paid-capable。

實際canonical recovery proof SHA488c2fe0a793dc01e6b14494754a4ded636739a68d7022c2f794aa2e4a2a5bf2已建立；原回覆WAV經工具正常trimSilence／encodeWav後，與新v2a0221.wav full SHA3d2887fbcdace0ec1a6ce0ff6946a41be71fbfbb80c9e7664bbc8298daeb4dc6逐bytes一致。這解釋raw WAV SHA與trimmed clip SHA不同，沒有拼接或修改ASR。原49個片段又讀回全未變，原confirmed tmp及recovery archive仍保留；沒有重買該exact request。見[dub-en-saved-answer-recovery.json](dub-en-saved-answer-recovery.json)。整條EN仍未完成／fit及audioQA未通過，不能先勾配音完成。

private bridge v1的正式獨立審查為**REQUIRES_FIXES，不可啟用**（receipt SHA49c57a59968557ce5288e117c8e42256a3e395fc6beacf0d54297bfb5749a281）：祖先junction alias及kill=false/no-close無有限reap都已mock重現。所有v1檔案／SHA保留；audio_plan在另存dub-en-bridge-prep-v2修補並補負控，之後還要pt_id獨立重審。沒有任何真SSH／ASR或check已因此啟動。完成EN fit後仍須凍結實際完整212WAV cohort與binding才可審啟用，不可拿fixture／v1 generic測試替代。

英文首次dub90907於18:23:18台北native1停下：Windows EPERM再次發生在完整synthesize answer已保存、confirmed journal升格rename時。request `0faeb13391cd2028b43a1c057808809afa05ec7e93af04c1c0de98f8c5d0444a`；producer47048已OS ESRCH、leasefree，當前active journal1，不能直接重送／delete／forget／手動rename。49個已產EN WAV及cache、source／翻譯／審稿／timeline／approvals／QA／command log已凍結在private dub-en-first-rename-failure-before，manifest SHA20fe65799325f7a7fb3d985fb1e1fc04c92df92e36f575754cd3027b11cb6fc2；sent994B／answer1951B／confirmed tmp1255B／回覆WAV203564B四檔SHA齊全保留，見[dub-en-first-rename-failure.json](dub-en-first-rename-failure.json)。root尚未重試該request。ko_es正在全新PRIVATE clone以官方synthesize journal做exact-request／default dead-PID／WAV response驗證，mock send及fetch必須0，通過後root再fresh核canonical四SHA才能normal resume新slot。共享Windows寫檔票已存在，本集不修改共用工具。中文final/source SHA仍完全不變，11/11與final gate有效。

18:29時無canonical producer（已由上段resume12945取代）；不要重播已完成dub-en-first槽位，不啟動ASR／check／下一語／下一集。英文品質重錄／縮句／reword仍0，49個片段不等於完整音軌或fit通過。新Chinese實際timeline的官方hook45秒與24loops檢查也已PASS，見[actual-timeline-narrative-listener-rw1.json](actual-timeline-narrative-listener-rw1.json)。private EN bridge v1已凍結且僅mock測試（27PASS／1權限skip／0external），pt_id正式審genericcode，尚無實際EN完整cohort／binding、不可啟用；與此次journal恢復是分開的關卡。

中文版新master已完成：assemble33528 native0，150景只重編16segments、406秒；29090frames／30＝969.666667秒（16:09.667），container969.705秒，301800813B，SHA b8bc3fcfe22e73cff79422124d89da99630bbf7c7e59b0480ef9804db11d2c60。當前body28310frames、intro150在frame1574／52.466667秒、v4outro630；-14LUFS／peak-1.9／bed-33.1，checks.ok=true／63frame samples。官方QA68642 native0 **11/11**，六章與九語metadata／caption綁定current；ja2、es5、pt1、vi2個閱讀速度警告保留，留待各語實際dub timing處理，不先刪事實。

新檔原生MP4播放已實際抽查開場進度、片頭door／Mokaair logo、546秒吳曾新字幕、868秒荔枝新字幕及v4片尾slot，最後currentTime=duration=969.705、ended=true／error=null。只作抽查，沒有全片連續觀看／人工聽音／站主觀看宣稱；v4視覺slot存在，YouTube可點end-screen尚未安裝。暫存tab與經PID／命令身分核對的loopback server已關閉，無動到別人程序。見[chinese-final-listener-rw1.json](chinese-final-listener-rw1.json)。final gate已於18:17:38台北native0依委託綁上述SHA，見[final-acceptance-listener-rw1.json](final-acceptance-listener-rw1.json)；原版final SHA648962…343af再次核對不變。這仍不是完整交付包。

**18:21時的production command為英文首次dub session90907（現已native1停下）**，slot dub-en-first，log private dub-en-first-production.txt，正式--locale en --line-by-line／無force／沿用既有speech quota。已完成dry-run171requests／10565字元，當時月額度5508182，估計9windows需加速、0預估fit over；實際fit及音訊QA尚未得知。source／final／en212格與文字審閱SHA在dispatch前核對current，原translation／review／timeline／approvals／languages／QA已備份dub-en-first-before。英文初次產音不算品質重錄，shorten／quality-retake／reword計數均0。先等該指令nativeexit；不能啟動ASR、check、另一語或另一集，也不能動active producer的journal。

英文首檢的private batch-second-opinion bridge由s31_audio_plan準備，尚未啟用、未SSH／API；須待實際EN fit完成後凍結全EN WAV cohort及binding，獨立審generic code＋cohort，才可掛官方check-audio --locale en。不可套用中文32句reader，不能先跑沒有second的付費check來探疑句；callback只可選已審EN cohort的完整WAV子集，忽略hints／原稿，單次cached Whisper／4CPU／nice19／離線／資源gate／總20分鐘含傳檔與cleanup，未知結果不得盲重送。

18:00時的唯一producer為assemble session33528（現已完成）／slot assemble-listener1-current（正式--intro-after-condensation），log在private同slot.txt。render56428已native0：5states新繪、228沿用、212字幕／cues；5張新字幕實圖已逐一查看，字形及版面正常，source／speech／subtitles binding均current。clips native0沿用129stills、0newclips；music native0核對既有976秒bed原SHA，無購買。見[media-refresh-listener-rw1.json](media-refresh-listener-rw1.json)。先等assembly完成與實際checks／frame count／新final SHA讀回，才captions／QA／native player及final決定；不要以預估片長或舊final充當新成片。

兩例獨立發音覆核已完成，見[audio-qa-phonetic-independent-review.json](audio-qa-phonetic-independent-review.json)（SHA131ecc59a6e7ba13eb373f31b340274dcac50deefe9cd8eebc51ee3424b8d27a）：0491的實際Whisper「無憎」對應作者Wu Zeng；0722的實際primary「麗芝」可讀lì zhī，與荔枝同音。比較器確實選了不合此語境的céng／lí。另一份ASR仍各有不同音，不能說兩份一致或聲調已逐聲聽驗。依站主直接委託，root作有界品質接受，完整記錄兩案反例及聲學不確定性，沒有改source／WAV／cache／flags／字典／Jev分數，也沒有人被宣稱聽過；不為文字誤判重買，listener2未執行。見[audio-qa-delegated-decision.json](audio-qa-delegated-decision.json)、[audio-acceptance-listener-rw1.json](audio-acceptance-listener-rw1.json)。官方local audio gate已於17:52:42台北native0記錄，綁timeline SHA461844fdcf9a29ecf581397c9c546637ce85262bc7ef2b8854e683fdf64d8f31；官方checker仍是native1／2flags，不能改寫成自動全過。

17:55時的producer是新render session56428（現已完成）（slot render-listener1-msedge），先等native exit與新frames讀回。首次default Chromium缺binary的render native5已對帳：十份舊manifest未變、leasefree、journal0；改用已安裝Edge及正式VIDEO_BROWSER_CHANNEL=msedge，無安裝或新增付費。後續本機render也須設此channel。舊final完整保存在private retake-context13-before/final.mp4。shared比較器問題已另立未認領P2票2026-10-27-avoid-polyphonic-character-false-flags-in；本集不修改共享工具。

當前source lint0錯誤／0警告；bundled Node24.19.0完整docs-video236/236通過、task validation2193通過（既有警告保留），見[validation-listener-rw1.json](validation-listener-rw1.json)。

17:46覆核前快照（已由上段委託決策取代）：官方check8572已於17:31:30台北結束native1：212＝155逐字＋30同音／口語＋4Jev＋21第二轉寫＋2flags（v2a0491、v2a0722），只新增5ASR／2Jev；見[audio-qa-listener-rw1-official.json](audio-qa-listener-rw1-official.json)。當前check／flags、兩個原始WAV及timeline／approvals已凍結，source／audio仍fa2912daff4bd218、audioEvidence0、active journal0、leasefree、producer0。沒有進行第2輪listener或再次付費。離線比較器發音診斷發現吳曾被預設為ceng2、麗芝的麗被預設為li2；實際轉寫與意圖可能只是專名／多音字假陰性，正作獨立來源與發音覆核。不能改flags／低分、拼接轉寫或為了green寫錯字幕；也不能先聲稱實際音訊通過。當前lint已0錯誤／0警告。

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

**當前可行動斷點是本集限定I/O重試處理的獨立覆核；當前入口見最上段**。先讀實際nativeexit／fit／current WAV／cache／timeline／journal，保留任何新uncertain outcome並對帳，不能重播舊slot。完整EN native0／fit妥當後，凍結全cohort，再獨立審實際binding＋已修的bridgev2（v1不可啟用），作EN第二ASR／official check／mix驗證，再依序ja→ko→es→pt→id→vi→th。若fit over，最多2輪受保護縮句；不得無上限重錄或以missing/skipped冒稱八語完成。private post-audio-current-entry-companion.json明示當前有界委託音訊決策，取代舊frozen recipe的「必須0flags」協調預設；舊recipe及原低分原封保留。尚未完成完整交付包，不能勾整集完成或開始S15。

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
