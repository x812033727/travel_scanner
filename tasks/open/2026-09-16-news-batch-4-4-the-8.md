---
id: 2026-09-16-news-batch-4-4-the-8
title: "News batch 4.4: secondary news for the three verticals (AI/tech 8/1–9/15, crypto all-2026), zh-TW only"
status: in-progress
priority: P2
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-23T00:17:49Z
created_at: 2026-09-16T14:16:20Z
completed_at:
branch: claude/news-batch-4-4-secondary
depends_on: []
scope:
  - docs/news-2026-batch-4/agents/DELTA-4-4.md
  - docs/news-2026-batch-4/candidates-secondary-2026-ai.md
  - docs/news-2026-batch-4/candidates-secondary-2026-tech.md
  - docs/news-2026-batch-4/candidates-secondary-2026-crypto.md
  - docs/news-2026-batch-4/published-news-2026-09-23.md
  - docs/news-2026-batch-4/check_article.py
  - docs/news-2026-batch-4/build_assets.py
  - docs/news-2026-batch-4/update_index.py
  - docs/news-2026-batch-4/HANDOVER.md
  - docs/news-2026-batch-4/factcheck-draft
  - docs/ai-news-2026-09-late/research
  - docs/ai-news-2026-09-late/manifest.json
  - docs/tech-news-2026/research
  - docs/tech-news-2026/manifest.json
  - docs/crypto-news-2026/research
  - docs/crypto-news-2026/manifest.json
  - apps/api/app/guides/content/ai-news-2026-january-september-index.json
  - apps/api/app/guides/content/tech-news-2026-index.json
  - apps/api/app/guides/content/crypto-news-2026-index.json
  - apps/api/app/guides/content/ai-news-gemini-student-offer-20260820.json
  - apps/web/public/guides/ai-news-gemini-student-offer-20260820
  - apps/api/app/guides/content/ai-news-meta-muse-agent-20260909.json
  - apps/web/public/guides/ai-news-meta-muse-agent-20260909
  - apps/api/app/guides/content/ai-news-openai-cursor-wind-down-20260828.json
  - apps/web/public/guides/ai-news-openai-cursor-wind-down-20260828
  - apps/api/app/guides/content/ai-news-claude-text-watermark-20260815.json
  - apps/web/public/guides/ai-news-claude-text-watermark-20260815
  - apps/api/app/guides/content/ai-news-openai-zero-data-retention-20260820.json
  - apps/web/public/guides/ai-news-openai-zero-data-retention-20260820
  - apps/api/app/guides/content/ai-news-openai-hugging-face-incident-20260826.json
  - apps/web/public/guides/ai-news-openai-hugging-face-incident-20260826
  - apps/api/app/guides/content/ai-news-chatgpt-business-premium-seats-20260810.json
  - apps/web/public/guides/ai-news-chatgpt-business-premium-seats-20260810
  - apps/api/app/guides/content/ai-news-anthropic-alignment-security-20260831.json
  - apps/web/public/guides/ai-news-anthropic-alignment-security-20260831
  - apps/api/app/guides/content/ai-news-gemini-notebook-usage-limits-20260829.json
  - apps/web/public/guides/ai-news-gemini-notebook-usage-limits-20260829
  - apps/api/app/guides/content/tech-news-apple-child-safety-ios27-20260914.json
  - apps/web/public/guides/tech-news-apple-child-safety-ios27-20260914
  - apps/api/app/guides/content/tech-news-eu-dsa-designation-20260831.json
  - apps/web/public/guides/tech-news-eu-dsa-designation-20260831
  - apps/api/app/guides/content/tech-news-windows-11-26h2-20260827.json
  - apps/web/public/guides/tech-news-windows-11-26h2-20260827
  - apps/api/app/guides/content/tech-news-high-na-euv-12inch-photomask-20260908.json
  - apps/web/public/guides/tech-news-high-na-euv-12inch-photomask-20260908
  - apps/api/app/guides/content/tech-news-apple-rosetta-end-20260901.json
  - apps/web/public/guides/tech-news-apple-rosetta-end-20260901
  - apps/api/app/guides/content/tech-news-tsmc-sony-image-sensor-jv-20260811.json
  - apps/web/public/guides/tech-news-tsmc-sony-image-sensor-jv-20260811
  - apps/api/app/guides/content/tech-news-edge-manifest-v2-sunset-20260807.json
  - apps/web/public/guides/tech-news-edge-manifest-v2-sunset-20260807
  - apps/api/app/guides/content/tech-news-windows-age-api-20260908.json
  - apps/web/public/guides/tech-news-windows-age-api-20260908
  - apps/api/app/guides/content/tech-news-chromium-v8-kev-20260909.json
  - apps/web/public/guides/tech-news-chromium-v8-kev-20260909
  - apps/api/app/guides/content/tech-news-sign-in-with-apple-domain-20260824.json
  - apps/web/public/guides/tech-news-sign-in-with-apple-domain-20260824
  - apps/api/app/guides/content/crypto-news-treasury-genius-issuance-20260818.json
  - apps/web/public/guides/crypto-news-treasury-genius-issuance-20260818
  - apps/api/app/guides/content/crypto-news-taiwan-travel-rule-20260804.json
  - apps/web/public/guides/crypto-news-taiwan-travel-rule-20260804
  - apps/api/app/guides/content/crypto-news-korea-tokenized-securities-20260904.json
  - apps/web/public/guides/crypto-news-korea-tokenized-securities-20260904
  - apps/api/app/guides/content/crypto-news-japan-crypto-fraud-measures-20260806.json
  - apps/web/public/guides/crypto-news-japan-crypto-fraud-measures-20260806
  - apps/api/app/guides/content/crypto-news-taiwan-antifraud-rules-20260720.json
  - apps/web/public/guides/crypto-news-taiwan-antifraud-rules-20260720
  - apps/api/app/guides/content/crypto-news-sec-transfer-agent-dlt-20260904.json
  - apps/web/public/guides/crypto-news-sec-transfer-agent-dlt-20260904
  - apps/api/app/guides/content/crypto-news-paxos-clearing-agency-20260529.json
  - apps/web/public/guides/crypto-news-paxos-clearing-agency-20260529
  - apps/api/app/guides/content/crypto-news-cftc-perpetual-contracts-20260603.json
  - apps/web/public/guides/crypto-news-cftc-perpetual-contracts-20260603
  - apps/api/app/guides/content/crypto-news-stablecoin-cip-20260622.json
  - apps/web/public/guides/crypto-news-stablecoin-cip-20260622
  - apps/api/app/guides/content/crypto-news-treasury-state-regime-20260403.json
  - apps/web/public/guides/crypto-news-treasury-state-regime-20260403
---

# News batch 4.4: secondary news for the three verticals, zh-TW only

## Why

批次 4.1–4.3 只寫了頭條；8 月 1 日到 9 月 15 日之間對讀者有用但沒排進頭條的官方公告（方案與計費、開發平台政策、
資料保留條款、家庭與兒少功能、具名漏洞、標準組織文件、政府方案的規則）一直沒有人整理，幣圈在同一界線下
（法規、技術、產業運作，不碰行情）2026 全年也還有一批份量較輕的法規動作沒寫。站主 2026-09-23 圈選探索代理
重建的候選清單：三個垂直全收，共 29 篇，只做 zh-TW。

## Definition of done

- [ ] 29 篇內容包（AI 9、科技 10、幣圈 10；slug 與 display_order 在 `agents/DELTA-4-4.md` 第 3 條）都有研究紀錄
      （`sourcing_verdict: full`）、兩輪不同代理的查核報告（`factcheck-draft/<slug>-round1|2.md`）、一張圖（`build_assets.py` `# 4.4` 區）。
- [ ] 每篇 `check_article.py <slug> --assets` OK（不帶 `--full`）、`pack_cli lint --kind life --slug` 零錯誤。
- [ ] 三個索引只動 zh-TW（`update_index.py --locale=zh-TW`，AI 依事件日插月份群），en／ja／ko／zh-CN 逐位元不變。
- [ ] 合併、部署、`guides-import --locale zh-TW --slug ×29 ＋三索引`（先 dry-run：29 create＋3 update）、發布、複核 dry-run 全 unchanged、
      `verify_public.py --from-report` 全 PASS；數字寫回本票與 HANDOVER §1g。

## Steps

- [ ] 候選清單三份、去重表、`agents/DELTA-4-4.md` 進 repo；`check_article.py` `RELATED` 加 `# 4.4` 區（已定第二連結）。
- [ ] 每篇一位 opus 研究代理（≤6 一波）寫研究紀錄 → sonnet 撰稿 → 兩輪 opus 查核 → 協調者裁決 → 繪圖 → relink → 索引。
- [ ] 額度規則：5 小時窗 >70% 或週額度 >90% 就停，未完成的篇在本票的進度節註明。
- [ ] commit、PR、CI、站主明確選「合併」→ 部署 → 匯入 → 驗證 → 本票 done。

## How to verify

- `PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe ../../docs/news-2026-batch-4/check_article.py <slug> --assets` 每篇 exit 0。
- `./.venv/Scripts/python.exe -m app.guides.pack_cli lint --kind life --slug <slug> …` 零錯誤、零 `image_missing`、零 `raw_internal_url`。
- `update_index.py ai tech crypto --locale=zh-TW --dry-run` 只有 zh-TW hunk；第二次執行拒絕。
- `pytest tests/test_guides_content_pack.py tests/test_guides_content_links.py -q`、`npm run check:tasks`。

## Notes

- 探索代理的原始抓檔與腳本留在 `C:\Users\x8120\mokaair-work\news44\`（不進 repo）；指派表 `news44/ASSIGNMENTS-44.md`。
- 4.7 的教訓照 DELTA-4-7 第 11、13 條；本輪新增的網路坑在 DELTA-4-4 第 6 條。
- 不做的「改維護票」項目列在 DELTA-4-4 第 5 條，要做另開票。

## 進度（2026-09-23，第一波六篇）

- 站主決定：候選全收 29 篇，但額度先給第八批；本波只做 AI #1–6，其餘 23 篇 9/27 週額度重置後續（研究 W2 從 #7 起）。
- 六篇研究（全 full）→ 撰稿 → 兩輪查核完成，兩輪合計 597 條主張、103 處改動；裁決與數字在 HANDOVER §1g；報告 12 份在 `factcheck-draft/`。
- 索引：`update_index.py ai --locale=zh-TW`（EXPANDED_ON 2026-09-23）把六個連結依事件日插進 8 月群（08-15、08-20、08-20、08-26、08-28）與 9 月群（09-09）；
  en／ja／ko／zh-CN 逐位元不變；第二次執行拒絕。科技與幣圈索引本波未動。
- relink 六篇（10 個連結轉 article inline）。繪圖：`build_assets.py` `# 4.4` 區六個函式；AI 整垂直重跑出 manifest 與 sheet。
