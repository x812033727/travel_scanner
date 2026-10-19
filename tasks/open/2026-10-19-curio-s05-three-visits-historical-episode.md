---
id: 2026-10-19-curio-s05-three-visits-historical-episode
title: Curio S05 Three Visits historical episode
status: in-progress
priority: P2
area: docs
owner: codex-s05
claimed_at: 2026-10-19T17:59:22Z
created_at: 2026-10-19T17:59:20Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s05
---

# Curio S05 Three Visits historical episode

## Why

站主授權持續製作新的歷史系列影片。S05「三顧茅廬，還是諸葛亮自己上門？」是尚未製作的 S 軸候選，適合接在 S34 等已啟動題目之後；需要把〈出師表〉、陳壽正文、裴注引《魏略》與小說場面分清，才不會把真正存在的古籍異說說成「三顧是假的」。本票只認領 `docs/videos/curio-s05`，不碰共用題庫。

## Definition of done

- [x] 固定可追溯的古籍轉錄、查核主要敘述和小說增飾，寫成約九分鐘可審的故事與分鏡。
- [x] `video.json` 與 `script.md` 通過奇聞檔案局 lint；逐句主張可追到史料層級。
- [ ] 獨立盲讀修改後的最終稿通過 13 題；更新過的旁白再做逐句聽辨；插圖、配樂、成片與上架包完成。

## Steps

- [x] 檢查同題資料與分支、認領窄 scope，選 A 案史料追查線。
- [x] 核讀固定《三國志》卷 35 與《三國演義》37／38 回，建立 `brief.md`、`research.md`。
- [x] 完成 `video.json`、`script.md`、`claims.md`，修到 0 lint errors／warnings。
- [x] 收取第一位盲讀者 13 題回饋，修正重述、問題回收、章名與章節銜接。
- [ ] 請全新讀者盲讀目前劇本雜湊；通過後恢復已暫停的插圖與語音關卡。
- [ ] 完成媒體與交付，並在同一 PR 將票結案。

## How to verify

`node tools/video/cli.mjs lint --slug curio-s05`（0 errors、0 warnings）；`node tools/video/cli.mjs script --slug curio-s05`；`node tools/video/cli.mjs narrative --slug curio-s05` 加新讀者的 `--answers`；`npm run test:docs-videos`（236 passed）；`npm run check:tasks`（既有其他 scope 的警告不影響本票）。後續另跑語音、插圖、QA、上架包關卡。

## Notes

- 2026-10-19：固定《三國志》轉錄 commit `10a0b1ab3019d8821262f7402366d14fb4aaa102`，小說轉錄 commit `761813427eb5685c395804493f9fbd7ad8dc7d`；詳細原文見 `docs/videos/curio-s05/research.md`。本次暫存 `/tmp/s05-sanguozhi`、`/tmp/s05-sanguoyanyi` 僅供核讀，不依賴暫存交接。
- 《三國志》正文與〈出師表〉都寫劉備三顧；裴注引《魏略》說諸葛亮北行見劉備，且稱《九州春秋》同說。裴本人依〈出師表〉反駁。《三國演義》的風雪、晝寢是更晚的小說場面；不可說「三顧只有小說才有」，也不可把裴注引文當裴認可。
- A 案成稿 113 句／94 張 still／2 張文字卡／片尾，估 9.1 分鐘；`narrative` 內容指紋 `bde3ee6c3e80beb1`，lint 0／0。第一位獨立盲讀者提出四類問題（章節預告、章末承接、荊州問題未回收、重述及末章名），已針對最新版全部修正。仍需另一位盲讀者重新給 13 題判定後，才提交劇本關卡與付費媒體。
- `npm run test:docs-videos` 236 passed；`npm run check:tasks` validated 2070 files，警告均屬其他舊票或重疊 scope。原稿、口語稿各已付費製作旁白並通過當時的 113/113 語音比對；第三輪盲讀指出末段證據問題，故再修兩句並刪一張重複插圖。現稿 `script.md` SHA-256 `449ca0f7a131285669001520f34f5623e2c16ba85c36796023584625cc4aed91`，112 句／93 張插圖、估 9.1 分鐘，lint 0／0；新稿尚待全新盲讀、再合成改過的兩句與語音複查。已畫並通過第一張插圖，整集畫圖在盲讀前暫停，恢復時會重用此圖；先前整集報價 94 張、最多 US$3.81，現稿張數更少。每次 `approve` 均記下使用者委派而非聲稱站主親讀或親聽。
