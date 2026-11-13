---
id: 2026-11-12-curio-pool-wave43
title: 奇聞檔案局素材池第四十三批
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round20
claimed_at: 2026-11-12T13:01:56Z
created_at: 2026-11-12T13:01:56Z
completed_at: 2026-11-12T13:56:01Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞檔案局素材池第四十三批

## Why

站主 2026-11-12：「持續擴充」。奇聞檔案局再補一批新題，去重、整理來源，太薄或無聊的合併或淘汰，不為片長硬湊。

## Definition of done

- [x] batches/wave43-20261112.json 與 reviews/wave43-review-20261112.json 入庫，`cli.mjs check` PASS，pool.test.mjs 全過。

## Steps

- [x] 八個研究代理（P1–P8：H 近代發明的古老傳統、G 鐵路鬼、M 偽造標本、S 永動機、F 非洲民間故事、P 年曆預言、L 古代奇觀、U 天上軍隊）先去重再實讀來源。
- [x] 八位非作者覆核（R431–R438）逐題重開關鍵來源，並逐筆讀工具紀錄。
- [x] 組批、成題（T143–T145）、更新 selection 與 README，跑語意近鄰（7 組字面近鄰判為不同題）。

## How to verify

`node tools/video/curio/pool/cli.mjs check`（PASS）與 `node --test tools/video/curio/pool/pool.test.mjs`（23 過）。

## Notes

入選 1265→1297；暫緩 N4645（L25 已在 T33）、N4744（兄弟題 N4741 待查）；待查 N4646、N4664、N4683、N4686、N4741、N4784。網址規則違規：P1（加 www. 與斜線）、P3（去 ?sp= 參數，自報）、P4（http 改 https；P4-S011、S012 要在 N4703 排題前以原網址重讀）。
