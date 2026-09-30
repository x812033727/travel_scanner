---
id: 2026-09-29-ai-terms-video-pilot
title: AI 名詞影片系列：前三集試片（token、上下文視窗、RAG）
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-29T23:43:22Z
completed_at:
branch:
depends_on:
  - 2026-09-29-ai-terms-video-series-plan
scope:
  - docs/videos/ai-terms
  - docs/videos/ai-term-token
  - docs/videos/ai-term-context-window
  - docs/videos/ai-term-retrieval-augmented-generation
  - docs/videos/lexicon.json
---

# AI 名詞影片系列：前三集試片（token、上下文視窗、RAG）

## Why

`docs/videos/ai-terms/README.md` 的規格還是紙上談兵：10 分鐘的骨架合不合 `target_minutes: [9, 11]`、三種場景配方會不會被 lint 判雷同、文章的示例改成影片要多少字、插圖與旁白一集花多少錢，都要做過三集才知道。挑 token、上下文視窗、RAG：三個名詞一個接一個（算單位 → 塞得下多少 → 塞不下時怎麼從外面拿），搜尋量高，來源穩定；其中上下文視窗的文章是保留舊網址的補強篇（`ai-context-window-explained`），順便驗證影片代號與文章 slug 不同的情況。

## Definition of done

- [ ] 三支影片各自的 `docs/videos/ai-term-<名詞>/`（`brief.md`、`video.json`、`claims.md`、`verify-1.md`）通過 `lint`；大綱、旁白、分鏡、成片、上架都核准（自動或站主）。
- [ ] 每支 `tts` 後的實際長度在 9–11 分鐘；`qa` 11 項全過。
- [ ] `terms.json` 的三列改成 `published`（或 `in-production`，Notes 說卡在哪一關），`video_id` 填上。
- [ ] README 的 §成本與產能 填上三集的實際數字（旁白字數、插圖張數與費用、站主花的時間）；§三種場景配方 依 lint 的結果修正。

## Steps

- [ ] 站主先在 `/admin/videos` 設定分頁存「頻道立場」（含或不含 README 提案的第 8、9 條），否則大綱關卡不會自動過。
- [ ] token：`terms.json` 改 `planned` → 企劃（`prompts/planner.md`，IDENTITY 附 README 的骨架與配方 A）→ `review-push --gate outline` → 撰稿、查核、聽眾審稿 → `tts` → `check-audio` → `keyframes` → `render` → `assemble` → `captions` → `qa` → `package`。
- [ ] 上下文視窗：同上，配方 B；`source_guide: ai-context-window-explained`，影片代號 `ai-term-context-window`。
- [ ] RAG：同上，配方 C；鄰近名詞連到 token 與上下文視窗兩集。
- [ ] 三集的英文詞補進 `docs/videos/lexicon.json`（RAG、Context Window、tokenizer…），試聽確認。
- [ ] 每集交 `shorts.json` 兩支（一句話定義、最常見的誤解），`node tools/video/shorts/cli.mjs from-episode --slug <slug> --check` 過。
- [ ] 把數字寫回 README。

## How to verify

```bash
node tools/video/cli.mjs status --slug ai-term-token
node tools/video/cli.mjs lint --slug ai-term-token          # 零錯誤；配方雷同只該出現警告
node tools/video/cli.mjs qa --slug ai-term-token            # 結束碼 0
python3 -c "import json;d=json.load(open('docs/videos/ai-terms/terms.json'));print([(t['id'],t['status'],t['video_id']) for t in d['terms'] if t['id'] in ('token','context-window','retrieval-augmented-generation')])"
```

## Notes

- 影片與音檔在 `VIDEO_WORKDIR`，不進 git；停手前寫下做到哪一關、等站主的是哪一項。
- `brief.md` 的「不做的事」要寫：token 集不用原來如此事務所 A08 的 strawberry 梗；三集都不講價格、模型名稱與排行榜。
