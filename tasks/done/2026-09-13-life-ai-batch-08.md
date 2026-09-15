---
id: 2026-09-13-life-ai-batch-08
title: 生活分享 AI 系列批次 08：圖片、影片、音樂生成（20 篇）
status: done
priority: P2
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-14T19:28:39Z
created_at: 2026-09-13T11:56:00Z
completed_at: 2026-09-15T01:08:05Z
branch: claude/travel-guides-tutorials-59j1dv
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

- [x] 二十個 `apps/api/app/guides/content/<slug>.json`（zh-TW），每篇：hero（自繪插圖渲染的 `hero.jpg` 或 Commons 照片）、
      至少一張自繪 `diagram-1.svg`、≥3 個 h2、一表、一 callout、sources 每筆有 `checked_on`、至少一個站內 `link`；
      合作連結只在總表標了的篇、只放文章真的用到的段落。
- [x] 沒有任何產品 logo、字標、圖示或介面截圖；照片只來自 Commons 的 CC0／PD／CC BY／CC BY-SA，授權由 Commons API 讀回。
- [x] 方案、價格、模型名、額度都在寫作當天查官網；查不到的寫「以官網為準」。
- [x] `guides-pack lint --kind life` 沒有 error；每張 hero 與圖解渲染成 PNG 後人工看過；`test_guides_content_pack.py` 全綠。

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

- [x] 認領後從總表抄出指派，一篇一個撰稿代理、每波最多七個，代理照 `docs/life-ai-series-brief.md` 產出工作區。
- [x] 每篇落地就 `guides-pack ingest`；被拒的退回修。
- [x] `guides-pack lint --render-dir` 逐張看圖；跑測試；更新這張票；commit。

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life --render-dir /tmp/renders --catalogue ../../docs/life-ai-series.md
cd apps/api && uv run pytest tests/test_guides_content_pack.py tests/test_guide_partner_links.py -q
npm run check:tasks
```

部署後在主機：`python -m app.cli guides-import --actor-email <admin> --dry-run`，再 `--publish`。

## Notes

- 前三批旅遊文章的經驗：兩篇一個代理會在半小時左右撞到額度，一篇一個代理、先寫檔再寫報告最穩。

## Outcome (2026-09-14)

- 二十篇全部完成並匯入：`apps/api/app/guides/content/<slug>.json` 與 `apps/web/public/guides/<slug>/{hero.jpg,hero.svg,diagram-1.svg}`；hero 全部自繪（總表標「照」的三篇也自繪，不畫產品介面、logo 與真人臉），每張 hero 與圖解都渲染成 PNG 逐張看過；所有 sources `checked_on` 2026-09-14（末段寫手跨過午夜，查證仍在 14 日完成）。
- 檢查：`pack_cli lint --kind life --catalogue ../../docs/life-ai-series.md` 零 error（僅既有的 `pack_not_in_catalogue` 與 sitemap 預算警告，sitemap 由 926 增為 946/1,000 列）；`pytest tests/test_guides_content_pack.py tests/test_guide_partner_links.py`：63 passed、28 skipped；`npm run check:tasks` 通過。
- 來源：每篇 9–20 筆，全部官方或一手（docs.midjourney.com、help.openai.com／openai.com、ai.google.dev／gemini.google／support.google.com／blog.google、kling.ai、runway.com／help.runwayml.com、hailuoai.video、suno.com／help.suno.com、elevenlabs.io、canva.com、help.gamma.app、support.microsoft.com／microsoft.com/zh-tw、heygen.com／help.heygen.com、synthesia.io、d-id.com、remove.bg、photoroom.com、upscayl、topazlabs.com、remini.ai／bendingspoons、helpx.adobe.com、help.shopify.com、help.shopee.tw、law.moj.gov.tw、tipo.gov.tw、law.ftc.gov.tw、moda.gov.tw、c2pa.org／contentcredentials.org／opensource.contentauthenticity.org、transparency.meta.com／facebook.com/help、tiktok.com、capcut.com、github 與 huggingface.co 的 README／LICENSE、meshy.ai、docs.tripo3d.ai、hyper3d.ai、docs.blender.org、Epson 支援文件、iTunes lookup）；審稿時逐篇用 curl、Zendesk／Intercom 內容 API、Wayback 快照、WebFetch 與 iTunes lookup 複核關鍵數字，十三篇退回一輪修正、一篇兩輪（審稿記錄在工作區 review-log.md）。
- 沒有合作連結（總表的 H 標記只是允許，repo 內無聯盟網址）。
- 與總表指派不同、照當天官網寫的事實：Sora 網站與 App 已於 2026-04-26 停止、Videos API 2026-09-24 關閉且官方不推薦替代，該篇改寫成匯出與換工具指引並改標題，比較篇只留規格當對照；Midjourney 預設 V8.2（V8.1 2026-04-14 推出）、沒有免費試用（只有 niji App）、`--cref`／Omni Reference 由 Edit Model 取代、多重提示只到 V6、`--q` 在 V8.x 不支援；Suno 現役 v6／v6-wild／v6-mini、商用權綁下載額度（Free 終身 7 次、Pro 20／Premier 60 每月）、條款 2026-09-03 生效；Kling 網域改 kling.ai、主力 VIDEO 3.0 與 Omni、原生 4K 每秒 30 點、服務條款 4.6 與付費條款對商用的寫法相反；Runway 網域改 runway.com、Gen-4.5、Aleph 2.0／Act-Two、Unlimited 2026-11-30 轉 Max；海螺當天模型 MiniMax H3；Veo 3.1 的額度是 Flow 點數（每天 50、Pro 每月 1,000、Quality 8 秒 100 點）；Google 訂閱以台灣頁新台幣寫（Plus NT$165、Pro NT$650、Ultra NT$3,300／6,500）；ChatGPT Pro $200 自 2026-09-10 暫停新申購、Images 2.5 2026-09-08 發布；Nano Banana 各模型參考圖上限不同（Flash Image 10 物件＋4 角色，3 張風格參考只有 Pro）；Canva 的 Magic Studio 改名 Canva AI、Teams 改 Business（$20／人／月）、AI Pass $100、額度為「營運控制而非固定權利」；remove.bg 已是 Canva 品牌並將於 2026-12-01 移往 Leonardo.Ai；Upscayl 桌面版 AGPL-3.0 另有 Cloud 與 Mac App Store 版（NT$390）；Photoshop 神經濾鏡頁面已 301 改址且無「產品改善計畫」句；Google 相簿 AI Enhance 只在美國；Remini 沒有黑白上色；CodeFormer 為 S-Lab 非商業授權；Gamma 的 Create with Agent 不含 Free 與 Business；PowerPoint Copilot 加投影片需 Designer 授權；Google Slides 整份簡報生成掛在 Workspace Experiments；NotebookLM 改稱 Gemini Notebook 且 Slide Deck 只能 PDF；蝦皮的 AI 揭露責任寫在 Shopee AI 服務條款 3.1.6 與 3.3；PChome 商店街 2024-11-01 起轉型；人工智慧基本法民國 115-01-14 公布（20 條、中央主管機關為國科會、透明原則寫給政府）、智財局生成式 AI 著作權指引仍是初稿（115-07-20 公聽會）、選罷法 115-07-01 修正第 51 條之 3；Meta 不要求標示 AI 圖片、SIEP 廣告 2026-06-01 起自動偵測、TikTok 公約 2026-09-24 換版但規則未變；HeyGen 現稱 Digital Twin、新增 Avatar V（15 秒、每分鐘 48 點）；ElevenLabs 額度單位是 credit、專業克隆只能做自己的聲音；CapCut 沒有公開定價頁；YouTube 的翻譯在觀眾端、Whisper `--task translate` 只到英文（turbo 不支援）；Meshy 現役 7／6／6 Lite 且免費層每月只有 10 次 Lite 下載；Luma 已無 3D 產品；Hunyuan3D 2.1 社群授權排除歐盟、英國、南韓。
- 官方文件內部不一致時擇一並註明：HeyGen 定價頁與 FAQ 的自訂分身名額（1+／5 vs 預設 5）；Remini 網頁版隱私政策 15 天 vs 1 天（改引 Bending Spoons 版）；FLUX.2 klein 顯示記憶體（bfl.ai 8.4／19.6 GB vs HF 13 GB）；Kling 與海螺的服務條款 vs 訂閱條款；Gemini API 文件比例表與各模型欄位。
- 取得資料的做法：docs.midjourney.com 403 → 同網域 Zendesk API `/api/v2/help_center/en-us/articles/<id>.json`；help.openai.com → 網址加 `.json` 加瀏覽器 UA；openai.com → Wayback `id_` 快照（gzip，要 `--compressed`；Wayback 當天數度離線）；helpx.adobe.com 403 → 帶完整瀏覽器標頭（Accept／Accept-Language／Upgrade-Insecure-Requests／Sec-Fetch-*）可讀；canva.com Cloudflare 403 → Wayback 快照；transparency.meta.com 與 facebook.com/help 對 curl 回 400 → WebFetch；help.shopee.tw → `/api/inhouse/hc/mobile/v1/article?id=<id>`；help.runwayml.com 同樣走 Zendesk API；gemini.google 台灣定價頁用 `?hl=zh-TW`；ai.google.dev 部分頁要 cookie jar 跟隨導向；app.klingai.com 方案頁與 www.tripo3d.ai 讀不到（前端渲染／403），只寫 API 文件的點數表；Kling 定價頁數字在內嵌 JSON；App Store 用 iTunes lookup `country=tw`。
- 標題與總表：十三篇在撰稿後調整了標題（Sora、Suno、圖片工具總覽、影片比較、Kling／Runway 未變、ElevenLabs、版權、去背、老照片、Canva、商品圖、字幕、虛擬主播、3D），`docs/life-ai-series.md` 批次 08 列已同步。
- 代理統計：二十個 Opus 撰稿代理，每篇 4–35 分鐘、16–31 萬 token；第一波七個代理在 20:00Z 左右撞到帳號的五小時額度，21:10Z 重置後用 SendMessage 續跑同一個代理（上下文保留），五個接著寫、兩個重來。
- 合併後：部署，然後在主機跑 `python -m app.cli guides-import --actor-email <admin> --dry-run`（應為二十篇 `create`），再 `--publish`。
