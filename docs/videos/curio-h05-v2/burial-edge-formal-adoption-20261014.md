# H05 研究對照圖卡接入正式分鏡（2026-10-14）

本輪只修改 `burial-edge` 一景的畫面：`shot` 改為原創 [研究對照來源圖卡](diagrams/burial-edge-control-source-card.svg)。`h5v101` 與其他 105 句旁白、章節、場景順序、逐句時間完全不變。卡面把「兩疊現代鈔票、各五張」「先埋沙，再通過 1 kg/L 矽藻土水」「紙邊約 3–4 mm 有限滲入」及「非原始贖鈔／非天然河水／非案發現場」並列，依 [Kaye、Meltzer（2020）原論文](https://www.nature.com/articles/s41598-020-70015-z)的方法與結果。此圖卡沒有假照片、假顯微影像或虛構物證。隔離的原始候選、來源摘記和 Chromium 720p／1080p 模擬 CC 實看留在 [候選品檢](burial-edge-sourcecard-candidate-20261014.md)，候選檔保留不覆寫。

變更前正式時間軸、核准、旁白、盲審、判圖 manifest、帳本的位元組及 SHA 收據保存在外部 `<home>/mokaair-work/videos/curio-h05-v2/_receipts/h05-burial-control-before-20261014T060711Z/`。正式新 `video.json` SHA-256 `7d94b12a24481bcbd550dbd5b6f5016752975e62e18e7de2842f9f0a613d472d`；正式 SVG SHA-256 `46ff8ce3ae34f5d32168d5ec0e86127a8d770faf1fc65038119ad2ecffb27f51`。格式 lint 0 error／0 warning。

另一位只看**現行純旁白**與 11 題面板的獨立讀稿員回覆 11/11 YES。首次送正式 `narrative` 指令時，答案檔是 JSON 陣列而非 CLI 所需 `{ "answers": [...] }`，被機械判作全部「no answer」；這是輸入包裝錯誤，未有新的劇情否定。保留原始答案，包成正確物件後正式 round 25 **11/11 PASS**，narrative hash `d1978915d7667708`，紀錄 SHA-256 `379ee2c1f5229f6297ba0bb11140a6d1cbd2518ad1792771f0a430833caa426c`。沒有把任何 FAIL 記錄改標 PASS。

`tts --dry-run` 為 100 個請求、**0 個待合成／0 計費字元**；`tts --refresh-evidence` 實際 0 合成、100 重用。新舊 `timeline.lines` 逐位元相同，總時長同為 15,912 格／30 fps＝8:50.4；合成旁白 WAV SHA-256 仍為 `ce18ff45161fbffe0fb058d7d6f8d8a438b0bc5bb9492a5ca099e7c7e43aa943`。`check-audio` 106/106 句，0 新轉錄／0 新 Jev，11 個舊機器標記沿用先前站主聽審，未重錄。畫面模板使新 `timeline.json` SHA-256 為 **`d01d24050ec6cd6a7d5cd720b677ccb64b7bfdbd5368c02b0b08327206f5d391`**；站主已在後台核准新音訊卡，`review-pull` 讀回之核准記錄與正式檔 SHA-256 完全一致（後台核准時間 2026-10-14 06:13:33 UTC）。舊 `fd724a0c…` 核准並未替代新核准。

新時間軸 106 句／91 景／106 個狀態，`cadenceProblems=[]`，最長 7.8 秒、平均 5.0 秒。`burial-edge` 205 格移出 `shot` 後，規劃插畫時長 **8,314／15,912＝52.2499%**（高於 50% 358 格）；這只是場景類型的時長分配，並非 54 鏡已有合格圖。原判圖 manifest SHA-256 `063869be88bc32e6e25d10a179928cc5ba8cf24744e88772dfa02eba0b119978`、帳本 SHA-256 `a0e126405bc555014288a633f5df75ae90a256c965d1632425521702b4116189` 均未變，沒有付費圖片或 judge。

卡片來源與事實文字不在 CC 後面，局部靜格可讀；正式 `.t-diagram .paper` 背景仍鋪滿到字幕附近，SVG 自身縮短底色不會改善外框的字幕距離。此版仍需全片來源與聲畫覆核、完整合格圖組、正常速度播放器看聽、CC 與 QA；不得以新圖卡和舊小樣宣稱已完成分鏡或成片。
