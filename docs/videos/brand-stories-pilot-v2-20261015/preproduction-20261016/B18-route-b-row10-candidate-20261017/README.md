# B18 Route B：10 筆事實上限內的離線企劃列候選

**狀態：HOLD。** 這是獨立的新企劃列候選，不是 active、已審查 row、可匯入的 `stories.json` 或正式工人章稿。它保留受審第三版全文的 SHA，僅在父版 row 的六個位置做變更，並以原有 10 筆 `must_verify` 索引維持目前企劃 schema。父版 85 景與 65 筆 `UNCHECKED` 主張完全不動，尚未與此 row 對位。

原 Route B 設計 `../B18-fullscript-route-b-plan-20261017/route-b-plan.json` 將新史料放到 fact 10、盤色定價放到 fact 11。現有 `tools/video/story-plans/plan.mjs` 只允許 4–10 筆 `must_verify`，因此那種 12 筆 row 不能通過。此後繼方案把法院 [1967 年授權展店](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf)（PDF P8 L476–495）和同判決第 579776 號權利 [1972 年期滿](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf)（P10 L574–578）合入既有 reviewer-only fact 4 的法院時間線；把[發明協會沿革](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)的後場直線送盤、盤色或裝飾分價合入既有 fact 9 的後期經營方式。這兩項是**複合事實**，需要獨立審稿者判斷粒度是否足夠清楚，不能只靠 schema PASS 視為來源審查完成。

`routing-amendment.json` 精確覆蓋原設計中 `t3` 的 10→4、`t18` 的 11→9；新 row 的正式 reviewer-only 名單預定為 `[4]`，仍須以新的 story SHA 重新出具審查收據。舊 row 審查收據不再有效。既有 65 筆主張原樣固定，未被偷偷改成已查核或塞入新版章稿。85 景逐句對位、全部主張獨立查核、片長與實測 TTS、正式 worker reference、影片與站主看片仍待完成。此包沒有付費、主機寫入、匯入或發布權限。

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-route-b-row10-candidate-20261017/build.mjs --check
```
