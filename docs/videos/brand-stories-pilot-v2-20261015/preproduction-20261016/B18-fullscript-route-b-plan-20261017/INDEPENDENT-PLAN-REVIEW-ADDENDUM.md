# B18 Route B 設計審查補充：12 筆事實超過現行上限

- 補充日期：2026-10-17；審查者：Codex `/root/b18_script_scene_alignment/b18_route_b_plan_review`。
- 原審查收據 `INDEPENDENT-PLAN-REVIEW.md` SHA-256 `679c20ceb91cee5b3280eef0df6f0e319705bac3d58398b14c6638d335710a98`；原設計 `route-b-plan.json` SHA-256 `3b3183525d995950bc9366ecffd82595938817eca09a8a4d6ca95100d1e88985`。本補充**不修改原審查**，只記錄當時漏查的現行匯入限制。
- schema 證據：`tools/video/story-plans/plan.mjs` SHA-256 `5ec625989c2aa9f86ea837b6c03f189554746618825292ad1c30fad1b6988de5`，第 162 行：`must_verify` 必須有 **4–10** 筆；第 169 行另有每筆 claim 200 字限制。父版已是 10 筆；原設計再 append 1967 法院事實索引 10、盤色事實索引 11，會成為 12 筆，無法通過 `storyProblems`。原審查只核對來源、25 段／85 景／65 claim 清單，漏掉 schema 上限。

**修正結論：原 12 筆事實 Route B 設計有 P1 採用阻斷；原報告的「設計候選 PASS、P1/P2 0」只適用於其來源與覆蓋率檢查，不可當成可落地企劃列的結論。原設計維持 HOLD，不能匯入、套用到 active 或付費製作。** 後繼 `../B18-route-b-row10-candidate-20261017/` 保留十個索引，以合併同來源的事實作為另外受審的方案；它的 schema PASS 也不會自動解除來源、歸屬口播及正式 worker／影片關卡。
