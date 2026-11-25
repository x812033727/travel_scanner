---
id: 2026-11-06-zhong-tian-e004-r2-remake-episode
title: Zhong-tian e004 r2: remake episode 4 (r2 script), stage 2 only, zh cut for the owner
status: in-progress
priority: P2
area: docs
owner: claude-opus-5.5-zt-e043
claimed_at: 2026-11-06T14:20:39Z
created_at: 2026-11-06T14:20:36Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e904.json
---

# Zhong-tian e004 r2: remake episode 4 (r2 script), stage 2 only, zh cut for the owner

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

站主 2026-11-06：「就這樣一直做下去：完成、更新、下一集」，每集一條分支（`claude/zt-e00N-r2`）。預算照第 2、3 集，**上限 US$28**。做法照第 3 集 r2。內部編號 904。

- 規格 `writer-tools/e004-r2/r2.py`（40 鏡、194.8 秒、40 句），配音已錄（中位 3.5 字／秒）；BUY：s03、s13、s37 長鏡 8，s10、s35 8，s14 12、s15 10（照錄好的長度）。
- `colab/runs/e904/extras.json`：秦霜這集柴刀回到腰帶，不拿掉；二牛 c27–c28 背著大鍋，拿掉 cast 的「empty-handed」，每鏡構圖自己寫手上拿什麼。
- 黑影（s38、s40）沒有定妝照、不寫名字，只寫背光、臉在暗處。
- 免費檢查 0 error、0 warning。

- [x] 規格、配音、免費檢查
- [x] 第一段草稿（每鏡兩個種子），挑片（`colab/runs/e904/picks.tsv`；s03 從 1.5 秒起剪）
- [x] 第二段精修
- [x] 剪接、cut-qa、量成片
- [x] `import --from`，備註「第 4 集重製版 r2，對照原版第 4 集」（2026-11-06 22:15，等站主看）
- 草稿挑片時看到兩種新錯：s03 兩支開頭都畫出發光的系統面板（正文寫「面前空氣的淡藍光、不畫面板」）；s24 一支跳成中景、眼睛發藍光。s03 用 9040101 從 1.5 秒起剪（避開面板），s24 用 9040102（眼睛大特寫）。
  教訓落地：`storyboard-shot-spec.md`、`storyboard-brief-for-planners.md` 加一行；`preflight-prompts.py` 加 warn glow（第 2–4 集舊 prompt 會擋到 e903 s20、e904 s03）。
- 20:06 起第二段精修 40 鏡，接著精修第 3 集重抽的 s06、s08（`scratchpad/chain904r.sh`，最後停 pod）。

## 結果

| | r2 第 4 集 |
| --- | --- |
| 片長 | 170.8 s |
| 鏡數 | 40 |
| 鏡長中位 | 4.1 s |
| 鏡內動量中位 | 7.2（目標 ≥ 7） |
| 靜止幀 | 7%（目標 ≤ 15%） |
| 平均每句字數 | 15.5（字幕 37 條、572 字） |
| 響度 | -13.6 LUFS，峰值 -1.1 dBFS |
| 幀率 | 24/1，無黑幀、無 held |
| 花費 | RunPod 約 US$15（pod 16:03–22:07 US$15.72，含第 3 集 s06、s08 重抽與精修約 US$0.9） |

`cut-qa.py` 0 problem(s)；整片每鏡中間一格看過，面板字跟稿一致。工作分支 `claude/zt-e004-r2`，備份 `transfer/zt-e904-media`。
- 2026-11-07 站主看片：「箱子忽大忽小」「最後門口跟鍋子的距離有問題」「主角門口出來沒看到詭異的人，另一個畫面詭異的人在倒東西」。
  - 木匣：s16、s22 小匣、s19 畫成沒蓋的扁托盤、s25 抱著大木箱。`BOX` 改成「一本書大小、兩掌寬一掌深、後面有鉸鏈的蓋、一手拿得動」，s19、s25 重寫。
  - 夜景：場景句加「屋門在灶棚右邊六步」；s38 黑影寫成在門縫正中、看得清楚；s39 改用屋內場景（`house_door_night`，對到 `set-xujia-wu-t1`），面向鏡頭看著畫外的黑影，畫面裡沒有灶與鍋。
  - `colab/runs/e904/fix1` 重抽 s19、s25、s38、s39（種子 9040201／202），排在第 5 集重抽之後同一個 pod；挑好後精修、重剪、重送後台。
  - 教訓落地：`storyboard-shot-spec.md`、`storyboard-brief-for-planners.md` 加三行（道具尺寸、固定距離、反應鏡的地點）。
- 2026-11-07 獨立審片另挑出約 20 項（s17 開匣沒開、s09 阿令沒走出門、s32 豬沒卸下、s37 二牛沒走、s40 黑影太小、s05 沒站起來、s11 小禾不在畫面、多鏡該不笑在笑）。站主：嚴重與中等都修。
  `r2.py` 重寫，`colab/runs/e904/fix1` 改成 25 鏡 50 支（含站主指出的 s19、s25、s38、s39；加 CROCK、POLE、FIGURE、BELT 常數與近景短場景句），preflight 0／0。
  預估再花約 US$8，第 4 集累計約 US$23（上限 28）。s37 改成中景（近景拍不到二牛出院門）。
