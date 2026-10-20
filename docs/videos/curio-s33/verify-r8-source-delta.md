# S33 R8 片尾政策修訂差分（作者自查）

2026-10-20 UTC。R7 站台實際核准的 `script.md` SHA-256 為 `3db98a782e552385def131784e1dc4c8096e2bceb36e10e58cb75a277e004815`；R8 的 `script.md` 為 `1a1d52712593055ed5d427696b273bdc7cf28de7736ef90c5ee98a0431a3556e`，`video.json` 為 `e0d7fed0c81ce7db2ff2a971e177d4fdef831d5bea5afe6523804f9d8ad965ae`，`claims.md` 為 `2f38d279e7eb2d6b34584c9ed853e3de1efd695a6d5a87921685d5c116e68fd0`。`brief.md` SHA-256 `b1cfc6aff2db4cf64a4f3e3fa1784d929d97f5a441ee23328101bf0c81f946a2` 未動。

R7 對精確劇本的一次 Jev 政策預檢為 **FAIL**：業配 0.36，高於 0.30；立場 0.82、建議 0.02。收據 [reviews/policy-r7.json](reviews/policy-r7.json)，請求 SHA-256 `47ca4d55bc089dcbc83ff73a346e679e8ff72188b1f857c1140e8986ed5cf76f`。此結果不能當作歷史句子不實；為免配音後才需重錄，只窄改片尾 `hj999c` 一句：

| R7 | R8 | 自查 |
| --- | --- | --- |
| 「想繼續從原文找歷史轉折，就訂閱奇聞檔案局。」 | 「本集《世宗實錄》原文的來源連結，放在說明欄。」 | `video.json.sources` 已列第三方保存之《世宗實錄》125、126、128 卷三個固定 commit URL；這是連結位置提示，沒有新增歷史斷言。片尾畫面 `cta` 的訂閱圖形未變。 |

以 `script --slug curio-s33` 由 R8 `video.json` 重新產生劇本，除 `hj999c` 外只有文末 narrative／speech 雜湊改變。`claims.md` 僅同步修正對該句的說明。R8 對新請求 SHA-256 `32719e2f706fae40ab354820d3bdacdfbcb0a6f57015801ab1956d42c0ccddb7` 的**一次** Jev 政策預檢為 **PASS**：立場 0.86、建議 0.01、業配 0.01；收據 [reviews/policy-r8.json](reviews/policy-r8.json)。`lint` 0 errors、4 warnings，第四項是片尾未口播訂閱字樣的提示，不是錯誤。

以上是作者差分自查，不代替另一人的來源／書面畫面核對與 R8 新版盲讀。R7 真實站台劇本核准綁舊雜湊，**不能**當作 R8 的站台核准；尚未對 R8 合成配音。
