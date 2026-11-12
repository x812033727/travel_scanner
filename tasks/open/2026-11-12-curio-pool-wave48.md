---
id: 2026-11-12-curio-pool-wave48
title: 奇聞檔案局素材池第四十八批
status: in-progress
priority: P2
area: docs
owner: claude-cloud-pool-round20
claimed_at: 2026-11-12T14:33:10Z
created_at: 2026-11-12T14:33:10Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞檔案局素材池第四十八批

## Why

站主 2026-11-12：「持續擴充」。奇聞檔案局再補一批新題，去重、整理來源，太薄或無聊的合併或淘汰，不為片長硬湊。

## Definition of done

- [ ] batches/wave48-20261112.json 與 reviews/wave48-review-20261112.json 入庫，`cli.mjs check` PASS，pool.test.mjs 全過。

## Steps

- [ ] 八個研究代理（ZD1–ZD8：H 偽造文書、G 戰場的聲音鬼、M 名動物傳說、S 被講走樣的實驗、F 拉丁美洲民間故事、P 預言詩的對號入座、L 地圖上不存在的地方、U 被當凶兆的極光）先去重再實讀來源，候選號段 N5421–N5580。
- [ ] 八位非作者覆核（R481–R488）逐題重開關鍵來源，並逐筆讀工具紀錄。
- [ ] 組批、成題、更新 selection 與 README，跑語意近鄰。

## How to verify

`node tools/video/curio/pool/cli.mjs check` 與 `node --test tools/video/curio/pool/pool.test.mjs`。

## Notes

研究進行中（owner claude-cloud-pool-round20）。BRIEF 新增 wave45–46 違規提醒：用 loc.gov 搜尋結果的 url 欄、不自己換主機、遇驗證頁不改抓同資料庫另一主機。
