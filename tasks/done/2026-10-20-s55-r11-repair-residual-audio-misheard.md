---
id: 2026-10-20-s55-r11-repair-residual-audio-misheard
title: S55 R11 repair residual audio misheard lines
status: done
priority: P2
area: docs
owner: codex-s55-r11-author
claimed_at: 2026-10-20T22:34:45Z
created_at: 2026-10-20T22:34:43Z
completed_at: 2026-10-20T22:39:10Z
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s55/video.json
  - docs/videos/curio-s55/claims.md
  - docs/videos/curio-s55/script.md
  - docs/videos/curio-s55/review/r11-author-oral-repair.md
---

# S55 R11 repair residual audio misheard lines

## Why

S55 R10 合格劇本完成 140／140 官方音檢與兩輪局部重錄後，仍有 14 句 Jev 旗標。多數為「試升／世生」、「鬆繩／封神」等同音誤認，`s55018` 另被轉寫為會把 **12 英尺**錯成 **12 英吋**的單位。R10 音訊 HOLD，依 curio-episode／youtube-video 流程改口說後須重新審核。

## Definition of done

- [x] 僅把仍被標記的 14 句改成自然、史料可查的口說，逐句主張同步，其他口說與畫面提示位元不變。
- [x] 新版劇本重產、完整來源與審核交接可追 R10／R11 五檔雜湊；不把作者候選稿稱為通過。

## Steps

- [x] 對照 [R10 最後音檢 14 句交接](../../docs/videos/curio-s55/review/r10-audio-archive/round2/wording-handoff.md)與固定版富蘭克林原文；核對「12 feet Diameter」，換算口說為約 3.7 公尺。
- [x] 修改 `video.json` 的 14 句及 `claims.md` 同 ID 列，重產 `script.md`；保留 source URL、章節／畫面提示、look 和配樂設定。
- [x] 在 [R11 作者凍結](../../docs/videos/curio-s55/review/r11-author-oral-repair.md)記全部舊→新與可逆 SHA、測試和待審核關卡。

## How to verify

`node tools/video/cli.mjs script --slug curio-s55`、`node tools/video/cli.mjs lint --slug curio-s55 --json`（0 error／0 warning）、`npm run test:docs-videos`（236／236）、`npm run check:tasks`。另將 14 句及換算註反向套回 R11 檔案，`video.json`／`claims.md` SHA-256 必須精確回到 [R10 作者凍結](../../docs/videos/curio-s55/review/r10-author-fix.md)的兩個雜湊。

## Notes

作者只改 14 個已標記 ID；R11 `script.md` SHA-256 `9ed20e5e29628392242bd4cd61cf8e4fa4e34322036a47b533f06294b12949fd`。138 個正文主張列與 138 句同字，另兩句既有 CTA。快速文字估算正文 2,637 漢字／325 字每分鐘為 8.11 分鐘；R10 實測音訊 13:07.40 已不能充作新稿驗收。下一位工作者先做獨立史料／畫面差分，再由兩名真正無前情讀者盲評 R11 和正式 OR；通過才送政策、TTS、全句音檢。尚未送任何 R11 付費媒體請求。
