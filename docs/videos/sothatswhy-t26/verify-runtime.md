# T26 實際正文、視覺節奏與成片獨立查核

正文初審時間：2026-10-02T10:33:36.016Z。成片獨立稽核完成：2026-10-02T12:15:16.797Z；品牌音訊接縫補測：2026-10-02T12:17:01.576Z。查核者：`integrate_duration_audit`。

結論：**PASS_ACTUAL_FINAL_MEDIA_AND_NORMAL_QA**。正文、成片實際解碼影格與時長、180 個狀態、目前素材綁定、正常字幕、11 項自動 QA 及既有成片核准均已獨立核對。PTS 確有下述小幅偏差，並非嚴格每格等距的 CFR；沒有以通過自動檢查宣稱完整人工播放、逐句聽審或 CC 播放驗收。本次沒有建立或修改任何核准紀錄、呼叫供應商或上傳／發布。

## 正文初審資料綁定（保留歷史收據）

| 資料 | 本次實際雜湊 |
| --- | --- |
| `video.json` SHA256 | `90975caf8b5f719d6f7f49fd0da4c80a8058cd376df74fc8db6242dd8b044f25` |
| 正常 `speechHash` | `ce1ab16b0fde5fad` |
| 正常 `visualHash` | `9e8853bd4d25fbd3` |
| `timeline.json` SHA256 | `e2baf37ca8c14e675cd250c8a5a4deb1cf05d17cb726ba38c89b4843f72c5e57` |
| `narration.wav` SHA256 | `66a09e48468adfa16cfcf660af70860d09417a6eb60536e4ff9bb19ad5d6adf3` |
| `audio/cache.json` SHA256 | `19784e3efe15f98d341a99596a2921026f423373ea0ff421ad36d7a4ec4d60a2` |
| `review/check.json` SHA256 | `ef5c8f076b3512101ea47aa73588c53358498466a9fbe01a9565dbafc4dfadb1` |
| `review/check-flags.json` SHA256 | `67f03af6a04b06bbb4f84374481054e2572062c2bfb81f03d050e73a2ec49189` |
| `vector-art/manifest.json` SHA256 | `c0043a639febae254d653de85ad3e8ee1d9a16620e11e157854ecf12898ca0ee` |

主稿為 169 景／180 句、`format=slides`、`category=explainer`。正常 `validateVideo` 與 `renderProblems` 均無問題。逐一實讀 157 張 SVG，檔案內容吻合 READY manifest；每個 entry 皆 ready，路徑與內容雜湊皆不重複。這驗證資產綁定，不代替逐圖幾何與視覺審稿。

上表 `c004…` 是正文初審時的圖稿 manifest。成片使用下節 `11cd…` 修圖後版本：兩張語義修正、155 張 unchanged；主稿、speech、timeline、WAV、cache 及轉寫均與正文初審完全相同。成片判定沒有沿用舊圖稿收據充當目前素材驗收。

## 實際聲音與正文

逐一解析主稿要求的 180 個 clip WAV，全部為正常 48,000 Hz／16-bit／mono PCM。每個 clip 的實際 sample count 與 timeline 相符；每句正常 `planRequests` 的 line key 或 legacy request key 都吻合 TTS cache。以實際 samples 呼叫正常 `buildTimeline` 重建，與現有 timeline（含 speech hash）逐欄位完全相同。再以正常 `buildNarration`／`encodeWav` 重建旁白，SHA256 與現有 `narration.wav` 完全相同。

| 實際項目 | 結果 | 判定 |
| --- | --- | --- |
| 純 clip 聲音合計 | **714.020000 秒** | ≥480 秒，PASS |
| 正文 | **26,701 個 30fps 影格／890.033333 秒** | 排除品牌片頭片尾後 ≥480 秒，PASS |
| 正文與 WAV 綁定 | 180／180 current；正常重建 exact | PASS |
| 音訊自動查核 | 180／180 current clip hashes，0 flags | PASS，非人工聽審 |

音訊結果以目前 script 重新套用正常 `matchKind` 與預設門檻，123 句 exact、37 句同音或允許的口語填充字、11 句由主要 Jev 判定通過、9 句由第二轉寫清除，合計 180 句。每筆轉寫綁定目前實際 WAV 雜湊與目前台詞；flags 的 speech hash 也為 `ce1ab16b0fde5fad`。

正常 `approvalState(audio)` 為 approved，綁定上述 timeline SHA256；本地 pull 紀錄時間為 2026-10-02T10:26:22.639Z，來源註記為後台 2026-10-02T10:25:39.017735Z 的設定自動核准。本查核只讀取既有紀錄。正常 outline gate 同樣為 approved。

## 實際視覺狀態與章節

以正常 `slideStates` 與 `cadenceSummary` 讀取實際 timeline，另以影格重新計算未四捨五入的 hold。

| 項目 | 實際結果 | 判定 |
| --- | --- | --- |
| 視覺狀態數 | 180 | 每句均有對應狀態 |
| 最長 hold | **7.666667 秒**（正常摘要顯示 7.7 秒） | ≤8 秒，PASS |
| 平均 hold | **4.944630 秒**（正常摘要顯示 4.9 秒） | ≤6 秒，PASS |
| 超過 8 秒狀態 | 0 | PASS |
| SVG 圖解正文占比 | **23,487／26,701 影格＝87.962998%** | ≥50%，PASS |
| 正常純 SLIDES pace check | 0 problems | PASS |

這是 native diagrams 的獨立 8 秒／6 秒／50% 驗證；沒有宣稱它走過 AI shot 的 keyframes／storyboard gate，也沒有把正常 `illustrationShare` 的 shot 計數改成圖解計數。

正常 `checkChapters` 無問題：六章、第一章始於 00:00，每章均超過十秒。以下為正文時間，最終加品牌片頭後須依正常 presentation timeline 重核。

| 章節 | 正文開始（正常整秒格式） | 實際章長（秒） |
| --- | --- | --- |
| 同一口飯，兩種動作 | 00:00 | 20.366667 |
| 日本飯碗怎麼拿 | 00:20 | 203.766667 |
| 韓國飯湯怎麼吃 | 03:44 | 200.133333 |
| 從座位看懂擺位 | 07:04 | 175.466667 |
| 三種器皿，三個問題 | 09:59 | 126.500000 |
| 陌生餐桌怎麼觀察 | 12:06 | 163.800000 |

鉤子句 `9xba`「日本常端飯碗，韓國通常留桌，為什麼？」從 0 秒開始，該句含正常尾停頓的狀態於 **5.7 秒**結束，具體問題已在前二十秒落下。整個開場章節為 **20.366667 秒**；不能把它寫成整章 ≤20 秒通過。

## 正文初審時的成片待辦（後續已核對）

正文初審時 `checks.json` 與 `final.mp4` 尚不存在，當時只判正文與狀態通過，正常 render 仍在執行。以下待辦於實際成片與正常 final review-pull 完成後才逐項核對。

- [x] 讀取實際 `checks.json` 與 `final.mp4`，確認 checks.ok／problems、speech／visual／render 綁定。
- [x] 依正常 `knowledgeDurationProblems`／`assembleItem` 檢查正文及成片各至少 14,400 個 30fps 影格。
- [x] 確認實際 branding pin／hash／body_frames／body_sha256 與正文 source 綁定，並重核 presentation timeline／章節。
- [x] 用 ffprobe 獨立完整解碼 body／final，量測 frame count、實際 PTS、duration 及音訊格式；核對正常 loudness／PSNR，另作波形抽樣對時。
- [x] 核對字幕、最終 QA 與目前最終審核；上傳／發布與完整人工播放另行區分。

執行期間重新讀取每個主稿、timeline、cache、轉寫、WAV 及 SVG 的 SHA，沒有變動；正文判定不使用舊版 848.6 秒或任何候選稿估算。執行 command 為 Node 24.19.0 呼叫外部 `t26-runtime-independent.mjs`，exit 0。

完整逐 clip／逐 SVG 收據在 workspace 外：`<home>/.codex/visualizations/2026/10/01/01a0f5cd-1f4c-7f91-9af1-b02370fcce78/t26-runtime-independent-body.json`，SHA256 `bcd1817797c080d72d04a7f02d10a1dfc070a4ff1f1044a23aef16b098b40b00`。

## 成片實測與目前版本

正常 final review-pull 完成後，執行 repo 外 `t26-final-independent.mjs --ready --art-manifest-sha256 11cd8be93dace7a2775e2b586294c111cb9ece036db0153033c30d27cd36b3a5`，Node 24.19.0，exit 0。helper SHA256 `466d2feb672f27c17081070bb9b68fc8944d05f612ff9d8123626e5cf0e410d3`。所有讀取的來源、180 clip WAV、cache／轉寫、157 SVG、180 rendered still、字幕、checks、QA、品牌及核准檔案在 audit 結束再次雜湊，snapshot unchanged。

| 目前成片綁定 | SHA256／紀錄 |
| --- | --- |
| `final.mp4` | `8aa8ad5b2fb7f89ecddf3a020d048e158bdc70195386f100c27e52cee9cc67b3` |
| 保留 `build/body.mp4` | `58dcc7961454be07c983bcc19e15e9e7c4e7a125757bf241ee2cc5af1fb144c2` |
| READY art manifest | `11cd8be93dace7a2775e2b586294c111cb9ece036db0153033c30d27cd36b3a5` |
| 品牌 package | `mokaair-brand-package-v2-cc`；hash `a27622022d8d9e2f56221a81a1d7443ab241c40a37a515925784511f0416dcdd` |
| 正常 final approval | approved；本地 pull `2026-10-02T12:03:59.925Z`，後台自動核准 `2026-10-02T11:59:39.749968Z`，綁上述 final SHA |

157 張目前 SVG 全部吻合 READY manifest，路徑與 SHA 唯一。與正文初審相比，恰好只有 `c5-s01-detail`／`c6-s12-detail` 改變，SHA 分別為 `c3d92b2b968e396edde125a70c837b91f27659fa8dce55a27b08e61298c5de69`／`0ee16da68dbf5abeab62dcff46c659c844da93d5d11966fdc911d806137ecef3`；其餘 155 張未變。180 個目前 normal renderPlan state keys 與實際 still 路徑相符，沒有使用舊 SVG 渲染快取。圖稿與實際成片的視覺抽樣審查範圍另見 `verify-visual.md`，本機械稽核沒有代替其看圖紀錄。

| 完整解碼／實測 | 正文 body | 成片 final |
| --- | ---: | ---: |
| video packets／decoded frames | **26,701／26,701** | **26,941／26,941** |
| 影格數 ÷30，名目 frame grid | 890.033333 秒 | 898.033333 秒 |
| 實際 video stream duration | **889.984831 秒** | **898.100000 秒** |
| 實際 audio／container duration | 890.100000 秒 | 898.100000 秒 |
| `r_frame_rate` | `30/1` | `30/1` |
| `avg_frame_rate` | `410127360/13670167` | `269410/8981` |
| 正常 `checkProbe` | 0 problems | 0 problems |

兩檔均 H.264 High、1920×1080、yuv420p、BT.709，AAC-LC／48kHz／stereo。正文及成片的實際影音時長與名目影格時長皆 ≥480 秒；純 clip 聲音仍為 714.020000 秒。品牌確為 intro 150 格＋body 26,701 格＋outro 90 格，retained body SHA 與 checks 記錄相符；正常 `knowledgeDurationProblems`、`assembleItem`、`checksCurrent` 及 `brandingCurrent` 全通過。正常 checks 實測 −14 LUFS／−0.9 dBFS，507 個抽樣影格吻合投影片；本次核對其 current receipt，沒有冒稱重新量測所有 PSNR／音量。

## 實際 PTS、波形與字幕界線

逐封包讀 PTS 而非把 frame number／30 當成實際時間：首 body frame 150 的 PTS 是 **5.000000 秒**。正文本身有 96 個場景接縫，單次比 1/30 秒短 0.326 或 0.651ms，累計 −48.503ms；final 原樣保留。最後 body frame 26,850 的 PTS 為 **894.951497 秒**，延展顯示 148.503ms，片尾首格 26,851 在 **895.100000 秒**。這是真實接縫時戳及末格 hold 偏差，不能稱為只有平均 fps 標籤差異。

額外 66.667ms 已出現在正常 `build/audio.m4a`，body mux 沿用其 890.100 秒容器時長。正常 branding concat 因此將片尾排在 895.100 秒，final 為 898.100 秒。最後一句 `er2m` 實際 clip 聲音於正文 **888.220 秒**結束，末格延展發生於後續靜音段。正常 `checkProbe` 對音訊與名目 frame grid 的容許範圍仍是 `-1/30` 至 `1/30+(3×1024)/48000`，上限 **97.333ms**；本次沒有改此 repo gate，也沒有將這個音訊容許值解釋為每格 PTS 都完全一致。

另作實際 PCM 波形抽樣：開頭 0.6 秒、中段 432.9 秒及最後一句 884.9 秒，每處比對兩秒波形。六組相關係數 0.999980–0.999999，量測解析度 0.167ms；narration→body 偏移為 0，body→final 精確 **+5 秒**。品牌原音另抽樣，intro→final 偏移 0，outro→final 為 **895.100 秒**，與實際片尾畫面起點相同。成片 AAC 封包 PTS 連續、沒有間隙；抽樣沒有發現旁白累積偏移或片尾影音錯位。這些是波形與時間戳實測，仍非完整人工聽審／播放驗收。

以實際 packet PTS 重算成片中的 180 個正文狀態：最長 **7.666015 秒**、平均 **4.945000 秒**、超過 8 秒為 **0**；SVG 圖解占 **87.963899%**，符合 8 秒／平均 6 秒／50% 要求。body 自身 PTS 狀態平均為 4.944360 秒、圖解 87.962342%。正文與最終實測均不使用舊 848.6 秒或預測時長。

正常 caption manifest 綁目前 speech 與 branding，180 個 zh-TW cues 的 SRT／VTT 與正常 `buildCues(presentationTimeline)` 完全一致，每段相對正文均 +5000ms；首 cue **5000ms**、末 cue **893620ms**，0 warnings，沒有手改對時。六章正常 `checkChapters` 通過，成片整秒章節起點為 00:00／00:25／03:49／07:09／10:04／12:11。第一個問題仍在正文前 5.7 秒落下，開場整章含片頭為 25.366667 秒。

正常 `review/qa.json` 的 11 個必需項目全部 ok，final SHA 相符；audio 與 final 的正常核准均為 approved/current。這是設定自動核准的既有紀錄，不宣稱站主已完整看過、聽過或在字幕播放器驗收。audit snapshot 沒有以 publish 核准取代上傳授權，也未執行任何上傳／發布。

## 可重核收據與原失敗保留

以下均位於 repo 外 `<home>/.codex/visualizations/2026/10/01/01a0f5cd-1f4c-7f91-9af1-b02370fcce78/`，保留原檔不覆写：

| 收據 | SHA256 |
| --- | --- |
| `t26-final-independent.json`，完整正式 audit exit 0 | `18d0f9f73e7acd8ef7d5ff44763eccb3085acf60882cbde85e13292fce288270` |
| `t26-pts-forensic.json`，完整 PTS／AAC 與原 strict 假設失敗 | `fe36365675c6c7ac2fdc33a93e4b15d330c84d27f181246b3a22dc5cdd20a102` |
| `t26-sync-readonly.json`，PCM 抽樣與全 180 PTS states | `ccff5bb73b7cedcb9dd4395a26a7de13cef368955ca710fd0000ef57cd58367d` |
| `t26-encoding-tail-readonly.json`，中間容器／末句實測 | `d7a37aa9483c7c4dd0e8abaabff850c65c3c96dbd3790975a6a25282315deda4` |
| `t26-bookend-audio-sync.json`，兩端品牌音訊波形抽樣 | `2434d16e47f25295b64dfac2f39c61ba9f00070da270e33e33e19137e34d9386` |

原預備 helper 的 `avg_frame_rate === '30/1'` 額外假設曾以 isolated 實際 probe 重現失敗：actual `'269410/8981'`、expected `'30/1'`；當時尚未執行完整 final audit。原錯誤與註記完整保留在 forensic receipt。取得實際 PTS／PCM 證據後，只修 repo 外 helper：保留正常 r_frame_rate／完整解碼影格數／正常 AAC bound，另檢查所有實際 PTS 單調、每個 state 的 hold 與占比、接縫及 hash 綁定，不改 repo gates，不將先前失敗抹成未發生。
