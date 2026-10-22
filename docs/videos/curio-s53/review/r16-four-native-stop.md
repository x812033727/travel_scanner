# S53 R16｜四張原生圖逐張驗收與停線

2026-10-22 UTC。依 [非作者書面 PASS](r16-four-prompt-independent.md)，只對 `s53003/04/06/07` 各用 MiniMax `image-01` 畫一次、各做一次 judge，直接開 **1280×720 未裁切原 JPEG**，並對照裁邊所選版。[逐張清單](r16-four-native-inventory.json)列原圖、所選圖 SHA-256、分數、評審意見與人工理由。**`s53003/04/06` 人工 KEEP；`s53007` 人工 REJECT。**既有 `s53002/05` KEEP 的 manifest key 與所選圖 SHA 均未變；這是首章六張候選中的五張人工 KEEP，並非全章或全片分鏡通過。

| 景 | 原 JPEG SHA-256 | 機器／原圖人工判定 |
| --- | --- | --- |
| `s53003` | `878039a01f4d0138abeb4262205886e48ed0f99ad03c5ac59c15e9f03ade9d09` | 10/10 PASS／**KEEP**。灰髮皺紋成年人在低矮木屋門邊，木屋與淡天空保持平面卡通質感；無原 R15 的近照片背景或黑邊。 |
| `s53004` | `17c28641f67e3452e7a08a6255e502dc551da79982dd94d037eadd0adf7cfaa6` | 9.29/10 PASS／**KEEP**。銀髮年長女性、小繫口布袋和無字單頁；大眼是本系列 chibi 畫法，不再是 R15 的童貌髮髻、現代扣包或黑邊。袋子置於紙頁上緣而非側邊，沒有宣稱這是歷史付款原件。 |
| `s53006` | `b2fcb14c21a4a30ee04af788f6cda493074dda1cce35773eb4300eb9550e02a0` | 10/10 PASS／**KEEP**。灰髮皺紋成年職員手持一張無可讀文字的紙，桌側小布袋；不再是 R15 的童貌、雙份有橫線紙或現代文件櫃。紙頂細線不構成可辨識契約內容。 |
| `s53007` | `c887c568fe24e68d24cf49d3236efb9c1fd2b9ea254f703fe571ce00ced97623` | 9.29/10 machine PASS／**REJECT**。原圖上下有明顯黑色 letterbox；成人雖正確、袋子也已縮小，卻握在人物手中而非門檻，易把「誰付搬遷費」指向單一持袋者。所選裁邊圖消掉黑邊，但不能把原圖和動作瑕疵當作已驗收通過。 |

`video.json` 保持 R16 SHA-256 `817819fb64717fb3dc6e5bd1e1957a5e7d14d9f8fb455001ac0d4a609ee62f12`；旁白、史料、其他鏡頭和已收圖未改。執行只帶 `--shot s53003,s53004,s53006,s53007 --takes 1`，EXIT trap 已恢復 `STOP`。私有前後快照、原圖、裁圖、manifest、ledger 和命令 log 位於 `/workspace/.video-work/curio-s53/review/r16-four-pre/`、`r16-four-post/`、`r16-four-native.log`。帳本從 **US$0.1925／15 images／14 judges** 增為 **US$0.2465／19 images／18 judges**，恰增 US$0.0540，預約 0，低於整集 **US$4.78** 上限；當前 manifest SHA-256 `6d48e6c5b910da68847488ae58ff7a9b20f70a594ebfbeb7ab533728505a5f6f`、ledger SHA-256 `a9ba37fa4e5c06a6255c32653b5f0d1620ed79d5bed91773f1bb00a0dd03c7d4`。

`s53007` 已是 R14、R15、R16 三次原生嘗試及 R15、R16 兩輪提示詞修訂後仍退件；下一步按系列規則評估**同章已通過的畫面重用或一張來源合格資訊卡**，保留總插圖比率至少 70% 與卡片連續上限。`s53008/09` 及全片其餘插圖仍未畫；網站企劃／劇本／音訊卡、人耳、配樂、長短片與 Studio 連結仍待辦。
