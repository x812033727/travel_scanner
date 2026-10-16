# B18 史料約束修訂候選（2026-10-16）

**狀態：離線修稿，整片 HOLD。** 本包只新增獨立候選；沒有改原六章、65 筆[獨立稽核](../B18-fact-audit-candidate-20261016/README.md)、已匯入的 B18 企劃或正式主機。沒有模型、圖片、語音、媒體、付費、上傳、審稿收據。`series.json` 是**尚未採用的企劃修訂提案**，不能把原企劃核准移植到它。

本稿保留「工廠送瓶 → 小店送盤 → 轉角難題 → 首店與萬博 → 更多店各自改良 → 今日」這條故事線。鉤子的第三問仍在後段回收，但不再把 1978 年說成原始餐台實用新案的到期日，也不把市場成長歸因於單一年份。`turn` 章把權利期滿放在設備整合之前，避免 1974 年講完再倒回 1972 年。其餘章節沿用原候選，`origin` 僅修一筆來源索引。

## 來源到主張的差異

| 原主張／位置 | 可直接核對的來源 | 候選處理與保留界線 |
| --- | --- | --- |
| `H02-4`、`T02-1`：1978 年原始餐台權利期滿 | [日本法院判決理由 PDF](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf) P8 L466–469 認定第 579776 號於 1962 年登錄；P10 L574–578 認定**1972 年**期滿。[J-Net21](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)與[發明協會](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)回顧寫 1978。 | 鉤子拿掉年份；`turn-s078` 以法院認定的 1972 年說**這一項**權利。1978 所指是否另一權利仍未釐清，不能外推「所有權利」的到期日。卡片與共圖提示也改掉舊年。 |
| `T02-2`：1978 後大批新業者才進場 | 同一[法院判決理由](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf) P10 L574–578 認定 1972 年基本權利期滿後，已有與元祿無關的公司經營。 | `turn-s079` 只講法院已認定的「此後」與獨立業者；不說某一年一夕打開市場，也不斷言權利到期是唯一原因。 |
| `T02-3`：原加盟店獨立被接在 1978 因果後 | [J-Net21](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)「市場規模は7500億円に」段有獨立掛牌的報導；法院另有自己的權利與品牌關係記載。 | 移到獨立一句 `turn-s080`，明說是另份報導，不替它指定 1972／1978 年或法律因果。 |
| `E03-1`：1960 年道頓堀「第二店」 | [J-Net21](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)「町工場の経営者が協力」說 1960；[法院判決理由](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf) P8 L470–474 記原告道頓堀店 1962 年 4 月。 | `engine-s048` 只說後來在道頓堀展店；旁白與圖像提示拿掉確定年份及第幾店。不同店址／法人是否能解釋歧異，仍待同期材料。 |
| `O04-2`：循環吧台原來源索引不對 | [J-Net21](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)「ビール工場のベルトコンベア」段明寫繞吧台設想。 | `o11` 來源由發明協會索引 2 改為 J-Net21 索引 0；旁白不變。 |
| `E03-3`、`E05-4`、`T01a-1`：翻譯名、博志在場、給茶年份 | [法院判決](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf)的日文權利名、[J-Net21](https://j-net21.smrj.go.jp/special/expo1970/20231113.html)的備料回憶與[發明協會](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)的設備沿革；其他版本見原稽核。 | 名稱改成「日文名稱的直譯」；萬博只引備料回憶，拿掉他確定暑假在場；給茶裝置不說有歧異的 1971 年，保留另有來源的 1974 年整合。 |

原 65 筆主張的 worker verdict **全仍是 `UNCHECKED`**。在候選 `series.json`，原索引 3 的 Wikipedia 被法院官方 PDF 取代；索引 0、2 回顧文獻所說的 1978 明標「版本紀錄」。若要交工人，必須先重新核准這份企劃與 source index，讓逐章查核實際讀到法院判決；工人對 PDF 的 fallback 文字不等於親自查過判決。

## 檔案與檢查

- [READABLE-SCRIPT.md](READABLE-SCRIPT.md)：新順序的六章逐鏡旁白；`idea` 與 `now` 直接引用原章。
- [series.json](series.json)：未採用的來源與企劃提案；[chapters/](chapters/) 僅有改動的 `hook`、`origin`、`engine`、`turn` 四章。
- [delta.json](delta.json)：逐句、主張、卡片／圖像提示與場景順序的前後值，以及八個來源檔 SHA-256。
- [verification.json](verification.json)、[lint-warnings.json](lint-warnings.json)：離線官方合稿/lint/cute 檢查摘要與原樣警告。`build.mjs` 僅讀取凍結原件，在系統暫存資料夾做本機 lint，結束後刪除暫存；不呼叫網路。

```powershell
node docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/B18-source-bound-revision-candidate-20261016/build.mjs --check
```

本機重建：96 鏡、99 行、65 筆 `UNCHECKED`，插畫 77/96（80.21%）；官方 lint 與可愛畫風檢查均 **0 errors**，30 條 warning 保留。預估正文 **644.7 秒**，只是文字與鏡頭計算，沒有 TTS 實測；含片頭片尾約 670.7 秒，也未證成「約 10 分鐘」成片或聲音品質。尤其 3 段 open-loop 間距警告、結尾近似畫面、title 卡手機可讀性與實際敘事吸引力仍需審。原六章候選的 parser/title 卡限制也未解除。

下一步是**獨立審核本次變動與其凍結 SHA**，處理剩餘來源歧異，然後讓真正 worker 依新企劃做逐章 checker、listener、敘事盲審與劇本審查。這些關卡及正式主機 A01/B18 付費製作均未由本包啟動。
