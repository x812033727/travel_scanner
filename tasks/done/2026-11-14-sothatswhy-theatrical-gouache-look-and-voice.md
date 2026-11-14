---
id: 2026-11-14-sothatswhy-theatrical-gouache-look-and-voice
title: "sothatswhy theatrical gouache look and voice rules — 原來如此事務所定案升級版劇場動畫光影×厚塗水粉畫風與生圖／語音固定配置"
status: done
priority: P2
area: docs
owner: antigravity-sothatswhy-rules
claimed_at: 2026-11-14T08:34:49Z
created_at: 2026-11-14T08:34:48Z
completed_at: 2026-11-14T08:52:00Z
branch: antigravity/sothatswhy-texture-and-voice-rules
depends_on: []
scope:
  - AGENTS.md
  - docs/videos/lessons/sothatswhy.md
  - docs/videos/so-thats-why/CURRENT.md
  - docs/videos/so-thats-why/look.md
  - docs/videos/so-thats-why/dialogue-pilot-20261103/README.md
  - docs/videos/so-thats-why/dialogue-pilot-20261103/HANDOFF.md
---

# 原來如此事務所：定案升級版「劇場級動畫光影 × 厚塗水粉質感」（內建生圖不走 MiniMax）與 Gemini 中文＋MiniMax 八語配音

## Why

在製作 `sothatswhy-p12-qr-code` 期間，站主對比舊版 MiniMax 圖（如 P21）與平塗繪本版後指出：舊版雖偶有透視或粉筆亂碼問題，但光影與筆觸質感較佳；經實測升級為「劇場級動畫光影 × 厚塗水粉質感」（暖深褐收尖細線、窗邊斜射暖金陽光＋金邊輪廓光與微塵、前景清晰＋背景奶油淺景深散景無黑框線、多層次布料與材質紋理）並以代理內建 `generate_image`（16:9 滿版＋角色設定圖參考）生圖匯入後，站主拍板「以後用這種的」，同時固定中文用 Gemini（`Sulafat`＋`Leda`）、八語配音用 MiniMax（`dub --provider minimax`）。把這套定案寫入系列規則檔、教訓檔與 `AGENTS.md`（每個新對話自動載入的頂層規則），之後任何新對話開工都會自動套用，無須手動貼提示詞。

## Definition of done

- [x] `docs/videos/so-thats-why/look.md`、`docs/videos/so-thats-why/CURRENT.md`、`docs/videos/so-thats-why/dialogue-pilot-20261103/README.md`、`HANDOFF.md` 與 `docs/videos/lessons/sothatswhy.md` 寫明 2026-11-14 定案（停用 MiniMax 生圖、改走內建 `generate_image`＋`keyframes import --provider external --usd 0`、五大質感配方與英文基底句、2 倍放大審圖、Gemini 中文＋MiniMax 八語配音）。
- [x] `AGENTS.md`（Where things are）補上 `sothatswhy-` 系列必讀入口，保持 `youtube-video/SKILL.md` 長片審查雜湊（`docs/videos/long-form/review.json`）不變。
- [x] `tools/video/long-form/review.test.mjs`、`npm run test:docs-videos`、`npm run check:tasks` 與 `node docs/videos/rules-sync/sync.mjs --dry-run` 全數通過。

## Steps

- [x] 更新 `docs/videos/lessons/sothatswhy.md` 記錄 2026-11-14 站主定案與升為規則檔案清單。
- [x] 更新 `docs/videos/so-thats-why/look.md`、`CURRENT.md`、`dialogue-pilot-20261103/README.md` 與 `HANDOFF.md` 的生圖路線、畫風基底句與語音規則。
- [x] 更新 `AGENTS.md` 頂層入口指引。
- [x] 通過 `long-form/review.test.mjs`、`test:docs-videos`、`check:tasks` 與 `rules-sync --dry-run` 後推送 PR。

## How to verify

```bash
npm run test:tools && npm run test:docs-videos && npm run check:tasks
node docs/videos/rules-sync/sync.mjs --dry-run
```

## Notes

- Claimed with `--force` because two stale `review` tickets (`2026-10-10-sothatswhy-minimax-images`, 836h stale with no active branch; `2026-11-03-sothatswhy-dialogue-pilot-p02`, >240h stale and already shipped) still list `docs/videos/so-thats-why/look.md` and `docs/videos/so-thats-why/dialogue-pilot-20261103` in their scopes. Checked `who-is-on-it.mjs` and open PRs before claiming: zero active sessions touch these files.
