---
id: 2026-11-14-curio-theatrical-gouache-look-and-thai
title: curio theatrical gouache look and Thai hashtag marks — 奇聞檔案局與解說系列共用定案劇場級動畫光影×厚塗水粉畫風，並修正泰語系 Hashtag 組合母音截斷
status: done
priority: P2
area: docs
owner: antigravity-curio-gouache-rules
claimed_at: 2026-11-14T10:14:08Z
created_at: 2026-11-14T10:13:34Z
completed_at: 2026-11-14T10:44:33Z
branch: antigravity/curio-gouache-look-and-thai-hashtags
depends_on: []
scope:
  - AGENTS.md
  - .agents/skills/curio-episode/SKILL.md
  - .claude/skills/curio-episode/SKILL.md
  - docs/videos/explainer-series/README.md
  - docs/videos/history-curiosity/README.md
  - docs/videos/history-curiosity/look.md
  - docs/videos/lessons/explainer.md
  - tools/video/core/metadata.mjs
  - tools/video/core/metadata.test.mjs
---

# 奇聞檔案局與解說系列共用：定案升級版「劇場級動畫光影 × 厚塗水粉質感」內建生圖規則，並修正泰語系 Hashtag 組合母音截斷

## Why

1. 繼 PR #2104 將「原來如此事務所」（`sothatswhy-*`）定案為升級版「劇場級動畫光影 × 厚塗水粉質感」與代理內建 `generate_image`（`16:9` 滿版＋角色設定圖 `ImagePaths`＋`keyframes import --provider external --usd 0`，停用 MiniMax 生圖）後，站主在奇聞檔案局製作時明確拍板「以後用這樣的風格」，需要將同一套現行標準與 `curio-m17`／`curio-p17` 的實戰防呆（單集跨 ≥ 4 鏡出場的歷史人物先產設定圖傳 `ImagePaths`、桌面靜物近景明寫背景顏料塗滿四邊最外層像素防留白邊、街道外景寫 `plain unadorned walls with zero hanging shop signs`、四格 2 倍放大獨立審圖含地圖方位與時代道具考證、外語說明欄壓在 `< 4,500` UTF-8 bytes、十步架構「還記得開頭…嗎？」顯性提示留頭尾最多 2 次）寫入 `curio-episode` skill（含 `.claude/skills` 同步副本）、`docs/videos/history-curiosity/{look,README}.md`、`docs/videos/explainer-series/README.md`、`docs/videos/lessons/explainer.md` 與 `AGENTS.md`。
2. 在 `curio-m17` 抽檢時發現 `tools/video/core/metadata.mjs` 的 `hashtagsFrom` 使用 `.replace(/[^\p{L}\p{N}_]/gu, "")`，而泰文上下母音與聲調屬於 Unicode `\p{M}`（Combining Mark）而非 `\p{L}`，導致 `#ปีที่ไร้ฤดูร้อน` 被削成母語者無法閱讀的子音串 `#ปทไรฤดรอน`。補上 `\p{M}` 並加上單元測試可一勞永逸修復泰語、印地語等組合字元語言的說明欄標籤。

## Definition of done

- [x] `tools/video/core/metadata.mjs` 的 `hashtagsFrom` 改用 `/[^\p{L}\p{M}\p{N}_]/gu` 保留組合母音與聲調（並確保至少含一個字母或數字），且 `tools/video/core/metadata.test.mjs` 新增泰文 `#ปีที่ไร้ฤดูร้อน` 與單獨組合符邊界測試。
- [x] `AGENTS.md`、`.agents/skills/curio-episode/SKILL.md`、`.claude/skills/curio-episode/SKILL.md`（位元組完全一致）、`docs/videos/history-curiosity/look.md`、`docs/videos/history-curiosity/README.md`、`docs/videos/explainer-series/README.md` 與 `docs/videos/lessons/explainer.md` 完整寫明 2026-11-14 奇聞檔案局與解說系列共用定案。
- [x] `npm run test:tools`、`npm run test:docs-videos`、`npm run check:tasks` 與 `node docs/videos/rules-sync/sync.mjs --dry-run` 全數通過。

## Steps

- [x] 修正 `tools/video/core/metadata.mjs` 的 `hashtagsFrom` 正規表示式，並在 `tools/video/core/metadata.test.mjs` 加入泰語系組合母音測試。
- [x] 更新 `AGENTS.md`、`docs/videos/lessons/explainer.md`、`docs/videos/explainer-series/README.md`、`docs/videos/history-curiosity/{look,README}.md` 與 `.agents/skills/curio-episode/SKILL.md`，並同步複製至 `.claude/skills/curio-episode/SKILL.md`。
- [x] 執行 `npm run test:tools`、`npm run test:docs-videos`、`npm run check:tasks` 與 `node docs/videos/rules-sync/sync.mjs --dry-run` 驗證後結案並發 PR。

## How to verify

```bash
npm run test:tools && npm run test:docs-videos && npm run check:tasks
node docs/videos/rules-sync/sync.mjs --dry-run
```

## Notes

- Claimed with `--force` because stale ticket `2026-10-14-curio-episodes-keep-the-series-look` (>740h stale, `[not found anywhere]`) still lists `.agents/skills/curio-episode/SKILL.md` and `docs/videos/history-curiosity/look.md` in its scope. Verified via `who-is-on-it.mjs` and `gh pr list` that zero active sessions or open PRs touch any of the 9 scoped files (`docs/videos/lessons/curio.md` was intentionally left out of scope to avoid colliding with open PR #2101).
