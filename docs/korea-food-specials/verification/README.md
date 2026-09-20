# 韓國美食與咖啡特輯：查核索引

本目錄收錄 22 篇 `zh-TW` 文章各兩輪的逐項查核紀錄。查核者重開文章所列的政府／觀光官方來源，核對同一分店、可見頁面文字、店名與道路地址，並檢查 Commons 圖片作者、授權、實際畫面和原創 SVG。原始工作紀錄中提到的 `WORK` 路徑，是撰稿期間的外部工作目錄；可供匯入的最終文章與資產已放在 repo 的 `apps/api/app/guides/content/` 和 `apps/web/public/guides/`。

入選依據依 [本批規則](../README.md)：A1 官方店家頁或官方專題確實點名該分店；品牌官網只補營業資料。兩輪查核不代表現場體驗，也不保證出發當日營業資訊仍相同。

| 文章 | 第一輪 | 第二輪 |
| --- | --- | --- |
| `busan-dwaeji-gukbap-food-guide` | [紀錄](./busan-dwaeji-gukbap-food-guide/verify-1.md) | [紀錄](./busan-dwaeji-gukbap-food-guide/verify-2.md) |
| `busan-jeonpo-yeongdo-cafe-guide` | [紀錄](./busan-jeonpo-yeongdo-cafe-guide/verify-1.md) | [紀錄](./busan-jeonpo-yeongdo-cafe-guide/verify-2.md) |
| `busan-milmyeon-food-guide` | [紀錄](./busan-milmyeon-food-guide/verify-1.md) | [紀錄](./busan-milmyeon-food-guide/verify-2.md) |
| `daegu-jjim-galbi-food-guide` | [紀錄](./daegu-jjim-galbi-food-guide/verify-1.md) | [紀錄](./daegu-jjim-galbi-food-guide/verify-2.md) |
| `daegu-makchang-food-guide` | [紀錄](./daegu-makchang-food-guide/verify-1.md) | [紀錄](./daegu-makchang-food-guide/verify-2.md) |
| `jeju-aewol-cafe-guide` | [紀錄](./jeju-aewol-cafe-guide/verify-1.md) | [紀錄](./jeju-aewol-cafe-guide/verify-2.md) |
| `jeju-gogi-guksu-food-guide` | [紀錄](./jeju-gogi-guksu-food-guide/verify-1.md) | [紀錄](./jeju-gogi-guksu-food-guide/verify-2.md) |
| `jeju-gujwa-sehwa-cafe-guide` | [紀錄](./jeju-gujwa-sehwa-cafe-guide/verify-1.md) | [紀錄](./jeju-gujwa-sehwa-cafe-guide/verify-2.md) |
| `jeju-heukdwaeji-food-guide` | [紀錄](./jeju-heukdwaeji-food-guide/verify-1.md) | [紀錄](./jeju-heukdwaeji-food-guide/verify-2.md) |
| `jeonju-bibimbap-food-guide` | [紀錄](./jeonju-bibimbap-food-guide/verify-1.md) | [紀錄](./jeonju-bibimbap-food-guide/verify-2.md) |
| `seoul-dak-hanmari-food-guide` | [紀錄](./seoul-dak-hanmari-food-guide/verify-1.md) | [紀錄](./seoul-dak-hanmari-food-guide/verify-2.md) |
| `seoul-dwaeji-gukbap-food-guide` | [紀錄](./seoul-dwaeji-gukbap-food-guide/verify-1.md) | [紀錄](./seoul-dwaeji-gukbap-food-guide/verify-2.md) |
| `seoul-ganjang-gejang-food-guide` | [紀錄](./seoul-ganjang-gejang-food-guide/verify-1.md) | [紀錄](./seoul-ganjang-gejang-food-guide/verify-2.md) |
| `seoul-ikseon-bukchon-hanok-cafe-guide` | [紀錄](./seoul-ikseon-bukchon-hanok-cafe-guide/verify-1.md) | [紀錄](./seoul-ikseon-bukchon-hanok-cafe-guide/verify-2.md) |
| `seoul-jokbal-food-guide` | [紀錄](./seoul-jokbal-food-guide/verify-1.md) | [紀錄](./seoul-jokbal-food-guide/verify-2.md) |
| `seoul-kalguksu-food-guide` | [紀錄](./seoul-kalguksu-food-guide/verify-1.md) | [紀錄](./seoul-kalguksu-food-guide/verify-2.md) |
| `seoul-naengmyeon-food-guide` | [紀錄](./seoul-naengmyeon-food-guide/verify-1.md) | [紀錄](./seoul-naengmyeon-food-guide/verify-2.md) |
| `seoul-samgyetang-food-guide` | [紀錄](./seoul-samgyetang-food-guide/verify-1.md) | [紀錄](./seoul-samgyetang-food-guide/verify-2.md) |
| `seoul-seolleongtang-food-guide` | [紀錄](./seoul-seolleongtang-food-guide/verify-1.md) | [紀錄](./seoul-seolleongtang-food-guide/verify-2.md) |
| `seoul-seongsu-cafe-guide` | [紀錄](./seoul-seongsu-cafe-guide/verify-1.md) | [紀錄](./seoul-seongsu-cafe-guide/verify-2.md) |
| `seoul-tteokbokki-food-guide` | [紀錄](./seoul-tteokbokki-food-guide/verify-1.md) | [紀錄](./seoul-tteokbokki-food-guide/verify-2.md) |
| `seoul-yeonnam-hongdae-cafe-guide` | [紀錄](./seoul-yeonnam-hongdae-cafe-guide/verify-1.md) | [紀錄](./seoul-yeonnam-hongdae-cafe-guide/verify-2.md) |

## 本機驗收與發布界線

- 22 篇經本批 `intake_check.py` 收件：零錯誤；5 篇落在建議字數帶外，但均低於 5,000 字硬上限。
- 同批無重複 hero、無跨篇重複 alias；每篇有 hero、原創 SVG 圖解與至少一張內文照片。`python docs/korea-food-specials/verification/check_batch.py` 可重跑這些跨篇檢查，並確認每家咖啡店都有本批允許的類型標籤。
- 來源標題只保留頁面名稱；來源證明的具體事實留在查核紀錄，不塞進讀者看得到的標題。逐篇 `pack_cli ingest --dry-run`、整批 `pack_cli lint`、任務檢查及工具測試結果以本次 PR 檢查記錄為準。
- 此目錄是撰稿與本機查核證據；正式站的部署、匯入、發布和逐頁瀏覽器驗證仍需依 `launch-runbook.md` 執行並另記結果。
