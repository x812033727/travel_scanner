# S46 R11｜語音兩輪修正與第三次轉寫的不明確回條

2026-10-20 UTC。此檔保留付費語音和音檢的實際邊界；**R11 沒有通過完整語音覆核，也沒有進入插圖或成片。**精確 R11 的來源、雙盲、政策與本地委派選稿另見 [R11 政策收據](review/r11-policy.md)；網站兩張卡仍是 `hand_pushed pending`。

`gemini:Sulafat` 首輪真實合成 120/120 句、計費字元 2,710。第一次完整 `check-audio` 檢出 16 句；只重唸這 16 句，368 字元、其餘 104 句沿用。第二次完整覆核檢出 8 句；再只重唸這 8 句，182 字元、其餘 112 句沿用。至此合成共 **144 次、3,260 字元**；兩份完整覆核原樣 JSON、flags、當時 WAV／時間線及受標原始音檔保存在私有 `/workspace/.video-work/curio-s46/review/`。第二次 flags 為 `bkw016, bkw027, bkw044, bkw062, bkw074, bkw076, bkw077, bkw088`，不能當成第三次結果。

第三次完整 `check-audio` 在 `bkw044` 的新音檔轉寫時收到 **HTTP 504 `video_speech_upstream_lost`**。speech journal 請求 SHA-256 `088da560df29e04f20490c4a0b7d5c32753035c9381eada5f3c3c5b9b508695f`，音訊請求 SHA-256 `697b17c151aabd313660bdcc3d6a8261260de523c5064b97252e696f4ef580f2`；送出 16:38:43 UTC，16:41:13 UTC 標 `held`。站台明示 Gemini 可能已轉寫但回答未回來。journal 沒有可用答覆，亦無可核的供應商使用紀錄能證明未執行。原請求保留在私有 `audio/speech-journal/`，重跑同稿 `check-audio` 只回 `held`，**沒有重送原請求**。

第三次前的 `narration.wav` SHA-256 `f6e1d540878aa0ea848bd4e19c96dcd77d470bb6f4a59575a638934a22008d06`，`timeline.json` `b5d76b06f711097b9155009952e3b34f02598de348fa6bf805dff204da588eb4`。前兩次完整檢查的 `check.json` SHA 分別為 `5a76db4e69cb24222918427af6b99c8b7c645f3d5ceb69351487e4db7f962886`、`593a51c18363cec7e52d71c2f2127f6d09ff3ac8d8319d982b7011b9c608b76f`；flags SHA 分別為 `e9d36e32c3ef665cbc78bdddfd926d798ecdfb54324bd40c83b7b899c4b77bf6`、`b4e68e398e43d23ce5071e3d09bb0ca79d0ce3ee19cc5c3521d7ab5116a36359`。

後續只可在有確定原答覆可恢復時恢復該請求，或修訂 `bkw044` 的文字、重新凍結與核准**新版**，讓新版音檔產生真正不同的轉寫請求；不得清掉 journal 後重送相同音檔。改稿後需重做受影響來源、盲讀、政策與站台精確版關卡，並完成全部 120 句音檢才可核音。
