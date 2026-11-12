---
id: 2026-11-12-tai-nainai-e009-e014-rewrite
title: 恁祖媽今年18 第9-60集：照種田拍法重寫分鏡並獨立審稿
status: in-progress
priority: P1
area: docs
owner: claude-opus-5-5-elegant-ritchie
claimed_at: 2026-11-12T14:21:13Z
created_at: 2026-11-12T14:11:30Z
completed_at:
branch: claude/elegant-ritchie-vpnwqm
depends_on:
  - 2026-11-12-tai-nainai-e001-e008-recover-v2
scope:
  - docs/videos/tai-nainai-e009/script.md
  - docs/videos/tai-nainai-e010/script.md
  - docs/videos/tai-nainai-e011/script.md
  - docs/videos/tai-nainai-e012/script.md
  - docs/videos/tai-nainai-e013/script.md
  - docs/videos/tai-nainai-e014/script.md
  - docs/videos/tai-nainai-e015/script.md
  - docs/videos/tai-nainai-e016/script.md
  - docs/videos/tai-nainai-e017/script.md
  - docs/videos/tai-nainai-e018/script.md
  - docs/videos/tai-nainai-e019/script.md
  - docs/videos/tai-nainai-e020/script.md
  - docs/videos/tai-nainai-e021/script.md
  - docs/videos/tai-nainai-e022/script.md
  - docs/videos/tai-nainai-e023/script.md
  - docs/videos/tai-nainai-e024/script.md
  - docs/videos/tai-nainai-e025/script.md
  - docs/videos/tai-nainai-e026/script.md
  - docs/videos/tai-nainai-e027/script.md
  - docs/videos/tai-nainai-e028/script.md
  - docs/videos/tai-nainai-e029/script.md
  - docs/videos/tai-nainai-e030/script.md
  - docs/videos/tai-nainai-e031/script.md
  - docs/videos/tai-nainai-e032/script.md
  - docs/videos/tai-nainai-e033/script.md
  - docs/videos/tai-nainai-e034/script.md
  - docs/videos/tai-nainai-e035/script.md
  - docs/videos/tai-nainai-e036/script.md
  - docs/videos/tai-nainai-e037/script.md
  - docs/videos/tai-nainai-e038/script.md
  - docs/videos/tai-nainai-e039/script.md
  - docs/videos/tai-nainai-e040/script.md
  - docs/videos/tai-nainai-e041/script.md
  - docs/videos/tai-nainai-e042/script.md
  - docs/videos/tai-nainai-e043/script.md
  - docs/videos/tai-nainai-e044/script.md
  - docs/videos/tai-nainai-e045/script.md
  - docs/videos/tai-nainai-e046/script.md
  - docs/videos/tai-nainai-e047/script.md
  - docs/videos/tai-nainai-e048/script.md
  - docs/videos/tai-nainai-e049/script.md
  - docs/videos/tai-nainai-e050/script.md
  - docs/videos/tai-nainai-e051/script.md
  - docs/videos/tai-nainai-e052/script.md
  - docs/videos/tai-nainai-e053/script.md
  - docs/videos/tai-nainai-e054/script.md
  - docs/videos/tai-nainai-e055/script.md
  - docs/videos/tai-nainai-e056/script.md
  - docs/videos/tai-nainai-e057/script.md
  - docs/videos/tai-nainai-e058/script.md
  - docs/videos/tai-nainai-e059/script.md
  - docs/videos/tai-nainai-e060/script.md
  - docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/s1-bible-e001-e060.md
  - docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/REVIEW.md
  - docs/videos/lessons/tai-nainai.md
---

# 恁祖媽今年18 第9-60集：照種田拍法重寫分鏡並獨立審稿

## Why

站主 2026-11-08：祖媽「以後應該也要都用這樣的拍法」（`production/RULES.md` 第三之一節）。第 1–8 集製作端已經照種田拍法重拆、拍完；
main 上第 9–60 集的 `script.md` 還是 11/6 的舊版（一集 20–37 鏡、平均約 4.5–5 秒、每分鐘 12–13 鏡），開拍前要照審劇本流程
（`.agents/skills/animation-preproduction/references/script-to-storyboard.md`）重寫並過獨立審稿。站主 2026-11-12：可以開 20 個子代理一起做；第 1–8 集有要改的也可以改，改動由站主轉告製作端。

## Definition of done

- [ ] 第 9–60 集每集照種田拍法：約 2.5–3 秒一鏡、每鏡一個看得見的動作、剪在動作中間、每場全景→過肩反打→插鏡→反應；台詞字與說話人沿用舊稿，除非審稿必修。
- [ ] 每集 `storyboard-check.py` 0 ERROR。
- [ ] 每段四集、相鄰重疊一集的獨立審稿做完，必修改完，每集記「審稿後的修改」。
- [ ] 系列設定補「寫稿中補定的事」（第 9–60 集，種田拍法版）與要站主決定的事。

## Steps

- [ ] 等 `2026-11-12-tai-nainai-e001-e008-recover-v2`：第 8 集實際的最後一鏡（9 的接點）。
- [ ] 寫稿：每位寫稿代理連續約五集。
- [ ] 程式檢查。
- [ ] 獨立審稿（每段四集、重疊一集）。
- [ ] 改稿（交回原寫稿者）、掃全季。
- [ ] 收尾：bible、PR 說明。

## How to verify

```bash
python3 -I docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/storyboard-check.py docs/videos/tai-nainai-e0[0-6][0-9]/script.md
```

## Notes

- 第 9–60 集的 `shots-en.json`、`video.json`、`brief.md` 是舊稿產生的，改稿後會跟中文對不上（`compile.py` 會停）；製作端每集開拍時照新稿重產英文，不在這張票。
