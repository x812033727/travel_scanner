---
id: 2026-11-14-curio-audience-critic-gate-p17
title: curio audience critic gate — 將獨立一般觀眾評分挑刺設為推後台與備份前必經關卡並收錄 P17 教訓
status: done
priority: P2
area: docs
owner: antigravity-curio-audience-gate
claimed_at: 2026-11-14T13:47:22Z
created_at: 2026-11-14T13:47:04Z
completed_at: 2026-11-14T13:48:26Z
branch: antigravity/curio-audience-critic-gate
depends_on: []
scope:
  - AGENTS.md
  - .agents/skills/curio-episode/SKILL.md
  - .claude/skills/curio-episode/SKILL.md
  - docs/videos/explainer-series/README.md
  - docs/videos/history-curiosity/README.md
  - docs/videos/history-curiosity/look.md
  - docs/videos/lessons/explainer.md
---

# 將「獨立一般觀眾視角評分挑刺與修正」納入解說片推後台與備份前必經關卡，並收錄 P17 實戰教訓

## Why

在 `curio-p17`（1666 倫敦大火與 666 預言）製作過程中，站主要求請獨立代理以一般觀眾視角評分內容與影片觀感，一次抓出機器 `lint`／`qa` 不會攔截、卻讓真實觀眾一秒出戲的五類問題（縮圖大標 9 單位導致字級過小裁字與外語副標單字孤行、古典英文姓氏 `Pepys` 未補音標式英文讀法導致全片飄出三種發音、同一集前段混留舊版大頭卡通與後段新版厚塗水粉、火災／審訊場誤套午後悠閒暖陽、17 世紀出現現代橡膠腳輪手推車與對折賀卡式信件），並明確拍板「把觀眾評分加入流程，修完後才推後台跟備份」。由於 PR #2106 已先合併至 `main`，需另開乾淨的後續票把這道必經關卡與五條實戰教訓正式寫入共用規則與教訓檔。

## Definition of done

- [x] `AGENTS.md`、`.agents/skills/curio-episode/SKILL.md`、`.claude/skills/curio-episode/SKILL.md`（位元組完全一致）、`docs/videos/history-curiosity/look.md`、`docs/videos/history-curiosity/README.md` 與 `docs/videos/explainer-series/README.md` 明確規定：`assemble`＋`qa`（11/11）＋`package`（4/4）後必先過獨立一般觀眾視角評分挑刺（外包裝、內容聲音、視覺連貫各項目標 ≥ 8.5／10），全數修完並重過 `qa`＋`package` 後，才允許執行 `review-push` 推後台與 `todrive.sh` 備份雲端硬碟。
- [x] `docs/videos/lessons/explainer.md` 與上述規則檔收錄 `curio-p17` 五條觀眾體感實戰教訓（縮圖 `headline` 硬上限 ≤ 6 單位與外語 `sub` 零孤行、拼讀落差大的英文姓氏如 `Pepys` 於單集 `story-lexicon` 補 `"Peeps"` 音標讀法、同集 100% 統一畫風禁混新舊、災難／審訊場情緒光影對齊、17 世紀道具防現代腳輪與賀卡折頁穿幫）。
- [x] `node --test tools/skills.test.mjs`、`node tools/tasks.mjs check` 與 `node docs/videos/rules-sync/sync.mjs --ref HEAD --dry-run` 全數通過。

## Steps

- [x] 在 `AGENTS.md`、`curio-episode` skill（含 `.claude/skills` 鏡像）、`docs/videos/history-curiosity/{look,README}.md`、`docs/videos/explainer-series/README.md` 補入成片獨立一般觀眾視角評分必經關卡與五項體感防呆。
- [x] 在 `docs/videos/lessons/explainer.md` 頂端新增 `2026-11-14 · curio-p17` 觀眾視角評分教訓紀錄。
- [x] 執行 `skills.test.mjs`、`tasks.mjs check` 與 `rules-sync/sync.mjs --dry-run` 驗證通過後結案發 PR。

## How to verify

```bash
node --test tools/skills.test.mjs
node tools/tasks.mjs check
node docs/videos/rules-sync/sync.mjs --ref HEAD --dry-run
```

## Notes

- PR #2106 已於 `2026-11-14T11:07:25Z` 合併進 `main`（`c166cb8ac`），本票基於最新 `origin/main` 開立獨立後續 PR（`no-auto-merge`），確保不改動已結案舊票、且所有路徑無其他活躍 session 或開著的 PR 衝突（`docs/videos/lessons/curio.md` 仍避開未合併的 PR #2101）。
