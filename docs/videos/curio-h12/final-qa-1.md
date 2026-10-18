# H12 繁中成片 QA 與人工送審

日期：2026-10-17（Asia/Taipei）。本收據記錄本機成片與後台送審；不代表站主已核准成片、選定其他語言或上傳 YouTube。

- 已核准的正式劇本 `script.md` SHA-256 為 `408E3C8BAAFC0063B0B53410B579D14BA09D650753DB466A409E59470F9A620B`；`video.json` SHA-256 為 `5AC5C6CEB1DF801BE0FCFD109BE8EE1CE291BEDFBD16F1D91D9EB11BDC94C13D`。站主已核准的 86 張分鏡 manifest SHA-256 為 `F61238CD938140C8467501B376183A1865DC20D18DFCCC2FFA91504C26A475AB`。本輪沒有改劇本、旁白或分鏡。
- `render` 完成投影片與縮圖；`clips` 沿用 86 張 still，沒有購買動態片段。`assemble` 完成 91／91 段、15,738 格／30 fps＝524.6 秒（8:44.6）的繁中 `final.mp4`，161,440,572 bytes，SHA-256 `2B24B5DF98A459CD587364C24D80FB0A7AFADFF4519DE86001B4A7D0E11D047D`。`checks.json` 無問題，整體響度 -14.1 LUFS、true peak -0.9 dBFS，15 個抽格與投影片比對通過；第一章後約 39.6 秒插入片頭。
- 繁中 CC 97 cue，`captions/zh-TW.srt` SHA-256 `9167E89A8EDEF9D695FE6D9A4D94141D2156A0A1D6CD8DC5E80C7373C57C1E71`；字幕 manifest 綁定目前旁白與品牌版本。獨立抽看八處畫面及六段音訊未見黑畫面、裁切、解碼錯誤或削波；抽看不代替站主完整試看與試聽。
- `review-push --gate final --manual-review` 內建 QA **9／11**，`review/qa.json` SHA-256 `482AF97C5F7ACF3A9069F9B030EB196C375953E6F7811784C80E4F6361E58006`。通過 assemble、render、narration、pace（最長 14.4 秒）、metadata、facts、links（4／4）、thumbnail、disclosure。未過的 `captions` 因 `languages.json` 尚不存在，工具暫檢英／日／韓字幕；站主仍未選定語言。未過的 `policy` 是 TypeSafe Jev 判讀「業配」0.36，高於 0.30 門檻；報告沒有給出具體句子或理由，不能視為已消除。保留原報告供站主判定，未改核准稿或放寬門檻。
- 後台 720p 預覽 `review/preview-2b24b5df98a459cd.mp4` 為 20,376,636 bytes，SHA-256 `63EC9052BF6A1EE43D03C383A80E19E2EE4DA091CC836761C0F5BBAE14D45245`。`review-push` 回報 `final submitted for review (pending)`；後台唯讀 GET 讀回最終審核 ID `9abacb14-5708-43c1-9f15-310908f4e6e3`、狀態 `pending`、content SHA-256 與成片相同；隨即 `review-pull --gate final` 讀回 `final: waiting for the owner`。站主可於 `/admin/videos` 或 `<VIDEO_WORKDIR>/curio-h12/review/final.html` 試看；核准前不製作上傳包。
- 最終 QA 僅呼叫 TypeSafe Jev 一次，已把預留 **US$0.05** 以保守估額結算，沒有供應商最終帳單。H12 累計估算 **US$4.235／US$6**；五集累計估算 **US$26.2295／US$39**。其餘作業沿用既有素材，沒有新增付費媒體請求。
