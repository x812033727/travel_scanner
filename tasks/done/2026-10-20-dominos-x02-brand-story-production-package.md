---
id: 2026-10-20-dominos-x02-brand-story-production-package
title: Dominos X02 brand-story production package
status: done
priority: P1
area: docs
owner: codex-gpt6-dominos-x02
claimed_at: 2026-10-20T10:24:23Z
created_at: 2026-10-20T10:24:20Z
completed_at: 2026-10-20T10:59:31Z
branch: codex/brand-story-dominos-x02
depends_on: []
scope:
  - docs/videos/story-everyday-dominos-pizza-x02
---

# Dominos X02 brand-story production package

## Why

站主要求品牌故事依奇聞檔案局的既定影片規則持續製作，Adobe X01 開 PR 後接續下一個品牌。X02 以達美樂 2009 年底重做美國市場核心披薩配方為主線；四份 SEC 原始申報可查美國同店銷售、廣告及多重歸因。此票先完成可審閱、可乾跑的獨立稿件包，不在 Adobe PR 開出前花費媒體成本或另開 PR。

## Definition of done

- [x] 六章約 9 分鐘的繁中逐句稿、MiniMax 可愛插圖提示詞、數字卡、可回收伏筆、YouTube 標題／說明／縮圖設定及 5 秒片頭／21 秒片尾製作交接齊備。
- [x] 所有數字與因果說法可追到四份 SEC 原件，明分美國同店銷售、季度／全年、公司自己的歸因及獨立可證事實；另一代理獨立來源查核。
- [x] `lint` 零錯誤與零警告、TTS 與圖片乾跑可執行，並列出 US$25 單集硬上限；未執行付費媒體、正式上架或本集 PR。

## Steps

- [x] 由 `origin/main` 建獨立 worktree／分支；建立企劃簡報及在旁白開始前固定故事發音字典。
- [x] 完成 SEC source notes、六章 treatment 與兩段逐句稿。
- [x] 合成 `video.json`、逐句來源矩陣及上架文案，兩位敘事盲讀與另一代理事實查核。
- [x] 零錯誤 lint、TTS／圖片乾跑、製作報價；交回主代理後續付費製作與 PR。

## How to verify

從 `/workspace/travel_scanner_dominos` 執行 `node docs/videos/story-everyday-dominos-pizza-x02/compose-video.mjs`、`node tools/video/cli.mjs lint --slug story-everyday-dominos-pizza-x02 --json`、`node --use-env-proxy tools/video/cli.mjs tts --slug story-everyday-dominos-pizza-x02 --workdir /workspace/.brand-video-workdir --dry-run`、`node --use-env-proxy tools/video/cli.mjs keyframes --slug story-everyday-dominos-pizza-x02 --workdir /workspace/.brand-video-workdir --dry-run --takes 3`，再跑 `npm run check:tasks`。正式生成前需復核獨立來源與敘事收據所綁的最終 `video.json` SHA。

## Notes

2026-10-20：獨立 worktree `/workspace/travel_scanner_dominos`，分支 `codex/brand-story-dominos-x02` 由 `origin/main` 的 `33e2bdd1` 建立，不碰 Adobe 變更。研究原件的本機抽取檔在 `/tmp/next-brand-dominos-{fy2009,q12010,fy2010,fy2011}.html.txt`。2008 美國國內同店 -4.9%、2009 +0.5%、2010 Q1 +14.3%、2010 全年 +9.9%、2011 全年 +3.5%；Q4 2009 重做核心披薩配方。產品、行銷、營運及加盟都有關，不能講成單一廣告造成。故事 lexicon 已在 `video.json` 前初始化，SHA `3a93cee17d9287682a449a727aa9a82d868a9273ebdf3f776428bf70227e6d20`。此票不覆蓋原 C03 Moleskine 編輯順位。

前製定稿 `video.json` SHA `b7801fb9fbe27d6342726b03398fb6ef53b1012e4eb67e98cf8c34cb4f61173c`：73 景（63 插畫、10 資料卡），11 組伏筆，正文估 9:02、開場 0:52。兩位獨立敘事盲讀各 12/12 必選題及建議題 PASS，收據在 `reviews/narrative.md`；獨立 SEC 逐句查核 73/73 與 10 卡 PASS，收據在 `reviews/verify-1.md`。TTS 乾跑 73 請求／2,184 計費字元；MiniMax 63 張估首輪 US$0.85、三輪上限 US$2.55；本集媒體支出 US$0.00。後續另在 X01 Adobe PR 開出後，按 US$25 硬上限生成語音／插畫／卡／配樂、合成明標概念試片、審片並開本集 PR。
