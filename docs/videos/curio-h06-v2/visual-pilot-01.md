# H06 v2｜開場三鏡圖像小樣與修正

日期：2026-10-14。首輪付費小樣只涵蓋 `hook-canal-rail`、`hook-canal-rail-beat-2`、`hook-hospital-door` 各一張；來源 `video.json` SHA-256 為 `fef8fac61b6a3623209b140ca083d925ec0c2c9683def439595633a56e3c2a7d`，`keyframes/manifest.json` SHA-256 為 `c09272c35f1414356c1423c530066132550ebde5f61a4d3fbfdf39574203df6f`（`look_hash=dd05e380962e92b7`、`pictures_hash=d1e5b654f454580e`）。原圖、裁切圖、聯絡表、來源稿、manifest、ledger 和 state 的**逐檔 SHA 相符副本**封存在外部工作目錄 `review/visual-pilot-20261014-first3/`；該目錄 `README.md` 列全套位元組雜湊與人工審查。

| 鏡頭 | 採用檔 SHA-256 | 自動 judge | 人工看原圖與裁切圖 | 結論 |
| --- | --- | --- | --- | --- |
| `hook-canal-rail` | `9a94365a460676eeaae9d0da9fd9324bee61df258ac65a5e314ebc21df1054ab` | 9.00、FAIL；style 0、details 7 | 像電影攝影的運河街景；匿名女子露出側臉輪廓，畫面可能被當作真實歷史影像。 | 退回；不可作開場或縮圖。 |
| `hook-canal-rail-beat-2` | `fd19ca5d2477b5e742cb7c17f55778ef4e04ef81a14f06367871d8efaeeff927` | 9.71、FAIL；style 0 | 手部皮膚、鏽蝕欄杆與背景景深均像照片，無法與平面插畫銜接。 | 退回。 |
| `hook-hospital-door` | `17e388e0807ee107220a11ad1a1e70e4a7a9ec496aba60ef94dfa9d69d6c33f9` | 10.00、PASS | 單一成年女子背影坐於病院長椅，臉不可辨；線條、色塊與既定色盤符合平面編輯插畫。 | 保留作候選，尚非成片核准。 |

外部 `media/ledger.json` 首輪 SHA-256 `582c8a4457717bf1be19665adaaf63a5d99c5817fd0beca270bbe06a5501e85e`：3 張 MiniMax `image-01` 圖像 US$0.0105、3 次 Gemini judge US$0.0300，合計 **US$0.0405**，0 筆保留額。首輪 manifest 的 `thumbnail_source` 仍指向已退回的第一張，不能當作可用縮圖；兩張運河鏡頭的 `needs_review=true`。judge 整體分數偏高仍因風格項為 0 而不合格，不以 9 分或 9.71 分偷渡。

來源只支持一九二〇年二月女子在柏林運河獲救，以及未報姓名、警方未查明身分。[CSUEB 博物館解說](https://www.csueastbay.edu/museum/pre-exhibit/dna/history-fraulein.html)也寫她從運河水中獲救，未提供她在救援前站在欄杆邊的姿勢或影像。欄杆接觸、衣著、街景與姿勢是情境示意，沒有可核的現場影像；保留片頭後的原生字卡與說明欄「AI 情境示意，非現場照片」揭露，且不能用寫實照片感代替揭露。第三鏡沒有畫誰先說出公主姓名，符合判決保留兩種說法的界線。

## 第二輪：運河全景一張重試

MiniMax `image-01` 不使用風格參考板。把平面編輯插畫放在提示開頭後，僅對 `hook-canal-rail` 再買一張；該輪來源 `video.json` SHA-256 `cf8dcf3f201c60aa0466472d929c2edaa8224c87dcecb9a76cdbbcf235bcf54c`、`pictures_hash=f870d8715220e30e`。產出裁切圖 SHA-256 `f7ca62fa0e45afefd19fcbd355e5a573a83b9ef9f820610595717b4bca26cf11`（原圖 `deec16f6f9479015c3a76cfa0286e27cce7fa6c42e754a59b0d287b1584369c6`）；judge **9.29 PASS**、details 7，也指出仍看得到女子側臉。人工查看原圖與裁切圖：平塗色盤與線條已接近平面插畫，但畫了女子在救援前站於欄杆邊，並露出側臉。c02 沒有證據支持這個姿態或可辨容貌，因此**退回，不作片頭或縮圖**。分數通過不是來源或人工審查通過。病院候選 `17e388e0807ee107220a11ad1a1e70e4a7a9ec496aba60ef94dfa9d69d6c33f9` 仍保留，未在本輪重買。

第二輪 `keyframes/manifest.json` SHA-256 `b151f65ed6ff8c0847b9a6c7dd14a8d6fc0456fb38e7ca99e9278eae2e619713`，累計 `media/ledger.json` SHA-256 `2c075f4dff0cb5780f969f6c085b8aede2895db4a639a1cef657a92ec9069774`；4 張圖、4 次 Gemini judge，共 **US$0.0540**、0 筆保留額，本輪增量 US$0.0135。原圖、裁切圖、聯絡表、來源稿、manifest、ledger、state 與未改的病院候選之**逐檔 SHA 相符副本**封存在外部工作目錄 `review/visual-pilot-20261014-canal-retry/`，該目錄 `README.md` 列八個檔案的 SHA 與人審理由。現行 manifest 的 `thumbnail_source` 仍指向退回的運河圖，不可作可用縮圖。

## 運河提示修正與下一輪有界小樣（節奏修訂前快照）

當輪 `video.json` **僅再改前兩鏡提示詞**：第一鏡畫無人的柏林運河空景，僅有簡化欄杆、河岸與水面；第二鏡畫無人的欄杆特寫，旁邊的空白紙塊明示為象徵缺失姓名的**圖像疊層**，不是現場物件、警方檔案或原始史料。兩鏡皆無臉、人物、手或救援姿勢，並要求平面色塊和描線。這是非寫實場景示意，不能反推確切事發地點或街景。病院候選和其提示、所有旁白 ID／文字／順序均未更動；`script.md` SHA-256 `87f3d96bd0022b57f98ba53f8a8b546c5a63ea1a794a3809e910308a193014b6`、當時站主已核音訊綁定的 `timeline.json` SHA-256 `500df86851e4891f6707882dc28a16bf43900179abe6924c6a06a566a5948747` 不變；節奏修訂後的新時間軸另見下節。

當輪 `video.json` SHA-256 `9a0c81de5dda856974db9779832b12f9e8b6a393a1140ea935bed8b445cec315`、`pictures_hash=046720f1333f63b4`、`narrative_hash=349cf912c147f530`；`lint` 為 0 errors／0 warnings，兩鏡 `keyframes --dry-run --takes 1` 通過，MiniMax `image-01` 1K 加 judge 預估兩張約 **US$0.027**（CLI 約 US$0.03）。**此版尚未付費生圖或 judge。** 先只驗第一鏡是否真為無人、無可辨地標、平面插畫；若通過，再驗第二鏡的留白是圖層且沒有假史料字、照片感，最後沿用病院候選。每鏡至多一 take，任何一鏡出現人臉、杜撰現場行為、假文件或攝影質感就停在小樣，不進 51 鏡批量。新生圖需由工具按請求鍵更新 manifest，不能把本輪舊圖冒稱新提示已過審。

**節奏修訂前的真實音訊時間軸檢查：**15,028 幀／30 fps＝500.933 秒；`shot` 畫面 7,853 幀／261.767 秒，占 **52.256%**，前兩鏡合計 293 幀／9.767 秒。保持 `template: shot` 與所有口播時，插圖占比及敘事 hash 不因提示修改而變。`cadenceProblems(video.json, timeline.json)` 當時另報兩個畫面狀態超過八秒：`grave-first-count` 第一狀態 **8.2 秒**，`end-outro` 單一狀態 **9.0 秒**；先前文件的 7.8 秒是合成前靜態估算，已被真實時間軸取代。`lint` 不會代替此項 QA。這兩處須在成片前另設有意義的畫面更新並重檢；片尾版型無 reveal 容量，若分景或改版型會變敘事 hash，須重跑獨立敘事關卡，不能沿用 11/11。**當輪畫面節奏未過關；修訂結果見下節。**

## 後續畫面節奏修訂（仍未付費重買運河圖）

第一墓加第四張來源可核的「9 具遺骸／其中 4 名隨行人員」資料卡，片尾同景改成檢體／判決雙欄、第二句才揭露判決欄；前兩張運河提示與病院候選皆未更動。現行 `video.json` SHA-256 `47ee9a64126003aa2076bbb12d12434f4bbaa71bc3f1ca53781245bd069c2f69`，圖像 `pictures_hash=046720f1333f63b4` 不變。正式 TTS 由 99 個快取請求重建時間軸，0 新合成、0 billable；104 句 WAV 和旁白 WAV SHA 全未變。新 `timeline.json` SHA-256 `a885d5871108adaeacf346ccefa8d30a15556dda9623b5fa9fc5d9cf792f8e84` 的真實節奏為 101 狀態、最長 8.0 秒、`cadenceProblems=[]`、插圖占 **52.256%**。五張局部渲染圖留在外部 `review/cadence-card-preview-20261014/`，版面檢查 0 問題並已人工看過。

改版型後 `narrative_hash=02a39e4e1fb460a7` 的獨立盲審及新時間軸音訊核准，已在後續輪次讀回通過；詳見 [verification-notes.md](verification-notes.md) 的完整新舊音訊與時間軸對照。下一輪運河小樣計畫仍只限無人空景與匿名留白卡各至多一 take；第一鏡的實圖與結果見下節。

## 第三輪：無人運河空景，一張實圖退回

在現行 `video.json` SHA-256 `47ee9a64126003aa2076bbb12d12434f4bbaa71bc3f1ca53781245bd069c2f69`、時間軸 SHA-256 `a885d5871108adaeacf346ccefa8d30a15556dda9623b5fa9fc5d9cf792f8e84` 下，只對 `hook-canal-rail` 執行 `keyframes --shot hook-canal-rail --takes 1`。前置 `lint --json` 為 0 errors／0 warnings；dry-run 顯示 MiniMax `image-01` 1K、無風格參考圖、一張圖加 judge 預估約 US$0.01，既有費用 US$0.054／單支上限 US$80；專案及上層沒有 `STOP`。實際生成一張、正常 judge 一次，沒有重買第二鏡或批量生成。請求鍵 `3eb3daf67f5a2208`，`look_hash=dd05e380962e92b7`，`pictures_hash=046720f1333f63b4`。

原圖 SHA-256 `20455ac9ede877126abc1b3433c99db3f786c19bd57de1ee657e1059712d317d`；裁去頂端約 8% 紙邊後供合成的圖 SHA-256 `c6ac3f47fcf6e8373a5d626f08e948020636ee0b3a352212d1c23bc14ec0d82b`。**人工已打開原圖與裁切圖：兩者都在近岸路燈旁畫出一名女子，也在遠岸畫了小人物；建築立面具體得像某處可辨認的運河現場。** 雖然平塗描線較前輪接近插畫，這些人物和細節違反明寫的「無人物、無可辨地標」，來源只支持女子曾從運河獲救，沒有支持救援前站在此處的畫面。因此人審 **FAIL**，不可用作片頭、縮圖或歷史現場的代替影像。

自動 judge 給 9.29／10、`passed=true`，但同一份判定的 `details=7` 及問題欄明寫「human figures appear on the bank and in the foreground → completely deserted empty canal scene with zero people」。此分數不推翻人審與來源限制。現行 `keyframes/manifest.json` SHA-256 `23cb0c66d086377196d4151b469e5ccff32469825e807466a41422c3aa4` 的 `thumbnail_source` 仍指這張退回圖，**不得當作可用縮圖或送分鏡核准**；`needs_review=false` 只是 judge 的機械欄位，不代表人工接受。`media/ledger.json` SHA-256 `a37d4021234a639076928943e76725587edea36b8684ab190136159469c1bb7e`：累計 5 張圖、5 次 judge、US$0.0675、0 保留額；本輪增量 US$0.0135。

原圖、裁切圖、聯絡表、來源稿、manifest、ledger、state 的逐檔 SHA 副本已留在外部 `review/visual-pilot-20261014-empty-canal-one-take/README.md`。這輪改的只有小樣媒體與該份紀錄；104 句旁白、逐句時間、分鏡提示與音訊核准檔皆未動。用現行時間軸重新量得 101 畫面狀態、最長 8.0 秒、`cadenceProblems=[]`，插圖占 52.2558%；第一鏡 155 幀、約 5.2 秒。**暫停第二鏡付費生圖與全量生圖，先換一條不會捏造現場人物的片頭視覺路線，再重新做有界小樣。**

## 第四輪：現行 2D 三色帶提示，一張小樣退回

站主後續只授權 H06 **一張** MiniMax 小樣。以現行 `video.json` SHA-256 `52e29bceaa443ce740ba0db5ff9eb64cca27613340828f813c56dcee00d2607a`、`look_hash=d57461da98a0ba9b`、`pictures_hash=09fd4baed7f1480e`，對 `hook-canal-rail` 送一次 `image-01` 1K 及一次 judge；請求鍵 `f2790fe93cdec0da`。正式旁白時間軸 SHA-256 仍是 `a885d5871108adaeacf346ccefa8d30a15556dda9623b5fa9fc5d9cf792f8e84`。

原圖 SHA-256 `57285728a07a103b06ed94da8dfcffa4fbe9e5c98d80b0c1702235d256f4b16a`，裁切圖 SHA-256 `3b50bc6fbcec7253873d02e44c774d96a3ad71814fa6493f6c42d2a5390e4188`。judge 的 overall 是 **9/10，但 `passed=false`、`subject=0`**：它判定畫面為層疊山湖而非三條水平紙帶的運河概念圖，且少了紅色點綴。人工看裁切圖後確認畫面像峽灣／山灣，底邊另有虛構小字。它不具備 Berlin 運河的場景可讀性，又違反「沒有假文字」的來源界線，故**退回，不得進片或作縮圖**；高總分不能覆蓋核心主體失敗。manifest 的該鏡 `needs_review=true`。

本輪現行 `keyframes/manifest.json` SHA-256 `a9b9a08abb9153b0487c3db1f67a8131cc08f957f94fe78f8195459060c614c0`，`thumbnail_source` 仍指上述退件裁切圖。外部 `media/ledger.json` SHA-256 `8bf039025dddd54081f12b23410318b8bb70112d02bb765a60c5a373612efd6e`：累計 6 張圖、6 次 judge、**US$0.0810**、0 保留額；本輪一圖一判增量 **US$0.0135**。新圖原檔、裁切圖、聯絡表、manifest、ledger、state 已連同逐檔 SHA 收據封存於外部 `review/pilot-single-20261014/`；`preflight.json` 記錄送出前的來源與費用估價，`postflight-sha256.json` 記錄送出後六檔的校驗結果。沒有重買第二鏡。

兩個開場運河提示已多輪無法穩定產出來源可接受的畫面；**停止這條路線的付費重試**。下一步只能先離線重設可確定呈現的運河／姓名空白視覺，再決定是否修改場景類型或補足插圖比例；精確的 50% 影格餘裕與關卡代價見 [離線視覺路線](offline-visual-route-20261014.md)。舊圖與新退件均保留追溯，但不能以 `--accept-best`、judge 分數或 manifest 的 `thumbnail_source` 冒充人工接受。

## 第五輪：圖卡後緊接的三鏡，各一張一判（2026-10-14）

站主另授權三個**不同** shot 各一張 MiniMax 小樣、一次 judge，禁止同鏡重抽或擴批。起跑前 `video.json` SHA-256 `499fcab1f69d8eb9e9e25d65f9f89eb37ccd686142637092b852676b2ba9b68a`、已核 `timeline.json` SHA-256 `829335243ac71490e3ba552ea18a2c1f949c47a06362aee3979cbf6005d170d2`，`status` 讀到旁白核准及敘事關卡通過。專案和上層 `STOP`、專案 `LEASE` 都不存在，帳本無保留額；三個 `--shot ID --takes 1 --dry-run` 均顯示 MiniMax `image-01` 1K、提示長度在預算內、單張費用顯示約 US$0.01，既有 US$0.081／每片 US$80 上限。生圖前的 manifest、ledger、approvals 和三份 dry-run 已封存在外部 `review/pilot-three-20261014T030325Z/`，`preflight.json` SHA-256 `7d5f5687bd19b47d37a1247817aa6b60a06c7806974172886c2c8dd670863ad5`。

三鏡**依序**送出；每鏡只新增一張圖和一次 judge。CLI 每次都回 exit 1，但原因是已知品質退件，而非請求／計費不明；每輪讀回帳本後才進下一個不同鏡頭。人審已開啟原圖；第三鏡另檢視裁切後的實際選用圖。人審與 judge 分別如下：

| shot／來源 | 一張圖與請求鍵 | judge | 人工目視決定 |
| --- | --- | --- | --- |
| `hook-hospital-door`／c03 | 原圖 SHA-256 `e06a57b337a41dc9920222b57268dbc3ed1e86001b9cdc8c58001d98ee0b41fe`；`ee80bff6113b4e37` | **9/10，FAIL**：照片感；女子成側身坐單椅，未依提示背向坐長椅。 | **FAIL**。像具體 1922 年病院室內照片，露側臉，超出 c03 對當年場景的可核細節；不可進片。檔名 `hook-hospital-door-1.jpg`，不要混淆舊 look 的 `-1-trim.jpg` 歷史候選。 |
| `hook-hospital-door-beat-2`／c03 | 原圖／選用圖 SHA-256 `24190e085237d6ac080804141649840d3e0074b9f23dfd1df7cae2d9be58e613`；`3bfa7ccc69b93919` | **10/10，PASS**。 | 單張的平面門口象徵圖可留作候選，沒有虛構人物、官方卷宗或假字；**整段 HOLD**，因前鏡失敗，而且工具標出兩相鄰鏡 dHash 距離 4、構圖近似。judge PASS 不等於連續分鏡核准。 |
| `hook-three-answers`／c05、c06、c07 | 原圖 SHA-256 `f5e968381d581ded7edf9ddc4205d6f4c61b7376e330bced8c371035bc285b4e`，8% 紙邊裁切選用圖 `57a7ebcab23b013059ed18de9715585a08284087073effdd7c638af47a2617cd`；`3f10a5611a7328f0` | **9.71/10，FAIL**：缺指定的一小處紅色點綴。 | **HOLD**。抽象法院門口可讀，沒有假徽記或文字；不能當 1970 年真法院外觀，且目前未過風格判定，不進分鏡。 |

聯絡表 `review/pilot-three-20261014T030325Z/contact-sheet-final.png` SHA-256 `0cc5636d60687683c174a6d761e3e18e00586448bedb43897b16773ff243a1f8`；一排三鏡可見第一張的照片感與其後兩張平面圖風格斷裂。每鏡原圖／實際選圖、逐輪 manifest／ledger、執行輸出、人審決定與 `postflight-summary.json` 均保留於同目錄，沒有覆寫第四輪退件副本，也沒有人工改 judge、manifest 接受欄或送 `storyboard-push`。

帳本由 **6 張圖／6 次 judge／US$0.0810** 精確增加為 **9 張／9 次／US$0.1215**，本輪 **3 張＋3 判，US$0.0405**，0 保留額。先前 manifest SHA-256 `a9b9a08abb9153b0487c3db1f67a8131cc08f957f94fe78f8195459060c614c0` 與 ledger `8bf039025dddd54081f12b23410318b8bb70112d02bb765a60c5a373612efd6e` 已封存；現行 manifest `fe4283e00e94973108923da4e2c670260a1ff8ac23be543ee018e3874e5cb066`、ledger `737fd1d6e30160f08d755a863f16c41a5f6d8c008275dc7e727600271e7c61d2`。現行 49 個 shot 中只有這三鏡有新圖，且兩鏡 judge FAIL；其餘 46 鏡仍缺圖。`thumbnail_source=null`，原先退件運河圖不能因此恢復為縮圖。

**本次三鏡連續小樣未過。** 目前 `shot` 剛好占 7,560／15,028 幀，只高於 50% 下限 46 幀；若把這批任一個較長 shot 再改原生圖卡，必須先重新設計可信插圖時窗並重新量正式節奏，不能直接靠換模板掩蓋退件。三張授權已用完，本輪不再付費重抽、擴批或送後台分鏡。

## 第六輪：混合修訂後兩鏡各一張一判（2026-10-14）

站主核准 [混合修訂設計](visual-recovery-design-20261014.md)：保留 `hook-hospital-door-beat-2` 原圖，只改 `hook-hospital-door` 與 `hook-three-answers` 的提示及第三鏡 camera。舊版、舊 manifest、舊帳本、退件圖及核准資料均先複製到外部 `review/pilot-revision-two-20261014T040020Z/`。現行 `video.json` SHA-256 `a41d5d784a4e7bfe189b8b2683a172656d84174bc1c2e247ff91f335c5f6f7d1`；`narrative_hash=a8b72a5524beace9`、`speech_hash=9ae95e3507d3809f` 未變。104 句、每個場景影格與總長 15,028 幀重新比對都相同；`timeline.json` SHA-256 `829335243ac71490e3ba552ea18a2c1f949c47a06362aee3979cbf6005d170d2` 仍是音訊核准所綁雜湊。`pictures_hash=1fa2c8f61603eff9`、`visual_hash=529d6a4176e2c008` 是新版畫面綁定。

前檢讀回專案／上層均無 `STOP`、專案無 `LEASE`，帳本 0 保留額及 0 待結算工作；`lint` 0 error，正式時間軸 `cadenceProblems=[]`；兩次單鏡 dry-run 均為 MiniMax `image-01` 1K、提示在字數預算內、單片 US$80 上限。正式請求**順序**執行，每鏡一張＋一次正常 judge，無重抽：

| shot／來源 | 新圖與 request key | 正常 judge | 人工目視／連續畫面 |
| --- | --- | --- | --- |
| `hook-hospital-door`／c03 | 原圖 SHA-256 `59a13f20743f94b2b9e2078f151d5131bd48a89cc91bd4db5e29f4bbce6d97fe`；選用裁切 `1961e0e4d6ca6ba7f3b5f438ad1422ba6b26db504e2997405d5d84f3900e686c`；`ceafb4245c4cf184` | **9.29/10，PASS**；details 7：右側有明令排除的長椅。 | **HOLD**。背影不可辨、畫面為平面示意，與下一張中央空門構圖有別；長椅具體細節違反已核提示，不能據此暗示真病院內景。需獨立複核，不因 judge PASS 自動收圖。 |
| `hook-hospital-door-beat-2`／c03 | **沒有新請求**；原圖／選用圖 SHA-256 `24190e085237d6ac080804141649840d3e0074b9f23dfd1df7cae2d9be58e613`；舊鍵 `3bfa7ccc69b93919` 原封未變。 | 第五輪既有 **10/10，PASS**。 | 仍只是一張可讀的空門候選；前後鏡與整段分鏡仍待獨立審查。 |
| `hook-three-answers`／c05–c07 | 原圖／選用圖 SHA-256 `03e528ed76253331102cd0748e970ea0324938d5a7269e1577fab0c17532d77b`；`b91b967731b2656f` | **9.29/10，PASS**；details 7：色塊顏色及位置與指定左上青綠、右下深色不符。 | **HOLD／待複核候選**。無人、假字、真法院或卷宗外觀；紅色只成左上局部弧線，與第二鏡紅色方塊不連貫，右側大色塊過於抽象且方位未按原設計。不能誤指法院確認她的另一身分，也不能以 judge PASS 代替整段人審。 |

聯絡表 `review/pilot-revision-two-20261014T040020Z/contact-sheet-final.png` SHA-256 `35745ae585878df42b0c47a42ef36fb97786ae1632adb3bd2ce857572b90c764`：斜向背影 → 中央空門 → 俯看色塊，三張造型可區分；第一張的長椅、第二與第三鏡紅色點綴斷裂，以及第三鏡右側過於抽象的大色塊仍在。外部 `postflight-summary.json` SHA-256 `956b669a063cf3c61d58f441094c176c483669f5512cc7ce6595de92ef2ecaa1` 保留每個快照的 SHA、正常 judge／第一輪人審分欄及逐筆付費紀錄；`independent-visual-review.md` SHA-256 `a679635f597b8c706e8c32bea4308828deb36e78e58347ad60a4850b74536362` 另存獨立目視，不覆寫原評分。新 manifest SHA-256 `d0620e0b9486628fd5f14002bb1b89391adcb2b844c64699843373503041e75d`、ledger SHA-256 `989e26821a8690d6965676b74933534aa9f8177664f011c0a00d8966f74efd8b`；帳本從 **9 張／9 判／US$0.1215** 到 **11 張／11 判／US$0.1485**，精確增量 **2 張＋2 判／US$0.0270**，保留額及未完成工作均為 0。

`status` 仍顯示旁白已核、storytelling panel 通過；全片 49 個 shot 只畫了這三張，**其餘 46 張缺圖**，storyboard 未核、影格未渲染、影片未組裝。`thumbnail_source=null`，退件運河圖不能再作縮圖。理論 `shot` 時間 7,560／15,028 幀，50.3061% 且只多 46 幀；成片未測。這兩張付費授權已用完，不在此輪擴批、手改接受狀態或送 `storyboard-push`。
