# S50 作者自檢｜2026-10-20 UTC

**版本註記：**本頁封存首次送交 R1 獨立查核的作者檢查與五個內容檔 hash；R1 結論為 [HOLD](review/r1-source-independent.md)。修訂後的目前版本與新 hash 見 [R2 作者凍結紀錄](review/r2-author-freeze.md)。本頁舊 hash 不代表目前檔案。

**狀態：**首次 R1 候選稿的作者靜態檢查，之後由獨立查核標為 HOLD；**不是**獨立史料覆核、雙人盲讀、網站關卡核准或成片驗收。下表只固定 R1 送審時的精確檔案版本。

| 內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `740ca5069b1bbc234406bae246b4e2312f0c03b67204c81b924c215189ee1e6b` |
| `research.md` | `e7d2425edc25442e12d82e4fbc38df7966045fa974b96c243d7babd74f083f9e` |
| `claims.md` | `67a4b84863c596ccfbcf154547000a3c1ae6f580949bda60cee6580d740eb3c8` |
| `video.json` | `4f255151d26925d30c1da2d764ecfc3550413b1fa94f83294cc033f9edcb3dad` |
| `script.md` | `27af733824aaa923ecbcfc870309406cfa7c3f92714caeeb34d8deb979bdcaa7` |

## 來源與論點檢查

- 作者直接讀取固定版本：[Pepys 日記](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt) 原始 SHA `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`；[1667 年證詞刊本](https://github.com/textcreationpartnership/A63385/blob/4ac29739d661a1c7f2a34f51ffb8a1811176f146/A63385.xml) 原始 SHA `0a4b379b932fc331c9ff10bd217e6d8b2cc513388a3fd73d7f64f0b35447595e`；[Vincent 1667 年記述](https://github.com/textcreationpartnership/A64990/blob/e15ce8bba340e6089deec4ff85b486842e568434/A64990.xml) 原始 SHA `36798f66f98c32482b09209d7acb0ed204bacae744b5eae7c40532ca7a093f29`。`research.md` 記每個用到的行段及可信界線。
- 《London Gazette》第 85 號和 London Museum 官方頁在此雲端環境回 HTTP 403；相關兩句依倉庫 P17 於 2026-10-12 記下的查核，**沒有冒稱 2026-10-20 直接重讀**。獨立查核者應在可連線環境重開這兩頁，尤其核對 `fire037` 的公報概述和 `fire108` 的博物館「可能」說法。
- 論點分成「Farriner 屋起火」、「點火方式未定」、「風、乾燥、街屋及拆屋進度促成擴大」。1667 年刊本的 13,200 是燒毀房屋數；Hubert 自白和 Farriner 自辯都只作證詞，刊本記下議院休會前未對報告作判斷。Pepys 在塔上看到火，**下塔後**才從塔樓官員得知起火屋址；腳本已按日記修正。

## 稿件與分鏡檢查

- `node tools/video/cli.mjs lint --slug curio-s50 --json`：**0 errors，0 warnings**；119 句、2383 spoken units、9 章，未加入付費媒體。
- 程式逐句比對 `video.json`、`script.md`、`claims.md`：**119/119 完全相同**，無缺失或多餘 ID。18 組 `loops` 的回收都在伏筆之後。正文 116 景中 113 景為 `shot`（97.4%），另有 3 張來源／數字卡；沒有連續卡片。
- 使用專案 `estimateTimeline` 的 250、300、325 CPM 加每景換畫停頓：前 8 景濃縮開場分別約 **50.1／43.0／40.5 秒**；其後 108 景正文約 **624.9／537.4／506.2 秒**。三種估速的正文均超過 8 分鐘，但仍須以實際頻道 TTS 檔驗證。JSON 最後三句普通片尾旁白約 17.1／14.6／13.7 秒，品牌片尾實長另以素材為準。
- 原創 5 秒片頭計畫插在第一章八景之後，製作 pin 應設 `intro_at: "after_first_chapter"`。共用 21 秒 `v4-endscreen` 素材接在成片末尾；最後 16 秒是兩個影片框與訂閱圈的清晰區，私人上傳後在 Studio 匯入現有範本、開始時間設影片長度減 16 秒並點測三個元素。此包沒有把片頭片尾素材嵌入 JSON，也沒有成片或 YouTube 上傳。

## 後續關卡

1. 由**獨立**查核者對同一內容 hash 覆核來源，重開目前 403 的官方頁，確認任何修改後再固定新版 hash。
2. 讓兩位不同讀者盲讀同一稿 hash；走站台大綱／劇本關卡。A 案是作者本地推薦，尚非站台核准。
3. 完成整集一次估價並取得必要授權後，才啟動頻道 TTS、原創 MiniMax 插畫與配樂；檢查實際正文至少 8 分鐘、音訊、插圖、品牌素材、成片和 Studio 片尾點擊。此頁未執行付費媒體、站台推送或核准。
