---
id: 2026-10-08-ou-de-jianghu-visual-handoff
title: 《偶的江湖》角色資產鎖定與第一集動畫試播交接
status: in-progress
priority: P1
area: docs
owner: claude-fable-5.1
claimed_at: 2026-10-09T10:58:58Z
created_at: 2026-10-08T10:52:24Z
completed_at:
branch: codex/ou-de-jianghu-visual-preproduction-20261008
depends_on:
  - 2026-10-08-ou-de-jianghu-animation-reference
  - 2026-10-08-ou-de-jianghu-scene-prop-design
  - 2026-10-08-ou-de-jianghu-external-look-import
scope:
  - docs/videos/series-plans/ou-de-jianghu/visual-development/handoff
---

# 《偶的江湖》角色資產鎖定與第一集動畫試播交接

## Why

把採用圖、參照和正常look綁到同一來源，第一集試播才能沿用同一張臉；production README仍寫過期14人。

## Definition of done

- [x] 9人資產manifest含來源commit／SHA、角色／look ID、用途、版本、媒體hash、judge與站主接受狀態；額外綁shot_looks目錄hash，不冒稱原生lookHash已有。
- [ ] 經正式匯入走正常look／choice／series-store；用少量已授權關鍵影格核對真正讀入的reference及當鏡造型文字，保存實際結果，不假填。
- [ ] 劇本／look／audio／storyboard／plan lock分別列；前期畫像完成不等於動畫完成。完成原持有人交接後更新production README，將前置條件接回既有試播票，保留連續三鏡及站主接受後放量。

## Steps

- [x] 讀[前期總覽](../../docs/videos/series-plans/ou-de-jianghu/visual-development/README.md)、[造型規格](../../docs/videos/series-plans/ou-de-jianghu/visual-development/character-design.md)、[製作清單](../../docs/videos/series-plans/ou-de-jianghu/visual-development/production-list.md)，重新核對來源與既有授權。
- [x] 完成可審交接文件，將實際證據及未決問題記入本票 scope；正式採用／正常runtime與原持有人接線仍保留待辦。
- [x] 候選實看與獨立核對範圍、匯入收據、SHA及圖冊驗證已整合；正式製作條件尚未滿足，收尾release。

## How to verify

逐項查驗實際文件／圖檔、來源及媒體雜湊與接受紀錄；涉及圖像必須實看，prompt／lint不能代替圖片驗收。

`npm run check:tasks`

## Notes

- 2026-10-09 Claude 接手（claude-fable-5.1）：依站主「接手完成第一集、沿用原方案與預算、十一鏡改案不採用」接續。歸檔 Codex STOP、取得新 lease（owner claude-episode-one-finish），授權檔只換 lease 持有人（備份 SHA 02858b41…），上限、take cap、來源 SHA 不變。用內建瀏覽器（站主登入）以作品詳情頁「無水印下載」回收 9 筆已付費原任務（3 張 t2 首格、6 支影片，無重送），逐筆入帳並寫 O/qa 收據：075/090/091 t2 首格候選，080/087 候選，046/049/053/055 有限候選（053 冠自首格起裁、055 落刀行程極短無火花）。接著按原案付費 6 支影片共 336 點：086 t1、045 t1、064 t1、091 t1 候選；090 t2 有限候選（與 087 銜接待核）；075 t2 HOLD（動作由沈而非寂聞執行，影片 take 已滿 2 次）。A 期實扣 7,015＋未知預留 70＝7,085，餘額 54,985。內建瀏覽器無法選本機檔，首格以頁面 JS 抓海螺 CDN 無水印原檔（SHA 逐張核對）注入上傳框；提示詞以 Slate 編輯器 API 寫入並核對。帳本、收據與下載紀錄在外部 O/claude-recover-20261009 與 F/actions。未改 source／lock，無購點、無 API 費用，未合併／部署／發布。
- 本輪本機成果：對白 D 軌候選 13 鏡（O/next-D-claude-20261009，087／049／064 場末停頓溢出、086 台詞 6.58 s 超過 5.17 s 片長待剪接決定）、下一批 12 鏡首格封包（O/claude-next-batch-20261009，A94–A105，prepared_not_submitted）。停在：把 12 鏡加進 active_batch 並調內部操作額度（7,600→9,200）被分類器擋下，未繞過；9 張參考圖在海螺頁面找不到既有上傳副本；首格以頁面 JS 注入 CDN 原檔的做法與 browser-production.md 第 1 節有張力，均待站主裁定。站主放行後第二輪：12 鏡加入 active_batch（版本化備份），066／072／085／092 首格＋影片各一 take 共 281 點，8 項皆候選，收據在 O/qa；A 期 7,366、餘額 54,704。其餘 8 鏡等 9 張參考圖來源決定。站主「先跳過這 8 鏡」後第三輪：A106–A119 參考齊全的 12 鏡（a02-s008/012/017/018/020/023/024/025/032/039/043/045）首格＋影片共 934 點，11 鏡候選、020 t1 HOLD（錯誤角色執行動作）、t2 有限候選（燕迴以刀臂攔人，take 已滿）；D 軌 10 鏡建好、045 無台詞；A 期 8,300、餘額 53,770。第四輪（站主「封包好了就繼續送」「額度不夠先做到邊緣」）：packet 3 的 12 鏡（a02-s064/071/072/073/083/084/089/094、a01-s040/042/018/023）首格＋影片共 861 點，首格 11 候選＋042 有限、影片 11 候選＋042 有限；A 期 9,161／內部額度 9,200，餘額 52,909；另 34 鏡因參考圖缺提供者端副本跳過。全集估算：剩餘約 24,200–26,700 點。完整進度在 [CLAUDE-PROGRESS-20261009.md](../../docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/CLAUDE-PROGRESS-20261009.md)。

- 2026-10-09 owner 明確要求轉交 Claude 並「收尾停止」：Codex 停止新增生成／API，交接入口 [CLAUDE-HANDOFF-20261009.md](../../docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/CLAUDE-HANDOFF-20261009.md)，外部 E 根目錄亦存同名副本。停止時 133 圖像 take／89 鏡、61 影片 take／57 母鏡（32 候選、10 有限、15 HOLD），尚 363／420 母鏡無下載；597 錄音候選存在，不代表完成剪接／聽驗。A 實扣 6,679＋unknown 70＝6,749，最後 UI 55,321；API估值含未知 US$0.3638495 不變。9 個已付費原任務尚未下載（3圖／6影片、354點已計入），group IDs 全列交接；不得重送。a02-s086-video-t1 在 intent 前被 guard 拒絕，未送未扣；最終表單混入人工輸入文字，不能直接點建立。
- 已寫外部 E/STOP（SHA `17718bbcbc43d89c3b7d04b9d35e17e9e90a6ac62270fd169ac62da46c3f4e60`），lease guard 回報 `lease_released`／exit0，原PID35956已退出、LEASE不存在；沒有背景繼續下單，海螺已送遠端任務可能自行完成。唯讀預覽8784保留。075/090/091 t2仍待原結果下載及QA；新增首格056/061/063 HOLD、064候選及048/092未送t2備料均已列交接。DoD未完成，本票release供Claude接手；未commit/push/merge/deploy/upload。精確收尾驗證外部 O/claude-stop-receipt.json。

- 2026-10-09 本輪續製進行中：站主明確回覆「保留原方案，先做其他鏡頭」，十一鏡修正不採用、不套用；外部 `finish-episode/eleven-shot-decision-20261009-deferred.json` SHA `0ae4f2206fe9c4b2f60b4ddac67bf8261329f102ccdfff0d2f3dc06ba2b47585` 綁定原話及已展示提案。原 source／A、B 總上限／每鏡 take cap 保持，原 HOLD 與 a01-s082、a02-s030、a02-s033 三筆 unknown／70 點預留均保留。只續做未受變更影響的原案；不能把 deferred 當放行。
- 2026-10-09T09:21Z 非終態快照：外部 `finish-episode/throughput-resume-20261009/current-turn-status.json` SHA `8ba0fc8a22f17146fc35a7d09d425f4532c5ee9afcf663019e227843b97af815` 補合併 previous 原 15 actions／475 點後，已下載 107 張 image takes／68 鏡、50 支 video takes／47 個不同動態母鏡，含原 pilot 與 HOLD，並非可用或採用數；後續仍在下載／判片，不把此快照冒稱最新終態。新增完整原音窗口／原 pause 的 D 候選及 15.208333 秒 pilot M/A/F 試混，分軌與可編輯工程已存；未實聽／未 owner 採用，重疊版本不得相加當新增母鏡。597／597 錄音候選及 API 估值 US$0.3638495（含舊未知預留）不變，沒有新增 API 請求。

- 本輪等待下載交接：上述兩個新增剪接MP4及原始D軌皆已落盤；1692票格式檢查、scoped diff check通過。製作lease正常release／exit0，原PID11428不再執行；本票release回open，沒有背景繼續下單。003原任務只待同一成品下載，不重生成；031起點限制、033／030／082未知結果與各自預留、其餘未製鏡與六鏡待決均保留。本輪只增加外部媒體及本票交接，未改源劇本／正式採用，未合併、部署或發布。

- 2026-10-09 本輪新增可播候選：外部 `finish-episode/assembly/throughput-resume-20261009/` 已輸出 067→068 中文 D 軌 MP4（8.833333秒）及070單鏡（3.766667秒），合計12.6秒，各保留獨立48k D.wav。5句既有WAV PCM逐段一致、原pause保留，兩片完整AV解碼過；尚未實聽／口型／正式採用。069完整台詞加原pause為5.30秒，超現片5.166667秒，留待切點核對，未跳過它串片。站主回覆「已恢復」後重新綁定IAB tab9，實見003任務已完成（00:04）、餘額58,310；下載事件卻因工具無法取得授權決定而失敗，並非明確拒絕。保留原任務，不繞過下載安全控制，已請站主手動下載同一支無水印檔；003仍不算本機已交付。033／030／082未知預留70未動，未新增付費。

- 2026-10-09 加速續製：依站主「做太久了」續做不受六鏡變更影響的原鏡，沒有縮短全片或默採變更。版本化本機操作批額 3,200→4,000，原 A/B 期與 take cap 不變；備妥 003／030／031／033／034／038／040 原案。003、031 首格各實扣24點，官方無水印下載完成；003內容候選，031仍有燕迴起點約高於最底階2–3階的限制。003原定H3四秒已送出、實扣48，任務564856595289645061，最後查見生成中，尚未下載。030原請求未查得任務與扣点，保留24；033建立時瀏覽器操作逾時，AX／截圖／重整／新分頁恢復均失敗，另保留24而不重送；連同舊082的22，共未知70。A期實扣3,690＋預留70＝3,760，最後可讀餘額58,310。原始操作、官方下載及短QA在外部 `finish-episode/throughput-resume-20261009/`；已請站主恢復IAB。現有已下載動態母鏡仍35／420、錄音候選597／597，003未下載不能加進完成數；未追加Google費用、購點、續訂或套用六鏡變更。

- 2026-10-09 收尾讀回追加：發現進度 JSON 的頂層 counts 仍直接引用上輪 timeline，主控先重新 who-is-on-it 確認 handoff 無 active scope、唯一相關 PR #1388 為本隊，重新 claim；`--force` 只略過同隊未結相依。將舊 timeline 數字另標 historical，當前統計改由 source／逐 take 收據／配音讀回計算，保留舊快照。另只補驗未有完整影音解碼的 11 支：全部 exit0、stderr 空、video/audio 都完整解碼且來源 SHA 未變；已有證據的 25 支未重跑，合計 36／36 有完整影音解碼證據，所有視覺 HOLD 與接受限制不變。外部 index SHA `3e2201dc53f2d6bc55144b9d7f41657c600c8f141b3ac6b7a5a14b0b60bc580e`。六鏡變更只凍結其改稿分支；a02-s003 原分鏡仍有四張 SHA 相符的備料可續製，尚未生成首格。3,200 點是本機操作批次額度，非新增站主總上限；下一次付費前仍須新 lease、版本化操作額度及即時餘額證據，不得直接繞過舊 guard。

- 2026-10-09 本輪最新收尾：597／597 句已有候選錄音及本機辨識資料（269 舊網頁句＋328 後臺句），後臺原音／48k 全解碼；實聽、表演、口型、整集對白剪接與混音尚未通過。API 已返回音檔估值 US$0.2161915＋舊 a7mv 未知預留 US$0.147658＝US$0.3638495，仍共用站主批准的 US$3，不是供應商帳單。Hailuo 已下載 36 支影片、覆蓋 35／420 動態母鏡，另外 385 尚未取得影片；35 也包含 HOLD／有限候選，不當成可用成片。A 期實扣 3,594＋082 未知保留 22＝3,616 點，實見餘額 58,406，沒有重送082或購點。六鏡變更稿已備並在瀏覽器展示（014／026／028中景、016右手插鏡、019原MCU有限第三版、029保留near-touch加末格），最多新增466點仍含在原26,980.8點上限；單次提問尚待站主回答，未套用source／lock或執行該批。071／074等既有HOLD、原生關卡與其餘缺料全部保留。最新完整收據見 [EP1 production progress](../../docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/EP1-production-progress-20261009.md)。
- 本輪實測：199 項 docs-video 測試通過，1692 票格式驗證通過（只有他票既有 stale warnings）。新版試聽頁位於127.0.0.1:8779，唯讀精確列408個交付檔；422次HTTP驗證及兩頁SHA、Range／拒絕規則通過。瀏覽器實見597句／344組，a7mv新take可播至1.84秒結束且error=null；六鏡審閱頁五張現況圖全載入，均明示失敗現況而非新修正版。這不等於聲音已聽驗。已知付費job均下載，離線ASR與抽樣程序均結束；production lease 正常release/exit0，之後核對LEASE、STOP及原PID都不存在。唯讀審閱服務保留，沒有背景付費生成；DoD仍未齊，收尾release供續作，草稿PR不合併／部署／發布。

- 2026-10-09 中文配音授權更新：站主指定既有 Google Smart IDE 金鑰與後臺影片工具權杖，並明確答覆「上限 US$3，完成中文配音（建議）」。本集中文配音及必要重錄共用單一累計 US$3 上限；這項授權取代下列歷史 API 0 限制，未擴及購點、續訂或其他 API 用途。既有權杖及後臺金鑰可用，沒有新建憑證或改後臺設定；已保留原 269 句，另完成 328 句後臺錄音，候選涵蓋原文 597／597 句；逐句盲辨識與聽驗另追蹤，沒有把錄音取得算成正式音軌採用。來源、每句請求、原音、48k 標準版與費用估值逐一綁定，供應商帳單實扣尚未核實；純本機 journal rename 故障只由已完整返回且 SHA 相符的音檔恢复，不重送付費 POST。詳見 [Google API 採用紀錄](../../docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/google-api-adoption-20261009.md)。082 未知結果仍單獨凍結與預留 22 點；獨立海螺鏡頭按原 A 期額度續做。中文配音取得、ASR 診斷、實聽、音軌剪接與正式採用分開追蹤，整集尚未完成。

- 2026-10-09 前輪驗證與交接（歷史紀錄）：199 項 docs-video 測試全過，範圍 diff 無空白錯誤；未重跑全部 tools、未合併／部署／發布。所有已知付費影片下載後，製作 lease 正常 release／exit 0，再查 LEASE 與 STOP 均不存在；082 unknown、22 點預留、Google R14 額度限制和未完鏡／音軌仍保留，不宣稱背景持續生成。071／074 首格修復提案已備且未送出；053／062 官方下載版另有逐格時間對應與抽樣浮水印覆核，原有動作及構圖限制未撤銷。077／078 已有獨立全格 QA，075 明列主控覆核；實速、聽驗、口型、連戲及整集接受仍待辦。本機試聽頁保留供審閱，本票仍未達 DoD，收尾釋出供後續續做。

- 2026-10-09 第一集續製歷史快照（API 授權與候選數量已由上方新紀錄及進度檔取代）：站主要求「直接到做完第一集」，仍以完整 459 張卡／420 個動態母鏡／597 句原對白為範圍，未將缺鏡改成靜圖或跳接。已保存 23 支生成片、覆蓋 22 個動態母鏡，還缺 398 個；其中仍含待覆核或局部 hold，不等於 22 鏡均正式採用。第 076 鏡已從海螺原任務下載，沒有重送。配音用 Google 網頁無 API key 路線保存 269／597 句、16 份原音；R14 顯示升級／額度限制，328 句尚缺，沒有付費 key、訂閱或自動重試。完整進度、來源 SHA、素材與 QA 收據見 [EP1 production progress](../../docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/EP1-production-progress-20261009.md)。
- 本輪收費與待查：A 期實扣共 2,179 點（含前次 475）；082 首格送出結果未知、另預留 22，合計已用與預留 2,201，不能把預留寫成實扣。帳戶重新載入實見 59,821 點；082 沒有新作品 ID／扣點回條，status=unknown 且禁止重送，現行執行守衛暫停新的付費送出。所有已知已收費影片都已下載；API 支出 0，沒有購點／續訂。R14 原送出及 082 unknown 收據保留於外部 finish-episode，後續先核對供應商原結果再恢復，不能靠空資產頁或餘額未變判成失敗。
- 聲畫交付仍為候選：051→052 官方母檔接 Google 對白 6.566667 秒、054 對白／環境／音效 4.458333 秒；未實聽、未驗口型、未有整集時間線或正式混音。16 份 48k headroom 候選自原音重採樣，完整 decode、等長與峰值檢查已過，原始 WAV／ASR／舊 48k 仍保留；ASR 不代替發音及演技聽驗。音樂、環境和音效分軌資料與授權收據已備，候選不等於配樂正式採用。本機試聽頁只綁 127.0.0.1:8775，逐句篩選／播放／媒體 Range 已驗，無對外發布。look／choice／series-store、正常 audio／storyboard 關卡與 owner 整集接受仍待辦，本票 DoD 不勾完成。
- 本輪新片缺陷待辦：071 獨立全格覆核在 f20 至末格持續裁冠，沒有可涵蓋完整原動作的乾淨全 take；074 在 f28–63 明確裁尖、f27/64–66 邊界，f67 後恢復，但中後段另外出現與原黑底銀蕨匣不一致的棕木徽飾盒並增加撫盒。兩片都 HOLD，正式收據綁 SHA；只另備未送出的首格修復提案，不靜默採用或重買。069 原階前站位差異、060 匣蓋細節連戲仍待核。075 已看完整 124 格全幅／動作 ROI 及首中末原尺寸抽格，披毯動作可作候選；它是根控覆核，未冒稱另一名獨立審片者或實速聽驗。所有這些限制及後續未完工作繼續追蹤於本票。

- 收工驗證：獨立覆核175格冠ROI全看，f16接頂／f20明確裁失，沒有可供053/059/065原時窗的足量完整冠區間；不改速或凍格救片。聲音15綁定、597句、459cue及133素材庫檔獨立核對一致。任務1692票及文件diff檢查過，只有其他票既有stale warnings。所有job下載後lease正常release/exit0，重驗LEASE及STOP均不存在；局部hold與後續待辦保存在本票，不是假称背景继续生成。本票DoD未齊，release回open，草稿PR不合併。

- 本輪收工追加：053影片已下載，7.291667秒／175格／24fps／2560×1440＋32kHz stereo AAC，完整decode、首格PSNR32.010299dB過；主控實看首末全幅與冠ROI0–15/160–174格，末段最高冠尖裁切，053及059/065暫hold、不重買同首格；062及069仍因右臉紫痕hold。所有15筆實扣均有下載，無unknown／open job；本輪175點、A累計475點不變。原片、靜音review副本、機械與獨立逐格QA留外部qa-a02-s053-video-t1；技術通過不等於動畫採用。

- 2026-10-09 續製：claim前重新who-is-on-it，handoff無active重疊、唯一PR#1388同隊；`--force`只略過同隊未結相依。本輪將三片剪成10.75秒（4段EDL、無變速／重複格、decode過），站主在採用節奏並續A期問題答「A 我儲值了」，已記採用；帳戶實見26,700→61,700，自行加35,000點，美元未知、非代理購點。036／038首格懸停敘述同步到外部continuation副本及獨立lock，597句及原v4/正常lock未動。已生053/062各2版首格共91點，053冠尖完整但留白極小，由root有條件選用、獨立headroom hold仍在；053七秒H3/2K片實扣84點生成中。062右臉殘留小紫痕，已停止此鏡及069依賴，沒有第三張圖或影片；053下載後須逐格查冠與動作，再裁定059/065可否切用。A期累計475點、餘額61,525、API0。最新結果與收工狀態見[續製紀錄](../../docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/episode-continuation-20261009.md)。
- 聲音續製待辦：站主明確Google配音後置且「好 另外準備」，外部audio-track-decision.json/.md綁定原話與來源；597句/9聲音、13音樂brief與逐鏡效果配置已備，官方Kenney CC0 130OGG已下載並全decode，9候選48kHz試聽已提供但未聽審採用；無真正配樂或M&E完成。後续須處理062局部除痕方案（不自動第三次整圖重買）、剩餘A/B逐鏡製作、Google逐語錄音/嘴型/真實時間線、正式匯入與look/audio/storyboard，不把分軌規格或原生AAC當完工。

- 2026-10-09 瀏覽器試拍：站主指定 Codex IAB 並登入，沿已採用316.8點pilot額度完成7次逐鏡圖像（156點）與3支H3四秒片（144點），合計實扣300點，帳戶27000→26700；無購點／續訂／API／TTS。s036兩版接觸末格都因冠尖與指段重疊歧義退回，未送接觸版影片。站主明確核准「採用懸停方案，繼續製作」，只在外部副本改s036 motion／end_frame.prompt、建立獨立native lock，原v4／正常lock未改。詳見[本輪製作紀錄](../../docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/hailuo-browser-pilot-20261009.md)。正式look/audio/storyboard、變更接回及片段匯入仍待辦；s035結尾手落身側接s036懸掌存在抬手跳接，3秒／2秒估剪也需改用實際動作收勢，需在放量前解決，不能把本輪下載／decode／抽格當owner接受。本輪claim前scope無其他active、唯一PR#1388屬同隊；--force僅略過同隊未結相依，不接管production原持有人。

- 2026-10-09 正式採用：站主明確回覆「採用素材與 v4，按此點數上限鎖定 plan」。[採用紀錄](../../docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/adoption-decision-20261009.md)／JSON逐一綁定146素材、既有限制、v4、兩期逐鏡預算與正常plan鎖。本期含預留26,980.8點、pilot316.8包含在內，第二期21,753.6須有實際額度，不購點／續訂、API支出授權0。原生write/check exit0且changed=false，455鏡 Hailuo Max H3/2K/assist off，lock SHA `6af3dafa4f9edc0a03270800a9d3fd44c6f487a3c015627fda4a4205f385d0c5`。ready exit1、2過429待製作，look依決定保留待判圖。
- 本輪最新9張基底（沈全身v3）已接入正常runtime，27次dry-run/import/exact-rerun全exit0，0fetch／0paid；manifest SHA `cf37aa3541380f13b864d3c01560e533fc176e7c5d85f472560408e85f7406b6`。正式來源與素材SHA重驗；沒有choice／judge／series-store或其他關卡核准。Hailuo空白表單核對Max27000點、H3 2K 4秒48點；Mokaair唯讀狀態drama=false及API單集200，未改設定。兩個剩餘DoD仍涵蓋真實判圖／參照送入／原持有人接線，因此本票保留open並release，不把plan完成當整條產線完成。

- 2026-10-09 最後整合完成：新 [asset-manifest](../../docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/asset-manifest.json) 核實 146 unique latest＝9 concepts＋27 portraits＋82 new references＋28 scenes/props，另 9 front reuse＝91 reference uses；29 份文件 hash 綁定含 portable gallery／fan／mouth reviews。455 鏡 mapping 最新 SHA 全過；193 鏡的扇分派都含 construction-details-v3＋personal-prop-states-v3，concept-v5/right-profile-v3/left-three-quarter-v3 僅身份服裝，沒有宣稱全圖扇拓撲一致。9 舊匯入逐筆保留 historical v3 與像素是否仍同新基底；沈 full-body-v3 未匯入／核准。build-manifest、其 --check、mapping --check、tasks check（1692票）與 scoped diff --check 全 exit0；只有其他票的 stale warnings。未 commit/push，release 交主控；source_commit 記當次工作基線，不因之後 commit 自動重建迴圈，正式採用 DoD 保留未勾。

- 2026-10-09 主控再分工 codex-ou-final-handoff 整合本票 `build-manifest.mjs`／README 與新收據：再次 who-is-on-it 查無 active scope、唯一 PR #1388 是同隊；claim `--force` 只略過同隊修圖／場景候選的未結相依。待主控最後修圖收據凍結後，依序重建 455 鏡 mapping 與 146 unique manifest，再 check/release；不改 production，不填 P7／owner／paid readiness，舊 9 筆匯入維持 v3 歷史。

- 2026-10-09 補交 [finalization](../../docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/finalization-20261009.md) 與 455 鏡 JSON／離線 builder。消費新 finalized 畫像／動畫參照收據；57 logical keys 的候選 hash、12 正典來源、27 原生 PNG header 核實，保留 18 張 native_below_target，未放大。6 個棋局狀態逐坐標與場景決定相等；冷場全部使用 clean master-v4＋狀態 spec，舊 cold-v* 不送模型。規劃 reference 並非已送模型；全部 final binding／owner acceptance／runtime 仍未寫。舊 9 人 staging 維持 v3／沈 full v1 歷史紀錄。本次只新增收尾檔，不改 README/build-manifest/asset-manifest；release 交主控整合，正式採用 DoD 不冒填。

- 2026-10-09 本輪收尾：由主控分工 codex-ou-final-handoff 補 `handoff/finalization-20261009.md/.json` 及離線重建／驗證器，不改既有 README、build-manifest、asset-manifest、production 或 approval。who-is-on-it 再查 handoff 無其他 active claim，唯一相關 PR #1388 即本團隊目前分支；`--force` 僅略過同團隊動畫參照／場景候選尚未結案的相依，不接管其他持有人，也不表示個別候選採用。完成後交回主控整合新資產 SHA。

2026-10-09收尾：[交接包](../../docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/README.md)與 [asset-manifest](../../docs/videos/series-plans/ou-de-jianghu/visual-development/handoff/asset-manifest.json)已備妥。12來源SHA、139張唯一latest候選（9概念＋27畫像＋74新角色參照＋29場景道具）、9張正面沿用關係、16種shot_looks獨立hash、9張隔離pending匯入及16份交付來源文件SHA已核對。正常lookHash為9b3e6914dbc8d109，僅來自隔離工作提案，不冒稱涵蓋shot_looks或正常runtime。455鏡v3／v3.1、全長文字animatic觀看、兩期預算及a02-s035～s037連續小樣計畫可直接審。白扇母版、紙窗近景、棋盤、原生尺寸及23:23.533估時差異均明列。剩餘兩DoD保留：正式個別採用／judge與正常關卡、當鏡真實參照驗證，以及production／原試播票持有人交接；沒有paid動畫或假approval。

- 2026-10-08 續做：本票 scope 收窄為 handoff/，先完成可審閱的第一集交接包；production/README.md 的原持有人交接及正式 runtime 選用/付費小樣仍列待辦，不占用其 scope。who-is-on-it 對 handoff/ 查無 active claim 或其他 PR。依站主「好 續繼都完成」授權，使用 --force 僅略過同一分工中尚未結案的三張相依票，並非覆蓋別人持有者、預算或站主接受。

第8集持有人占production scope，不能強行claim／覆寫。本輪未改既有試播票depends_on；接線仍待辦，要改它時先將精確路徑加入scope並完成所有權交接。後續14人／16狀態按同流程分批，不阻塞第一集。

- 2026-10-08建票快照：當時依站主「先補齊任務、造型規格與畫像製作清單」新增待辦，尚未生成或核准媒體；後续交付見2026-10-09紀錄。沒有部署或發布。
