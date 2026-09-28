---
id: 2026-09-28-video-story-pilot
title: 試作兩支品牌故事並記錄數字
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-09-28T03:31:15Z
completed_at:
branch:
depends_on:
  - 2026-09-28-video-story-worker
  - 2026-09-28-video-story-backlog
  - 2026-09-28-video-story-api-policy-languages
scope:
  - docs/videos/STORY.md
---

# 試作兩支品牌故事並記錄數字

## Why

`docs/videos/STORY.md` 裡的時間、張數、花費都是從程式常數估的，沒有量過。每天兩支之前要先知道：一支實際要多久、花多少、1K 的圖放大到 1080p 夠不夠清楚、訂閱帳號撐不撐得住、自動關卡會不會卡住。

## Definition of done

- [ ] 兩支試作（A01 輪子行李箱、B18 迴轉壽司）在正式主機上從清單開始做到「可以上架」，站主看過成片。
- [ ] `docs/videos/STORY.md` §試作紀錄 填了：每支的長度、鏡數、圖片張數與重做率、各階段秒數、帳本花費、訂閱帳號的 token 用量、`final.mp4` 的大小。
- [ ] 1K 圖片的清晰度有結論：維持 1K，或建議改 2K（附每支成本差額，由站主決定）。
- [ ] 卡住的地方都開了票或當場修掉；`STORY.md` 的上限表依量到的數字更新。

## Steps

- [ ] 站主先做三件事：開「AI 漫劇」、寫頻道立場、確認帳號有 `settings.manage`（`STORY.md` §站主要先做的事）。
- [ ] 部署（要站主同意，走 skill `deploy`）。
- [ ] 調上限：每月圖片與 judge 次數、作品每月集數、同時進行數、旁白每月字數、Jev 每日次數、審核單檔大小。
- [ ] 匯入清單：先試跑，再套用；每日支數先設 1。
- [ ] 看工人日誌與後台，兩支做完後記錄數字。

## How to verify

成片用 ffprobe 確認 1920×1080、30 fps、長度 720–900 秒；`review/qa.json` 全過；`checks.json` 的每個鏡頭都是 `motion`；帳本的花費在每支 US$25 以內。

## Notes

- 前幾支成片請站主親自看過，再開「自動品管全過就核准成片」給故事用。
- 任何對正式站的操作都要站主同意；這張票不是授權。
