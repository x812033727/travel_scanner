---
id: 2026-11-06-tai-nainai-rename-title
title: 恁祖媽今年18：中文劇名從《祖奶奶今年十八》改名
status: in-progress
priority: P1
area: docs
owner: claude-opus-5-5
claimed_at: 2026-11-06T17:03:04Z
created_at: 2026-11-06T17:03:03Z
completed_at:
branch: claude/intelligent-gates-9n92xm
depends_on: []
scope:
  - docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai
  - docs/videos/series-plans/top40-2025-2026/README.md
  - docs/videos/series-plans/top40-2025-2026/rankings.json
  - .agents/skills/minimax-h3-colab/references/lessons.md
  - tasks/open/2026-11-06-tai-nainai-screen-test.md
  - tasks/open/2026-11-06-tai-nainai-production-tools.md
  - docs/videos/tai-nainai-e001
  - docs/videos/tai-nainai-e002
  - docs/videos/tai-nainai-e003
  - docs/videos/tai-nainai-e004
  - docs/videos/tai-nainai-e005
  - docs/videos/tai-nainai-e006
  - docs/videos/tai-nainai-e007
  - docs/videos/tai-nainai-e008
  - docs/videos/tai-nainai-e009
  - docs/videos/tai-nainai-e010
  - docs/videos/tai-nainai-e011
  - docs/videos/tai-nainai-e012
  - docs/videos/tai-nainai-e013
  - docs/videos/tai-nainai-e014
  - docs/videos/tai-nainai-e015
  - docs/videos/tai-nainai-e016
  - docs/videos/tai-nainai-e017
  - docs/videos/tai-nainai-e018
  - docs/videos/tai-nainai-e019
  - docs/videos/tai-nainai-e020
  - docs/videos/tai-nainai-e021
  - docs/videos/tai-nainai-e022
  - docs/videos/tai-nainai-e023
  - docs/videos/tai-nainai-e024
  - docs/videos/tai-nainai-e025
  - docs/videos/tai-nainai-e026
  - docs/videos/tai-nainai-e027
  - docs/videos/tai-nainai-e028
  - docs/videos/tai-nainai-e029
  - docs/videos/tai-nainai-e030
  - docs/videos/tai-nainai-e031
  - docs/videos/tai-nainai-e032
  - docs/videos/tai-nainai-e033
  - docs/videos/tai-nainai-e034
  - docs/videos/tai-nainai-e035
  - docs/videos/tai-nainai-e036
  - docs/videos/tai-nainai-e037
  - docs/videos/tai-nainai-e038
  - docs/videos/tai-nainai-e039
  - docs/videos/tai-nainai-e040
  - docs/videos/tai-nainai-e041
  - docs/videos/tai-nainai-e042
  - docs/videos/tai-nainai-e043
  - docs/videos/tai-nainai-e044
  - docs/videos/tai-nainai-e045
  - docs/videos/tai-nainai-e046
  - docs/videos/tai-nainai-e047
  - docs/videos/tai-nainai-e048
  - docs/videos/tai-nainai-e049
  - docs/videos/tai-nainai-e050
  - docs/videos/tai-nainai-e051
  - docs/videos/tai-nainai-e052
  - docs/videos/tai-nainai-e053
  - docs/videos/tai-nainai-e054
  - docs/videos/tai-nainai-e055
  - docs/videos/tai-nainai-e056
  - docs/videos/tai-nainai-e057
  - docs/videos/tai-nainai-e058
  - docs/videos/tai-nainai-e059
  - docs/videos/tai-nainai-e060
---

# 恁祖媽今年18：中文劇名從《祖奶奶今年十八》改名

## Why

站主 2026-11-06：「中文劇名改恁祖媽今年18」。原本的《祖奶奶今年十八》是 `plan.json` 的暫定候選。

## Definition of done

- [x] 企劃、系列設定、角色表、60 集 `script.md`、第 1 集 `video.json`／`brief.md`、製作工具、試鏡文件、`lessons.md`、top40 的 README 與 rankings 都改成《恁祖媽今年18》（92 處）。
- [x] `plan.json`：`title` 改新名，`title_candidates` 留舊名，`title_decision` 記站主的決定。
- [x] `tasks/done/` 的舊票是歷史紀錄，不改。

## Steps

- [x] 全文取代，`plan.json` 手改。
- [x] `lib/validate.mjs`、`lib/build.mjs --check`、`storyboard-check.py`（60 集 0 ERROR）、`compile.py 1` 與 `lint`（0 錯）。

## How to verify

```bash
git grep -n "祖奶奶今年十八" -- docs tasks/open .agents   # 只剩 plan.json 的候選與決定紀錄
node docs/videos/series-plans/top40-2025-2026/lib/validate.mjs docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai
```

## Notes

- slug、資料夾與檔名（`tai-nainai-eNNN`、`2025-01-tai-nainai`）不改：它們是 id，改了會斷掉站台與工作資料夾的對應。
- 劇名用「恁祖媽」（台語自稱「你祖母我」的口吻）。bible 寫台詞「不罵髒話」；這三個字只在劇名，台詞沒有用到。
