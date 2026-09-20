---
id: 2026-09-19-news-batch-4-6-news-since
title: News batch 4.6: news since 2026-09-18 (AI 4, tech 4, crypto 3, zh-TW only) plus two updates
status: done
priority: P2
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-19T18:09:01Z
created_at: 2026-09-19T18:08:59Z
completed_at: 2026-09-19T23:49:54Z
branch: claude/news-batch-4-6-since-0918
depends_on: []
scope:
  - docs/ai-news-2026-09-late/research
  - docs/tech-news-2026/research
  - docs/crypto-news-2026/research
  - docs/news-2026-batch-4/check_article.py
  - docs/news-2026-batch-4/build_assets.py
  - docs/news-2026-batch-4/verticals.py
  - docs/news-2026-batch-4/tech.md
  - docs/news-2026-batch-4/agents/DELTA-4-6.md
  - apps/api/app/guides/content/ai-news-anthropic-accenture-evaluation-20260918.json
  - apps/web/public/guides/ai-news-anthropic-accenture-evaluation-20260918
  - apps/api/app/guides/content/ai-news-openai-australia-youth-safety-20260918.json
  - apps/web/public/guides/ai-news-openai-australia-youth-safety-20260918
  - apps/api/app/guides/content/ai-news-gemini-notebook-study-tools-20260918.json
  - apps/web/public/guides/ai-news-gemini-notebook-study-tools-20260918
  - apps/api/app/guides/content/ai-news-kimi-k3-bedrock-20260918.json
  - apps/web/public/guides/ai-news-kimi-k3-bedrock-20260918
  - apps/api/app/guides/content/tech-news-npm-stage-only-tokens-20260918.json
  - apps/web/public/guides/tech-news-npm-stage-only-tokens-20260918
  - apps/api/app/guides/content/tech-news-cisa-kev-linux-kernel-20260918.json
  - apps/web/public/guides/tech-news-cisa-kev-linux-kernel-20260918
  - apps/api/app/guides/content/tech-news-windows-cloud-rebuild-20260918.json
  - apps/web/public/guides/tech-news-windows-cloud-rebuild-20260918
  - apps/api/app/guides/content/tech-news-iphone-duo-dev-resources-20260918.json
  - apps/web/public/guides/tech-news-iphone-duo-dev-resources-20260918
  - apps/api/app/guides/content/tech-news-taiwan-matsu-cable-tm4-20260918.json
  - apps/web/public/guides/tech-news-taiwan-matsu-cable-tm4-20260918
  - apps/api/app/guides/content/tech-news-apple-september-hardware-20260909.json
  - apps/web/public/guides/tech-news-apple-september-hardware-20260909
  - apps/api/app/guides/content/crypto-news-eba-third-party-risk-20260918.json
  - apps/web/public/guides/crypto-news-eba-third-party-risk-20260918
  - apps/api/app/guides/content/crypto-news-occ-three-trust-charters-20260918.json
  - apps/web/public/guides/crypto-news-occ-three-trust-charters-20260918
  - apps/api/app/guides/content/crypto-news-sec-crypto-fraud-patterns-20260918.json
  - apps/web/public/guides/crypto-news-sec-crypto-fraud-patterns-20260918
---

# News batch 4.6: news since 2026-09-18 (AI 4, tech 4, crypto 3, zh-TW only) plus two updates

## Why

站主 2026-09-20 要求「補 AI／科技／幣圈相關新聞」。三個垂直的內容包最新只到 9/17–9/18，
本批接續 4.5 的做法只寫 **2026-09-18 之後**的新消息，並依站主選擇**只做 zh-TW**（不翻譯、不逐語審稿）。

三位 opus 探索代理各掃一個垂直的官方來源（規格 `docs/news-2026-batch-4/{ai,tech,crypto}.md`），
9/19–20 是週末、三個垂直都沒有一手來源的新消息，所以全部 19 個候選都是 9/18。站主圈選：

- AI 4 篇：Anthropic 找 Accenture 駐點評測、OpenAI 澳洲青少年安全藍圖、Gemini Notebook 開學工具（三則併一篇）、Kimi K3 上 Amazon Bedrock
- 科技 4 篇：npm 只送審權杖、CISA 把三個 Linux 核心漏洞列為已遭利用、Windows 11 Cloud rebuild、iPhone Duo 開發資源
- 幣圈 3 篇：OCC 同日核准三家穩定幣信託銀行、EBA 第三方風險最終指引、SEC 執法處長點名兩種詐騙包裝
- 另兩則與既有文章重疊太高，站主選「更新既有文章」：馬祖 5G 示範 → `tech-news-taiwan-matsu-cable-tm4-20260918`；
  Apple 9/18 全球開賣 → `tech-news-apple-september-hardware-20260909`

規則差異在 `docs/news-2026-batch-4/agents/DELTA-4-6.md`；協調者狀態檔（進度、代理 id、樣板）在該 session 的
scratchpad `news46/STATE-4-6.md`；探索候選檔 `news46/candidates-{ai,tech,crypto}.md`。

## Definition of done

- [x] 11 篇 zh-TW 內容包各有研究紀錄（各垂直 `research/<slug>.json`，4.5 的 schema，無 translations），
      經撰稿、兩輪獨立查核，`check_article.py --full --assets` 全過，`pack_cli lint --kind life` 0 error
- [x] 兩則更新：已評估——目標文章是五語系且字數頂格，只加一節與 checker 互斥；兩位代理的改動已還原，另開票 `multi-language-maintenance`（見 Notes）
- [x] `check_article.py` RELATED 與 `verticals.py` 接續號段：AI 167–170、科技 317–320、幣圈 214–216
- [x] 三個索引文章不改標題；索引增補另開 `2026-09-19-4-6-11-zh-tw-update`（update_index.py 是五語機制，zh-TW-only 不能直接套）
- [x] PR 合併、部署後 `guides-import --slug`（先 dry-run 核對計畫），正式站每篇 200、可索引、在 `life-zh-TW.xml`
- [x] 本票記下 slug 清單、dry-run／publish 輸出與驗證結果

## Steps

- [x] 探索（3 位 opus）→ 19 候選；站主圈選 11＋2（2026-09-20）
- [x] 開 worktree `news46-0918`、分支 `claude/news-batch-4-6-since-0918`、本票
- [x] 研究紀錄第一波（opus ×6：AI ×4、幣圈 OCC、EBA）— 已派出，寫到 scratchpad 再搬進工作區
- [x] 研究紀錄第二波（opus ×5：科技 ×4、幣圈 SEC）
- [x] 更新代理 ×2（sonnet）：馬祖 5G、Apple 開賣 —— 各完成核對，但 --full 三個結構性 FAIL（字數／來源數／五語 parity）；還原，diff 存 scratchpad，另開票
- [x] 幣圈三個 slug 定案後補進本票 scope
- [x] `DELTA-4-6.md`、`check_article.py` RELATED、`verticals.py`
- [x] 撰稿（sonnet ×11，5 小時窗 19:20Z 重置後派）→ 查核第一輪（opus）→ 第二輪（opus，SECOND-ROUND）
- [x] 出圖、`check_article.py --assets`（不帶 --full）、relink、lint、commit、PR
- [x] 站主 AskUserQuestion 明確選「合併並發布」→ 部署 → `guides-import --slug` → 驗證 → 本票 done

## How to verify

```bash
cd docs/news-2026-batch-4 && for s in <11 slugs>; do python check_article.py --full --assets "$s"; done
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life --slug <13 slugs>
# 正式站（部署後）
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-import --actor-email <admin> --locale zh-TW --publish --dry-run --slug … # 11 create + 2 update
```

## Notes

- **發布紀錄（2026-09-19T23:41Z–23:49Z UTC，台北 2026-09-20 早上）**：站主在 AskUserQuestion 明確選「合併並發布」。PR #572 squash 為 `7f2c5478`；
  主機前置檢查：無 hold 檔、無進行中的分段發布、repo 落後 3 個 commit；`/root/deploy-travel-scanner.sh` 23:44Z 起跑、23:47Z health 3/3、alembic `0081_affiliate_click_article (head)`（無 migration）、log `deploy_20260919_234433.log`。
  `guides-import --actor-email <容器 ADMIN_EMAILS 第一位> --locale zh-TW --publish --dry-run --slug ×11`：計畫 11 篇、taxonomy create 11、zh-TW create 11、update 0；
  `--publish`：created 11、updated 0、unchanged 0、published 11、taxonomy_updated 11、`failed: null`。
  驗證（UA `Mokaair-editorial/1.0`、每請求間隔 1.5 秒）：11 頁 `https://mokaair.com/zh-TW/life/<slug>` 皆 200、無 robots meta（可索引）、`/guides/<slug>/hero.jpg` 皆 200、11 個網址都在 `sitemaps/sitemap/life-zh-TW.xml`、`/feed.xml` 已出現；
  `guides-links-check --locale zh-TW` findings 19 筆、無一涉及本批 slug。主機輸出在 `/root/news46-20260920/`（dryrun.json、publish.json、publish-run.log、links-after.json）。
- 發稿日活資料：第二輪查核全部在 2026-09-20 當天重抓（EBA 活動頁兩欄仍空、SEC 兩案無新判決、iPhone Duo 39 場未變、OCC 三份 PDF md5 相符），與發稿同日，未再重抓。
- slug 清單：AI `ai-news-anthropic-accenture-evaluation-20260918`、`ai-news-openai-australia-youth-safety-20260918`、`ai-news-gemini-notebook-study-tools-20260918`、`ai-news-kimi-k3-bedrock-20260918`；
  科技 `tech-news-npm-stage-only-tokens-20260918`、`tech-news-cisa-kev-linux-kernel-20260918`、`tech-news-windows-cloud-rebuild-20260918`、`tech-news-iphone-duo-dev-resources-20260918`；
  幣圈 `crypto-news-occ-three-trust-charters-20260918`、`crypto-news-eba-third-party-risk-20260918`、`crypto-news-sec-crypto-fraud-patterns-20260918`。
- 給下一批的教訓：zh-TW-only 的批次 `check_article.py` 不帶 `--full`；`cmd | tail && git commit` 會吃掉 FAIL，要看 exit code；含中文的 FAIL 訊息要 `PYTHONIOENCODING=utf-8`；表格 caption ≤200 字、description 120–200 字；
  用 `json.dump` 改內容包會把表格陣列展開成多行，改用文字插入；第二輪查核平均每篇再改 13 處（含推翻第一輪與協調者自己新寫的句子），不能省。

- PR #572（2026-09-20）：11 create／0 update；兩輪查核合計改 327 處＋35 條協調者裁決；出圖 11 篇；索引增補另開 `2026-09-19-4-6-11-zh-tw-update`。等站主明確選「合併並發布」。

- **NCC 官網已改成 Angular SPA**，舊 `news.aspx` 網址失效、API 的 folder id 在 bundle 裡找不到；探索代理依 BRIEF「猜網址等同捏造」沒去猜。
  下批探索前要先確認 NCC 新聞稿的可抓取入口，否則科技垂直會系統性漏掉 NCC（已寫進 `tech.md` 的維護待辦）。
- **Accenture 事件日裁決 2026-09-18**：頁面自印 Sep 18；`publishedOn` 16:00Z 是整點排程佔位（台北恰 09-19 00:00），沿用上一輪 OpenAI `00:00` 判例。
- **Gemini Notebook 三合一**：時間線是 9/15 消費端公布、9/18 Workspace 公告開放條件，不能寫成 9/18 才發表。
- **EBA 指引適用日在最終報告仍是 `[date]` 佔位**，任何生效日期都不可寫。
- **SEC Woodcock 演講**探索只讀到 WebFetch 版，研究紀錄代理必須補讀 sec.gov 原文。
- 探索代理用量：AI 195K、科技 180K、幣圈 256K subagent tokens（讀了三份 OCC PDF）。
- **兩則更新在本批取消**（2026-09-19 ~20:10Z）：兩篇目標文章都是五語系、zh-TW 已頂 3000 字、sources 已 4 條；DELTA-4-6 第 8 條在它們身上與 checker 互斥。協調者親跑 checker 確認後還原，另開票處理多語維護。匯入清單因此是 **11 篇 create、0 篇 update**。
