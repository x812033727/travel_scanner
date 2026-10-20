---
id: 2026-10-20-curio-s56-chicago-fire-river-crossings
title: Curio S56 Chicago fire river crossings episode
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-20T19:24:19Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s56
---

# Curio S56 Chicago fire river crossings episode

## Why

站主委託持續製作新的奇聞檔案局歷史影片。S56 以 1871 年芝加哥大火目擊者的逃生路線，回答「河水為何沒擋住對岸火點」，重點是飛火、可燃街面與水廠失效，不拿奶牛起火傳聞當定案。

## Definition of done

- [x] 題材不重複現有 `curio-s*`；作者整理兩份可重開的固定版目擊者文字、SHA-256、Git blob 和逐行主張。
- [x] **不同工作者**重開原文、重算 SHA-256、逐項核對 `research.md` P01–P12，對七章、8–15 分鐘可行性判 PASS／HOLD。見 [source-feasibility-1.md](../../docs/videos/curio-s56/source-feasibility-1.md)。
- [ ] 只在題材 PASS 後寫逐句劇本、主張表及原創 `cute-mystery` 分鏡，進獨立逐句史料／書面畫面審查與兩位新讀者的正式盲評。
- [ ] 旁白實測正文至少 8 分鐘，音檢、站台關卡、插圖、配樂、30–60 秒濃縮開場、5 秒片頭、21 秒片尾、四語字幕及上傳包完整；實際可點的結尾推薦只能在 YouTube 私人上傳後設定與驗證。

## Steps

- [x] 搜尋同題並讀 `curio-episode`／`youtube-video`；1904 聖路易馬拉松官方資料在此環境仍受代理 403，已有舊 HOLD 票，不重做傳聞稿。
- [x] 固定 Foster 1871-10-31 家書的 1923 年印本與 Loesch 1925 年回憶；寫 [research.md](../../docs/videos/curio-s56/research.md)、[brief.md](../../docs/videos/curio-s56/brief.md)。
- [x] 獨立史料題材覆核；作者不能自判 PASS。
- [ ] 逐句腳本 R1 已落地；接著由不同工作者查核全稿來源與畫面、由兩位真正隔離的新讀者盲評，再決定是否進入語音與媒體。任何需站台決定的卡片保留真實狀態。

## How to verify

`git clone` 兩個 [research.md](../../docs/videos/curio-s56/research.md) 指定提交，取 `66472-0.txt` 和 `66433-0.txt` 後核 SHA-256；引用網址含固定 commit 和行號。`npm run check:tasks` 驗任務格式，`git diff --check` 驗空白；機械檢查不代替獨立原文對讀。

## Notes

Foster 信文標明 1871 年 10 月 31 日，但 1923 年編者說原稿已不知去向、保存的是家人抄本；他親見飛火與南支河岸次生火點，不能說他逐格看見某塊木片飛過河。Loesch 於事件後 54 年出版回憶，關於北側街道、抽水站和雨的場景要歸他。兩人不曾在本來源中碰面；不能把他們拍成對話。1923 編者轉述的牛與另一掉燈說法都不能當火因定論。題材 PASS 後，作者為配合格式 lint 只把 `brief.md` 的合併標題拆成 `## 問題`／`## 一句答案`，故題材覆核報告所列舊 brief SHA 已成歷史快照；內容不變，劇本獨立覆核仍須讀現稿。媒體尚未製作，真實長片網址不存在。
