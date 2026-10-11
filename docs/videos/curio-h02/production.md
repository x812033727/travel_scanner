# H02 製作紀錄

工作日期：2026-10-12（Asia/Taipei）。媒體僅存於 repository 外的 `<VIDEO_WORKDIR>/curio-h02/`；本檔不含帳號或金鑰。

## 大綱決定

- 站主在本聊天明確回答：「採用 A，繼續製作」。A 沿懷特返島、讀懂留言、追索去向和考古線索推進。
- 凍結 `brief.md` SHA-256：`7475f2d93110b9cde572aac2531ccd77ec98a0e23f7c922987eff69b9d221404`。保留送審時的原文，因此 brief 首行「尚未核准」是當時狀態；本收據記錄後來的核准，不修改已核准來源。
- 本機官方 `approve --gate outline` 已記錄聊天決定，收據時間 `2026-10-11T17:03:12.133Z`。
- 原後台審核 `bf2328c0-0b5e-4edb-ac0e-ac951b0278c1` 送審時待決定。Jev 推薦 A，但 explainer 被要求 demo ≥ 0.6，該項實為 0.18；這是既有追蹤票 `2026-10-10-outline-pick-demo-exempts-explainers` 的範圍。後來依站主已選A的明確決定，從已登入的Chrome只操作本張大綱卡；`2026-10-11T19:27:49.870Z` 伺服器GET讀回approved、choice A及相同完整brief SHA。後台核准及畫面證據分別在 `_audit/backend-readback.json` 與 `_audit/outline-A-approved-20261012.jpg`，未操作其他關卡或設定。

## 當前製作

- 來源刷新與四張公有領域圖片下載完成，現行成片採用其中三張，詳 `research-refresh.md`。圖片已以 SHA-256 檔名放入工作區 `stock/`，複製後再次讀回雜湊一致。
- 本機路線：插圖投影片、MiniMax image-01、Gemini Sulafat、1080p、繁中 CC 不燒字幕。正文及成片各至少八分鐘，目標十至十一分鐘，實際時間以媒體量測為準。
- 現行稿109景、134句、68個插圖鏡頭，另有三張公有領域史料圖。來源 SHA-256 為 `4dfe4d73dd458323949542ba5c22cd68a7838cbdc237b36543b07ea18620322e`；完整旁白134句檢查全過，最新音訊時間軸已由後台核准並讀回。1080p成片11:20.5及134條繁中CC已完成；全片解碼exit 0、19張成片抽樣未見阻塞問題，但正文平均幀率嚴格檢查有差異且null muxer報時間戳警告，原結果保留。站主已明確核准目前分鏡與成片（含四張保留圖），正式站及本機批准均綁原媒體雜湊；繁中上傳包4／4檢查通過、publish已核准。詳 `delivery.md`。
- 本集正式選擇只出繁中，後台及本機語言決定已同步。原完整QA 9／11保持不變；語言決定後的官方字幕單項檢查通過。`ready_to_upload=true`，未上傳YouTube、未公開；這些狀態均有實際讀回。

## 工具收據

本機階段的 stdout/stderr、程序 PID、runtime 與 exit code 均保存在工作區 `_audit/`。使用 bundled Node `v24.19.0`；獨立 Whisper 使用本機既有 Python、`small` 模型，逐一執行，不開兩批互搶 CPU。

正式站 speech/media 預檢已讀回：Sulafat 可用，slides_enabled 為 true，MiniMax image-01 已配置，每片上限 US$80。這只是配置檢查，並非已扣款、生成完成或品管通過；每個付費階段之前仍先 dry-run，任何未知結果保留請求紀錄而不盲目重送。

## 製作前檢查

- 完整 lint：0 errors、3 warnings（構圖／光線提示重複字詞）；2341口語單位，估11.3分鐘。媒體實測尚未發生，警告所涉及的畫面多樣性仍待聯絡表確認。
- `test:docs-videos` 同等指令：199 passed、0 failed，exit 0，約164秒；日誌在 `_audit/docs-video-tests.log`。
- 語音 dry-run：120個新請求、2797字，Gemini Sulafat；當次剩餘9,369,384字。
- 插圖 dry-run：91個鏡頭均在模型提示長度內，MiniMax image-01、1K；一輪估US$1.23，最多三輪估US$3.69。這是預估，實際付費以ledger為準。

## 稿件凍結

第二輪 `verify-2.md` 及聽眾審稿綁定 `video.json` SHA-256 `7b8d066cbb42ad7ee621171fcaedcda7c5eeafb9acf9bf8dc6c7d287b08c482d`，`claims.md` SHA-256 `6db38c75194a57b3361ee9eaab058b46da1f76fa0bab47ac48ea70de187be3a3`。首輪超過三項事實修正已由不同代理覆核；第二輪唯一新增的 tree prompt 修正已讀回，不再有必修項。此結論僅限稿件，不表示合成旁白或成片已驗收。

## 旁白合成與時間讀回

首次 TTS 完成，exit 0：120個新請求、2797字、134句音檔。當時 `timeline.json` 為20071幀／30fps，完整音訊669.033秒（11:09）；逐句原音合計549.695秒（9:10），不靠延長停頓達到八分鐘。128個畫面狀態，最長8秒、平均5.2秒，插圖時間占比約73.9%，實測 cadence 無問題。後續局部重錄的最終雜湊及時間見下方最終音訊讀回。

首次 `_audit/audio-metrics.json` 獨立讀回所有134句 WAV完整SHA、旁白完整SHA與當時speech hash，全部一致；speech hash `b60a99487d6f6a4a`，旁白SHA-256 `175f8800850dd7b8d41ee7980c273e7cd893f323ad732e933d1f075291b57c5e`。這是首版紀錄；該檔後來更新為下方最終音訊讀回。這證明來源／檔案／時間一致，首版發音當時仍待 `check-audio`。

三張代表插圖的啟動被同一影片的 `check-audio` 製作鎖擋住，exit 3，官方輸出明示 nothing was sent or written；沒有產生圖片請求或付費媒體。保留該收據，待讀音檢查釋出鎖後接續，不刪除鎖或同時開兩批讀音檢查。

逐句轉寫第一批因 Windows `EPERM` 在收據 atomic rename 時中斷，exit 1。原 `sent` 和完整 `confirmed` 暫存檔均保留；獨立覆核確認答覆完整，另以原音檔重建工具實際上送的 16 kHz WAV，135724 bytes／SHA-256 `b83082247c3de626031e718194484eced9a243a1fe8697c75170ac0ec8d0ee5d`，請求 SHA `baf09ddacc99728a607364f0f4d2fc2e17c38bdd3bf311c2928c32689d21ad7f` 完全相符。原程序已退出後，備份兩份檔案，再原樣恢復 confirmed 收據；離線官方 journal 重用實驗為 reused=1、new POST=0。恢復收據保存於 `_audit/recovery-baf09ddacc99/recovery-receipt.json`，未使用 `forget` 或重購已收到的答覆。官方 `check-audio` 已續跑，原有轉寫快取保留；此恢復不代表讀音品質通過。

恢復後該句轉寫已在 `review/check.json` 讀回，原 journal 由工具正常 release。Windows 寫入問題已有 [待辦票](../../../tasks/open/2026-10-09-windows-speech-journal-rename-failures.md)，本集僅恢復已知答覆並留下證據，不修改共用產線。

全134句第一轉錄完成：94句逐字相符、15句僅同音／語助、7句Jev通過、18句疑點；該階段 exit 1，不能視為旁白核准。第二轉錄程式因 Windows stdout 預設 cp1252 無法輸出中文而失敗，單句唯讀診斷確認 `UnicodeEncodeError`。僅在外部 launcher 加 `PYTHONUTF8=1`／`PYTHONIOENCODING=utf-8`，沿用原134句轉錄與Jev快取再跑獨立 Whisper；未重購第一轉錄或預先改稿。

獨立 Whisper 排除7句疑點，仍有11句需處理。第一輪僅這11句重錄，dry-run及實際皆為222字，TTS exit 0；其餘109個請求沿用，稿件未修改。原11句音檔、timeline、兩份check report已保留在 `_audit/audio-before-retake-1/` 及 `_audit/check*-before-retake-1.json`。重錄後逐句檢查進行中。

第一輪重錄再查為134/134覆蓋、5句剩餘疑點；第二輪只重錄這5句，101字，TTS exit 0，其餘115個請求沿用。第二輪重錄前快取／flags／5句WAV／timeline亦留於 `_audit/`，重錄後覆核仍有5句疑點，處理見下方。未由聊天大綱核准推定旁白核准。

## 旁白關卡通過與試圖修正

兩輪後仍5句疑點，交由聽眾模型只改措辭，再由不同代理覆核原意、人名與中文數字；官方 `rewriteProblems` 全過。五句改寫及兩張試圖 prompt 的視覺修正恰為全部差異，詳 `audio-rewrite-review.md`。初始verify-2的完整查核加上本次差異覆核，綁定當前 `video.json` SHA-256 `aa6a6155da421683bdb9a2bf16532d1460e78d15a17cd5505d14748efa9c917e`；claims未改。

改寫後僅5句合成，114字，exit 0；最終 `check-audio` 134/134句、102逐字相符、18同音／語助、7Jev通過、7獨立轉錄排除、0 flagged，exit 0。`review-push --gate audio` 後台自動approved，`review-pull` 已記錄實際核准。

最終音訊實測672.5秒（11:12.5），逐句原音合計553.175秒（9:13.175）；全部134 WAV SHA讀回一致。speech hash `20d0bfc523979b9f`；timeline SHA-256 `aea370f8541b9ef5e9c4027c31c1659b9851804508c10e91d0e341ed5f4c00c0`；旁白 SHA-256 `d94e49a3f8bc79c2676c2a7082d865c0a8c7e9c1ae66e8d94c03fc96961c9b20`。`_audit/audio-metrics.json` 為當前最終音訊讀回。

首批3張試圖共4個take，ledger實際US$0.05。雖然judge全部有passed候選，實際看圖仍發現開場石造城牆替代木柵、鹿未吃瓜藤，因此只改這兩張prompt並重新生成；樹幹圖沿用。舊圖與原manifest保留，不以自動評分取代實看。

鹿圖第二版三次仍有畫風問題；第三版以較近構圖與明確配色修正，最後一張通過9.29分，實看能辨識嘴中葉子、地上瓜藤與完整屋頂。三張試圖的目前完整雜湊與實看範圍見 `visual-review.md`。試圖累計11張原圖、US$0.15；此成本不包括後續全套生成。

第三版僅改鹿圖prompt；旁白、claims與timeline不變。`_audit/pilot-prompt-2-receipt.json` 及獨立差異覆核將來源鏈綁定目前 `video.json` SHA-256 `64c95e39f9021c4dbe2793b758df4ee5c72a4668b787a833de5d52346d032910`。首版試圖的四張原圖及兩張裁邊圖已從已知付費job做唯讀GET與確定性裁邊恢復，完整SHA一致，0新POST；收據 `_audit/pilot-v1-recovery.json`。

目前來源的199項影片文件測試再次全過，exit 0，日誌 `_audit/docs-video-tests-final-source.log`。全91張插圖於 `2026-10-11T19:05:32.168Z` 啟動一次，沿用三張試圖；逐張保留評圖與選用紀錄。全套尚未完成，分鏡及成片關卡仍待後續送審與讀回。

## 年代服裝修正與安全續跑

首批實看發現木屋門口多餘怪鳥、承接懷特的現代登山客、現代水手制服與修屋工人的服裝／牆材歧義。建立本聊天自有 STOP，讓工具完成手中單位後安全退出；官方收據為16張新生成、11張選用圖、exit 0，但全91張並未完成。製作鎖已釋放，暫停時圖片及評圖ledger累計US$0.3545。

`_audit/visual-correction-1/` 已保留43個檔案及完整SHA清單，包含當時source、全部keyframes、media jobs/cache/ledger、timeline、approvals與STOP。原圖及已知付費job均保留，不刪除失敗候選或盲目重送未知請求。

完整prompt檢查後，只改31個提示詞的年代／服裝／人物或道具範圍；現代研究、後段其他世紀及象徵場景分別維持原時代。魚與草蓆改為無人靜物，避免模型把手部互動錯畫成斷頭；樹幹改為原生quote卡，精確顯示「CRO」與懷特1590史料來源，不再使用額外年輕人物。109景、134句及所有claims不變，插圖數91→90。`_audit/visual-correction-1-receipt.json` 完整重播與獨立覆核通過，當前source SHA-256 `c9269e0e278a150b3de585a5e57ebf66e69fcb72cf74165429623a7614b9a663`，詳 `audio-rewrite-review.md`。

獨立 `_audit/visual-correction-1-timing-proof.json` 使用實際 `start_frame`／`end_frame`／`audio_samples`，驗證全134行、109景、128states及20175 frames不變，唯一timeline差異為樹幹的template。原apply helper曾用不存在的start/end欄位；該比較不是時碼證據，已修正程式並以此獨立實測覆核為依據。

確認自有STOP內容及來源覆核後，只移除本聊天建立的那一個檔案；讀回已不存在，收據 `_audit/stop-released-visual-correction-1.json`，未移除其他停機檔。官方 `tts --refresh-evidence` 完成0新合成／0計費字、120請求沿用；全134 WAV與旁白完整SHA仍相同。新timeline SHA-256 `5ad5408f37ca1811492b00a2aa3b352a35dfe761cb762af27255a8b2cf4d9504`，旁白SHA仍 `d94e49a3f8bc79c2676c2a7082d865c0a8c7e9c1ae66e8d94c03fc96961c9b20`。

新的audio送審已自動approved，local approval精確綁新timeline。當次review-pull同時列出舊版audio stale與當時原outline pending，exit 3；不能把此碼當作新音訊未核准，也不能把新audio核准推定其他關卡完成。

五張修正試圖完成6個新take，11張當前鏡頭有passed選用圖，ledger累計US$0.4355。實看空屋、懷特服裝與木材修屋問題已消除；魚草蓆靜物沒有斷頭或額外人物。獨立覆核指出北灣圖雖已改善服裝，但主要工具仍像劍，不當作正確航海工具；改成來源清楚的目的地文字卡，不為此鏡追加購圖。

全90張於 `2026-10-11T19:28:33.858Z` 啟動單批續跑，沿用11張；全套dry-run的全部prompt均在模型上限內，一輪估US$1.22／三輪估US$3.65，當時ledger約US$0.44／有效cap US$80。啟動與單批試圖exit 0均不是全套或成片完成。

## 純物件提示限制與第二次集中修正

續跑實看發現無敵艦隊船體上有巨大人頭、返島小艇內出現泛東亞古裝人物；兩者雖judge過線，不能作為普通英國軍艦或1590年懷特返島人物示意。與北灣道具合為三張來源卡修正，不為這三鏡追加購圖。祖父與新生兒的選用圖則內容正確，主要是畫風偏差；新生兒選用圖實為閉眼，不把別的take的睜眼問題推定到選用圖。

獨立逐鏡提示檢查指出未生成的純物件／環境圖缺乏明確禁用人物的限制，而全域look含chibi characters。`2026-10-11T19:42:31.7954762Z` 建立本聊天自有STOP，讓手中單位安全退出；STOP完整SHA為 `0a464535db9c31fdcd1e8a6e18c235409c97fd5ebe485132fad7b9dc57d18d9d`，收據 `_audit/stop-created-visual-correction-2.json`。批次exit 0只證明安全停止，不代表全套完成。

停止後選用圖25／90，23張judge passed、2張畫風待人工保留；製作鎖已釋放。ledger累計US$0.763、59張原圖、56次評圖、reserved及reservations皆0，`media/jobs.json`為空。木樁鏡seed2為正式站已記錄的terminal failed（`video_media_upstream_failed`，cost 0），不是未知請求；seed3實已生成、下載並保存於cache，STOP阻擋的是接續評圖／選用完成，並非seed3生成。其263171 bytes及完整SHA已獨立讀回；實看仍有兩個漂浮吉祥物頭部，改為精確的CROATOAN來源卡。既有候選／失敗／cache及ledger全部保留。

集中候選包含四張來源卡、36張尚未生成的純物件／環境提示及6張手部提示；保留所有旁白、claims與時碼。不同代理逐一檢查46個完整before／after，全部before與來源相同、旁白與claims無變、物件／手部分類合理；另一獨立覆核驗證所有實際整數時碼、TTS keys及官方prompt上限，0 lint errors、0超限／0截斷。

`2026-10-11T19:49:15.115Z` 僅套用一次經覆核的46項差異。套用前已保存226個既有來源／canonical檔案，約138MB，複製後逐檔完整SHA一致；未遍歷或複製 `_audit` 本身。來源讀回SHA-256 `294227a3e6ee357312f0c9faa2b23f9cbc22e72bad7e2e1edb3fa8e188eb62c2`、claims SHA不變。收據 `_audit/post-batch-source-delta-2026-10-11T19-49-15-115Z/source-delta-receipt.json` 完整SHA `9b25b28dc6f7a1aab5a45adc3a9116193e2249b76e5b4320ef7ffd4d205b74e8`。此次只寫source與待獨立讀回紀錄，0媒體生成／0付費請求；原圖與正式核准未改寫。四張字卡改變template，因此後續需由官方refresh-evidence刷新timeline及audio核准，不能直接沿用舊timeline的核准。

套用後獨立重驗226／226快照完整SHA及bytes、46項完整重播、18項來源／實際整數時碼／134音檔／TTS keys檢查全部通過。不可變proof完整SHA `f9258494519dbb6b8c4dfdb3eef60a5a948e0c255392b723b3252aa03b8ab40e`；來源差異報告已追加實際PASS，交付helper已綁完整五版本鏈，source-only 30項全過，尚未將缺少的成片項目算成通過。

`2026-10-11T19:50:54.5918739Z` 驗證精確自有STOP與proof、目前來源及全域STOP不存在後，只移除本聊天的STOP並確認已不存在，收據 `_audit/stop-released-visual-correction-2.json`。官方refresh-evidence完成0新合成／0計費字、120請求沿用；全134 WAV SHA及旁白完整SHA均不變。最新timeline SHA `dc836e614a3c748b73ac32f2dd1e3b5f31eeae1953add2b16d9d5034d98c5506`、speech hash `20d0bfc523979b9f`、旁白完整SHA `d94e49a3f8bc79c2676c2a7082d865c0a8c7e9c1ae66e8d94c03fc96961c9b20`。正文原音553.175秒、timeline672.5秒、128states最長8秒，插圖時間占比約69.7%，cadence無問題。

新audio已由後台自動approved並讀回current local approval；review-pull同時指出兩個歷史audio版本stale，這不抵銷當前timeline的核准。全86張新dry-run均在官方prompt上限，exit 0；單批續跑精確沿用22張及其評圖紀錄，其餘64張接續生成，沒有force、清除已知job或重買已可用鏡頭。

## 全套逐圖複核中的集中收尾

全套生成保持單一製作鎖；獨立覆核分小組實開選用原圖，先落地完整SHA與判定。`2026-10-11T20:07:35.593Z` 為46／86張選用圖，44張judge passed，祖父與新生兒兩張待保留畫風偏差；這只是當時進度，不表示全套、分鏡或成片已完成。

實看另確認六個必修鏡頭：沿溪搜索與船長決策的金邊三角帽錯置年代、讀懂留言後的石造拱門、Croatoan地名鏡的近代方窗屋、斷纜圖的現代吉祥物、風浪帆圖的擬人器物笑臉。整批結束後集中換成附史料出處的原生字卡，保留原134句及時碼，0新購圖；「本集判讀」與「事件摘要」不假稱史料逐字引述。南航遠景的小船員可沿用，保留偏差註，不將合理小差異一律重買。

以上修正尚未套用；準備中的source candidate、snapshot工具保持外部唯讀／disabled，不能在當前LEASE期間改來源。需等完整批次收據及鎖釋放，保存所有已知媒體／job／ledger／來源後，才套用最終集中差異、獨立重播覆核及刷新當前音訊證據。原paid候選及judge紀錄不刪除或改寫。

## 全套完成後的18張來源卡修正

完整86張原批次於 `2026-10-11T20:39:13.703Z` 結束，exit 1：80張judge passed、6張需處理；沒有缺圖。分兩組逐一實開選用圖後，最終確認18張有年代服飾、建築文化錯置、擬人器物、額外人物或生成文字的必修問題，改為附出處的原生quote卡。原生文字明確標示史料摘要、本集判讀或條件式例子，不假稱史料逐字引述，也不把可能去向或器物脈絡說成結案。

套用前保留357個檔案、170264017 bytes的完整SHA／bytes快照，目錄 `_audit/final-native-card-delta-2026-10-11T20-46-08-231Z/`；inventory SHA `376c6c8b361552991d9b14ae2cfcb2b8da4459a98b5347d7550bf134389e2580`。不可變snapshot receipt SHA `b2b961e9a3cb7395219ca21c0ac4c916925c12bf09e6875ee6507581dc9ed30f`，另存applied receipt SHA `27c81da47d907ef3c1f659a389745df1e78ad5ad7c7ae818dce6f3173b6c2069`。`2026-10-11T20:46:08.231Z` 只套用一次18個template／data差異，當前source SHA `4dfe4d73dd458323949542ba5c22cd68a7838cbdc237b36543b07ea18620322e`；claims仍 `6db38c75194a57b3361ee9eaab058b46da1f76fa0bab47ac48ea70de187be3a3`。0新TTS、0新購圖、0 API／native stage呼叫；原86圖、失敗候選、評圖及ledger保留。

獨立實際讀回394項全true、exit 0，proof SHA `913ae5039b8b14167311a46537ec666e4d2dc8e787a8facad63a94f001a1d1ee`。逐檔核對357個快照、18項exact replay、134完整line objects／TTS keys、135個WAV含完整旁白、109景／128states／20175整數frames、原86張選用圖SHA及297筆ledger。圖片／評圖ledger重算US$1.9915、150原圖、147次judge，reserved及reservations皆0，沒有pending jobs；此數字不包括TTS等其他費用。插圖減為68張，實際時間占比11064／20175 frames＝54.8401%，仍超過正式門檻50%。此proof只證明來源修正和既有證據完整，不表示成片／交付核准。

祖父、新生兒、器物來源不等於攜帶者、其他器物解釋四張選用圖的內容可以沿用；前兩張及來源圖主要為畫風偏差，另一張僅小背景儲物箱偏差。只針對實際選用take判讀，不將其他候選的睜眼、水印或手部問題套到選用圖。後續由官方accept-best保留原judge與take紀錄，四張及其問題需列在成片審核卡，由站主看完決定。

`2026-10-11T20:51:10.262Z` 驗證394項proof、當前source、確切自有STOP SHA、無製作鎖／全域STOP／pending jobs後，僅移除本聊天的STOP，收據 `_audit/stop-released-final-native-cards.json`。官方 `tts --refresh-evidence` 再次0新請求／0計費字、120請求沿用；134 WAV與旁白完整SHA皆相同。當前timeline SHA `4c9de49bf9536d6d645b6aa3cd40a7301a809bd1149365223910922cbb8ff4c3`，旁白SHA仍 `d94e49a3f8bc79c2676c2a7082d865c0a8c7e9c1ae66e8d94c03fc96961c9b20`，正文原音553.175秒、timeline672.5秒、最長單一state8秒，cadence無問題。新的audio核准、current keyframes綁定、render、成片、字幕、QA與後台實際readback接續處理；未上傳YouTube或公開。

## 現行分鏡與實際渲染覆核

最新audio review `b958b6ae-0978-4cb1-92e0-ca58829020b2` 已於 `2026-10-11T20:51:53.023892Z` 由後台核准，`review-pull` 於20:52:14讀回相同timeline SHA。三筆歷史audio版本stale訊息保留，沒有代替或否定這次current核准。

官方keyframes來源重綁為68張unchanged、0生成／0新增評圖；`accept-best` 只保留四個已逐圖覆核的實際take。現行manifest SHA `92961cfc19a1109001fdc82e1f2b4cde66042580d41eb898c67930acdfc67055`；全部68張實檔SHA及99個unique候選／選用檔均對回快照。獨立405項檢查通過，原judge／takes、297筆ledger與cache不變；診斷收據 `_audit/storyboard-pending-92961cfc-independent-receipt.json` SHA `cd4de15285698757bfb2b1ac285b8cc0be14744020e46f47bc0c5871a86adc2e`。

分鏡review `e8cbd0f9-bf91-4a9b-b8f9-8fff70d9a946` 綁相同manifest，當時後台狀態為pending；後續22:36已核准，見末段。68張／三頁聯絡表及四張保留圖已送達；整體最低分7.18、頂層problems為空，但52張native passed圖仍保存個別soft remarks。以實際payload執行正式站原 `storyboard_check_passed` 函式、threshold=7，結果false；這是保留備註與自動核准條件的差異，未刪除原remarks或改門檻。修復另列 [待辦票](../../../tasks/open/2026-10-11-align-storyboard-approval-with-retained-soft.md)。

原生render於 `2026-10-11T20:54:23.035Z` 啟動，exit 0，60個非shot畫面狀態全部新渲染，無版面／缺字問題。`frames/manifest.json` SHA `fbcee7b24a321044e189eeee34f2e6f4dd6d3c3f1ea0deaa9afa1d3e43f5edc0`，綁現行source、visual hash `75becb74ee2f79c7` 及完整109景。縮圖SHA `93427f863a7eb0a42504aa333c46265b3a8e4970cf3a01045a499a38d1f74b25`，1280×720。

兩組獨立實看分別涵蓋18張新卡、CRO／CROATOAN、三張公有領域圖與縮圖共24張，以及後段9張新卡／3張原比較卡共15個state，沒有阻擋問題；合併不重複範圍為29／60個native still states及1張縮圖。詳 `visual-review.md`、`visual-review-late.md`。前組495項來源／映射檢查通過，QC SHA `78db8e6806989d14f1972661b9010850b34a8941a051372dcf0616d3b971c969`；後組QC SHA `ae5d2f2bea8238a177441cb694d689f1e627b04a516ce4c23c563f5554224cb6`。原前組外部QC文字曾將剩餘native數寫為36，已另保存count correction receipt SHA `c3c63d3162b7993f7cb1047062a8c9a30a4c67c510f3bba46fd39f6121778675`：前組是23／60 native、餘37，加1縮圖才是24；原QC bytes／雜湊和495項檢查完整保留。這是actual still覆核，未聲稱完整聲畫、CC或站主成片驗收。

現行來源的199項影片文件測試全過，0 failed／exit 0，日誌 `_audit/docs-video-tests-final18.log`；lint為0 errors、5項構圖字詞警告，實際多樣性已在上述逐圖覆核中判讀。1080p assemble單次啟動，未使用force／adopt；下段記錄實際結束碼及成片讀回。

## 成片、字幕與送審讀回

assemble於 `2026-10-11T21:24:41.780Z` 結束、exit 0，109／109景完成。成片 `final.mp4` 為1920×1080、30fps、20415幀、680.5秒（11:20.5）、204325624 bytes，完整SHA `d86471c94a661023f697f2261bab8c8a61a8bf203a1a1c09b9f3ace28eb1c5a6`。正文20175幀／672.5秒，原音553.175秒，未以延長停頓補足八分鐘；正文檔SHA `a061ad4c1a6b2ce6cdfa745da88afc8d0bf57a3e6e2c67f656bb1cc173654806`。`checks.json` 為ok true、problems空，−14 LUFS／true peak−0.9 dBFS，42個採樣與來源畫面相符。

實際品牌套件為 `mokaair-brand-package-v2-cc`，adopted SHA `a27622022d8d9e2f56221a81a1d7443ab241c40a37a515925784511f0416dcdd`，150幀片頭及90幀片尾。這是既有全域套件，沒有新購音樂或音效。captions於21:25:00.478Z結束、exit 0，繁中134 cues、0問題；第一句05.000→09.180已計入五秒片頭。SRT SHA `c8d49f959b2c898384a25f8fa0dc47251805e27b421e212df432c42d5aa22112`，VTT SHA `9eef2af4e7870589af9185602eebc8ff9367c5d9f2447ab652dc8452fb3a764e`；`burn_in:false`，外掛CC播放器顯示未驗收。

`review-push --gate final` 單次完成exit 0。QA綁完整成片SHA，9／11通過；captions因尚未選額外語言而缺工具預設要求的英／日／韓，links則兩個Smithsonian網址自動GET回403，瀏覽器正文可讀的既有證據保留，不改寫QA結果。新成片review `a3f6b386-f6ec-41ce-a5e2-9ded114a605b` 為pending、manual_review=true，明列四張保留圖及原judge意見。720p附件25101154 bytes／SHA `623f66b9e8ceda9dcda4cab8123ee7235c536628756d394ba3fd290997cecdf1`；與1080p成片是不同檔案。

21:28:26.297Z實際後台GET讀回：大綱A與當前audio approved，分鏡 `e8cbd0f9-bf91-4a9b-b8f9-8fff70d9a946`、成片 `a3f6b386-f6ec-41ce-a5e2-9ded114a605b` 均pending，YouTube ID為null。review-pull native exit 3保留等待決定。consumer audit七個附件角色／size／本機完整SHA相符，只有兩個pending關卡各缺approved／decided_at四項gate錯誤；這不是遠端bytes或完整播放證據。獨立附件讀回21項通過，收據SHA `1d4d59e17734f9047efb191b5266917d21e54ec54d0ff485b83041c230650197`。實際Chrome成片卡片與人工審核提示截圖在 `_audit/h02-final-review-browser.jpg`，SHA `2fcaa48f14d1ee50d958068ef1256b9d839bc927b3806e74b77330c1b72e20eb`；播放操作逾時，未將海報載入當作播放完成。

## 獨立成片檢查與界線

唯一一次full audit共299項，290通過／9未過，原收據 `_audit/delivery-audit-full-20261012.json` SHA `2b50bae4122f6398d78d3f135ca05b0bcd59397057ca030fb01e864891cb4fbe`。八項是額外字幕三語缺件、QA非11／11、分鏡／成片／publish未核准及上傳metadata缺件；另一項為正文 `avg_frame_rate=15494400/516461`（約30.001104），不等於helper要求的exact30。正文實測20175幀、r_frame_rate=30/1、容器672.5秒、video stream672.475260秒，差24.74ms。成片實測20415幀／30fps／680.5秒，H264／AAC48k stereo；原音、正文及成片完整decode各exit 0，但null muxer重複DTS警告12974／13124仍保留。這些數值沒有取代人耳聲畫同步或完整播放器驗收。

為確認新警告，另作兩次純packet metadata讀回，未重跑decode或修改媒體。正文20175／成片20415個video packets，原PTS及DTS沒有重複，packet DTS沒有非單調；將精確有理數換算成30Hz後，正文12974／12975及成片13124／13125各落在同一格，成片索引多150幀、正好五秒片頭。這重現了null muxer警告，支持時間基取整的解釋；不把精確CFR／完整聲畫同步改成PASS。正文及成片完整SHA在讀回前後不變，原full audit的九個FAIL完整保留。新收據 `_audit/timestamp-packet-readback-20261012.json` SHA `997c2d22695a00dfdd4a210ae8c05c1b25fd9bd87bbecbf00ff590563b48423e` 保存兩個raw packet JSON及其完整SHA。

分類收據 `_audit/final-media-classification-20261012.json` SHA `5ac9d61f93127efc6144e1375afdd10d58d6e25f7861067b8ff79adcf3cc3785` 將本機媒體／字幕／雜湊的已驗項、正文strict FPS差異、null warnings、QA9／11與待站主關卡分別列出；沒有覆寫原full audit、helper或canonical媒體。

成片抽樣實際開啟19個unique PNG，16個正文點加4個品牌相鄰界線（最後正文格共用），175項來源／frame／bytes檢查通過，未見阻塞視覺問題。QC SHA `76ba8578e8374404bdb719f97220d49812dfbecf589af6260d24681acfdb82b4`，詳 `visual-review.md`。抽樣helper原1ms PTS guard對正文尾段最多24.74ms差異回exit 1，原收據保留；新recovery receipt SHA `1385bd833d59369ee1544f7ea5746f9b071560611fc09bfecc61d4224bae583c` 明列nominal frame time與actual PTS，沒有重擷取或假稱完全同步通過。抽樣後成片完整SHA未變。

上述21:28交付時，package工具因成片待核准而未執行，沒有上傳YouTube或公開。當時等待站主確認四張保留圖及本集語言；後續決定與完成紀錄見下段。

交付文件的獨立覆核確認299項分類與待驗界線；delivery摘要補明第八項為QA未全過，原覆核收據保留。推送前task check通過1850檔；staged whitespace check只有凍結brief末尾空行提醒，排除此一檔後通過。brief完整SHA仍 `7475f2d93110b9cde572aac2531ccd77ec98a0e23f7c922987eff69b9d221404`，保留已核准bytes，沒有為格式提醒改寫來源。兩支Shorts仍只是腳本；本次只修其中JSON多餘末尾空行，未製作Shorts媒體。

## 站主核准、繁中選擇與完成上傳包

站主回覆「只出繁體中文（建議）」及「核准分鏡與成片，只出繁中（建議）」，包含審核問題中列明的四張保留圖。原分鏡及成片卡分別於 `2026-10-11T22:36:39.268917Z`、`2026-10-11T22:38:46.372034Z` 保存approved，完整hash仍為 `92961cfc19a1109001fdc82e1f2b4cde66042580d41eb898c67930acdfc67055` 與 `d86471c94a661023f697f2261bab8c8a61a8bf203a1a1c09b9f3ace28eb1c5a6`。正式GET及本機review-pull均確認；沒有再問相同核准，也沒有新製作或重購媒體。

後台「只出繁體中文」實際保存 `locales={}`，決定時間 `2026-10-11T22:39:38.663108Z`。本機以官方 `writeLanguages` 從該讀回同步，沒有虛構時間；`languages.json` SHA `c107ffc1b2d1cf4405a918d5d915e8183852db37911b6dfb6993ce7ab6f9effe`。批准／語言收據 `_audit/owner-approval-language-receipt-20261012.json` SHA `cf98d557c041ff595fadb8671ff31c694d0fff1526e2e3f68ed80697d92b9bf7`，原QA、字幕manifest及後台快照完整保存於 `_audit/owner-approval-snapshot-20261012/`。

製包前獨立source/media檢查99／99通過，68張selected圖片及所有來源／音訊／成片pins不變，收據SHA `269f8e7cbcd79449568bb6e7461600c728705e9995f0ed0cff64fd6ce68fe7b5`。captions與package分別於22:40:10及22:40:11啟動，均exit 0；134 cues仍為原SRT/VTT bytes，無其他語言或dub。`upload/metadata.json` SHA `e616ccd4515b2c7ba382b25903a3f9f73fec4ab0e5fce32e46a5e4a46b07d89e`；包內final實拷與已批准MP4完整SHA相同。

獨立package覆核42／42通過，收據 `_audit/zh-TW-package-independent-readback-20261012.json` SHA `c4cbcb47eb0a3935a47052b44d79d27dfdcfef2e1bb4e7c81192e30df92ed3ca`。官方四項包檢查全過，七章／來源／圖片credits／繁中說明與官方compose結果相同；官方 `captionsItem` 對當前繁中選擇單項通過。原完整QA9／11及原full audit九個FAIL均原樣保存，未重跑解碼或付費政策judge；兩個來源GET403及播放器驗證界線不變。

`review-push --gate publish` 於22:41:53完成exit 0，review `fb4ff837-1f5b-4a32-8f7e-baa27a251f9d` 已approved，決定時間 `2026-10-11T22:41:53.985239Z`，綁上述metadata完整SHA。五個附件為繁中SRT（12290 bytes／`c8d49f95…`）、繁中說明（4170 bytes／`ce74effa…`）、完整成片（204325624 bytes／`d86471c9…`）、metadata（5792 bytes／`e616ccd4…`）、縮圖（132769 bytes／`93427f86…`）；實際GET讀回及本機批准同步完成。後台 `ready_to_upload=true`、`youtube_video_id=null`；stage字串 `on YouTube` 是流程下一步，不表示已上傳。Chrome實見「可以上架」，「已上YouTube」未勾；證據 `_audit/h02-ready-zh-TW-20261012.jpg`。

製包另發現共用 `UPLOAD.md` 模板把category27誤寫「科學與技術」。本repo schema明定27 Education、28 Science & Technology；本集metadata保持27，本機操作說明只更正為「教育（27）」並保留原檔。原說明SHA `64d1559fe9adfd54010b7fd803ab9244dd86086479b4c98fa8ac79209f2f9167`、更正後 `2e967201f934954e3708b0263c454b5c0ac8af365632091f66ff944e36966ca7`。UPLOAD.md不是送審附件，五個附件及metadata完全不變；共用程式另開 `2026-10-11-render-upload-checklist-category-labels-from`，本次不越scope修模板。

最終publish獨立覆核41／41通過，收據 `_audit/final-publish-package-independent-readback-20261012.json` SHA `8e3442f4c7c3761e6d85066739aa74009f5cb4ba7bda8e0f8b41ab9b2ed3455c`：五個附件metadata與本機實檔hash／size／type均相同，四個current本機批准有效，語言決定時間吻合；重讀官方包檢查4／4且與publish payload相同。原UPLOAD說明比較恰一處label修改，metadata與媒體不變。遠端consumer GET實際bytes仍未另驗。

交付狀態為站主已核准的繁中上傳包。沒有YouTube上傳、排程或公開，也沒有merge／deployment；完整播放器播放、聽音及CC疊字未另由代理驗收，不能從正式批准或4／4包檢查反推。
