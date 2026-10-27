# DuckDB2.0：視覺元件與22份附件已驗證，音訊及正式成片待完成

2026-10-27T15:24:42.199Z，正常初始恢復程序（累計attempt2／retake0）以exit4結束：同一句dg2i收到5次HTTP429，原生按Retry-After正常等待4次後到達每句5次上限。本輪沒有第6次speech POST或第三個製作程序，音檔仍0；前次1次加本次5次，累計6次speech POST。見[本次實際退出](receipts/master-audio-resume02-20261027/actual-native-exit.json)與[獨立實體核對](receipts/master-audio-resume02-20261027/independent-refusal-review.json)。所有未知請求、原品質結果與既有22份後台附件保持，沒有帳單或零扣款宣稱。

2026-10-27T14:37:26.315Z，正常初始TTS程序實際結束為exit4（PID381994／session16864）：1個status GET、1個speech POST，第一句dg2i的23字元請求回HTTP429 `video_speech_upstream_busy`，Retry-After為10秒。這次受限程序停止原生等待，沒有第二次HTTP送出、成功WAV、旁白或時間軸；不是完整111句合成。見[真實退出](receipts/master-audio-initial-20261027/actual-native-exit.json)、[原始回覆](receipts/master-audio-initial-20261027/provider-response.json)及[獨立失敗驗核](receipts/master-audio-initial-20261027/independent-failure-audit.json)。

先前所有新TTS暫停是Root本地排程決定，不是站主禁止其他影片使用不同的新請求。本次DuckDB獨立首次製作在原111句／2508字元額度內明確授權，沒有動ForTy PT3cc1／ES9a36或Kimi未知請求。當前是已知忙碌回覆的服務停點；未來可在冷卻後另立一次受限的正常初始resume，沿用當前plan、cache、journal與原句上限，不必等待ForTy舊計費事實。這不允許自動重試迴圈、重跑已消耗的first helper、forget、清旗或啟動另一條ASR鏈。

截至2026-10-27T09:56:16.602807+00:00，64張原生圖卡與繁中加八語共9張JPEG縮圖已實際製作並逐張驗收；同一待審SCRIPT已附22份視覺元件，正常完整下載及獨立bytes／SHA查核完成。[當前進度](production-progress.json)、[實際元件索引](receipts/visual-components/index.json)與[完整下載證據](receipts/visual-components/normal_full22_proof.json)分列範圍。

22份為9張縮圖、聯絡表、9份完整原始標題說明草稿TXT、原生frames manifest、誠實元件報告及128秒無旁白視覺樣片。64張真實圖卡依稿件順序各停2秒，這是檢閱速度，並非實測旁白或章節時間；沒有把樣片當成正式成片，也沒有ZIP或64張PNG後台交付宣稱。

繁中已完成兩次初始程序嘗試：前次1次、本次恢復5次speech POST，均回HTTP429 `video_speech_upstream_busy`，未取得音訊，raw仍0。actual audio timeline與CC尚無；八語已驗M4A仍0/8，fit／meter／ASR、正式語言包、至少480秒正文、正式成片及完整QA仍待完成。原生靜態字標不等於官方5秒片頭／21秒片尾，本片尚未套用動畫bookends。

當前來源[video.json](video.json)SHA `1c475c928a02a6f584dd224ecfed1c5fafd53aa4bf1795c7a3758699692a12c8`；只刪除4張卡片被裁切的可選重複title，相同文字保留於key。正常快取render重用60張並重畫4張，原64張實看中的4項裁切失敗、4張替換圖的真實複審，以及初次native0／outer1縮圖失敗均完整保留。[視覺delta](receipts/visual-components/source-visual-delta.json)也記錄ES／PT／ID／VI四個縮圖短標的正常metadata merge；111句完整line objects、全部八語targets與完整metadata不變。

[script.md](script.md)仍為7aac，既有SCRIPT `dd47b9a0-6456-4651-9456-32b320909338`仍pending；新增附件不構成server／UI批准。40eb的verify4及source-gates保持原來源綁定；兩份原生敘事結果仍各12/13 false，教學取捨不改raw失敗或門檻。

| 語言 | 當前i18n SHA-256 | 範圍 |
| --- | --- | --- |
| en | `faf5cb2f1c7fd536e012cd2a8191062ee4069d42ef46b8b8fbf8f10543f2cf4b` | 111句／六章／完整metadata；CC及M4A未完成 |
| ja | `324c6f070993c1fc1b08f18d5f9131527eb24278e8ff4f200dfb63c6db4b83f2` | 111句／六章／完整metadata；CC及M4A未完成 |
| ko | `6b1e38d9b3e868a5cf312a1cb0180f88b43d5741aad0bb1959f9e9d0f8738d0f` | 111句／六章／完整metadata；CC及M4A未完成 |
| es | `61cf0a0077d9cf9fd3b93d8117bf3975dc162a982acc981213af6789e1889b9c` | 111句／六章／完整metadata；CC及M4A未完成 |
| pt | `43dc7e4434394fb72def2921db8a4201d32d0b66bac73a8deaab146407b5db6e` | 111句／六章／完整metadata；CC及M4A未完成 |
| id | `a71014a6452b76e081f276bd6cf628015c1d4a1cfbc9e04bda6ebc4975ce262a` | 111句／六章／完整metadata；CC及M4A未完成 |
| vi | `198c81025f5164c9c8e2d2e9ff821743674342f14a90a0c10691485967b68623` | 111句／六章／完整metadata；CC及M4A未完成 |
| th | `0af06dff9045602f026526516e3d7d10c1c689effa9c06c1a5d57d8eb257d544` | 111句／六章／完整metadata；CC及M4A未完成 |

原創1,200筆配送教材、480筆完整條件交付與720筆需求變式，見[可攜教材](public-run/README.md)；公開CSV／ZIP的既有200／SHA證據保持。

五份原始摘要已[逐bytes封存](history/before-visual-components-docs/identity.json)，舊索引／freeze保持原位，未遞迴複製history。本次公開proof只含明確審查過的文字／JSON／真實log，不含媒體、私有project、credentials、profile或release。PR1861維持no-auto-merge；本票尚未done，責任與原branch／PR1861延續；未merge／deploy／上傳YouTube。


## 正常初始恢復 attempt3 — 2026-10-27T16:29:20.998500+00:00

Root session10397／PID1005於16:25:20.126Z真tool/native exit4。同一句dg2i依原生上限收到5次HTTP429 upstream_busy，正常等候4次後停止；raw0、無新增旁白／時間軸／CC／M4A／成片或後台媒體。累計initialprocess3／speechPOST11／retake0／rewrite0，沒有第四個程序或自動迴圈。

[實際退出](receipts/master-audio-resume03-20261027/actual-native-exit.json)、[HTTP事件](receipts/master-audio-resume03-20261027/http-events.jsonl)與[獨立失敗保存查核](receipts/master-audio-resume03-20261027/independent-refusal-review.json)均綁實際bytes；查核確認原E844／W948、3held與10份前次收據完整。這是失敗證據保存，並非音訊／聽校／品質核准或帳單結果。原111句、八語文字、native品質false與歷史失敗不變。已正常release／blocked，責任同對話及PR1861；尚未done，無背景製作工人。


## 初始恢復 attempt4：原第一句單次請求 — 2026-10-27T17:19:56.114447+00:00

Root session95755／PID2587於17:15:59.599Z真tool/native exit4。原稿第一句dg2i單次POST仍回HTTP429 upstream_busy；較窄的首句dispatch上限保存真nativewaiting收據後停止，無第二次POST或實際等待，也無新音檔／時間軸／CC／M4A／成片或後台媒體。累計initialprocess4／speechPOST12／retake0／rewrite0，沒有第五個程序；其他原生上限與品質門檻保持。

[實際退出](receipts/master-audio-resume04-20261027/actual-native-exit.json)、[HTTP事件](receipts/master-audio-resume04-20261027/http-events.jsonl)與[獨立失敗保存查核](receipts/master-audio-resume04-20261027/independent-refusal-review.json)保存實際bytes。原E847／W948、4份hold（含全域ASR實際LEASE）與15份舊收據完整；原111句、八語文字及所有歷史品質false不變。查核只確認失敗保存，沒有聽校或計費核准。網站月字數與10秒等待值無法判定供應商配額及恢復時間，已首次詢問供應商端currentTTS配額／錯誤代碼與重置時間；未要求金鑰、未重問ForTy舊facts。先取得新的服務恢復資訊再評付費續作，不因同一句續作訊息自動重開。已正常release／blocked，責任同對話及PR1861，未done／移交。
