---
id: 2026-09-28-video-1m-google-vids-free
title: Million-views batch 4: Google Vids makes AI video free with Gemini Omni 1.1, limits and a worked example
status: blocked
priority: P1
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-30T03:40:47Z
created_at: 2026-09-28T02:30:46Z
completed_at:
branch: claude/video-1m-production
depends_on: []
scope:
  - docs/videos/google-vids-free-ai-video-omni-1-1
---

# Million-views batch 4: Google Vids makes AI video free with Gemini Omni 1.1, limits and a worked example

## Why

2026-09-23 起任何 Google 帳號能在電腦版 Google Vids 免費用 Gemini Omni 1.1 生成影片，是高搜尋量的時效題（free AI video、Gemini Omni）。這支示範怎麼做一段，並講清楚四個界線（額度、只在電腦、SynthID 浮水印、只供 Vids 內用），額度部分兩份官方頁不一致（6 支 vs 50 支），影片兩個都列。企劃 `docs/videos/google-vids-free-ai-video-omni-1-1/brief.md` 已寫好。

## Definition of done

- [x] `brief.md` 寫好，流程 steps、四界線、兩份官方頁額度不一致的處理、英文包裝都在。
- [ ] 影片走完全自動路線到「可以上架」，站主上傳，英文配音已上傳。
- [ ] 額度數字在撰稿當天以兩份官方說明頁重查，仍不一致就兩個都列。

## Steps

- [x] 企劃：`brief.md` 已寫好，三個大綱選項、站主觀點、示範或實算、會過期的事實、英文包裝都在（`node` lint 的 outlineOptions 與 checkBrief 通過）。
- [ ] 站主在 `/admin/videos` 設定分頁存好「頻道立場」（若條號和 brief 的「套用立場」不同，改 brief 那一行即可）。
- [ ] 選大綱：`review-push --gate outline`；Jev 依立場挑，或站主選。
- [ ] 撰稿（sonnet）→ 換人查核（opus）→ 聽眾審稿 → `lint` 零錯誤。撰稿當天用瀏覽器重查「會過期的事實」表裡的每個官方頁。
- [ ] tts → check-audio → render → assemble → 五語 CC → `qa` 11 項 → 成片核准。
- [ ] package → 上架確認 → 站主上傳。
- [ ] **配音**：站主在影片頁勾 en（ja、ko、zh-CN 建議一併），工人做多語言音軌（英文市場是這批的重點，別漏勾）。
- [ ] 縮圖先出英文；一支對多語言掛不同縮圖等 `2026-09-28-video-localized-thumbnails` 落地。
- [ ] 重查 Google 說明頁：規格（24fps、720p/1080p、3-10 秒）、額度兩頁數字、上傳影片的地區限制、旁白 coming soon。

## How to verify

```bash
node tools/video/cli.mjs lint --slug google-vids-free-ai-video-omni-1-1
node tools/video/cli.mjs status --slug google-vids-free-ai-video-omni-1-1 --workdir <VIDEO_WORKDIR>
```

## Notes

- 這是「百萬點閱批次」的一支，總規劃在 `docs/videos/MILLION-VIEWS.md`。
- 目標市場是英文，中文旁白服務台灣；靠英文題目搜尋量＋多語言音軌衝點閱，靠站主觀點＋實算守 YouTube 非原創內容政策。
- 撰稿階段會往共用的 `docs/videos/lexicon.json` 加英文詞的唸法；那支檔全批共用，由產線集中處理，本票 scope 只含自己的資料夾，跑到撰稿時再協調（自動產線是單一工人依序做，不會六支同時搶）。
- 官方數字都以撰稿當天重查為準，brief 的「會過期的事實」列了每個要重查的網址。
- 不放實際生成的影片片段（使用範圍未定）；用投影片版型描述流程。
- 記憶點：關分頁前要先把生成片段插進 Vid，否則消失。

## Progress (2026-09-28, claude-opus-5-5)

Pipeline stages 1–4 done: `video.json` (option A, 11 chapters, ~8.2 min, lint 0/0), `claims.md` (c1–c11), `verify-1.md`. Two facts corrected: the usage-scope quote is now the help page's verbatim sentence, and the quota chapter no longer calls the 6-clip figure a personal-account limit (the page labels it Workspace Individual; default is 500 seconds; the generation page says most users get 50). Follow-up filed for the site article: `google-vids-quota-recheck`. Lexicon gained `Lite`, `Vid`, `Individual`. Remaining stages need the owner setup; next is `review-push --slug google-vids-free-ai-video-omni-1-1 --gate outline`.

### 2026-09-29 independent P1 fact review

第一輪與不同查核者第二輪完成；恢復英文avatar條件、正確區分50／6／500的帳號及單位。來源與查核證據見 `docs/videos/google-vids-free-ai-video-omni-1-1/verify-p1-20260929.md`（如有第二輪，以 `verify-p1-20260929-round2.md` 為最新交接）。同步更正旁白、字卡、標題／說明及claims；未改brief或共用lexicon。最終lint結果由本輪總報告記錄。

只完成獨立事實重查及稿件修正；CTA是否對應已發布文章、觀點／大綱、聽眾與真人試用、TTS／字幕／成片QA／上架仍未完成。既有 `verify-1.md` 是原作者自查且绑定舊稿，CLI顯示fact-checked不能代替上述驗收。

站主對六片後續製作方向尚待回覆；未產生付費媒體、改正式設定或上傳。釋出本次claim，保留原製作票與未勾條件供接續。

## 2026-09-30 製作進度（claude-fable-5-1／claude-opus-5-5）

- 站主 09-28 選大綱 B；重寫 → 查核兩輪（第一輪發現大綱 B 的「五件沒寫清楚的事」有三件在其他官方頁有答案，改成「公告沒寫清楚的五件事＋說明頁的答案」，站主要決定這個框架是否可接受）→ 聽眾審稿。
- 旁白：兩輪改寫後 0 標記；最長畫面 14.2 秒。`qa` 10／11：Jev 的「有示範」0.52（門檻 0.6），站主已手動核准成片（41f9a10eab79）。
- 四語字幕翻譯＋審稿（zh-CN 用站上文章的 虚拟化身、列名的方案）；配音 en 0 標記、ja 剩 4 句、ko 剩 3 句（都是同音或助詞）。`package` 4／4（metadata.json a7bd735ee6e6）→ 上架確認自動核准 → 語言卡已送出、等站主。剩下的是站主的事：照 `upload/UPLOAD.md` 在 Studio 上傳成私人、在「語言」頁加三條配音音軌並在語言卡按「已在 Studio 上傳配音」、在「可以上架」卡貼網址與上架時間。本機工作區 `C:/Users/x8120/mokaair-work/videos/<slug>/`（`upload/`、`dubs/<語系>.m4a`）。
- 站上文章 `ai-news-google-vids-omni-free-20260924` 的 zh-CN 版仍寫官方沒說年齡限制與中文提示；影片的查核（c7、c8）已找到答案（18 歲以上、只支援英文），文章要另開票更新。
