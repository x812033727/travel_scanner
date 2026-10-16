# A01 round15 獨立畫面與來源審查

日期：2026-10-16。結論：**PASS，僅限納入草稿 PR 的離線文字候選；製作與正式環境維持 HOLD。** 本審查只適用於 `manifest.json` SHA-256 `9aa8ef49cf6e7df4cdc260f126dbf3102a1bcf7d960af5f5a95ce1f4196f0a8b`；任何候選檔或 manifest 改動都須重新核對。這不是劇本審稿收據、圖片驗收、成片核准或付費授權。

## 獨立核對範圍

- 逐位元組核對 round14 與本輪的 `candidate/series.json`、`source-map.json`，兩者完全相同；逐景刪去 `data.prompt` 後比對六章 JSON，其他欄位完全相同。唯一變動是 `hook-01`、`hook-03`、`origin-06`、`origin-13`、`origin-15`、`engine-r12-04`、`turn-12` 的七個提示詞。場景仍為 79 景、旁白仍為 108 句；章節、句子、主張、loop、角色綁定、鏡頭與運鏡均未變。
- 獨立重算 manifest 雜湊，並執行 `node build.mjs --check`：七處變動、0 lint 錯誤、0 cute-story 畫面錯誤、39 警告。以 `keyframes.mjs` 的 `shotPrompt()` 另行重組七景的 look、camera 與 cast，逐字等於 `effective-prompts.json`；七景長度 709–1191 字元，均小於 MiniMax image-01 的 1,500 字限制，沒有截斷。有效提示詞檔 SHA-256 為 `8ef0ed280e2a34f7917eb9bc3811c265497cee80f41878130746f965789bac5c`。
- `validation.json` 的八條來源索引與企劃來源 URL 相符；它們保留既有的 `CONFIRMED`、`PLAN` 或 `PENDING` 判定，**沒有因本次畫面審查升級主張或劇本查核狀態**。

## 七景的史料界線

| 景 | 獨立觀察 |
| --- | --- |
| `hook-01` | [Sadow 本人訪談](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)支持兩只沉重手提箱；新版移除未證實的月亮與黃昏。完整提示詞仍附加 `traveler-heavy` 的「手提一只」外觀，鏡頭文字則要求雙手各一只；文字並非邏輯矛盾，但模型可能只畫一只，必須以實圖核對。 |
| `hook-03` | 同一[訪談](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)描述一名男子推著底下有輪子的載重滑板。新版以空地分隔前景的輪板與後景 `traveler-heavy` 手提的無輪箱；完整提示詞與附加角色相容，也不指定木材或推板者職業。兩個景深主體仍可能被生成模型混合，實圖須確認輪子只在滑板底下。 |
| `origin-06` | [溫尼特卡歷史學會](https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/)記錄一只安妮塔輪子箱留存，但沒有證明它就是先前旅程插畫所指的同一只。新版只畫中性背景的簡化展示示意，不安排館內開櫃事件或精確復原館藏品。 |
| `origin-13` | Sadow [訪談](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)支持四個箱底腳輪與繩子；新版不再畫未經記載的鎖螺絲步驟。 |
| `origin-15` | [Sadow 專利](https://patents.google.com/patent/US3653474A/en)列有較早的 Kelly 專利；兩只關閉的空白資料夾是年代先後的象徵，沒有偽造專利文字、圖紙或審查員事件。 |
| `engine-r12-04` | [專利說明](https://patents.google.com/patent/US3653474A/en)把四組輪件 23–26 分為窄箱蓋底部兩組與寬箱身底部兩組。新版的俯視箱底是設計示意，不宣稱已出售實物採用相同構造；實圖須能數出四組且位置正確。 |
| `turn-12` | [Travelpro 的歷史頁](https://travelpro.com/pages/our-history)支持乘客採用，[品牌回顧](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage)另敘述 Plath 於 1991 年離開航空公司。新版只畫匿名一般乘客拉兩輪箱並看手柄，與附加的 `traveler-upright` 外觀相容，沒有把兩件事演成同一天或同一人。 |

三鏡連續小樣 `turn-15 → now-01 → now-02b` 的「兩輪直立 → 四輪直推 → 四輪萬向」是不同年代的概念比較；[Samsonite 官方年表](https://corporate.samsonite.com/en/about-us.html)支持 1997 年平衡四輪直立箱及 2000 年四輪 spinner 的年份。橫向移動是對 spinner 功能的示意，不能剪成同一場歷史實拍。此處只審查小樣計畫，尚無圖片或播放結果。

## 尚未通過的關卡

`hook-01` 的兩箱數量、`hook-03` 的滑板／手提箱分隔、`origin-06` 的非實物復原、`engine-r12-04` 的四組輪件位置，均須在實際 MiniMax 圖像中核對。文字估時在每分鐘 250 spoken units 下有 16 景超過 10 秒；這不是 TTS 或實速觀看證據。39 條 lint 警告尚在，包含畫面物件重複與長靜圖。round14 以前的敘事、事實、lexicon 與正式劇本收據缺口未由本輪消除。沒有生成圖片、音檔、三鏡小樣或成片，沒有主機寫入、匯入、部署、付費工作、上傳及站主觀看核准。本審查不放行這些步驟。
