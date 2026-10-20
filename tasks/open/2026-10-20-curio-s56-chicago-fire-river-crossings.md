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
- [x] 只在題材 PASS 後寫逐句劇本、主張表及原創 `cute-mystery` 分鏡，進獨立逐句史料／書面畫面審查與兩位新讀者的正式盲評；R4 史料與正式 OR 敘事關卡皆 PASS。
- [ ] 旁白實測正文至少 8 分鐘，音檢、站台關卡、插圖、配樂、30–60 秒濃縮開場、5 秒片頭、21 秒片尾、四語字幕及上傳包完整；實際可點的結尾推薦只能在 YouTube 私人上傳後設定與驗證。

## Steps

- [x] 搜尋同題並讀 `curio-episode`／`youtube-video`；1904 聖路易馬拉松官方資料在此環境仍受代理 403，已有舊 HOLD 票，不重做傳聞稿。
- [x] 固定 Foster 1871-10-31 家書的 1923 年印本與 Loesch 1925 年回憶；寫 [research.md](../../docs/videos/curio-s56/research.md)、[brief.md](../../docs/videos/curio-s56/brief.md)。
- [x] 獨立史料題材覆核；作者不能自判 PASS。
- [x] 逐句腳本 R4 的窄幅畫面／主張表修正凍結於 [r4-author-fix.md](../../docs/videos/curio-s56/review/r4-author-fix.md)，不同工作者的來源／書面畫面覆核於 [r4-source-independent.md](../../docs/videos/curio-s56/review/r4-source-independent.md) 判 PASS。先前繼承脈絡的兩讀者 OR 於 [r4-isolated-merge.md](../../docs/videos/curio-s56/review/r4-isolated-merge.md) 曾判 PASS；後來真正無歷史脈絡新讀者的覆核取代該票，見下一步。
- [x] R4 網站註冊為 `explainer`／`drama`，完整 Jev 政策 PASS；精確企劃／劇本網站卡手推後仍 `pending`。Gemini Sulafat 實測正文 13:03.17（限縮重錄後），176／176 音檢由 52 旗標降到 33；詳 [verify-4.md](../../docs/videos/curio-s56/verify-4.md)。無歷史脈絡新讀者的[正式合併](../../docs/videos/curio-s56/review/r4-clean-merge.md)對 R4 判 12／13 FAIL，音訊只是 R4 草稿，不可放行。

## How to verify

`git clone` 兩個 [research.md](../../docs/videos/curio-s56/research.md) 指定提交，取 `66472-0.txt` 和 `66433-0.txt` 後核 SHA-256；引用網址含固定 commit 和行號。`npm run check:tasks` 驗任務格式，`git diff --check` 驗空白；機械檢查不代替獨立原文對讀。

## Notes

R2 的獨立史料與書面畫面覆核為 PASS，但正式兩讀者 OR 敘事關卡有五項未過；見 [r2-isolated-merge.md](../../docs/videos/curio-s56/review/r2-isolated-merge.md)。R3 作者修訂五項後，[R3 獨立史料／書面畫面審查](../../docs/videos/curio-s56/review/r3-source-independent.md) 判 HOLD：避難地夜間提示詞仍寫下午光線，主張表搬動後的畫面界線與引用有錯位。R4 作者只修那些提示詞、畫面界線和引用，五檔雜湊與檢查見 [r4-author-fix.md](../../docs/videos/curio-s56/review/r4-author-fix.md)；不同工作者於 [R4 獨立審查](../../docs/videos/curio-s56/review/r4-source-independent.md) 逐項核對後判 PASS，176 句與 lint 仍過。原先繼承脈絡的 [R4 合併](../../docs/videos/curio-s56/review/r4-isolated-merge.md)雖為 13／13 PASS，兩名無歷史脈絡的新讀者依同一 OR 規則[重判](../../docs/videos/curio-s56/review/r4-clean-merge.md)為 **12／13 FAIL**，共同否決 `no_recap`。這個較嚴格結果取代舊票，R4 須修稿後重新覆核；不得把本輪 [政策／語音收據](../../docs/videos/curio-s56/verify-4.md) 當作放行。R4 旁白已合成，首次 141 請求／3,798 字元，一輪只重配 52 旗標句、48 請求／1,055 字元；最後仍 33 句音檢旗標，沒有第二輪重錄或付費插圖。

Foster 信文標明 1871 年 10 月 31 日，但 1923 年編者說原稿已不知去向、保存的是家人抄本；他親見飛火與南支河岸次生火點，不能說他逐格看見某塊木片飛過河。Loesch 於事件後 54 年出版回憶，關於北側街道、抽水站和雨的場景要歸他。兩人不曾在本來源中碰面；不能把他們拍成對話。1923 編者轉述的牛與另一掉燈說法都不能當火因定論。題材 PASS 後，作者為配合格式 lint 只把 `brief.md` 的合併標題拆成 `## 問題`／`## 一句答案`，故題材覆核報告所列舊 brief SHA 已成歷史快照；內容不變，劇本獨立覆核仍須讀現稿。媒體尚未製作，真實長片網址不存在。

2026-10-20 R12：R11 兩輪限縮重錄後仍有兩句音檢旗標，作者只改這兩句口語並[重凍結五檔](../../docs/videos/curio-s56/review/r12-author-oral-repair.md)。[獨立來源／書面畫面](../../docs/videos/curio-s56/review/r12-source-independent.md)、[正式雙讀者 OR 13／13 與同版政策](../../docs/videos/curio-s56/review/r12-merge-policy/summary.md) PASS。只新合成兩句、37 計費字元；WAV SHA 清單確認只有這兩句更動。[完整音檢](../../docs/videos/curio-s56/review/r12-audio-gate/summary.md) **154／154、0 旗標，本地機器 PASS**；旁白實測 12:11.67、濃縮開場 54.53 秒。[驗證](../../docs/videos/curio-s56/verify-12.md)記錄站台大綱、R12 劇本與音訊卡均已送出但仍待站主審核。全片插圖、配樂、片頭片尾、組片、字幕、Shorts 與實際可點上架連結尚未完成。
