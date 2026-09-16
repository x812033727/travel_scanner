---
id: 2026-09-16-news-batch-4-2-non-ai
title: News batch 4.2: non-AI technology news
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-09-16T13:21:40Z
completed_at:
branch:
depends_on:
  - 2026-09-16-news-batch-4-0-crypto-and
scope:
  - docs/tech-news-2026
---

# News batch 4.2: non-AI technology news

## Why

既有 38 篇 `ai-news-*` 幾乎全是 AI 模型發布，硬體／晶片／消費電子／電信／法規
只有 `ai-news-nvidia-rubin-20260105` 與 `ai-news-siri-ai-ios-27-20260914` 兩篇沾到邊。
`tech` 父主題與 `tech-news` 子主題由 PR #536 帶進來。

## 界線

見 [`docs/news-2026-batch-4/tech.md`](../../docs/news-2026-batch-4/tech.md)：
**不寫購買建議**（不寫「該不該買」「值不值得升級」），
廠商的效能宣稱一律歸因（「Apple 表示」），本站沒有實測；
資安題目寫影響範圍與該做什麼，**不寫攻擊手法與入侵指標**。

**不帶 `finance` 主題，所以不要自己加投資免責。**

## 候選題目

[`docs/news-2026-batch-4/candidates-tech-and-ai.md`](../../docs/news-2026-batch-4/candidates-tech-and-ai.md)
有 **11 則已驗**：Apple iPhone Duo 與 9/9 發表會硬體、歐盟 CRA 通報義務、
台灣數發部四則（主權 AI 語料庫那條線最適合本站讀者）、
Apple 歐盟 App 商業條款、Windows Project Zenith、September Pixel Drop。

**一個待站主決定的分類問題**：Apple M6／M5 Ultra（8/25）目前放在「次要新聞」，
但 **M6 是 Apple 第一顆 2 奈米製程晶片**、站上完全沒寫過，我建議升級成重要新聞。

**與既有文章的分工**：`ai-news-siri-ai-ios-27-20260914` 已經寫過 iOS 27 與 Siri AI，
9/9 那篇**只寫硬體**，軟體連回去那篇。

## 這張票還不能認領

`tasks/open/2026-09-15-content-summary-howto-and-life`（`in-progress`，
scope 是**整個 `apps/api/app/guides/content` 目錄**）擋住所有內容包任務。
它的認領在 **2026-09-17T03:39Z** 變 stale，屆時才能 claim。
**不要用 `--force` 繞過**——那條規則正是用來擋兩個 agent 互相覆蓋的。

## scope 還沒填完

目前只有工作區目錄。**站主圈完題目之後**，要把每篇的兩行路徑補進 `scope`：

```
apps/api/app/guides/content/<slug>.json
apps/web/public/guides/<slug>
```

比照 `tasks/done/2026-09-15-ai-news-batch-3-seven-mid.md`。
**絕對不要用整個 `content/` 目錄當 scope**，否則就變成現在擋住這張票的那個問題。

## 流程

照 [`docs/news-2026-batch-4/BRIEF.md`](../../docs/news-2026-batch-4/BRIEF.md)：
一篇一個撰稿代理 → **獨立查核代理**（不可省：批次 3 每篇 56–102 條主張、
每篇都改了 15–38 處）→ 翻譯（五語）→ 逐語系審稿 → 圖像 → 索引 → 驗證。

每篇必帶 `summary` 與 `faq` 區塊——這批是站上第一批全面帶的
（845 篇 life 只有 5 篇有 summary、1 篇有 faq）。

## 已知會擋路的兩件事

- **這個容器沒有 headless 瀏覽器**，而 `build_assets.py` 要靠它把 hero SVG 轉成 JPEG。
  圖像階段開始前先確認 Chromium 可用（環境有 `/opt/pw-browsers/chromium`，
  但 `build_assets.py` 目前找的是 Edge／Chromium 的路徑，要確認能不能指過去）。
- **`pack_cli ingest` 會拒絕帶子主題的內容包**（`_known_topics()` 只回父主題）。
  批次 3 是直接寫進 `content/` 不走 `ingest`，這批照做。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --kind life    # 0 error
uv run pytest tests/test_guides_content_pack.py tests/test_guides_content_links.py
npm run check:tasks
```
