---
id: 2026-11-12-tai-nainai-e001-e008-recover-v2
title: 恁祖媽今年18 第1-8集：把雲端上的新版分鏡收回 repo
status: in-progress
priority: P1
area: docs
owner: claude-opus-5-5-elegant-ritchie
claimed_at: 2026-11-12T14:12:14Z
created_at: 2026-11-12T14:11:24Z
completed_at:
branch: claude/elegant-ritchie-vpnwqm
depends_on: []
scope:
  - docs/videos/tai-nainai-e001/script.md
  - docs/videos/tai-nainai-e002/script.md
  - docs/videos/tai-nainai-e003/script.md
  - docs/videos/tai-nainai-e004/script.md
  - docs/videos/tai-nainai-e005/script.md
  - docs/videos/tai-nainai-e006/script.md
  - docs/videos/tai-nainai-e007/script.md
  - docs/videos/tai-nainai-e008/script.md
  - docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/s1-bible-e001-e060.md
---

# 恁祖媽今年18 第1-8集：把雲端上的新版分鏡收回 repo

## Why

站主 2026-11-08 要求祖媽改用種田拍法，製作端已經把第 1–8 集重拆鏡頭並拍完（雲端硬碟 `AI劇/恁祖媽今年18/第00N集/製作檔/`），
但新版中文分鏡只留在製作 session 的工作區，main 上第 1–8 集的 `script.md` 還是 11/6 的舊版（一集 22–28 鏡）。
沒有新版分鏡，第 9 集以後的重寫（`2026-11-12-tai-nainai-e009-e014-rewrite`）就沒有範本、也沒有第 8 集結尾的接點；以後重拍第 1–8 集的某一鏡也沒有中文分鏡可對。

## Definition of done

- [ ] 第 1–3 集：雲端上找得到的最新中文分鏡原文放回 `script.md`。
- [ ] 第 4–8 集：中文稿沒有備份，從雲端的英文提示詞、字幕與舊稿反推成同格式的 `script.md`，開頭寫明是反推稿與來源。
- [ ] 每集 `storyboard-check.py` 0 ERROR。
- [ ] `s1-bible-e001-e060.md` 的接點表改成新鏡號，第 8→9 集的接點照第 8 集實際的最後一鏡。

## Steps

- [ ] 第 1 集：`tn-e001/_scratchpad/e001-partA.md` + `e001-partB.md`（48 鏡）。
- [ ] 第 2 集：`tn-shared/_scratchpad/e2-script.pass2`（50 鏡，對得上 `e002v2a/prompts` c01–c50）。
- [ ] 第 3 集：`tn-shared/_scratchpad/e3-script.pass1`（51 鏡，含 c32b、c36b，對得上 `e003v2a/prompts`）。
- [ ] 第 4–8 集反推稿。
- [ ] bible 接點表。

## How to verify

```bash
python3 -I docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/storyboard-check.py docs/videos/tai-nainai-e00[1-8]/script.md
```

鏡號對雲端的 `e00Nv2a/prompts/`（或該集實際用的 prompts 資料夾）逐一對得上。

## Notes

- 2026-11-12 認領時兩張 11/6 的舊票（`2026-11-06-tai-nainai-rename-title`、`2026-11-06-tai-nainai-change-ageing-opening`，owner claude-opus-5-5）仍鎖著這些路徑；
  它們的工作已在 #2032、#2035 合進 main、認領過期六天，站主同意用 `--force` 認領。舊票本身沒動。
- 雲端上的新版中文稿只有第 1–3 集；第 2、3 集取的是 `tn-shared/_scratchpad` 裡最後一輪（`pass2`、`pass1`），之後製作端的 v2b、ff2 若再改過字，中文稿沒有留下來。
  第 4 集的 47 鏡只有英文（`tn-e004/_scratchpad/e004-gen-en.py`），第 5–8 集只有 `prompts/`。PR #2047、#2038 都沒有分鏡。
- 第 1–8 集的 `shots-en.json`、`video.json`、`brief.md` 還是舊版，不在這張票的 scope（`compile.py` 看到中文改了、英文沒跟上會停）；製作端已經拍完這幾集，需要時再照新稿重產。
