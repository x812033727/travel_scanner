# S53 R47｜`s53036` 原版申請單畫面付費前獨立預檢

2026-10-22 UTC。**PAPER HOLD，僅針對尚未開畫的原版 `s53036` prompt 與 claims 畫面敘述。** 本審只讀固定史料、現稿與私人媒體快照；沒有修改影片、claims、音訊、manifest、帳本，也沒有呼叫圖片或 judge。R4 [作者凍結記錄](r4-author-freeze.md)已明記刪除原 `s53035` 的完整分配名冊岔題；現行 124 景中 `s53034` 之後的下一景是 **`s53036`**，不可把舊 ID 當成待畫鏡頭。

| 固定輸入 | SHA-256 |
| --- | --- |
| 現行 `video.json` | `1e16b8aaf5718f0df251947136df7e51ca3032346280703c6061feeae381f91d` |
| 現行已按 `s53034` 入選圖修正的 `claims.md` | `05cf94f523ccdcd825ceb7dc78b0c5b61945f0bd3d4367a00364fe095dba50aa` |
| `script.md` | `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc` |
| 固定 1913 年 *San Francisco Relief Survey* 本機原文 | `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72` |
| [R43 同類申請單預檢 HOLD](r43-s53032-unchanged-application-slip-preflight.md) | `689916c99500a516ee57b279b837cd70708c5c581771dba552e76fbf4e1fe087` |

現行 `s53036` 台詞逐字是「也有沒被燒毀住處、卻需要改善住房的人領到小屋。」；原 prompt 逐字是 `Wide shot inside a cramped 1906 room, an anonymous adult studies a blank cottage application while seated near a plain bed, diffuse morning light`。claims 同列僅寫「未燒毀原屋但需要改善住所者亦得小屋」。固定 [Survey E L4887–4897](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4887-L4897) 說 `Some who had not been burned out, but needed to be better housed, received cottages and moved them for permanent use to lots which they owned or leased.` 這直接支持有人即使未被燒毀住處仍領到小屋；它**沒有**記此人填／看申請單、書面申請程序、申請文件外觀或具體受配日期。下一句 `s53037` 才講其中有人把屋搬往自有或承租地，本審不將地塊動作提前塞入 `s53036`。

原畫面的中心動作是研究 `blank cottage application`，容易把未見於此段史料的申請程序誤作這群住戶領屋的方式；它也沒有畫出已領到的小屋。即使文件沒有文字，作為**主要動作**仍可能誤導。這與 [R43 `s53032` 的先例](r43-s53032-unchanged-application-slip-preflight.md)一致：兩張空白申請單作為焦點時也在付費前 HOLD，而非等機器出圖後才據圖臆測。`anonymous adult` 雖指定 adult，但缺灰髮、面紋和成人肩背等足以降低本集多次童貌退件風險的可見線索。此 HOLD 是來源與畫面風險的**開畫前**判斷，不是對已產生圖像的 HUMAN REJECT。

建議只窄修尚未開畫的 `s53036` prompt／claims 同列：1906 年一位銀灰髮、有面紋、成人身形的匿名住戶站在**一棟**低矮完工的救濟木屋旁；後方僅以簡單、完整但擁擠的舊住處暗示「原屋未燒毀、仍需改善住房」，不畫可讀文件、空白申請單、鑰匙、名冊、正式隊列或交屋儀式。畫面應維持原創概念，不聲稱該人物／房屋是調查指認的個案、真實受配程序、具體日期，也不暗示所有未被燒毀住處的居民都領屋。保留固定來源、台詞與其他 123 景；新稿須有精確可逆差分、不同作者按新 hash 的紙審、STOP 下安全回綁與即時模型／額度／集上限／單景 dry-run，才可考慮最多第一張一圖一審。

只讀核對時私人有效 `keyframes/manifest.json` SHA **`116b28ed12436e90f4fe1f16300ed670372691df94325ec7326556087512532d`**，`visual_hash=12d4b1dcd57ea4c0`，**22 KEEP**；22 張所選 JPEG 實檔 SHA 均對、judge PASS 且無 needs-review，`s53036` 未入選。contact sheet SHA `50d9bbd8f253f4e1dc1615e80e6671a62a6696d2570731227bd09eab427a74ea`。STOP 在位；jobs SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3` 且 `{}`。ledger SHA `ca3c43a1e588bc38daa689a3044a4983a42412459b57fbdec71e475375c032d0`，真實已付 **US$0.7695／58 images／57 judges／0 reservations**，低於已核准的整集 US$4.78 上限。本審**不**放行 `s53036` 原提示的任何付費媒體。
