# S54 R8｜固定來源與書面畫面獨立差分覆核

2026-10-20 UTC。**PASS：R8 新句的史料歸屬、主張錨點與書面畫面；147 景文字對齊 PASS。** 此結論僅對下列精確檔案有效。我沒有改作者稿件或購買媒體；正式新稿敘事盲讀、政策、實際圖片、語音和網站關卡另驗。R7 的 [獨立來源 PASS](r7-source-independent.md) 不能代替本次 R8 新句覆核。

| R8 輸入 | 獨立重算 SHA-256 |
| --- | --- |
| `research.md` | `47642150198fa8dcc9a9991a5be9497dfd1f0db4a3085ff3f7d74f7f53126336` |
| `brief.md` | `b10fa670558f3a0e6fb7296c77ee3979e7faf2d5f9ee22ac3b9172c5ba5b236d` |
| `claims.md` | `0b7d0c2817f57be52f2b05a16771a8984cdf308942f0114cffc8d2cce237eadd` |
| `video.json` | `100128600cbd4027bd2855fb904336fb12655bf203cd370c1a60d0bbcb508726` |
| `script.md` | `b9981a1b503504e48b452b2a37ddc42731ee7a4bcc6096dd6d7f79ec9d25438c` |

五檔與 [R8 作者凍結](../author-freeze-8.md) 逐位相同。`research.md` 亦與 R7 的 `47642150…` 完全相同。以 R7 的 150 句敘事 payload（本機 `/tmp/s54-r7-panel-a.json`，SHA-256 `5f57f7689f8c23f0a47e70ffb6b3f39ef4ae77cd161d1fb5a6b8e5f8dced913d`）按 line ID 對 R8 JSON 全部旁白，只有 `s54104` 和 `s54110` 兩句不同；`s54111` 未改，其 R7 答句由新版提問直接承接。這項逐句比較不宣稱擁有 R7 五檔的完整位元組快照；R8 其餘書面來源／畫面沿用既有 R7 覆核，新增部分如下直接重核。

## 固定原文與 R8 窄修

重新讀取本機固定來源全文並重算原始文字 SHA：A 1839 法案 OCR `/tmp/s54-butterworths-1839.txt` 為 `f19541ff9faab28b3d61739f09e23b40115fe2220eda870c2d7cd0867758e254`，其 Git blob `433e7fa217b90a06f21b491788fb4b08b0ecd487`；H 希爾第一卷 `/tmp/s54-review-hill/59390-0.txt` 為 `3bdf96943eea935aec86101874f15aa8f60d518db1437902da52b446f006f939`，repo HEAD `b508867f1e1390093789dd72b1d84bcd6bbdaa58`；L Leavitt `/tmp/s54-review-leavitt/27196-0.txt` 為 `cc4b05beb60da3f29bc3565b9bdcefa8a643bf972454c7c0a14690f5bdd49d5e`，repo HEAD `df94d1d290d2b99b1af422c3595438dea38fbdd8`。三者均符合 [research.md](../research.md) 固定版，沒有改用浮動網頁或另一版本。R8 新句只直接用到 H；A、L 的既有 R7 主張未改。

| 位置 | 固定原文對讀與畫面界線 | 判定 |
| --- | --- | --- |
| `s54103→104` | 早前 `s54024–29` 已交代希爾曾提背面塗膠的小紙片作例外辦法；[H L9627–9637](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L9627-L9637) 的 *bit of paper … glutinous wash* 與 *mere expedient for exceptional cases* 直接支持「備用的那片附膠紙」。[H L13139–13145](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13139-L13145) 說財政部採預付與**三種**郵票形式，票要等備妥才投入；新 claims 行把 P03 和可點的 P07／H L13138–13145 並列，兩段合起來足夠支持「現在窗口等的正是它」這個回呼。句子是把附膠紙作故事的具體答案，不能讀成它是唯一獲准形式，或一月已開賣／准用。新 prompt 是 *early 1840 planning office* 的職員比較**無字紙樣**與硬幣盤；沒有畫一月寄件人拿到成品、真 Penny Black 版面或可讀原件。 | **PASS** |
| `s54110→111` | R7 `s54110` 問「反對者究竟是誰」，H 未具名，因而 R8 改問「部門一開始怎麼看？」；下一句直接答「希爾記部門起初反對」。[H L13338–13341](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13338-L13341) 原文是 *Objection was raised in the department to the sale of stamps at the three Chief Offices*，並列倫敦、都柏林、愛丁堡；它沒有指認官員或更精確的部門名稱。新問答只要態度，不追索姓名，`s54112` 再列三處。claims 的 P09 直接指 H L13328–13353；相鄰 prompt 僅畫規劃室與三個無字托盤，沒有冒稱特定部門開會的歷史影像。 | **PASS** |

源文層級維持：H 是希爾後來出版、帶日記摘錄的當事人回顧，不是 1840 年郵局完整帳簿；`s54111` 保留「希爾記」。書面畫面是可愛概念插圖，並未畫成真實票樣、公文或當日照片。新 `s54104` 的「等」不可轉述為某一月窗口已有票，五月一日開售與五月六日准用仍在後文明分。

## 對齊與靜態檢查

當前 JSON 有 7 章、147 個編號場景（140 `shot`、7 `big`）、23 組 `loops`，另有片尾三句，合計 150 個唯一 line ID。`claims.md` **147/147** ID、次序、旁白同 JSON；`script.md` **150/150** 旁白同文同序；140/140 插圖行標明概念示意、7/7 字卡行標明工具排字卡，23/23 loop 起訖 ID 均存在。R8 的 `s54103→104` 與 `s54110→111` 在 JSON、claims 和 script 完全同字。

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s54 --json` 退出碼 0，**0 errors／0 warnings**；工具摘要為 150 lines、13.8922 分鐘書面估時。估時不是實際 TTS 長度。這份 PASS 不判新稿的正式十三題雙盲，也不放行付費圖、語音或成片。
