# S53 R23｜`s53023` 一張原生圖人工退件與停線

2026-10-22 UTC。接續 [R23 離線重綁與媒體預檢](r23-source-card-offline-rebind-and-media-preflight.md)，僅對下一個未繪 `s53023` 執行 `keyframes --shot s53023 --takes 1`，MiniMax `image-01` 產一張 1280×720 原生 JPEG，judge 一次。**機器 9.29／10 PASS，原尺寸人工 REJECT；依停線約定，沒有開 `s53024` 或第二張。** [逐檔清單](r23-s53023-native-inventory.json)固定本次的 SHA、request key、帳本與前 14 張 KEEP。

## 原圖與來源判定

已直接以原尺寸打開私人原圖 `/workspace/.video-work/curio-s53/keyframes/s53023-1.jpg`，SHA-256 `02174ee03ecf99221669a3968b359db4c1418812aef497859d1d2777e4d1d084`，1280×720。此景沒有另外的裁圖，所選圖就是原圖。畫面主角是童貌、短小身形，戴鮮黃色硬式工程帽、穿現代感工作服，站在規整鋪面廣場的大型木框公園／小屋示意板旁；示意板有小屋草圖，但場地內沒有看得見的實體救濟木屋或帳棚。大幅看板加全身人物是寬景，未得到已紙審的「1906 年廣場，匿名救濟工作者近景查看空白公園街區圖、旁有小屋草圖」。原提示詞未明寫成年，下一輪應收窄人物年齡。judge 只列 `details`：full shot instead of close shot；它未攔住童貌、硬帽與現代感，所以人工 **REJECT**。此圖若用在「公園廣場能否讓救災小屋一直住下去？」的旁白，會使 1906 救濟小屋與場地的年代感、視覺主題偏離已核准畫面。1913 年固定調查 [G L4934–4941](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4934-L4941)仍支持原旁白的公園臨時用地及期限問題；**退件只針對圖像，不改歷史主張或 126 句旁白**。

## 可追溯的停線與恢復

付費前重新驗 R23 `video.json`／`claims.md`／`script.md` 三檔精確 SHA、私人 14-KEEP manifest SHA `b8e3159267747d1ea80b70276d79cbf70cfb6c497fdbcd2cd516978e1a4eaca1`、ledger SHA `dc7aaf8ca062b7680113bde534ce7d1cbdc218ab5567626f0365f6fa39dfc01f`、jobs 空及 `STOP` 存在。命令只在 EXIT trap 保護下暫時移開 `STOP`，完成後自動恢復；exit 0，未留下背景工作。這一圖／一 judge 增 **US$0.0135**，帳本從 US$0.4725／36 image／35 judge 到 **US$0.4860／37 image／36 judge／0 預約**，仍低於整集 US$4.78 上限；新 ledger SHA `b9a520e5e3a0ac3ccfaab32d4fa1b27e3f2bde332b515f882eff51178ff32cd2`。

生成後的 manifest SHA `9ba1b0dee9bf2689b44a87fc54e3f90b612ab8a02d5a1c13c671bd4104335ecc` 連同機器評分、request key 獨占備份至 `/workspace/.video-work/curio-s53/rebind-backups/r23-s53023-native-before-human-reject.json`，原 JPEG 保留私人區作退件證據。人工退件後，以 R22 備份和 R23 `visualHash` 在記憶體中重建原 14-KEEP manifest，先證明重建 SHA 恰為 **`b8e3159267747d1ea80b70276d79cbf70cfb6c497fdbcd2cd516978e1a4eaca1`**，再驗全部 14 張選圖檔雜湊與條目相符，`keyframeProblems` 為 0，原子寫回並讀回同 SHA。有效 manifest 沒有 `s53023`、`s53010` 或 `s53018` 退件條目，contact sheet 引用空；14 張既收圖一筆未動。jobs SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3`，jobs 空、`STOP` 在位。現有 113 張 `shot` 中 14 張 KEEP、**99 張仍缺合格圖**；lint 再跑為 0 errors／0 warnings。

本輪對 `s53023` 是第一張實際原生圖。下一步須由作者依童貌／硬帽／大型看板與缺小屋的原圖問題，窄修此景提示詞與對應 claims 畫面欄，留下可逆差分，再交另一人獨立核畫面和來源，才可限額重試。`s53010`、`s53018` 已各三張上限，不得再畫第四張；`s53024` 以下本輪未開畫。網站審查、人耳聆聽、全片圖、配樂、片頭片尾、成片與 Studio 連結仍待後續實際完成。
