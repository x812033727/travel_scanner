---
id: 2026-09-25-add-article-localization-skill
title: Add the article-localization skill
status: done
priority: P2
area: tools
owner: claude-opus-5-5-article-localization
claimed_at: 2026-09-25T15:10:41Z
created_at: 2026-09-25T15:10:18Z
completed_at: 2026-09-25T15:19:09Z
branch: claude/skill-article-localization
depends_on: []
scope:
  - .agents/skills/article-localization
  - .claude/skills/article-localization
---

# Add the article-localization skill

## Why

補既有文章四語（en、ja、ko、zh-CN）的做法散在 `tools/article-localization/README.md`、`docs/article-localization/*.py` 的 docstring、十幾份 `releases/<batch>/README.md` 與三十多張 localize／release-localized 票裡，而且實際上有兩條路線：Codex 的產線＋bundle（batch007–025）與 Claude 的代理翻譯＋`guides-import`（desk-cable）。每個新 session 都要從長文件重新推導順序與坑。`content-pipeline` 只有一行指向產線 README。

## Definition of done

- [x] `.agents/skills/article-localization/` 有 SKILL.md（兩條路線、規矩、主幹、指令、指向表）、`agents/openai.yaml` 與五份 references（pipeline、bundle-release、agent-route、tickets-and-records、pitfalls）。
- [x] `.claude/skills/article-localization/` 是逐字複本。
- [x] `node --test tools/skills.test.mjs` 全過；description 612 字、沒有「冒號空格」與角括號；沒有機器路徑、個人 email、主機 IP。
- [x] 每個指令、旗標、路徑都對過現在的程式（`pipeline.py`、`assemble_bundle.py`、`install_bundle.py`、`publish_bundle.py`、`report_progress.py`、`app/cli.py`、`verify_public.py`）。

## Steps

- [x] 讀 deploy 與 content-pipeline 兩個 skill、`tools/skills.test.mjs`。
- [x] 讀產線 README、docs/article-localization 各腳本的 argparse 與 docstring、CI workflow。
- [x] 讀 batch009、batch024（翻譯＋發布）、desk-cable（翻譯＋發布）、原文修正與部署內容包比對等票，以及 batch018、batch024、desk-cable 的發布紀錄。
- [x] 寫 skill、複製到 .claude、跑測試。

## How to verify

```bash
node --test tools/skills.test.mjs
diff -r .agents/skills/article-localization .claude/skills/article-localization
```

## Notes

- 與 repo 文件的出入（沒有在這張票改，scope 外）：
  - `apps/api/app/guides/publish_holds.json` 仍擋著兩篇新加坡文章，理由是 batch010 的驗證與審稿未完成；但 `docs/article-localization/releases/2026-09-22/README.md` 記錄 batch010 已在 2026-09-22 五語發布（走 `publish_bundle.py`，它不讀這個檔）。這兩條 hold 可能已過期，之後有人用 `guides-import --publish` 動這兩篇會被擋。
  - `tools/article-localization/README.md` 的 assemble／install 範例把 bundle 輸出到 `docs/article-localization/releases/batch-001`，但實際的 `releases/<batch>/` 只放 README 與 evidence.json，bundle 放在 repo 外。
  - `docs/article-localization/` 底下的 `work/`、`baseline.json`、`production-baseline.json`、`source-differences.json` 是產線預設的輸出位置，卻沒有被 `.gitignore` 忽略。
  - 多份舊的 `releases/*/README.md` 與票寫了本機證據目錄的絕對路徑；skill 明文要求新紀錄不要照抄。
- skill 把 desk-cable 的路線 B 當 Claude 的預設，因為路線 A 要把 `export_snapshot.py`／`publish_bundle.py` 灌進正式站容器，auto 模式分類器會擋。
