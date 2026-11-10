---
id: 2026-10-20-s57-r3-formal-narrative-merge-diagnostic
title: S57 R3 formal narrative merge diagnostic
status: done
priority: P1
area: docs
owner: codex-s57-r3-merge
claimed_at: 2026-10-20T23:15:31Z
created_at: 2026-10-20T23:15:28Z
completed_at: 2026-10-20T23:17:38Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s57/review/r3-merge
---

# S57 R3 formal narrative merge diagnostic

## Why

R3 已有兩份對同一凍結劇本的獨立盲讀票，但尚無官方固定 OR 合併、CLI 紀錄或給作者的精確診斷；R3 來源覆核另有時序 HOLD。

## Definition of done

- [x] 原票、逐字引用的 13 題官方 JSON、固定 OR 合併、CLI 結果及完整五檔 SHA 綁定於 `review/r3-merge/`，明確給出 PASS/HOLD 與下步。

## Steps

- [x] 核對五檔與兩份原票 SHA；逐題忠實轉錄 Yes／No 並逐字檢查 26 個劇本行引用。
- [x] 以官方函式合併；在五檔 SHA 前後不變時執行 CLI，封存原樣輸出、紀錄及與來源 HOLD 的交接。

## How to verify

檢查 `docs/videos/curio-s57/review/r3-merge/merge-audit.json` 的原票 SHA、26 個 `matches_frozen_line`、A 9／13、B 10／13、合併 10／13；`cli-status.json` 的前後五檔 hash match、`cli.exit-code.txt` 為 1、`official-narrative-record.json` 的 `failed` 恰為 `chapters_link,payoffs,no_recap`；`npm run check:tasks`。

## Notes

報告：`docs/videos/curio-s57/review/r3-merge/summary.md`。**正式敘事 HOLD** 10／13：共同 No 為 `chapters_link,payoffs,no_recap`；A 的 `no_detour` No 被 B 的 Yes 依固定 OR 合併為 Yes，異議仍完整保留。官方 CLI exit 1、三題 fail、零 advisory。R3 獨立史料另因二月補給事件先後顛倒 HOLD；未執行 Jev 或媒體呼叫，也未改創作檔。
