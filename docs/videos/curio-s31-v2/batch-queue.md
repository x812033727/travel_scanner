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
| 1 | curio-s31 | curio-s31-v2 | 中文轉寫212句已跑完、31句做離線第二意見；插圖生成中，八語稿已完成並交叉覆核 |
| 2 | curio-s15 | 先查既有新版與持有者，再決定隔離路徑 | 等 S31 完成 |
| 3 | curio-s12 | 同上 | 等 S15 完成 |
| 4 | curio-s16 | 同上 | 等 S12 完成 |
| 5 | curio-s19 | 同上 | 等 S16 完成 |
| 6 | curio-s20 | 同上 | 等 S19 完成 |
| 7 | curio-s21 | 同上 | 等 S20 完成 |

## 續作原則

- 每集先查現有分支、任務、PR、完整媒體及實際核准，再認領窄範圍新票；原版 PR #1800 與原版工作目錄保留。
- 依當前 `curio-episode`、`youtube-video` 的新規則改稿／查核／新讀者盲評，目標約13分鐘；實際正文與成片都量測。長度不足時補有來源的實質內容，不用空白、重複或慢播補時。
- 依站主推薦選擇授權，例行聲音、分鏡與成片決定可由代理依有證據的品質檢查處理，記錄為「站主委託依檢查採推薦選擇」，不得寫成站主本人已聽／已看。
- S31 的圖片及圖片評審費明確核准上限 US$6。後續採同級保守建議：每集以 US$6 為圖片／圖片評審上限，不改正式站全域預算；若報價或剩餘帳本不容納，先停該集付費部分並回報實際差額。旁白／配音用現有網站字元額度，不提高預算或開新供應商。
- 原圖、配樂及有效快取先驗雜湊再沿用；不把舊核准當新版核准。超時或 uncertain 付費請求先對帳，不能忘記記錄後盲重送。
- 中文版先定案，再按原集已選語言完成標題說明、CC、配音及逐語檢查。原版外語僅保留，不冒充新版。上架包、站主本人驗收、上傳與公開狀態分別記錄。
- 同一集一次只跑一個持有製作鎖的指令；不動其他集或其他聊天持有的鎖、STOP、正式站設定或工作。
- 完成一集即更新本表與該集任務，再接下一集。進度不變時保持安靜，只通知成品完成、真正失敗、預算超限或需要站主處理的事項。

## 當前斷點

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
