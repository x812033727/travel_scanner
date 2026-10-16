# 五集完整旁白與來源更新

2026-10-16。這裡保存「接著再做五集」後新增的完整旁白、來源定位與獨立修訂紀錄。規格沿用 MiniMax `image-01`、`cute-mystery`、約 10 分鐘、單人台灣口音、可關閉繁中 CC；濃縮開場後接既有 5 秒動畫，正文後接 21 秒片尾，實際 YouTube 可點元素另行設定。

## 閱讀方式

- `source-refresh-and-outline-*.md` 的旁白表才是要配音的正文；來源、主張、loops、審稿說明不配音。
- 作者原檔按受審 bytes 保存，開頭的「待審／只存 Temp」描述的是提交當下。下列獨立 review 與本索引記錄後續進度；例如 A16 v4 的舊 `AUTHOR_V3` 標籤不改變它實際受審的 v4 hash。
- 早期作者版本供差異核對；不把早期 review 當後續變更的批准。
- `sources-*/sha256.json` 是當時來源擷取的識別資料。原始 HTML、PDF 和閱讀用圖片留在製作工作區，沒有加入公開儲存庫；此處正文與審查文件保留官方連結和頁碼。失敗下載仍如實記錄。

## 製作順序與目前稿件

| 順序 | 集數 | 本次進度 | 編輯稿與最近審查 |
| --- | --- | --- | --- |
| 1 | A29 LEGO：為何出售仍有獲利的樂園 | 完整稿的來源與文字待修已結清；65 段、2,201 字 | [作者 v3](source-refresh-and-outline-A29.md)、[全文審查](A29-draft-review.md)、[v2 差異](A29-v2-diff-review.md)、[v3 差異](A29-v3-diff-review.md) |
| 2 | A16 Costco：一美元五角熱狗背後的生意 | 完整稿的來源與文字待修已結清；50 段、2,114 字 | [作者 v4](source-refresh-and-outline-A16.md)、[敘事修訂](A16-narrative-review-v2.md)、[全文審查](A16-v3-independent-review.md)、[v4 差異](A16-v4-diff-review.md) |
| 3 | A37 Adidas／Puma：兄弟分家後的競爭 | 完整稿修訂及新增來源已核對；48 段、2,152 字 | [作者 v4](source-refresh-and-outline-A37.md)、[原全文審查](A37-independent-review.md)、[v4 覆核](A37-v4-independent-diff-review.md) |
| 4 | B14 味之素：調味料公司如何做出晶片材料 | 完整稿修訂及新增來源已核對；48 段、2,161 字；正式章稿可合併 T03a／T04 相鄰概括句 | [作者 v4](source-refresh-and-outline-B14.md)、[原全文審查](B14-v2-independent-review.md)、[v4 覆核](B14-v4-independent-diff-review.md) |
| 5 | A21 Pringles：洋芋片的三回合稅案 | 五組修訂與新增裁判主張已覆核；47 段、2,281 字 | [作者 v3](source-refresh-and-outline-A21.md)、[v2 全文審查](A21-v2-independent-review.md)、[v3 差異覆核](A21-v3-independent-diff-review.md) |

字數以六章正文的旁白欄去除空白、標點及符號計算，英文字母與數字也逐字元計，不是發音音節。每分鐘 230–250 字只是編輯估算；TTS 尚未生成，沒有實測片長。片頭片尾不能補足正文至少 8 分鐘的門檻；以具體事件和解釋補足內容，不用重複、慢播或延長停頓。

分鏡拆解時發現 A29 舊統計誤收 8 列懸念回收表，因而多算 8 段、39 字；已依明確正文區段重新核對全部五篇，僅 A29 受影響。正確旁白粗估為 8:48–9:34，含固定動畫約 9:14–10:00。詳見[更正報告](corrected-metrics-20261016.md)與[逐列核算](corrected-metrics-20261016.json)。作者原稿與舊審稿 bytes 保留，原稿中的「73 段」是歷史計數誤文；[舊 metrics](A29-draft-metrics-before-count-correction.json)另存，現用 metrics 已修正。這不改變旁白內容、來源、worker rows 或編譯檔。

## 和工人輸入的關係

五份完整稿均已通過來源知情的獨立文字覆核；它們不等於正式 worker 產出的章 JSON、合併 narration 或盲評結果。

本次五份新 rows 已按全文重編來源和主張、取得各自匹配的新獨立收據，並更新上層 `episodes/`、`episodes/reviews/` 與 `stories.json`。A37 改用同篇官方新聞稿 PDF 與 2019 官方年報；PDF 所在 must_verify `[0]` 由獨立審者實讀。正式輸入收窄原 v4 的「戰爭帶來壓力」「與西德隊密切合作」「Adidas 按天候換釘」三處修飾；v4 全文與原 review 精確 bytes 均保留，不能把原稿當成逐字已改。詳見[本次 worker 輸入索引](worker-inputs-20261016/README.md)。

整合前，已將原 episodes 的五個 rows、五個 reviews、三份 evidence 說明和 stories.json 共 14 檔，按精確 bytes 保存至 [previous-worker-inputs-20261015](previous-worker-inputs-20261015/sha256.json)，索引逐檔列 bytes／SHA-256。五份新收據的 hash／schema 已驗證一致後才替換上層。正式 build 與預編譯 bytes 相同，Python check_story_file 前後檢均為 5 rows、0 problems／refused／ignored。原 100 題題庫 SHA 不變。編譯檔及各 row／review hash 見[整合紀錄](worker-inputs-20261016/integration-verification.json)。

作者 rows、source maps 與來源補充裡的「候選／待審」是凍結交稿當下的描述；當前 row 核准以相符的 `episodes/reviews/<id>.json` 和整合紀錄為準，不改受審 bytes。來源存取失敗與後續成功紀錄同時保存，不把 PDF 的 HTTP 200 說成 reader 能讀正文。

## 媒體與驗收

逐鏡準備與獨立重建結果集中在[分鏡索引](storyboards/README.md)。分鏡完成不表示正式章稿或成片已通過；原旁白、精確的文字限縮、畫面用途、卡片口徑與開場共用圖的對應分別記錄。

五集的分鏡編輯覆核已完成，共 424 鏡、349 張規劃獨立插畫。上表仍記作者原稿的字數；分鏡候選另有 A37 三段來源限縮（2,136 字）及 A21 一處上訴人指代澄清（2,283 字），各有逐字差異與獨立覆核，沒有覆寫原稿或冒用舊審稿結果。

[完整製作報價 v3](cost-proposal/B18-five-production-cost-proposal-v3.md)依上述素材數重算：後五集模型估算合計 US$10.92590，建議各片 US$5、五片共 US$25；B18 另估 US$2.60098、建議上限 US$5。六集提案合計上限 US$30，尚未核准。已獨立重算六集公式與核對 69 個來源雜湊；現行固定 US$25 的 pilot 帳本尚不能執行這個逐片 US$5 提案，須另完成限額實作與部署驗證。A01 原有授權獨立。

五集尚未匯入正式站，未生成 TTS、插畫或 MP4。順序仍依站主決定：先完成 A01／B18 試作及看片，再接這五集。僅 A01 有明確 US$25 付費授權，不能自動延伸給 B18 或五個新預算。使用者已豁免訂閱帳務／餘額舉證，不再以餘額截圖作前置關卡；進入媒體前仍需各集具體張數、整片報價與授權；之後驗實際旁白時長、音訊、插畫、可關閉 CC、完整成片，最後由站主看片。上傳、排程、公開及結束畫面可點仍各自記錄。
