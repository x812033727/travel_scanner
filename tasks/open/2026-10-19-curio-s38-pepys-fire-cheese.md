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
- [x] 完成 R4 [影片稿](../../docs/videos/curio-s38/video.json) 與 [旁白稿](../../docs/videos/curio-s38/script.md)：112 句、111 個畫面、12 組懸念回收、估 9.995 分鐘，lint 0 error / 0 warning。劇本檔 SHA-256 `62af2f7d762b082a1e6910df28a721fac6c14cb4d081f06516f48b5511cd1411`；影片稿 SHA-256 `f497a97a9de671ba39dad98f92898671035dae6c1ccace5f8740b215a18da4e5`。
- [x] 首輪獨立 [盲讀與史料／畫面覆核](../../docs/videos/curio-s38/verify-1.md) 已留原始答案和 10/13 失敗證據；R2 已集中修正其敘事斷點、無依據的掃水方向與六處畫面問題。
- [x] R2 獨立敘事盲讀 13/13，但來源查核抓到 9 月 2 日午餐前後的事件倒置；這份 R2 劇本不得用於媒體製作。
- [x] R3 獨立敘事盲讀 13/13；史料／畫面查核發現搬走與清點混用、未記錄的寫作時刻、9 月 4 日花園討論的下午時序，以及塔樓、筆記、書面報告畫面問題。R4 已按固定日記集中修正；R3 不能作媒體製作依據。
- [ ] 交給另一位未參與撰稿的讀者在看研究／既有覆核前，對 R4 已鎖定 SHA 的旁白獨立回答 13 題；另查固定日記原句及每個畫面提示詞。保存新原始答案與覆核紀錄，並以實際語音量測正文是否至少 8 分鐘。
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

固定日記：GITenberg `68fcf49f70ee793b989a6fd0464264d55beb4451`；`4200.txt` SHA-256 `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`。本工單僅認領 `docs/videos/curio-s38/**`，不碰已有歸屬的 S01／S09／S18。R1 盲讀 10/13 未過；R2 敘事 13/13 卻有來源時序錯誤；R3 敘事 13/13 卻有來源／畫面問題；R4 待新讀者覆核。未簽核稿件、未花費任何媒體權杖。另有 [題目可行性筆記](../../docs/videos/history-curiosity/source-feasible-expansion-20261019.md)：S27／S21 因同期互補資料在本雲端未能重開，暫停進入製作。
