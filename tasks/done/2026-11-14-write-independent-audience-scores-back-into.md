---
id: 2026-11-14-write-independent-audience-scores-back-into
title: Write independent audience scores back into the Curio and So Thats Why pools
status: done
priority: P2
area: tools
owner: claude-opus-5-5-pool-audience
claimed_at: 2026-11-14T17:02:20Z
created_at: 2026-11-14T17:02:17Z
completed_at: 2026-11-14T17:16:25Z
branch: claude/determined-lamport-1dky28
depends_on: []
scope:
  - tools/video/curio/pool
  - tools/video/so-thats-why/pool
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
---

# Write independent audience scores back into the Curio and So Thats Why pools

## Why

站主 2026-11-14 要求把奇聞檔案局與原來如此事務所兩個素材池掃一次，列出獨立觀眾評分並排名，接著要求「把分數寫回題目池」，而且「之後擴充如果有成題的也要補評分」。兩池原本沒有任何觀眾評分欄位。成片的觀眾評分關卡（`review/audience-review.md`）只評做好的影片，選題階段沒有吸引力的參考。

## Definition of done

- [x] 兩池每一組 ≥ 8 分鐘的長題案在 `themes.json` 帶 `audience`（分數、名次、五項、短評、紀錄檔），`THEMES.md` 開頭有排名表。
- [x] 奇聞入選單集長題的抽樣分數經 build 掛到 `pool.json` 的 `audience`。
- [x] 每池一份 `reviews/audience-20261114.json`：方法、錨點、評審偏移、每題分數。
- [x] 可成題長題沒有評分時，`build`／`check` 失敗；兩池 README 寫明之後怎麼補評。

## Steps

- [x] 長題案評分：奇聞 155 組（3 位評審），原來如此 108 組（3 位評審，含 PR #2093 新增的 G630–G648），每批同一組錨點題校正。
- [x] 奇聞單集題：206 題分層抽樣（4 位評審，6 題錨點）；寫回其中 156 題入選的 `episode_core`（片長下限 ≥ 8 分鐘）。
- [x] `render.mjs` 驗證並輸出 `audience`；奇聞 `core.mjs` 讀 `reviews/audience-*.json` 掛到候選題；測試補上。
- [x] 以 PR #2093 的池子為基底重建兩池，`check` 通過。

## How to verify

```bash
node tools/video/curio/pool/cli.mjs check
node tools/video/so-thats-why/pool/cli.mjs check
node --test tools/video/curio/pool/pool.test.mjs tools/video/so-thats-why/pool/pool.test.mjs
```

## Notes

- 本分支建在 `claude/pool-expansion-20261113`（PR #2093）之上，因為那才是兩池的現況（1,512／5,125、長題 107 組）。PR #2093 合併後，本分支再對 main rebase。
- 原來如此的「入選問題」是一句話的機制素材（約 1–2 分鐘），不是一集。同日評過的 206 張單題卡只當參考，不寫回。能成片的單位是題案。
- 評審共同的意見：奇聞後補的 N 題「題目」欄常是一整段考據摘要，不像片名；原來如此的新長題（G630–G648）片名太長、中段術語堆疊，排名多在中後段。這兩點可以另開票改片名與章節。
- 奇聞還有約 1,000 題入選單集長題沒有評分。檢查目前只要求題案有評分，單集題不擋；要全部補評時，用同一份錨點分批派評審。
