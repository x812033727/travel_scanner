# H03 視覺製作檢查

日期：2026-10-12。本紀錄區分實際看過的圖片、原生 judge 與製作採用；沒有用評分取代目視檢查。

## 第一輪開場小樣：退回

來源 SHA：`ce7418c4415cf9c8ce8c1afe9b024e562b4bc600307022ce4483d7ad5d87b590`；look `e77cf823ca0ea548`，pictures `37d66522cea4f234`。

- `hook-standing-trunk` take 1：独立研究代理看原图，發現男孩、動物、疑似長凳與整齊切面的倒木，與無人災後林地不符。原生 judge 9/10、未通過。
- 同鏡 take 2：主代理與研究代理均實看，樹根旁有明確嬰兒頭，主幹偏左且仍有長裸枝。原生 judge 9/10、未通過。
- 同鏡 take 3：主代理實看，主體變為低矮且切口平整的樹樁，沒有呈現高聳直立殘幹；左側小石塊亦有疑似臉部特徵。原生 judge 9.71/10 仍因主體錯誤未過，不因分數高而保留。
- `hook-kulik-puzzled` take 1／2：judge 都因 3D 外觀未通過。主代理實看 take 2，人物及布料的立體光影與背景材質偏 3D，與指定平面畫風不一致。
- 在五張圖片完成、沒有未結生成 job 時暫停原生小樣批次；STOP 是本製作程序所加，已核對內容後移除。原生命令此路徑 exit 0，但實際是停止且小樣未通過，不記為成功製作。第三個鏡頭當時尚未生成。

原始五張圖、manifest、media cache／jobs／ledger 與來源已完整保留在外部 `_audit/pilot-v1`。該輪圖片及判讀約 US$0.07；沒有將任何失敗圖標成 passed。

## 第二輪修正與驗證目標

當前來源 SHA：`6ff91a461a100b1e3adbaf0aed46e0c8ea6acab3aea88f98cfd886f24150b988`；look `a8294bb11b91c1ed`，pictures `88b5de1d0bddb6fa`。

失敗可能來自全域 style 無條件寫入 chibi characters，以及寫實模糊背景與平塗要求的衝突。這是根據圖片和文字的推論，不是供應商已證實的原因。

修正保留第 3 版的深藍、羊皮紙黃、灰綠及警示紅、粗線、平塗與可愛比例；把畫法明定為 2D、兩段式賽璐璐陰影，人物條件限定在鏡頭明確指定人時。兩個無人鏡頭改為有限自然物件的正向列舉，樹幹須高聳、自然斷裂而非鋸切；人物鏡改平面輪廓背景及小塊平塗亮部。

旁白文字、聲線、時間及 camera 未變，speech hash 仍是 `cba1834e2d1021c3`。第二輪 dry-run 通過，每張最多三次、三張估 US$0.04 至 US$0.12，仍在原本 US$80 上限內。

第二輪實際產出五張、累計媒體帳本 US$0.14。`hook-standing-trunk` take 2 的中央裸露殘幹較符合內容，但因粗線不足，judge 9.71 未過；take 3 雖然 judge 9.29 通過，主代理與獨立研究代理均實看發現主樹偏左、有長枝與綠葉，不採為開場。兩張及所有原始評分、收據保存在 `_audit/pilot-v2`。

另外兩張由主代理與研究代理實際看圖、對過旁白：

- `hook-kulik-puzzled`：平面卡通近景、抬頭表情與背後樹幹可承接空爆推理。judge 10/10。帽上無法辨認為真實標誌的裝飾不符合 plain cap，記為輕微偏差；這是泛化情境重建，不當成庫利克真實肖像。
- `hook-sky-above`：受損殘幹配大片天空，可承接「天上的東西怎麼壓倒地面的樹」。judge 9.29/10。樹幹偏左而非居中，保留此構圖偏差；後續檢查運鏡有沒有切掉樹頂。

## 第三輪：只修開場殘幹

2026-10-12T00:46:51Z，完成第二次提示詞修正：只把 `hook-standing-trunk` 明定為孤立死木、有限短斷枝、低處兩根自然倒木與底部遠景樹線，未改全域畫風或旁白。來源 SHA `e1b3e0eab0cb326601f4b3e33548de6a4a5519f5c9f81a307092d978f489587f`；look `a8294bb11b91c1ed`，pictures `843d78eb8ed076ef`，speech 保持 `cba1834e2d1021c3`。

原生 keyframes 明確沿用另外兩張既有圖及評分。本輪只新增一張，judge 9.29/10 通過；主代理實看為置中、無葉、帶斷枝的裸露殘幹，沒有多餘人臉，適合開場。部分斷面仍较平整，作概念重建可用，不當成現場證據。小樣階段累計媒體帳本 US$0.15；所有 paid job 已結束後才接續其餘 79 張。

這是插圖素材驗收，尚未代表全片分鏡、運鏡、合成或站主審片完成。

## 六月場景的季節修正

第一批新增圖中，研究代理逐張實看發現 `morning-trading-post`、`witness-back`、`tent-cloth` 均有厚積雪，驛站另外畫成月夜且缺少強光。三張雖然原生 judge 通過，仍因與 1908 年六月早晨不符退回。本批在四張新圖完成後以本程序 STOP 暫停；第四張 `fallen-corridor` 已生成但當時未判讀，留在原生快取，不重買。

原圖、manifest、媒體收據及來源備份到 `_audit/summer-v1` 後，三張提示明定晴朗夏日、綠草、裸土及白天天空；驛站明列高空強光，人物改夏季襯衫。相同的夏季場景描述也套到尚未生成的 `inhabited-camp` 與 `empty-stool`。其他提示、全域畫風、事實及音訊未改。

本次來源 SHA `c0b73538768d1eb80ea21d73e77687ae55325b57988b9f6a1c3612e8f2d65873`；pictures `0f84b6749f12fb50`；look、speech hash 保持不變。只在確認没有未結 job、上一個原生命令已停止、STOP 雜湊未變後，移除自己加入的暫停檔並恢復生成。修正圖仍需看實際畫面，未提前記為通過。

## 背景畫法回到選定的第 3 版

三個夏季場景及河岸陸續出現相同的背景畫法退件。獨立實圖覆核認為它們屬可辨認的 2D 描線、色塊與柔和 cel 陰影，背景細節較多；相較站主原選第 3 版，本製作過度限縮成 strictly flat／two-tone，與原定 soft cel shading 有落差。人物正常成人比例的問題另記，沒有藉背景說明掩蓋。

2026-10-12T00:59Z，在本程序 STOP 生效、當前 paid job 完成後，將整批八個已判讀場景、其全部 takes、來源與帳本備份到 `_audit/cel-background-v1`。只修 `look.style`：保留 2D、粗乾淨描線、指定人類才有大頭比例；背景改回原選定的柔和 cel 陰影與簡單色塊，navy night 的色名改 navy blue，以減少非預期的夜景提示。未更動評分題、門檻或原始 judge。

原生綁定因此重新生圖與判讀，不冒用舊 look 的核准。四張擴充小樣累計新生七張：庫利克近景、夏日居民背面、河岸空舟由主代理及研究代理實際看過，皆可用，居民已呈現明確大頭比例。另存 `_audit/cel-pilot-review.md/json`；look `635987294f938929`，來源 `96bee3bb363822e7d9448502bc16da3b1af26b9441e300f574c0528d17d36b61`。

驛站最後一張雖 judge 通過，實際有朝木屋延伸的彗星狀白光，不作定稿。備份至 `_audit/cel-pilot-v2` 後，把它改成木屋牆面受畫外強光照亮，天空與發光來源在取景外；避免圖像暗示已知飛行軌跡或直接撞屋。其他三張原生沿用，未重買。

目前來源 SHA `39699a32346ad389a58bfbbe771a63dc2ec00e1985b5a9c62e85ee0dfc6c17f0`；pictures `0cec58ec27b565e9`；look `635987294f938929`；speech 仍 `cba1834e2d1021c3`。全片插圖繼續生成與逐張實查；歷史小樣通過不代表本次重畫的同名圖片已驗收。

獨立保全稽核 `_audit/visual-lineage-audit.md/json` 已證明截至畫風修訂的四個版本差异均限於列明 style／prompt、139 段音訊與核准版一致、29 筆早期付費圖像皆能循 job→cache→SHA 找回保存原圖。後續新圖另行記錄，不把生產中 job 誤報為遺失。

## 正向物件提示與前二十景實查

來源 `39699a…` 的前二十景逐張實看後，十四景可用或有輕微構圖偏差；六景需修：開場殘幹有紅白異物、居民場景把強光畫成燈、庫利克循倒木場景像伐木工及雜亂工具、空泥地出現巨石與坑、斷枝特寫出現電線設施、庫利克觀察近景變成真人照片。原生 judge 通過不取代這些實際畫面判讀。

`marsh-route` 的原生最佳圖未通過 judge，但實圖是無人的棧道、濕泥與蘆葦；多片木板而非一片屬小偏差。保留原判讀與三張 takes，尚未冒記為無瑕疵通過。`round-marsh-pool` 實圖可用，本次不重畫。

2026-10-12T01:21:25.901Z，原生批次在本程序 STOP 下收工，27 張新增 takes、20 個場景；exit 0 在此只代表停止完成。確認 jobs 為空後，原件、manifest、帳本、來源與 STOP 備份至 `_audit/positive-prompts-v1`。STOP SHA `261e33a7bce7d31b3018d41baf203698ad88f3fd59dcd5fca43405241190da9d` 已原樣保存，再核對後移除。

獨立代理提出 66 案正向有限物件提示；只套用六景實際缺陷及 59 個尚未生成的場景，跳過已完成的沼池。這是提示詞修正，未改旁白、字卡、camera、時間軸、claims 或全域畫風；不改評分或核准。居民場景改成夏日居民仰望的反應近景，避免讓未知光源被畫成撞屋軌跡或燈具。提示提案 SHA `c8b00e92018e77d0e349f636488639269902d47cda94f50ba50d011f125dc35a`；套用收據 `_audit/positive-prompt-revision.json`。

新來源 SHA `09a6de779cd2975d0a13ca1329328c46b889c431a54b7e77a4d9116d84a75e15`；look 仍 `635987294f938929`，pictures `8467939604a71642`，speech 仍 `cba1834e2d1021c3`。原生續跑確認十四張圖與評分沿用，其餘逐張生成與實查；成片尚未完成。

## 全片八十二張實查與集中修正

`09a6de…` 全批完成 82 個場景、111 張新增 takes，原生命令因八個場景未過 judge 而 exit 1；圖像與判讀帳本累計 US$2.33。四頁聯絡表、manifest 與每個原始判讀保留，不把 exit 1 記成全部通過。

三名代理分別實看第 1–27、28–55、56–82 張，逐檔核對選定圖片 SHA。報告為外部 `_audit/visual-review-current-first27.md/json`、`visual-review-28-55.md/json`、`visual-review-56-82.md/json`。第一段的六項舊問題已解除；本輪新問題依實圖列出，與 native 分數分開記。

集中修正十七景：排水坑、空標本盤、受損樹、受壓發光前緣、下降天體、碎片群、俯看直立樹幹、折斷木刺、碎片散布、斜向天體、2013 日間火球、玻璃裂痕、計數框、四倍面積、湖景異物及兩種沉積泥芯。修案在 `_audit/material-fixes-approved.json`，SHA `b0c6f7647bc0c99331f65a3f8d5c240ad15f4b62ccc2b5a10cc8762456e0f334`；未另造數字或事實。

初始中段覆核將 `incoming-small-body` 判為風格需修。主代理另實看原圖 SHA `ba5b24985e85c6512c224cc73f3fd6cea2be6e3051fdcfcad0be12a533d9cf0d`，確認石體仍在高空，主要問題是電影感光影；決定與普通石頭、湖盆模型、微粒等純風格偏差一樣，保留原生失敗意見供成片審看，不再為此重買。這項採用決策不覆寫独立覆核的原始分類，也未把 judge 改成通過。棧道僅板數與構圖偏差，同樣保留原評語。

2026-10-12T02:29:54Z，確認前批程序結束、jobs 為空及沒有 STOP 後，全部來源、圖片、media 帳目與三份覆核報告備份至 `_audit/material-fixes-v1`。只套用上述十七個 prompt；來源 SHA `a32373b5b8f791bb053d04eed102d917b670037d4bab468aa5b8a410be8f38ac`，pictures `f7abfe2c72ada894`，look 與 speech 不變。原生續跑確認 65／82 個已畫場景沿用。新圖仍需實查，尚未送分鏡或合成成片。

## 十七景修後覆核與最後三圖／一字卡

集中修圖新增 24 張 takes，原生因五張既定保留候選仍未過 judge 而 exit 1；媒體帳本累計 US$2.65。前六修圖實看解除原問題；中段木幹、自然折斷、玻璃裂痕可用，斜向天體由主代理實看後保留小眼般斑點備註，獨立代理原意見未被覆寫。湖岸异物與兩種泥芯也已修好。報告為 `_audit/material-recheck-early.md/json`、`middle.md/json`、`late.md/json`。

仍需修正：碎片散布出現五雙完整眼睛、2013 日間火球仍有星空、計数框仍像擺錘架。這三個 prompt 再作一次窄修。四倍面積图兩輪都沒畫準兩張紙的比例，改用既有 native `big` 字卡：標題「約 4 倍」，算式「8,000 km² ÷ 2,000 km² ≈ 4」，明確承接原句與 c19，未新增事實或旁白。錯誤紙張圖只保留在備份，不進成片。

2026-10-12T02:46:01Z，來源 SHA `27d8f51b6460578ae1ac0fe60653cd5a77a024910d2009b429dc667bb01e428e`，pictures `128a0fe78ded537f`，look 與 speech 不變；共 81 張插圖，插圖時間占比 60.6586%，cadenceProblems 為空。原件與時間軸保存在 `_audit/final-visual-fixes-v1`，修改收據 `_audit/final-visual-fixes-revision.json`。原生 `tts --refresh-evidence` 0 新請求、0 計費、139 段沿用，只刷新字卡模板證據；仍需渲染實看字卡。原生圖片续跑只新增最後三張，未重買其餘素材。

## 最終圖片覆核與保留項目

最後三張的實際內容問題已解除：碎片沒有眼睛，2013 火球改為日間白色尾跡，計數框已有水平串珠。
外部 `_audit/final-three-recheck.md/json` 保留逐張圖片 SHA 與小偏差，沒有把生成數量的小落差當成新事實。

原生 `keyframes --accept-best` 將以下五張列為保留，新增生成次數為零：

| 場景 | 實圖採用範圍與保留意見 |
| --- | --- |
| `marsh-route` | 無人棧道、濕泥與蘆葦可用；木板片數及構圖不同於提示。其他 take 的人影不冒算到這張選用圖。 |
| `incoming-small-body` | 高空石體可辨認；電影式光影較強。独立覆核的 `REPAIR_STYLE` 原判斷仍保存。 |
| `scattered-small-stone` | 普通未標名石頭，用來說明候選物證；微距照片感較強。 |
| `lake-basin-model` | 泛指湖盆的模型，不視為已證實撞擊坑；模型質感及額外筆具為小偏差。 |
| `microscopic-candidate` | 泛指候選微粒，沒有標成確定隕石；顯微照片感較強。 |

上述圖片的 selected file、SHA、judge、takes 與接受前完全相同。原生只變更接受相關欄位，
包括 `needs_review`、`accepted_with_problems`、`fixes` 與生成記錄時間；未改原始評分。
接受前備份 `_audit/accept-best-before.json`；獨立保全與覆蓋報告 `_audit/current-visual-coverage.md/json`。
81／81 張都有相同檔案 SHA 的實看紀錄，missing、stale、實檔雜湊不符皆為零。
這份覆蓋不等於全圖無異議：`oblique-approach` 的獨立 HOLD 及 root PASS_WITH_NOTE 並存，
`incoming-small-body` 的風格異議也保留，交成片關卡判斷。

最終圖片 manifest SHA `3557df3d544adaaeb4f8ad5a073d23d4c60ace5ea8f909ab1c1ffff95ce44af8`。
分鏡 review `da0651b4-5904-4232-81ec-d71928e3e551` pending 的原因是普通通過鏡頭仍帶評語，
不是最低分不足或圖像缺失；完整唯讀診斷見 `_audit/storyboard-pending-diagnosis.md/json`。
尚未記錄站主分鏡或成片核准。

## 最終畫面與縮圖覆核（2026-10-12）

34 個非 shot 場景共 56 個原生 PNG 狀態已逐張實看，實際 SHA 與 render manifest 全部吻合。
第一組 26 狀態 PASS_WITH_MINOR（報紙來源字覆蓋原圖下緣少量區域，但原件與來源可辨識），
第二組 30 狀態 PASS；沒有文字溢出、缺字或科學關係錯置。原生面積字卡正確顯示
「8,000 km² ÷ 2,000 km² ≈ 4」，照片標示 2024 年影像，不是 1908 年現場紀錄。

縮圖原檔 1280×720 與 320×180 審核副本都已實看：主字「坑在哪裡」與人物表情清楚，
右下沒有重要文字。副標及字標在小尺寸偏小，保留為 minor；原圖未修改。
外部證據：`_audit/render-review-first17.md/json`、`render-review-last17.md/json`、`thumbnail-review.md/json`。
靜態覆核不等同完整播放、聽音或站主核准。
