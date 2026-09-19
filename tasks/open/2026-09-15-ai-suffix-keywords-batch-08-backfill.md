---
id: 2026-09-15-ai-suffix-keywords-batch-08-backfill
title: 批次 08 落地後補 14 篇字尾關鍵字（生圖、去背、簡報、影片、配音、作曲、3D、Canva、字幕、版權）
status: in-progress
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

- [ ] 14 篇的 `description` 第一句自然帶出該篇字尾詞、120–200 字；導言第一段加一句含字尾詞；標題不動。
- [ ] `docs/ai-suffix-keywords.md` 對應列改為「已寫｜補描述」，經驗記錄加一行。
- [ ] `guides-pack lint --kind life` 沒有 error；`pytest tests/test_guides_content_pack.py` 綠；總表「狀態怎麼看」的檢查全部 ok。

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

- [ ] 照上一張補強票的腳本做法：先 dry-run 檢查長度與字尾詞，再套用。
- [ ] 改總表狀態；跑檢查；commit。

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
