# A01 round19 整稿獨立複核 — 離線編輯 PASS／正式審核待跑

日期：2026-10-17（台北）。我依 `origin/main` `e3723862afa52598a93efe9ba3edb3841b95fa75` 的 13 題敘事規則，沿用已逐字讀完的 [round17／18 六章 108 句整稿審查](../A01-round17-source-bound-candidate/independent-full-script-review-20261017.md)，獨立比對 round18 → round19 所有章檔、企劃與來源表，再重讀受影響的 `origin` 開頭、前後鉤子及片尾。本報告是**離線人工編輯判讀**，不是工人 verifier、listener、盲讀 narrative panel，也不是正式機 `story/reviews/script-review.json`。

## 精確版本與差異

| 內容 | 本機重算 SHA-256 |
| --- | --- |
| round18 基底 `manifest.json` | `df5908caec1b88147b19a50b42ea992f88388750eecf4ffd681cb394707d60da` |
| round19 `delta.json` | `8d9ded432ebb705b04a078fc29450f172d207597db4fc4f2b56bab2d3902c47f` |
| round19 `manifest.json` | `a8bd87c659f536b92acd7563ba89c34912802dbf73e6b48717edb0d7e5a44469` |
| round19 `candidate/chapters/origin.json` | `0686434d49bdc076445b30a9f2daf90a34f44bf396ba193649d97abaa1a32589` |
| round19 `source-map.json` | `352b056e5a9c516ac1c89c9d2f74a53c9b6f1e7f730ec247514fc099a28cd19a` |
| round19 `validation.json` | `63869d1a48ecab7a4692e558fb985aa4f43b287cd8d5f3c5a88d8e7966f3ff14` |
| round19 manifest 所綁旁白 | `af2ff39f523bcbd029e79f4ab2a4d84698c6ed4600ae8c22d9bb9ffcb80879f4` |

我用逐行差異另核一次：`origin.json` 只改 `origin-01/zc7k.text` 和 `o22.claim`，兩處都從「據館方記載，**1928 年**安妮塔……」變成「據館方記載，安妮塔……」；`source-map.json` 只改 active `zc7k.text` 同一句。舊 `previous_text` 是歷史紀錄，原封保留。`hook`、`idea`、`engine`、`turn`、`now` 五章及 `candidate/series.json` 與 round18 各自逐檔 SHA 相同；全部畫面、場景順序、其餘 107 句旁白、`loops` 和片尾亦相同。

`node build.mjs --check` 退出碼 0：**79 景／108 句、旁白變更 1 句、active 來源行變更 1 筆、lint 0 error／40 warning、cute-story 0 error**。這只證明候選檔的機械一致性，不能替正式審稿。

## 受影響段落與來源綁定

新的連續旁白是 `origin/r12o01`「**1928 年出發前**，安妮塔問……」→ `csdd` 兒子裝舊嬰兒車兩輪 → `9ij6` 裝伸縮木把手 → `zc7k`「據館方記載，**安妮塔拉著兒子做的輪子箱出發**；它仍是一家人的自製品。」→ `6b28` 一家六口展開第二次環遊世界。聽眾仍從第一句知道出發年份，第四句不再近距離重唸同一年；「發問、造箱、出發」的因果次序、開場 `p5hs/y9b6` 的預告及 `origin/83ew` 的館藏回答均未變。

我獨立核對 `o22.claim` 與 `zc7k.text` 和旁白逐字一致，仍標 `PENDING`／`PENDING_INDEPENDENT_REVIEW`、`source=8`／`source_index=8`、`fact=5`／`fact_index=5`；未擅改舊判定。`series.plan.must_verify[5]`、`series.plan.sources[8].supports` 與 `origin.point` 仍載有 1928 年出發、兒子以舊嬰兒車輪造箱和不據館藏圖說推定製作年。此次另讀[溫尼特卡歷史學會的原始館方文章搜尋索引](https://www.winnetkahistory.org/gazette/before-her-time-anita-willets-burnhams-rolling-suitcase/)：它記第二次旅程為 1928–1930、旅前發問、兒子造箱及家人帶輪子箱旅行。新句有來源；索引與稿件都不證明館藏物件就是那次旅程畫面裡同一只。館方頁直接開啟曾逾時，本次所見是該官方頁的搜尋索引全文；沒有稱已核對 1933 年原書。

## 13 題敘事規則的本地判讀

| 題目 | 本地判讀與精確旁白依據 |
| --- | --- |
| `scene_first` | **是**。`hook/3rdw→e37u→avqs→wibh` 立即落在波多黎各機場的提箱與工人推重機器。 |
| `no_spoiler` | **是**。`p5hs/y9b6`、`47gq/b6mn`、`jtmg/x7r4` 預告後續三個時刻，未說出館藏、Macy's 進貨或車庫改造的結果。 |
| `one_line` | **是**。片頭預告後正文按 1928 `r12o01`、1943 `heut`、1970 `dgbq/76ur`、1987 `3zwf`、1997／2000 `7asx/5tik` 前進；沒有回頭重講同一事件。 |
| `no_toc` | **是**。`x7r4`、`rpvf`、`rs29` 是事件疑問，不是章節清單或「接下來要講」的宣告。 |
| `chapters_link` | **是**。`hook/x7r4→origin/r12o01` 回到先前同一個搬運難題；其餘 `origin/zaky→idea/j9sw`、`idea/rpvf→engine/3d52`、`engine/rs29→turn/5wnh`、`turn/4e5m→now/7asx` 都讓上一章的動作或疑問直接接到新事實。 |
| `open_loops` | **估算支持**。六章 `loops` 未改：開場有 `6h2q/y9b6/b6mn/emju/jtmg/x7r4`，正文還有 `dkkz/eghq/rpvf/rs29/b7mz/4e5m/kkjv`；文字檢查沒有 90 秒缺口提示。實際秒數須由 TTS 和正式 panel 核對。 |
| `payoffs` | **是**。跨段 `6h2q→3zkh/idiy`、`y9b6→83ew`、`b6mn/emju→8n2r/76ur`、`jtmg→9dkc/3zwf`、`x7r4→g5b8` 均有點名或具體新答案；相鄰的 `rpvf→3d52`、`rs29→5wnh`、`4e5m→7asx` 可直接答，無需硬插回呼。 |
| `no_recap` | **是，原窄修已解除**。`r12o01` 留下唯一正文「1928 年」，`zc7k` 改成只說出發行動。驗證仍提示 `1970` 三次，但 `47gq` 是片頭百貨預告、`dgbq` 是 2 月專利申請、`amrq` 是 10 月展示，分別是不同事件與月份，沒有把同一事實重述三遍。 |
| `chapters_are_events` | **是**。如「樣品被退回後拿到訂單」「機師把推車和箱子合在一起」，章名描述發生的事。 |
| `outro_no_next` | **是**。`now/g5b8→xjmb→ek2s` 回答、邀留言、邀訂閱，未口播下一支影片。 |
| `opening_hooks` | **是**。首場後有 1928 家庭、1970 採購、1987 車庫等至少三個結果留白的具體預告。 |
| `one_thread` | **是**。從 Anita 的自製輪子箱、Sadow 的貨架、Plath 的拉法到 Samsonite 的轉向，始終追「行李如何買得到且帶得順手」；`origin/nzyh/dkkz`、`engine/w9bj/rs29` 明說上一種做法尚有什麼難處，且未虛構發明者間的直接傳承。 |
| `no_detour` | **是，仍待真實聽眾檢驗**。專利結構段 `engine/r12e03→r12e07` 與 `turn/r12t04→r12t08` 在解釋如何拖、提、站立與轉向，尚未脫離主線；但若真圖無法清楚呈現，仍有像念零件的聽感風險。 |

這些「是」是審查者讀稿判斷，沒有執行正式盲讀 panel，不能偽作工人驗收結果。round9 的 `chapters_link`／`payoffs`／`one_thread` 三項歷史 FAIL 未被覆寫。

## 剩餘非稿件關卡

[round18 `n14` 來源中繼資料獨立複核](../A01-round18-n14-provenance-candidate/independent-review-20261017.md)已對其**局部差異**給 `PASS_METADATA_DELTA_ONLY`，本輪繼承且未再更動；來源表其餘 active 列仍保持原先待真實 verifier 的狀態。標題「有了輪子，為什麼還等了這麼久？」只宜配這支實際能證成的自製品、零售拒絕與用法改良，不宜在文案擴寫成對 1928–1970 整段時間差的單一成因。機械估計開場約 62 秒，全文 650.93 秒（250 units/min）或 556.1 秒（300 units/min）；都是文字估算，不是實際 TTS。約 10 分鐘、第一段濃縮、MiniMax 插圖與成片聽感仍須以真實媒體檢查。

**結論：PASS_OFFLINE_EDITORIAL_FOR_EXACT_ROUND19**。目前沒有再找到需修改這 108 句旁白的確定性編輯阻擋；這個 PASS 只限本報告所綁的 round19 精確檔案和來源陳述。正式 verifier、listener、盲讀 narrative panel、對正式機實稿的審核收據、TTS／圖像／成片檢查均未完成；不得憑本報告安裝主機稿、啟動付費製作或上傳 YouTube。
