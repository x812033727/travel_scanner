# S48｜R2 精準修訂與再審交接

2026-10-20 UTC。此版回應 [R1 獨立史料／書面畫面 HOLD](review/r1-source-independent.md)。以下是作者改稿及靜態檢查，**不自行撤銷 R1 HOLD，也不冒稱獨立差分通過、兩名盲讀通過、站台核准或成片**。

| 固定稿 | R1 SHA-256（見 [verify-1.md](verify-1.md)） | R2 SHA-256 |
| --- | --- | --- |
| [brief.md](brief.md) | `5a6f3e107bb21f7104d9a132d11bd4f38eb259e82f2448f44ff6a7fbd60f8680` | `c4a7a6fb51dcfc59429b834047cfbb657f2c73dd0e2c254ca018e4bf00af84d4` |
| [research.md](research.md) | `da0be70bbba324df9bf84f87e88fbf061dfea935c9cbe5d662172aff502ce927` | `67f286745510347b2ad8ce1dcb4bd2cbf46634a8c6574c0360bc4e089c0b7f53` |
| [video.json](video.json) | `72ec6a1cfbd0c767a0e087ed53bc7b48ac293485bcd79a1b22b58c328da54608` | `431f19fcf13bc325df7de65678fcc6d34368becb946a722ca931e9a3786032f3` |
| [script.md](script.md) | `9955e0fbd9f023e31926c3de2036b4091acbd6c38ee8d723f861bb6944f017de` | `4cacc1bc8e130373d0783dad3382209be4fbbbc04a69b38b86221b294d53e898` |
| [claims.md](claims.md) | `7083fe431b7c7d69ef56fcebb112430ec781d8bd47f495a730f9000099d530ed` | `f85eae29e70897fadc62e07bd13348443ee2faaccc739f3a593ff447586e7054` |

兩份原文固定檔未變：Russell `558efcc342df669e7387ffff818c104690e7ec910de49e795f996abf147ea750`；Field `bee659b24ace56a5e1f7104a6a306e9325ccd9c864fc373ad35b0863c5a8c675`。R2 的 `video.json` 共 100 張預定 `shot`、18 個 `loops`、103 句含片尾；程式比對 [claims.md](claims.md) 103 列與 JSON 103 句，文字完全一致。正文插畫還沒生成。

## 對 R1 HOLD 的逐點改動

| R1 問題 | R2 改動與請覆核的固定原文 |
| --- | --- |
| `atl080` 把總目視五分鐘誤說成斷後五分鐘 | 改為「海面總共只看得見約五分鐘；固定前即斷、立刻沉」，同步 P14、企劃、主張；[Field F9440–9472](https://github.com/GITenberg/The-Story-of-the-Atlantic-Telegraph_34765/blob/6b50b44d3cd2f3f1831e2c1a8fa052f53c51a4cd/34765.txt#L9440-L9472)。 |
| `atl095` 把規律光訊歸給 Dudley | `atl094` 只讓 Dudley 講船上近一刻鐘等待、隨後歡呼；`atl095` 明指 Field **另引《Spectator》** 報導愛爾蘭端反光訊號從亂跳變規律，並把畫面搬到愛爾蘭端；`atl096` 保留兩地可通的結果。P16 和逐句引用拆成 [Dudley F9652–9685](https://github.com/GITenberg/The-Story-of-the-Atlantic-Telegraph_34765/blob/6b50b44d3cd2f3f1831e2c1a8fa052f53c51a4cd/34765.txt#L9652-L9685)、[《Spectator》F9693–9719](https://github.com/GITenberg/The-Story-of-the-Atlantic-Telegraph_34765/blob/6b50b44d3cd2f3f1831e2c1a8fa052f53c51a4cd/34765.txt#L9693-L9719)。 |
| P10 把脆線當撈鉤樣本 | P10 及 `atl057` 現明說 Russell 檢查**船上儲放的電纜盤**；鏡頭示意船上線圈，非海底拖鉤樣本；[Russell R4093–4103](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L4093-L4103)。 |
| `atl099` 說「測出」搜尋帶 | 改為「靠航位推估並標定搜尋帶」，主張表註明浮標不是測出海底端頭的儀器；[Russell R3880–3885](https://github.com/GITenberg/The-Atlantic-Telegraph_40948/blob/ba499c6bc32adef8c8a91a306dcb2d54bf7e898d/40948-0.txt#L3880-L3885)、[Field F9331–9365](https://github.com/GITenberg/The-Story-of-the-Atlantic-Telegraph_34765/blob/6b50b44d3cd2f3f1831e2c1a8fa052f53c51a4cd/34765.txt#L9331-L9365)。 |
| 插畫提示詞可能畫錯儀器、提早看見海底線、增加無據道具 | `atl003/029/096` 改空白刻度與鏡面反光點；`atl076` 只畫抓鉤繩入不透明海面，舊電纜直到 `atl077` 才能看見；`atl024` 刪證物托盤，保留原文有的線材與工作桌。文字表逐景記下這些界線。原生圖尚未畫出，須在試畫時再看。 |

## 時長與門檻

本機 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs script --slug curio-s48` 重生 R2 腳本；`lint --slug curio-s48 --json` 為 **0 errors／0 warnings**。`npm run check:tasks` 通過（舊任務有既存警告）。`estimateTimeline` 含每句預設停頓、**非語音實長**：

| 語速（單位／分鐘） | 30–60 秒濃縮 | 不含片頭／片尾正文 | 片尾三句 | 全部旁白 |
| --- | ---: | ---: | ---: | ---: |
| 250 | 55.4 秒 | 10:48.9 | 16.3 秒 | 12:00.7 |
| 300 | 47.4 秒 | 9:15.0 | 14.0 秒 | 10:16.4 |
| 325 | 44.5 秒 | 8:40.6 | 13.2 秒 | 9:38.3 |

即使以 325 推算，正文多於八分鐘約 41 秒；真正門檻須按合成語音再量。原創 5 秒片頭要接在濃縮後；正片後計畫共用 21 秒 `v4-endscreen`，末約 16 秒放兩個推薦框與訂閱圈。**動畫、語音、插畫、配樂、片尾、組片和可點連結都尚未製作或核准**；推薦／訂閱連結需實際私人上傳後在 YouTube Studio 設定與點測。

下一步是**另一位審稿人**以本表的 R2 五檔 SHA 對 R1 HOLD 項目做獨立來源及文字畫面差分；若通過，再由兩名未看過本檔與彼此答案的新讀者各自按官方題目盲讀。任何再改字都須重生劇本、主張表、雜湊及相關審核。獨立審核、站台 A 案與劇本核准、TTS 音檢、MiniMax 原生試畫和付費門檻都還待後續處理。
