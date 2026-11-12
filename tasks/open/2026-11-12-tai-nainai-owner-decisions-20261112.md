---
id: 2026-11-12-tai-nainai-owner-decisions-20261112
title: 恁祖媽今年18：套用站主 2026-11-12 的八項決定（書包、燈座、辮子、片長、童謠、第8集重拍、迴廊燈、正廳樓梯）
status: in-progress
priority: P1
area: docs
owner: claude-opus-5-5-elegant-ritchie
claimed_at: 2026-11-12T15:59:19Z
created_at: 2026-11-12T15:59:18Z
completed_at:
branch: claude/elegant-ritchie-vpnwqm
depends_on: []
scope:
  - docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/s1-bible-e001-e060.md
  - docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/cast.json
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
---

# 恁祖媽今年18：套用站主 2026-11-12 的八項決定

## Why

第 9–60 集重寫與審稿後，bible〈要站主決定的〉留了八件事。主控提了建議，站主 2026-11-12 回「好」，八項照建議定案：
書包報信鈴在翻蓋圓銅扣旁；燈座改數字跟拍出來一致（第 41 集台詞跟著改）；照片全部一條辮；17 集超長接受；童謠 Kore 唸唱加古箏；
第 8 集只重拍 c12、c28；迴廊燈白燈罩小壁燈；正廳樓梯跟場景圖（左後角落地鐘旁）。

## Definition of done

- [x] 第 9–60 集 `script.md` 照八項改完，`storyboard-check.py` 0 ERROR、`parse_script.py` 讀得過。
- [x] bible〈要站主決定的〉改成已定，〈道具〉〈場景格局〉接點表跟上；`cast.json` 的 `baoxinling`、書包、`huiyi-1948`、`huaibiao`、`mihang-laozhao`、`shibasui-zhao`、`shenjia-zhengting`、`shenjia-huilang` 跟上。
- [x] 已拍的第 1–8 集不改，跟決定不同的地方記成已知瑕疵（在 bible 與 `2026-11-12-tai-nainai-e001-e008-shots-en`）。

## Steps

- [x] 四個代理分段改第 9–24、25–40、41–50、51–60 集；一個代理改 bible 與 `cast.json`。
- [x] 檢查、提交、推到 PR #2087。

## How to verify

```bash
python3 -I docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/storyboard-check.py docs/videos/tai-nainai-e0[0-6][0-9]/script.md
```

## Notes

- 第 8 集 c12、c28 重拍（約 6 CU）由製作端做，不在這張票。
- 2026-11-12 做完：四個代理套用八項到第 9–60 集、一個代理改 bible 與 `cast.json`；站主再說「你建議改都改」「品質為主，該修就修」，
  所以另派五個沒參與改稿的代理逐鏡審正廳樓梯牽動的集（第 10、18、21、23、24、28、29、41–45、49–57 集），約 40 鏡依機位修正左右、背景、前景、視線，台詞不動。
  審稿抓到主控寫錯的一條：「往南拍時樓梯在畫面右後」——樓梯在西北角，往南拍時在鏡頭背後右側、不入鏡；bible 已更正。
  第 41 集錢老闆那句改成「連燈帶座三十公分高，裝箱好搬。」（新錄）。60 集 storyboard-check 0 ERROR、parse_script 全讀得過、第 1–8 集 compile --check 都對得上。
- 製作端還要做：第 8 集重拍 c12 c28（約 6 CU）、第 22 集前童謠試聽、重畫一條辮的照片道具圖與 `prop-shubao-t1` 核對、場景圖同時畫出西北角樓梯與北牆西端院子門。第 9–60 集的 `shots-en.json` 仍要照新稿重產。
