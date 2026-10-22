# S49 R40｜`moon040–047` 來源與畫面非作者紙審

2026-10-22 UTC。**固定來源、八行主張、八景畫面提示詞：8／8 PAPER PASS。**我不是 R39 或 R40 作者；本結論只核這份凍結文字，不等於付費原圖、整集 storyboard、音訊或成片通過。沒有改動 `video.json`、`claims.md`、任務或私人圖單，也沒有製圖、judge、TTS、配樂、manifest 重綁或付費呼叫。

## 窄修與八景結論

[R39 非作者紙審](r39-next-eight-visual-source-independent-paper.md) SHA-256 `0450a229dc45e3df2eb2c4a403e6caaf23da49c194887157c8b816adf05ae18e` 已核固定來源與八行主張 8／8 PASS，畫面 `moon040/041/042/043/046/047` PASS，僅 `moon044/045` 因工匠未明示成人而 HOLD。我獨立對 Git `3c0696887` 逐景、逐行比對：那六個 scene 完整物件與 claims 完整行都**逐位元不變**，原判仍適用。`moon044/045` 的旁白與來源欄也不變。

| 景 | 本輪畫面判斷 |
| --- | --- |
| `moon040` | **PASS，承 R39**：成年年代技術員拿無字玻璃，數週試驗與櫥窗玻璃只歸虛構報導。 |
| `moon041` | **PASS，承 R39**：成熟讀者指桌上概念圓斑，油燈只照桌面；Jacoby 只支持光學對話荒謬，不核證器材。 |
| `moon042` | **PASS，承 R39**：成熟人物遞無字折紙，不偽裝成皇家學會存世提案或正式場地。 |
| `moon043` | **PASS，承 R39**：成熟讀者對報導費用作反應，不畫真實付款或王室文件。 |
| `moon044` | **PASS，修復 R39 HOLD**：提示詞與 claims 同列畫面欄逐字加入 `a visibly middle-aged adult with grey temples, lined face, broad adult shoulders and plain period work clothes`。保留一位**想像中的 1830 年代**工匠只檢查**空圓形鑄模**，柔和爐光；沒有把鑄模變成完成的真鏡片。成人面紋、灰鬢、成人肩寬及年代工作衣共同鎖定成熟外貌。 |
| `moon045` | **PASS，修復 R39 HOLD**：加入同一組成熟成人與年代衣著線索；保留一位工匠只檢查**有兩處邊緣小瑕疵**的普通大鏡片，柔和工場光。這是虛構報導的想像示意，不是存世赫歇爾鏡片。 |
| `moon046` | **PASS，承 R39**：成年排字者排三塊無字木塊，不偽造原報或讓 Jacoby 替數字背書。 |
| `moon047` | **PASS，承 R39**：「報紙聲稱／24 英尺鏡片／虛構器材數字」將尺寸鎖回報導。 |

我重讀 Locke 名下 1859 年《The Moon Hoax》重印本 `/tmp/s49-moon-hoax-62779.txt` SHA-256 `3ca0bc9b6fc5c50b090d61bf2049e925d22dd1cdef2b443a282f7fdc5749e654`：[P05 L435–489](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L435-L490) 寫數週試驗與珠寶店櫥窗玻璃、皇家學會提案、£70,000 與國王允款；首鑄失敗、再鑄近圓周**兩處**小瑕疵；二十四英尺、14,826 磅近七噸、42,000 倍。這些皆是**虛構報導內的說法**，不是工程、觀測或財務紀錄。Jacoby 1902 年評論 `/tmp/s49-jacoby-53396.txt` SHA-256 `f5ab32e64e7ea3735ff90fb000ae8cc82dddea594e0de0c6be30b30f94485029` [J4083–4125](https://github.com/GITenberg/Practical-Talks-by-an-Astronomer_53396/blob/073dd7dd24b8515dec681441a1cde79477fabf08/53396-0.txt#L4083-L4125) 稱光學對話為 *absurd imaginary conversation*，沒有獨立核證鑄鏡、數字或資金。兩句旁白原有「紙上的」「文章說」，來源界線未被本輪改動。

## 可逆性、工具及私人守衛

- 凍結 `video.json` SHA-256 **`7c793e461696644e78e9723e0a2103e40746bf5e0e51c7c587da080d427f5f75`**、`claims.md` **`93945e1368d357cd4baa178b156a46735f9de0d9b4ac6386c46f81eb60a023c4`**、[R40 結構差分](r40-moon044-045-mature-glassworker-structured-diff.json) **`3f5eced82e96ae89f8820365c4ff539b036278987a3de22c686382c29c162331`**。獨立用差分記載的兩個 `after→before` 原始位元組替換，精確還原 Git `3c0696887` 的 R39 `video.json` SHA `a3baea2c12c8930690379a04c6d6f2707f68661e53a692f462134a9ee402706d` 與 `claims.md` SHA `df770faf47821fefc2ee8d3b42b7fc91c808420b85f891714efbb44a07a7b111`。129 個 scene 僅 `scenes[40/41].data.prompt` 變，其他 127 個完整物件不變；claims 僅 `moon044/045` 兩行變。全部 131 句台詞不變；`script.md` SHA `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`、`research.md` SHA `f5da15ac571478389b9b9920832f79434f83af0d312cb84747dcdb680a667750` 與基底逐位元相同。
- `node tools/video/cli.mjs lint --slug curio-s49 --json` exit 0：**0 errors／0 warnings／131 lines**。`NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1` 下兩景 `keyframes --shot … --takes 1 --dry-run` 均 exit 0、MiniMax `image-01` ready，提示詞預算 `moon044` **210／1068**、`moon045` **233／1070** 字元；只讀預算檢查，沒有生成圖片。程式重算 `visual_hash=12f2aee4595df518`、`look_hash=98a370ae40badbaf`。正文 128 景＝**117 shot＋11 big**，插圖 **117／128＝91.40625%**，最長連續字卡 **2**。
- 私人 active manifest `/workspace/.video-work/curio-s49/keyframes/manifest.json` SHA-256 **`6ff57bfb19e7c3be0ad77e02190026f53e20855bd7fdba926ef1c1210147f023`** 仍綁 **R38** `visual_hash=c2f2beaa8befb76d`、同一 `look_hash`；31 張 KEEP 選檔都存在且實檔 SHA **31／31 相符**，無 `needs_review` 入選項。`STOP` 在位；`media/jobs.json` SHA **`a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3`** 且 jobs 空。ledger SHA **`b022285fdfdc39149d90579e612265235263893d6f5f3cca6321483df6f0b059`**，178 筆＝**89 image／89 judge**，合計 **US$1.2015／0 預約**；距本集 US$5.30 委派上限餘 **US$4.0985**。服務顯示的 US$200 通用 cap 不取代本集上限。

**結論：八景整批取得文字／來源紙審 8／8 PASS；私人 manifest 仍在 R38 且 STOP 必須保持。**下一個獨立守衛可在 STOP 下審安全離線重綁 R40；本紙審不自行放行付費 `moon040–046` 原圖。每張後續原圖仍需核成年外貌、空模或兩處**邊緣**瑕疵、年代、虛構來源界線及不該出現的文字。
