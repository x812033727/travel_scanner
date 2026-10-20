---
id: 2026-10-19-curio-s38-pepys-fire-cheese
title: Curio S38 Pepys fire and cheese historical episode
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-root
claimed_at: 2026-10-19T23:55:04Z
created_at: 2026-10-19T22:34:43Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s38
---

# Curio S38 Pepys fire and cheese historical episode

## Why

為奇聞檔案局新增 S38〈倫敦大火時，佩皮斯為何把起司埋進土裡？〉。這個小動作有可重開的 1666 年日記原文，但網路轉述常加上起司大小、價值或被挖回的結局；本集按 9 月 2–6 日的行動順序講完整故事，並保留日記沒有回答的部分。

## Definition of done

- [ ] 一支經史料、敘事、旁白、插圖與輸出覆核的繁中歷史影片可提交站主發佈審核，並清楚區分佩皮斯親見、聽聞與日記留白。
- [ ] 正片至少 8 分鐘；本機影片與字幕的封裝／QA 證據可重開。

## Steps

- [x] 固定可重開的日記全文與版號，寫 [企劃](../../docs/videos/curio-s38/brief.md)、[研究](../../docs/videos/curio-s38/research.md)、[逐句主張](../../docs/videos/curio-s38/claims.md)。
- [x] 完成 R4 [影片稿](../../docs/videos/curio-s38/video.json) 與 [旁白稿](../../docs/videos/curio-s38/script.md)：112 句、111 個畫面、12 組懸念回收、估 9.995 分鐘，lint 0 error / 0 warning。劇本檔 SHA-256 `62af2f7d762b082a1e6910df28a721fac6c14cb4d081f06516f48b5511cd1411`；影片稿 SHA-256 `f497a97a9de671ba39dad98f92898671035dae6c1ccace5f8740b215a18da4e5`。
- [x] 首輪獨立 [盲讀與史料／畫面覆核](../../docs/videos/curio-s38/verify-1.md) 已留原始答案和 10/13 失敗證據；R2 已集中修正其敘事斷點、無依據的掃水方向與六處畫面問題。
- [x] R2 獨立敘事盲讀 13/13，但來源查核抓到 9 月 2 日午餐前後的事件倒置；這份 R2 劇本不得用於媒體製作。
- [x] R3 獨立敘事盲讀 13/13；史料／畫面查核發現搬走與清點混用、未記錄的寫作時刻、9 月 4 日花園討論的下午時序，以及塔樓、筆記、書面報告畫面問題。R4 已按固定日記集中修正；R3 不能作媒體製作依據。
- [x] 未參與撰稿的新讀者先只看 exact R4 劇本，獨立敘事 13/13、理解 13/13，再重開固定日記並核對 112/112 旁白及 111 提示詞；證據見 verify-4.md。正式 `narrative --answers` 已按讀者行號證據記錄通過。實際語音量測在 TTS 完成後另記。
- [ ] 劇本過門檻後按 `curio-episode` 的整集報價及審核程序製作語音、插圖、分鏡、音樂、字幕、正片，完成輸出與包裝 QA。

## How to verify

在 `/workspace/travel_scanner` 執行：

```bash
VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s38 --json
sha256sum docs/videos/curio-s38/script.md docs/videos/curio-s38/video.json docs/videos/curio-s38/claims.md
npm run check:tasks
```

核對 `docs/videos/curio-s38/research.md` 中 GITenberg 固定 commit 的 1666 年 9 月 2–6 日原文，尤其 9 月 4 日兩個土坑、9 月 2 日塔樓官員轉述的起火地點、9 月 5 日局部止火和 9 月 6 日起司去向未記載。

## Notes

固定日記：GITenberg `68fcf49f70ee793b989a6fd0464264d55beb4451`；`4200.txt` SHA-256 `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`。本工單僅認領 `docs/videos/curio-s38/**`，不碰已有歸屬的 S01／S09／S18。R1 盲讀 10/13 未過；R2 敘事 13/13 卻有來源時序錯誤；R3 敘事 13/13 卻有來源／畫面問題；R4 由新讀者對同一 SHA 先盲讀 13/13，再核固定日記、112 行與 111 圖提示詞通過，詳 verify-4.md。2026-10-19 23:46 UTC：`brief.md` 補具 A／B 兩方案，Jev 選 A 0.94，主代理依站主「採推薦方案持續做完」授權本機核准；R4 精確劇本 SHA `62af2f7d762b082a1e6910df28a721fac6c14cb4d081f06516f48b5511cd1411` 送審後本機透明核准，沒有聲稱站主親讀。112 句 TTS 正在進行；付費插圖仍需語音核查及整集成本上限。另有 [題目可行性筆記](../../docs/videos/history-curiosity/source-feasible-expansion-20261019.md)：S27／S21 因同期互補資料在本雲端未能重開，暫停進入製作。

- 23:56 UTC：112 句 Gemini Sulafat 旁白完成，`timeline.json` 為 17,902 frame／30 fps，總 596.733 秒（9:56.73）。正文從 `pf006` 867 frame 到片尾 `pf112` 17,701 frame，**561.133 秒（9:21.13）**，超過 8 分鐘正文門檻；逐句 `check-audio` 正在跑，結果未出前不批准音訊與付費圖。MiniMax `keyframes --dry-run --takes 3` 對 111 圖報一輪 US$1.50、最多三輪 US$4.50；Gemini Lyria 600 秒配樂報 US$0.08，**整集插圖加配樂上限 US$4.58**，依站主廣泛推薦方案授權預先記帳。圖像仍須先過語音 gate 並排入共用每小時 240 次提交窗口。音檢持有專案鎖時試啟音樂被工具拒絕，未產生費用，待音檢結束再啟。
- 00:07 UTC：配樂已成功生成 600 秒，實支 US$0.08。第一輪音檢保存 74/112 轉寫後，第 75 個請求 `60ffa6a6e03f4a439758f04d4dc8cf51ed24b6dc06da44cfd51b793ccd68da7f` 於 00:04:02 收到無具體錯誤碼的 HTTP 502，speech journal 標 `held`。重跑原生 `check-audio` 只回傳同一 hold，沒有重送。此集非 pilot，網站的 `speech/status` 只報 TTS 月度字數，不報單次 Gemini 轉寫用量；故不能由該端點確認這一次是否計費。保留 journal、錯誤日誌與請求雜湊供核對。語音、圖片 gate 仍未核准。
- 00:09 UTC：站主已在本任務概括授權「以你推薦的就好不用問我，一直做完所有影片」。工具沒有單次轉寫計費查詢，且保留的檔案沒有完整答案。主代理據此選擇**僅對這一筆**清除 journal hold 並重送一次，接受其可能重複計費的風險；記錄原雜湊及該決策，不把重送說成免費。若再遇同類不明結果，另評估而不無限重試。
- 00:12 UTC：重送後完整 `check-audio` 112/112：85 字詞精確、8 同音／語助詞、5 經 Jev 接受、**14 旗標**。旗標 ID 為 `pf007,pf021,pf033,pf040,pf042,pf061,pf069,pf070,pf073,pf074,pf077,pf081,pf082,pf085`；已啟動只重錄這 14 句的 `tts --redo`。重錄及再檢通過之前仍不批准音訊與圖像。
- 00:17 UTC：14 句重錄後第二輪仍剩 4 旗標 `pf040,pf069,pf077,pf085`；按 [verify-5.md](../../docs/videos/curio-s38/verify-5.md) 集中改成 4 句更易聽清、史料邊界更明確的 R5 旁白，稿件 SHA `e7eca53fdb4d6fbae4c4454fc652bb33bd00ca1156f5e30e9fada26413a63cd5`、video SHA `cafb69b501d7f0d41d09d90c8650a2f7198ffb5388c57beacf15a5a88f2994ec`、claims SHA `2c0041720122040c94782054024e82f6dcf6da352e10986d1cdc71c93c594bb1`；lint 0/0。R4 盲讀／劇本核准因雜湊變更不適用於 R5；待新讀者重審與來源／畫面再核後，才能重送 R5 劇本 gate 及只合成更動句。
- 00:34 UTC：R5 新讀者盲讀 11/13，R6 再改夜間敘事後新讀者盲讀 13/13，但獨立來源查到 9 月 2 日 `pf047`–`pf050` 客人抵達／開始裝箱與月光花園／地窖搬箱的兩處先後倒置，故 R6 不得用於媒體。R7 依日記重排四句及四景，script SHA `8aeec7edaaa87f571e66894f0367fc101ec19ad70011bc0e526fef489a073a6d`、video SHA `bdbdb58148a510327bb290a80990a94d7cc4108ed7b6526a02b984e5c4f3ce32`、claims SHA `e4920984987d17ed3211f82062bca185f1c75b4f4e9a67569d46b569d992d2f4`，lint 0/0。新盲讀與全部 112 主張／111 景覆核仍需完成，見 [verify-6.md](../../docs/videos/curio-s38/verify-6.md)。此期間不重錄、不付費開畫。
- 00:37 UTC：R7 全新讀者先僅憑劇本封存 **13/13** 敘事盲評，再獨立重取固定佩皮斯日記查 112/112 主張和 111/111 靜圖提示詞，日期時序與全稿通過。正式 `narrative --answers` 依封存行號通過；兩次 `review-push` 後依站主概括授權本機核准 R7 大綱及 exact script，不稱站主親讀。`tts --dry-run` 報 112 句中只需重錄 11 句、255 個計費字元，已開始重錄；新增音訊、實測正文與零旗標音檢仍待完成，付費插圖未開始。證據見 [verify-6.md](../../docs/videos/curio-s38/verify-6.md)。
- 00:50 UTC：R7 11 句更新後 112/112 音檢只剩 `pf085`：第一次 Gemini 多聽「一」，一次重錄後把「泰晤士河」誤聽成「太湖市河」。本機 faster-whisper 取得模型遇 proxy 403，沒有第二轉寫。R8 僅將此句改成史料同義「這一次……乘船沿河往下游走」；script SHA `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`，video `3dbe6dd23eedef3ff999801f6e548ab69ea480ee8a2b00095e78e1d48ec837b9`，claims `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`。**另一位新讀者** R8 盲讀 13/13、固定日記 112/112 和靜圖提示 111/111 全通過；本機大綱／劇本重新按 exact hash 核准，僅重錄 `pf085` 24 字元，其餘 111 句快取重用。新 `timeline.json` 全片 596.2 秒，正文 `pf006`→`pf112` **560.6 秒／9 分 20.6 秒**；完整音檢 **112/112、0 旗標**，本機音訊 gate 已透明核准，未稱站主親聽。配樂已支 US$0.08、整集插圖加配樂硬上限 US$4.58；圖片尚未開畫，等共用時窗。細節見 [verify-8.md](../../docs/videos/curio-s38/verify-8.md)。
