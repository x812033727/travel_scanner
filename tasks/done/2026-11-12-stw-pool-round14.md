---
id: 2026-11-12-stw-pool-round14
title: 原來如此素材池第十四輪：補讀後備組題與從頭研究新長題
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round14
claimed_at: 2026-11-12T08:11:26Z
created_at: 2026-11-12T08:11:25Z
completed_at: 2026-11-12T08:43:30Z
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/pool
---

# 原來如此素材池第十四輪：補讀後備組題與從頭研究新長題

## Why

站主 2026-11-12：「繼續擴充」「持續擴充」。一邊替後備組題補讀，一邊從零研究全新長題；夠成一集的才成題，不為片長硬湊。

## Definition of done

- [x] wave64 批次、checkpoint-3978、reviews/material-20261111-round14.{json,md} 入庫，`cli.mjs check` PASS，pool.test.mjs 與 catalog.test.mjs 全過。

## Steps

- [x] 作者 F23 補讀 C8-02、C9-02；作者 F24 對八個候選去重後從零研究 C10-01 冰為什麼滑、C10-02 衣服濕了為什麼變深。
- [x] 兩位非作者覆核（V26、V27）重抓全部來源、重算片長。
- [x] 組進素材池：新增 G625，其餘留後備。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`、`node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`（32 過）。

## Notes

可成題長題 83→84。後備的補法：C9-02 約 8.3 分，差約半條（Baltodano-Goulding 或 Lu 2007 合法全文、Møller & Bonn 2007，或淡水對海水濕沙乾後強度的受控對照）；C10-01 約 6.35 分，差約 4.1 條，需要非 Bonn 研究室的原研究（Sazaki、Murata、Sánchez 的 PNAS 開放全文，Europe PMC 全文端點這輪回 500）與 Canale 期刊版；C10-02 約 4.0 分，主機制與池中「濕紙變透明」相同，除非有區分兩種散射路徑的機制原文或布料乾濕量測，否則不必再追。F24 的研究稿用了「物理／光學／地球科學」這種池中沒有的領域名，整合時改成生活力學、生活光學。F24 候選去重：茶壺效應（G193、F17006）、橡皮筋變熱（P26002、G265）、汽水噴（LEG-S72）、氣球黏牆（LEG-S36、E2003）、義大利麵斷三段（G169）已有；冰黏舌頭會變成安全建議；淋浴簾效應沒有同儕審查的開放原研究。
