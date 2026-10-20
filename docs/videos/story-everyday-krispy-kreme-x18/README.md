# X18｜試點說賣得好，Krispy Kreme 為何撤出麥當勞？

**狀態：v3 離線前製，等待對本版 SHA 的新獨立 SEC 逐句審核與兩名新讀者盲評。** v2 的[獨立來源稽核](reviews/script-source-audit-v2-independent.md)對其舊 SHA 判 PASS，但新讀者 [A](reviews/blind-a-v2-independent.md)／[B](reviews/blind-b-v2-independent.md)共同指出重述與公司整體財務岔路，B 另指出七月終止後倒回六月季末。這些舊收據不核准 v3；[作者 v3 回應](reviews/author-response-v3.md)逐項記錄本次修訂。本包沒有付費媒體、配音、插畫、MP4、Shorts 成片、YouTube 網址或發布證明。它是二十支新品牌故事系列 `brand-stories-everyday-reversals-extra` 的第 18 支，追的是 Krispy Kreme 與麥當勞一項每日配送合作，不是兩家公司全部業務。

肯塔基 160 家試點被雙方形容需求超出預期。2024 年 3 月宣布向 2026 年底全國參與門市**預期**推進；10 月先芝加哥、年末每日配送逾 1,900 家；2025 年 3 月逾 2,400 家時，公司與麥當勞重估部署，預期第二季不再新增。6 月 23 日雙方共同**宣布**終止，6 月 29 日 Q2 季末仍含約 2,400 家合作店，7 月 2 日才**生效**，9 月 28 日 Q3 全球銷售點另有退出後的統計。麥當勞表示滿足自身及加盟經營者期待，Krispy Kreme 表示成本未能配合單店需求。此反差是故事答案；公司整體 Q3／FY 財務留來源矩陣和說明欄，不能推算單一合作利潤。

八份一手 SEC HTML 均重抓 HTTP 200、小於 3 MiB，原始 bytes／SHA、核心段落前 40,000 字可讀性與禁區在 [source-matrix.md](source-matrix.md)。[六章企劃](treatment.md)與 [簡報](brief.md)說明事件主線；[逐句稿](script.md)、[作者逐句來源表](line-source-matrix.md)及 [分鏡](visual-plan.md)對應 `video.json`。兩支獨立 Short 的 [逐句稿](shorts-script.md)、[逐句來源](shorts-source-matrix.md)、[逐拍 9:16 規劃](shorts-portrait-plan.md)對應 `shorts.json`。`drafts/` 是可讀母稿；兩個 compose 腳本重建 JSON、逐句稿和矩陣，改字後先重編再審。

本版主片濃縮開場 185 字，正文 **2,482 個實質書寫字元**，@300 字／分紙面約 8.2 分、13 條已綁句 ID 的回收環；六章之外恰三句結尾。第六章按 6/29 → 7/2 → 9/28 前進，保留全球銷售點分母與退場成本的有限後果，最後回到被收起的合作路線。主片規劃 106 張靜態插畫、6 張原生數字卡、1 張純後製結尾槽，Shorts 各 8 拍、198／188 字，重用 16 張不同主片圖；Short 2 的 18,113／14,851 各由對應主片 `shot` 加原生數字疊字呈現。插畫固定 MiniMax `image-01`、`look: {"preset":"cute-mystery"}`，不畫商標／可讀字／真人；縮圖以模板排橘色大字「Krispy Kreme」。離線 lint 必須 0 錯誤／0 警告，實際 TTS 仍須確認正文 ≥8:00、Shorts 各 25–55 秒。

本版待獨立審核的 JSON SHA-256：`video.json` `ba5500bc756135bd2a0d5093fd0a0d209b8c7b3bdcd3b087c0d205e76b852b43`；`shorts.json` `ecb5cc1422695b11ebd62efae8a6369ec89c9cf481a4b18f71490b8367e23141`。稿、視覺或來源若變，重編兩份並以新 SHA 重審。

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
