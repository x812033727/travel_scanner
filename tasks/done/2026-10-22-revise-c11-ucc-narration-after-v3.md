---
id: 2026-10-22-revise-c11-ucc-narration-after-v3
title: Revise C11 UCC narration after v3 blind HOLD
status: done
priority: P2
area: docs
owner: codex-c11-ucc-author
claimed_at: 2026-10-22T16:42:04Z
created_at: 2026-10-22T16:41:57Z
completed_at: 2026-10-22T16:49:15Z
branch: codex/brand-story-ucc-c11-script
depends_on: []
scope:
  - docs/videos/story-everyday-ucc-c11/script.md
  - docs/videos/story-everyday-ucc-c11/visual-plan.json
  - docs/videos/story-everyday-ucc-c11/visual-plan.md
  - docs/videos/story-everyday-ucc-c11/script-source-notes.md
---

# Revise C11 UCC narration after v3 blind HOLD

## Why

C11 UCC 的 v3 劇本雖有版本綁定的來源差異 PASS，純旁白新鮮盲讀 A 對 SHA `C24907438D46BF2607CCC559D3A950D969E9F347538A2A37827F469CDDF2E3BC` 判 HOLD：開場先講出兩孔與 1981 拉環，Mira、罐壁變色及結尾重述過多。須在站主審稿前修好故事連續性；來源、盲讀、TTS 時長與費用各自仍是獨立關卡。

## Definition of done

- [x] 83 個旁白 ID、六章與 83 個一對一鏡頭保留，開場的三個具體後續時刻都停在結果前，1981 拉環留到第六章揭曉。
- [x] Mira 1965-09-14 與 UCC 1969-04 的先後、UCC 博物館「含奶」限定、初代兩孔及 1981 第三代拉環均維持來源界線。
- [x] 新旁白、JSON、閱讀版分鏡及作者來源註記同步；舊來源與盲讀收據明標歷史，無自我 PASS。
- [x] 聚焦機械檢查通過，提交並推送原草稿 PR；新 SHA 交獨立代理重核。

## Steps

- [x] 讀 v3 盲讀 HOLD 與 v3 來源差異收據，界定需改的 ID 與不可越過的史實。
- [x] 重排開場、Mira、罐壁、萬博到 1981 的鉤子與首尾動作，並同步圖像提示詞和卡片。
- [x] 執行 ID/鏡數/文字鏡像/禁用字/差異/JSON 檢查，記錄雜湊與推送結果。

## How to verify

`git diff --check`；用 Node 解析 `script.md`、`visual-plan.json`、`visual-plan.md` 比對 83 個唯一 ID 與逐鏡文字，再檢查 74 shot、9 stats、連卡上限及原創插圖提示詞。此檢查只能證明結構，不取代兩位新鮮盲讀、獨立來源審查或 TTS 480 秒實測。

## Notes

本票是同一作者在相同 C11 文件上的窄範圍後續修稿；認領使用 `--force`，因本 worktree 另有七張前次 `tasks done` 遺留的同作者 untracked `tasks/open/` 副本，使普通認領把自己的舊 scope 視為 active。未刪除或修改那些副本。新稿仍未獲獨立來源與盲讀判定，沒有付費生成、上傳或發布。

聚焦 Node 檢查：script/JSON/MD 各 83 唯一 ID，順序及 MD/JSON 行文字鏡像一致；74 shot、9 stats、最長連卡 2。`npm run test:docs-videos` 曾啟動，前 34 個測試輸出皆為綠；此範圍廣且持續進行，依任務優先序以 Ctrl+C 結束，因此**不能宣稱整套通過**。仍須 `git diff --check` 與提交後記錄雜湊；來源與敘事判定交獨立代理。
