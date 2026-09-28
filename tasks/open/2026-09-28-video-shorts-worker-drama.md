---
id: 2026-09-28-video-shorts-worker-drama
title: Video shorts T4: vertical drama Shorts, with the drama pipeline following the aspect setting
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-28T03:55:00Z
completed_at:
branch:
depends_on:
  - 2026-09-28-video-shorts-worker-lab
  - 2026-09-26-video-drama-pilot
scope:
  - tools/video/core/drama.mjs
  - tools/video/core/drama.test.mjs
  - tools/video/core/lint.mjs
  - tools/video/media/stages.mjs
  - tools/video/media/keyframes.mjs
  - tools/video/media/clips.mjs
  - tools/video/media/qc.mjs
  - tools/video/render/subtitles.mjs
  - tools/video/assemble/plan.mjs
  - tools/video/assemble/drama.mjs
  - tools/video/shorts/vertical.mjs
  - tools/video/shorts/vertical.test.mjs
  - .agents/skills/youtube-video/references/prompts/shorts-drama.md
---

# Video shorts T4: vertical drama Shorts, with the drama pipeline following the aspect setting

## Why

站主選的第三條內容線是「漫劇直式短篇」：漫劇的預告、精彩片段，或獨立的直式小故事。漫劇產線把畫面寫死 1920×1080（`assemble/plan.mjs` 的 `WIDTH`、`HEIGHT`、`media/stages.mjs` 的 `IMAGE_SIZE`、`render/subtitles.mjs` 的字幕條、`media/qc.mjs` 的最小尺寸），後台的 `drama_aspect` 設定（`16:9`、`9:16`）伺服器有送給片段的供應商，工具卻沒有任何一處讀它。把 16:9 的成片裁成直式會切掉角色與燒錄的字幕。

設計全文在 `docs/videos/SHORTS.md`（§三條內容線）；漫劇產線在 `docs/videos/DRAMA.md` 與 `docs/videos/BINGE.md`（畫面等級與運鏡）。

## Definition of done

- [ ] `video.json` 的漫劇多一個可選的 `aspect`（`16:9`、`9:16`，預設 `16:9`）；畫面大小由它決定（1920×1080 或 1080×1920），從關鍵影格、片段的請求、運鏡、字幕條、合成到檢查都跟著走。**沒有 `aspect` 的漫劇一個位元組都不變**（雜湊、快取鍵、編碼參數）。
- [ ] 直式的字幕條放在 Shorts 的安全區（下緣不超過 1600，左右留 78 與 178），每行字數照直式的寬度重算。
- [ ] `make` 在題目的 `line` 是 `drama` 時走 `vertical.mjs`：
  - 從來源的一集挑 5–8 個鏡頭與它們的台詞（`planner`、`variant: shorts-drama`）：第一鏡是鉤子，最後一鏡是懸念，不劇透結局；估計 25–55 秒。
  - 每個鏡頭用原本核准的關鍵影格當參考，重畫一張 9:16 的關鍵影格（judge 檢查角色還是同一個人）；預設全部是靜圖加運鏡，最多兩個鏡頭買片段。
  - 旁白與角色聲音沿用該作品；台詞一字不差時旁白快取命中。
  - 成片走漫劇的合成，輸出 1080×1920；之後照 Shorts 的 `qa`、`package`、`push`（`format: "drama"`、`shorts_line: "drama"`、`source_slug`）。
- [ ] 品管的 `policy` 項對漫劇只看「沒有建議」「沒有業配」兩題（故事沒有「觀眾能照著做的東西」）；`disclosure` 一律是要勾。
- [ ] 花費：每支的圖片與片段走既有的媒體預算與單支上限；`usage` 帶進成片審核，記到 Shorts 的花費帳。
- [ ] 煙霧測試多一支直式漫劇（用 `lavfi` 造的替身），檢查尺寸、格數、字幕條的位置。

## Steps

- [ ] **先跟漫劇那條線協調**：這張票動到的共用檔，漫劇、長篇作品、合集都在用；開著的 PR（#870）與試作票有沒有在改同一批檔。
- [ ] 讀品牌故事影片那條線的設計（票 `2026-09-28-video-story-*`；它在漫劇產線上加了 `kind: "story"`、全靜態圖、只有旁白）：它的集數也是直式短篇的來源，而且它會改到同一批共用檔。獨立的直式小故事（不是從某一集切出來的）是 `source_slug` 空白的 `drama` 題目。
- [ ] `aspect` 貫穿產線，加回歸測試證明 16:9 不變。
- [ ] `vertical.mjs` 與提示詞。
- [ ] 測試與煙霧測試。

## How to verify

```bash
node --test "tools/video/**/*.test.mjs"
node tools/video/assemble/smoke.mjs
```

## Notes

- 要等漫劇試作（`2026-09-26-video-drama-pilot`）跑出第一集：沒有核准的關鍵影格與成片，就沒有東西可以切。
- 片段的供應商收不收 9:16、價格一不一樣，實作時對著 `apps/api/app/video_media/catalog.py` 再查一次；MiniMax 的影片請求目前不送 aspect。
- 伺服器的片段工作從設定的 `drama_aspect` 拿比例，請求本身沒有這個欄位；一支直式短篇與一集橫式漫劇同時在做時會互相影響。要不要讓片段的請求自己帶比例，寫成一張給 API 的小票。
- 後台的 `look` 與 `storyboard` 圖片類別在 W1 已經不再強制 16:9。
