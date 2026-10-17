# A01 round-9 敘事 FAIL → round20 離線稿的逐章接續候選

**狀態：OFFLINE_DIAGNOSTIC / HOLD。** 這份文件把正式機 round-9 的三項真實 FAIL 對到目前最小且已有獨立離線閱讀的文字候選。它不修改任何章稿、來源表、審核結果或正式機；沒有新一輪 verifier、listener 或盲讀敘事 panel。下文的「已修」只指離線候選的**文字設計**，不代表正式驗收通過。

## 精確輸入與核對

- 2026-10-17 唯讀擷取：`A01-20261017-095816-2a72b1e1`，摘要在 [A01-live-readback-20261017.md](../A01-live-readback-20261017.md)。擷取中的 `review/narrative.json` SHA-256 是 `dd458ee2b6eee90a3b358408c605620c108ca4387afb94249fd555abc01babab`，與保存的 [round-9 panel 原檔](../A01-round10-candidate/evidence/round9-narrative.json)相同；`round=9`、`passed=false`、失敗項目為 `chapters_link`、`payoffs`、`one_thread`。擷取的六個 `story/chapters/*.json` 也逐檔與 [round-9 保存稿](../A01-round10-candidate/source/chapters/) SHA-256 相同。原始擷取留在 Git 之外。
- 本機目前逐題規則來自 `tools/video/core/narrative.mjs`（本次讀取 SHA-256 `44687e2eb319119be7975fdba903afb41d2d00cdabe09449f430a6dddd5c88af`）。它明許預告式片頭之後回到更早的故事起點，也允許跨年代產品史沿著同一個**具體使用難題**推進；這兩處與 round-9 回答時看到的舊題目不同。這裡沒有核對正式機是否已部署相同程式位元組；規則更新也不能反過來改寫歷史 FAIL。
- 最新離線文字／來源中繼資料基準是 [round20 i17 候選](../A01-round20-i17-fact-index-candidate/README.md)，`manifest.json` SHA-256 `4d701779891e1076c3729788cc82165901d71140bfbd77c07fa9b1c060b32549`，合成旁白 SHA-256 `af2ff39f523bcbd029e79f4ab2a4d84698c6ed4600ae8c22d9bb9ffcb80879f4`。本次 `node build.mjs --check`：79 景、108 句、27 條 active source rows，exit 0；回報仍為 `HOLD_UNREVIEWED_OFFLINE_CANDIDATE`。round20 六章與 round19 逐位元組相同；[round19 整稿獨立閱讀](../A01-round19-origin-year-repeat-candidate/independent-full-script-review-20261017.md)只判離線敘事可讀，並未跑正式 panel。

## 三項 FAIL 的具體根源及最小對應

| 真實 round-9 結果 | 舊稿的具體閱讀問題 | 已存在的最小離線修正及其界線 |
| --- | --- | --- |
| `chapters_link=false`，panel 指向 `origin/zc7k` | 片頭在 Sadow 機場，下一章突然以「開場那一家人」帶到 1928 年，還先講一家人不必提箱子的結果。這使時間倒回的理由及「搬箱困難」的接法不夠清楚；`zc7k` 位於 `origin` 內，panel 證據本身不足以指認其他五個章首。 | round20 以 `origin/r12o01` 的 **1928 年出發前搬箱疑問**先接片頭 `hook/x7r4` 的「輪子為何還不足以進入日常」，之後才到兒子造箱與 `zc7k` 的出發行動。其餘四個正文邊界是 `origin/zaky→idea/j9sw`（推銷被拒）、`idea/rpvf→engine/3d52`（長路在航站）、`engine/rs29→turn/5wnh`（橫拖易翻）、`turn/4e5m→now/7asx`（直立四輪）。這是依新版規則的編輯判讀，仍待實際 panel 回答。 |
| `payoffs=false`，panel 指向 `idea/eghq` | `eghq` 是「顧客買不買帳？」的**設問**，不是答案；原回答無法單靠這一行定位所有失收的伏筆。舊 `hook/6h2q` 問一般重物差異，`hook/y9b6` 問「那只箱子」下落，可能暗示館藏物就是 1928 年旅程同一只；`hook/b6mn` 的 payoff 表錯落在早期拒絕 `idea/j9sw`，並未回答最終是否上架。 | round20 把 `6h2q` 縮成輪板辦法能否用在箱子，回收於 `origin/3zkh→idiy` 的四腳輪與繩帶；把 `y9b6` 縮成家族自製箱**有一只**是否保存，回收於 `origin/83ew`，不宣稱同一物件；把 `b6mn` 指到 `idea/76ur`，該句明說試走的副總裁要 Macy's 進貨。`idea/eghq→ys5y→quhs` 則只以 Sadow 回憶回答顧客反應，並承認沒有確切銷量；不可擴寫為已證銷售數字。這些對應由離線 reviewer 讀稿確認，不能據此覆寫 panel。 |
| `one_thread=false`，panel 指向 `now/7asx` | 舊題要求同一個人物／物件一路走到底；故事實際從 Anita 家庭、自製箱，跨 Sadow、Plath 到 Samsonite。`now/7asx` 以「有。1997 年，Samsonite……」換品牌，容易像另一個無關例子。不能為滿足舊題捏造不同發明人彼此承襲，或把多件行李說成同一只。 | 新版規則容許追同一具體難題：如何從**輪子能承重**，進到**店家肯賣、旅客能省力且帶得順手**。round20 `engine/w9bj→rs29` 說明橫拖的餘留難處，`turn/5wnh` 回答易翻與碰腳踝，`turn/4e5m→now/7asx` 由往後拉轉成站著推，`now/g5b8` 一次回收上架與用法。這是產品使用問題的連續性，並非任何人物或技術的直接傳承；正式 panel 必須讀精確新稿重新判定。 |

## 六章在畫面與敘述中的同一條線

| 章 | 必須讓觀眾看清的動作／問題 | 交給下一章的事 |
| --- | --- | --- |
| `hook` | Sadow 提箱，工人推輪板；再閃過家庭自製箱、百貨試走和機師車庫，各停在結果前。 | 有輪子，為何還難以走入旅客日常？ |
| `origin` | 1928 年的搬運疑問 → 家庭造箱；之後 Sadow 用四腳輪與繩帶做待售樣品。家庭箱和待售樣品須視覺上分開，不畫成同一只。 | 他帶樣品去百貨推銷，會被接納嗎？ |
| `idea` | 先拒、試走、決定進貨；以當事人回憶界定顧客反應，銷量未知。 | 專利指出旅客得自己走的一段路在哪裡？ |
| `engine` | 大型航站的自提長路，輪子讓箱子能橫放拖行，但這個拉法仍有問題。 | 為何常跑機場的人想再改？ |
| `turn` | 機組員遇到橫拖不便；機師改成直立兩輪與伸縮拉桿。1987 原型與後來專利圖不得視為同一份實測紀錄。 | 立起來後能否四輪站著推與轉向？ |
| `now` | 1997 的直立四輪、2000 的萬向四輪是後續產品例子；結尾回答上架與用法問題，也保留樓梯前仍須提起的限制。 | 完成片頭的主問題，不口播下一支影片。 |

**最小下一版文本決定：沿用 round20 的六章與來源表精確檔案，不再預先改字或改鏡。** 這版已包含可追來源的邊界、伏筆和使用難題修正，也有綁定同一旁白 SHA 的離線獨立整稿閱讀。若新的正式 panel 仍退回某一項，先保存它對**新輸入雜湊**的回答和逐行證據，再只對指出的章首、payoff 或畫面接縫開一個新候選並重做來源／整稿覆核。不要把上表當作新的審稿收據。

剩餘一處主觀風險是 `hook/x7r4→origin/r12o01` 的年代倒回：它能接上片頭的搬運難題，也符合現行規則允許預告後回到起點的文字；盲讀者是否仍覺得跳接，必須由對精確 round20 輸入的新 panel 說明。現有證據不足以在送審前再改已獨立讀過的六章。

## 接續關卡

正式機現有 80 事件稽核鏈的來源 composite 與目前共用 lexicon 不符；另有一筆 `uncertain` stage job。舊的 81 事件提案綁另一個 lexicon SHA，不能直接套在 2026-10-17 擷取。要先由另案完成精確來源過渡、共用寫入鎖與雙掛載回復設計、主機實況與工作／預算前檢，才可談採用 round20。採用後仍須真實 worker 逐章 verifier／listener、盲讀 panel、綁精確稿的 `story/reviews/script-review.json`、實測 TTS、真圖及成片觀看。這份離線診斷不授權主機寫入、付費製作、匯入 B18／後五集或上傳 YouTube。
