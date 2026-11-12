---
id: 2026-11-12-tai-nainai-e001-e008-shots-en
title: 恁祖媽今年18 第1-8集：shots-en.json 與 cast.json 跟上收回的新版分鏡
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-11-12T14:43:25Z
completed_at:
branch:
depends_on:
  - 2026-11-12-tai-nainai-e001-e008-recover-v2
scope:
  - docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/cast.json
  - docs/videos/tai-nainai-e001/shots-en.json
  - docs/videos/tai-nainai-e002/shots-en.json
  - docs/videos/tai-nainai-e003/shots-en.json
  - docs/videos/tai-nainai-e004/shots-en.json
  - docs/videos/tai-nainai-e005/shots-en.json
  - docs/videos/tai-nainai-e006/shots-en.json
  - docs/videos/tai-nainai-e007/shots-en.json
  - docs/videos/tai-nainai-e008/shots-en.json
---

# 恁祖媽今年18 第1-8集：shots-en.json 與 cast.json 跟上收回的新版分鏡

## Why

`2026-11-12-tai-nainai-e001-e008-recover-v2` 把第 1–8 集照種田拍法的新版中文分鏡收回 repo（第 1–3 集原稿、第 4–8 集反推），
但 repo 裡這八集的 `shots-en.json`（還有 `video.json`、`brief.md`）仍是 11/6 舊稿的鏡號（23–28 鏡），`compile.py` 一跑就會停；
實際送出的英文在雲端硬碟 `AI劇/恁祖媽今年18/第00N集/製作檔/` 的 `prompts/` 與 `e004-gen-en.py` 這類檔裡。
兩位獨立審稿者另外建議 `cast.json` 跟成片或裁定對齊：垃圾桶、廚房與洗衣間（滾筒洗衣機、鐵皮盆）、福伯第 1 集中灰的註記、
十八歲照片 `shibasui-zhao` 刪掉「as in huiyi-1948-t1」、書包報信鈴（等站主決定 `prop-shubao-t1`）。

## Definition of done

- [ ] 第 1–8 集 `shots-en.json` 照新版中文稿的鏡號，正文取自雲端實際送出的英文；`compile.py N` 與 `lint` 0 錯。
- [ ] `cast.json` 照 recover 票 bible 補定的裁定修改，`video.json` 重產。

## Steps

- [ ] 從雲端 `prompts/` 取每鏡實際送出的英文（反推稿〈這版改了什麼〉列了每集的來源資料夾）。
- [ ] 改 `cast.json`；重跑 `compile.py`、`lint`。

## How to verify

`python3 -I docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/tools/compile.py N` 與 lint 0 錯；鏡號跟 `script.md` 一致。

## Notes

- `video.json`、`brief.md` 由 `compile.py` 產生，不在 scope 裡列，重產時一起提交（要先把它們加進 scope）。
