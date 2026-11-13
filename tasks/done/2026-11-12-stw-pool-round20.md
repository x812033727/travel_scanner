---
id: 2026-11-12-stw-pool-round20
title: 原來如此素材池第二十輪：從頭研究新長題
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round20
claimed_at: 2026-11-12T11:30:39Z
created_at: 2026-11-12T11:30:38Z
completed_at: 2026-11-12T13:11:06Z
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/pool
---

# 原來如此事務所素材池第二十輪

## Why

站主 2026-11-12：「持續擴充」。後備補讀（第十七到十九輪）已無效益，改為從零研究新長題，同時把讀到的開放原研究收成新核心。

## Definition of done

- [x] batches/wave70-{physics,earth,life}.json、reviews/material-20261111-round20.{json,md}、checkpoint-4119 與 VALIDATION-4119 入庫，`cli.mjs check` PASS，pool.test.mjs 與 catalog.test.mjs 32 項通過。

## Steps

- [x] 六位作者（F36–F41）先在全池大範圍去重，再各從零研究兩個新長題。
- [x] 六位非作者覆核（V39–V44）重抓來源、逐筆讀工具紀錄、重算片長。
- [x] 併入 138 個核心，十二題記為後備，新增 10 組分題理由。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`（PASS）與 `node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`（32 過）。

## Notes

入選 4,119→4,257；可成題長題維持 86 組。十二題覆核重算 4.4–6.7 分，全部後備：從零開新長題連續第四輪沒有成題。下一輪建議把相近後備合併再評，或只挑覆核寫明「補到某篇原文就能過線」的題。F41 一次去掉 /pdf 取得目錄頁（覆核循搜尋結果的目錄頁確認後保留），F39 對 MIT 429 限流連試四次，都記在紀錄裡。
