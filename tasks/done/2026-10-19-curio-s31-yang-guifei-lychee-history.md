---
id: 2026-10-19-curio-s31-yang-guifei-lychee-history
title: Curio S31 Yang Guifei lychee history episode
status: done
priority: P2
area: docs
owner: codex-gpt6-s31
claimed_at: 2026-10-19T23:23:52Z
created_at: 2026-10-19T23:23:49Z
completed_at: 2026-10-19T23:51:09Z
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s31
---

# Curio S31 Yang Guifei lychee history episode

## Why

站主授權持續製作新的奇聞檔案局歷史集。S31 的流行講法常把杜牧詩句、《新唐書》騎傳、白居易荔枝圖序拼成一條確定的荔枝路線與天數；目前找到的古籍並沒有同一批貨的逐站記錄。先完成能查核、能交給音訊與畫面製作的文稿和分鏡。

## Definition of done

- [x] `docs/videos/curio-s31` 有 8 分鐘以上正文的故事稿、2–3 個大綱、固定版史料、逐句主張及可渲染靜圖分鏡。
- [x] 獨立讀者重新盲讀通過；系列 lint 零錯誤零警告；交接註明音訊及付費媒體尚未開始。

## Steps

- [x] 固定杜牧、《新唐書》、白居易與《舊唐書》全文網址／commit／本地全文 SHA-256，核對原句及不能推定的果園、里程與速度。
- [x] 寫 brief、research、claims、video.json、script.md；圖片提示詞依可愛懸疑系列，音樂沿用系列固定值。
- [x] 完成獨立盲讀後，核對最終 script SHA，寫 verify 與交接。

## How to verify

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s31`；`node tools/video/cli.mjs script --slug curio-s31`；`node tools/video/cli.mjs narrative --slug curio-s31`（另一位不看研究筆記的讀者回答）；`npm run test:docs-videos`；`npm run check:tasks`。逐句對照 [claims.md](../../docs/videos/curio-s31/claims.md) 和 [research.md](../../docs/videos/curio-s31/research.md)。

## Notes

- 全文 pin `garychowcmu/daizhigev20` commit `4a6d6f2088825f132521d848c2ea86cf9c9a7620`。`research.md` 列四個全文 SHA-256 和原句；杜牧《樊川文集》一騎是詩的場景，《新唐書》只說騎傳、數千里、味未變到京師；其〈禮樂志〉「南方」不等於果園；《舊唐書》轉引白居易巴峽荔枝的變味時序，不是楊妃那批貨的獨立紀錄。
- 先前獨立盲讀指出開場像目錄、來源與數字重述、終章重報證據；已逐項修文。第五位新讀者對最終 script SHA `72eb00f5f0f05268dc9125705c3e75eaea98b8b933e2471fb42cf6e28762826c` 盲讀，13 題全過，逐題紀錄在 `docs/videos/curio-s31/narrative-review.json`。固定版來源與插圖 prompt 沒有畫出特定驛路或保鮮器具。
- 2026-10-19：現版 97 句、96 張 still、8 章、18 條 `loops`，系列 lint 0 errors／0 warnings，預估全片 9.4 分鐘、開場 46 秒、正文約 8 分 35 秒；`npm run test:docs-videos` 236/236 passed，`npm run check:tasks` exit 0（其他舊票有警告）。尚未執行 TTS、音檢、MiniMax、配樂或成片，費用 US$0。後續媒體製作另行交接。
