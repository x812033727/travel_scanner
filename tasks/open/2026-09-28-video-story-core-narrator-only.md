---
id: 2026-09-28-video-story-core-narrator-only
title: 沒有角色的漫劇跳過設定圖，加上故事的 lint 規則
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-09-28T03:31:11Z
completed_at:
branch:
depends_on:
  - 2026-09-28-video-story-design-docs
scope:
  - tools/video/core/state.mjs
  - tools/video/core/state.test.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
  - tools/video/core/story.mjs
  - tools/video/core/story.test.mjs
  - tools/video/core/fixtures/story
  - tools/video/media/keyframes.mjs
  - tools/video/media/look-keyframes.test.mjs
  - tools/video/assemble/smoke.mjs
---

# 沒有角色的漫劇跳過設定圖，加上故事的 lint 規則

## Why

品牌故事（`docs/videos/STORY.md`）是只有旁白、全部靜態圖的漫劇。格式本身允許沒有角色（`tools/video/core/drama.mjs` 的 `validateCharacters` 寫著空陣列是 narrator-only），但產線走不過去：

- `stepsFor`（`tools/video/core/state.mjs`）永遠把「look generated」「look approved」排進步驟；
- `look` 在沒有角色時直接丟錯（`tools/video/media/look.mjs` 第 88 行）；
- `keyframes` 要求設定圖關卡已核准（`tools/video/media/keyframes.mjs` 第 97–104 行）。

故事另外需要幾條漫劇沒有的 lint 規則，才不會讓不合規格的稿子一路做到花錢的階段。

## Definition of done

- [ ] `characters` 是空陣列的漫劇，`status` 的步驟裡沒有設定圖的兩步，`keyframes` 不要求設定圖關卡，其餘步驟照舊；有角色的漫劇行為不變。
- [ ] `series.json` 的 `kind` 是 `story` 時，lint 多檢查：每個鏡頭都是 `visual: "still"`、每一句的 `speaker` 都是旁白、至少 70 鏡、章節 5–7 個、`sources` 至少 3 個 https 網址、鏡頭的提示詞不含 `series.json` 的 `names` 裡任何一個名字。
- [ ] `tools/video/core/fixtures/story/` 有一支最小的故事範例（`video.json`、`brief.md`、`series.json`），lint 零錯誤。
- [ ] 煙霧測試能用故事範例從頭做到成片，每個鏡頭在 `checks.json` 都是 `kind: "motion"`。
- [ ] `npm run test:tools` 通過。

## Steps

- [ ] `state.mjs`：`stepsFor` 在沒有角色時拿掉設定圖的兩步；`pipelineStatus` 對應調整。
- [ ] `keyframes.mjs`：沒有角色時跳過設定圖的核准檢查，參考圖只用風格錨定圖。
- [ ] `core/story.mjs`：故事的 lint 規則，`lint.mjs` 在 `series.json` 是故事時呼叫。
- [ ] 範例與測試；煙霧測試加 `--fixture story`。

## How to verify

```bash
node --test tools/video/core tools/video/media
node tools/video/cli.mjs lint --file tools/video/core/fixtures/story/video.json
node tools/video/assemble/smoke.mjs --fixture story
npm run test:tools
```

## Notes

- `state.mjs` 是共享檔，只有這張票動它；PR #870 也改了這個檔 8 行，合併順序誰後誰 rebase。
- 故事可以有 0–3 個主角（只出現在畫面、不說話）；有主角時設定圖照常產生，由 judge 自動選（免關卡作品本來就這樣）。
- `MAX_SHOT_SECONDS = 12` 不動。
