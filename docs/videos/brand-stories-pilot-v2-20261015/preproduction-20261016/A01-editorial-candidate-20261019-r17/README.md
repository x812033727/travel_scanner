# A01 輪子行李箱 r17：1993 年通路節拍候選 — HOLD

這是從已釘選 r16 離線稿衍生的**另一份候選**。r16、r15、正式機、媒體與付費素材不改動。建置器須先驗證 r16 全部輸出，以及 r16 的 25 筆來源企劃校正包，再只寫此資料夾。舊審查不自動核准 r17。

## 精確修訂

- 第 56 鏡 `now-1993-retail` 把「三關：拉箱被笑、百貨拒賣、安檢拆推車」清單式重述，換成 1993 年記者 Judi Dash 當時寫下的新通路變化：Travelpro 初期靠郵購，至 1993 年主要百貨已可買到四家品牌的輪子登機箱。[Dash 當時的實測文章](https://www.latimes.com/archives/la-xpm-1993-08-01-tr-19135-story.html)直接支持這兩句。口播仍只說「記者」，不引入未登記的外語發音。它回答開場「有輪還缺什麼」中的**買得到**，下一鏡接著試乘機艙。本文沒有把可買到推論成全市場普及或確切銷量。
- 第 53 鏡 `now-passenger` 的匿名插畫移除未經史料確定的 `late-1980s` 場景年份；[2010 年《紐約時報》回顧、2016 年 RNPA 重印第 48 頁](https://rnpa.org/images/old-contrails/Contrails-199-Aug2016.pdf)只說旅客曾在航站看到空服員拉 Rollaboard，未為那個畫面標日期。旁白不變。
- 第 56 鏡不再唸到的 `n60`／`n64`／`n65`／`n66`／`n67` 五筆舊回扣主張從該鏡和主張表移除；這些來源仍由其他場景引用。主張數由 78 變 73，18 個公開來源順序、25 個企劃來源順序、65 鏡、其他 64 鏡、全部台詞 ID、章序與鉤子 setup／payoff ID 均保留。新的 `source-map.json` 和 `source-alignment.json` 明確重算 73 筆映射；r16 的 78 筆來源對照不能沿用作 r17 正式審稿收據。

## 使用界線

離線查核只確認檔案可重建、來源映射與靜態敘事；實際旁白與剪輯時長仍未測。全部主張仍是 `PENDING`。正式機仍須核對 104→新版本、六章、重編主張、verifier、listener、兩名獨立敘事讀者、`story/reviews/script-review.json`、實際 TTS 與圖片聯絡表。此候選保持 **HOLD**，不授權主機寫入、解除 STOP、付費呼叫、合成或上傳。

在儲存庫根目錄執行：

```bash
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-editorial-candidate-20261019-r17/build.mjs --check
```
