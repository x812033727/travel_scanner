---
id: 2026-09-28-video-story-image-model-pricing
title: 故事的圖片照作品的圖片模型計價、快取與記錄
status: done
priority: P2
area: tools
owner: codex-story-image-pricing
claimed_at: 2026-09-29T03:33:55Z
created_at: 2026-09-28T14:30:21Z
completed_at: 2026-09-29T03:58:06Z
branch: codex/story-image-model-pricing
depends_on:
  - 2026-09-28-video-story-worker
  - 2026-09-28-video-story-api-policy-languages
scope:
  - tools/video/media
---

# 故事的圖片照作品的圖片模型計價、快取與記錄

## Why

品牌故事用的圖片模型設在作品上（`video_drama_series.image_model`，站主選的是 Gemini 3.1 Flash Image），不動漫劇預設的 Pro。伺服器已經照影片所屬的作品挑模型（票 `2026-09-28-video-story-api-policy-languages`，PR #938），所以實際出圖的是 Flash。

但工人自己算錢、做快取、寫日誌時，問的是 `/video/media/status`，那裡回的仍是設定分頁的圖片模型。兩邊不一樣的時候：

- 工人估的每支花費用的是 Pro 的單價（每張 US$0.134），實際是 Flash（US$0.067），估計值是實際的兩倍；故事的單支花費上限是 US$25，估高了會提早停下來。
- 快取與日誌記的模型名稱跟實際出圖的不同，之後換模型時哪些圖要重畫會判斷錯。

## Definition of done

- [x] 故事的圖片，工人用 `job.series.image_model`（寫在 `series.json`）來估價、當快取的鍵、寫進日誌與帳本的說明；沒有覆寫時照 `/video/media/status`。
- [x] 工人估的每支花費與伺服器帳本記的，用的是同一個模型的單價；有測試用兩個不同的模型證明。
- [x] 漫劇與投影片的行為不變。

## Steps

- [x] 讀 `tools/video/media/` 裡估價、快取鍵與日誌用到模型名稱的地方，列在 Notes。
- [x] 讓這些地方先看作品的覆寫。
- [x] 測試。

## How to verify

```bash
node --test "tools/video/media/*.test.mjs" "tools/video/automation/*.test.mjs"
```

## Notes

### 2026-09-29 implementation and offline verification

- `stages.imageStatus` mirrors the API's series model/vendor choice and uses its
  catalog price. `look`, `keyframes` and scoped `media-status` use it; no override
  retains the settings choice. Unknown/retired models and unusable override prices
  stop before generation. Cross-vendor credentials are reported as unknown when
  status cannot establish them; the API still checks them before a paid call.
- Manifests compare image identity; version 1 isolates series artifacts produced
  before correct selection, including a cleared override. Legacy images can need
  one regeneration and renewed approval; hashes alone cannot prove their old model
  label. Cache reads verify bytes in bounded chunks, including Pro/Flash/Pro reuse.
- Shared character sheets retain their generating model or explicit unknown
  provenance. A series with an image selection never reuses mismatched/unknown
  sheets, even when the override has been cleared.
- A server-returned model mismatch preserves the actual charge/job and stops for
  reconciliation; it cannot populate a wrongly labeled cache. Job-id accounting
  updates failed-zero to successful cost without charging repeated reads twice,
  and resolved job aliases are cleared. The companion API retry-estimate fix is
  tracked in `2026-09-29-restore-media-job-cost-estimates-after` in the same PR.
- Independent test authoring reproduced seven original failures; four additional
  legacy cases passed on the fix and failed against a read-only HEAD loader.
  Two independent reviews found and resolved shared-store provenance, migration
  and same-job retry accounting gaps. Final focused media suite: 56 passed,
  zero skipped, using bundled Node 24.21.0. Final full tools suite: 709 passed,
  zero failed, two environment skips (Windows bash cannot see its temp directory;
  file symlinks unavailable). The bash probe was slow but completed naturally.
  Related API suite: 34 passed; scoped Ruff and mypy passed.
- No production access, provider call, generated media, account login, upload or
  deployment. This does not complete the separate pilot or its all-provider
  budget and owner-viewing acceptance.

- 2026-09-29 scope review (codex-story-image-pricing): `story.mjs` already persists
  the series image model and its test covers that contract. Narrow this task to
  `tools/video/media`; the initial claim collided only with broad automation
  scopes. Checked worktree/remote branches, open PR file lists and main history;
  no open PR changes these media paths. No other task's claim is changed.

- 這是做伺服器票時回報的（2026-09-28）：伺服器那邊已經照作品挑模型，`/video/media/status` 的估計也用更正過的 Flash 單價，缺的只是工人這一側。
- 試作（票 `2026-09-28-video-story-pilot`）量每支花費時，以伺服器帳本的數字為準，不要用工人日誌的估計值。
- 單價是 2026-09-28 讀 Google 官方價目頁的數字（頁面最後更新 2026-09-24）：Flash 1K US$0.067、Pro 1K 到 2K US$0.134。
