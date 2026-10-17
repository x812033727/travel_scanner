# A01 輪子行李箱 r11：年份、鉤子與片尾修訂候選 — HOLD

r11 是從凍結的 [r10 離線稿](../A01-editorial-candidate-20261018-r10/README.md)單獨產生的新候選。r10 `manifest.json` SHA-256 是 `6F60A5ECA2E907AB494BC0FCEA44D70B323E7968AC8AE435678C08F7449D5701`；修訂針對 [r10 獨立全文審查](../A01-editorial-candidate-20261018-r10/independent-full-review-20261018.md)，SHA-256 `DC279EBC66884D16C4C0BF4C4CD11A9CF23FDB130C3A3EDE2A7551DA07885E29`。審查結果是 **HOLD**，不是後續版本的通過收據。`build.mjs` 驗證這兩個雜湊和 r10 全部候選輸出；r8／r9／r10、試作系列與 B18 都沒有修改。

## 史料界線與公開說明

- 原開場把「1987 年」和「在車庫製作」合成同一條 Travelpro 主張，現已拆開。[Plath 2012 年受訪](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)的安檢後車庫鎖推車回憶**未標年份**；[Travelpro 公司沿革](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage/)把直立雙輪伸縮拉桿設計記在 **1987 年**，另記 1989 年由車庫搬進倉庫；[Plath 自己的 2024 年校友刊自述，第 17 頁](https://www.sl8.com/journal/may24/journal_images/Chinook_2024_5-3-24_FINAL.pdf)則寫 **1988 年**發明直立 Rollaboard。口播分清歸屬，未裁定哪一年正確，也沒有把未標年份的車庫回憶排到兩者之前或之後。
- 原車庫視覺回場 `hook-06→turn-09` 已改為 **`hook-06`→`turn-07`**：兩鏡用同一構圖，回收未標年份的「箱子與外置推車鎖在一起」。`turn-09`／`turn-09b` 改用中性的產品示意，不畫成 1987 年車庫現場；直立雙輪拉桿在 `turn-09b` 才揭露。實際圖片仍須以核准首圖驗兩鏡能否辨認為同一地點，這些只是提示詞。
- 公開 `youtube.description` 刪除影片未講的 **2000 年**，只保留 `now-01`／`n1` 有來源的 1997 年平衡四輪直立箱。正式工人重併企劃來源與說明欄時，仍須核對真正在正式機產出的文字。
- [Sadow 2010 年受訪](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469)只說因帶兩名孩子同行，兩只 27 吋箱塞得滿滿，沒有列出所有內容物；`idea-memory` 口播與 `i35` 不再說箱內都是孩子們的行李。

## 敘事節拍

- `origin-budget`／`r14o01` 和 `engine-porter`／`r17e01` 改成較短的口語句。後者仍明確保留 **Shiller→助理→Sadow→採購** 的多層轉述，不把理由冒充為原始採購文件。
- 大問題 `x7r4` 的回收仍在 `now-1993-retail`：新增 `r11n01` 先回想被笑、百貨拒賣與安檢拆外置推車三道障礙；`r3n03` 再用直立拉桿獲機組採用、旅客看見，以及 1993 年記者所寫的百貨多品牌供應，回答觀念、通路與使用設計各走到哪一步。**可買到不等於市場銷量或普及率已證實。** `now-outro` 的 `g5b8` 改為一句短回扣，後接留言與訂閱；21 秒獨立片尾動畫另計，不能用它補正文長度。
- 各段沒有宣稱 Anita、Sadow、Plath 的發明存在直接傳承；同樣沒有替 Emmer 未標年份的回憶排定精確順序。

鉤子登錄位置：未標年份車庫回路 `hook-06/jtmg`→第 46 鏡 `turn-07/q4zn`，300 CPM 紙上相隔 **264.8 秒**；主問題 `hook-06/x7r4`→第 56 鏡 `now-1993-retail/r3n03`，相隔 **322.8 秒**，並由同鏡前句 `r11n01` 提醒三關。這是腳本代理時間，須用實音與實剪檢查觀眾能否記住問題與辨認回場。

## 離線檢查與剩餘關卡

在儲存庫根目錄執行：

```bash
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-editorial-candidate-20261018-r11/build.mjs --check
```

`source-map.json` 逐網址列播出主張 ID；builder 斷言 `claims.md` 與場景 ID 一對一、所有主張仍為 `PENDING`、公開 `video.sources` 與主張來源集合相等。新播出的 1988 年當事人自述會讓來源總數從 r10 的 16 變 **17**。`validation.json` 列片長、回路位置、lint、插畫提示檢查，這些是文字與結構代理，不是實際台灣口音配音或畫面品質證明。

正文紙上估時依 **300／275／250 CPM 分別為 433.2／467.5／506.9 秒**；前兩項落在 A01 特訂的 420–480 秒，250 CPM 已超出。`now-1993-retail` 兩句合計 44 口語單位，`g5b8` 39，`r14o01` 33，`r17e01` 30；目前 lint 和可愛插畫檢查均為零錯誤。這些不等於實測語速或成片片長。

**A01 持續 HOLD。** r11 須重新獨立全文史料／敘事／畫面審查，實際 TTS 與盲聽，並完成正式機六章資料、來源重新合併、工作／預算與 A01 專屬片長關卡的核對。沒有新的正式 `story/reviews/script-review.json` 和主機安全前檢之前，不匯入、不啟動付費供應商、不簽影片審核。B18 與後五集仍是約十分鐘規格。
