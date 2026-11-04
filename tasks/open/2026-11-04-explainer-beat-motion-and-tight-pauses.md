---
id: 2026-11-04-explainer-beat-motion-and-tight-pauses
title: 解說類（奇聞、原來如此）運鏡改停住再重拍、縮短句間停頓
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5-producer
claimed_at: 2026-11-04T02:24:00Z
created_at: 2026-11-04T02:23:46Z
completed_at:
branch: claude/explainer-beat-motion
depends_on: []
scope:
  - tools/video/assemble/drama.mjs
  - tools/video/assemble/drama.test.mjs
  - tools/video/assemble/cli.mjs
  - tools/video/core/drama.mjs
  - tools/video/core/timeline.mjs
  - tools/video/core/timeline.test.mjs
---

# 解說類（奇聞、原來如此）運鏡改停住再重拍、縮短句間停頓

## Why

2026-11-03 拿奇聞檔案局五支成片（s04、s05、s06、s09、s17）跟參考的說故事解說片（黑貓研究院三支、馬臉姐一支）量節奏
（製片 skill 的 `references/pace-targets.md`，PR #2005）。結果我們換圖不比參考片慢，差在兩件事：

- **鏡內動態**：參考片是先停住，再快速推近一個細節。我們是整張圖從頭到尾慢慢飄，所以 `reference_analysis` 的 `slow_share` 是 0.32–0.57（參考片 0.15–0.25），`mean_difference` 只有 2.5–3.5（參考片約 5）。
- **停頓**：參考片靜音 0–2.5%，我們 4.3–7.5%。每句後停 300 ms，換景再多 700 ms，合起來 1 秒，超過 `silencedetect` 算靜音的 0.5 秒。

站主 2026-11-04 說「接著改」。

## Definition of done

- [x] 奇聞（`curio-`）與原來如此（`sothatswhy-`，或戴 sothatswhy 身分的解說）的靜止鏡頭改成「停住 → 0.33 秒推近」。2.5–7 秒的鏡頭推一次，7–12 秒推兩次，更長推三次；2.5 秒以下的鏡頭和 locked 鏡頭不動。
- [x] 這兩個系列「量測」時間軸的停頓改成：句間 150 ms、換景 250 ms。稿子自己寫的 `pause_after_ms`（揭曉前那一拍）照舊。
- [x] 品牌故事、漫劇、其他投影片的運鏡、停頓與快取鍵一個位元都不變。
- [ ] 第一支用新規則做的成片，量起來 `slow_share` ≤ 0.30、靜音 ≤ 3%。

## Steps

- [x] `assemble/drama.mjs`：`BEAT_MOTION` profile、`beatExpr`、`MOTION_BEAT_VERSION` 進快取鍵。
- [x] `assemble/cli.mjs`：漫劇路線與插圖投影片路線都依 `beatMotion(doc)` 傳 `tier: "beat"`。
- [x] `core/drama.mjs` 的 `pacedExplainer`，以及 `core/timeline.mjs` 的 `TIGHT_PAUSES`：只在 `basis === "measured"` 時套用。
- [x] 測試。
- [ ] PR #2005 合併後，在 `pace-targets.md`〈怎麼改進成片〉寫明前兩條已經在工具裡做好。

## How to verify

```bash
node --test tools/video/assemble/drama.test.mjs tools/video/core/timeline.test.mjs
node .agents/skills/youtube-video/scripts/reference_analysis.mjs --file <新成片 final.mp4> --range 0-180 --range 300-480 --out ra.json
```

## Notes

- **估計時間軸不改。** lint 與盲評讀的是估計時間軸，而盲評的收據綁著含開始時間的稿子雜湊（`core/narrative.mjs` 的 `panelNarrationSha256`）。改估計值會讓已存的盲評全部失效，所以只改 tts 產生的量測時間軸。代價是 lint 估的長度偏長約 5%，8 分鐘下限要靠 QA 讀量測時間軸來擋。
- **已經過配音關的集數不受影響。** 它們的時間軸已經寫在 timeline.json 裡，要到下次重跑 `tts` 才會用新停頓。重跑後 narration.wav 會變，配音關要重新送審。
- **2026-11-04 試做。** 從 curio-s04-v2 成片截八張圖，鏡長 5–12 秒，舊飄移和新節拍各做一段 70 秒的片來量。結果記在下面〈試做數字〉。

### 試做數字（2026-11-04）

同樣八張圖（鏡長 5–12 秒、沒有聲音），`reference_analysis` 的 `motion`：

| | frozen | slow | active | `mean_difference` |
| --- | --- | --- | --- | --- |
| 舊：整張慢慢飄 | 0.77 | 0.23 | 0 | 0.77 |
| 新：停住 → 推近 | 0.87 | 0.06 | 0.08 | 1.01 |

- 慢慢飄的比例降到四分之一。推近的那一下讀得出來（active 從 0 變 0.08）。
- 成片的 `mean_difference` 是 2.5–3.5，比這裡高，因為字幕、溶接和換圖都算在裡面。參考片約 5。
- 單靠運鏡到不了 `pace-targets.md` 的 ≥ 4.5，還要靠畫面裡的元素跳入，或換更多張圖。這個目標要等第一支新成片量過後再校準。
- 第一版的焦點偏到畫面的 0.62／0.38，在 s04 的海灘那張推到第二次時，把站在左邊的小孩切掉一半。所以把偏移收到 0.55／0.45（pan 0.62／0.38）。
- 停頓沒辦法在這裡量（要配音）。預期換景的空白從 1.0 秒降到 0.4 秒，低於 `silencedetect` 的 0.5 秒門檻。
