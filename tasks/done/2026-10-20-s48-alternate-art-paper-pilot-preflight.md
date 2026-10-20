---
id: 2026-10-20-s48-alternate-art-paper-pilot-preflight
title: S48 alternate art paper pilot preflight
status: done
priority: P2
area: docs
owner: codex-s48-preflight
claimed_at: 2026-10-20T22:52:38Z
created_at: 2026-10-20T22:52:35Z
completed_at: 2026-10-20T22:54:43Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s48/review/r10-alternate-art-paper-preflight.md
---

# S48 alternate art paper pilot preflight

## Why

S48 R10 的 `atl001/017/070` 兩輪原生試畫均 0／3 KEEP，舊方案已達預先規定的 STOP。全片 102 句音訊已零旗標，但插圖和配樂被本月評審／配樂額度卡住。先在書面上為不同的三景新方案核對史料、可見主物件、停損與整集費用，供額度恢復時決定是否採入。

## Definition of done

- [x] 候選三景 prompt 的史料與畫面界線、原尺寸 KEEP／REJECT 條件、一次有界重試及整集累計上限均存成單一 S48 文件，舊 STOP 與網站音訊 pending 狀態清楚保留。

## Steps

- [x] 重開固定 Russell／Field 全文並核 SHA，重看三張第二輪 1280×720 原圖與 ledger。
- [x] 依系列規則撰寫新三景紙上候選、3／3 原圖門檻、一次改詞重試 STOP 與 US$0.15 試畫／US$4.16 整集累計上限。
- [x] 不改稿、`video.json`、已錄音訊或媒體，也不向站台做任何付費呼叫。

## How to verify

`sha256sum` 核固定兩本書、現行三檔稿、三張原圖及私有 ledger；`node tools/video/cli.mjs keyframes --slug curio-s48 --takes 3 --dry-run` 核 99 景與約 US$4.01；`npm run test:docs-videos`、`npm run check:tasks`、`git diff --check`。

## Notes

主文件：[S48 新三景書面預檢](../../docs/videos/curio-s48/review/r10-alternate-art-paper-preflight.md)。這是撰案者自查，新方案尚無獨立書面覆核、付費試畫或原圖 PASS。本站目前 judge 20,000／20,000、配樂 60／60；月重置前不得買未評審圖。額度恢復後先重核精確版網站狀態、乾跑與 ledger，再考慮把三句放進 `video.json`，並由未撰詞者覆核來源／分鏡綁定。網站音訊卡仍待站主。
