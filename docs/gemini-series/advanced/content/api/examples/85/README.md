# 85 Batch追蹤

cases.jsonl固定20題，partial.jsonl純作者合成。reconcile與merge不連網；submit/fetch/cleanup須--live及自己的成本條件。

先reconcile response-fixtures/partial.jsonl，預期16 accepted、B17 retryable、B18/B20 failed、B19 missing。真實submit前保存帳本；送件逾時先查原工作，不能刪ledger重送。fetch一次查狀態，成功且有結果檔才下載。

真實輸出經reconcile產生retry-cases.jsonl，再submit新帳本並以--parent-ledger引用上一輪；驗證雜湊、模型與精確暫時故障清單。最多三代，第三代引用第二代；不能兩個終端同時寫帳本。

merge每題只採用一次；重複摘要會報錯。未採用題目保留unresolved，accepted仍要對evaluation.csv核對品質。cleanup只刪本帳本已終止的工作/檔案；未終止者先用官方client.batches.cancel(name=自己的job)要求取消，再fetch查到終止。取消成功不代表立即停止計費。
