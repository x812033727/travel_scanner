---
id: 2026-09-28-video-1m-siri-ai
title: Million-views batch 2: Siri AI on iOS 27, who gets it and how to turn it on
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-09-28T02:30:45Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/siri-ai-ios-27-how-to-get-it
---

# Million-views batch 2: Siri AI on iOS 27, who gets it and how to turn it on

## Why

iOS 27 的 Siri AI（beta、英文、Gemini 合作）是 2026-09-14 的大新聞，觀眾想知道能不能用、怎麼開、讀什麼資料。英文搜尋量高（how to get Siri AI、Siri AI waitlist），10 月多語言上線前還有第二波。企劃 `docs/videos/siri-ai-ios-27-how-to-get-it/brief.md` 已寫好，全照 Apple 官方頁，不碰媒體報導的參數與金額。

## Definition of done

- [x] `brief.md` 寫好，機型表、申請流程、隱私原話、歐盟與中國大陸例外、英文包裝都在。
- [ ] 影片走完全自動路線到「可以上架」，站主上傳，英文配音（建議加日、韓）已上傳。
- [ ] 機型清單與語言時程在撰稿當天以 Apple 支援文件重查過。

## Steps

- [x] 企劃：`brief.md` 已寫好，三個大綱選項、站主觀點、示範或實算、會過期的事實、英文包裝都在（`node` lint 的 outlineOptions 與 checkBrief 通過）。
- [ ] 站主在 `/admin/videos` 設定分頁存好「頻道立場」（若條號和 brief 的「套用立場」不同，改 brief 那一行即可）。
- [ ] 選大綱：`review-push --gate outline`；Jev 依立場挑，或站主選。
- [ ] 撰稿（sonnet）→ 換人查核（opus）→ 聽眾審稿 → `lint` 零錯誤。撰稿當天用瀏覽器重查「會過期的事實」表裡的每個官方頁。
- [ ] tts → check-audio → render → assemble → 五語 CC → `qa` 11 項 → 成片核准。
- [ ] package → 上架確認 → 站主上傳。
- [ ] **配音**：站主在影片頁勾 en（ja、ko、zh-CN 建議一併），工人做多語言音軌（英文市場是這批的重點，別漏勾）。
- [ ] 縮圖先出英文；一支對多語言掛不同縮圖等 `2026-09-28-video-localized-thumbnails` 落地。
- [ ] 重查 Apple 新聞稿與〈How to get Siri AI〉：機型清單、語言時程、等候名單、歐盟與中國大陸例外是否有變。

## How to verify

```bash
node tools/video/cli.mjs lint --slug siri-ai-ios-27-how-to-get-it
node tools/video/cli.mjs status --slug siri-ai-ios-27-how-to-get-it --workdir <VIDEO_WORKDIR>
```

## Notes

- 這是「百萬點閱批次」的一支，總規劃在 `docs/videos/MILLION-VIEWS.md`。
- 目標市場是英文，中文旁白服務台灣；靠英文題目搜尋量＋多語言音軌衝點閱，靠站主觀點＋實算守 YouTube 非原創內容政策。
- 撰稿階段會往共用的 `docs/videos/lexicon.json` 加英文詞的唸法；那支檔全批共用，由產線集中處理，本票 scope 只含自己的資料夾，跑到撰稿時再協調（自動產線是單一工人依序做，不會六支同時搶）。
- 官方數字都以撰稿當天重查為準，brief 的「會過期的事實」列了每個要重查的網址。
- 不放 Apple 產品圖或截圖（版權）；機型用 table、流程用 steps。
- 台灣觀眾的取捨（要把整台手機改英文）是繁中旁白的重點；英文觀眾不需要這段，翻譯時照字幕處理。
