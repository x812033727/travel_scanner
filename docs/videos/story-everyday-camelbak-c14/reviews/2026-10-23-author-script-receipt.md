# C14 CamelBak｜作者 v6 O02 窄修收據（待獨立覆核）

- 日期：2026-10-23（台北時間）；作者：`codex-c14-script`；去向：[draft PR #1695](https://github.com/x812033727/travel_scanner/pull/1695)。
- 站主已採用 [Treatment](../treatment.md) SHA-256 `078DC1D77C46EB49BB6F27F60535F22775781E5963783BDA7C1F7625B1A8700E`、[來源矩陣](../source-matrix.md) SHA-256 `F8CF68AA36264DF18CDBE6ECD698D4AF1F22E405DEAADA8ED275B7685050587E`；本輪重驗且未改其位元組。
- v5 [獨立逐句與逐鏡 HOLD](independent-v5-source-visual-review.md) 綁前版四個 SHA；本收據只是原作者對唯一 O02 HOLD 的修稿，不轉簽任何來源、畫面、純旁白或站主 PASS。

## v6 作者檔案 SHA-256

| 作者檔案 | SHA-256 |
| --- | --- |
| [`script.md`](../script.md) | `A513041C93AD462CF4480B82EC420DDA8E3D0F8745DF0DE92D9F833DEDF67126` |
| [`script-source-notes.md`](../script-source-notes.md) | `02F00FF7A568E381BEA54950F1FEBADF783ED913469D2525F7EC40298F29EF84` |
| [`visual-plan.md`](../visual-plan.md) | `2E7FEFFBE350F9DF46386552DD50E0C82CB8D45C83A60DF700FE2247D1E1CF83` |
| [`visual-plan.json`](../visual-plan.json) | `C4D70878DEEC5911A75AC584B70E6870268B45665757D54A1E9335D4F7323715` |

## 唯一故事變動與來源界線

v5 O02 把「車架上的瓶子還在」放進 Eidson 那次騎乘，[地區品牌回顧](https://camelbak.co.nz/pages/about-us)未記這個現場細節；Fawcett [US5085349A](https://patents.google.com/patent/US5085349A/en)只支持騎車取瓶的一般難題。v6 O02 改為「那次騎乘，他的第一步，是讓水跟著身體一起移動。」並只引 S2／M02；配鏡改為匿名騎士背上布套與封口水袋的**概念圖**，不再放車架瓶。H01 仍是泛用車架瓶場景，不當作那次騎乘的畫面證據。v5 對比證實 **74 句只變 O02、74 鏡只變 O02**；其他口播和鏡頭方向未改。

## 機械檢查與停線

- 74 個唯一口播 ID 對 74 個同序 JSON 鏡頭；每句 S 原件代碼存在；O02 鏡頭依 23 個口播字元重算為 5.5 秒。正文 **2,336 字元／1,911 漢字、紙上 560.8 秒**；加開場後 5 秒片頭與 21 秒 v4 片尾為 **586.8 秒（約 9:47）**。**沒有 TTS，實際正文 ≥480 秒尚未證實。**
- 58 幅概念插圖／16 張後製字卡；規劃插圖 **426.7／560.8 秒＝76.09%**，最長連卡 2，最長單鏡 **T16 11.3 秒**。只算新「鉤」而排除「回收鉤」，依鏡頭終點並計入 5 秒片頭，最長間隔 **T18→N05 41.1 秒**。這些不代表獨立敘事或成片圖片 PASS。
- `git diff --check` 與作者逐 ID、秒數、來源代碼、look 欄位、禁項、圖時比例及節拍機械檢查 exit 0。`npm run check:tasks` exit 1，錯誤仍是兩份既存未追蹤的 v4 獨立覆核 task 同 ID（`tasks/done/...` 與 `tasks/open/...`）；本作者未編輯、暫存或刪除它們。

請另一位代理依以上**四個 v6 SHA**重查 O02、相鄰 H01／O03 與 O02 鏡頭，再交兩位未讀本版的讀者純旁白盲讀。其後仍須自然語速 TTS、生成圖片逐張驗收、站主採用稿與分鏡及付費前整集報價。此輪沒有付費、匯入、上傳、合併、發布或部署。