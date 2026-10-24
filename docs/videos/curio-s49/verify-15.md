# S49 R15｜政策與完整旁白 PASS，網站三卡待審

2026-10-20 UTC。R15 精確稿 `script.md` SHA-256 `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a`；`brief.md` `b9658ef9df619b6c92ba440ff395065a7702206690a72be863da24bcf098e8e9`、`research.md` `f5da15ac571478389b9b9920832f79434f83af0d312cb84747dcdb680a667750`、`claims.md` `a9e869d51c898ad1cdd11d02291aff52198067c3cc8c154db899205fedc351f5`、`video.json` `1cc788913568dc241e57221692b979fb9a699c7c0c36becacdb3e0c65109a37d`。獨立[來源及書面畫面](review/r15-source-independent.md) PASS；兩名全新隔離讀者的[正式敘事合併](review/r15-isolated-merge.md) 13/13 PASS；`lint` 0 error、0 warning。

完整 `policyRequest({doc,brief})` 對此精確稿只送一次，[去憑證政策回條](review/r15-policy.md) **PASS**：Jev 立場 0.87、建議 0.01、業配 0.21。網站沿用同一 SHA 的大綱卡，並手動送出 R15 劇本卡；兩卡的 `review-pull` 均為 `waiting for the owner`。本機依站主常設推薦編輯委派，沿用精確 brief SHA 的大綱批准，另記 R15 精確 script SHA 的**委派本機編輯批准**；`approvals.json` 註記明確說網站仍待審。網站批准與本機決定沒有混稱。

`tts --dry-run` 預報 131 requests、6 句／176 billable characters 新合成。實跑以頻道聲音 Gemini Sulafat 合成 `moon019/064/076/083/112/120` **6 句／176 字**，重用 125 句舊快取。首次 `check-audio` 檢查 **131/131**：97 逐字、27 同音或語助差異、6 經 Jev 判可接受，**1 旗標** `moon120`（Jev 0.22；聽寫將「愈」作「越」，並省略引號）。旗標原檔已存私有 `review/r15-audio-archive/round0/`；`check.json` SHA-256 `0a726d59fdb5246db6be4abadfd926efba48217e6c4e664f706f77108f32ab21`，`check-flags.json` SHA-256 `5dfaa030e2f36639542e0568ce4a3eb8d90f6f1b30738728e8fc26827cc6e1b1`。未遮掩或改寫正式旗標。

依原旗標只定點補錄 `moon120` **一輪／36 billable characters**，其餘 130 句重用；再完整檢查 **131/131**：98 逐字、27 同音或語助差異、6 經 Jev 判可接受、**0 旗標／0 未檢**。第二輪原檔存私有 `review/r15-audio-archive/round1/`；最終 `check.json` SHA-256 `b7afdb6adcfae9071915364b5cebdd29b03725e59d76bda7099ff25e6bc25c32`，`check-flags.json` SHA-256 `18c109ce544257c20293273191b48e8fc63d2706f6a9263fce21dd1c631cb15c`。最終聽寫把 `moon120` 的「愈讀愈怪」辨成原字；總共只用一次定點補錄，未耗盡兩輪上限。

最終 `narration.wav` SHA-256 `6f6df93ed6f14bf0195cc2ccf90342c7c416467644ef801dfe9cbee905ff4de6`，`timeline.json` SHA-256 `d671161a8fc56422fae03821ae5de44259c5cde079a4a2b27f1b1d54e1f430b6`。WAV 與時間軸同為 **24,043 frames／30 fps＝13:21.43**。第一章 `moon001–008` 到 `moon009` 起點是 **1,441 frames＝48.03 秒**，符合 30–60 秒開場濃縮；`moon009` 到 `outro` 起點 **22,135 frames＝12:17.83** 正文，超過 8 分鐘；outro 467 frames＝15.57 秒。這是旁白時長，品牌片頭插入與最終成片還須另驗。

`review-push --gate audio` 已送網站，`review-pull` 顯示 **outline／script／audio 均 `waiting for the owner`**。音檢本身 PASS，尚無網站或本機音訊核准；沒有把待審寫成已通過。本輪未製作插圖、配樂或成片；後續媒體關須沿用上述精確稿與零旗標音訊，依系列規則驗收分鏡及品牌片頭片尾。

後續 2026-10-20 19:58 UTC，依站主「用推薦的決定就好不用問我」的常設委派，在完整音檢 131/131、零旗標且上述時間軸雜湊不變後，記錄**本機編輯音訊核准**（`approvals.json` 綁定 `timeline.json` SHA `d671161a8fc56422fae03821ae5de44259c5cde079a4a2b27f1b1d54e1f430b6`）。站主未親自聆聽；網站音訊卡仍待審，兩者不得混稱。此註補述原驗證時點之後的狀態。
