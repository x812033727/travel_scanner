# S53 R5｜政策通過；語音兩輪限縮重錄後 HOLD

2026-10-20 UTC。對象為 1906–1908 年舊金山公園救災小屋一集的 R5，**沒有修改**企劃、研究、主張、分鏡或劇本。五檔仍是[作者凍結](review/r5-author-freeze.md)與[獨立來源／書面畫面覆核](review/r5-source-independent.md)的精確版本：

| 檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `8e44f47693dd75ad0a7509ab0f495c06adcc2e614b8c8bc09a51559d7202a27c` |
| `research.md` | `2e61530c650852281402476041175154ee69c414daf7431d6aa0db352e7c3d22` |
| `claims.md` | `6a0a1f315fb21baeec5665d0996a97be17b62239b1f72abe5ca93a3b26dab5a5` |
| `video.json` | `2d9e0036e03712028890b4c9af01d776f13394baabefb7cb389b8bb6b6c28f1d` |
| `script.md` | `5f944532562e9e6072efe08cd8d1e3c4caa64f380d4497adccf276df50f3a07d` |

## 關卡與網站狀態

固定史料與書面畫面覆核均為 **PASS**。[原雙讀者合併](review/r5-official-panel.md)及工具記錄 PASS，但讀者的上下文隔離需由兩名全新、`fork_turns:none` 的讀者重做，故**獨立敘事關卡 pending**。本輪付費語音是在發現此隔離缺口前，依既有回條推進；該回條不得轉作最終敘事證據。

網站先用 `review-push --report-only` 登錄並讀回 `category=explainer`、`format=drama`、零張審查卡；完整 `policyRequest({doc,brief})` 只送 **一次**，請求 SHA-256 `868719b3772e0fc3b00edb600d52752d535ef59219a2de3053c248a6cc06629c`，含 2,760 字元旁白與 213 字元站主觀點。Jev 回 `questions=explainer`、`passed=true`：立場 `0.64`、示範不適用、建議 `0.02`、業配 `0.12`。去憑證[回條](review/r5-policy.json) SHA-256 `26f1b690ba7d03cd465b78006eb2b88124a05bffaaa6f9d8550e25fabad656a9`；私有防重送紀錄 `policy-pre-tts-r5-attempt.json` SHA `bc0d83d9ee031821f9a8e5dd08818efcb4a3fdb533040ffbc40ebc77500a3415`、原始回條 `policy-pre-tts-r5.json` SHA `96138f22737430a9a77c656dc882cf452f06143e8260059510a7c4f16ed6aa8e`。

`review-push --gate outline` 和 `--gate script` 已送出精確 `brief.md`／`script.md`；網站讀回兩張皆 **pending**、`hand_pushed`，未有網站核准。本機 `approvals.json` 記站主常設「用推薦的決定」下的 A 案及 R5 劇本**委派編輯選擇**，與網站決定分開。19:09 的劇本備註曾引用原敘事 PASS；19:34 已另附同雜湊更正備註，明列新隔離覆核 pending、網站劇本卡 pending、不得進畫面或成片。本機紀錄不冒充網站核准。

## 真實語音與逐句檢查

`tts --dry-run` 預報 125 次請求、2,538 計費字元；Gemini Sulafat 可用。實際首次合成 125 次／2,538 字元；其後依上一輪 `check-flags.json` **只重錄** 18 次／364 字元及 10 次／206 字元，分別沿用其餘 107、115 個場景。共 **153 次 TTS 請求、3,108 計費字元**，無未確認的語音請求。三輪均用正式 `check-audio` 覆核當前全稿 **127／127 句**，只重新轉寫變動音檔，每輪 Jev 差異判讀各一次：

| 輪次 | 新轉寫 | 逐字 | 同音／語助詞 | Jev 接受 | 旗標 | 正文實測 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 首次 | 127 | 93 | 12 | 4 | **18** | 9:47.63 |
| 限縮重錄一 | 18 | 99 | 14 | 4 | **10** | 9:53.17 |
| 限縮重錄二 | 10 | 103 | 14 | 4 | **6** | **9:51.03** |

最終 `timeline.json` 為 125 場／127 句，`speech_hash=120585e9b1ff83ac`。從 `s53010` 開始至 `outro` 前的正文 **591.03 秒**，超過系列的 8 分鐘下限；濃縮開場 **51.10 秒**，片尾旁白 **17.07 秒**，全旁白 **10:59.20**。這是語音與時間線實測，未含尚未製作的 5 秒品牌片頭、21 秒片尾動畫；最終影片仍須另外驗收。

最後六個官方旗標仍須處理；以下只列差異要點，原意圖、轉寫及 Jev 分數均保留在私有 `check-r5-redo2.json`／`check-flags-r5-redo2.json`：

| ID | 劇本關鍵字 → 轉寫關鍵字 | Jev |
| --- | --- | ---: |
| `s53003` | 小屋 → 隊伍 | 0.04 |
| `s53014` | 先、帳棚 → 現、帳篷 | 0.15 |
| `s53070` | 期限 → 視線 | 0.05 |
| `s53096` | 搬修 → 翻修 | 0.07 |
| `s53099` | 新址 → 信紙 | 0.07 |
| `s53129` | 失訪 → 釋放 | 0.05 |

三輪的完整 WAV／時間線、原樣 `check`／`flags`、受標單句 WAV 及 SHA manifest 均封存在私有 `/workspace/.video-work/curio-s53/review/`；各輪關鍵雜湊如下：

| 輪次 | 旁白 WAV | 時間線 | `check` | `flags` | 受標 WAV manifest |
| --- | --- | --- | --- | --- | --- |
| 首次 | `2dda8f5ba50c814af37659398c0280f4a2b874c2813e6bf1c3f0cac0a7739093` | `0b25beb33ada68d5fa3e0412a1481f9fbe8eed2f483f8e7ee769fe46cfc6600f` | `331d9297cc3948d7125f67eb372fe880ec020b4dc050ab3ee5d8e271e8172ecd` | `22d5a8b221394065cc6dfd79ef1235ec6820dfe23ba094e94d8b839875e4ecb6` | `cdd89a65e61fad8ad89443d0bd7203fdae49dc309bf0c2062012eb9f457abeea` |
| 重錄一 | `9c921bafea464b9a4c2850887d34b3b84188c1e28338c80e6e7dc862fd54556a` | `88a6c7c295a65696b772f56b13b4b4280a1bff0f3e21c62c1c0bf21a847689d3` | `2f96601eed6f287ae1e2396f06499bbe683dafb2dfe09f2d861b4ac59c1cc9c5` | `cbddf12535ad31c125625eca1ced98b30fd6787c20cc8d65d7a69bb913df7607` | `a43fc13e22bde77d7b5ab37f742807f43096ec8ded812da3b3ae8b8142c648d1` |
| 重錄二 | `328069b89070993083060b8c27dfa9ed2ab5d1363d71aa1a524098763069b36f` | `6d4df8f93a59ceaf7499e1f0977754bcb39f83049f3fb2444dda3f16ecea07ea` | `da2efc97a26ddda89df7c13ff977bddd62c1b69a4dea27bdaab3066d47c51395` | `d6d24cfbba9494390f62f0c2d74ec32e9ba66969c0686c7cb6b12f814fe80d24` | `4606cdc36ecda51e5682729eedb19169196e73b3263e692ff73e42cadc548e0f` |

**R5 現況：政策 PASS、真實正文時長 PASS；敘事隔離覆核 pending、網站企劃／劇本 pending、音訊 6 旗標 HOLD。** 兩輪重錄上限已用盡；沒有生成插圖、音樂、片頭／片尾動畫或成片，也沒有送音訊／最終網站卡。

## 下版改句提案（尚未改稿）

六句在兩輪限縮重錄後仍被官方音檢標記。以下僅供下一位作者按固定原文與章節鉤子審看；**不屬於 R5 劇本或已核准口播**。若採用，須同步改 `video.json`、`claims.md`、`script.md` 及相關畫面提示，重新核對來源、敘事、政策、網站卡和語音：

| ID | 可考慮的口播改法 |
| --- | --- |
| `s53003` | 那年夏天，搬離期限到了；一排排救災小屋還留在廣場上。 |
| `s53014` | 營地裡的帳篷，讓人暫時躲雨、休息。 |
| `s53070` | 委員會要求清空各處公園與廣場，不只金門公園。 |
| `s53096` | 慈善機構協助搬運和修繕部分小屋，直到那年六月下旬。 |
| `s53099` | 住戶搬屋後留下的新地址，是訪查員找小屋的線索。 |
| `s53129` | 除了完整訪查，報告還記下什麼地租後果？ |
