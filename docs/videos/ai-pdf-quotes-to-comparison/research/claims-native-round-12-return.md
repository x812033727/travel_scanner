## 第12輪獨立查核附記（2026-10-26）

本節只附加在現有 claims.md 末尾，不取代、不刪減前文任何內容。前文 c1–c41 的證據列、八頁抽文全文、需求與提示詞全文、計算與執行收據全部原樣保留。

- 查核報告：verify-12.md。結果為 49 CONFIRMED、0 CHANGED、0 NOT FOUND、1 OUT OF SCOPE，video.json 不需修改。
- 逐項複核方式：
  - c1–c27、c38–c41 的所有金額，用八頁抽文逐字核對後重新手算。結果為 2100／2050／待確認、2100、50、3990／4100／3937.50、110、52.50、12張 2478／2460／2467.50、13張 2667／2665／2651.25、+7.50／−13.75、21.25，全部吻合。
  - c31、c36、c39 的命令卡 argv，與實跑收據逐字一致。exit code、stdout／stderr 末行、output_directory_created 也都一致。
  - c37 的詢問句與 questions-21.txt 逐字一致。
- 本日官方頁複核：
  - openpyxl：https://openpyxl.readthedocs.io/en/stable/simple_formulae.html （status 200，2026-10-26），原文「openpyxl never evaluates formula」，支持描述欄的「不宣稱它會計算公式」。
  - pypdf：https://pypdf.readthedocs.io/en/stable/user/extract-text.html （status 200，2026-10-26），原文「pypdf is not OCR software.」，支持描述欄的「不做掃描影像 OCR」。
- 待下一輪處理的措辭建議（非事實錯誤）：threshold-results 的 source 可註明丙取自 cedar-revised.pdf。
- 本次查核沒有執行任何程式、呼叫 AI／TTS、上傳或核准。
