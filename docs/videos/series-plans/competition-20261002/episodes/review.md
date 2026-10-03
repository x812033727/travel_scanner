# 全劇優化及 E1／E2 製作前覆核

覆核日：2026-10-02。覆核者：`final_review`。這是來源、故事因果、製作文件、映射及錄音收據的檢查；不是母語聽校、口音核准、影片觀賞驗收或使用者本人確認。

錄音及 hash 依各節的 run 快照保留；最新狀態以文末「一次有界重錄後的覆核」及 [audio-check-summary.json](./audio-check-summary.json) 為準。

## 結論與範圍

- 全 40 集的故事大綱、章篇、連戲資料、production design 與 [最終優化表](../selection-and-final-polish.md) 40 列已覆核；本次指出的文字 P2 已修正，未留下已知的文字 P1／P2。這不代表 E3–40 已具備全部逐句錄音稿或逐鏡可執行稿。
- E1 全稿 33 句與 E2 全稿 34 句已逐句對映 editorial／voice runtime；兩集均可進行繁中錄音與實測剪輯。這個放行不包含動畫、混音或完整 CC 的驗收。
- E1 已有 33 個可讀 WAV，初次自動辨字收據有 6 個 flagged；後續仍有待查項目，不能宣稱聲音全部通過。詳見下方錄音快照及聲音預演補記。
- 本輪是前兩集繁中影片及可開關繁中 CC。整部繁中全片及 CC 必須由使用者本人確認後，才做日／韓／英；兩集、pilot、代理或自動檢查不能代替該確認。

原始 `source.mjs` 物件 SHA-256（`JSON.stringify(source)`）：`37328fa1c643e0edfcd1d138a158410653b36d6e02739ce7a9c555b26bc5bb9c`。本次沒有修改原始 source、章篇或 production design。

## 全劇因果與修改揭露

本次回讀了文件權利、證物持有、人物知情、婚紗／頭紗／銀方錶、兩次不同火災、錄音修復、舊委任及現世救援時序。沒有把 E3 停止新授權寫成舊委任已全部消失，也沒有把 E36 保存證物寫成已定罪、E39 起訴寫成已判刑。前世資訊仍只屬知棠；E30 不新增回憶閃回。母親、妹妹禮袋及錄音資訊依原集數揭露。

以下優化表修改由本覆核者依 root 授權直接完成，因此不能把這幾處寫成完全獨立於作者的驗收：

| 位置 | 原風險及修正 | 覆核分工 |
| --- | --- | --- |
| E33／E35 | 原剪法可能讓妹妹與兩工人看似站在可用東側出口空等。現明列尋人與抵固定點的路程、接近 18:20 抵點；E35 接同一段通話，回報此時新有阻礙後轉北側，不因先播 E34 外圍至 18:30 而等到 18:30 才出發。未新增倒落物成因。 | 本覆核者修改；root 已獨立回讀原 source 時窗並確認。 |
| E06 | 顧送來的是書面說明；現明列由本集既有發聲角色讀出必要詞，避免誤排顧的旁白。source 本集角色是知棠、周啟德、許聞。 | root 指出措辭風險；本覆核者核 source 後修改。 |
| 本輪工作與外語次序 | 改為前兩集繁中試製，完整繁中全片及 CC 由使用者本人確認後才啟動外語。 | 本覆核者依最新授權同步。 |

其他 E1／E2 稿件及 JSON 均由另一位作者製作，本覆核者只提出問題及檢查修正。

## E1 核對

[完整稿](../pilot/episode-01-screenplay.md) 的 33 句，與 [dialogue](./episode-01-dialogue.json)、[voice runtime](./episode-01-voice.video.json)、[edit plan](./episode-01-edit-plan.json) 已以本地斷言逐項檢查：

- 文字、speaker、stable line ID、runtime ID、鏡頭關聯均相等。33 句位於 32 個有聲 scene；42 個原始鏡頭與 10 個無聲鏡都留在 editorial 計畫，沒有用假台詞填滿無聲鏡。
- 角色與 named look 可解析；前世知棠穿褲裝，E1 現世知棠皆保留頭紗。妹妹只試圖交出仍封閉禮袋，知棠未接；母親、錄音内容、許聞未提早出場。
- 撕的是薄展示副本；含附件的未簽原件留桌側見證位置；拍照與取得另存完整副本的動作保留。退戒盒與 E23 未送出的男戒沒有混為一件。
- 前 11 句 TTS request body、request key、line key 與 pilot 全等；原 11 個 WAV 複製後也逐檔 byte-identical。新增 22 句有獨立錄音，沒有拿相似台詞冒充。
- S16 接 51 秒開場聲音剪輯；不空等至原 60 秒。153.5 秒只是整集 editorial 規劃，後半仍須依新錄音重新排時。
- S35→S34 與 S39→S38 已標為候選合鏡。只有實測對白合計能放進 8 秒來源素材、且畫面有有效動作時才合併；stable ID 仍保留。42 是參照鏡數，不是必須付費生成 42 支的要求。

E1 screenplay、pilot voice、opening timing report、opening measured edit 的 4 個來源 hash 已重算，與 E1 dialogue／edit plan 的 binding 相符。

## E2 核對

[完整稿](./episode-02-screenplay.md)、[editorial dialogue／shots](./episode-02-dialogue.json)、[voice runtime](./episode-02-voice.video.json)、[series](./episode-02-series.json) 已核對：

- 34 句的文字、speaker、emotion、stable／runtime ID 全對。runtime ID 按文件所載 SHA-256 算法重算皆相符，無 E1 ID 碰撞、無 `audio_ref`；34 個 TTS request 僅使用 Kore／Puck／Charon，本集沒有旁白句。
- 實際呼叫本地 `productionSetting(setting, design, profile)` 後比較，三名角色 appearance／voice／shot_looks 全等。Kore／Puck 設定與 E1 逐字相同；voice／series 的 episode 都是 2。
- 34 個有聲 scene 對應原動作、camera、look 及精簡 prompt；另 7 個無聲鏡完整留在 41 鏡 editorial。所有 planned 時窗連續且每鏡 ≤8 秒，合計 178 秒，尚非實測長度。
- 全集同一 2D 畫風及婚宴場景；知棠由首鏡起無頭紗、銀方錶仍留腕。沒有妹妹、禮袋、母親、許聞或新增發聲見證人。
- 承川親口念受託人與表決權是第一回報，規劃於 23.5 秒完成。完整原件含附件由既有無聲見證人封存、交保管收據並收入見證人保管提袋；知棠仍留自己的完整副本。取得收據規劃於 145.5 秒，來源 118 秒目標未冒充實测結果。
- 尾句仍是舅舅要求「先把相機都關掉」；沒有演出服從、刪除影像、沒收手機或先行曝光舅舅。

兩項 P2 已由 E2 作者修正，並已回讀確認：L014 改為「舅舅，表決權是我的。我得知道要交給誰。」；全部鏡頭移除與 E1 衝突的 3D 畫風及未建立的花牆／深藍桌前提。runtime prompt 繼承相同狀態及 E1 的 `anime-2d`，沒有換畫風。

## E1 錄音收據快照

本節只讀 repo 外媒體檔與記錄，沒有發出付費請求、重錄、改全域設定或做人耳聽校。

媒體位置：`/workspace/mokaair-work/competition-20261002/media/wedding-reckoning-e01-voice-zh-tw/`。

- `state.json` TTS run `2026-10-02T15:43:23.960Z`：33 requests、22 synthesized、277 billable characters、無 fallback。另 11 句重用 pilot WAV。277 是計費字元，並非已確認美元支出；此快照沒有第二次 TTS run。
- 實讀 33 個 WAV，乾聲總長 **94.63 秒**。`timeline.json` 的有聲場景時間軸是 **128.1333 秒**；它省略無聲動作鏡，不能稱為 E1 完整剪輯或影片長度。
- `state.json` check-audio run `2026-10-02T15:46:32.804Z`：33 checked、18 exact、4 alike、11 judged、6 flagged、0 unchecked；本次 transcribed 22、Jev calls 1。
- `review/check.json` 的 alike 包含 3 個 sound 與 1 個 filler；18 exact 以工具的文字正規化規則計算。11 judged 不等於 11 全通過。6 個 flagged 仍需解決，不得把 0 unchecked 寫成 0 flagged。

| 尚待辨明的 stable ID | runtime ID | 自動轉寫差異摘要 |
| --- | --- | --- |
| WR-E01-L016 | `7410ddec` | 「還怕」被辨為「害怕」 |
| WR-E01-L017 | `105882b7` | 「這一份」被辨為「這份」 |
| WR-E01-L019 | `824e2f7a` | 轉寫尾部多「啊」 |
| WR-E01-L022 | `aa839f9a` | 「姐」被辨為「這」 |
| WR-E01-L026 | `8704bfd6` | 轉寫妳／你且 Jev 低於接受門檻 |
| WR-E01-L032 | `3ec2e067` | 「這幾頁」被辨為「這集也」 |

以上差異是工具記錄，尚不能直接判定全部為實際錯唸；須依可追溯的後續聽校／覆核處理，再決定是否重錄。Jev 比較預期文字與轉写，不代表人耳已驗證台灣口音、情緒或角色一致性。後续若修正，保留原 receipt 並以新紀錄更新狀態。

E2 在本次映射檢查時尚未錄音。兩集動畫驗收皆為 **0 秒**；完整聲畫剪輯、混音及逐語 CC 尚待實製。文件中的 Lite／1080p 設定不證明執行後端已採用該設定，實際生成仍須查當次工作參數與回執。

## 兩集聲音預演實測補記

本補記在兩集聲音預演輸出後，獨立讀取原 WAV、master、角色 stems、SRT／VTT、`measured-edit.json`、`timing-report.json` 及 `original-shot-plan.json`；沒有只依賴 builder 自報的通過欄位。媒體根目錄為 `/workspace/mokaair-work/competition-20261002/media/`，兩集各在 `wedding-reckoning-e01-voice-zh-tw/editorial-zh-TW/` 與 `wedding-reckoning-e02-voice-zh-tw/editorial-zh-TW/`。

| 項目 | E1 | E2 |
| --- | --- | --- |
| 聲音預演實測長度 | 144.86 秒／6,953,280 samples | 159.05 秒／7,634,400 samples |
| 原錄音乾聲合計 | 94.63 秒／33 句 | 119.49 秒／34 句 |
| 聲音剪輯參照鏡數 | 40，原 42 鏡映射保留 | 41，原 41 鏡映射保留 |
| 無聲動作鏡保留 | 10 | 7 |
| 實測後正式動畫 | 0 秒 | 0 秒 |

獨立檢查結果：

- 67 句台詞依原稿順序各出現一次。master 中每段 PCM 與來源 WAV 在對應 sample 範圍 **byte-exact**，每個角色 stem 也完全一致；其餘空間為零。沒有裁掉語音、伸縮、複製或重排台詞，沒有混入其他聲音。
- 兩集全部 SRT／VTT 的 67 個 cue，文字與 speaker prefix 皆對應同一句原稿；起訖對應 sample placement，毫秒四捨五入誤差不超過 0.5 ms。這是聲音預演 CC，不是已與動畫畫面完成驗收的 CC。
- 83 個原始 shot ID 仍全部且按順序存在於映射；17 個無聲動作鏡沒有因 voice runtime 無該 scene 而遺失。無聲動作時間仍沿 planned 秒數，須在真實畫面出來後驗證。
- E1 前 51 秒 master PCM 與既有 pilot 完全相同。S35 併入 S34、S39 併入 S38 後各為 **7.26 秒**，可放入單支 8 秒素材。兩對保留 target 原 prompt、camera、主要動作、visible cast 及 look；知棠合入的回答明列畫外音，沒有把兩個原動作強行合成，也沒有新增她到承川單人鏡頭中。這是剪輯可行性核對，仍需真實畫面自然表演，不能停格填滿。
- 其他鏡頭的 prompt／motion／camera／character_looks 與已覆核來源一致；E1 頭紗、E2 無頭紗、文件持有與 E2 封存階段沒有被 builder 改寫。
- 兩集 dialogue、edit-plan、screenplay、builder 的 source binding 與檔案 hash 已重算相符；`original-shot-plan.json` 與實際輸入逐物件相等。timing report 所列每個 artifact 的 hash／bytes 均相符。

E2 第一回報所在 S06 在聲音預演中於 22.26 秒結束；接取收據 S33 於 133.71 秒結束，見證人收入保管提袋 S34 於 136.71 秒結束。這是聲音時間軸安排，不是已生成畫面證明。

錄音狀態也保留實況：E2 `state.json` 的 TTS run `2026-10-02T15:49:11.250Z` 為 34 synthesized、503 billable characters、無 fallback。`check-audio` run `2026-10-02T15:51:40.522Z` 為 34 checked、20 exact、6 alike、8 judged、4 flagged、0 unchecked；6 alike 含 5 sound、1 filler。4 個 flagged 為 `585129ad`、`e71ea610`、`c3ba746c`、`fccfbc0e`，自動轉寫有同音稱呼／妳你及口頭詞差異，未由本覆核者清除。

E1 後續 `check-audio` run `2026-10-02T15:53:05.880Z` 記錄 cleared 4、flagged 2，18 exact／4 alike／11 judged 不變；目前 `check-flags.json` 剩 `aa839f9a`（L022）及 `8704bfd6`（L026）。本報告仍保留初檢 6 項及原 run，沒有將新版數字冒稱人耳聽校通過。root 正另做獨立辨字覆核；本次尚未把該步寫成已完成。兩集 state 中各只有上述一次新 TTS run，未見重錄。

兩集總計 303.91 秒是**乾聲預演及動作留位**。沒有配樂、環境或情節音效，動畫仍為 **0 秒**。口音、角色表演、最終辨字、唇形、動作持續性和與畫面對時的 CC 均未在本補記中獲准。

| 實測媒體 | SHA-256 |
| --- | --- |
| E1 `master.wav` | `91fdf6b432d84376674897d4187c4c741adf2eacf1e6b82c3db4c5167eb72e28` |
| E1 `timing-report.json` | `eb6ec592a28a1f81aba7bb4fc3469f932c60fe7ea240dc1f92adb0b9df733063` |
| E1 `measured-edit.json` | `1e6b0c5f438a630af889253f2160f41f7f78d0e145a640753bcac3d2b2e77fbd` |
| E2 `master.wav` | `6f99752b179dc74dcb96d32826f2ea6198c1a1afdf5b9ad5c7da6cd2b527d894` |
| E2 `timing-report.json` | `050af8466aeabdab115273e82ebc0b6067a9db3d16e8c04f2e3be8a9e35d4368` |
| E2 `measured-edit.json` | `f3bf26329c8795f5bf4c033fb542703cead9da4fa5739235dffbbedde8fb37bf` |

## 審查版本指紋

以下為本次讀取的檔案 SHA-256；後續實錄與剪輯紀錄可追加，但如果改台詞、角色、鏡頭因果或來源 binding，須重新檢查相應部分。

| 檔案 | SHA-256 |
| --- | --- |
| `../selection-and-final-polish.md` | `8ee94b3d12f576b646717885e3e08dda58dea7299c2cf612e5eab306786525f0` |
| `../pilot/episode-01-screenplay.md` | `82352b248e66810bd217092b6284ea13c0ec688dbb410e6f791107e13781c429` |
| `episode-01-dialogue.json` | `855b0f7a0a336c32fb5a6ac73de5d48867bf77efb89649ad0575ba2f345a7af5` |
| `episode-01-voice.video.json` | `949f6c51dc944e3ef972b859822fb5d5d87d9938effa4c9e93fc8e0eae4b408c` |
| `episode-01-edit-plan.json` | `d0269e9e67196f88b33394b8a117e36ddbdd4927d638874b64b64c42a1c2afb3` |
| `episode-01-series.json` | `b7f880ac764ad07c4e0fe75b489a72a30cb61aec767e87cd056127973878972c` |
| `episode-02-screenplay.md` | `3e1d8461cd7013ea646dd517e1f7bc35b960e191f9ac005df039c112e1468bdd` |
| `episode-02-dialogue.json` | `6e0c9cc6f22c5e9b3b425ae03fecc6eb3db83878b41d44af3cdffb710e3b264b` |
| `episode-02-voice.video.json` | `58475bb8c46424777f5e7e5e8e720b653ac30dbab890bdf6f72bb60b9692ad43` |
| `episode-02-series.json` | `b275a799d87f01fb1343c19a49316b61f236f145b24bb8fd6020aa458616a4d2` |

## 一次有界重錄後的覆核

E1 只針對 WR-E01-L022／`aa839f9a` 的「姐。」做一次同文、同 Aoede 聲線重錄。原 WAV、cache、check、state 及原因收據保存在媒體目錄 `retakes/aa839f9a/take-01/`，沒有抹除初次結果。新 TTS run `2026-10-02T16:00:57.472Z` 為 1 synthesized、2 billable characters；兩集其餘台詞未重錄。

獨立覆核確認：

- archived cache 的 33 個 request cache key 與現有值完全相同；32 個其他 WAV 的完整 SHA-256 全部不變。只有 `aa839f9a` 改變，舊 take 0.40 秒、新 take 0.32 秒。
- 新 take 在 E1 master 的 samples **5,128,800–5,144,160**（106.85–107.17 秒）逐 byte 相等，角色 stem 同樣相符。把這一處換回 archived 舊 PCM 後，可以重建本報告先前的完整 master SHA-256 `91fdf6b432d84376674897d4187c4c741adf2eacf1e6b82c3db4c5167eb72e28`，證明其餘 PCM 未變。
- 前 51 秒依然與 pilot 完全相同。E1 乾聲總長更新為 **94.55 秒**；聲音預演仍是 **144.86 秒**，原鏡映射、40 個剪輯鏡與 10 個無聲動作不變。
- 兩集現有的 67 個 SRT／VTT cue 及每個角色 stem 已重新核對；L022 cue 更新為新 take 時窗。repo 的 `episode-01-*`、`episode-02-*` measured-edit、timing-report、SRT、VTT 與媒體目錄版本逐 byte 相同。這些 repo 檔是可追溯的聲音預演交接，尚非完整影片交付。

截至本次讀取，E1 最新 `check-audio` run `2026-10-02T16:01:26.817Z` 是 18 exact／4 alike／11 judged／4 cleared／**2 flagged**／0 unchecked；L022 的 Gemini 轉寫仍為「這」、Whisper 為「借」，L026 轉寫為棠棠／唐唐、妳／你的差異仍未清除。新 take 不等於已解決發音。

E2 最新 `check-audio` run `2026-10-02T15:59:46.415Z` 是 20 exact／6 alike／8 judged／2 cleared／**2 flagged**／0 unchecked。留下 L002／`585129ad`（原文「附件」，第二辨字轉為「復健」）及 L016／`fccfbc0e`（額外「啊」／「他」）。這些仍需人耳辨明；不得統稱成僅有妳／你而忽略附件一詞的差異。兩集都沒有為了清旗標而繼續無上限重錄，也沒有把 ASR 接受當作口音或表演核准。

[E1 validation](./episode-01-validation.json) 原先的 22 句未錄等欄位已明標為 **pre-synthesis 歷史快照**，保留原值，另追加 `current_section`；沒有改寫歷史為全部通過。[音訊檢查摘要](./audio-check-summary.json) 記錄當前 2＋2 flags、原字與兩個辨字結果、WAV／check／state／剪輯檔 hash 及重錄收據。

可由現有 TTS state 加總的計費字元為 **900**：pilot 118、E1 新 22 句 277、單次重錄 2、E2 503；共 67 句現有台詞、68 次含 pilot 的生成 take。這是字元紀錄，不是美元實支；完整美元費用及其他生成／辨字成本仍由總帳登錄，沒有因本地辨字而宣稱總成本為零。

| 最新 E1 媒體 | SHA-256 |
| --- | --- |
| 新 `aa839f9a.wav` | `50e5803f96ccd1d9bb62cff3b9bc426f3eb9fb04edebfdea0e2c2f65c1688b1e` |
| `master.wav` | `ea622b797df573509b791e180798e17595179fd95158fd6e0676d2c46a466515` |
| `timing-report.json` | `0d6445470b374a185b77490ad7cc297051a62c295a12479f84ddaf904bb9bbe6` |
| `measured-edit.json` | `34438e1c64cc6535a1ad1cbee685027801483f33783093c5038941f1d9917bb6` |

E2 媒體 hash 與前節相同。兩集合計仍為 303.91 秒聲音預演，**動畫 0 秒、所有音訊內容／台灣口音的人耳驗證仍未完成**。
