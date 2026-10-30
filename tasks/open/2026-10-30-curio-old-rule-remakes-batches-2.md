---
id: 2026-10-30-curio-old-rule-remakes-batches-2
title: Curio old-rule remakes under the 10-25 rules, no burn-in: batches 2 to 4
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-30T22:10:42Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-h02-v3
  - docs/videos/curio-h03-v3
  - docs/videos/curio-h06-v3
  - docs/videos/curio-h07-v3
  - docs/videos/curio-h10-v2
  - docs/videos/curio-h11-v2
  - docs/videos/curio-h12-v2
  - docs/videos/curio-l08-v3
  - docs/videos/curio-m09-v2
  - docs/videos/curio-u09-v2
  - docs/videos/curio-s12-v2
  - docs/videos/curio-s15-v2
  - docs/videos/curio-s21-v2
---

# Curio old-rule remakes under the 10-25 rules, no burn-in: batches 2 to 4

## Why

站主 2026-10-31：舊規則的奇聞檔案局要照 10-25 規則重寫，都不燒字幕。第一批五支在票 `2026-10-30-curio-old-rule-remakes-under-the`，已做到稿子、查核、盲評。這張票是其餘 13 支，一批最多 5 支。舊片、舊 slug、YouTube 上的影片一律不動；新片核准後換片由站主決定。

## Definition of done

- [ ] 每支新 slug：`lint` 0 錯誤、獨立查核 `verify-1.md`、兩位盲讀讀者沒有任何一題同時答否（`panel/`）。
- [ ] 每批把 `tts`、`keyframes` 的 dry-run 實數交給站主，一批一次核准。未核准前不做付費生成。

## Steps

- [ ] 批 2：curio-h02-v2 羅阿諾克 → `curio-h02-v3`、h03-v2 通古斯 → `curio-h03-v3`、h06-v2 安娜塔西亞 → `curio-h06-v3`、h07-v2 鐵面人 → `curio-h07-v3`、h10 富蘭克林遠征 → `curio-h10-v2`。
- [ ] 批 3：h11 伏尼契 → `curio-h11-v2`、h12 弗蘭南燈塔 → `curio-h12-v2`、l08-v2 麥田圈 → `curio-l08-v3`、m09 安提基特拉 → `curio-m09-v2`、u09 小綠人 → `curio-u09-v2`。
- [ ] 批 4：s12 關原 → `curio-s12-v2`、s15 伊達政宗 → `curio-s15-v2`、s21 鬱金香 → `curio-s21-v2`。

## How to verify

`node tools/video/cli.mjs lint --slug <slug>`；`node tools/video/cli.mjs keyframes --slug <slug> --dry-run`；`node tools/video/cli.mjs tts --slug <slug> --dry-run`；`npm run check:tasks`。

## Notes

- 做法、撰稿說明、查核說明都在 [`docs/videos/history-curiosity/old-rule-remake-playbook-20261031.md`](../../docs/videos/history-curiosity/old-rule-remake-playbook-20261031.md)，先讀。
- `curio-s31` 不在這張票：`curio-s31-v2` 已是新規則，只要拿掉燒字幕重新合成（session `burn-in-reassemble`）。
- 動 h07 前看舊票 `2026-10-14-remake-curio-h07-with-the-series`；動 h10–h12、m09、u09 前看舊票 `2026-10-15-produce-five-new-curio-episodes-h10`。兩張都是舊認領，範圍是舊 slug，不擋新 slug。
- 第一批的成本與學到的事寫在第一批的票裡；一批同時最多 3 個子代理時約要 2 小時。
- 子代理傳 model "opus"，提示要禁止在任何地方放個人 email。
