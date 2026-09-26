---
id: 2026-09-26-video-drama-core
title: Video drama T1: the drama format in video.json, hashes, lint, status steps and the look gate
status: done
priority: P1
area: tools
owner: claude-fable-5-1-video-drama
claimed_at: 2026-09-26T02:00:12Z
created_at: 2026-09-26T01:53:29Z
completed_at: 2026-09-26T02:17:16Z
branch: claude/animation-feature-planning-43667c
depends_on: []
scope:
  - tools/video/core
  - tools/video/cli.mjs
  - tools/video/cli.test.mjs
  - docs/videos/DESIGN.md
  - docs/videos/README.md
  - docs/videos/DRAMA.md
---

# Video drama T1: the drama format in video.json, hashes, lint, status steps and the look gate

## Why

漫劇路線是既有產線 `tools/video` 的第二種格式：畫面不是投影片而是 AI 生成的鏡頭片段，一支影片有多個角色與聲音，字幕燒進畫面，有背景音樂。這張票把格式本身放進 `video.json`，其他票（媒體用戶端、設定圖與關鍵影格、片段、render、assemble、自動流程）都以它為準。共享檔（`core/schema.mjs`、`core/state.mjs`、`core/timeline.mjs`、`core/approvals.mjs`、`cli.mjs`）只由這張票碰，所以它要先做完。

## Definition of done

- [x] `format: "drama"` 通過 `validateVideo`：`characters`、`look`、`music`、`subtitles`、`template: "shot"`、`line.speaker`／`emotion` 依 `docs/videos/DRAMA.md` §資料模型 驗證；slides 拒絕這些欄位；鏡頭句子拒絕 `reveal`。
- [x] `speechHash` 隨 speaker／emotion／角色聲音改變；新的 `lookHash`、`keyframeKey`、`clipKey`、`subtitlesHash`、`mixHash` 在 `core/drama.mjs`；`visualHash` 改鏡頭提示詞就變。
- [x] lint：鏡頭估計 >12 秒錯、>10 秒警告、相鄰提示詞太像警告、Azure 聲音配 emotion 警告；drama 的 `brief.md` 必要章節是「故事前提」「角色」「站主觀點」。
- [x] `pipelineStatus` 依格式給步驟（drama 多 look generated／look approved／keyframes drawn／storyboard approved／clips generated／music generated），`ARTIFACTS` 與 `GATES.look`／`GATES.storyboard` 登記；`cli.mjs` 的 `AREAS` 有 `look`／`keyframes`／`clips`／`music`／`media-status`（模組還沒做時結束碼 5）。
- [x] fixture `tools/video/core/fixtures/drama/video.json`＋`brief.md`（精衛填海）過 lint；slides 的 fixture 與 `npm run test:tools` 仍綠（274 個測試）。
- [x] `docs/videos/DRAMA.md` 併入；`README.md` 的「不燒錄」改成每支影片的 `subtitles.burn_in`（slides 預設不燒、drama 預設燒），`DESIGN.md` 指到 DRAMA.md。

## Steps

- [x] `core/drama.mjs`：常數、`validateDrama(doc, errors, validateVoice)`、`voiceFor`、`lookHash`、`keyframeKey`、`clipKey`、`subtitlesHash`、`mixHash`、`clipsHash`、`PRESETS`、`shotProblems`、`emotionProblems`。
- [x] `schema.mjs`：FORMATS、TOP_KEYS、LINE_KEYS、shot 場景；`validateVoice` 帶路徑前綴；呼叫 `validateDrama`。
- [x] `timeline.mjs`：`speechHash` 納入說話者與角色聲音（只對 drama，slides 的雜湊不變）；時間軸的句子帶 `speaker`。
- [x] `lint.mjs`：依格式的 brief 章節與鏡頭規則；drama 不做版型相似度；slides 有 music 就警告。
- [x] `state.mjs`：ARTIFACTS、`SLIDES_STEPS`／`DRAMA_STEPS`／`stepsFor(doc)`、`lookChosen`；`approvals.mjs`：`GATES.look`、`GATES.storyboard`；`cli.mjs`：AREAS 與 help。
- [x] fixture、測試（`core/drama.test.mjs`）、文件。

## How to verify

```bash
npm run test:tools
node tools/video/cli.mjs lint --file tools/video/core/fixtures/drama/video.json
node tools/video/cli.mjs status --file tools/video/core/fixtures/drama/video.json --workdir <空目錄>
node tools/video/assemble/smoke.mjs --channel msedge   # slides 煙霧測試仍過
```

## Notes

設計全文在 `docs/videos/DRAMA.md`（跟 T1 一起合併）；供應商、價格、政策的研究依據也在那裡。 句子仍是時鐘：鏡頭長度＝句子音檔＋停頓，片段長短由 assemble 的 `fitPlan` 對齊，不反過來。

- 2026-09-26 做完。`drama.mjs` 不從 `schema.mjs`／`timeline.mjs` 匯入任何東西（它們匯入它；ESM 循環會讓一邊在載入時拿到 undefined），所以它自己走一遍句子、自己用 30 fps 換算秒數。
- 「shot」不在 `TEMPLATES` 裡：`schema.mjs` 對它不報錯，交給 `drama.mjs` 在非 drama 格式時報「belongs to format drama」，才不會同一個路徑報兩次。
- 狀態步驟多了 `storyboard approved`（伺服器端可設自動核准）；`music generated` 只在 `video.json` 有 `music` 時出現。
- `characters/manifest.json`、`keyframes/manifest.json`、`clips/manifest.json`、`music/manifest.json` 的最小形狀寫在 `state.mjs` 的 `ARTIFACTS` 註解，T4／T5 照它寫。
- `review/sync.mjs` 的 `STEP_LABELS` 還沒有 drama 步驟的中文（那是 T4 的 scope）；在那之前送審頁會顯示英文的步驟 id。
- 在 worktree 跑測試前要 `npm ci --ignore-scripts`，否則 `pinyin-pro` 與字型套件找不到（dev-and-ci skill 有寫）。
