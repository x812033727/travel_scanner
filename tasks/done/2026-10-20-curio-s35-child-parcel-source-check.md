---
id: 2026-10-20-curio-s35-child-parcel-source-check
title: Check original sources for Curio S35 child parcel post
status: done
priority: P2
area: docs
owner: codex-gpt6-s35-source
claimed_at: 2026-10-20T05:58:39Z
created_at: 2026-10-20T05:58:35Z
completed_at: 2026-10-20T05:59:33Z
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s35
---

# Check original sources for Curio S35 child parcel post

## Why

S35 題庫有「寄送兒童」的吸睛說法，但尚無來源查核。先驗證能否在本雲端重開 1913–1915 年規則與個案，避免把後世轉述、擺拍照片或年份混成已核史實。

## Definition of done

- [x] 記錄已重開的固定來源、雲端不可讀的原件及本題重開條件。
- [x] 對八分鐘故事做可行性決定，不據候選題卡先寫稿或購圖。

## Steps

- [x] 查 S35 認領與 S01／S09／S18 題目衝突：S35 未認領，題材不同。
- [x] 逐項試開 USPS、Smithsonian、LOC、govinfo、Internet Archive；核兩份 GitHub 固定全文與雜湊。
- [x] 史料不足，留下 [`research.md`](../../docs/videos/curio-s35/research.md)，改查 S33。

## How to verify

核對 `research.md` 兩份固定全文及 SHA-256；來源障礙與每項不可作的推論均在同檔。`npm run tasks -- check` 驗 task metadata。

## Notes

USPS、Smithsonian Postal Museum、LOC、govinfo、Archive.org 在本雲端 `curl` 均回 CONNECT 403；已有 1911 政策辯論與 1922 後出概述都不能充當 1913–15 郵務規則或寄童個案。S35 **暫緩前製**，完成的是來源可行性查核，不是影片製作。
