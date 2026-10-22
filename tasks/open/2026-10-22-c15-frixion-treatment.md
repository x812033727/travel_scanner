---
id: 2026-10-22-c15-frixion-treatment
title: Research C15 FriXion brand story treatment and sources
status: review
priority: P1
area: docs
owner: codex-gpt6-c15-treatment
claimed_at: 2026-10-22T16:41:36Z
created_at: 2026-10-22T16:41:23Z
completed_at:
branch: codex/brand-story-frixion-c15-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-frixion-c15
---

# Research C15 FriXion brand story treatment and sources

## Why

新系列 C15 只有 20 題表上的取證入口；必須先釐清 FriXion 是熱致無色、早期技術先用於變色杯／玩具、與 2002 ILLUSION 的差別，以及不同年代 60／65°C 說法，才可把「擦得掉」寫成可查核的品牌故事。

## Definition of done

- [x] 有六章、連續問題與 30–45 秒節拍的非虛構 Treatment；包含濃縮開場、5 秒片頭、21 秒片尾與連結位。
- [x] 有可直接讀的 PILOT 原廠及專利原件、逐項 M01–M14 主張邊界。
- [x] 另一位代理獨立重讀原件，初版 HOLD 後差異重核 PASS；兩輪收據各綁定 Treatment／矩陣 SHA。
- [ ] 草稿 PR 供站主審核；企劃採用、逐字稿、付費各自分關。

## Steps

- [x] 確認本題未由其他任務／分支佔用，建立專用工作樹與窄範圍任務。
- [x] 重讀 PILOT 兩篇 2024 開發回顧、現行商品與回色 FAQ、2017 新聞稿及熱變色微膠囊專利。
- [x] 撰寫 Treatment 與來源矩陣，保留公司回顧／現行規格的差異。
- [x] 獨立覆核、窄修、提交，建立草稿 PR #1696。
- [ ] 站主審閱修訂企劃並決定採用或退修。

## How to verify

`git diff --check`；`npm run check:tasks`；`npm run test:docs-videos`（若環境缺模組，明示該環境問題）。另由獨立審查者實際開 S1–S6 核對 M01–M14；即使文件測試綠，也不能代替來源核對。

## Notes

2026-10-23：PILOT 2024 開發回顧寫早期變色範圍 -20–65°C 的開發結果、2017 新聞稿約 65°C；現行 FAQ 則寫消色設定 60°C。文件說法不能合成所有年分統一的精確門檻。PILOT 原廠回顧提供 1970、1976、1988、2002、2004、2006、2007、2010 節點；專利 US20060112851A1 僅作微膠囊技術旁證，不能替代未找到的 1972 原案。全部來源連結及禁止推論見 `docs/videos/story-everyday-frixion-c15/source-matrix.md`。

2026-10-23：另一位代理初版判 M03、M07、M08 與跨章年數 HOLD；作者依其窄修，保留舊版 HOLD 收據。該代理重核新版 Treatment SHA `D84494C81E2034B116C0322EF416E17C3DDE860B58626D12DE2E73501980D9C0`、矩陣 SHA `6E030F4399F6FD2AE99550DE89B5B46658D708CF870910199804069A784C4C09` 後，回報 M01–M14 與六章在企劃來源關卡 PASS；作者誠實轉錄在 `reviews/independent-treatment-delta-v2.md`。站主採用未取得。
