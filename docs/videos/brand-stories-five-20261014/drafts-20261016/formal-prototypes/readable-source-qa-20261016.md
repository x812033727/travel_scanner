# 四集字卡來源文字與視覺檢查

2026-10-16。本紀錄僅涵蓋 A16、A37、B14、A21 的 **49 張既有 title 字卡**。原始章稿與原審查證據保留；另存四份「只改來源標示」候選，尚未採用到正式工作者，也不是影片驗收。

## 來源文字修正

初次用正式 `openRenderer.capture`／`slideHtml` 輸出 49 張卡：版面、字型與資源載入問題均為零。逐張檢視 1920×1080 原尺寸及 320×180 縮圖後，發現每張來源徽章都含內部 `S` 編碼；A16 `turn-062` 還顯示「後製分行排版」備註。原始渲染證據 SHA-256 `bd0db4fabaf1549d97513473e23012c4fe1324abce11ab8c2bee96267e5862f2`，PNG 與聯絡表留在本機工作區。

候選依各集現存 `storyboards/<集數>/source-map.json` 展開來源代碼：已有人能讀的來源名稱只去掉尾端括號代碼；A16 的 `S2` 明確換為 `Costco FY2025 Form 10-K`，`turn-062` 只刪排版備註，`turn-063` 避免重複 FY2025；A37 的 DFB 代碼換成來源映射中的德國足協及其 1954 決賽回顧／紀錄。美國專利號 `US3498798A` 原樣保留。每張 before／after 與所用來源出版者、URL 都在下表的 `evidence.json`。

| 集數 | 卡片 | 候選章稿與逐卡證據 | `evidence.json` SHA-256 |
| --- | ---: | --- | --- |
| A16 Costco | 16 | [A16 證據](A16/readable-source-candidate/evidence.json) | `a2c51be1af0fce0a21b43f6b2e31e7e0c715e0ae0134b29e7a54f489c776211d` |
| A37 Adidas／Puma | 14 | [A37 證據](A37/readable-source-candidate/evidence.json) | `f07332def3babd1b51e6ba3e3d206e825d11533c2e4d702a1732aff18aa08329` |
| B14 味之素 | 8 | [B14 證據](B14/readable-source-candidate/evidence.json) | `f0f9b708394d07ff34e96b00b3b05bd27ba0f62298a859228498af8f3d1e2229` |
| A21 Pringles | 11 | [A21 證據](A21/readable-source-candidate/evidence.json) | `8a4ee9d118569034b1c254afd506964ab3589cf735ab96512212d34af86a8fcd` |

候選產生時對每章做反向還原及物件逐值比較：除這 49 處 `scene.data.tag` 外，`title`、`subtitle`、原本的數字與界線、所有旁白、line／scene ID、鏡頭 prompt／camera、claims 與 loops 均相同；claim 仍待正式查核。候選 24 個章檔皆另存於各集 `readable-source-candidate/chapters/`，原有 `chapters/` 沒有覆寫。各檔前後 SHA-256 見對應證據。完整本機候選索引 SHA-256 `ac70757f531fc86e758429df9105ca606d5a743f4539483a8ec6a42c636072c8`。

## 實際畫面結果

候選 49 張全部重新由正式 renderer 輸出 1920×1080 PNG，零版面、字型與資源錯誤。逐張查看原尺寸聯絡表與每張以 **320×180** 顯示的聯絡表：**大標題沒有裁切或相互蓋住，主要數字可辨識**；A16 `turn-062` 的兩行算式、A21 `origin-009`／`now-083` 的兩行標題亦完整。

**手機可讀性仍未通過。** 共用 title 模板把來源徽章設為 36px、副標題 46px，縮到 320×180 約為 6px／7.7px；實看來源徽章與灰色副標題普遍難讀，較長的 A16 `now-072`、B14 `turn-075` 更明顯。候選解決了畫面上不該出現的內部代碼和備註，沒有解決字體尺寸。後續需另案處理卡片字體／資訊分層，再重新驗收縮圖；不能以 renderer 的零錯誤代替這項檢查。PNG、6 組正式尺寸及 6 組手機尺寸聯絡表留在本機工作區的 `five-next/card-source-candidate-20261016-r3/`，未加入 Git。

第一版來源對照器曾把 `US3498798A` 誤認為 `S3498798` 而停止；原失敗輸出另存。第二版重新檢查後，A16 算式來源句仍重複年份；本版只修正該句。此前輸出均留在不同本機目錄，沒有覆寫。這些是資料準備與視覺診斷，仍需正式來源查核、聽稿、敘事、實錄、插圖及整片 QA。
