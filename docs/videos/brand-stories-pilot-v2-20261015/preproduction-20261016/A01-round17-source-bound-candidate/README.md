# A01 round17 來源界線候選 — HOLD

此資料夾從 [round16 企劃對齊候選](../A01-round16-origin-plan-alignment-candidate/README.md) 產生，保留 round14、未追蹤的 round15 與 round16 原檔。修正依據是 [逐句獨立來源複核](../A01-round14-source-bound-loop-candidate/independent-source-map-review-20261017.md)；這仍是**作者的離線修訂**，須由另一名審查者對這份精確候選做來源、畫面與整稿覆核。

| 修改 | 新邊界 |
| --- | --- |
| `origin-r12-03/r12o03` | 館方說安妮塔旅後巡迴講旅行故事時仍帶著輪子行李箱；不再以「那只」指認與旅途或館藏箱為同一件。這景的插畫提示詞也拿掉 *same trunk*。 |
| `origin-02/4prs` | 只說在港口、車站、住處之間搬行李；不說「每到一站」。 |
| `engine-r12-07/r12e07` | 專利設計保有提把、拖帶可拆；「需要提起時」是條件說法，不把台階寫成發明人記載的實測。這景畫面改成平地上的提把與可拆帶示意。 |

三句的 `claim`、來源矩陣與 `origin`／`engine` 企劃同步更新，既有判定仍是 `PENDING`。Winnetka 來源 8 的 `supports` 加上館藏品 `2005.26.576` 及「未證實與 1928 年旅程示意為同一只」的界線；`must_verify[14]` 專列館藏品，`o20` 與來源表的 `83ew` 都綁到新項，仍待真正查核。來源矩陣另補 `origin-03/9ij6`（與 `csdd` 同屬 `o2` 的木把手主張）和 `now-06/tszs`（一般物理推論）。`n14` 的來源索引改為 `null`：ABC 的受訪者故事不是「輪子不減重量」的物理證據。舊 `NOT FOUND` 與其來源紀錄保留在原候選及矩陣歷史欄，沒有回寫成通過。

`node build.mjs --write` 僅在此資料夾產生候選；`node build.mjs --check` 核基底與所有產物雜湊、三句與兩景的精確變更、27 條來源矩陣與旁白對位，並重新 compose、lint 與檢查 cute-story 畫面規則。檢查結果：**79 景／108 句、3 句旁白修正、2 景提示詞修正、lint 0 error／41 warning、cute-story 0 error**。正文在每分鐘 250／300／320 units 的文字估時計為 651.67／556.70／528.97 秒；並非 TTS 實測。`node --check build.mjs` 也通過。

候選 `manifest.json` SHA-256：`fb664ada083dbd09529edfc4462d16bbb0d23d406126c5e7d76fde8622729a81`；`delta.json` SHA-256：`b2fc89c47d2731b2f8dda949cff8d932a565bbc5f7ca1eb7a6eaf49000dcea30`；基底 round16 manifest SHA-256：`2f44419c43c64a2ea3762dd5d2053bb0febefcfd055f057e9c940c6c6d6249df`。`manifest.json` 另釘選六章、series、來源矩陣、機械檢查與旁白全文的雜湊。

**仍 HOLD：** 對 108 句精確整稿的獨立事實與聽感審查、正式 verifier／listener／整片 narrative panel、`story/reviews/script-review.json`、實際 TTS 片長、MiniMax 圖像和成片播放皆未完成。round9 的 `chapters_link`／`payoffs`／`one_thread` 仍是歷史 FAIL。此離線候選不是正式機實稿，不授權主機安裝、付費旁白／插畫／影片、B18 或後五集匯入、YouTube 上傳。
