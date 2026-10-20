# X11 FedEx｜品牌故事本機前製包

**狀態：v4 候選稿已鎖版，等待新版來源差異審查與兩位新獨立盲讀。** [v3 兩位盲讀](reviews/)指出未回收問題、重複資訊和 Freight 支線，v4 已修稿，舊版審查收據不能沿用。這裡沒有付費生成、試片、正式片頭片尾檔或 YouTube 公開連結；稿件不能當成已完成的影片或審查 PASS。

- [選題簡報](brief.md)與[六章 Treatment](treatment.md)：觀眾問題、反轉、濃縮開場與章節事件。
- [原始來源可行性](source-feasibility.md)、[作者主張矩陣](source-matrix.md)、[逐句來源矩陣](line-source-matrix.md)：五份 SEC 年報、日期邊界及待獨立覆核的逐句依據。
- [逐句稿](script.md)、[主片編排](video.json)、[兩支 Shorts 編排](shorts.json)與[Shorts 稿](shorts-script.md)：正式語音和剪輯都尚未製作。
- [畫面計畫](visual-plan.md)、[費用護欄](production-quote.md)、[上架交接](publishing-handoff.md)：MiniMax、Sulafat、字幕、片頭片尾、US$25 上限及真實連結的待辦條件。
- `drafts/narration.md`、`drafts/visual-cues.mjs`、`compose-video.mjs`、`compose-shorts.mjs` 是可重建稿面的作者檔；更改任何作者檔後須重編、重算雜湊並重新獨立審查。

目前 v4 鎖定的 `video.json` SHA-256：`b2226de5962c60ffa90ee177011a9203deb340d3ebbe2355d9be8c79d512d5b0`；`shorts.json` SHA-256：`7413df056023ae9dfc38f57fa34526c26b0e4d3e4206d911c92a7120db99ba45`。指令 `node docs/videos/story-everyday-fedex-x11/compose-video.mjs`、`node docs/videos/story-everyday-fedex-x11/compose-shorts.mjs` 可重建；`node tools/video/cli.mjs lint --slug story-everyday-fedex-x11` 可檢查格式與故事規格。[作者修訂與來源差異](revision-v4.md)只列覆核入口，不能充當獨立審查。鎖版審查若要求改稿，這兩個 SHA 必須更新。
