# 本批實際驗證

從完整練習包根目錄執行 `python verification/test_materials.py`。測試使用標準函式庫，檢查版本來源、引文、十二題答案依據、三份 PDF 雜湊、三十筆媒體觀察表與官方 YouBike 快照的資料條件；不連線或呼叫模型。

單篇 ZIP 解壓後可執行 `python research_checks.py versions 57`，其他模式為 `evidence 58`、`quiz 59`、`papers 60`、`media 61`、`transit 62`。完整包則將程式與目錄都加上 `examples/` 前綴。`media` 回報 pending 不等於驗收通過，其他檢查也不保證模型語意正確。

2026-09-14：Windows、Python 3.13.15。論文原文用 bundled Python 3.12.14／pypdf 6.10.0 讀取，Poppler 渲染相關頁面後逐頁檢視；三篇 PDF 均保留原始 bytes。PDF 的頁序與印刷頁碼是兩種定位，表格紀錄同時保留。

尚待 NotebookLM／Gemini Notebook 真實帳號驗證：Drive 同步、上傳替換、引用點擊、模型產生題庫與實際重測、論文矩陣生成、Studio 語音與影片及下載格式、Deep Research 研究計畫與模型報告。本次瀏覽器回報 User unavailable，沒有建立筆記本、共享資料或生成媒體。

60/papers 的 ACL 論文依 CC BY 4.0；62 的官方 JSON 依政府資料開放授權條款第1版。作者程式與原創合成教材依各資料夾 LICENSE.txt。報告採一次歷史快照，不能作為目前租還車資訊或年度交通量。
