# H04 製作紀錄

2026-10-12，Asia/Taipei。承接站主「繼續」，製作已查核題庫的下一集，僅繁體中文。H03 已完成上傳包；本集沒有沿用 H03 的核准或媒體。

## 目前狀態

- 分支：`codex/curio-h04-production-20261012`，由當前 `origin/main` 的 `f7691d8cb` 建立。
- 任務：`2026-10-12-produce-curio-h04-dyatlov-traditional-chinese`，scope 僅本資料夾。
- 碰撞檢查：H04 沒有 active task 或 open PR；正式站 H04 GET 回 404，沒有既有製作要接手。
- 正式站頻道立場已讀回，`auto_pick_outline=true`。本次大綱套用 2、3、4、6、9。
- `brief.md` 三案已送審，Jev 推薦 A，正式站仍待站主選定；詳見下方審核收據。
- `video.json` 目前是原生送審所需的企劃佔位，非完整腳本，未執行 TTS、生圖或合成。

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

媒體及執行證據只放 repo 外：`C:/Users/x8120/mokaair-work/videos/curio-h04`。
`_audit/preflight-reviews.json` 與 `_audit/preflight-settings.json` 保存唯讀預檢。
`_audit/plan-check.json`、`review-push-2026-10-12T04-53-20-715Z.receipt.json`、
`reviews-2026-10-12T04-54-15.480Z.json` 與 `outline-review-pending.png` 保存當前送審、回讀與瀏覽器畫面。
本集只授權製作及上傳包；YouTube上傳、公開、PR合併和部署未執行。
