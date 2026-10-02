# T26 實際正文與視覺節奏獨立查核

查核時間：2026-10-02T10:33:36.016Z。查核者：`integrate_duration_audit`。

結論：**PASS_ACTUAL_BODY_AND_STATES_FINAL_PENDING**。本報告驗收目前原創 native SVG／SLIDES 主稿的實際正文與狀態節奏；成片、品牌片頭片尾、音量、編碼、字幕、最終核准及上架仍未驗收。沒有建立或修改任何核准紀錄，也沒有呼叫供應商。

## 本次資料綁定

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

## 成片仍待核對

本次查核時 `checks.json` 與 `final.mp4` 尚不存在。尚未判定成片通過，也尚未讀到可證明品牌拼接正確的 checks。正常 render 當時仍在執行。

- [ ] 讀取實際 `checks.json` 與 `final.mp4`，確認 checks.ok／problems、speech／visual／render 綁定。
- [ ] 依正常 `knowledgeDurationProblems`／`assembleItem` 檢查正文及成片各至少 14,400 個 30fps 影格。
- [ ] 若含 branding，確認實際 pin／hash／body_frames／body_sha256 與正文 source 綁定，並重核 presentation timeline／章節。
- [ ] 用 ffprobe 獨立量測實際 body／final 的 frame count、fps、duration、音訊格式與同步；核對 loudness／PSNR 等正常 assemble 結果。
- [ ] 核對字幕、最終 QA 與最終審核；沒有上架授權或發布結論。

執行期間重新讀取每個主稿、timeline、cache、轉寫、WAV 及 SVG 的 SHA，沒有變動；正文判定不使用舊版 848.6 秒或任何候選稿估算。執行 command 為 Node 24.19.0 呼叫外部 `t26-runtime-independent.mjs`，exit 0。

完整逐 clip／逐 SVG 收據在 workspace 外：`C:/Users/x8120/.codex/visualizations/2026/10/01/01a0f5cd-1f4c-7f91-9af1-b02370fcce78/t26-runtime-independent-body.json`，SHA256 `bcd1817797c080d72d04a7f02d10a1dfc070a4ff1f1044a23aef16b098b40b00`。
