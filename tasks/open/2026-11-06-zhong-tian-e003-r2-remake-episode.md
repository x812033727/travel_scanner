---
id: 2026-11-06-zhong-tian-e003-r2-remake-episode
title: Zhong-tian e003 r2: remake episode 3 (r2 script), stage 2 only, zh cut for the owner
status: in-progress
priority: P2
area: docs
owner: claude-opus-5.5-zt-e043
claimed_at: 2026-11-06T06:12:58Z
created_at: 2026-11-06T06:12:57Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e903.json
---

# Zhong-tian e003 r2: remake episode 3 (r2 script), stage 2 only, zh cut for the owner

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

站主 2026-11-06：「就這樣一直做下去：完成、更新、下一集」，每集一條分支（`claude/zt-e00N-r2`）。預算照第 2 集，**上限 US$28**，超過先停下來回報。
做法照第 2 集 r2（`tasks/open/2026-11-06-zhong-tian-e002-r2-remake-episode.md`）。內部編號 903，`docs/videos/zhong-tian-qu-qi-e903` 是本機連結。

- 規格 `writer-tools/e003-r2/r2.py`（40 鏡、185 秒、35 句），配音已錄（中位 3.6 字／秒，所以 s04、s07、s08、s11、s13、s15 買 8 秒、s21 8、s22 10）。
- `colab/runs/e903/extras.json` 多一條：拿掉秦霜 cast 裡「腰帶插柴刀」，因為第 3 集開頭柴刀釘在門框上（s02、s03、s16 腰帶空著，s29 插回去）。
- 免費檢查 0 error、0 warning。

- [x] 規格、配音、免費檢查
- [x] 第一段草稿（每鏡兩個種子），挑片（`colab/runs/e903/picks.tsv`）
- [x] 第二段精修
- [x] 剪接、cut-qa、量成片
- [x] `import --from`，備註「第 3 集重製版 r2，對照原版第 3 集」（2026-11-06 16:15，等站主看）
- 2026-11-06 08:03 草稿開跑；容器約 08:20 前後重啟，跑完 4 支就斷，pod 空轉到被站台 60 分鐘停掉（約 US$2.6 白花）。10:30 重跑（已有的跳過），EU-CZ-1 沒貨，`scratchpad/chain903d.sh` 最多等 8 小時，抽完接真人版試拍的定妝照（同一個 pod）。
- 2026-11-06 12:45 站主：「真人版試拍不用試拍了」。排在草稿後的定妝照 manifest 改名成 `colab/runs/live-pilot/portraits.cancelled.json`，那一步會檢查失敗直接結束，不花錢。
- 挑片：s14、s19、s21、s25、s29 各有一支中途跳鏡，用另一支；s12 用 02（三根手指比清楚）。s01、s07 兩支動態都低（插鏡、坐著說話），照用。
- s39（本集最後一句）兩支都拍成全景：`fix1` 把場景長描述縮短、寫明「第一格就是阿令的臉與肩膀」，重抽用 9030202（低角度、短刀橫在膝上、推到臉）。
- 14:10 起第二段精修 40 鏡（跑完自動停 pod）。剪接表 `hailuo/edit-dh-e903.json`（tension／comedy／suspense，照稿的音效表）。

## 結果

| | r2 第 3 集 |
| --- | --- |
| 片長 | 166.0 s |
| 鏡數 | 40 |
| 鏡長中位 | 3.9 s |
| 鏡內動量中位 | 7.3（目標 ≥ 7） |
| 靜止幀 | 7%（目標 ≤ 15%） |
| 平均每句字數 | 16.1（字幕 31 條、499 字） |
| 響度 | -14.1 LUFS，峰值 -1.2 dBFS |
| 幀率 | 24/1，無黑幀、無 held |
| 花費 | RunPod 約 US$17（精修 pod 10:30–16:03 US$14.34 + 早上被容器重啟中斷、空轉的 pod 約 US$2.6） |

`cut-qa.py` 0 problem(s)；整片每鏡中間一格看過，面板字跟稿一致。工作分支 `claude/zt-e003-r2`，備份 `transfer/zt-e903-media`。
- 備份 `transfer/zt-e903-media`（680 MB；第一次因磁碟滿失敗，清出空間後重推成功）。
- 2026-11-06 站主看片：「第三集主角的手為什麼會有一顆一顆的?」——s06 許硯手背長出深色碎塊（稿子的「手背沾木屑」被畫成黏在皮膚上的碎片），s08 也有幾個小點。
  `r2.py` 拿掉木屑（改寫額頭有汗）；`colab/runs/e903/fix2` 重抽 s06、s08（種子 9030301／302，排在第 4 集草稿後同一個 pod），挑好後精修、重剪、重送後台。
- 教訓落地三處：`animation-preproduction/references/storyboard-shot-spec.md` 與 `production/storyboard-brief-for-planners.md` 各加「皮膚上的細小東西」一行；
  `preflight-prompts.py` 加 warn skin（木屑、泥點、血點等寫在手、臉、皮膚上就警告；用第 3 集舊 prompt 試過會擋、改後的不會）。
  main 上的 r2 稿子還有：第 17 集唐小棠、第 37–38 集秦霜「臉上沾灰」——拍到那幾集時改成「衣服上有灰」或確認抽出來沒有斑點。
- s06 用 `fix2` 9030302、s08 用 9030301（手乾淨）；舊的精修片與草稿移到 `st2/refined-woodchips`、`st1/out-woodchips`。
- 22:15 重剪（s06、s08 換成乾淨的手），cut-qa 0 problem(s)（動量 7.2、靜止 8%），`import --from --force` 重送後台，備註寫明是修正版。
- 修正版備份推到新分支 `transfer/zt-e903-media-fix`（702 MB；含 s06、s08 新片與舊的 `refined-woodchips`）。舊分支 `transfer/zt-e903-media` 是修正前，留著不動（覆蓋要強制推，不做）。
- 2026-11-07 連戲審查補做：`cut-jumps.py` 找到鏡頭開頭閃一下別的畫面，照 `stage-clips-args.txt` 從跳完後起剪，重剪後 cut-qa 0、cut-jumps 0，`import --from --force` 重送後台（備註寫明修正版）。
