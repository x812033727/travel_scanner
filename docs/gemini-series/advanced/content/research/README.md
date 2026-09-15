# NotebookLM 與研究方法｜57–62 作者交付

六篇繁體中文原稿、內容包、十二張原創配圖、六份單篇練習 ZIP 與一份整合 ZIP 已完成本機建置。本文的「作者交付」不代表雲端實測、課綱全部驗收或公開發布；尤其第 61 篇尚缺真實生成的音檔、影片與三十筆跨格式觀察。

系列總入口：[深入教學課綱](../../README.md)。原公開系列入口仍維持五十篇，這批不修改共用目錄與發布收據。

| 篇章 | 原稿 | 作者練習材料 | 真實操作狀態 |
| --- | --- | --- | --- |
| 57 來源版本管理 | [教學](57/lesson.md) | [六個 ID 與兩版規格](examples/57/README.md) | Drive 同步、上傳替換與四次回答待驗 |
| 58 引用查核 | [教學](58/lesson.md) | [三份矛盾資料、五列矩陣](examples/58/README.md) | 模型回答、引用點擊與修正待驗 |
| 59 備考與複習 | [教學](59/lesson.md) | [兩章、十二題、錯題與重測表](examples/59/README.md) | 生成題庫與真實作答／重測待驗 |
| 60 多篇研究比較 | [教學](60/lesson.md) | [三份原始論文與比較表](examples/60/README.md) | 模型矩陣與逐欄引用待驗；原文已查 |
| 61 多格式教材 | [教學](61/lesson.md) | [十項事實、參考講義／腳本、三十列空白觀察表](examples/61/README.md) | 語音與影片尚未生成，不能當完整媒體成品 |
| 62 專題報告 | [教學](62/lesson.md) | [公開快照與作者參考報告](examples/62/report.md) | Deep Research 計畫與模型報告待驗；資料已重算 |

## 已完成的驗證

- 六篇正文依內容包計數為 2,055–2,219 字，均有四階段、故障與修正、可複製內容、表格、三個 FAQ、先修與相關文章連結。
- 22 項本機測試通過：有效版本唯一、來源位元組、假引用、未知問題、單選選項、章節依據、論文完整性、媒體觀察缺項、交通資料缺欄／重複 ID／非整數／負值／未來時間等。程式不做網路請求或模型呼叫。
- 七個 ZIP 的 CRC、路徑與原檔位元組一致。整合包解壓後再次執行 22 項測試通過。
- 三篇 ACL 論文全文保留原始 PDF，作者查閱方法、資料與代表結果，九張相關頁面渲染後逐頁檢視。HyDE 方法定位為第 3.2 節，圖一在 PDF 第二頁，不能寫成第 2 節方法。
- YouBike 快照實際重算 1,800 筆唯一站點、十三種 sarea 標籤，包含六十五筆臺大公館校區；資料集頁列舊欄位而 JSON 已用另一組名稱。Quantity 的正式含義未確認，報告不直接套用容量或需求推論。
- 十二張圖片的桌面與 360 像素手機預覽共 24 張均經逐張檢視，沒有文字裁切或重疊。這是素材檢查，未代替完整網站手機操作驗收。
- 新六篇、先前工作／MD／CLI 自動化共十八篇，以及原五十篇加總目錄的內容、資產與連結檢查通過。新六篇通過 guide pack lint。相關 API 測試 38 項通過、8 項因未提供獨立 PostgreSQL 整合服務而跳過；SQLite 分支通過。Ruff 與任務檢查通過，任務工具仍有既存其他任務的警告。

證據：[來源收據](source-downloads.json)、[官方來源](sources.json)、[本機測試](verification/fixtures.json)、[ZIP 核對](verification/delivery.json)、[配圖與論文檢視](verification/visual-review.json)、[建置與字數](verification/build.json)、[凍結快照](verification/authoring-review.json)。

## 尚未完成的驗收

本次瀏覽器狀態回報 `User unavailable`。沒有建立筆記本、呼叫 Gemini 模型、操作個人 Drive、分享資料或生成媒體。所有模型答案、Studio 產出和使用者作答紀錄均未偽填成功。

1. 57：同一來源經 Drive 與本機上傳的 v1／v2 真實同步、引用位置與舊產出重做觀察。
2. 58：真實五列回答、引用逐一點擊、假主張修正與缺證據問題。
3. 59：Studio 題庫生成、十二題審閱、實際作答與後續重測；預定日期保持未完成。
4. 60：三篇全文的模型矩陣、引用定位與故障提示詞修正；作者矩陣不等於模型輸出。
5. 61：真實講義、音檔、影片、各自下載格式與 30 筆觀察；旁白腳本不能代替音檔或影片。
6. 62：Deep Research 研究計畫、實際模型報告、Notebook 引用與修正紀錄；公開資料分析已完成。

上述項目仍保留在[研究批次任務](../../../../../tasks/open/2026-09-14-gemini-advanced-research.md)。素材／API 兩批、共用導覽、發布與公開頁面驗收仍待後續完成；整套驗收前不開放深入系列入口。

## 重新建置

```powershell
apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/advanced/content/research/build-data.py
apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/advanced/content/research/build-report.py
apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/advanced/content/research/build-data.py
apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/advanced/content/research/verification/test_materials.py
apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/advanced/content/research/verify-delivery.py
apps/api/.venv/Scripts/python.exe -X utf8 docs/gemini-series/build.py --track research
node tools/gemini-series.mjs check --draft --track research
```

第二次 build-data.py 讓 ZIP 納入最新作者報告；此程式只重建原創練習，不重抓或改寫外部原始 PDF／JSON。已附 hero.jpg，正常重建不需瀏覽器。修改 SVG 時重跑 build-art.py、以 --render 建置、render-art.mjs --track research，再逐張檢視並更新凍結紀錄。

原創教材與檢查器採 MIT；論文原始 PDF 另依 CC BY 4.0，官方交通資料另依政府資料開放授權條款。授權來源與顯名分別保留，不能把整包第三方資料一概改標 MIT。作者凍結快照排除自身與快取，記錄交付位元組，並不表示使用者核准或正式發布。
