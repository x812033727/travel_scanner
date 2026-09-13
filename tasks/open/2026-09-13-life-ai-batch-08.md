---
id: 2026-09-13-life-ai-batch-08
title: 生活分享 AI 系列批次 08：圖片、影片、音樂生成（20 篇）
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-13T11:56:00Z
completed_at:
branch:
depends_on:
  - 2026-09-13-life-ai-series-tooling
  - 2026-09-13-life-ai-series-catalogue
  - 2026-09-13-life-ai-batch-01
scope:
  - apps/api/app/guides/content/ai-image-tools-overview-2026.json
  - apps/api/app/guides/content/midjourney-getting-started.json
  - apps/api/app/guides/content/midjourney-prompt-guide.json
  - apps/api/app/guides/content/sora-video-guide.json
  - apps/api/app/guides/content/ai-video-tools-compared.json
  - apps/api/app/guides/content/kling-runway-video-tools.json
  - apps/api/app/guides/content/suno-music-generation-guide.json
  - apps/api/app/guides/content/ai-voice-cloning-elevenlabs.json
  - apps/api/app/guides/content/ai-image-copyright-taiwan.json
  - apps/api/app/guides/content/ai-image-watermark-c2pa.json
  - apps/api/app/guides/content/ai-remove-background-upscale.json
  - apps/api/app/guides/content/ai-photo-restoration-old-photos.json
  - apps/api/app/guides/content/canva-ai-features-guide.json
  - apps/api/app/guides/content/ai-slides-generation-tools.json
  - apps/api/app/guides/content/ai-product-photo-for-sellers.json
  - apps/api/app/guides/content/ai-video-subtitles-translation.json
  - apps/api/app/guides/content/ai-avatar-video-tools.json
  - apps/api/app/guides/content/ai-generated-content-disclosure.json
  - apps/api/app/guides/content/ai-art-prompt-styles-reference.json
  - apps/api/app/guides/content/ai-3d-model-generation.json
  - apps/web/public/guides/ai-image-tools-overview-2026
  - apps/web/public/guides/midjourney-getting-started
  - apps/web/public/guides/midjourney-prompt-guide
  - apps/web/public/guides/sora-video-guide
  - apps/web/public/guides/ai-video-tools-compared
  - apps/web/public/guides/kling-runway-video-tools
  - apps/web/public/guides/suno-music-generation-guide
  - apps/web/public/guides/ai-voice-cloning-elevenlabs
  - apps/web/public/guides/ai-image-copyright-taiwan
  - apps/web/public/guides/ai-image-watermark-c2pa
  - apps/web/public/guides/ai-remove-background-upscale
  - apps/web/public/guides/ai-photo-restoration-old-photos
  - apps/web/public/guides/canva-ai-features-guide
  - apps/web/public/guides/ai-slides-generation-tools
  - apps/web/public/guides/ai-product-photo-for-sellers
  - apps/web/public/guides/ai-video-subtitles-translation
  - apps/web/public/guides/ai-avatar-video-tools
  - apps/web/public/guides/ai-generated-content-disclosure
  - apps/web/public/guides/ai-art-prompt-styles-reference
  - apps/web/public/guides/ai-3d-model-generation
---

# 生活分享 AI 系列批次 08：圖片、影片、音樂生成（20 篇）

## Why

`docs/life-ai-series.md` 的批次 08。生活分享專區今天是空的，站主要至少 200 篇 AI 工具的介紹與教學，
分十一批產出；這張票是其中一批，scope 精確到這二十篇的內容包與圖片目錄，和其他批次可以同時進行。

開工前先讀 `docs/life-ai-series.md` 的「經驗記錄」與批次 01 票的 Outcome。

## Definition of done

- [ ] 二十個 `apps/api/app/guides/content/<slug>.json`（zh-TW），每篇：hero（自繪插圖渲染的 `hero.jpg` 或 Commons 照片）、
      至少一張自繪 `diagram-1.svg`、≥3 個 h2、一表、一 callout、sources 每筆有 `checked_on`、至少一個站內 `link`；
      合作連結只在總表標了的篇、只放文章真的用到的段落。
- [ ] 沒有任何產品 logo、字標、圖示或介面截圖；照片只來自 Commons 的 CC0／PD／CC BY／CC BY-SA，授權由 Commons API 讀回。
- [ ] 方案、價格、模型名、額度都在寫作當天查官網；查不到的寫「以官網為準」。
- [ ] `guides-pack lint --kind life` 沒有 error；每張 hero 與圖解渲染成 PNG 後人工看過；`test_guides_content_pack.py` 全綠。

## Steps

這二十篇（slug · 標題 · topics · 圖 · 合作 · 易變）：

1. `ai-image-tools-overview-2026` · AI 圖片工具總覽：ChatGPT、Nano Banana、Midjourney、Flux · ai, software · 圖：插 · 易變
2. `midjourney-getting-started` · Midjourney 入門：網頁版、參數與訂閱 · ai, tutorial · 圖：插 · 易變
3. `midjourney-prompt-guide` · Midjourney 提示詞：風格、比例、參考圖 · ai, tutorial · 圖：插
4. `sora-video-guide` · Sora 影片生成教學 · ai, tutorial · 圖：插 · 易變
5. `ai-video-tools-compared` · AI 影片工具比較：Veo、Sora、海螺、Kling · ai · 圖：插 · 易變
6. `kling-runway-video-tools` · Kling 與 Runway：影片生成工具介紹 · ai · 圖：插 · 易變
7. `suno-music-generation-guide` · Suno 做歌：從歌詞到成品 · ai, tutorial · 圖：插 · 易變
8. `ai-voice-cloning-elevenlabs` · ElevenLabs 與語音克隆：配音與注意事項 · ai, tutorial · 圖：插 · 易變
9. `ai-image-copyright-taiwan` · AI 生成圖片的版權：台灣法規與商用注意 · ai, misc · 圖：插
10. `ai-image-watermark-c2pa` · AI 圖片的浮水印與 C2PA：怎麼標示、怎麼辨識 · ai, misc · 圖：插
11. `ai-remove-background-upscale` · AI 去背與放大：免費工具實測 · ai, tutorial · 圖：照
12. `ai-photo-restoration-old-photos` · 用 AI 修復老照片 · ai, daily · 圖：照
13. `canva-ai-features-guide` · Canva 的 AI 功能怎麼用 · ai, software · 圖：插 · 易變
14. `ai-slides-generation-tools` · AI 做簡報：Gamma、Copilot 與 Gemini · ai, productivity · 圖：插 · 易變
15. `ai-product-photo-for-sellers` · 賣家用 AI 做商品圖：注意事項 · ai, daily · 圖：照
16. `ai-video-subtitles-translation` · AI 上字幕與翻譯影片：CapCut、Whisper · ai, tutorial · 圖：插
17. `ai-avatar-video-tools` · AI 虛擬主播與數位分身：HeyGen 等工具 · ai · 圖：插 · 易變
18. `ai-generated-content-disclosure` · AI 內容標示：YouTube、Meta 與台灣的規定 · ai, misc · 圖：插 · 易變
19. `ai-art-prompt-styles-reference` · AI 繪圖風格提示參考：50 種風格描述 · ai, tutorial · 圖：插
20. `ai-3d-model-generation` · AI 生成 3D 模型入門 · ai · 圖：插 · 易變

- [ ] 認領後從總表抄出指派，一篇一個撰稿代理、每波最多七個，代理照 `docs/life-ai-series-brief.md` 產出工作區。
- [ ] 每篇落地就 `guides-pack ingest`；被拒的退回修。
- [ ] `guides-pack lint --render-dir` 逐張看圖；跑測試；更新這張票；commit。

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life --render-dir /tmp/renders --catalogue ../../docs/life-ai-series.md
cd apps/api && uv run pytest tests/test_guides_content_pack.py tests/test_guide_partner_links.py -q
npm run check:tasks
```

部署後在主機：`python -m app.cli guides-import --actor-email <admin> --dry-run`，再 `--publish`。

## Notes

- 前三批旅遊文章的經驗：兩篇一個代理會在半小時左右撞到額度，一篇一個代理、先寫檔再寫報告最穩。
