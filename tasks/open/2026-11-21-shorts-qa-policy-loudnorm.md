---
id: 2026-11-21-shorts-qa-policy-loudnorm
title: Shorts 零台詞匯入：首次 qa 的 policy 與 loudnorm 響度落差
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-11-21T15:49:53Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/shorts
  - docs/videos/shorts-drama/production
  - docs/videos/shorts-drama/REVIEW.md
---

# Shorts 零台詞匯入：首次 qa 的 policy 與 loudnorm 響度落差

## Why

2026-11-21 第一次用 #2200 的 `shorts/cli.mjs import` 匯入《社畜地獄》e01–e06（零台詞，`silent: true`），碰到兩個工具問題：

1. **還沒推過的 slug，policy 一定不過。** 站上的 `policy_questions_for`（`apps/api/app/video_automation/judge.py`）讀專案那一列的 `format`，`drama` 才免「有示範」。第一次跑 `qa` 時站上還沒有那一列，所以被當成教學片評：六集都是「有示範 0.03–0.04，沒過」。只能先推一次讓站上建檔，再重跑 `qa → package → push`（每次都要付一次 Jev）。
2. **響度量法不一致。** 製作端的 `qa_check.py` 用 `ebur128` 量，站上的 `shorts qa` 用 `loudnorm` 量（`build.mjs` `measureFinal`）。e02、e05 用 ebur128 量是 -14.0／-13.9，用 loudnorm 量是 -12.9／-12.5，超出 -14 ± 1。音樂停掉、只剩短音效的段落多的片，差距最大。

## Definition of done

- [ ] 零台詞短劇第一次跑 `qa` 時，policy 就用劇的題目評（不必先推一次）。
- [ ] 製作端交片前的響度檢查和站上 `qa` 讀出同一個數字。

## Steps

- [ ] 二選一：`qa` 在 silent 時把 `format: drama`（或 `line`）帶給 `automation/judge/policy`，讓站上沒有那一列時也照劇評（要改 API 端，scope 另加 `apps/api/app/video_automation`）；或在 `qa` 前先 `client.report` 建檔。
- [ ] `docs/videos/shorts-drama/production/qa_check.py`（雲端硬碟 `AI/備份/Shorts/<系列>/production/` 是原檔，repo 若沒有就在 REVIEW.md 寫明）改用 `loudnorm` 的 `input_i`，或兩種都印。
- [ ] REVIEW.md §6 的匯入步驟補上這兩點（在問題修好前先寫「推兩次」的做法）。

## How to verify

拿一個沒推過的 slug 跑 `node tools/video/shorts/cli.mjs qa --dir <BUILD_DIR>`，policy 應該顯示「有示範：不適用」；拿 `import-work/shechu-hell-e05` 的 `final-pre-loudnorm.mp4` 跑兩邊的檢查，讀數要一樣。

## Notes

- 這次的做法與數字寫在 `docs/videos/lessons/shorts.md` 2026-11-21〈匯入後台〉那一條。
- `layout` 在匯入的片本來就不過（站上沒有安全區量測），不在這張票的範圍。
