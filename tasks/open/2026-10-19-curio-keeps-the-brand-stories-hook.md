---
id: 2026-10-19-curio-keeps-the-brand-stories-hook
title: Curio keeps the brand stories' hook cadence and music bed
status: review
priority: P1
area: tools
owner: claude-opus-5-5-quirky
claimed_at: 2026-10-19T01:10:56Z
created_at: 2026-10-19T01:09:33Z
completed_at:
branch: claude/quirky-files-optimization-1605cd
depends_on: []
scope:
  - tools/video/core/narrative.mjs
  - tools/video/core/narrative.test.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/curio.mjs
  - tools/video/core/curio.test.mjs
  - tools/video/automation/explainer-series.mjs
  - tools/video/automation/explainer-series.test.mjs
  - .agents/skills/curio-episode
  - .claude/skills/curio-episode
---

# Curio keeps the brand stories' hook cadence and music bed

## Why

站主 2026-10-19：「目前看起來品牌故事比奇聞檔案局好很多，內容也感覺比較順也有比較多鉤子，而且有音樂」，
要奇聞檔案局做到一樣好或更好，兩個系列都再成長。量到的差距：

- 品牌故事的撰稿規則是每 30–45 秒一個鉤子、十分鐘 8 個伏筆、章末停在沒解的問題上
  （`tools/video/automation/story-prompts.mjs` 的 `STORY_HOOK_RULES`）；奇聞檔案局的撰稿提示與 lint 都還是 90 秒、3 個。
  H10、H11、H12、M09、U09、H01 v2 最長空檔 69–81 秒，每集 2–7 段超過 45 秒。
- 品牌故事每一集由工人自動加配樂（`story.mjs` 的 `STORY_MUSIC`）；奇聞檔案局每一支 `video.json` 都沒有 `music`，
  本機製作包還把配樂寫成「不在授權內」。
- lint 對品牌故事也只用 90 秒、3 個（票 `2026-10-17-warn-brand-stories-at-45-second`）。

## Definition of done

- [x] lint 對品牌故事（`kind: story`）與 curio- slug 用 45 秒、十分鐘 8 個伏筆警告；其他旁白影片維持 90 秒、3 個。
- [x] curio- slug 沒有 `music` 時 lint 警告，給系列的配樂設定（`CURIO_MUSIC`，音量同品牌故事）。
- [x] 主機奇聞檔案局撰稿提示（`explainer-mystery`）加入同樣的鉤子節奏、章末懸念與「設定開著配樂就一定寫 music」；
      聖經的「鉤子」改成十分鐘至少 8 個。原來如此的提示字一個不動。
- [x] `curio-episode` skill 寫下鉤子與配樂的做法與預算。

## How to verify

```bash
node --test tools/video/core/narrative.test.mjs tools/video/core/curio.test.mjs tools/video/core/lint.test.mjs tools/video/automation/explainer-series.test.mjs tools/skills.test.mjs
node tools/video/cli.mjs lint --slug curio-h10   # 0 errors；超過 45 秒的段落與缺配樂是警告
```

## Notes

- **部署前**：`planner:bible-explainer-mystery`、`writer:explainer-mystery`、`planner:discuss-mystery`、`writer:discuss-mystery`
  四段提示字的 digest 變了；主機上不能有未完成的 cute-mystery 單集，否則那一階段會再問一次、再付一次。
- 警告不會自己觸發重寫（`flow.mjs` 的 `lintWarnings` 只跟著錯誤要求的重寫一起送），所以收緊不會多花撰稿呼叫。
- 偵測器沿用 `hookCadenceProblems`：問號、升級、預告、章節轉折都算；它只指出要讀的段落，不證明那是好鉤子。
- 認領時 scope 跟三張停在 in-progress 的舊票重疊（`2026-10-14-ai-and-tech-videos-tell-one` #1504、
  `2026-10-17-story-narrative-panel-asks-two-independent` #1562、`2026-10-14-curio-episodes-keep-the-series-look` #1500），
  三個 PR 都已合併，所以用 `--force`。
- 主機路線的 `settle()` 還沒有強制加配樂、主機奇聞檔案局盲評還是一位讀者：`flow.mjs` 在別人的票裡，開了
  `2026-10-19-host-explainer-route-always-adds-the`。
- 已交付的集數要不要補配樂（一首約 US$0.15＋重新合成，旁白與插圖不動）等站主決定。
- PR https://github.com/x812033727/travel_scanner/pull/1577
