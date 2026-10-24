# S49 R39｜`moon040–047` 下一組八景來源／畫面作者窄修

2026-10-22 UTC。**本輪只提出書面候選，須非作者逐景核來源與提示詞；沒有任何付費媒體或私人圖單重綁。**R38 `moon039` 來源卡及圖單已經紙審 PASS、離線重綁，現行 31 張 KEEP 不變。接著先核下一組八景，避免把 1859 重印本所記的 1835 **虛構報導**畫成真實望遠鏡工程、皇家學會館藏或財務紀錄。

固定 Locke 名下 [1859《The Moon Hoax》重印本 P05 L435–490](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L435-L490) SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654` 中的玻璃、皇家學會、七萬英鎊、鑄鏡、重量／直徑／倍數均是故事自身聲稱，不是發生紀錄。固定 [Jacoby 1902 評論 J4083–4125](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4083-L4125) SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029` 批評光學對話為 *imaginary* 與 *optical jargon*，不能拿它獨立驗證那個故事中的尺寸或資金。

| 景 | 來源／現稿處理 | 本輪畫面窄修 |
| --- | --- | --- |
| `moon040` | P05 故事說數週試驗及珠寶商櫥窗玻璃；旁白明用「又寫」。 | 成人、無字玻璃、假想 1830 年代工作室原提示不動；仍需原圖驗成年、年代及非真器材。 |
| `moon041` | P05 的假想焦像照明，加 J 的光學質疑；旁白是編輯說明，不宣稱真實實驗。 | 舊畫面人物把燈拿向窗外月亮，可能誤成燈能照月；改成年讀者指桌上無紋圓斑，油燈**只照桌面**，窗外月亮仍遠而暗，不畫光束或已運作的赫歇爾設備。 |
| `moon042` | P05 故事聲稱計畫提交皇家學會。 | 舊會議桌上透鏡圖易冒充館藏／會議；改一位成熟年代人物把**無字小提案紙**遞向畫外，不畫學會大廳、印鑑、存世設計圖或實物。claims 錯標「後出天文評論」改回虛構報導。 |
| `moon043` | P05 故事聲稱估價七萬英鎊、國王允款；非付款證據。 | 舊硬幣帳冊像真財務紀錄；改成熟年代讀者對一張無字提案頁的費用主張反應，不畫收據、付款或王室印鑑。 |
| `moon044` | P05 後段談鑄鏡，旁白問「紙上的鏡片」；已有假想年代工匠與空鑄模。 | 提示詞與 claims 不動；原圖仍須確認空模具與非完成實物。 |
| `moon045` | P05 故事說第一次鑄鏡失敗、第二次有兩處邊緣小瑕。 | 假想工匠看邊緣瑕疵的現稿不動；原圖仍須確認這只作報導插畫。 |
| `moon046` | 三項數量來自 P05 故事，J 只評論光學術語。 | 舊排字桌的**可讀數字鉛字**與透鏡圖會像 1835 原報；改成熟年代排字者排三塊無字木塊與無字圓形記號，僅作三項數據概念示意；claims 的數值來源只留 P05，說明 J 並非尺寸核證。 |
| `moon047` | P05 故事給 24 英尺口徑、14,826 磅近七噸。 | 三行字卡原文及台詞不動；claims 移除 J 的數值引用，明確說報紙聲稱、非真赫歇爾鏡片或 J 獨立查證。 |

[逐字可逆結構差分](r39-next-eight-visual-source-structured-diff.json) SHA-256 **`03d2e70e5b079936d5af8eeac108ab6e86c3aa3daeb38176c1b501a04901d64f`** 記錄 `moon041/042/043/046` 四個 `data.prompt` 舊／新值及五個 `claims.md` 行（含 `moon047`）；`after→before` 逐位元還原 Git `4c6c76c39` 的 `video.json` SHA `5d899f4e40c792761e9935345191af3f1f4637532a85c82b6f90e6be776c8d4c`、`claims.md` SHA `5bda4ed9c7b7242ae5b3ae3b34c94ed6f70f4b00b3dc6cc08c7a15dfaf9287bc`。現 `video.json` SHA **`a3baea2c12c8930690379a04c6d6f2707f68661e53a692f462134a9ee402706d`**、`claims.md` **`df770faf47821fefc2ee8d3b42b7fc91c808420b85f891714efbb44a07a7b111`**，新 `visual_hash=d85f16ad28e5b6c8`；`look_hash=98a370ae40badbaf`。其他 **125 景**完整物件、全部 **131 句**台詞、script SHA `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`、research SHA `f5da15ac571478389b9b9920832f79434f83af0d312cb84747dcdb680a667750` 未變。`moon040/044/045/047` 的完整 scene 物件不變，`moon047` 只清理 claims 來源及畫面說明。

CLI `lint --json` exit 0、**0 errors／0 warnings／131 lines**；`npm run test:docs-videos` **236／236 PASS**。只讀 `keyframes --dry-run --takes 1` 對下一組七個 `shot` 均 exit 0；四個新提示詞預算分別 `moon041` **436／1070**、`moon042` **400／1072**、`moon043` **343／1071**、`moon046` **409／1069** 字元；這不是圖片驗收或付費預檢。正文仍 **117／128 shot＝91.41% 插圖**、最多 **2** 連卡。沒有更改旁白、開頭片尾、Short 或輸出影片。

私人 active manifest **仍綁 R38** `visual_hash=c2f2beaa8befb76d`，SHA `6ff57bfb19e7c3be0ad77e02190026f53e20855bd7fdba926ef1c1210147f023`；31 張既收圖實檔仍需在獨立紙審重核。ledger SHA `b022285fdfdc39149d90579e612265235263893d6f5f3cca6321483df6f0b059`，**US$1.2015／89 image／89 judge／0 預約**，低於整集 US$5.30，STOP 在位、jobs 空。**由非作者逐景核 P05／J 的歸屬、八景提示詞、四景改動和 31 KEEP 後，才可安全離線重綁 R39；任一 HOLD 先修書面。**`moon040` 及後續付費原圖、完整 storyboard 均未放行。
