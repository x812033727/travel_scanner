---
id: 2026-09-15-ai-suffix-keywords-batch-08-backfill
title: 批次 08 落地後補 14 篇字尾關鍵字（生圖、去背、簡報、影片、配音、作曲、3D、Canva、字幕、版權）
status: review
priority: P2
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-19T11:09:29Z
created_at: 2026-09-15T01:11:35Z
completed_at:
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - apps/api/app/guides/content/ai-slides-generation-tools.json
  - apps/api/app/guides/content/ai-remove-background-upscale.json
  - apps/api/app/guides/content/ai-image-tools-overview-2026.json
  - apps/api/app/guides/content/ai-video-tools-compared.json
  - apps/api/app/guides/content/ai-photo-restoration-old-photos.json
  - apps/api/app/guides/content/ai-product-photo-for-sellers.json
  - apps/api/app/guides/content/ai-art-prompt-styles-reference.json
  - apps/api/app/guides/content/ai-avatar-video-tools.json
  - apps/api/app/guides/content/ai-voice-cloning-elevenlabs.json
  - apps/api/app/guides/content/suno-music-generation-guide.json
  - apps/api/app/guides/content/ai-3d-model-generation.json
  - apps/api/app/guides/content/canva-ai-features-guide.json
  - apps/api/app/guides/content/ai-video-subtitles-translation.json
  - apps/api/app/guides/content/ai-image-copyright-taiwan.json
  - docs/ai-suffix-keywords.md
---

# 批次 08 落地後補 14 篇字尾關鍵字（生圖、去背、簡報、影片、配音、作曲、3D、Canva、字幕、版權）

## Why

`docs/ai-suffix-keywords.md` 把「〇〇 AI」字尾詞對到文章時，這 14 篇還是「待批次 08」；#513 合併後 #516 把批次 08 的
二十篇併進 main，它們的 description 與導言是照原指派寫的，沒有字尾詞。要比照 `tasks/done/2026-09-14-ai-suffix-keywords-backfill.md`
的做法補進去，並把總表這些列的狀態改成「已寫」。

## Definition of done

- [x] 14 篇的 `description` 第一句自然帶出該篇字尾詞、120–200 字；導言第一段加一句含字尾詞；標題不動。
- [x] `docs/ai-suffix-keywords.md` 對應列改為「已寫｜補描述」，經驗記錄加一行。
- [x] `guides-pack lint --kind life` 沒有 error；`pytest tests/test_guides_content_pack.py` 綠；總表「狀態怎麼看」的檢查全部 ok。

## Steps

字尾詞 · slug：

1. 簡報 AI · `ai-slides-generation-tools`
2. 去背 AI · `ai-remove-background-upscale`
3. 生圖 AI · `ai-image-tools-overview-2026`
4. 影片 AI · `ai-video-tools-compared`
5. 老照片 AI · `ai-photo-restoration-old-photos`
6. 商品圖 AI · `ai-product-photo-for-sellers`
7. 動畫 AI · `ai-art-prompt-styles-reference`
8. 虛擬主播 AI · `ai-avatar-video-tools`
9. 翻唱 AI（聲音克隆 AI）· `ai-voice-cloning-elevenlabs`
10. 作曲 AI · `suno-music-generation-guide`
11. 3D AI · `ai-3d-model-generation`
12. Canva AI · `canva-ai-features-guide`
13. 字幕 AI · `ai-video-subtitles-translation`
14. 版權 AI · `ai-image-copyright-taiwan`

- [x] 照上一張補強票的腳本做法：先 dry-run 檢查長度與字尾詞，再套用。
- [x] 改總表狀態；跑檢查；commit。

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life --catalogue ../../docs/life-ai-series.md
cd apps/api && uv run pytest tests/test_guides_content_pack.py -q
npm run check:tasks
```

部署後在主機以 `--slug` 限定這 14 篇 `guides-import --dry-run` 再 `--publish`。

## Notes

- 寫法規則在 `docs/ai-suffix-keywords.md`「寫法規則」；每篇只在 description 與導言各出現一次，h2 不重複。
- 之後批次 09、10、11 落地時同樣要再做一輪（總表裡標「待批次 09／10／11」的列）；可以直接複製這張票。

### 2026-09-19 done in repo (claude-fable-5-1)

- claim 被拒（`2026-09-16-retitled-guides-stale-link-text` 同一擁有者、程式已合併部署但仍在 review，持有
  `ai-video-subtitles-translation.json` 與 `ai-voice-cloning-elevenlabs.json` 的 scope），改以 `--force` claim。
- 14 篇只改 `description` 與導言第一段（第一個 h2 前的第一個 `paragraph`／`rich_paragraph`）；以
  `json.dumps(ensure_ascii=False, indent=2) + "\n"` 重寫，14 個檔案 no-op 往返都 byte-identical，先 dry-run 再套用。
  `ai-remove-background-upscale`、`ai-video-tools-compared` 以 `summary` 區塊開頭，導言第一段是其後那段；六篇導言是
  `rich_paragraph`，句子接在最後一個 text inline 後。標題、圖片、sources、topics、其他區塊都沒動。
- `canva-ai-features-guide` 的 description 原本就在第一句帶「Canva AI」一次、190 字，沒改，只加導言一句；
  「Canva AI」是產品名，正文與一個 h2 本來就有。
- `ai-voice-cloning-elevenlabs` 用總表主要詞「翻唱 AI」（不是變體「聲音克隆 AI」），導言那句照文內既有說法把唱整首歌導向音樂生成。
- `docs/ai-suffix-keywords.md`：14 列改「已寫｜補描述」（備選已補的四列寫「補描述（兩篇／三篇）」，同前一張票）；
  「狀態怎麼看」的 python 檢查原本讀 `blocks[0]["text"]`，既有 30 列的導言現在都是 `rich_paragraph`，跑起來直接 KeyError，
  改成讀第一個 h2 前的第一段；經驗記錄加 2026-09-19 一行。
- 本票沒有自己 commit／push：14 個 pack 檔在寫完後被這條分支的 wip snapshot commit（`96f8382a`）帶進去，
  `docs/ai-suffix-keywords.md` 與本票檔寫這行時仍在工作樹，由同一條分支的 PR 帶。

| slug | 字尾詞 | description 舊 → 新（字） |
| --- | --- | --- |
| `ai-slides-generation-tools` | 簡報 AI | 156 → 159 |
| `ai-remove-background-upscale` | 去背 AI | 188 → 195 |
| `ai-image-tools-overview-2026` | 生圖 AI | 179 → 180 |
| `ai-video-tools-compared` | 影片 AI | 189 → 197 |
| `ai-photo-restoration-old-photos` | 老照片 AI | 198 → 199 |
| `ai-product-photo-for-sellers` | 商品圖 AI | 200 → 198 |
| `ai-art-prompt-styles-reference` | 動畫 AI | 188 → 196 |
| `ai-avatar-video-tools` | 虛擬主播 AI | 143 → 154 |
| `ai-voice-cloning-elevenlabs` | 翻唱 AI | 197 → 199 |
| `suno-music-generation-guide` | 作曲 AI | 196 → 198 |
| `ai-3d-model-generation` | 3D AI | 146 → 150 |
| `canva-ai-features-guide` | Canva AI | 190 → 190（未改） |
| `ai-video-subtitles-translation` | 字幕 AI | 161 → 184 |
| `ai-image-copyright-taiwan` | 版權 AI | 194 → 197 |

檢查：

- `guides-pack lint --kind life --catalogue` exit 0、無 error，912 entries checked；與改前輸出逐行 diff 只差一行：
  `ai-art-prompt-styles-reference` 原本就有的 `text_length` 警告從 6202 變 6234 字（本來就超過 6,000；其他 13 篇加句後最高 5185）。
  `no_summary` 等警告與 sitemap 數字不變。
- `pytest tests/test_guides_content_pack.py -q`：9 passed, 5 skipped。
- 「狀態怎麼看」檢查：39 列全部 ok（含本票 9 個單一 slug 的列；多 slug 的列 regex 本來就不比對）。
- `npm run test:tools`：74 pass；`npm run check:tasks`：Validated 590 task file(s)，只剩既有的 scope 重疊警告（含本票與 retitled 票那兩個檔案）。

部署後在主機（`--slug` 可重複）：

```bash
python -m app.cli guides-import --actor-email <admin> --locale zh-TW \
  --slug ai-slides-generation-tools --slug ai-remove-background-upscale \
  --slug ai-image-tools-overview-2026 --slug ai-video-tools-compared \
  --slug ai-photo-restoration-old-photos --slug ai-product-photo-for-sellers \
  --slug ai-art-prompt-styles-reference --slug ai-avatar-video-tools \
  --slug ai-voice-cloning-elevenlabs --slug suno-music-generation-guide \
  --slug ai-3d-model-generation --slug canva-ai-features-guide \
  --slug ai-video-subtitles-translation --slug ai-image-copyright-taiwan \
  --dry-run
# 看過 dry-run 後，同一串 --slug 把 --dry-run 換成 --publish
```
