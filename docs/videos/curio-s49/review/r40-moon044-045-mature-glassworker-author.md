# S49 R40｜`moon044/045` 成年玻璃工匠作者窄修

2026-10-22 UTC。這是對 [R39 非作者下一組八景紙審](r39-next-eight-visual-source-independent-paper.md) SHA-256 `0450a229dc45e3df2eb2c4a403e6caaf23da49c194887157c8b816adf05ae18e` 的**兩景 HOLD 精確修復**，仍是作者書面候選，待另一位重核，沒有圖單重綁或付費媒體。R39 已認固定來源／八景主張 **8／8 PASS**，畫面 `moon040/041/042/043/046/047` **6／8 PASS**；`moon044/045` 只因原提示的 `one imagined 1830s glassworker` 未鎖成年外貌而 HOLD。S49 先前多次出現童貌工匠／讀者原圖，職業本身不足以表明年齡。

本輪只在這兩個原提示加「**明顯中年成人、灰鬢、成人面紋、寬肩、1830 年代樸素工作衣**」線索，同步照錄在 claims 同列畫面欄；其他字眼與聲音不動。

| 景 | 保留的單一動作／物件 | 明確退件風險 |
| --- | --- | --- |
| `moon044` | 一位想像中的 1830 年代工匠在柔和爐光下**檢查空圓形鑄模**；對應「紙上的鏡片究竟鑄出來了嗎？」 | 新原圖若仍像孩童，或把空模畫成實際完成的大鏡片，仍須 HUMAN REJECT。 |
| `moon045` | 一位想像中的 1830 年代工匠**檢查有兩處邊緣小瑕疵的普通大鏡片**；只示意虛構報導中的鑄鏡結果。 | 新原圖若童貌、鏡片瑕疵在中心、現代防護具或像存世真赫歇爾鏡片，仍須 HUMAN REJECT。 |

固定 Locke 名下 [1859《The Moon Hoax》重印本 P05](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L465-L490) SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654` 的鑄鏡與瑕疵全在**虛構報導**裡，並非史實工場或保存的鏡片；Jacoby 1902 評論 SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029` 沒有獨立核證鑄鏡。旁白已標「紙上的」「文章說」，未改。

[逐字可逆結構差分](r40-moon044-045-mature-glassworker-structured-diff.json) SHA-256 **`3f5eced82e96ae89f8820365c4ff539b036278987a3de22c686382c29c162331`** 只記 `scenes[40/41].data.prompt` 與 claims `moon044/045` 兩行的新／舊值；`after→before` 逐位元還原 Git `3c0696887` 的 R39 `video.json` SHA `a3baea2c12c8930690379a04c6d6f2707f68661e53a692f462134a9ee402706d`、`claims.md` SHA `df770faf47821fefc2ee8d3b42b7fc91c808420b85f891714efbb44a07a7b111`。現 `video.json` SHA **`7c793e461696644e78e9723e0a2103e40746bf5e0e51c7c587da080d427f5f75`**、`claims.md` **`93945e1368d357cd4baa178b156a46735f9de0d9b4ac6386c46f81eb60a023c4`**；其餘 **127 景**完整物件、全部 **131 句**台詞、`script.md` SHA `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`、`research.md` SHA `f5da15ac571478389b9b9920832f79434f83af0d312cb84747dcdb680a667750` 逐位元不變。新 `visual_hash=12f2aee4595df518`，`look_hash=98a370ae40badbaf` 不變。

CLI `lint --json` exit 0、**0 errors／0 warnings／131 lines**；只讀兩景 MiniMax `image-01` dry-run 提示詞各 **210／1068**、**233／1070** 字元，沒有圖片或費用。插圖仍 **117／128＝91.41%**、最多 2 連卡。私人 active manifest **仍綁 R38** `visual_hash=c2f2beaa8befb76d`，SHA `6ff57bfb19e7c3be0ad77e02190026f53e20855bd7fdba926ef1c1210147f023`；31 張 KEEP 及帳本 SHA `b022285fdfdc39149d90579e612265235263893d6f5f3cca6321483df6f0b059`（US$1.2015／89 image／89 judge／0 預約）未動，STOP 在位、jobs 空。**下一步另一位只核兩景成人線索、R39 其他六景／來源仍適用、精確差分、31 KEEP 與 STOP；全八景紙審通過後才可安全離線重綁 R40。**`moon040` 及後續付費原圖、完整 storyboard 仍 HOLD。
