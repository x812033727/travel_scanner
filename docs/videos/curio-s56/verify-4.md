# S56 R4｜政策、網站卡與實測語音收據（歷史草稿，HOLD）

2026-10-20 UTC。此收據只綁 S56 R4 精確輸入；五檔快照另存私有 `/workspace/.video-work/curio-s56/review/r4-input-snapshot/`，往後的 R5 修稿不會改寫下列結果。

| 輸入 | R4 SHA-256 |
| --- | --- |
| `brief.md` | `a17b3ac122723c1229bdb1bcf1af2c546b7665407bad5677a24658ad50583dfd` |
| `research.md` | `59549e98e6ae258cedfc5b43e6684ecaa1102284d0dee13b0beef6443e4a6fb7` |
| `claims.md` | `1d267cb9365eab571b3b94f13de5ebc136e323bc0d80869db0abac3874ccc1d3` |
| `video.json` | `9516fc7c0d76c011d39e00be5262e6011a2b2a8597636074334c88ba901447ff` |
| `script.md` | `b76995caa74f0a1f65b068d9e115659d7c48678600b80e9ff502e641a6505152` |

[R4 獨立史料／書面畫面](review/r4-source-independent.md) **PASS**，`lint --json` 為 0 errors／0 warnings，176 句、141 景、七章。先前繼承對話脈絡的 [R4 OR 敘事合併](review/r4-isolated-merge.md) 曾判 PASS；兩名真正無歷史脈絡讀者的[新正式合併](review/r4-clean-merge.md)則 **12／13，`no_recap` 共同否決，FAIL**。因此本輪音訊屬需修稿的 R4 草稿，不能當成敘事或音訊放行。

## 政策及網站

先以 `review-push --report-only` 註冊並讀回網站 `category=explainer`、`format=drama`，再對完整 `policyRequest({doc,brief})` 呼叫 Jev 一次。請求 SHA-256 `0e393e8b49d1551040a3879e721e1fbd489266e829c1380f4e04a51670f64e4d`；Jev `explainer` **PASS**，立場 `0.83`、示範不適用、建議 `0.01`、業配 `0.01`。原樣去憑證回條在 [r4-policy.json](review/r4-policy.json)，SHA-256 `51d0008e102a2ef34be073d5ebcdb87b9dacb35b6c58c24a1a60b256b9971d08`；原始請求、預送紀錄及回覆在私有工作目錄 `review/policy-pre-tts-r4-*.json`。R5 改稿後需要重新分類精確新稿。

精確 R4 企劃卡 `6bd1bab2-beed-4a42-b374-45ec294c59a8` 綁 `brief.md` 上表雜湊，劇本卡 `0201b972-612e-4231-8080-6215de15bae1` 綁 `script.md` 上表雜湊。提交後讀回兩卡均 `hand_pushed=true`、`pending`；**沒有網站站主核准**。本站的 brief parser 回 `0 options`，並未自動選案。[本地委派編輯選擇](review/r4-delegated-choice.json)只記使用者常設推薦偏好下的 A 綱及 R4 精確劇本供語音／音檢，明寫 `owner_approval=false`；沒有在本地 `approvals.json` 偽造站主核准。

## TTS 與真實時長

`tts --dry-run` 預報 Gemini Sulafat 已就緒，141 個新請求、約 **3,798** 計費字元，當時本月剩餘 **8,543,027** 字元。首次正式合成實際 **141 請求／3,798 字元**、0 沿用；唯一限縮重錄只用首次官方 52 句旗標，乾跑預報 48 請求／1,055 字元，實際 **48 請求／1,055 字元**、93 個場景請求沿用。逐句 WAV SHA 比對證明恰好 **52 句旗標音檔改變、124 句未標音檔逐位不變**；兩輪合計 189 新請求、4,853 計費字元，0 fallback，未觀察到 429 或額度封鎖。未作第二次重錄。

| 版本 | `timeline.json` SHA-256 | `narration.wav` SHA-256 | 總旁白 | 開場至 `s56014` | 正文 `s56014` 至末 |
| --- | --- | --- | ---: | ---: | ---: |
| 首次 | `eeebffdfc777174c43ce4ba36064087d713e8899232ab0cd5ad97aaf3aebe3b2` | `bb7fcb45e7dc08470f62462c0f1f79beae03bdf471990e4a9fae79c83c495513` | 25,195 frames＝13:59.83 | 1,635 frames＝54.50 秒 | 23,560 frames＝13:05.33 |
| 限縮重錄一 | `1d67422f2e05746554b89d17771d6286fa0489b8276dd4aa9d2c99030e727f80` | `74fe7ec1dd727dc4a32d0601355819c5f7c2fa4d2ff306c47c48c13286e80a80` | 25,156 frames＝13:58.53 | 1,661 frames＝55.37 秒 | 23,495 frames＝13:03.17 |

時間線為 30 fps，兩版皆 176 句／141 景／七章。首次 WAV 的 `ffprobe` 時長 `839.833333` 秒與時間線相符。兩版正文均超過八分鐘，開場在 30–60 秒之內；5 秒品牌片頭和 21 秒動畫片尾尚未做入成片。

## 官方全稿音檢與停手點

| 輪次 | 已查 | 逐字 | 同音／語助 | Jev 接受 | 旗標 | 新轉寫／Jev 呼叫 | 原樣收據 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 首次 | 176／176 | 93 | 25 | 6 | **52** | 176／2 | [flags](review/r4-audio-flags-round0.json) SHA `1ec5179860c8c01afc8207c122609a535e212327e6b223c9a944146af751420f`；私有 `check.json` SHA `292ee3298f2412eeb7ba79c3e7cefc94cfe97fed86549a03ac7d59d60c16ee3c` |
| 限縮重錄一 | 176／176 | 103 | 32 | 8 | **33** | 52／1 | [flags](review/r4-audio-flags-round1.json) SHA `1317fd68e1531ba718e3e483424fed56112171a001226326bddc6c3a37720636`；私有 `check.json` SHA `16ab6b2c399cee19056a1913cacccf40636ce7883207ea01abb2bf46afc86a4e` |

兩次 `check-audio` 都因旗標退出碼 1，0 句未查。52→33 代表 19 句清除，沒有新旗標；剩餘 33 句仍為 **HOLD**。其中 14 句含福斯特／洛許人名、17 句含「火」，如 `s56004` 的「主火→燭火」、`s56028` 的「洛許→若許」、`s56038` 的「街面→介面」和 `s56050` 的「信裡→心裡」；這些重複詞形提示 ASR 或發音辨識問題，但**不能在沒獨立聽辨時自行清旗標**。R4 正式敘事已 FAIL，依停手要求不做第二輪付費重錄或音訊網站卡。初版及重錄版的 WAV、timeline、完整轉寫、原樣旗標、逐句 WAV 雜湊清單均保存在私有 `/workspace/.video-work/curio-s56/review/r4-audio-archive/round0/`、`round1/`；兩版輸入亦有上述 R4 私有快照。沒有製作插圖、配樂、成片或發布。
