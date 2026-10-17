# B18 Route B：保留第三版 T06 說法的 row10b 候選

**狀態：HOLD。** 這是隔離的離線企劃列，沒有取代 active、既有審查收據或工人章稿。它固定受審第三版全文，尤其 T04 口播「發明協會記錄」後場直線送盤，而 T06 只口播盤色與價格變化，不唸資料來源名稱。

前一個 `../B18-route-b-row10-candidate-20261017/` 雖通過 10 筆 `must_verify` 的 schema，卻把後場送盤與盤色定價合入同一個 `attributed:true` fact 9。正式工人會要求 T06 也口播來源，與受審稿相衝突。本候選保持 fact 9 原文不動；只將[法院判決](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf) P8 L476–495 的 1967 年授權展店加進既有法院 fact 4，連同 P10 L574–578 的第 579776 號權利 1972 年期滿，限定為一條法律史時間線。

[發明協會沿革](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)的盤色或裝飾分價則只進來源 `[2].supports`。`routing-amendment.json` 指定將來 T06 的 `t18` 用獨立逐景主張、來源 `[2]` 與不朗讀的來源字卡表達，`fact:null`；此檔只是未實作的路由指示，舊 85 景／65 筆 `UNCHECKED` 主張位元組未動。舊 Route B 12-fact 設計中的 fact 10、11 不建立；`t3` 將來轉到 fact 4。新的 row reviewer-only 名單仍應是 `[4]`，但必須針對此 row 的新 canonical story SHA 重審。

**順序要求：** 正式重寫 `turn` 章時，先把 `t18` 存成 `scene=turn-s088, source=2, fact=null, verdict=UNCHECKED`，並安排不朗讀的原生來源字卡，之後才交給 verifier。`story.mjs` 的 `checkedRows` 對 verifier 回傳的 `fact:null` 會退回上一版 `fact:7`，因此只在 verifier 答案裡改成 null 無效。verifier 後要讀回已存章稿，確認 `t18.fact` 仍是 null、來源卡確實存在且沒有進口播；目前這些關卡全未完成。

`build.mjs` 只把父版 row 的開場、轉折、法院 fact 4，以及來源 `[2]`／`[3]` 的 supports 共五個文字欄位改寫；會對照原 85 景 SHA、65 筆 claim 的 `UNCHECKED` 狀態、目前 `storyProblems` schema 和舊審查失效情況，產生 delta、verification 與 SHA manifest。獨立來源審查、正式 85 景與第三版全文對位、所有主張查核、TTS 片長、媒體與站主看片都尚未完成。此候選沒有主機寫入、付費、匯入或發布授權。

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-route-b-row10b-candidate-20261017/build.mjs --check
```
