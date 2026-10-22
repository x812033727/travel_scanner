---
id: 2026-10-22-independently-source-review-c10-oxo-script
title: Independently source-review C10 OXO script and visual plan
status: done
priority: P1
area: docs
owner: codex-c10-oxo-source-review
claimed_at: 2026-10-22T14:31:05Z
created_at: 2026-10-22T14:30:42Z
completed_at: 2026-10-22T14:35:51Z
branch: codex/brand-story-oxo-c10-script
depends_on: []
scope:
  - docs/videos/story-everyday-oxo-c10/reviews/independent-script-source-review.md
---

# Independently source-review C10 OXO script and visual plan

## Why

C10 OXO 的繁中單旁白及逐鏡已成草稿，需要與作者分離的來源審查，逐句區分品牌回顧、採訪者回憶、館方物件與設計評價，防止圖片暗示無紀錄的歷史場面。

## Definition of done

- [x] 直接讀原發行者頁與原設計參與者資料，不沿用作者企劃查核的 PASS。
- [x] 對固定 SHA 的 80 句與同 ID 的 80 畫面各自給 PASS／HOLD，寫明支持來源、推論與具體停線。
- [x] 核對年代、初批件數、零售／銷售敘述、品牌自述，以及沒有 TTS 時不能宣稱的時長。
- [x] 將獨立收據交到既有 draft PR #1689；不修改作者稿件或送付費製作。

## Steps

- [x] 讀本庫 AGENTS、brand-story、youtube-video/story、curio-episode、task-board 規則。
- [x] 直接讀 OXO、Cooper Hewitt、MoMA、Design Council、Los Angeles Times、Smart Design；另讀 Cooper Hewitt 圖錄與初期設計成員自述，專查原型研究。
- [x] 寫 `reviews/independent-script-source-review.md`，80 個 ID 一對一；旁白 79 PASS／1 HOLD，畫面 71 PASS／9 HOLD。
- [x] 機械核對 ID、種類、連卡及原稿 SHA；`npm run check:tasks` 和 `git diff --check`。

## How to verify

Receipt 的 80 個表格 ID 與 `script.md`、`visual-plan.json` 的 80 個 ID 順序完全一致且無重複；JSON 是 71 個 `shot`、9 個 `stats`，最多連續 2 張 `stats`。原稿兩個 SHA-256 仍為 `1A05017A9C6DF2A60365655975E00AC954AF799D2264C9E006F89B21449C2CB3`、`4241FC748B5FA81927EC81B3FAAF4BEC8AC332AA5893F7B2DC3C6CD240AE1CF9`。檢查結果與提交紀錄可在 PR #1689 查看。

## Notes

HOLD：c100308 把多類使用者研究與泡棉模型測試合成「不同手反覆試握模型」的場面，直接來源沒有把兩者連起來；八個圖片 `prompt` 含企劃姓名、公司或館名，即使否定句仍不合本系列提示詞規則。修正交還 `2026-10-22-write-c10-oxo-script-and-visual` 的作者範圍，本票不改 script／visual。1989 設計與 1990 上市分清，初批 15／20 件衝突不入稿。尚未有 C10 TTS、真實圖片、依秒數 70% 插圖或站主核准，不作已成片聲明。
