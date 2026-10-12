# H04 製作紀錄

2026-10-12，Asia/Taipei。承接站主「繼續」，製作已查核題庫的下一集，僅繁體中文。H03 已完成上傳包；本集沒有沿用 H03 的核准或媒體。

## 目前狀態

- 分支：`codex/curio-h04-production-20261012`，由當前 `origin/main` 的 `f7691d8cb` 建立。
- 任務：`2026-10-12-produce-curio-h04-dyatlov-traditional-chinese`，scope 僅本資料夾。
- 碰撞檢查：H04 沒有 active task 或 open PR；正式站 H04 GET 回 404，沒有既有製作要接手。
- 正式站頻道立場已讀回，`auto_pick_outline=true`。本次大綱套用 2、3、4、6、9。
- `brief.md` 三案已送審，站主選定 A；正式站與原生 consumer 均讀回本次雜湊的核准。
- 完整 A 案腳本已落地，獨立事實與聽眾審稿均 PASS、0 未解必修；最終 dry-run 通過，旁白正在合成，尚未生圖或完成成片。

## 製作界線

插圖投影片，`category: explainer`，Sulafat 旁白，系列同色盤與線條。匿名人物只用遠背影／剪影；不生成近代人物肖像，不呈現遺體或傷勢。長片10–11分鐘目標、正文及成片各至少8分鐘。繁中旁白、標題說明與可關閉字幕；其他語言不製作。

文件與論文事實另查原件，2022考察明確歸於作者報告。不將模型可行性稱當年經過已證實。原題卡的切口數、日期、溫度與在世檢察官支線已收窄。

## 2026-10-12 大綱送審收據

- 正式站已確認 `format=slides`、`category=explainer`；主工人未接手，本機接續。
- brief SHA-256：`32bf76ed25e862e3e7c9e0bf8d1d369a2f9ad625a270c5518ed0919592f32a63`。
- outline review：`d76bc11e-0d58-4983-b7d2-378d18e17bd2`，送審 `2026-10-12T04:53:24.919440Z`，狀態 `pending`，choice／decided_at 均 null。
- Jev：A 推薦機率 0.98、符合立場 0.91、有示範 0.37、建議 0.01。因 demo 低於 0.60，沒有自動核准。
- 原生 `review-push --gate outline` exit 0 僅代表送審成功；`review-pull` exit 3，明示仍等站主，不等於核准。
- `checkBrief`、`stanceProblems`、`outlineOptions` 原生檢查通過，3 選項。這是企劃檢查，完整腳本尚未完成，沒有宣稱影片 lint 已通過。
- 獨立歷史與聽眾審閱已整合；科學審閱要求不把 7.5–13.5 小時當獨立預測，送審前已刪精確範圍，保留「檢驗延遲數小時情境」。
- 已向站主送出 A／B／C 選項；繁中授權沿用，未再次詢問語言。沒有執行 TTS、生圖或合成。
- [歷史查核](research-history.md) 與 [科學查核](research-science.md) 已保存，企劃階段沒有未解 must-fix。科學報告明分官方索引正文已讀、直接 PDF 受阻、補充材料及完整推導未讀。正式稿不能把這次企劃審閱當成逐句通過。
- C 案的 `stats 延遲範圍` 是畫面類型標籤，製稿僅呈現「數小時／模型情境」，依本版示範節限制，不把精確區間放回字卡。
- 最後一次回讀為 `2026-10-12T04:56:56.492Z`，仍 pending、尚未選案。若站主選定後接續，先重新認領原任務，將選擇保存到同一 review，再 `review-pull`；保持本次 brief SHA。

這是既知的關卡適用性問題：[解說類大綱免示範任務](../../../tasks/open/2026-10-10-outline-pick-demo-exempts-explainers.md)。該修正尚未落地；本次未改共用審核或分數，不為湊 demo 門檻將歷史說書改成操作教學。已保存一次 Jev 結果，不反覆付費要求不同分數。

## 工作區與證據

### 2026-10-12 A 案核准與接續

- 站主回覆：「採用 A：沿脚印回到帳篷，再檢查雪板解釋（建議）」。繁中授權沿用。
- 同一 outline review 已於 `2026-10-12T05:19:58.330973Z` 決定為 `approved`、`choice=A`。本次沒有重送大綱或改 brief。
- `review-pull` 於 `2026-10-12T05:22:04.516Z` 正常記入 `approvals.json`；brief SHA 仍是 `32bf76ed25e862e3e7c9e0bf8d1d369a2f9ad625a270c5518ed0919592f32a63`。
- `reviews-2026-10-12T05-22-13.712Z.json` GET 200，回讀同一 review ID、雜湊與 A；`outline-approved-a.png` 保存後台畫面。先前短暫 502 與一次 pull exit 4 均保留，之後已成功讀回。
- 原任務已重新認領。撰稿、原件素材清權與獨立來源查核並行；現階段核准僅指大綱，不代表完整稿、旁白或成片核准。

### 正式稿與成本預檢

- 原稿 100 景、119 句、72 張插圖、46 項主張。原生估正文 603.4 秒，插圖占 64.3%；實際時間仍待 TTS。略低於大綱 65–75% 的插圖目標，未為比例增添空洞畫面；原生 50% 下限已滿足。
- 三頁 1959 結案書局部已整合為 `screenshot`；檔案 SHA、授權、裁切矩形與實看紀錄見 [素材登錄](asset-register.md)。整合只更改三景 template/data 與 assets，逐句旁白、voice、look 均完全保持。
- 整合後 `video.json` SHA：`74c91a6cc79b1f38a7fa3430ccad816c0907aaa34a2da26d193421c639ff50e9`。外部 `source-integration-*.json` 保存前後 SHA 與素材對應。
- 原生 lint 0 errors、4 warnings：日光、雪與置中構圖詞頻，以及首章約29秒。日光／雪是本集場域；鏡頭另有室內文書、器材與材質近景，第一句直接落鉤，未將章長當成鉤子延遲。沒有估計狀態超過8秒的警告。
- `tts --dry-run` exit 0：115 個請求、119句，約2,364計費字元；Gemini Sulafat ready，當月剩9,290,812字元。
- `keyframes --dry-run` exit 0：72張、MiniMax image-01／1K；每張一次估US$0.97，每張最多三次估US$2.92，低於有效US$80本集上限。這是圖片與judge預估，不是整片總支出；當前支出US$0。
- 沒有改聲音 style／look、共享字典、主機設定或審核門檻；不新增 Shorts 或其他語言。

媒體及執行證據只放 repo 外：`C:/Users/x8120/mokaair-work/videos/curio-h04`。

### 逐句審稿完成與旁白起跑

- [事實覆核](verify-1.md) 核對 100 景、119 句與 46 組主張；三組事實修正已回讀，0 未解必修。[口語覆核](listener-review.md) 完整回讀所有句子、卡片與 reveal，同樣 PASS。
- 兩份報告共同綁定最終 `video.json` SHA `98b2fe192185644dd7a36a3deac8c4f8c9314a54486cedf1ff23cdd85dfae2f8`；`claims.md` SHA `3ca492d642fc4c3e4a3ea690c50d41e5d2f119b2937af993d51961ea09ae2989`。
- 審稿後僅修順三句口語及兩組卡片揭示時機，原生 lint 仍為 0 errors／4 warnings。相關 docs-videos 測試 199 passed、0 failed。
- `2026-10-12T05:40:30.268Z` 最終 TTS dry-run exit 0：115 requests、約 2,363 計費字元，Sulafat ready。隨後啟動原生 `tts`；完成、實際時長及讀音判斷另記收據，不將起跑當成完成。

`_audit/preflight-reviews.json` 與 `_audit/preflight-settings.json` 保存唯讀預檢。
`_audit/plan-check.json`、`review-push-2026-10-12T04-53-20-715Z.receipt.json`、
`reviews-2026-10-12T04-54-15.480Z.json` 與 `outline-review-pending.png` 保存當前送審、回讀與瀏覽器畫面。
本集只授權製作及上傳包；YouTube上傳、公開、PR合併和部署未執行。
