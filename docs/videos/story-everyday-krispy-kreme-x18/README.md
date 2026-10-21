# X18｜試點說賣得好，Krispy Kreme 為何撤出麥當勞？

**狀態：v7 離線前製候選，等待本版 SHA 的新獨立 SEC 逐句審核與兩名全新讀者盲評。** [v6 獨立 SEC 稽核](reviews/script-source-audit-v6-independent.md)通過該版事實界線，但兩名首讀者 [A](reviews/blind-a-v6-independent.md)／[B](reviews/blind-b-v6-independent.md)都對必答 Q8／Q13 判 No，敘事仍 HOLD。[作者 v7 回應](reviews/author-response-v7.md)記錄修訂；v6 收據不核准 v7。本包沒有付費媒體、配音、插畫、MP4、Shorts 成片、YouTube 網址或發布證明。它是二十支新品牌故事系列 `brand-stories-everyday-reversals-extra` 的第 18 支，追的是 Krispy Kreme 與麥當勞一項每日配送合作，不是兩家公司全部業務。

肯塔基 160 家試點被雙方形容需求超出預期。2024 年 3 月宣布向 2026 年底全國參與門市**預期**推進；10 月先芝加哥、年末每日配送逾 1,900 家；2025 年 3 月逾 2,400 家時，公司與麥當勞重估部署，預期第二季不再新增。6 月 23 日雙方共同**宣布**終止，6 月 29 日 Q2 季末仍含約 2,400 家合作店，7 月 2 日才**生效**，9 月 28 日 Q3 全球銷售點另有退出後的統計。麥當勞表示滿足自身及加盟經營者期待，Krispy Kreme 表示成本未能配合單店需求。此反差是故事答案；公司整體 Q3／FY 財務留來源矩陣和說明欄，不能推算單一合作利潤。

八份一手 SEC HTML 在 2026-10-20 重抓 HTTP 200、小於 3 MiB；當日原始 bytes／SHA、可讀性與禁區在 [source-matrix.md](source-matrix.md)。10/21 的 v6 獨立稽核重抓八份，各份 raw HTML 比前日多 9 bytes；只替換尾部輪替的注入 script 標籤，其餘位元組才相同。**兩日 raw SHA 並不相同。**新審稿仍須記錄當次原件及正文差異。**S7 的第三季約 2,400 退出註腳在解析字第 40,000 字之外**，正式匯入必用完整頁面加數字錨點定向擷取，或列人工查核。[六章企劃](treatment.md)與 [簡報](brief.md)說明事件主線；[逐句稿](script.md)、[作者逐句來源表](line-source-matrix.md)及 [分鏡](visual-plan.md)對應 `video.json`。兩支獨立 Short 的 [逐句稿](shorts-script.md)、[逐句來源](shorts-source-matrix.md)、[逐拍 9:16 規劃](shorts-portrait-plan.md)對應 `shorts.json`。`drafts/` 是可讀母稿；兩個 compose 腳本重建 JSON、逐句稿和矩陣，改字後先重編再審。

本版主片濃縮開場 191 字，正文 **2,474 個實質書寫字元**（lint 計 2,419 口播單位，@280／300 字每分紙面約 8:38／8:04）、103 句、17 條已綁句 ID 的回收環；六章之外恰三句結尾。第三章刪去全球總點數旁白，改由 S3 支持的第四季全美配送網樞紐與支線投資接住餐盤路線；第四章問題不再重述剛說過的獲利模式。第六章按 6/29 季末仍有合作店 → 7/2 生效退出 → 十一月公布第三季的滯留成本與移除情況前進，最後回到被收起的合作路線。兩季**全球**銷售點的詳細對照留給獨立 Short 2 和來源說明。主片規劃 95 張靜態插畫、4 張原生數字卡、1 張純後製結尾槽，Shorts 各 8 拍、198／190 字，重用 16 張不同主片圖；Short 2 的 18,113／14,851 各由對應主片 `shot` 加原生數字疊字呈現。插畫固定 MiniMax `image-01`、`look: {"preset":"cute-mystery"}`，不畫商標／可讀字／真人；縮圖以模板排橘色大字「Krispy Kreme」。離線 lint 為 0 錯誤／0 警告，實際 TTS 仍須確認正文 ≥8:00、Shorts 各 25–55 秒。

本版待獨立審核的 JSON SHA-256：`video.json` `b62883b6acc5d486c7a329e8458f03b0e070b04b51f547f1fb410abafeb2100f`；`shorts.json` `53423ea2bed98681476de0cff436ff1543c3ac9a98a479c1baff410cc84acfd9`。稿、視覺或來源若變，重編兩份並以新 SHA 重審。

**濃縮內容、動畫與連結。** 開場 30–60 秒先於正式 5 秒片頭；最後三句後放官方 21 秒 v4 片尾。繁中 CC 可關閉、不燒字幕。主片、兩支 Shorts、播放清單及濃縮內容的真 URL 均待私人上傳後回填，結束畫面最後 16 秒的三個可點元素須實測。媒體、審核、成本、連結的順序在 [publishing-handoff.md](publishing-handoff.md)；[整片 US$25 配額](production-quote.md)涵蓋兩 Short、評審、重試與預留，這份試算不是已花費。

離線重編及驗證：

```bash
node docs/videos/story-everyday-krispy-kreme-x18/compose-video.mjs
node docs/videos/story-everyday-krispy-kreme-x18/compose-shorts.mjs
node tools/video/cli.mjs lint --slug story-everyday-krispy-kreme-x18
npm run test:docs-videos
npm run check:tasks
sha256sum docs/videos/story-everyday-krispy-kreme-x18/{video,shorts}.json
```

`shorts.json` 是兩支物件的陣列；單支 `tools/video/shorts/cli.mjs validate --file <暫存單支.json> --source-base docs/videos/story-everyday-krispy-kreme-x18` 各驗一次，再用 `episodeShortsProblems(shorts, video)` 驗整集兩支的 slug、來源和 shot 綁定。所有驗證只保證稿／schema，**不**代表已審圖、真時長、成片品管或上架。
