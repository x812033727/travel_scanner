# X11 FedEx｜品牌故事本機前製包

**狀態：v6 候選稿已鎖版，等待同版來源差異審查與兩位新獨立盲讀。** v5 的[來源審查](reviews/source-audit-v5-independent.md)因末章美國地理口徑未明而 HOLD；[盲讀 A](reviews/blind-a-v5-independent.md)通過 11／12 題，但要求關鍵畫面的兩網／兩地辨識持續清楚。v6 已做窄幅修訂，舊收據不能沿用。這裡沒有付費生成、試片、正式片頭片尾檔或 YouTube 公開連結；稿件不能當成已完成的影片或審查 PASS。

- [選題簡報](brief.md)與[六章 Treatment](treatment.md)：觀眾問題、反轉、濃縮開場與章節事件。
- [原始來源可行性](source-feasibility.md)、[作者主張矩陣](source-matrix.md)、[逐句來源矩陣](line-source-matrix.md)：五份 SEC 年報、日期邊界及待獨立覆核的逐句依據。
- [逐句稿](script.md)、[主片編排](video.json)、[兩支 Shorts 編排](shorts.json)與[Shorts 稿](shorts-script.md)：正式語音和剪輯都尚未製作。
- [畫面計畫](visual-plan.md)、[費用護欄](production-quote.md)、[上架交接](publishing-handoff.md)：MiniMax、Sulafat、字幕、片頭片尾、US$25 上限及真實連結的待辦條件。
- `drafts/narration.md`、`drafts/visual-cues.mjs`、`compose-video.mjs`、`compose-shorts.mjs` 是可重建稿面的作者檔；更改任何作者檔後須重編、重算雜湊並重新獨立審查。

目前 v6 鎖定的 `video.json` SHA-256：`e8aa68f3aef2a8d8d1068152fe5cf024cfc9e91590103c37b586b338ba10d240`；`shorts.json` SHA-256：`7d352677b785667866b6ef09e7c4f4934d6659fb966f334c8d98c4ac063dcaa6`。Shorts 的 JSON 位元組未變，但其引用的主片鏡頭提示詞已改，須和 v6 主片成對審查。指令 `node docs/videos/story-everyday-fedex-x11/compose-video.mjs`、`node docs/videos/story-everyday-fedex-x11/compose-shorts.mjs` 可重建；`node tools/video/cli.mjs lint --slug story-everyday-fedex-x11` 可檢查格式與故事規格。[v6 作者修訂與來源差異](revision-v6.md)只列覆核入口，不能充當獨立審查。鎖版審查若要求改稿，主片 SHA 必須更新。
