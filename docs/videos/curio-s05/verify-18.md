# S05 R22：刪除重述後的精確候選稿

2026-10-20。兩名對 R21 精確稿 `d1edab78…` 的新盲讀者同否 `no_recap`，因結尾 `eg139` 重說 `eg137` 已標的裴注引書身分，且 `eg070` 已明說裴自己的反駁。原始分數與來源覆核見 [`verify-17.md`](verify-17.md)。因此直接刪掉 `eg139` 與其只承載這句的 `visit-085a` 插圖；`eg085` 的諸葛亮〈出師表〉作者身分現在直達片尾查書問句。`eg137` 仍分清陳壽正文與裴引《魏略》，`eg130` 仍分清引書與「臣松之以為」，`eg070` 仍給出裴的上門方向判斷，必要的史料界線沒有刪掉。

同步把 `eg005` 開場問「哪一句」的 `loops.payoff` 從裴寫「可怪」的 `eg072` 改為揭曉他引用哪一句的 `eg069`。這只校正掛鉤定位；不改任何口播或原文。`claims.md` 去掉舊 `eg139`、更新有效 ID 計數，原有史料對照仍覆蓋全部在稿旁白。

新版 `script.md` SHA-256 **`8e9632a4d1cce5a25a2876db16ea8d7c66de1d5d0544c367541b2cd845ae8121`**；`video.json` SHA-256 `cb0b83c24d20be9ee39c2cd2b07f59acdaedc10f73e8541d9f2da15aedabf7fe`；`claims.md` SHA-256 `cf2b9f440e62e93f43f904635c97f14eac36324e04a64ebc2e2034caa740a016`。`node tools/video/cli.mjs script --slug curio-s05` 已重生劇本；`lint --json` **0 errors／0 warnings**，97 句／89 景，估全片 9.28 分鐘。R21 的 `eg134`「設想」與 `eg160`「裴松之的引文接著是」維持在 R22；兩處已由第二名 R21 讀者按固定 SG35 p1/p8 來源驗證，但 R22 仍需全新精確稿盲讀與重核對。

## R22 盲讀、史料與劇本關卡

全新讀者在只見此精確劇本和 CLI 正式十三題時先向負責者封存 **13/13 是** 的判斷，之後才讀研究與前評。其 [`blind-22.json`](blind-22.json) SHA-256 `5774dbdc1ad6aab9ad700d44bba9c5a1baa218fddbeafd19a4d9bb0a01ae4b93` 是**封存後補寫的 CLI 格式轉錄**，保留先封存的判斷並附實際稿句，不能錯稱檔案寫入時間早於史料閱讀。`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs narrative --slug curio-s05 --answers docs/videos/curio-s05/blind-22.json` 記為正式 **round 25**：12 個必答及參考題均是，`failed: []`、`advisory: []`，`narrative_hash` `a62d0988a0ecf2a9`。這是對 R22 的新讀者，不沿用 R21 兩位讀者的分數。

讀者封存後的[獨立來源／對照收據](source-22.md) SHA-256 `4f801c7d41e544ebb4e7a0a2f47dda5ec9e5f16170f07875c68ab6117dbf2e1b`：固定 SG35 卷 35 `p0`／`p1`／`p8`／`p21` 支持兩個口語改法及其史料界線；**89/89 景、97/97 句、claims 97/97 個唯一 ID** 全對，86 張插圖提示詞和兩張字卡與相鄰旁白相合。`eg139`／`visit-085a` 在三份現行檔都已消失。另由本輪獨立程式計數 claims 97/97，無缺漏或多餘 ID。

已用正確工作根呼叫 `review-push --gate script`，網站回報 R22 卡已提交、`pending`；再依站主既有「以你推薦的就好不用問我」委派，對本頁精確劇本作**本機劇本核准**，時間 `2026-10-20T00:08:23.874Z`。核准註記列明 R21 雙否已修、R22 新讀者與來源核查通過，並明說**站主未親讀**。網站待審與本機委派核准是不同狀態。

## R22 旁白與音訊關卡

以網站頻道聲音 `gemini:Sulafat` 合成：93 個請求中 **2 個新合成／68 計費字元，91 個使用已付快取**；旁白時間線 89 景／97 句，全長 **591.467 秒＝9:51.467**。故事正文從 `visit-008` 到 `outro` 前的實測 **535.833 秒＝8:55.833**。`timeline.json` SHA-256 `8ce9fe5b9e928298ac7f7dcc5e867dbaa7ea3239782c9369fb1e6cdaa1e878c1`，`speech_hash` `a23c5fbd76205a29`，旁白 SHA-256 `3abbbf59d17d87cb6e1b4445b0198cd081cf71bce0cad1068ad030361d3514d0`。

`check-audio --slug curio-s05` 對 **97/97 句**逐句檢查：**83 逐字相符、11 同音或語助、3 Jev 判可、0 flag**。`review/check.json` SHA-256 `b7e883b8c2960843e5189409200e9d11646e140f4442ccecd225b84ade3df9f1`；`check-flags.json` 綁定此輪 `speech_hash` 且 `flags: []`。已 `review-push --gate audio`，網站回報 `pending`；依同一站主委派作本機音訊核准，時間 `2026-10-20T00:09:37.323Z`，註記明說依工具逐句辨識與時長量測、**站主未親耳聽過**。此處不把機器查核冒充真人聽感驗收。

## 整集媒體報價與共用配額

`keyframes --dry-run` 報 **86 張插圖、0 end frame、最多每景三次**；MiniMax `image-01` 報一輪約 **US$1.16**，三輪上限 **US$3.48**。`music --dry-run` 對現片長報新生成約 **US$0.08**；S05 已有同一 `mix_hash` `71ecdd098c551254` 的 Lyria 3.5 合格音樂檔和 manifest，音樂的 US$0.08 **已付**、CLI `status` 為 generated，無需再花一次。整集插圖＋音樂報價上限 **US$3.56**，後續新增插圖開支上限 **US$3.48**；若重畫觸頂就停止，不超價。

目前 S05 ledger 合計 **US$0.097**，逐項是音樂 $0.08、先前已接受一張圖 $0.0035、其評審 $0.01，與一筆舊圖預留 $0.0035；後者尚屬預留，非第二張可用圖。既有 MP3 manifest 標 600 秒，但 `ffprobe` 實測檔長 **175.647 秒**，組裝會循環；成片須查全程覆蓋和循環接點。因 R22 現片長 591.467 秒，重跑 `music` 會以 597 秒另取 key、再收約 $0.08；系列負責者已同意**重用目前有效音樂**，不作重複採購。

付費插圖尚未開始。`ten_topics` 通知目前先跑 S23 的定點修圖，S04 91 圖首輪接著占共用窗口；等其回報剩餘額度，S05 才在上列整集上限內一次畫完。不得把目前的一張舊圖或 dry-run 報價寫成整集已完成。
