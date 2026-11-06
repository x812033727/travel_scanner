---
id: 2026-11-06-tai-nainai-change-ageing-opening
title: 恁祖媽今年18 變更單：老化記號放大＋插鏡、第 1 集開場四鏡
status: in-progress
priority: P1
area: docs
owner: claude-opus-5-5
claimed_at: 2026-11-06T17:15:41Z
created_at: 2026-11-06T17:15:40Z
completed_at:
branch: claude/intelligent-gates-9n92xm
depends_on: []
scope:
  - docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/cast.json
  - docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/s1-bible-e001-e060.md
  - docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/screen-test/decisions.md
  - docs/videos/tai-nainai-e001/script.md
  - docs/videos/tai-nainai-e001/shots-en.json
  - docs/videos/tai-nainai-e001/video.json
  - docs/videos/tai-nainai-e001/brief.md
---

# 恁祖媽今年18 變更單：老化記號放大＋插鏡、第 1 集開場四鏡

## Why

站主 2026-11-06 看了 `production/screen-test/decisions.md` 後說「先依據擬建議的」：老化記號 A＋B；節奏照 11/05 規格（選 1），開場 10 秒至少四鏡照做。

## Definition of done

- [x] A：`cast.json` 的 `wrinkle`、`yaoju`、`faint-line`、`white-strand` 英文外貌放大記號；bible〈燈帳與她的樣子〉加〈記號在畫面上有多大〉；分鏡的中文用詞不改（155 處，改了會動到每一列的雜湊，也會跟 #2030 衝突）。
- [x] B：查過分鏡已經有記號出現與退掉的插鏡（第 30 集 c29、41 集 c21、48 集 c16、56 集 c25、57 集 c23），不加鏡。
- [x] 第 1 集開場：c01 拆成 c01（倒油的手，1.5 秒快拍）＋c01b（從供桌往門口、院子對面正廳的窗亮著，林美鳳的畫外笑話），`lint` 的 hook.opening 過了。
- [ ] 記號的參考圖：`white-strand` 胸像（以十八歲基本款為 image 1）、手背老人紋與淺紋的手部插鏡參考圖，下一個出圖 session 一起畫（約 0.5 CU）。
- [ ] 第 2–60 集開場也照四鏡：等各集 `shots-en.json` 寫好、`lint` 報 hook.opening 的再逐集改（每加一鏡約 0.5–0.9 CU 片段費）。

## How to verify

```bash
node tools/video/cli.mjs lint --slug tai-nainai-e001 | grep hook.opening   # 沒有這一行
python3 -I docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/storyboard-check.py docs/videos/tai-nainai-e001/script.md
```

## Notes

- 開場 10 秒不到四鏡（`lint` 的 hook.opening）的集，寫完英文正文時記在這裡，最後一起出變更單：e015（3 鏡）、e016（2 鏡）。

- 決策單原本說開場加鏡「用 source 切同一支片段、不多買」是錯的：同一支片段切開是同一個構圖，是跳接；已在 decisions.md 更正。
- 決策單原本說 B 要每集加一鏡，也錯了：分鏡本來就有。
