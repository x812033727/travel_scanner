---
id: 2026-10-22-c07-dr-martens-script-visual
title: Write and independently review C07 Dr. Martens script and visual plan
status: in-progress
priority: P2
area: docs
owner: codex-c07-reviser
claimed_at: 2026-10-22T12:03:53Z
created_at: 2026-10-22T05:29:06Z
completed_at:
branch: codex/brand-story-dr-martens-c07-script
depends_on: []
scope:
  - docs/videos/story-everyday-dr-martens-c07/script.md
  - docs/videos/story-everyday-dr-martens-c07/visual-plan.md
  - docs/videos/story-everyday-dr-martens-c07/script-source-notes.md
  - docs/videos/story-everyday-dr-martens-c07/reviews/script-source-review.md
  - docs/videos/story-everyday-dr-martens-c07/reviews/narrative-reader-1.md
  - docs/videos/story-everyday-dr-martens-c07/reviews/narrative-reader-2.md
  - docs/videos/story-everyday-dr-martens-c07/reviews/script-review-summary.md
---

# Write and independently review C07 Dr. Martens script and visual plan

## Why

站主已採用 C07 六章企劃（Treatment 原檔雜湊見 owner-treatment-approval.md）。須在同一證據界線內寫出可朗讀的連續故事與奇聞檔案局風格逐鏡稿，先補可直接讀取的獨立博物館文化來源，再進逐句查核與兩位盲讀。

## Definition of done

- [ ] 六章逐句稿、每句依據與一對一逐鏡方案完成；青年文化轉向有可直接讀的獨立館藏或研究來源。
- [ ] 另一代理逐句核查，兩位真正盲讀；各審查收據與本版 SHA-256 綁定。
- [ ] 相關檢查通過，草稿 PR 貼 `no-auto-merge`；未付費生成、上傳或發布，劇本仍待站主另審。

## Steps

- [x] 從已核准 Treatment `68c8c8766` 開獨立工作樹與窄票。
- [x] 補直接可讀倫敦博物館館藏與獨立研究來源，寫 77 句逐句稿與 77 鏡方案。
- [ ] 交獨立來源審查和兩位盲讀，修改並重綁收據。
- [ ] 執行文件／看板檢查並開草稿 PR。

## How to verify

`npm run check:tasks`、`git diff --check`；來源逐句可讀性及檔案 SHA-256；稿件句數與分鏡行數一致、插圖占比至少七成、連續文字卡最多三張。正式正文 ≥480 秒仍須以核准後 TTS 實測，字數估時不充數。

## Notes

2026-10-22：倫敦博物館 1995 年館藏物件頁可直接讀，明確寫 Dr. Martens 於 1960 年代末被 skinheads 採用、後有其他次文化；Arthur Crucq 的 2021 年獨立研究可直接讀，分開晚 1960s、晚 1970s punk 與後來極右挪用。V&A 品牌專頁直取仍 403，不作逐句唯一依據。出廠日與未知零售日嚴格分開。舊 Treatment 任務 `done` 曾寫出 done 副本但 open 檔刪除受政策拒絕，詳見舊工作樹，**勿以改寫命令繞過**。

2026-10-22：初稿凍結雜湊見 `reviews/script-review-summary.md`。77 句與 77 鏡 ID 一對一、63 插圖／14 卡、最長兩連卡；仍待另一代理逐句查核、兩位真正盲讀、時長與時間占比實測，不能宣稱 PASS。`npm run check:tasks` 與 `git diff --cached --check` 通過（前者有全庫舊票警告）。首輪 `npm run test:docs-videos` 因新工作樹缺 `pinyin-pro` 中止；`npm ci` 完成後重跑 **235/236 PASS**，唯一失敗是 `docs/videos/imported-long-languages/runner.test.mjs` 的 `initial runtime freezing resolves a portable relative root...`，子程序在 Windows 回 `3221226505`、stderr 空，未觸及 C07 文件。草稿 PR #1680 已貼 `no-auto-merge`，等待獨立審查；不得把 235/236 說成全綠。

2026-10-22：另一代理已先做只看旁白的盲讀，再直接核對來源與逐鏡，完整 77 句 SHA-bound 獨立紀錄見 [script-source-review.md](../../docs/videos/story-everyday-dr-martens-c07/reviews/script-source-review.md)。判定 HOLD：c070304、c070310、c070407、c070412、c070601 的主張範圍／歸因要修；c070603–c070604 的 V&A 照片段事實界線正確但盲聽脫離靴子；c070405 聽感待改；分鏡 c070101／505／608 多焦點、c070310／507 空白紀錄示意及 c070301 密集卡需重排。舊版 script SHA DB10ADC588C1FC8E52EE126084D4FC60833A5ACEC60C644AC97D38D98316A3C6；visual SHA 563327B512A7EC674EE53DFDF1F44D4EDB5E514518537E2715584CF9865111FF。

2026-10-22：按初審窄幅修訂 77 句，明分 1460 產品史與廣義品牌靴的青年文化史；V&A 1981 照片退回背景查核，不再口播或出卡。分鏡改為 64 插圖／13 單項卡，圖像不造首賣收據、不拼多個焦點。新版 script SHA A1BE5CFC53CE24EDEFA95094E4D442F6E86FE6B0B4F8D0E0D7E5BE7CEE510A14；visual SHA 32B854AE849421F14B39B81CC612745B522E9EBFDFEC1FF62AA09EEAE43984CA。`npm run check:tasks`、`git diff --check` 通過；仍需另一代理重查全部 77 句、兩位只看旁白的新盲讀與站主劇本審核。未作 TTS 480 秒、付費媒體、上架或合併。

2026-10-22：獨立 v2 收據 `reviews/script-source-review-v2.md` 對前稿 77 句判 74 PASS、3 HOLD（c070105 的設計目的、c070310 的檔案性質／首賣日範圍、c070609 的公司現行定位來源）。本輪只修三句與必要的 B5 來源標註；B5 在 `script-source-notes.md` 登錄，不更動已核准 Treatment 的來源矩陣。現稿 script SHA 5264D383C8E1CA8787DAD68F24989B774E53233813D4F6DEE00764B31B6E6F60，visual SHA 仍 32B854AE849421F14B39B81CC612745B522E9EBFDFEC1FF62AA09EEAE43984CA。等同一位獨立查核者在新 SHA 上重看差異，再做兩位新盲讀；目前仍 HOLD。另有他人建立的未追蹤重複票 `tasks/open/2026-10-22-c07-revised-script-source-review.md`，本輪未觸碰或刪除。

2026-10-22：獨立 v3 收據 `reviews/script-source-review-v3.md` 對上述稿件判來源 77/77 PASS；之後一位只讀旁白的讀者指出 c070413–414 先問「誰先」，再答六〇年代末，會暗示無法證明的第一位或第一群。本輪只改這兩句為六〇年代末**已見**的採用例子與下章提問；77 句／77 鏡、64 插圖／13 卡不變，visual SHA 仍 32B854AE849421F14B39B81CC612745B522E9EBFDFEC1FF62AA09EEAE43984CA，script SHA 76D12402756C390CD6F3018E29CB90D2DAD6B95D9897690AC7F675DF7D1D1385。須對此新 SHA 再做獨立來源差異覆核與兩位新盲讀；站主劇本核准與任何付費製作仍未取得。既有未追蹤重複票未觸碰。

2026-10-22：獨立 v4 收據 `reviews/script-source-review-v4.md` 對前稿判來源與逐鏡文字 77/77 PASS；其後嚴格純旁白盲讀仍 HOLD：工作服到街頭的過橋重複，c070509 問下一群人的不同「內容」卻只列風格，c070516 提對立立場而下章未明說另一方。作者直接讀 [Crucq 2021 研究](https://www.pismowidok.org/en/archive/2021/31-visuality-of-social-classes/double-class-on-the-popularization-of-dr.-martens) 中服飾拼搭、加勒比音樂與部分 skinhead 後來反種族主義的段落後，修 c070408–411、509、516、602–603，並同步單焦點視覺 c070408–411；不新增未證的群體信念。現稿 script SHA 1045463BC76C8285A0EE40B0F00BA9E64A44434C71E50597B35DC783BA498654，visual SHA 1487B891ED7A3FB680A96915E06E7B2C076280F3AD8903A2546B5F53B12FCB2A，source notes SHA 8FE0C6BC4D16D43289C77742AC1CF078C18AFA079D380362457BB12ECE687A2D。77 句／77 鏡、64 插圖／13 卡不變；v4 PASS 對新 SHA 已失效，仍待獨立差異來源查核與兩位新盲讀。未追蹤重複票未碰，也未做付費媒體、合併、上傳或發布。
