---
id: 2026-09-16-content-packs-counts-in-hub-titles
title: "Content packs: counts in hub titles and lesson ordinals in body text"
status: blocked
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-16T06:14:00Z
completed_at:
branch:
depends_on:
  - 2026-09-16-stop-showing-article-counts-and-lesson
scope:
  - apps/api/app/guides/content/ai-terms-index.json
  - apps/api/app/guides/content/ai-search-terms-index.json
  - apps/api/app/guides/content/gemini-guide.json
  - apps/api/app/guides/content/claude-code-tutorials.json
  - apps/api/app/guides/content/codex-learning-hub.json
---

# Content packs: counts in hub titles and lesson ordinals in body text

## Why

站主要求全站不再顯示會成長的數字，理由是「篇數會一直增加」。
`2026-09-16-stop-showing-article-counts-and-lesson` 處理程式與版面那一半，
但有一類數字是寫死在文章內容裡的，程式改不掉。

**已上線，改完要重新匯入：**

| 內容包 | 寫死的數字 |
| --- | --- |
| `ai-terms-index.json` | 標題「AI 名詞總索引：**81 個概念**，從 Loop Engineering 到生成式 AI」；描述「把 81 個概念分成八組」 |
| `ai-search-terms-index.json` | 標題「GEO、AEO、AIO 與 SEO 名詞總索引：**10 篇**看懂差在哪」；描述「連到**十篇**專文」 |
| `gemini-guide.json` | 描述「這裡整理 Gemini、Google AI 與開發工具的**五十篇**教學」 |

站主在規劃時明確選了「標題與描述都改掉」。

**尚未發布，只要改檔案：**

| 內容包 | 寫死的數字 |
| --- | --- |
| `claude-code-tutorials.json` | 描述「從 **96 篇**文章…分成 **96 個**可以獨立閱讀的小題目」 |
| `codex-learning-hub.json` | 描述「規劃 **60 篇** Codex 教學、十個單元」，**五個語系都有** |
| `claude-code-build-todo-app.json` | 描述「不必先完成**前五十四篇**」 |

**73 個內容包的正文有「第 N 篇」**（37 個 `claude-code-*`、29 個 `gemini-*`、5 個 `notebooklm-*`、
2 個 `google-flow-*`）。多數是下載連結標籤（「第 61 篇練習材料」「下載第 69 篇完整練習包」）；
另有三處是散文引用（`gemini-api-document-service-capstone.json:169,267`、
`claude-code-practice-project-setup.json:90`、`notebooklm-multiformat-lesson-pack.json:96`）。

## Definition of done

- [ ] 三篇已上線的中心文章標題與描述不再有數字，並已重新匯入正式站。
- [ ] 尚未發布的三個中心文章描述不再有數字（`codex-learning-hub` 五語系都改）。
- [ ] 73 個內容包的正文不再有「第 N 篇」。
- [ ] `docs/` 的上游檔案（如果還在產生內容）也一起改，否則下次重建會長回來。

## Steps

- [ ] 標題改寫時保留原本搶的查詢詞（`AI 名詞`、`GEO AEO AIO SEO 差別`），只把數字換成不會過期的說法；
      slug 不動，不需要轉址。
- [ ] 下載連結標籤改成「本篇練習材料」「下載完整練習包」。
      `gemini-cli-memory-scope-lab.json:337,341` 同一篇有兩個下載連結，要用內容區分而不是編號。
- [ ] 三處散文引用改寫成用標題連過去，不要用編號稱呼另一篇。
- [ ] 確認 `docs/claude-code-series/lessons/61.md`…`96.md`（37 個）與 `docs/` 底下其餘帶同樣文字的檔案
      是不是還在用的產生器；是的話同一輪改掉。

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life
grep -rn "第 [0-9]\+ 篇" apps/api/app/guides/content/ | wc -l    # 應為 0
```

部署後：

```bash
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli guides-import \
  --actor-email <admin> --publish \
  --slug ai-terms-index --slug ai-search-terms-index --slug gemini-guide
```

匯入走 admin write path，搜尋索引與連結圖會自動跟上，不必再跑 reindex。
`curl 'https://mokaair.com/api/v1/guides/search?locale=zh-TW&q=AI%20名詞'` 確認新標題進了索引。

## Notes

**blocked 的原因**：`apps/api/app/guides/content` 整個目錄被
`2026-09-15-content-summary-howto-and-life`（claude-fable-5-1，2026-09-16 claim）佔著。
那張票的摘要批次做完釋出 scope 之後，這張才能動。

**已查證：那 73 個包全部都還沒發布**（`gemini-cli-memory-scope-lab` 在正式站是
「這篇文章目前看不到」），所以正文那一段不影響線上任何一頁，也不需要重新匯入 ——
但一定要在那幾批內容上線前做完，否則讀者第一眼看到的就是會過期的編號。
只有上面三篇中心文章需要重新匯入。

**判斷後刻意保留**：`finance-glossary-50-terms`（slug 自己就寫 50、文章範圍固定五十個詞，不會成長）、
`ai-for-seniors-first-steps` 的「第一堂 AI 課」、`wordpress-blog-build` 的「第一篇文章」——
都是散文，不是目錄大小。
