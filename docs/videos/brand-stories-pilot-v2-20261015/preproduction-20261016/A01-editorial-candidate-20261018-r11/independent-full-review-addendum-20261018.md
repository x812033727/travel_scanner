# A01 r11 獨立審查更正附錄：n14 正式事實關卡 P1

日期：2026-10-18。此附錄只對 `manifest.json` SHA-256 `39BCC9E69C4D89EEA044E145ABB592C587183796E92BB13646C83F82511D289A` 的 r11 候選，以及 [原獨立全文報告](independent-full-review-20261018.md) SHA-256 `2ED2F086AF582EA75DDE7ABFDF43FB032D3FA7DA2FEB3917B249C7C890D774AC` 有效。沒有修改原報告、候選、manifest 或審稿收據。

## 更正結論

原報告的「P0 = 0，P1 = 0；`PASS_OFFLINE_WITH_P2_NOTES`」**不得用作正式事實關卡通過結論**。我漏判 `candidate/claims.md:95` 的 active `n14`：`now-06/tszs` 在 `candidate/script.md:286-288` 仍說「到了樓梯前，旅客仍得提起箱子；輪子省得了拖行，省不了重量」，而 `n14` 的來源網址和查核日期均空，判定仍為 `PENDING`。`candidate/video.json` 的第 64 鏡繼續引用 `n14`，它不是已刪掉的歷史主張。此處改列 **P1：正式 factual-claims 審查前的來源與措詞缺口**。P0 仍為 0；原報告對其餘史料、結構及 P2 實剪風險的逐項觀察仍可供修稿參考。

## 為何不能以「常識」直接簽過

- `candidate/series.json` 的 `plan.must_verify` 沒有對應這句的物理條目；`n14` 也沒有可供查核者引用的來源頁。`tools/video/automation/story-prompts.mjs` 的故事撰稿規則要求企劃以外的事實有來源段落，查核規則將 `CONFIRMED` 綁到來源段落、`PLAN` 綁到企劃事實，沒有「不證自明」的正式判定。輪子不會減少箱子和內容物的重量，可作編者的普通物理推論，但須明示這個性質並讓正式審稿者判定；空來源的 `PENDING` 列不能被默認為已查核。
- 工人 `story.mjs` 允許 `source: null`，並會把空網址寫入 `claims.md`；`pilotScriptReviewProblem` 核對的是獨立 PASS 收據、檔案雜湊、章稿與敘事收據，沒有逐條拒絕空來源。`tools/video/qa/facts.mjs` 只阻止 `NOT FOUND` 主張仍被場景引用。**程式未自動阻擋不等於真人可簽 factual-claims PASS。**
- 先前 [round18 的 n14 來源歸屬局部複核](../A01-round18-n14-provenance-candidate/independent-review-20261017.md)只確認現行 `source:null` 與舊 ABC 訪談已分開；它明說是 metadata delta PASS、整片 HOLD。舊 [ABC 空服員訪談](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)能支持「裝太滿時離開輪子可能搬不動」這位受訪者的觀察，不能冒充重量不變或每位旅客都必須提箱上樓梯的直接證據。

「旅客仍得提起箱子」也把情境說成全稱；[Travelpro 的旅行說明](https://travelpro.com/blogs/the-travelpro-blog/best-luggage-for-european-travel)只說旅途中**可能**需要把輪箱提上樓梯，可作較窄敘述的來源候選。最小修法應在新的、重新雜湊的候選中限定樓梯情境，補足這句的來源及編者推論標記，並同步檢查主張表、企劃來源、影片來源索引和場景引用；再交獨立查核者覆核。此處未建立 r12，也未預先宣告新句一定通過。

## 可繼續與不得跨越的界線

r11 仍可作**唯讀正式機資料銜接**的比對基準，核對六章稿、來源重併、工作與預算，不因此匯入或開付費製作。r11 的正式事實審查狀態為 **HOLD_P1_N14**；在精確新候選與獨立複核前，不簽 `story/reviews/script-review.json`，不把原報告當成 `factual_claims: PASS`。實際 TTS、盲聽、圖像與成片關卡也仍未完成。
