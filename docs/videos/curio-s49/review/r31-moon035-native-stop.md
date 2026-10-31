# S49 R31｜`moon035` 少年貌與放射圖退件，停於第二章

2026-10-22 UTC。**`moon035` 機器 9.29／10 PASS，三次原尺寸目視均 REJECT；`moon036–039` 未開畫。**[R30 `moon034` 原圖 KEEP](r30-moon034-rebind-native-keep.md)後，本輪只沿用[R26 第二章八景非作者紙審](r26-next-chapter-eight-prompt-independent-pass.md)對未改的 `moon035` 書面 PASS，限界買一張 MiniMax `image-01` 原圖及一次 judge；沒有批次送五景。

## R26 紙審是否仍適用

從 R26 提交 `825b0360e` 讀出 `video.json` SHA-256 `57027ce7870f736e8662b6774ed4f6e85922d153e6ac864fb8a9ca1cf389ca22`、`claims.md` `ced02136c94ec5f93f34a62ad5bddfd635b8fde8af93297cff531f91ae40bbcc`，逐景解析比較 `moon035–039` 的**整個 scene 物件**，並逐位元比較五列 `claims.md`：5／5 scene 及 5／5 claims 行與現稿完全相同。[機讀清單](r31-moon035-native-stop-inventory.json)列每項 SHA。因此 R27 `moon032/033`、R28 `moon032` 來源卡、R30 `moon034` 修法均沒有轉改這五景，R26 書面審核仍精確適用於其提示詞與史料界線；書面 PASS 並非原圖 KEEP。現稿 `video.json` SHA `df908e395da02b427bea4f6ae03c3ca69c834058cff90f881c0ac2139f05dc7b`、`claims.md` `c7278022364e16210ac5fbb6d85c4498b0e5a534e3db35ea62736b3d666a64c9`、劇本 `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a` 均在這次付費前後不變。

## 原圖驗收與停止

付費前私有 manifest SHA `5e660a3839c5a51923dfe4f8b36c3e8e988aaf10919a76d19e07bc3ebac3e77b` 綁 `visual_hash=0ec110a386fb0098`，28 張先前 KEEP 的完整項目與實檔 SHA 逐張相符；`moon035` 尚無圖單條目。`STOP` 在位、jobs 空，帳本 US$1.0800／80 image／80 judge／0 預約。新查 `media-status` 顯示 MiniMax `image-01` US$0.0035／圖、圖片餘 10,051、judge 餘 8,484；定點 dry-run 提示詞 315／1070 字元。加一圖一 judge 約 US$0.0135 仍低於整集 **US$5.30** 上限。守衛命令只執行 `keyframes --slug curio-s49 --shot moon035 --takes 1`，CLI exit 0，隨後 STOP 即恢復。

本輪所選即 **1280×720 原圖** `keyframes/moon035-1.jpg` SHA-256 `2265702635c6de2285d5902e24ba567d46c5499d528f1e75c3be524d49036699`，未產生或選用新裁圖；原圖另存私人 `review/r31-next-five-native/moon035/`。機器 9.29／10 PASS，但指出紙上約十二條向外射線，而提示詞是中央點與兩條鬆散無字光線。三次原尺寸目視判 **REJECT**：人物黑髮、面部圓潤、眼睛與身形偏少年，正式領巾仍不足以辨為要求的 1830 年代**成年**讀者；紙張幾乎與人同高、直立如海報，放射線組成具體圖樣，不再是那張小幅、空白、只有兩條概念線的紙。沒有可辨文字或現代設備，但巨幅放射圖會提高把虛構焦點討論看成特定史料插圖的風險。固定重印本只寫虛構 Herschel 問人工光能否穿過焦點影像，**沒有這張圖紙原件**。機器分數不能補正少年貌和假圖印象。

付費後圖單 SHA `98be6876d6188b7715527360c7191dfd2d6220fac8dc0aafd380070ba959920b` 一度選入機器 PASS、人工退圖。先把原圖與兩張機器 contact sheet、前後 manifest／ledger、stdout／stderr 保存在私人 `review/r31-next-five-native/moon035/`，然後在 STOP 下把事前 **28 KEEP manifest 逐位元恢復**，並把 R30 歸檔的兩張 contact sheet 覆回；現行圖單 SHA 再為 `5e660a3839c5a51923dfe4f8b36c3e8e988aaf10919a76d19e07bc3ebac3e77b`，沒有 `moon035` 退圖或退件圖頁引用。28 張 KEEP 的項目及選圖實檔 SHA 未變，`keyframeProblems` 僅列 **91 張未畫**、其他 0。帳本 SHA `9258461cc0ef50d2015ac5020def8e734a136d99203a1364bb65158c489e2428` → **`a2c44d8e8b053d5a0a0dac91eeb421c720a56f6b335ba968b3fc38e459f4da91`**，累計 **US$1.0935／81 image／81 judge／0 預約**；只加 US$0.0135，低於 US$5.30。STOP 在位、jobs 空。

**`moon036–039` 未付費試畫。**下輪先把 `moon035` 窄修為有可辨中年特徵的讀者與較小、抽象、無字的焦點示意，交非作者紙審；若仍被畫成假原件，可考慮有來源註明的字卡。完整分鏡、站主卡與人耳、動畫、Short、成片及 Studio 連結仍待。
