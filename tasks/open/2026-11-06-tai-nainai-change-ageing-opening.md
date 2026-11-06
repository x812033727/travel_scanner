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
  - docs/videos/tai-nainai-e002/script.md
  - docs/videos/tai-nainai-e003/script.md
  - docs/videos/tai-nainai-e004/script.md
  - docs/videos/tai-nainai-e005/script.md
  - docs/videos/tai-nainai-e006/script.md
  - docs/videos/tai-nainai-e007/script.md
  - docs/videos/tai-nainai-e008/script.md
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
- [ ] 站主 2026-11-06「全部」：第 2–60 集開場也照四鏡（50 集裡除第 1 集外的 49 集）：等各集 `shots-en.json` 寫好、`lint` 報 hook.opening 的再逐集改（每加一鏡約 0.5–0.9 CU 片段費）。

## How to verify

```bash
node tools/video/cli.mjs lint --slug tai-nainai-e001 | grep hook.opening   # 沒有這一行
python3 -I docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/storyboard-check.py docs/videos/tai-nainai-e001/script.md
```

## Notes

- 站主 2026-11-06 回覆：第一章缺的參考圖「好」、開場四鏡「全部」、整季預算「可以」（片段 1312×736，估 1,300–1,500 CU）。

- 開場 10 秒不到四鏡（`lint` 的 hook.opening）的集，寫完英文正文時記在這裡，最後一起出變更單：全季 60 集裡 50 集（第 1 集已改；沒有的是 e010、e011、e014、e022、e029、e046、e056、e057、e058）。多數 3 鏡、少數 2 鏡。每集多一支短片段約 0.5–0.9 CU，50 集約 25–45 CU，要站主點頭。

- 決策單原本說開場加鏡「用 source 切同一支片段、不多買」是錯的：同一支片段切開是同一個構圖，是跳接；已在 decisions.md 更正。
- 決策單原本說 B 要每集加一鏡，也錯了：分鏡本來就有。
