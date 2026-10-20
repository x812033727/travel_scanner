# S45 R10｜政策、網站待審及 102 句實音零旗標

2026-10-20 UTC。以下只對 R10 `script.md` SHA-256 `b5354170966637ceea44ba6d2b96d27b052f3195db02ba91507af2dff984986c`、`video.json` `6339b421fd41c585039d5b3b8ef933513dff05b0fe9fbf56da82ab929d9537cb` 有效。[獨立原著與書面畫面差分](review/r10-source-independent.md)皆 PASS；[兩位全新隔離讀者](review/r10-official-panel.md)各 13/13，合併 PASS。這些不代替聲音或圖像檢查。

完整 `policyRequest({ doc, brief })` 對精確 R10 於本日一次成功，請求 SHA-256 `e427f22c8f9bb63169a2bea8ef445f1069c73802d786c9d2048c5bba263b5c8a`，私有原始回條 `/workspace/.video-work/curio-s45/review/policy-pre-tts-r10.json` SHA `f2c1415dfffe454be85fb17b4c8b49f0c04c48a8908e5c59577485cef7617e21`。Jev `explainer` **PASS**：立場 0.78、示範不適用、建議 0.02、業配 0.02。沒有重送相同請求。`review-push --gate script` 已送站，回覆 `hand_pushed`／**pending**；站台大綱也是舊版等待站主決定，不稱網站已核准。本地 `approve --gate script` 於 15:57:34 UTC 針對精確劇本記**使用者委派的本地編輯決定**，註明站台仍 pending。

先 `tts --dry-run`：102 請求中只有改寫的 `bly098` 需新合成，約 40 個 Gemini 免費層計費字元；實際 `tts` 成功 **1 新句／101 沿用，40 字元**。首次全片 `check-audio` 102/102 仍只標 `bly098`（把「布萊」聽成「布萊爾」），回條 `review/check-r10-first.json` SHA `2a884729be3dcfc7069a296a16e7f66dedb314e1ec1cd8f0c4ed6b2554ae624c`，旗標 SHA `bdebede9bb34b6d13d71cc600f963cb77531c69e75af01f3bd9e9a813da353db`。原 WAV 先存 `review/audio-r10-first/bly098.wav` SHA `1723bd9c38ecf62ae14d0d0aa372fe5caa8d24caa9707af70ff2c2b66b82d6d6`。

只補錄 `bly098` 一句，再計費 40 字元、其餘 101 句沿用。第二次**完整**音檢 102/102：45 逐字、55 同音或標點／語助差異、2 Jev 判可接受、**0 旗標、0 未查句**；本輪只新轉寫一個補錄片段、沒有新 Jev 呼叫。該句轉寫「布萊在書裡寫，陪審團仍支持他……」與台詞「她」的文字性別差是國語同音字，音檢判 `sound`。現行 `review/check.json` SHA-256 `57b4ec76906f27d4afc26d2b56818038c92d8ddc7d62e28f88e1aa8954a292fb`、空旗標 `review/check-flags.json` SHA `701b8ed3f364258e865deb286eaf0955b812f12249908d44a3172078fa3264e9`。

精確最終 `narration.wav` SHA-256 `f96cdc37885e5b44f986027cd32466ab793656556ad3bb18404c51e924f3e45b`、`timeline.json` SHA `0e15cc2e80bcaebc86f808f54d9ef397b9ae23a1356acc11709350625a9d638b`，30 fps 時開場 45.43 秒、開場後至片尾前正文 585.63 秒（9:45.63）、102 句含片尾口播 650.23 秒（10:50.23）。`review-push --gate audio` 已送站但回 `hand_pushed pending`；`review-pull --gate audio` 顯示 `waiting for the owner`。本地 `approve --gate audio` 於 15:59:55 UTC 只記**依使用者持續授權的本地精確音訊決定**，不冒稱網站或站主親耳核准。

插圖前一次整集報價：`keyframes --dry-run` 為 96 張 1K MiniMax `image-01`，最多每張 3 次、全片上限約 **US$3.89**；同版 `music --dry-run` 600 秒約 **US$0.08**，合計採 **US$3.97** 本集上限。起點網站帳本 US$0.00。使用者已持續授權「採推薦、不例行詢問、繼續做完」，本地採推薦上限及系列畫風；先選三個不同場景各只試一張，原生圖至少 **2/3 可用**才對餘下 93 景花費。若未達，停止全片付費圖、配樂與成片，記錄結果；若通過，後續仍不能超出同一整集上限。這個**本地委派預算決定**不是站台 storyboard／final 核准。插圖、配樂與影片截至本收據尚未生成。
