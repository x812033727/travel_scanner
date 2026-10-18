# A01 輪子行李箱 r12：樓梯敘述來源修訂候選 — HOLD

r12 是從凍結的 r11 離線稿單獨產生的新候選。r11 `manifest.json` SHA-256 為 `39BCC9E69C4D89EEA044E145ABB592C587183796E92BB13646C83F82511D289A`；r11 原獨立審查 SHA-256 為 `2ED2F086AF582EA75DDE7ABFDF43FB032D3FA7DA2FEB3917B249C7C890D774AC`；[r11 的 P1 更正附錄](../A01-editorial-candidate-20261018-r11/independent-full-review-addendum-20261018.md) SHA-256 為 `ED0C8932DBE71440CCE9E7A3E6D55EC791EF2785010B53F282357C52CEDDF1D7`。原審查的 PASS 不能作為正式事實關卡結論；`build.mjs` 會驗證這三份檔案及 r11 候選所有輸出雜湊，r12 不繼承 PASS。

## 本輪唯一史料修正

r11 `now-06/tszs` 說「到了樓梯前，旅客仍得提起箱子」，`n14` 沒有來源。這把可能的困難說成所有旅客必須提箱。[Travelpro 官方比較文章](https://travelpro.com/blogs/the-travelpro-blog/bring-this-not-that-duffel-bags-versus-rolling-suitcases)於 2021-09-15 發布，2026-10-18 核對；它只說**對部分旅客，推輪箱走樓梯或顛簸人行道可能困難**，同篇也說輪箱在一般移動時容易推行。r12 口播改成「到了樓梯前，有些人推輪箱也會犯難；平地好走，不代表每一段路都順手。」`n14` 同步加上該網址與限定。畫面只讓匿名旅客和輪箱停在樓梯前，輪子仍著地；不畫必然提箱或攀階的動作。

這是今天旅客的使用限制，不代表早期任何一款原型的歷史性能、也不歸因於特定發明者。r11 的其餘年代、人物、鉤子、片尾、章序與已標的 P2 均未修訂。

原企劃 `stories.json` 與正式機保存的 `beats.sources` 未在本輪改動。`plan-source-addition.json` 是日後正式機來源重併時應核對的**提案資料**，不能直接當成已匯入或已審核的主機企劃。正式稿與主機重新合併若產生額外或缺漏網址，仍須重審公開來源清單。

## 可重現檢查

從儲存庫根目錄執行：

```bash
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-editorial-candidate-20261018-r12/build.mjs --check
```

`build.mjs --write` 只寫本 r12 目錄。它重新產生 `candidate/video.json`、`script.md`、`claims.md`、`source-map.json`、`validation.json` 與雜湊清單。逐筆主張仍為 `PENDING`，紙上估時與 lint 不能當作 TTS、圖片或成片驗收。

**A01 持續 HOLD。** r12 尚須獨立全文／來源／敘事審查，正式機六章唯讀核對及稿件差異審查、實際旁白時長與盲聽、畫面聯絡表及安全前檢。這份候選沒有簽發正式 `story/reviews/script-review.json`，沒有匯入、主機寫入、付費圖片或配音，也沒有授權 B18 或後五集製作。
