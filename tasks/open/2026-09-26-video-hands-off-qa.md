---
id: 2026-09-26-video-hands-off-qa
title: 影片交給 AI 決定：成片自動品管指令 qa
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-09-26T16:18:29Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/qa
  - tools/video/cli.mjs
---

# 影片交給 AI 決定：成片自動品管指令 qa

## Why

自動品管是把「看成片」交給機器的依據（`docs/videos/HANDS-OFF.md` §自動品管）。11 項裡大部分的檢查已經散在 assemble、render 與 lint 裡。還缺的是：一個把結果收齊的指令，以及畫面停留時間、連結、縮圖、查核殘留這四項檢查。

## Definition of done

- [ ] `node tools/video/cli.mjs qa --slug <slug> [--workdir <W>]`：
  - 寫出 `<workdir>/review/qa.json`：`{ ok, final_sha256, items: [{ id, ok, detail, warnings? }] }`；
  - 結束碼：0 是全過，1 是有項目沒過，4 是外部服務失敗。
- [ ] 項目 id 固定為 assemble、render、narration、pace、captions、metadata、facts、links、thumbnail、policy、disclosure。
  - `policy` 呼叫 judge 端點。端點還沒上線時標成 `ok: false`，細節寫「judge endpoint not available」，不能假裝通過。
- [ ] `pace`：由時間軸與畫面計畫算出每個畫面狀態停留幾秒，超過 15 秒的列出場景 id 與秒數。
- [ ] `links`：用 GET 抓說明欄的每個網址，會跟著轉址，列出不是 2xx 的網址。
  - User-Agent 固定用 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`；
  - 同一個網域間隔 1 秒，逾時 15 秒。
- [ ] `thumbnail`：1280×720、小於 2 MB；縮到 320 寬時，標題字高仍然夠大。門檻值寫在程式裡，並註明怎麼訂出來的。
- [ ] `facts`：最後一輪查核標成 NOT FOUND 的 claim id，已經沒有場景引用。
- [ ] `captions`：lint 的過期警告（句子、章節、標題、說明、標籤）在品管裡算失敗；每秒字數超標只放進 warnings。
- [ ] 所有純函式都有單元測試，I/O 包在薄薄一層裡；CI 沒有 Chromium 或 ffmpeg 也能跑測試。

## Steps

- [ ] `tools/video/qa/`：各項檢查、`qa.json` 的組裝、CLI 子指令。
- [ ] `pace`：2026-09-26 重排第二批時，是用本機腳本算停留時間的，做法見下面 Notes。把它改寫成純函式並加測試。
- [ ] 拿第二批三支（`chatgpt-ads-upgrade`、`gemini-student-offer`、`ai-agent-permissions`）實跑，應該全過；`pace` 應該是 0 個。

## How to verify

```bash
node --test tools/video/qa/*.test.mjs
npm run test:tools
node tools/video/cli.mjs qa --slug ai-agent-permissions
```

## Notes

- `pace` 的算法：每個場景的第一句開始時，畫面進入第一個狀態；之後每一句帶 `reveal` 的句子開始時，進入下一個狀態。一個狀態的停留時間，就是下一個狀態（或下一個場景）的開始時間減去它自己的開始時間。句子時間來自 `timeline.json`，場景與 reveal 來自 `video.json`。
- 連結檢查的網址不能帶任何個人資料；User-Agent 不能放個人 email。
