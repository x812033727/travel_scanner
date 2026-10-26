# Claude形式驗證255：首次聽眾重述八句定向事實複核

RESULT: PASS

2026-10-25 UTC。**八句均保留原義、數值、否定、輸入域與公開release範圍；0 must-fix、0 not-found。** 這是八句文字重述的事實／語義收據，沒有宣稱新版配音或ASR已通過，也不是重查整個105句或歷史112句的全輪收據。未執行付費ASR／TTS、未聆聽新WAV、未改來源、提案、flags、cache、逐字稿、舊verify或其他檔案。

## 實際版本綁定

- 當前video.json SHA256：`232b4495b433041007c039630ec517b7e0b4948c3cd7a5a47da6ecd88cae8a15`
- 當前claims.md SHA256：`527048b6061d21f70e00475cc4790a46b0de6e536a37e8966402194a043fa9c6`
- 舊版archive：`/workspace/work/ai-tech-next/formal-audio-archives/before-listener-reword1-20261025T2040Z`
- archive video SHA256：`a77c48e48131a2a17196cbddf2bf192f33c02c9d5defc3953a543155e441514d`
- archive claims SHA256：`134e8e888f6aba07ed4da185b8d97f26e0ef65877c542684fe0433ed08e1b1d8`
- `audio-reword1-proposals.json` SHA256：`1754d9941c63a753c79b5baca3075d3dbe2b6ce299cdcf5b7c6a20a4983ea25e`
- `audio-reword1-application.json` SHA256：`5894f183aed25c187ff42c8abd45e68c07aae8bd16a6e886e798ac43a86e8d98`

本輪直接讀archive與當前JSON，不只採用application自述。依scene／line ID比較，確定**只有以下8個line.text改動**，105個ID與順序一致，其餘97句相同；將這8個text還原後，完整JSON物件與archive完全相等，因此所有code、圖、data、metadata、voice設定與其他非text欄位未改。當前claims的8個新句還原後，和archive claims全文字串相等，沒有其他段落變動。另逐條核對當前105個quote與當前JSON，全文及序號均匹配；這是引句一致性檢查，未冒稱105項新來源查核。

## 八句完整核對表

表中HTTP沿用同日verify-1／verify-2的200及本地原始證據，本輪不發新HTTP。LOCAL公開來源為 https://github.com/x812033727/travel_scanner/tree/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data 。數值／控制模型沿用已綁hash的原始產物，沒有新增執行結果。

| # | Scene／line | Before → after（實際當前句） | 證據／HTTP | 判讀 | Verdict |
|---|---|---|---|---|---|
| 1 | deny-all-preview／z9dp | 紀錄上只寫不收錯的，全部拒絕能算修好嗎？ → **紀錄上只寫不收錯的，全部拒絕能算完成嗎？** | LOCAL `sat-output.json`、完整接受契約；目錄200，當日既有證據 | 「完成」仍指同一修正的驗收；只、不、全部均保留，仍為待答問題。沒有把一律拒絕說成已符合完整功能。 | CONFIRMED |
| 2 | zero-passes-capacity／femu | 拿零和容量八比較，它於是回傳接受。 → **拿零和容量八比較，程式就回傳通過。** | LOCAL `guard.c`、`results.json` n255；目錄200，當日既有證據 | 0與8均保留。`return total <= CAPACITY`在total=0時回傳bool true；「通過」是此布林結果的白話，不宣稱函式回傳中文字串、接收資料或寫入buffer。 | CONFIRMED |
| 3 | only-extra-accepted-value／dfhy | 錯版多接受的只有二百五十五；加寬版則接受零到七。 → **錯版額外放行的只有二百五十五；加寬版只放行零到七。** | LOCAL完整256列、`bad_false_accepts=[255]`；目錄200，當日既有證據 | 「額外」保留唯一多出的255，不誤成錯版僅接受255。加寬版的只／0..7保留；原域及錯版原有0..7沒有消失。 | CONFIRMED |
| 4 | symbolic-versus-compiled／tksv | 模型的結果，還逐值對回實際C程式，二百五十六列全相符。 → **模型結果逐筆對照C語言程式的實際執行結果，二百五十六筆全相符。** | LOCAL `symbolic-vs-c.json`；目錄200，當日既有證據 | 比較雙方仍為符號模型與實際C執行。256筆及全部相符均保留；C語言只展開原名稱，沒有改為Rocq、官方重現或獨立proof certificate。 | CONFIRMED |
| 5 | complete-acceptance-contract／4akm | 兩個方向合起來，就是應且只應接受零到七。 → **兩個方向合起來，零到七都要放行，其他長度一律拒絕。** | LOCAL數學契約`n+1<=8`及前文域`n=0..255`；目錄200，當日既有證據 | 拆成雙向量詞：0..7全部接受，其餘8..255全部拒絕，等價於原iff。**「其他長度」限前文既定0..255**，未擴張到負數或任意大整數，也沒有把單向安全當完整契約。 | CONFIRMED |
| 6 | timeout-not-enough／ihny | 單靠這次逾時，還不能判定。 → **這次超過等待上限，光憑這點還不能斷定程式永遠不會結束。** | LOCAL `loop-results.json` timeout=0.25，另有有限控制圖；目錄200，當日既有證據 | 明確保留不能僅由本次timeout推出不終止；沒有保證一定終止。前句的0.25秒觀察及後續固定n的256步環理由各自保留，未把等待當證明。 | CONFIRMED |
| 7 | counter-record-fields／5feu | 我把返回值和離開條件，分開填進同一列紀錄。 → **返回值和離開條件，在同一列紀錄分欄填寫。** | 未改的scene.data兩欄與LOCAL loop結果；目錄200，當日既有證據 | 返回值與是否離開仍分欄、同列，沒有增加「無法返回」的否定。移除我把只調整主詞，未合併數值與終止要求。 | CONFIRMED |
| 8 | separate-halting-statement／4nfp | 這說的是這份公開版本，不能推成整個研究都沒處理終止。 → **這說的是這份公開版本，不代表整個研究都沒處理終止。** | https://github.com/theorem-labs/oss-verify-proofs/blob/main/README.md 、`docs/statements.md`；同日200，verify-1原文收據 | 公開release限定與外推否定均保留。沒有宣稱所有239研究案例已證或未證終止；前文僅此release沒有已證halts命題不變。 | CONFIRMED |

## 未改內容與原始程式

完整JSON還原比對證實code和卡片均未動；另重新計算兩份原始C的SHA：

- guard.c：`4bfc837e2f17c1ae8326924a926929ee3d8dec29e88ec355b77db591c0d9e799`
- loop.c：`b1d181702c61b152724eeeb693891f45005e7ca0c7dfa583cb5378a6fc68f0a2`

因此前輪已核的完整guard RHS、loop宣告與更新轉型兩處、兩C獨立、官方kernel／wrapper／allowlist次序、plain預算前提、有限可觀察紀錄集合與release-only no-halts均沒有因本次重述而改動。沒有新增數字、輸入域、官方產品／研究主張或第三個實驗。這八個同義重述不是八項新事實變更。

舊verify-1與verify-2重新hash仍分別為`343ae6c16019587edb5b1da34a9cfbe835671c281300db43c40cefda2ace3be8`及`2f1a3f1af227ca63ce66ba14724a60d2a8409c6b31375f45f64471fa7320c5b1`，原REVISE／PASS結論與綁定維持歷史。

## Native與結論範圍

實跑native lint：**0 errors、3 warnings**，仍為25秒短開場與255／256重複算步的敘事heuristic；沒有為解除警告刪掉事實。105句及IDs不變。文字估時已隨重述改變，不把舊版560秒WAV或舊522.7333秒正文音長當成新版實際音長。

原ASR訊息只說明為何提出這次較清楚的文字；本收據沒有認定ASR差異必然代表人耳聽到錯誤，也沒有清除其flags、逐字稿或cache。**新八句仍須走正常生成與實際音檢。**

- 本輪查核八句：8 CONFIRMED；0 CHANGED pending；0 NOT FOUND。
- 105個claims引句匹配；97個未選句及所有非text欄位未變。
- 意見／站主經驗／承諾無新增不實之處。
- 事實／語義結果：**PASS，只綁本頁列出的當前video與claims SHA。**
- 本輪無新增事實修正，不觸發超過3事實變更的換人全輪二查；音訊／字幕fit／敘事盲讀／成片另走既有關卡。
