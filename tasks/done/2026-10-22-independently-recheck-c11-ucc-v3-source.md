---
id: 2026-10-22-independently-recheck-c11-ucc-v3-source
title: Independently recheck C11 UCC v3 source delta
status: done
priority: P1
area: docs
owner: codex-c11-independent-source-v3
claimed_at: 2026-10-22T15:30:55Z
created_at: 2026-10-22T15:30:34Z
completed_at: 2026-10-22T15:35:33Z
branch: codex/brand-story-ucc-c11-script
depends_on: []
scope:
  - docs/videos/story-everyday-ucc-c11/reviews/script-source-delta-v3.md
---

# Independently recheck C11 UCC v3 source delta

## Why

C11 UCC 的前版來源審查和兩位盲讀只綁前版 SHA；作者依盲讀修了 17 句及 5 個畫面。需由不同審查者直接重讀一手頁面、逐 ID 確認新事實與畫面不越界，並明確劃出舊審查可沿用的範圍。

## Definition of done

- [x] 新稿 SHA 綁定的 17 句與 5 鏡逐 ID PASS／HOLD 收據，含直接來源 URL、舊列承接界線及付費停線。

## Steps

- [x] 重讀 UCC 2025／2026 原頁、博物館、沿革及濱田市／島根縣頁面。
- [x] 機械比對前後 83 個 ID、17 句與 5 鏡差異，逐列審查並落地收據。

## How to verify

`Get-FileHash` 核對 `script.md` 與 `visual-plan.json`；以 `git show ca31895d8^:<path>` 對照新檔每個 ID；`npm run check:tasks`。來源 URL 與逐 ID 判讀見收據。

## Notes

收據：`docs/videos/story-everyday-ucc-c11/reviews/script-source-delta-v3.md`。17 句、5 鏡文字預檢 PASS，特別是 `c110512` 只能歸屬 UCC 的事後需求說法，不推產量或銷量。前版未改 66 句、78 個 JSON 物件的來源判定可承接；本版兩位純旁白盲讀與付費關卡仍待處理。未付費。
