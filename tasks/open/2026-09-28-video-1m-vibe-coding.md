---
id: 2026-09-28-video-1m-vibe-coding
title: Million-views batch 5: vibe coding your first website in 2026 with Claude, ChatGPT or Gemini, published free
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-09-28T02:30:46Z
completed_at:
branch:
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
