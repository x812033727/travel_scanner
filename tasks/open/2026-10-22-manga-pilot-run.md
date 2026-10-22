---
id: 2026-10-22-manga-pilot-run
title: 動態漫畫試片：部署 0137 後在站上發起三分鐘爽文旁白單集、選旁白聲音、勾八語 CC，把花費與邊角裁切結果寫回
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-22T01:40:18Z
completed_at:
branch:
depends_on:
  - 2026-10-22-manga-image-01
scope:
  - docs/videos/manga-pilot-20261022.md
---

# 動態漫畫試片：部署 0137 後在站上發起三分鐘爽文旁白單集、選旁白聲音、勾八語 CC，把花費與邊角裁切結果寫回

## Why

票 `2026-10-22-manga-image-01` 做完了程式（`manga` 畫面等級、單集表單的「畫面做法」、image-01 邊角裁切），站主要的是**一支三分鐘、純靜圖、旁白說書的爽文試片**，還要 CC 與旁白聲音的選擇。這些要在 0137 部署之後才做得到，而且發起、選聲音、勾語言都是站主在後台按的，所以另開一張票接著走。

## Definition of done

- [ ] 正式站 `alembic current` 是 `0137_video_manga_tier`，後台「新的漫劇」看得到「動態漫畫」。
- [x] 旁白聲音：站主 2026-10-22 聽過試聽頁（`~/mokaair-work/videos/_audition/manga-narrator-20261022/index.html`，八個 Gemini 聲音 × 說書／沉穩）選 **Sulafat・說書（快、尾音有力）**。Sulafat 就是漫劇現在的旁白聲音，不用改設定；說書的語氣寫進 manga 等級的撰稿規則（`VISUAL_TIER_RULES.manga` 要撰稿把 `voice.performance` 寫成說書人：節奏快、尾音收得乾脆有力、關鍵字加重、句間不拖），每集的 performance 會併進 Gemini 的 style，所以只有 manga 等級的片會這樣念。
- [ ] 「新的漫劇」發起：原創都市爽文前提（不是參考片的小說）、風格 anime-2d、3 分鐘、畫面做法「動態漫畫」；圖片模型跟漫劇設定（現在是 minimax image-01）。
- [ ] 劇本關卡：劇本沒有任何 `visual: "clip"`、每鏡一兩句、旁白帶故事、lint 沒有「no hook between」的警告（貼圖漫劇每 30 秒一個鉤子，站主 10-22 定的，只套 manga 等級）；`clips --dry-run` 印 0 個要買的鏡頭。
- [ ] 成片核准後，語言面板勾八語的 CC（配音先不勾：有角色台詞的漫劇配音是第二期）。
- [ ] `docs/videos/manga-pilot-20261022.md` 寫下：鏡數、圖片張數與花費、judge 重畫次數、邊角小字裁掉後還有沒有露出、雙人鏡頭怎麼處理的、站主看片的回饋。

## Steps

- [x] 部署：PR #1663 於 2026-10-22 03:2xZ 合併（8faa39929），03:35Z 部署完成，host-verify 11/11 PASS，alembic `0137_video_manga_tier`。
- [x] 發起試片：2026-10-22 03:4xZ 在後台「新的漫劇」送出，作品 **`one-off-252a53bc`**（標題「系統說我是 BUG 第 1 集 凌晨三點的叮」、anime-2d、3 分鐘、畫面做法動態漫畫、圖片模型跟設定＝image-01）；接下來工人寫故事聖經 → 站主討論／核准 → 劇本關卡。
- [ ] 站主選旁白聲音；試聽頁若要補錄（當天 gemini-3.8-flash-tts 一直回「忙碌或達到用量上限」，錄音用的是 lite 模型），用樣張資料夾旁的 `audition.mjs`。
- [ ] 故事聖經與劇本關卡：**站主自己在後台看、自己核准**（站主 2026-10-22 決定）；代理不代核。
- [ ] 成片核准、勾 CC、寫紀錄。

## How to verify

後台作品頁：單集卡片顯示「動態漫畫」；`docs/videos/<slug>/series.json` 有 `visual_tier: "manga"`；`keyframes/manifest.json` 每個鏡頭的 take 帶 `inset: 0.04`；成片裡沒有邊角小字。

## Notes

- **方向改了（站主 10-22）**：不做都市贅婿，改成**異世界＋系統面板＋系統技能**。企劃包 `docs/videos/series-plans/xitong-shuo-wo-shi-bug/`（《系統說我是 BUG》，第一季 30 集已過 validate）。
- **試片的表單值**（「新的漫劇」）：標題《系統說我是 BUG》第 1 集〈凌晨三點的叮〉；風格 anime-2d；3 分鐘；畫面做法「動態漫畫」；圖片模型跟漫劇設定；前提貼 `season-01.json` 第 1 集的 logline、hook、hooks、mid_hook、cliffhanger 與篇章 1 的 beats（設定：九域人人十六歲覺醒面板、一到三格技能槽、廢技可捨棄；江河面板「職業：無、技能：撿垃圾 Lv.1、技能槽 ∞」；角色江河、系統、唐測）；備註：旁白說書帶故事、面板內容由旁白念「叮」、圖裡面板不寫字、角色只講短句、一圖一人、江河疲倦吐槽的程式設計師語氣。
- 樣張與做法：`~/mokaair-work/videos/_audition/image01-anime-20261022/`（20 張，US$0.07），結論寫在前一張票的 Why。
- 雙人鏡頭是 image-01 的弱點（一次只收一張臉）：撰稿規則已經要求一圖一人、第二人縮小或背對；看試片時特別看這點。
