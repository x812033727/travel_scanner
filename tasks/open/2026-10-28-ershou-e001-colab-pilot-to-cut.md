---
id: 2026-10-28-ershou-e001-colab-pilot-to-cut
title: 重生系統 第 1 集 Colab 小樣到成片
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-28T04:50:28Z
completed_at:
branch:
depends_on:
  - 2026-10-28-ershou-chongsheng-season-one-plan-e001
scope:
  - docs/videos/ershou-chongsheng-e001
  - docs/videos/series-plans/ershou-chongsheng/production
---

# 重生系統 第 1 集 Colab 小樣到成片

## Why

第 1 集的分鏡、鎖定包與 Colab manifest 在 `docs/videos/series-plans/ershou-chongsheng/production/`；站主確認鎖定包第 0 節之後，照 `production/colab/README.md` 把第 1 集做出來。做法跟《修仙獎勵》第 1 集（票 `2026-10-27-xiuxian-e001-colab-pilot-to-cut`）一樣，兩部共用同一個 Colab compute units 池，先做哪一部的小樣要站主排。

## Definition of done

- [ ] look 關卡過（7 角色設定圖，zhouye 與 zhouye32 像同一個人）；audio 關卡過；聲音照 `voice-audition.md` 試聽過
- [ ] 42 張關鍵影格過 judge；關鍵影格版 animatic 給站主看，storyboard 關卡過
- [ ] 小樣 s29–s31 在 Colab 跑出來、`clips import` 收進去、站主看過說可以放量
- [ ] 其餘 36 支做完、`assemble` 出 1080p 成片、面板的青綠色框樣式在 `assemble` 裡做出來
- [ ] 收據：每支的 CU、seed、正文 SHA-256（等於鎖定檔）、第 0 格 PSNR；回填每鏡實際 take 到鎖定包第 9 節

## Steps

- [ ] 站主確認鎖定包；改了的項目 `plan_lock --write --force` 重鎖
- [ ] `look` → `tts` → `check-audio` → `shot_plan --timeline` 看買的秒數
- [ ] `keyframes` → animatic → storyboard 關卡
- [ ] bootstrap Colab、放首格、跑 `manifest-pilot.json`、匯入、站主看
- [ ] 跑 `manifest.json`、匯入、`music`、`assemble`、languages

## How to verify

`production/colab/README.md` 的流程與「小樣看什麼」；`drama_preflight.mjs --stage clips` 沒有 refuse；`plan_lock --ready` 程式項全過。

## Notes

照《修仙》第 1 集的經驗寫：Colab 路線自己的四條風險在 colab README 最後一節。
