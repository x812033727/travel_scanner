# S04 六句白話新版：獨立查核與配音關卡

查核日：2026-10-19。`script.md` SHA-256 `2201aaa948660f2375d60d5fe598a87c4a61e10d22cf32c137c2702d1ba494ac`；92 句／91 插圖／七章，估 8.1 分鐘，`lint` 0 errors／0 warnings。上一版三輪配音查核及六句改稿原因見 [`verify-9.md`](verify-9.md)。

全新、未參與寫作的讀者先只讀確切劇本，再答十三題，全部 **13/13 YES**，前後 SHA-256 一致；原始逐題證據見 [`blind-9-final.json`](blind-9-final.json)。之後才抽核固定原文，六句 `s04048`、`s04058`、`s04062`、`s04064`、`s04065`、`s04071` 對應《三國志》卷 54〈周瑜傳〉與〈魯肅傳〉、裴注《江表傳》，另以固定《資治通鑑》辨孫瑜；逐項文字與畫面審查見 [`source-9-final.json`](source-9-final.json)，無事實或畫面阻斷。「這一帶」依前句指鄰近邊境，不指稱公安城每一位居民。

正式 `narrative --answers blind-9-final.json` 已按現版通過；在使用者既有「採推薦方案、持續製作」授權下，代理重新記錄企劃及劇本核准，兩者均綁定各自現版 SHA-256。本文件不聲稱站主已逐句親耳聽過。

頻道 Gemini／Sulafat 先重製六個改稿句，其餘 86 句沿用；第一次新稿 `check-audio` 檢查 92/92，72 句逐字相合、16 句同音或語助詞差、2 句 Jev 判可，`s04058` 與 `s04065` 仍被標記。只對這兩句各補錄一次，最終 92/92：**74 句逐字相合、16 句同音或語助詞差、2 句 Jev 判可、0 旗標**；實際 `narration.wav` **489.40 秒，即 08:09.4**，高於 8 分鐘關卡。原始機器回執位於 `/workspace/.video-work/curio-s04/review/check.json`；音訊時間軸 `timeline.json` SHA-256 `b75ebe3056f3d261b71610cd3e95dfca0dfb8aa42e1b0af63d6c67e33fb2b8f4`。`review-push --gate audio` 已送後台，伺服器仍為 pending；本機依使用者持續授權記錄 audio 核准，**不稱站主本人已親聽**。

Gemini Lyria 配樂報價約 **US$0.08**，已生成同系列無歌聲配樂。`music/manifest.json` 記目標 495 秒，`ffprobe` 實測 MP3 為 **178.18 秒**；組片器須循環至旁白結束，最終成片需查循環接點與片尾沒有靜音。MiniMax 插圖 dry-run 為 **91 張**，一次約 **US$1.23**、每張最多三次約 **US$3.69**；尚未生成，等待媒體排程。
