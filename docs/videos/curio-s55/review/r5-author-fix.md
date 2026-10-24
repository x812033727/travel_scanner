# S55 R5｜作者窄幅修正與精確凍結

2026-10-20 UTC。R4 [獨立來源與書面畫面覆核](r4-source-independent.md) 判 **HOLD**，指出 `s55032`–`s55033` 把 [F 165–173](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L165-L173) 未指名說話者的被動推測歸給富蘭克林。以下是作者修正，**不是獨立來源 PASS 或敘事盲評**。

## R5 五檔 SHA-256

| 檔案 | SHA-256 |
| --- | --- |
| `research.md` | `b30ea8f4021ebb27fc2f2b8f63c633e4dde00c5fcb52241daa3aa1fb18af371c` |
| `brief.md` | `e603fdcccf91d884b71cf073005299bcf97dfa8b8cd4a35a44a9b8ea46a28f77` |
| `video.json` | `4964298ad28fd5daeca1b1a71dbdc0a6cccbe4010bfcff053e0b171b1e4270df` |
| `script.md` | `323ed25718b4f20d1fa5dd8fa9311d7afe1810b5418e1615688528510c9fcd21` |
| `claims.md` | `677fa4c37b555c6ea4862678c3ec8296c5e283bcdc626e7a73e91cab86c0af17` |

`research.md`、`brief.md` 與 R4 同 SHA；其餘三檔在此輪更動。來源網址及固定行號未改。

## 精確改動

- `s55032` 旁白改為「傳回的消息說球身破裂；**信裡記下一種推測：內部氣體膨脹**。」；`s55033` 改為「**這不是已查明的原因**；落地時富蘭克林本人不在那裡。」不再把無署名推測指給他本人，仍交代隔天傳回的落地消息與他不在場。`claims.md` 的兩列同步，並寫明被動推測未署名、破球只畫在分隔的回報插圖。
- `s55125`／`s55126` 共用的分鏡提示詞由巴黎上空乘員視角改成獨立的**象徵性機制示意**：泛指的乘員在沒有標定地點的畫面裡投稻草。`claims.md` 同步說明可投料只是操作機制，不表示富蘭克林目擊這次自由飛行的具體投料。
- 用 `node tools/video/cli.mjs script --slug curio-s55` 從 `video.json` 重生 `script.md`。章節、開場、片尾、句序、縮圖、來源欄、loop 和說明文字均未改。

## 作者機械檢查及交接

`VIDEO_WORKDIR=/tmp/curio-s55-r5-author node tools/video/cli.mjs lint --slug curio-s55 --json`：**0 errors、0 warnings**，工具估全稿 13.888 分鐘。`video.json` 有 135 個 `shot`、145 句正文及開場、2 句片尾；`claims.md` 的 145 列 ID／旁白與 JSON 同序同文，`script.md` 的 147 句與 JSON 同序同文。159 個逐句固定行號連結仍在；14 個 loop 端點存在且先後正確。最速 325 漢字／分鐘估開場 **175 字、32.31 秒**，其後正文 **2668 字、8.21 分鐘**。`git diff --check` 退出 0。這些是文字估算，實際配音時長仍待量測。

請另一位工作者按上述 R5 SHA **獨立重查** F 的被動推測歸屬及 `s55125` 畫面界線，然後由兩位新讀者對 R5 劇本分別盲評。作者沒有對自己的修正做獨立來源或敘事 PASS；沒有開始付費配音、插圖、配樂或成片。
