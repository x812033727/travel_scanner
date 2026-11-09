---
id: 2026-11-07-sothatswhy-p15-dialogue-why-the-sea
title: sothatswhy P15 dialogue: why the sea stays salty
status: done
priority: P2
area: docs
owner: claude-opus-5.5-peaceful-einstein
claimed_at: 2026-11-07T16:39:26Z
created_at: 2026-11-07T16:39:20Z
completed_at: 2026-11-09T04:04:53Z
branch:
depends_on: []
scope:
  - docs/videos/sothatswhy-p15-salty-sea
---

# sothatswhy P15 dialogue: why the sea stays salty

## Why

原來如此事務所對話版下一集：EPISODES.md 的 P15〈河水一直流入，海水怎麼還是鹹？〉。形式照 `docs/videos/so-thats-why/dialogue-pilot-20261103/README.md`（§9 關卡、§10 教訓）。

## Definition of done

- [x] 成片、上架確認、語言包送上 /admin/videos，等站主決定；每一關的工作目錄都備份在 `claude/backup-sothatswhy-p15-salty-sea`。

## Steps

- [x] 研究與 claims.md、build_scenes.py、lint 0 錯
- [x] 獨立查核 verify-1.md、盲評 narrative 14 題、稿子評分
- [x] 旁白、check-audio
- [x] 插圖、眼睛放大檢查、分鏡評分 ≥ 49
- [x] 配樂、合成、qa、final
- [x] 八語翻譯、縮圖、配音、package、publish／languages

## How to verify

The exact commands or clicks that prove it works.

## Notes

- 系列配樂床 `sothatswhy-p02-bed.m4a` 沒有在任何備份分支裡。2026-11-07 從 P02 備份的付費原檔 `music/e4225993d121c03b.mp3` 照 P02 NOTES 的做法重做（去尾到 175.15 秒、五段 3 秒交叉淡化、863.75 秒）：`_music/sothatswhy-bed-r2.m4a`，sha256 `9bb4ba6f…28c6`。沒有另外生成。
- 所長不寫灰髮：用 `shot_looks` 的 `office` 外觀（沒有灰髮），設定圖的鍵不變（`lookHash`／`sheetKey` 只看 `appearance`）。

## 結案（2026-11-09）

成片、上架、語言三關站主都已核准；八語配音已傳到 YouTube Studio。九語縮圖、配音、字幕、說明都在上傳包，整個工作目錄與重製所需的工作目錄外檔案在分支 `claude/backup-sothatswhy-p15-salty-sea`（逐檔核對 0 不符）。經驗：上架核准後才補八語配音會讓核准失效，之後的集數先做齊八語再送上架關。
