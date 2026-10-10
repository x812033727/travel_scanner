---
id: 2026-10-10-curio-topic-bank-checks
title: Curio topic bank: independent re-check of H02-H07, then H08 and the other four axes in small batches
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-10T14:38:30Z
completed_at:
branch: claude/curio-topic-checks
depends_on: []
scope:
  - docs/videos/history-curiosity/topic-checks
  - docs/videos/history-curiosity/topics.json
---

# Curio topic bank: independent re-check of H02-H07, then H08 and the other four axes in small batches

## Why

奇聞檔案局的題庫（`docs/videos/history-curiosity/topics.json`，40 題）只有拍成集的 H01、U02、L08 查核過。2026-10-10 第一次整批查核（每題一個研究代理加一個覆核代理）因帳號每週用量上限中斷：H02–H07 的研究寫完了（`topic-checks/H02.md`–`H07.md`），但沒有人重開來源覆核，`topics.json` 仍是 `candidate`；H08 與 M、P、U、L 四軸的 31 題還沒查。前三集每一集都在查核時改掉題目卡上的事實（H01 的熱飯菜、U02 的「否認 58 年」、L08 的年份），沒查過的題目卡不能直接拿來寫企劃。

## Definition of done

- [x] H02–H07 各有「## 獨立覆核」一節（另一個代理重開來源，逐列 UPHELD／REFUTED／UNOPENED），通過的題目在 `topics.json` 改成 `checked`，`note` 寫查核後的更正；被否決的寫明處置。（2026-10-10：六題都是 ADOPT_WITH_CHANGES，都改成 `checked`。）
- [ ] H08 研究加覆核。
- [ ] M、P、U、L 四軸：站主或下一季的排程決定先做哪一軸；每批 4–8 個代理，批與批之間看一次用量。
- [ ] `topic-checks/README.md` 的狀態表與實際一致。

## Steps

- [x] 開票、認領；第一批只放三個覆核代理（H02–H04），量每個代理的用量。
- [x] H05–H07 的覆核。
- [x] 依覆核結果改 `topics.json`（只改通過獨立覆核的題目）與 README 狀態表。
- [ ] H08；其餘四軸分批。

## How to verify

`grep -L "## 獨立覆核" docs/videos/history-curiosity/topic-checks/H0*.md` 沒有輸出；`python -X utf8 -c "import json;d=json.load(open('docs/videos/history-curiosity/topics.json',encoding='utf-8'))"` 可解析，`checked` 的題目都有對應的覆核一節；`npm run test:tools` 的衛生測試沒有抓到本機路徑。

## Notes

- 2026-10-10 H02–H07 覆核完成（claude-opus-curio-topics）：六個代理各重開一題的全部來源，實測每個 25 萬到 39 萬 token、17 到 28 分鐘（合計約 179 萬 token）。六題都維持「改過後可採用」，沒有一題的主幹被推翻，但每題都有一到四列被否決或改判；最要緊的三件：H03「八千萬棵樹」是 1933 年的粗估（面積高估約四倍）、H07「鐵是伏爾泰 1751 年才寫的」不成立（1738 年的信已有）、H03 最有名的倒樹照片不是可靠的公有領域檔。逐題的改動與要站主決定的事在 `docs/videos/history-curiosity/topic-checks/README.md` 的表與各檔的〈獨立覆核〉。
- 題目卡怎麼寫回題庫：scratch 的小腳本從各檔〈題目卡（查核後）〉讀 `title`／`hook`／`finding` 與處置，沒有〈獨立覆核〉一節就拒絕；`photo_candidates` 改成指向該檔的圖片清單（原卡的候選圖有幾張覆核後不能用）。
- 覆核代理不准跑 git、只准改自己那一個檔；`topics.json` 與 README 由主線改。六個代理同時在一個 worktree 裡各改各的檔，沒有互相蓋到。
- 還沒做：H08 與 M、P、U、L 四軸的 31 題。照這次的量，一題研究加覆核約 50 萬到 70 萬 token；四軸全做約 1,500 萬到 2,000 萬，要分批、看用量，先做下一季要拍的那一軸。
- 2026-10-10：覆核代理的提示沿用第一次整批查核的寫法（預設否決、引句要在頁面上找得到、打不開的頁不算數、圖片逐張看授權頁）。一個做網路查核的代理約 15–30 萬 token，見票 `2026-10-10-history-curiosity-pilot`（已結案）的教訓：不要一次放幾十個。
