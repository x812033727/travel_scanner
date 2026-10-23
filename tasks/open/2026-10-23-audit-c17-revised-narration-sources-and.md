---
id: 2026-10-23-audit-c17-revised-narration-sources-and
title: Audit C17 revised narration sources and paired visuals
status: in-progress
priority: P1
area: docs
owner: codex-root-c17-review
claimed_at: 2026-10-23T04:01:05Z
created_at: 2026-10-23T04:00:51Z
completed_at:
branch: codex/brand-story-nalgene-c17-review-v2
depends_on: []
scope:
  - docs/videos/story-everyday-nalgene-c17/reviews/independent-script-v2.md
---

# Audit C17 revised narration sources and paired visuals

## Why

站主已採用 C17 企劃；作者因第一次只讀旁白 HOLD 窄修了 69 句劇本和配鏡，須由非作者重新核查每句來源及每鏡是否偷渡資訊。

## Definition of done

- [x] 對精確稿件雜湊留下逐句來源與逐鏡文字的獨立審查收據，並指出可操作的窄修。

## Steps

- [x] 直接重開 S1–S7 一手／原發行者材料，檢查 1949 商品分類、1960s 公司回顧、2008 宣布與 2020 質量平衡。
- [x] 對照全部 69 ID 的劇本、來源欄、畫面 Markdown 與 JSON；獨立標出 E06、T04 配鏡 HOLD。

## How to verify

`Get-FileHash` 計算四份作者文件 SHA-256；PowerShell 檢查劇本／JSON 的 69/69 ID、旁白，及分鏡 Markdown／JSON 的 69/69 畫面文字；`git diff --check`、`npm run check:tasks`。詳見 `docs/videos/story-everyday-nalgene-c17/reviews/independent-script-v2.md`。

## Notes

旁白來源 69/69 PASS；配鏡 67/69 PASS，E06 提前揭曉目的地、T04 把未來停產計畫視覺化成已淡出，兩項 HOLD。這是來源／配鏡查核，不是只讀旁白盲讀或站主核准。作者只需窄修兩鏡，送同審查者覆核差分。
