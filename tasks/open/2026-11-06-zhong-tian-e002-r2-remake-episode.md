---
id: 2026-11-06-zhong-tian-e002-r2-remake-episode
title: Zhong-tian e002 r2: remake episode 2 (r2 script), stage 2 only, zh cut for the owner
status: in-progress
priority: P2
area: docs
owner: claude-opus-5.5-zt-e043
claimed_at: 2026-11-06T02:05:27Z
created_at: 2026-11-06T02:05:14Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e902.json
---

# Zhong-tian e002 r2: remake episode 2 (r2 script), stage 2 only, zh cut for the owner

## Why

Describe the problem in the terms someone who has never seen it would need.

## Definition of done

- [ ] The observable outcome, not the implementation.

## Steps

- [ ] First sub-task.
- [ ] Second sub-task.

## How to verify

The exact commands or clicks that prove it works.

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.

站主 2026-11-06：第 1 集 r2「這集我算滿意」，接著做第 2 集。預算 RunPod **上限 US$28**（估 US$22–26），超過先停下來回報。
做法照第 1 集 r2（`tasks/open/2026-11-05-zhong-tian-e001-r2-remake-episode.md`、`docs/videos/zhong-tian-qu-qi-e001-r2/brief.md`）：只做到第二段 1312×736、中文配音、不放片名卡、24 fps，剪完量數字，`import --from` 只送成片給站主看。

- 內部工作編號 902：工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e902-dh/`、`hailuo/*-dh-e902.json`、`colab/runs/e902/`；
  `docs/videos/zhong-tian-qu-qi-e902` 是本機指向 `zhong-tian-qu-qi-e002-r2` 的連結（`.git/info/exclude`）。
- 規格 `writer-tools/e002-r2/r2.py`，用 `writer-tools/e001-r2/build-r2.py <spec 路徑>` 產生製作檔。
- 阿令「沒戴鐵鐐」不另畫定妝照：她的定妝照是胸像、本來就沒有鐵鐐（第 1 集的鐵鐐是正文寫的）。
- 錢員外 `cast.json` 基本造型拿掉「身後兩個家丁」（跟二牛扁擔同一種錯：道具寫進基本造型）。

- [x] 規格與免費檢查（preflight 0 error、0 warning）
- [x] 配音（中文整句，38 句，句內語速中位 4.2 字／秒）
- [x] 第一段草稿（每鏡兩個種子），挑片（`colab/runs/e902/picks.tsv`）
- [x] 第二段精修
- [x] 剪接、cut-qa、量成片
- [x] `import --from`，備註「第 2 集重製版 r2，對照原版第 2 集」（2026-11-06 08:20，等站主看）
- 錢員外的三句錄出來 7.4–7.8 秒（他說得慢），`BUY` 補成 s06 8、s27 10、s29 10、s30 8、s33 10、s38 8（另有 s03 8、s34 10）。
- 2026-11-06 02:10 起第一段草稿：41 鏡 × 兩個種子（9020101／102）共 82 支，`colab/runs/e902/v1/spec.json`，pod fpfiyl95634b56。
  `retake-run.sh` 用 `setsid nohup` 跑（背景工作兩小時會被砍，這批要約四小時）。
- 挑片排除：s13 02（中途從眼睛特寫跳成中景）、s35 01（跳成全景再跳夜景）、s27 02（開頭是村民背影）。s12 用 02（阿令轉身走開）、s36 用 02（手擋著嘴）。
- s40 兩支都不行（柴刀沒飛、唐小棠在笑）：改寫正文（家丁拖著害怕的唐小棠、柴刀最後才從左邊飛進來），`fix1` 重抽，用 9020201。剪的時候要從片段後段起，柴刀才在 3 秒裡。
- 05:55 起第二段精修 41 鏡（`setsid nohup`，跑完自動停 pod）。

## 結果

| | r2 第 2 集 |
| --- | --- |
| 片長 | 190.2 s |
| 鏡數 | 41（c13 拆 c13、c13b） |
| 鏡長中位 | 4.4 s |
| 鏡內動量中位 | 8.3（目標 ≥ 7） |
| 靜止幀 | 4%（目標 ≤ 15%） |
| 平均每句字數 | 16.7（字幕 37 條、619 字） |
| 響度 | -13.7 LUFS，峰值 -1.4 dBFS |
| 幀率 | 24/1，無黑幀、無 held |
| 花費 | RunPod US$15.13（草稿 82 支 + s40 重抽 2 支 + 精修 41 鏡，同一個 pod 02:13–08:03） |

`cut-qa.py` 0 problem(s)。整片每鏡中間一格看過；c40 柴刀在半空收尾（`stage-clips-args.txt`：`s40@2.0`）。原版第 2 集本機沒有檔，沒有並排量。
工作分支 `claude/zt-e002-r2`，工作資料夾備份 `transfer/zt-e902-media`。
