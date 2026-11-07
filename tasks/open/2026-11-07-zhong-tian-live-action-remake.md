---
id: 2026-11-07-zhong-tian-live-action-remake
title: 種田娶妻打天下改成真人版：試鏡、小樣、鎖定後逐集重做
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-11-07T12:00:49Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/series-plans/zhong-tian-qu-qi
---

# 種田娶妻打天下改成真人版：試鏡、小樣、鎖定後逐集重做

## Why

站主 2026-11-07：「種田改成真人版重做」「不要用動畫的」。3D CG 版第 1–6 集 r2 的重抽一直卡在同樣的錯（參考圖帶笑、道具每鏡不一樣），站主決定整部改成真人版。
CG 的重抽佇列（`scratchpad/chainR`–`chainU`）已經停掉，pod 也停了（這次 pod 計 US$11.50），兩個定時自查都改成不准重開 CG 佇列。
計畫在 `docs/videos/series-plans/zhong-tian-qu-qi/production/live-action-plan.md`。

## Definition of done

- [ ] 站主看過真人定妝照、場景圖，以及第 1 集三鏡小樣，點頭鎖定。
- [ ] 第 1–6 集真人版剪好，經過四道審片與獨立審片，匯入後台，站主看過。
- [ ] 每一批花了錢的東西都當天備份並驗證（missing=0 differ=0）。

## Steps

- [x] 0. `cast.json` 的畫風本來就是真人（`look.style`：photorealistic live-action），外貌照用；定妝照拿掉道具（秦霜的刀、小禾的草兔、趙捕頭的鐵尺），由 `production/live-action/screen-test.py` 產生提示詞。
- [x] 1. （2026-11-07）試鏡：三輪共 US$1.44；站主「照你的建議選，唐小棠用齊胸襦裙」，選定的放在 `production/assets/refs-live/`（README 列來源）。三位女主角另加「胸部豐滿一點」的腰上照。原本：10 個角色＋許硯現代裝的真人定妝照、6 張場景圖，各兩個種子（上限 US$8，**等站主點頭**）。
- [x] 2. 主要角色的角度圖（`refs-live/angles/`；女主角從沒改胸部的原圖重畫）。
- [ ] 3. 第 1 集三鏡小樣 s23–s25：草稿 6 支（US$0.67），挑 s23-02、s24-01、s25-01，精修（US$1.09），配上原錄音給站主看（`_live-pilot/…/st2/pilot-refined.mp4`）。**等站主決定真人路線過不過**。
- [ ] 4. 鎖定：換掉提示詞的畫風句，重建 manifest，preflight 0 錯。
- [ ] 5. 第 1–6 集逐集做，每集上限 US$28。

## 已經做的（2026-11-07）

- CG 版最後的狀態都已備份：`transfer/zt-e90N-media-20261107`（第 1–6 集）、`transfer/zt-series-media-20261107`、`transfer/zt-import-dubs-review-20261107`，全部 verify-bk 都是 missing=0、differ=0。
  後來又補了 `…-20261107b`，內容是第 1 集 fix3 的部分草稿與今天畫的定妝照。
- 改定妝照的教訓（畫風要寫系列自己的；舊提示詞照抄會把 CG 畫成真人）已經寫進 storyboard-shot-spec 與 route-a。
