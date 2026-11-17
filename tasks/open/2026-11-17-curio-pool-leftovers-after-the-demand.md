---
id: 2026-11-17-curio-pool-leftovers-after-the-demand
title: Curio pool leftovers after the demand-score work
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-11-17T11:45:12Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool/batches
  - docs/videos/history-curiosity/pool/legacy
  - docs/videos/history-curiosity/pool/reviews
  - docs/videos/history-curiosity/pool/selection.json
---

# Curio pool leftovers after the demand-score work

## Why

PR #2136（票 `2026-11-17-fold-a-demand-dimension-into-the`）替奇聞檔案局素材池加了需求分、收了三批商業與品牌題、
評了 499 題並改包裝了近門檻的題。有幾件事當時沒做，也不屬於別張票；記在這裡，免得只留在對話裡。
來源查無的批次另有票 `2026-11-17-so-that-s-why-waves-89`，不在這張的範圍。

## Definition of done

- [ ] N2501（Fisher 的鬼魂）的 `answer_target` 是完整的答案，不是覆核修訂註記。
- [ ] 舊題庫檔裡總分 6.0–6.5 的 14 題單集題，決定要不要改包裝；要改的話寫回規則寫進池 README。
- [ ] 改包裝時沿用、查核內容沒載的名稱，以及舊問句裡沒出處的字眼，有一份清單可以在寫劇本前對。

## Steps

- [ ] **修 N2501。** 它在 `pool.json` 的 `answer_target` 開頭是「（只改兩處，其餘照原文）」，原本的答案被覆核的修訂註記蓋掉了。
  從 `batches/` 裡它所屬批次檔的 git 歷史找回修訂前的 `answer_target`，把兩處修訂套進去再寫回；`selection.json` 的 `raw_changes` 要寫理由。
- [ ] **舊題庫的 14 題。** 代號：G05、G06、G07、G09、H23、H28、H31、H34、L28、L34、U05、U08、U39、U40。
  它們的問句不在 `batches/`，在舊題庫來源（`legacy/` 與 `pool-records.json` 的 legacy 紀錄），改寫後寫回哪裡要先讀 `tools/video/curio/pool/core.mjs` 的 legacy 讀法。
  這些題的問句本來就短（多半 40–60 字），前一輪的經驗是短問句改包裝只救得回少數，做之前先估值不值得。
- [ ] **沒出處的字眼。** 改包裝第 4–7 輪的改寫編輯回報：舊問句裡有不少查核內容不支持的字眼（例如「24 噸」「上千隻蝙蝠」「世界最老」「印在日本教科書上」）。
  被採用的改寫已經拿掉；沒被採用、維持原文的題還留著。第 8、9 輪採用的 8 題沿用了名稱，列在各題 `notes`（搜尋「沿用原問句」）。
- [ ] **參考頻道方向第 81 名以後（站主 2026-11-17 決定先停，這一項不代表要做）。** 要續收時：
  `docs/videos/history-curiosity/reference-heimao-20261031/topics.json` 的 W、asia、tech、everyday 四類依 `views` 由高到低排，前 80 名已處理（wave72–74）。
  下一批題號從 N7401、研究代理 ZT1–ZT4、覆核 R751–R754。三批每批過 6.5 的題數是 3、5、2，越後面越少；建議先用品牌四問篩方向，只研究中兩題以上的。

## How to verify

```bash
node tools/video/curio/pool/cli.mjs pairs    # 0 pending
node tools/video/curio/pool/cli.mjs build && node tools/video/curio/pool/cli.mjs check
node tools/video/pool-admin/bundle.mjs build && node tools/video/pool-admin/bundle.mjs check
node --test tools/video/curio/pool/pool.test.mjs tools/video/pool-admin/bundle.test.mjs
```

## Notes

- 做法都在 `docs/videos/history-curiosity/pool/README.md`：〈獨立觀眾評分〉記評分、校正與改包裝的規則與每一輪的結果；
  〈第七十二批〉到〈第七十四批〉三節記收新題的流程（請求紀錄、非作者覆核、主編抽查）。
- 改包裝的複評紀錄檔名要排在既有紀錄之後才會生效（build 依檔名順序套用），當時用 `audience-20261117z-repack<n>.json`。
- 當時用的抓取工具、研究與覆核說明、改包裝腳本都在工作階段的暫存區，沒有進 repo；要重做得照 README 重建。
- 總分 6.5 以上的單集題清單（2026-11-17 快照）：`docs/videos/history-curiosity/pool/reviews/cores-6.5-20261117.md`。
