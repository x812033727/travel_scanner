---
id: 2026-09-28-sothatswhy-explainer-preset
title: So That's Why: flat-illustration explainer preset for the drama route (narrator only, all still shots)
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-28T09:00:00Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/
  - tools/video/automation/prompts.mjs
---

# So That's Why: flat-illustration explainer preset for the drama route (narrator only, all still shots)

## Why

「原來如此事務所」（`docs/videos/so-thats-why/README.md`）每集 7–9 分鐘、約 90–120 張插圖，全部是 `visual: "still"` 鏡頭，只有旁白、沒有角色對白、沒有影片片段，畫風是扁平編輯插畫而不是漫劇的 3D 寫實。現在的漫劇路線預設是有角色、有對白、有 clip 的故事，企劃與撰稿提示也是寫故事；每集都手改會漂移。

## Definition of done

- [ ] 有一個解說用的風格預設（扁平插畫、固定色盤、所長吉祥物當參考圖），`video.json` 可以指定它。
- [ ] 純旁白、全 still 的集數過 `lint`（畫面等級 `stills`，不要求角色對白）。
- [ ] 撰稿提示有「解說」變體：鉤子 20 秒、3–4 個原因章節、一句答案收尾、每 4–6 秒一鏡、數字與地圖用卡片場景。
- [ ] 有一份 fixture 與測試。

## Steps

- [ ] 讀 `docs/videos/DRAMA.md`、`docs/videos/BINGE.md` 的 still 鏡頭與畫面等級，決定是新的風格預設還是新的 format。
- [ ] 加預設與 lint 規則、提示詞變體、fixture。

## How to verify

`npm run test:tools`；對 fixture 跑 `node tools/video/cli.mjs lint --slug <fixture>`。

## Notes

規格來源：`docs/videos/so-thats-why/README.md` 的「一集長什麼樣」「畫面風格」。
