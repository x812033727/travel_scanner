---
id: 2026-09-28-video-1m-vibe-coding
title: Million-views batch 5: vibe coding your first website in 2026 with Claude, ChatGPT or Gemini, published free
status: blocked
priority: P1
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-30T03:40:52Z
created_at: 2026-09-28T02:30:46Z
completed_at:
branch: claude/video-1m-production
depends_on: []
scope:
  - docs/videos/vibe-coding-first-website-2026
---

# Million-views batch 5: vibe coding your first website in 2026 with Claude, ChatGPT or Gemini, published free

## Why

「vibe coding」「build a website with AI」是 2026 年英文市場超高搜尋量的常青教學題（多支破百萬）。這支教不會寫程式的人把需求寫成一段話、用三家工具產出單一 HTML、一次只改一件事、免費上線，並在上線前檢查沒把個資或金鑰寫進原始碼。企劃 `docs/videos/vibe-coding-first-website-2026/brief.md` 已寫好。

## Definition of done

- [x] `brief.md` 寫好，需求四面向、三家工具差別、免費上線兩服務限制表、上線前檢查、英文包裝都在。
- [ ] 影片走完全自動路線到「可以上架」，站主上傳，英文配音已上傳。
- [ ] Artifacts、ChatGPT Sites、Canvas、GitHub Pages、Cloudflare Pages 的方案與限制在撰稿當天重查。

## Steps

- [x] 企劃：`brief.md` 已寫好，三個大綱選項、站主觀點、示範或實算、會過期的事實、英文包裝都在（`node` lint 的 outlineOptions 與 checkBrief 通過）。
- [ ] 站主在 `/admin/videos` 設定分頁存好「頻道立場」（若條號和 brief 的「套用立場」不同，改 brief 那一行即可）。
- [ ] 選大綱：`review-push --gate outline`；Jev 依立場挑，或站主選。
- [ ] 撰稿（sonnet）→ 換人查核（opus）→ 聽眾審稿 → `lint` 零錯誤。撰稿當天用瀏覽器重查「會過期的事實」表裡的每個官方頁。
- [ ] tts → check-audio → render → assemble → 五語 CC → `qa` 11 項 → 成片核准。
- [ ] package → 上架確認 → 站主上傳。
- [ ] **配音**：站主在影片頁勾 en（ja、ko、zh-CN 建議一併），工人做多語言音軌（英文市場是這批的重點，別漏勾）。
- [ ] 縮圖先出英文；一支對多語言掛不同縮圖等 `2026-09-28-video-localized-thumbnails` 落地。
- [ ] 重查三家工具的官方說明頁與兩個上線服務的限制頁（方案名稱與數字 2026 變動快，一律「以官網當天為準」）。

## How to verify

```bash
node tools/video/cli.mjs lint --slug vibe-coding-first-website-2026
node tools/video/cli.mjs status --slug vibe-coding-first-website-2026 --workdir <VIDEO_WORKDIR>
```

## Notes

- 這是「百萬點閱批次」的一支，總規劃在 `docs/videos/MILLION-VIEWS.md`。
- 目標市場是英文，中文旁白服務台灣；靠英文題目搜尋量＋多語言音軌衝點閱，靠站主觀點＋實算守 YouTube 非原創內容政策。
- 撰稿階段會往共用的 `docs/videos/lexicon.json` 加英文詞的唸法；那支檔全批共用，由產線集中處理，本票 scope 只含自己的資料夾，跑到撰稿時再協調（自動產線是單一工人依序做，不會六支同時搶）。
- 官方數字都以撰稿當天重查為準，brief 的「會過期的事實」列了每個要重查的網址。
- 全自動路線目前不做螢幕錄影，用投影片描述流程；等 `2026-09-24-video-screencast-steps` 落地才有手把手螢幕操作。
- 記憶點：上線前用純文字編輯器搜自己的電話、地址、像金鑰的字串；原始碼所有人都看得到。

## Progress (2026-09-28, claude-opus-5-5)

Pipeline stages 1–4 done: `video.json` (option A, 8 chapters, ~8.0 min, lint 0/0), `claims.md` (c1–c9), `verify-1.md`. ChatGPT's website feature is named only at the "以官網為準" level because its help page returned 403 today; everything else about Artifacts, Canvas, GitHub Pages and Cloudflare Pages was confirmed on the official pages. Lexicon gained `vibe`, `coding`, `GB`, `Git`, `NC`, `ND`. Remaining stages need the owner setup; next is `review-push --slug vibe-coding-first-website-2026 --gate outline`.

### 2026-09-29 independent P1 fact review

第一輪與不同查核者第二輪完成；保留Cloudflare拖放限制及GitHub Actions例外的適用範圍。來源與查核證據見 `docs/videos/vibe-coding-first-website-2026/verify-p1-20260929.md`（如有第二輪，以 `verify-p1-20260929-round2.md` 為最新交接）。同步更正旁白、字卡、標題／說明及claims；未改brief或共用lexicon。最終lint結果由本輪總報告記錄。

只完成獨立事實重查及稿件修正；CTA是否對應已發布文章、觀點／大綱、聽眾與真人試用、TTS／字幕／成片QA／上架仍未完成。既有 `verify-1.md` 是原作者自查且绑定舊稿，CLI顯示fact-checked不能代替上述驗收。

站主對六片後續製作方向尚待回覆；未產生付費媒體、改正式設定或上傳。釋出本次claim，保留原製作票與未勾條件供接續。

## 2026-09-30 製作進度（claude-fable-5-1／claude-opus-5-5）

- 站主 09-28 選大綱 B；重寫 → 查核兩輪（`verify-1.md`、`verify-2.md`；09-28 A 案報告改名 `verify-1-outline-a-20260928.md`）→ 聽眾審稿。
- 旁白：Gemini 標 17 句，Whisper 清 10 句，改寫兩輪後 0 標記；一個畫面 15.3 秒，拆成兩個 big 後最長 14.1 秒。縮圖標題太長（手機上 21 px），改短後過關。
- `qa` 10／11（只剩 help.openai.com 的 ChatGPT Sites 頁對檢查程式回 403），站主核准成片（ea2b9817da40）。
- 四語字幕翻譯＋審稿；配音 en 0 標記、ja 剩 1 句（ctf9，寫法差異）、ko 剩 2 句（助詞與斷字）。`package` 4／4（metadata.json ec48de930262）→ 上架確認自動核准 → 語言卡已送出、等站主。剩下的是站主的事：照 `upload/UPLOAD.md` 在 Studio 上傳成私人、在「語言」頁加三條配音音軌並在語言卡按「已在 Studio 上傳配音」、在「可以上架」卡貼網址與上架時間。本機工作區 `C:/Users/x8120/mokaair-work/videos/<slug>/`（`upload/`、`dubs/<語系>.m4a`）。
