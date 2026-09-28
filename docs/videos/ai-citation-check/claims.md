# 事實與示範查核表

2026-09-27 撰稿者初查。這不是獨立事實審稿；另一位查核者須比對 `video.json` 的旁白、字卡、標題、縮圖及說明欄。

| 編號 | 影片中的主張與位置 | 原始來源 | 初查結果／限制 |
| --- | --- | --- | --- |
| C1 | `real-page`：來源為 Anthropic 的 Reduce hallucinations 文件，主題是減少模型錯誤 | [Anthropic 原頁](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations) | 2026-09-27 打開原頁；來源隨時可能改版。 |
| C2 | `ci032`–`ci039`, `ci096`–`ci099`, `ci128`–`ci131`：引用可讓主張可查核；找不到支持句就撤回 | 同上，`Verify with citations` 段落 | 原頁使用短語 `Make Claude's response auditable`，並要求每個主張能找到支持引文；找不到就撤回。 |
| C3 | `ci044`–`ci047`, `ci056`–`ci059`：降低錯誤的方法不能消除錯誤，重要資訊仍要驗證 | 同上，頁面結尾限制段落 | 來源說這些方法能減少但不能消除錯誤，關鍵資訊仍應驗證。 |
| C4 | `ci052`–`ci055`, `ci104`–`ci107`：可變動資訊應看最新來源 | 站內 `ai-chat-prompt-basics` 的查證提醒；一般編輯建議 | 不提供某產品目前價格、功能或版本；僅教讀者注意時效。 |
| C5 | `ci060`–`ci063`, `ci068`–`ci071`：允許說不知道、要求資料來源能讓錯誤較易被檢查，但不能保證正確 | [Anthropic 原頁](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)；站內 `ai-chat-prompt-basics` | 官方建議允許不確定與逐項找支持來源；「較容易」屬合理編輯推論，不能表述成保證。 |

## 示意與意見

- `mock-answer`、`marker-trap`、`corrected` 是**編輯刻意製作**的示意對話。錯句「只要附引用，就不必人工查核」不是任何真實模型的輸出；旁白 `ci004`–`ci007` 已明說，畫面亦標「示意」。
- 原文短摘錄只有標題 `Reduce hallucinations` 和 `Make Claude's response auditable`；在成片上仍應檢查引文、翻譯、來源標籤與字體可讀性。
- 三步法及「一分鐘」是編輯提供的快速檢查習慣，非研究得出的耗時保證。若旁白實際給人保證時間的印象，應改弱。

## 覆核前待辦

1. 由非撰稿者重新開 C1–C3，逐項核對所有 `lines`、字卡、標題與說明欄；寫 `verify-1.md`。
2. 查核者確認沒有將示意對話誤呈現為真實商用模型輸出，並確認引用只支持修正後的結論。
3. 站主確認 `brief.md` 的編輯立場，然後才送大綱關卡；改稿後重新跑 `lint`。
