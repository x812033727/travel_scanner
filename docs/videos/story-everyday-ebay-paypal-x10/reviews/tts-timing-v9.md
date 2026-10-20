# X10 eBay／PayPal v9｜實際語音與時長收據

**時長 PASS；語音內容仍待逐句複查。** 對已通過[同版來源與雙盲讀](combined-v9-independent.md)的主片 `video.json` SHA-256 `f5c7ec99142c4508d06ef58c8e5e0c136bd7e556a4254dba940d4328f804757c`，採用[獨立覆核的 X10 詞表](manual-lexicon-adoption-applied.md)後，配對影片工具的 `tts --dry-run` 回 105 個待合成請求、約 2,456 個 billable characters、`gemini:Sulafat ready`。實際 `tts` 成功合成 **105／105** 句、0 沿用；供應商報 2,456 個 Gemini 免費額度計費字元，旁白 **09:51**。這是字元額度記錄，不是 US$ 成本估價。

本機 `timeline.json` SHA-256 `0d654dc9792cda1cb2336f9be4ff9b2b0d410b326601fbbedb992845f741547f`，`narration.wav` SHA-256 `950be18af2d67ef72d3d357363ca0cebc4d8bc28a4406b711c49c57bb3b972ce`；時間軸 `speech_hash` 為 `810fcc61f9e93275`，30 fps、總 17,737 格＝**09:51.233**。第一章濃縮開場從 0 到第二章起點 **00:50.433**，符合 30–60 秒；從第二章起點到最後三句第一句 `x100717` 起點的實質正文 **08:40.567**，超過 8 分鐘底線；原生最後三句 **00:20.233**。如果站主正式 5 秒片頭和 21 秒片尾都插入，理論總長 **10:17.233**，但兩段正式授權動畫尚未取得、合成或驗收。

這份收據只證明指定 WAV 與時間軸的量測，不代表發音、逐字稿一致、Shorts 25–55 秒、圖片、配樂、可關閉繁中 CC、正式片頭片尾、MP4 或 YouTube 可點連結已通過。下一關是 `check-audio` 的逐句轉錄與人工聽檢；有旗標的音訊須保留證據並修正後重新量時。
