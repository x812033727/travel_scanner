# X11 FedEx｜品牌故事本機前製包

**狀態：v5 候選稿已鎖版，等待同版來源差異審查與兩位新獨立盲讀。** v4 的[來源差異審查](reviews/source-audit-v4-independent.md)通過，但[盲讀 A](reviews/blind-a-v4-independent.md)與[盲讀 B](reviews/blind-b-v4-independent.md)都未通過；v5 已按兩份具體意見重寫，舊收據不能沿用。這裡沒有付費生成、試片、正式片頭片尾檔或 YouTube 公開連結；稿件不能當成已完成的影片或審查 PASS。

- [選題簡報](brief.md)與[六章 Treatment](treatment.md)：觀眾問題、反轉、濃縮開場與章節事件。
- [原始來源可行性](source-feasibility.md)、[作者主張矩陣](source-matrix.md)、[逐句來源矩陣](line-source-matrix.md)：五份 SEC 年報、日期邊界及待獨立覆核的逐句依據。
- [逐句稿](script.md)、[主片編排](video.json)、[兩支 Shorts 編排](shorts.json)與[Shorts 稿](shorts-script.md)：正式語音和剪輯都尚未製作。
- [畫面計畫](visual-plan.md)、[費用護欄](production-quote.md)、[上架交接](publishing-handoff.md)：MiniMax、Sulafat、字幕、片頭片尾、US$25 上限及真實連結的待辦條件。
- `drafts/narration.md`、`drafts/visual-cues.mjs`、`compose-video.mjs`、`compose-shorts.mjs` 是可重建稿面的作者檔；更改任何作者檔後須重編、重算雜湊並重新獨立審查。

目前 v5 鎖定的 `video.json` SHA-256：`3d2a7d1d422105802fd1d755fa8f90f1ca5667057f76aa133d90db0f5efba0d8`；`shorts.json` SHA-256：`7d352677b785667866b6ef09e7c4f4934d6659fb966f334c8d98c4ac063dcaa6`。指令 `node docs/videos/story-everyday-fedex-x11/compose-video.mjs`、`node docs/videos/story-everyday-fedex-x11/compose-shorts.mjs` 可重建；`node tools/video/cli.mjs lint --slug story-everyday-fedex-x11` 可檢查格式與故事規格。[v5 作者修訂與來源差異](revision-v5.md)只列覆核入口，不能充當獨立審查。鎖版審查若要求改稿，這兩個 SHA 必須更新。
