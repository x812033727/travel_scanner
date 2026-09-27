---
id: 2026-09-26-video-drama-look-keyframes
title: Video drama T4: look (character sheets) and keyframes stages with the look review gate
status: done
priority: P1
area: tools
owner: claude-fable-5-1-video-drama
claimed_at: 2026-09-26T06:31:26Z
created_at: 2026-09-26T01:53:34Z
completed_at: 2026-09-26T06:44:48Z
branch:
depends_on:
  - 2026-09-26-video-drama-core
  - 2026-09-26-video-drama-media-client
scope:
  - tools/video/media/look.mjs
  - tools/video/media/keyframes.mjs
  - tools/video/media/look-keyframes.test.mjs
  - tools/video/review
---

# Video drama T4: look (character sheets) and keyframes stages with the look review gate

## Why

角色跨鏡頭一致是漫劇品質的第一件事。做法：先為每個角色生幾張設定圖讓站主選（`look` 關卡），之後每個鏡頭的關鍵影格都以選定的設定圖當參考生成，並用視覺模型打分、不合格自動換 seed 重做。這張票做 `look` 與 `keyframes` 兩個階段，以及它們的送審與讀回。

## Definition of done

- [x] `look --slug S`：每角色 `candidates` 張（預設 3）、judge 評分（rubric `SHEET_RUBRIC`）、`suggested`（通過者中最高分）、聯絡表 `characters/contact-sheet.png`（瀏覽器開不了就略過並提示）、`characters/manifest.json`（含 `look_hash`）；全部不及格再補一輪（seed 101…）仍不過就結束碼 1 並列出評語；`--choose` 直接寫 `characters/choice.json`；`--dry-run` 印提示詞、張數與估價。
- [x] `review-push --gate look` 每角色送一張審核（`subject`＝角色 id，檔案 `candidate_a…`，payload `character`／`options`／`suggested`）；`review-pull` 把每張核准的選擇寫進 `choice.json`（沒選就用建議），每個角色都有決定才記 look 核准（綁 manifest 雜湊）；`STEP_LABELS` 涵蓋兩種格式的每一步（有測試）。
- [x] `keyframes --slug S`：需 look 已核准且每角色有選定設定圖；每鏡提示詞＝prompt＋style＋camera＋角色描述，參考圖＝選定設定圖（重新上傳到媒體庫）＋風格圖（≤4）；judge（每角色 identity、prompt、style、clean、no_text、subtitle_band）不過換 seed，最多 3 次；`needs_review` 與評語進 manifest；`end_frame.prompt` 另出一張；相鄰鏡頭 dHash 太近警告（ffmpeg 不在就略過）；`keyframes/contact-sheet.png`；`thumbnail_source`。
- [x] `review-push --gate storyboard` 送每鏡關鍵影格（`shot_01…`）與聯絡表，payload `shots`／`judge.overall`（最低分）／`judge.problems`（只有待修鏡的）／`duplicates`；成片送審附 identity 分數留給 T5（片段的 judge 才有每鏡最後一格的 identity）。
- [x] 所有遠端呼叫之間看 STOP 檔；中斷後重跑不重付（`media/cache.json`、`media/jobs.json`）。

## Steps

- [x] `media/stages.mjs`（共用：生成＋快取＋帳本＋judge＋聯絡表＋dHash）→ `media/look.mjs` → `review/sync.mjs` 的 look 送審與讀回 → `media/keyframes.mjs` → storyboard 送審 → 本機 `review/look.html`、審聽／成片頁的「【名字】」→ 測試。

## How to verify

```bash
node --test tools/video/media/look-keyframes.test.mjs tools/video/review/*.test.mjs
node tools/video/cli.mjs look --slug <SLUG> --dry-run
```

## Notes

設計全文在 `docs/videos/DRAMA.md`（跟 T1 一起合併）；供應商、價格、政策的研究依據也在那裡。

2026-09-26 做法（claude-fable-5-1-video-drama）：

- 共用流程在 `media/stages.mjs` 的 `Stage`：`image()` 用 `keyframeKey`（provider、model、prompt、negative、1920×1080、seed、參考圖 sha）當快取鍵，命中就不付錢；送出前對 `max_usd_per_video` 把關；沒結束的工作記在 `media/jobs.json`，重跑接著輪詢；每次生成與 judge 都寫 `media/ledger.json`（judge 以 US$0.01 記，同 catalog.py）。`drawContactSheet` 用 render 的 Playwright，開不了瀏覽器只提示不失敗；`pictureHashes` 用 ffmpeg 算 dHash，沒 ffmpeg 就略過。測試用 `ctx.openRenderer`／`ctx.hashImage` 換掉。
- `look`：seed 第一輪 1…N、第二輪 101…；候選編號 n 連續，審核頁的選項字母＝`optionKey(n)`（1→A）。`keyframes`：seed＝take 次數（1、2、3），檔名 `keyframes/<shot>-<seed>.png`；選定設定圖每次跑都 `putFile` 回媒體庫（伺服器 14 天會清）。judge 的 rubric key 不能有連字號，角色 id 轉底線（`identity_jing_wei`）。
- 給 T5 的合約：`keyframes/manifest.json` 的 `shots[<id>] = { file, sha256, key, seed, judge, takes, needs_review, problems?, end_frame?: { file, sha256, key } }`，`thumbnail_source`、`duplicates`；設定圖 sha 在 `characters/manifest.json` 的 `candidates[].sha256`，選定的 n 在 `characters/choice.json`（`lookChosen` 會退回 `suggested`）。成片送審附最低的 identity 分數要等片段 judge（T5）。
- `review-pull` 的 look 規則：每個角色都要有核准的審核（選了就用選的，沒選用 judge 建議），全部到齊才 `approve --gate look`；只有一個角色決定時回結束碼 3 並印「waiting for <id>」。
- 給後台（S4／UI 票）的 look payload：`{ subject, character: { name, description, voice }, options: [{ key, index, file_role, judge }], suggested, prompt }`；storyboard payload：`{ shots: [{ id, chapter, prompt, seconds, file_role, needs_review, judge }], judge: { overall（最低分）, problems（待修鏡的）}, duplicates }`——`storyboard_check_passed` 看 `judge.problems` 為空與沒有 `needs_review` 才自動核准。
