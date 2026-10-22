# S49 R33｜`moon036` 童貌與錯誤畫線退件，停止下一張

2026-10-22 UTC。**`moon036` 一張 1280×720 原生圖，機器 9／10 FAIL、獨立人眼 REJECT；`moon037–039` 沒有開畫。**承接 [R32 `moon035` KEEP](r32-moon035-rebind-native-keep.md)，未做多景批次。

## 固定版本及付費前守衛

從 R26 提交 `825b0360e` 逐物件比對：目前 `moon036–039` 四個完整 scene 和四行 claims **4／4 均逐位元相同**，故 [R26 非作者紙審](r26-next-chapter-eight-prompt-independent-pass.md)對這些書面畫面仍適用，但沒有預先核准原生圖。現 `video.json` SHA-256 `33c5340f8c84888851fe4e968a7ec316431e8d721e95ef1e2390ff639dce15f5`、`claims.md` `27ac2780c03c2aa7f2fccc041f18dcfbf007187eeec8015402c6532a67c48463`、`script.md` `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`，本次畫圖前後未改。旁白「布魯斯特在文中遲疑，先提折射和入射角該怎麼辦」只指 [1859 重印本](https://github.com/GITenberg/The-Moon-Hoax-Or-A-Discovery-that-the-Moon-has-a-Vast-Population-of-Human-Beings_62779/blob/ce684a827afd854e0843679fe4568fcaeeb12ae7/62779-0.txt#L390-L520)所載虛構對話，非真實實驗。

付費前 `media-status`：MiniMax `image-01` ready，圖片餘 10,042、judge 餘 8,462；`--shot moon036 --takes 1 --dry-run` 顯示提示詞 324／1072 字元、服務 ready。圖單 SHA `c4e11b2f9080b2d998d813a4cb70b4c99f945eef378658c19f120dcd5af7de86` 有 **29 張 KEEP**，全部完整條目與選用實檔 SHA 再驗；帳本 SHA `de8cebf204d3e2584102d84c1fefe19ac90d95562e2a8450d5975284910bf2f1` 為 US$1.1070／82 image／82 judge／0 預約，最多增加 US$0.0135 仍低於整集 **US$5.30**。守衛確認 STOP 在位、jobs 空、精確文稿／圖單／帳本 SHA 和 29 選圖位元，暫時解除 STOP 後只執行一個 `moon036`、一 take，退出即恢復 STOP。

## 原尺寸驗收、回復及停止

產生 `keyframes/moon036-1.jpg` **1280×720**，SHA `aaf3051acddcb5557185537611304d5bf7aff9877eca28a26fa09f9be071dd7e`。機器判 **9／10 FAIL**、`needs_review=true`：主體分數 0，認為沒人正在描 V 形角；細節 7，左側像孩童。整合者及非作者各以原尺寸看過，均判 **HUMAN REJECT**：左側明顯是圓臉小孩，另一位也偏年輕、服裝輪廓不顯 1830 年代成年讀者；右側把筆舉在紙外，沒有在描入射角；紙約半桌寬，畫上兩條很長的交叉曲線，不是簡單 V 形墨角。雖無現代器材或可讀文字，年齡與動作均偏離准許的兩名成年人物討論，無法靠機器分數或卡通容忍度收下。

CLI exit 1，一度把退圖寫入 `needs_review` manifest SHA `baf7e88d510ba80b09a662bb84efefb5e828e48167aeca989f3b408868376041`。[機讀庫存](r33-moon036-native-stop-inventory.json) SHA-256 `c658db79b43e6332b83037a291b715c06b9d8db911f7682167e8c4f2fc690d90` 保留 29 張既收完整項目及實檔 SHA、R26 書面同一性、原圖和帳本證據。原圖、兩張機器 contact sheet、前後 manifest／ledger、stdout／stderr／exit 存私人 `review/r33-next-four-native/moon036/`。STOP 下把付費前 29-KEEP manifest **逐位元恢復**，兩張 contact sheet 從 R32 KEEP 封存逐位元覆回。現行圖單再為 `c4e11b2f9080b2d998d813a4cb70b4c99f945eef378658c19f120dcd5af7de86`，不含 `moon036`，`keyframeProblems` 僅列 **90 張未畫**、其他 0。

帳本計入一次真實支出，不回滾：SHA `03726e2755a995b16f809393d44dd8f3c8ab07833b38f3200554d200695dc7c6`，**US$1.1205／83 image／83 judge／0 預約**，仍低於 US$5.30；STOP 在位、jobs 空。**`moon037–039` 未付費畫圖。**下一步只窄修 `moon036` 的成年人物、年代外套與可見小 V 角，另人紙審後才准再買一張；完整 storyboard、站主卡／人耳、動畫、Short、成片和 Studio 連結仍待。
