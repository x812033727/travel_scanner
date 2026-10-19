---
id: 2026-10-19-curio-s38-pepys-fire-cheese
title: Curio S38 Pepys fire and cheese historical episode
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-next-episode
claimed_at: 2026-10-19T22:34:44Z
created_at: 2026-10-19T22:34:43Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s38
---

# Curio S38 Pepys fire and cheese historical episode

## Why

為奇聞檔案局新增 S38〈倫敦大火時，佩皮斯為何把起司埋進土裡？〉。這個小動作有可重開的 1666 年日記原文，但網路轉述常加上起司大小、價值或被挖回的結局；本集按 9 月 2–6 日的行動順序講完整故事，並保留日記沒有回答的部分。

## Definition of done

- [ ] 一支經史料、敘事、旁白、插圖與輸出覆核的繁中歷史影片可提交站主發佈審核，並清楚區分佩皮斯親見、聽聞與日記留白。
- [ ] 正片至少 8 分鐘；本機影片與字幕的封裝／QA 證據可重開。

## Steps

- [x] 固定可重開的日記全文與版號，寫 [企劃](../../docs/videos/curio-s38/brief.md)、[研究](../../docs/videos/curio-s38/research.md)、[逐句主張](../../docs/videos/curio-s38/claims.md)。
- [x] 完成 [影片稿](../../docs/videos/curio-s38/video.json) 與 [旁白稿](../../docs/videos/curio-s38/script.md)：102 句、101 個畫面、10 組懸念回收、估 8.9 分鐘，lint 0 error / 0 warning。劇本檔 SHA-256 `461c0d454b94e370c4071c6a7f8c75326976fd7d796d347a44a030f7323efeea`。
- [ ] 交給未參與撰稿的讀者在看研究／既有覆核前，對同一份已鎖定 SHA 的旁白獨立回答 13 題；另查固定日記原句及每個畫面提示詞。把原始回答與修稿紀錄保存於 `verify-1.md`。
- [ ] 劇本過門檻後按 `curio-episode` 的整集報價及審核程序製作語音、插圖、分鏡、音樂、字幕、正片，完成輸出與包裝 QA。

## How to verify

在 `/workspace/travel_scanner` 執行：

```bash
VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s38 --json
sha256sum docs/videos/curio-s38/script.md docs/videos/curio-s38/video.json docs/videos/curio-s38/claims.md
npm run check:tasks
```

核對 `docs/videos/curio-s38/research.md` 中 GITenberg 固定 commit 的 1666 年 9 月 2–6 日原文，尤其 9 月 4 日兩個土坑、9 月 2 日塔樓官員轉述的起火地點、9 月 5 日局部止火和 9 月 6 日起司去向未記載。

## Notes

固定日記：GITenberg `68fcf49f70ee793b989a6fd0464264d55beb4451`；`4200.txt` SHA-256 `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`。本工單僅認領 `docs/videos/curio-s38/**`，不碰已有歸屬的 S01／S09／S18。未經獨立盲讀；未簽核稿件、未花費任何媒體權杖。另有 [題目可行性筆記](../../docs/videos/history-curiosity/source-feasible-expansion-20261019.md)：S27／S21 因同期互補資料在本雲端未能重開，暫停進入製作。
