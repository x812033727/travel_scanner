---
id: 2026-11-05-zhong-tian-e056-route-a-clips
title: Zhong-tian e056: route A clips on RunPod, cut, import, dubs and publish package
status: in-progress
priority: P2
area: docs
owner: claude-opus-5.5-zt-e043
claimed_at: 2026-11-05T03:41:01Z
created_at: 2026-11-05T03:41:00Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e056.json
---

# Zhong-tian e056: route A clips on RunPod, cut, import, dubs and publish package

## Why

第 56 集（36 鏡）照第 43–55 集的做法走 RunPod 路線 A（`tasks/done/2026-11-01-zhong-tian-e043-route-a-clips.md`），一台長開的 pod 接力（`_scripts/chain.sh st23:55 st1:56`）。

## Definition of done

- [ ] 36 鏡 1080p 片段，紀錄在 `colab/runs/e056/`
- [ ] 剪接、匯入、站主核准；八語、上架包核准

## Steps

- [ ] 錄台詞、剪接表
- [ ] 第一段（chain）、審、重抽
- [ ] 第二、三段、剪接、匯入

## How to verify

`/admin/videos` 上第 56 集核准。

## Notes

2026-11-05 收尾交接：第一段審完、重抽 9 鏡（兩輪），選鏡見 `colab/runs/e056/review-st1.md`、`takes.tsv`；第二、三段 09:38 開始、收尾時讓它跑完，跑完由 scratchpad 的 finish56.sh 停 pod（`~/mokaair-work/videos/finish56.log`）。
接著要做：確認 final/ 有 36 支 `_1080.mp4`（不夠就 `bash colab/runs/_scripts/st23-retry.sh 56 560000 $(cat <runpod/a>/st2-seeds.txt)`）→ `stage-clips.sh 56`（沒有剪頭）→ s02 `crop=1500:844:420:0`（燒的信有字）→ `asm.sh 056` → `prep-import.mjs 56`（改 meta.json 的 note）→ `import --from` → 站主審成片。台詞已錄、剪接表 `hailuo/edit-dh-e056.json` 已寫。
2026-11-05 12:17 UTC：站主說第 56 集升 1080p 先不用跑（「因為可能會重做」，等第 1 集 r2 的結果決定第一季要不要照新寫法重做）。升 1080p 停在 19／36 鏡（`final/` 有 19 支，第二段 refine 36 支都在 `st2/refined/`）；剪接、匯入暫停。要接著做時：`bash .agents/skills/minimax-h3-runpod/scripts/route_a_st23.sh 56 560000 $(cat <runpod/a>/st2-seeds.txt)` 只會補剩下的 17 支。
