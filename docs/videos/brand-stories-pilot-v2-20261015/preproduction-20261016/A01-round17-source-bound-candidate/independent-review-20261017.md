# A01 round17 精確差異與來源獨立複核 — 局部可接受，來源中繼資料仍 HOLD

日期：2026-10-17（台北）。本覆核只比較 round16 → round17 的精確變動，並參照 [round14／15 的 25 條來源表逐句審查](../A01-round14-source-bound-loop-candidate/independent-source-map-review-20261017.md)。這不是正式機實稿的 verifier、listener、narrative panel 或 `script-review.json`。

## 檔案綁定與獨立差異

- round16 基底 `manifest.json` SHA-256：`2f44419c43c64a2ea3762dd5d2053bb0febefcfd055f057e9c940c6c6d6249df`。
- round17 `delta.json` SHA-256：`b2fc89c47d2731b2f8dda949cff8d932a565bbc5f7ca1eb7a6eaf49000dcea30`；`manifest.json` SHA-256：`fb664ada083dbd09529edfc4462d16bbb0d23d406126c5e7d76fde8622729a81`。這些以本機 SHA-256 重新讀取確認，並非只照抄 README。
- `node build.mjs --check` 退出碼 0，報 79 景／108 句、僅三句旁白變動、lint 0 error／41 warning、cute-story 0 error；機械檢查狀態仍是 `OFFLINE_MECHANICAL_ONLY_HOLD_FULL_REVIEW`。
- 獨立遞迴比較 round16／17 JSON：`hook`、`idea`、`turn` 章逐欄位相同；`origin` 只動兩句旁白、兩筆 claim 的 claim/note、`o20.fact/note` 和一景 prompt；`engine` 只動一句旁白、對應 claim/note 和一景 prompt；`now` 只動 `n14.source/note`。series 只動 `origin.point`、`engine.point`、`sources[8].supports` 並增 `must_verify[14]`。source map 只改三條對應行的來源描述／文字、`83ew.fact_index`、狀態說明，並在末尾增 `9ij6`、`tszs`。沒有發現旁支欄位或其他章旁白變動。

## 三句旁白與兩景畫面

| 精確位置 | 來源判讀 | 本地結論 |
| --- | --- | --- |
| `origin-r12-03/r12o03` 改「旅程結束後，安妮塔巡迴講旅行故事時，仍帶著輪子行李箱。」 | [Winnetka Historical Society 館藏文章](https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/)記第二次旅程後，她帶輪子行李巡迴講藝術與旅行。拿掉「那只」後不再把巡迴時的箱子、1928 旅途示意箱、館藏物件指成同一件；保留館方歸屬。 | **此句來源範圍可接受。** 同景 prompt 的匿名女子、普通無品牌輪子箱、示意而非實物復原也在來源界線內；需看生成圖是否真的沒有重建特定箱子。 |
| `origin-02/4prs` 改「在港口、車站和住處之間，行李得跟著搬。」 | [同一館方文章](https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/)記在港口、車站和各式住處之間搬行李。刪去舊句「每到一站」的全稱頻率。 | **此句來源範圍可接受。** |
| `engine-r12-07/r12e07` 改「需要提起時，還能用原本的提把拿起箱子；拖帶也能拆下來。」 | [Sadow 原專利 US3653474A](https://patents.google.com/patent/US3653474A/en)的示例有原提把 16、端環 17、可拆拖帶 18；權利要求容許提與滾。新句是專利設計的條件用途，沒有再聲稱台階實測。 | **此句來源範圍可接受。** 同景 prompt 改平地展示提把、環與分離拖帶，沒有無據台階事件；四輪箱是專利設計示意，需以真圖 QA 核對。 |

三句對應 `claim-r12o03`、`o17`、`claim-r12e07` 的 `claim` 字串與 source-map 行文字均與旁白逐字一致，原 `PENDING` 與 `PENDING_INDEPENDENT_REVIEW` 保留。兩景 prompt 之外的場景畫面欄位未變。本審查沒有看 MiniMax 真圖或實際成片。

## 來源鏈補強與剩餘矛盾

- series `sources[8].supports` 新增館藏品 `2005.26.576` 的有限說法；`must_verify[14]` 專列一件留存的安妮塔輪子箱及未證明與 1928 旅途示意同一件的界線。`origin/o20.fact` 與 source-map `origin-06/83ew.fact_index` 均為 14，`o20.verdict` 仍 `PENDING`。館方[館藏文章](https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/)與[2010 年藏品紀錄](https://www.winnetkahistory.org/gazette/from-the-curator-fall-2010/)能支撐「有一件留存」，不能指認與片頭示意同一件；本次綁定正確。
- source map 由 25 增至 27 條，新增 `origin-03/9ij6 → o2/source 8/fact 5`，木把手句有來源；另增 `now-06/tszs → n14/source null/fact null`，章稿 `n14.source` 也改 `null`。這是正確區分一般物理敘述與 [ABC 2010 空服員訪談](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469) 的觀察。27 條 source-map 行仍全部 `PENDING_INDEPENDENT_REVIEW`。
- **仍有一筆中繼資料矛盾**：同份 `source-map.json` 的 `inherited_claim_reconciliation` 裡，`n14` 列仍標 `active: true`、頂層 `source: 6`、`source_url` 指 ABC，且 `current` 筆仍沿用原說明；新 active `tszs` 行與章稿卻已把來源改 `null`。若此欄要保留舊 ABC 歸屬，應明確標為歷史來源、把「現行來源」指向 null，或改為非 active 的舊歸屬紀錄；不要讓後續 verifier 把受訪者觀察當成重量的物理證據。**在這筆內部來源鏈歧義修好前，不宜聲稱來源表完整對齊。**

最窄的 **round18** 修法是只重建來源矩陣與 manifest：`inherited_claim_reconciliation[n14]` 保留 `active: true`，將頂層現行 `source`／`source_url` 設 `null`，`current` 明列 `source: null` 並改註為一般物理敘述；把舊 ABC 的 `source: 6` 與 URL 搬進 `historical` 或 `prior_source` 子欄，保留舊 `NOT FOUND` 判定原文。新 `tszs` 行、章稿 `n14`、27 條對位、全部旁白／prompt／series 均不改；builder 應只容許這筆 provenance 結構與相應 source-map／manifest 雜湊改動，且仍標 `PENDING`。

## 結論與下一關

**PASS_DELTA_ONLY_WITH_METADATA_HOLD**：三句縮限與兩個示意 prompt 在所列原始來源範圍內，候選產物與 manifest／delta 對位，未見旁支改動；`n14` 的歷史／現行來源標記尚須消歧。此結論不替 108 句精確整稿、聽感、真實敘事 panel、TTS 片長、MiniMax 圖像或成片播放背書。round9 `chapters_link`、`payoffs`、`one_thread` 的歷史 FAIL 仍有效。不可據此寫正式 `story/reviews/script-review.json`、安裝主機稿或啟動付費製作。
