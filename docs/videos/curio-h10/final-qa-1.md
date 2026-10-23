# H10 繁中成片 QA 與人工送審

日期：2026-10-16（Asia/Taipei）。本收據記錄本機成片與後台送審；不代表站主已核准成片、選定其他語言或上傳 YouTube。

- 已核准的正式劇本 `script.md` SHA-256 為 `A4A64B02732D97C9DDB216B2CD42F789D95A0B0ADEB8AB3CE22B3C9CA679E596`，82 句正文與已核准旁白未改。已核准的 73 張分鏡 manifest SHA-256 為 `658D8630C8B9EAACA8AD4EF3F3A572291938B471C43C6865C628DFE7D702374E`，本輪未改圖片或提示詞。`video.json` SHA-256 為 `A43541019B57D0EF624A6AF2573C728CC5009894121EE9DE6E8BBF5623EC8C57`。
- `render` 畫出 7 個文字卡狀態；`clips` 沿用 73 張 still，沒有購買動態片段。`assemble` 完成 80／80 段、18,425 格／30 fps＝614.17 秒（10:14.17）的繁中 `final.mp4`；旁白正文 17,645 格／30 fps＝588.17 秒（9:48.17）。片頭 150 格放在第一章後、約 43.77 秒處；片尾品牌包 630 格。成片 171,269,977 bytes，SHA-256 `912F39E5DF15E0FEC7AADE44FE6872B28E8C6E5E9EDA63F60EEECB7E4949017C`。合成收據 `checks.json`：0 problems、-14 LUFS、true peak -0.9 dBFS、21 個抽格與投影片比對通過。
- 繁中 CC 102 cue，`captions/zh-TW.srt` SHA-256 `56FA66BD91608FE58A4215DDB82778A6523E0C32DC1B09DA5627959B02075E62`，manifest 綁目前旁白與品牌版本。`languages.json` 記 `{ "locales": {}, "decided_at": null }`，表示站主尚未決定其他語言；此時只驗 zh-TW，不能解讀為「只出繁中」。
- `review-push --gate final --manual-review` 內建 QA **10／11**，報告 `review/qa.json` SHA-256 `E11505CEF4FF69B20585B0E61F23D2C0B35D9AD9188CA2A2CFD5DA3472B6C990`。唯一未過 `pace`：片尾 `outro state 0` 停留 17.4 秒，超出單畫面 15 秒上限。其餘 assemble、render、narration、captions、metadata、facts、links（7／7）、thumbnail、Jev policy、disclosure 全過。Jev 回傳符合立場 0.71、建議 0.01、業配 0.18，判定通過。保留站主已核准的稿、旁白與分鏡，將節奏項交站主在成片關卡判定。
- 送後台的 720p 預覽 `review/preview-912f39e5df15e0fe.mp4` 為 21,975,388 bytes，SHA-256 `C50EC0EC30951D2D86EF0CCE17AA6B5E60512E7CA53E3023D35FA3561B6DBCB7`。`review-push` 回報 `final submitted for review (pending)`；後台 read-only API 讀回最終審核 ID `3264b871-0278-4f3d-8c36-c3434a068059`、狀態 `pending`、content SHA-256 與成片相同；隨即 `review-pull --gate final` 讀回 **`final: waiting for the owner`**。站主可於 `/admin/videos` 或 `<home>/mokaair-work/videos/curio-h10/review/final.html` 看成片；核准前不做上傳包。
- 最終 QA 僅呼叫 TypeSafe Jev 一次，依共用預算預留的 **US$0.05** 保守估算；沒有供應商最終帳單。批次協調者已將這次估額記入共用帳本，H10 累計估算 **US$2.569／US$6**。
