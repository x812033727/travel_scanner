# 當前67bb繁中完整節目M4A已交後台並完整讀回

當前1080p成片67bb的繁中完整節目M4A已追加至[Mokaair同片後台](https://mokaair.com/zh-TW/admin/videos?video=ai-slides-outline-review)。音檔17,283,566 bytes，SHA256 `7df65621fc219d971bf191f466d245b795570320378dce9fe70d3815e9f689ad`，音訊stream與container均629.605秒。來源為 `67bb7eef3955933514c726968d9b76cd6c141260972661526874fc935f25de3d`；保留第一章後5秒官方片頭及21秒片尾的完整節目音訊。舊c387的629.610秒M4A／report繼續保留為歷史角色。

本次只有一次AAC streamcopy，實際mux delta為0、changed bytes為空；最後M4A與保留的remux intermediate完整bytes相同，沒有實際metadata／timing修補。來源和輸出的29,511個封包payload SHA、PTS／DTS、duration、flags、side-data及stts／elst／stsz／mdhd時序均精確相符。兩條完整48kHz雙聲道f32le解碼管線皆exit0且error stderr空：241,745,920 bytes／30,218,240 sample frames，SHA `8340897c26016cdcc57d202ca879f2c7ab3d5c2c65dd9cd41728182ddf2512f2`相同。實量-14.1 LUFS、LRA4.2 LU、true peak -1.9 dBFS；僅量測，未新增或降低門檻。PCM frame count與stream／container秒數是不同量測，未用前者冒充節目時長。[實際manifest](program-audio-manifest.json)／[Root成分核對](root-component-verification.json)／[獨立成分審查](independent-component-review.json)。

實際producer六個child均exit0，Root觀察工具88f960／session11747→42ab90真正exit0，兩個來源project leases正常釋放；原E305／歷史W2096／當前C3502檔與held4由實producer前後fullhash保護。Root與peer核對保留的packet／child收據與新M4A；完整PCM由真正producer管線雜湊，沒有保存PCM buffer，也沒有由審查者再解碼。[真正completion](producer-completion.json)／[Root工具終態觀察](root-producer-tool-exit.json)。

118句當前WAV各完整hash一次，完整intended／發音稿／primary與second轉寫／clip／快取／timeline與原接受紀錄保持。a261現稿僅縮圖變更，並未冒稱它整份SHA等於舊296稿；當前旁白WAV SHA4a298與說故事審稿hash分開。沒有新TTS、ASR或完整人耳重聽；既有67bb主片QA11/11沿用、未重跑，舊false／stale敘事結果保留。[118句來源摘要](current118-proof-summary.json)／[獨立來源綁定](inherited-source-record-review.json)。

正常checked-only追加helper真正完成於2026-11-03T03:58:00.832Z：同一pending FINAL `af432542-47db-4649-9761-17c0f6ca2127` 47→48 refs，只新增角色 `evidence_zh_tw_program_m4a`。原47份參照及順序、整個payload／QA11／九語metadata／章節／summary、所有其他review／choices／設定／歷史均精確保留。helper的正常auth1／projectGET4／PUT5／POST1（201）／fullGET1皆有真收據，完整新M4A下載保存在工作區；大小／SHA／audio/mp4 MIME及bytes與本地音檔相同。Root和獨立peer重開同一份已保存的實際下載檔，沒有再發第二個網路GET；舊47個binary亦未重下。[交付完成](backend-completion.json)／[完整新M4A讀回](backend-full-new-M4A-readback.json)／[Root全project驗證](root-delivery-verification.json)／[獨立交付驗證](independent-delivery-review.json)。

後台helper不產生process-exit檔，真exit0由Root工具a98a8c／session62666→37e458另行觀察，沒有補造檔案。一次錯誤本機dispatch digest在admission前即被拒，0 auth／network、沒有once／run／lease；原失敗和stderr保留，更正後只有一個實際POST，沒有清除或重播已派送請求。[Root後台工具終態](root-backend-tool-exit.json)／[原拒絕紀錄](wrong-dispatch-pre-admission-rejection.json)。原生API無atomic CAS，以before／immediate-prePOST／after／after-binary四次完整project對比核對觀察到的結果。

只新增一個M4A後台附件，沒有另加TXT或manifest超過48上限，沒有壓縮／替換舊參照；小型證據只在本公開收據目錄。raw HTTP／POST body、private profile、auth／LEASE內容、完整packet stdout、PCM bytes及MP4／M4A本體不複製到公開repo。

八外語checked M4A與actual-dub CC仍各0/8，沒有server／final／language-batch核准，整集尚未done。global ASR other-host、未知供應商結果、各次失敗／retake／改寫上限均保持。Root已正常release／blocked；本輪test:docs-videos 241 pass／0 fail／0 skip，check:tasks 2298 files／273既有其他scope警告／本片0項，diff check通過。原始subprocess退出碼與日誌已保存並於環境重連後核對，沒有重跑測試；[本輪實際檢查](required-checks.json)。不合併、不部署、不上傳YouTube。
