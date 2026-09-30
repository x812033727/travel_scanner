---
id: 2026-09-29-ai-terms-video-pilot
title: AI 名詞影片系列：前三集試片（token、上下文視窗、RAG）
status: review
priority: P2
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-30T00:04:26Z
created_at: 2026-09-29T23:43:22Z
completed_at:
branch: claude/ai-terms-pilot
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
- [x] token：`terms.json` 改 `planned`、企劃（brief.md，配方 A）、撰稿、兩輪查核、加長與聽眾審稿都做完（2026-09-30，lint 零錯誤）。
- [ ] token：`review-push --gate outline`（要站主先存頻道立場）→ `tts` → `check-audio` → `keyframes` → `render` → `assemble` → `captions` → `qa` → `package`（要有工具權杖與 ffmpeg 的機器或主機工人）。
- [x] 上下文視窗：brief（配方 B）、撰稿、兩輪查核、加長與聽眾審稿做完；`source_guide: ai-context-window-explained`，影片代號 `ai-term-context-window`。
- [ ] 上下文視窗：大綱關卡起的產線步驟，同 token。
- [x] RAG：brief（配方 C）、撰稿、兩輪查核（第一輪改 4 處所以有第二輪）、加長與聽眾審稿做完；鄰近名詞連到 token 與上下文視窗（兩集都還沒上架，片尾先指文章）。
- [ ] RAG：大綱關卡起的產線步驟，同 token。
- [x] 字典：只需要加 `RAG`（R A G）；其他英文只在字卡。試聽要確認：RAG（業界也有唸成一個字的）、Hugging Face 連唸、「二〇二五」的「〇」。
- [x] 每集 `shorts.json` 兩支，撰稿時用 `episodeShortsProblems` 驗過；`from-episode --check` 要等關鍵影格畫好才跑得了。
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
- 2026-09-30 認領時用了 `--force`：scope 裡的 `docs/videos/lexicon.json` 與 `2026-09-27-developer-ai-coding-tool-comparison-video`、`2026-09-28-en-video-01-openai-agents-broke` 重疊。字典只會加詞、不改既有的詞，合併時是可以自動合的 JSON 新增行，所以蓋過重疊。
- 2026-09-30 進度（分支 `claude/ai-terms-pilot`，接在 `claude/ai-terms-video-series`（PR #991）後面；#991 合併後要 `git rebase --onto origin/main claude/ai-terms-video-series`）：
  - 三集的示範都真的跑過（腳本與輸出在 session 的暫存區，各集的 `demo-log.md` 逐字抄）：token 用 tiktoken 0.14.0 的 o200k_base 與 cl100k_base 數一份虛構社團公告（完整 142／200 個 token，精簡 86／115；「週六臺北見，帶雨傘」9 個字是 10／16 個 token）；上下文視窗用同一工具數三份虛構會議紀錄（合計 535 個 token；62 字的壞摘要 55 個 token 漏掉「尚未核准」，62 字的好交接 60 個 token 保留）；RAG 用純 Python 的 BM25 對六段虛構規章檢索（退費問題第一名是已失效的 2025 年版、材料費例外排最後；問法一換找到的是報名方式）。
  - 官方來源今天都開過（Google tokens、Google long context、Anthropic context windows、HF tokenizer summary、arXiv RAG 與 Lost in the Middle、Google Cloud RAG Engine、LangChain retrieval、PyPI tiktoken）；OpenAI help 與 GitHub 對編輯 UA 回 403，所以旁白不說哪個編碼新舊。
  - 字典加了 `RAG`。
  - 撰稿：三個代理各寫一集（brief、spec.json → build_video.py → video.json、claims、demo-log、shorts），lint 零錯誤為關卡；接著換人查核（verify-1.md）、聽眾審稿、再 lint。
  - 這個環境沒有 ffmpeg、沒有影片工具的權杖：`review-push`、`tts`、`keyframes` 之後的步驟要在有權杖的機器或主機工人上跑。
- 2026-09-30 校正：lint 估每分鐘 250 字，實際合成約 300 字（`automated.md` §坑），三集初稿估 9.9–10.1 分，成片會只有 8 分多。做法：每集加長到估 11.8–12.3 分（2,650–2,750 單位），`target_minutes` 保持 `[9, 11]`（最終品管量真實時間軸），lint 的「about 12 minutes」警告留著；README 的長度規則已改。`tts` 後把實際長度填回 README。
- 2026-09-30 第一輪查核結果：token 51 條主張改 3；上下文視窗 94 條改 1；RAG 152 條改 4（超過 3，要第二輪）。三集都沒有意見不符，但 brief 的站主觀點都還是「提案，待站主確認」，頻道立場空白，站主存立場前不算定稿。RAG 的文章沒有示範用的六段規章與排名，查核者把它們抄進說明欄本文；站主若把示範補進文章，說明欄可改回指文章。
- 2026-09-30 文字階段完成（分支 `claude/ai-terms-pilot`，接在 main 後面）：三集各有 brief.md、video.json、claims.md、demo-log.md、shorts.json、verify-1.md、verify-2.md；lint 都零錯誤，只剩兩個已知警告（估計 12.3–12.5 分、平均 6.6–6.7 秒換畫面）。撰稿、查核、加長與聽眾審稿、第二輪核對都是不同的代理。三集之間 lint 沒有版型雷同警告。
- **交接（下一個人或主機工人）**：
  1. 站主先在 `/admin/videos` 設定分頁存「頻道立場」（`docs/videos/HANDS-OFF.md` 草稿 7 條，可加 README §YouTube 政策提案的第 8、9 條）。
  2. 立場存了之後，三集 `brief.md` 的「站主觀點」第一行要從「提案，待站主確認（對應…）」改成「套用立場：N、M」（lint 在立場非空時會要求這一行；大綱還沒核准，改 brief 不會讓任何核准失效）。各集 brief 括號裡寫了對應的草稿條號。
  3. 在有影片工具權杖與 ffmpeg 的機器（或主機工人）依序：`status` → `review-push --gate outline`（brief 的選項 A 是採用案）→ `review-pull` → `tts --dry-run`（看實際長度是否落在 9–11 分；估 12.3–12.5 分是刻意的，實唸約每分鐘 300 字）→ `tts` → `check-audio` → `review-push`（旁白）→ `keyframes --dry-run` 看費用 → `keyframes` → `review-push --gate storyboard` → `render` → `assemble` → `captions` → `review-push --gate final` → `package` → `review-push --gate publish`。
  4. 試聽要特別聽：RAG（字典唸 R A G）、Hugging Face（連唸，字典是 null）、「二〇二五」的〇；被標的句子照 `listener-rewrite.md` 改。
  5. `tts` 後把三集實際長度、`keyframes` 的張數與費用、站主花的時間填回 README §成本與產能，並依實際語速修 §站主的決定 的長度一行。
  6. 上架後 `terms.json` 三列改 `published`、填 `video_id`，其他集的片尾「下一個名詞」改指影片。
- 查核者留下、要站主決定的幾件事：token 集 `mu7he`「存取權杖要保密」比文章「可能需要保密」強；RAG 集說明欄現在含六段示範規章與三題排名（因為文章沒有），站主若把示範補進文章可改回指文章；三集 brief 的站主觀點都是提案；「今年一月失效」「去年停辦」等說法只在 2026 年成立。
