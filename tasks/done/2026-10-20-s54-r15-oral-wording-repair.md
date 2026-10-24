---
id: 2026-10-20-s54-r15-oral-wording-repair
title: S54 R15 oral wording repair after audio HOLD
status: done
priority: P2
area: docs
owner: codex-s54-r15-author
claimed_at: 2026-10-20T22:39:56Z
created_at: 2026-10-20T22:39:53Z
completed_at: 2026-10-20T22:44:19Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s54/brief.md
  - docs/videos/curio-s54/video.json
  - docs/videos/curio-s54/claims.md
  - docs/videos/curio-s54/script.md
  - docs/videos/curio-s54/review/r15-author-oral-repair.md
---

# S54 R15 oral wording repair after audio HOLD

## Why

S54 R14 的逐句音檢最後仍有 17／148 句旗標；15 句可透過窄幅口語修稿降低誤聽風險，另兩句是同音字形的 ASR 差異，需要獨立聽辨。舊稿已獲得的審核不適用於改稿後的新雜湊。

## Definition of done

- [x] 15 句改稿與主張表逐字對齊，另兩句同音旗標保留並交接。
- [x] 新劇本重產、五檔雜湊凍結，沒有擅自通過獨立史料／敘事／政策／語音關卡。
- [x] lint、逐句對齊和書面時長核對通過。

## Steps

- [x] 讀取 R14 最終音檢交接及各句來源界線，保留 145 個正文場景、1 個片尾場景與 148 個旁白 ID。
- [x] 同步修改 `video.json` 與 `claims.md` 15 句；因字數改變，修正 `brief.md` 書面估長與正文漢字數。
- [x] 重產 `script.md`，撰寫 `review/r15-author-oral-repair.md` 的完整舊稿→新稿與五檔雜湊。

## How to verify

- `node tools/video/cli.mjs script --slug curio-s54`：已重產，narrative hash `4e745d33a4829b72`。
- `node tools/video/cli.mjs lint --slug curio-s54 --json`：0 errors、0 warnings、148 句、14.1189 分鐘書面估長。
- 本地逐句比對：145／145 主張列、148／148 劇本旁白均與 `video.json` 相同，148 個 ID 唯一；R14 的 `video.json`、`claims.md`、`brief.md` 以本次精確改動反向重建後雜湊相符。
- `npm run check:tasks`、`git diff --check`。

## Notes

凍結紀錄：[R15 作者口語修稿](../../docs/videos/curio-s54/review/r15-author-oral-repair.md)。`research.md`、各景畫面提示詞與 loop 均未動。`s54109`／`s54119` 只因「希爾／席爾」「准／準」遭標，未根據 ASR 字形改動；`s54013` 地名也可能再出現同音異字。R14 音檔屬舊稿，不可作 R15 的音訊 PASS。下一手須針對本輪五檔凍結另請獨立史料查核與兩位新盲讀者，合併政策關卡後才可開始付費 TTS。
