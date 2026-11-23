---
id: 2026-11-11-curio-pool-wave23
title: 奇聞素材池第二十三批新題
status: done
priority: P2
area: docs
owner: claude-opus-cloud-channel-review
claimed_at: 2026-11-11T10:56:37Z
created_at: 2026-11-11T10:56:36Z
completed_at: 2026-11-11T11:46:54Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞素材池第二十三批新題

## Why

站主 2026-11-11：「繼續擴充素材池」（規則同前：去重、整理來源、太薄或無聊的合併或淘汰、不為片長硬湊）。

## Definition of done

- [x] 新一批題目經研究、去重、非作者覆核後進素材池；撐不起的章節題不收。

## Steps

- [x] 4 個研究代理（約 64 個點子，收 26 題）。
- [x] 4 位非作者覆核（R231–R234），退回 3 個兄弟題已是完整單集的章節題。
- [x] 語意近鄰去重。
- [x] `batches/wave23-20261111.json`、`reviews/wave23-review-20261111.json`、selection（832）、題案 T115–T117、README 第二十三批。

## How to verify

`node tools/video/curio/pool/cli.mjs check`（PASS，入選 832、題案 111）；`node --test tools/video/curio/pool/*.test.mjs`。

## Notes

- 覆核有幾筆修改寫成「把 A 改為 B」的說明，不是完整欄位；組裝時逐筆手動套用並檢查沒有殘留說明文字（`scratchpad/wave23/build/assemble.py`）。下一批的覆核簡報要明寫「changes 一律給完整的新欄位」。
- 天狗、妲己、吸血鬼三個章節題的合併要縮短既有題（N443、N369、F34），留給站主決定。
