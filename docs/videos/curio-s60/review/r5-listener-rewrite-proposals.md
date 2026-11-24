# S60 R5｜持續音訊旗標的聽眾措辭提案

2026-10-22 UTC。依 `youtube-video/references/prompts/listener-rewrite.md` 準備，**僅提案，未套用**。第三／最後一次原措辭重錄仍在執行；協調者應只挑最終仍被標示、且需實質修正的句子。這份表不是配音通過、聽過原音或授權記錄。審者只讀既有 Jev `intended/heard` 與固定原文；第二套 ASR 模型下載受阻也不構成覆蓋既有旗標的證據。

所有專名與數字、日期保持原拼法；人名誤聽不以改名解決。未改 `video.json`、`script.md`、`claims.md`、發音字典或任何媒體。現行 video SHA-256 `c0a474072ffa37604dfe2acb9a46f600cac37c9815da5b4b692e213f560fd8ac`，script `f09ce432bfdec71135e44bc9ed3ad6f48119e95e01b2acd318fda13f8bda9dd1`，claims `3a1bc97deb2be249b4b5fe2a90fd51f0d4ac8625c2e5fbc73a02e921276d6a88`。旗標來源 `r4-redo1-audio-check/check-flags.json` SHA `c5b86e27eedebd615c80c426e9a56b11e5fecf4612f737e337438e097b8a1a9d`、`check.json` SHA `d7ed6c67051ab2c62d2242a25df397b0fa18097ebda1bfc7a565e726f68f32dd`；14 個 ID 與本表一致。

| ID | 原句 → 候選 | 原因與保留界線 | claims 固定錨點 |
| --- | --- | --- | --- |
| `s60014` | 可是出發當天，橇旁的雪面突然開成深裂縫；這條路還能走嗎？<br>→ 可是出發當天，雪橇旁邊的雪面突然開成深裂縫；這條路還能走嗎？ | 單字「橇」被轉寫成橋；補成雪橇並加旁邊，不改裂縫與懸念。 | [P02](https://github.com/GITenberg/The-South-Pole--an-account-of-the-Norwegian-Antarctic-expedition-in-the--Fram---1910-12---Volu__4229/blob/242036c254a5ff483c59e5dc4c66a97f4486f70c/4229.txt#L10065-L10083) |
| `s60015` | 他們只差一小段距離，就可能連人帶橇落下。<br>→ 他們只差一小段距離，就可能連人帶雪橇一起掉下去。 | 連人帶橇被轉寫成橋；雪橇及掉下去較口語，保留只是可能落下。 | [P02](https://github.com/GITenberg/The-South-Pole--an-account-of-the-Norwegian-Antarctic-expedition-in-the--Fram---1910-12---Volu__4229/blob/242036c254a5ff483c59e5dc4c66a97f4486f70c/4229.txt#L10065-L10083) |
| `s60019` | 布亞蘭德抓住牽繩，狗把腳爪深深抵在雪裡。<br>→ 布亞蘭德緊抓拉雪橇的繩子，狗把腳爪深深抵在雪裡。 | 牽繩被轉寫成韁繩，未必代表聽感實錯；若第三次仍有實質誤聽，明說拉雪橇的繩子，對應 trace。 | [P02](https://github.com/GITenberg/The-South-Pole--an-account-of-the-Norwegian-Antarctic-expedition-in-the--Fram---1910-12---Volu__4229/blob/242036c254a5ff483c59e5dc4c66a97f4486f70c/4229.txt#L10180-L10250) |
| `s60028` | 舊冰川有張開的裂縫，隊員在可通行的線上架雪標。<br>→ 這片老冰川上有寬大的裂縫，隊員沿著能走的路堆起雪標。 | 舊／這不穩，改老冰川並用沿著能走的路；保留老冰川、寬裂縫及標記安全線，不增加新裂縫。 | [P03](https://github.com/GITenberg/The-South-Pole--an-account-of-the-Norwegian-Antarctic-expedition-in-the--Fram---1910-12---Volu__4229/blob/242036c254a5ff483c59e5dc4c66a97f4486f70c/4229.txt#L10948-L10979) |
| `s60029` | 那些雪標不是裝飾，返程能用它們繞開裂縫。<br>→ 那些雪標不是裝飾，回來時能靠它們避開裂縫。 | 返程被寫成凡程；改回來時，保留回程用途與避開裂縫。 | [P03](https://github.com/GITenberg/The-South-Pole--an-account-of-the-Norwegian-Antarctic-expedition-in-the--Fram---1910-12---Volu__4229/blob/242036c254a5ff483c59e5dc4c66a97f4486f70c/4229.txt#L10948-L10979) |
| `s60031` | 等上高原，前方連山形也不見了；他們還能朝哪裡走？<br>→ 到了高原，前方連山形也不見了；他們還能朝哪裡走？ | 等上／登上語音近似且含義相近，不宜據此宣稱唸錯；候選到了高原讓時點更清楚，問句不變。 | [P04](https://github.com/GITenberg/The-South-Pole--an-account-of-the-Norwegian-Antarctic-expedition-in-the--Fram---1910-12---Volu__4229/blob/242036c254a5ff483c59e5dc4c66a97f4486f70c/4229.txt#L12453-L12520) |
| `s60034` | 漢森讓自己的狗先走，一手護橇，一面盯指南針。<br>→ 漢森讓自己的狗走在前頭，一手扶著雪橇，一面看指南針。 | 護橇被轉寫成護鞘；扶著雪橇更清楚，漢森姓名保留。 | [P04](https://github.com/GITenberg/The-South-Pole--an-account-of-the-Norwegian-Antarctic-expedition-in-the--Fram---1910-12---Volu__4229/blob/242036c254a5ff483c59e5dc4c66a97f4486f70c/4229.txt#L12453-L12520) |
| `s60043` | 那天下午三點，駕橇的人一起喊停。<br>→ 就在那天下午三點，駕著雪橇的人同時喊停。 | 那天被轉寫成每天且駕橇成架橋；加就在並寫駕著雪橇，保留三點及同時喊停。 | [P05](https://github.com/GITenberg/The-South-Pole--an-account-of-the-Norwegian-Antarctic-expedition-in-the--Fram---1910-12---Volu__4229/blob/242036c254a5ff483c59e5dc4c66a97f4486f70c/4229.txt#L12754-L12811) |
| `s60058` | 這些外走路線替他們圈住一片區域，卻仍想靠得更近。<br>→ 往不同方向走過一趟後，他們已圈住一片區域，卻還想靠得更近。 | 外走路線拗口且被改成外圍；改直接描述分向走過，沒有聲稱沿圓周繞一整圈。 | [P06](https://github.com/GITenberg/The-South-Pole--an-account-of-the-Norwegian-Antarctic-expedition-in-the--Fram---1910-12---Volu__4229/blob/242036c254a5ff483c59e5dc4c66a97f4486f70c/4229.txt#L12862-L13012) |
| `s60061` | 十二月十六日，布亞蘭德走在新路最前面。<br>→ 十二月十六日，走在新路最前面的，是布亞蘭德。 | 名字被縮成布朗德；姓名完全不改，只移到句末並隔出短停頓。 | [P07](https://github.com/GITenberg/The-South-Pole--an-account-of-the-Norwegian-Antarctic-expedition-in-the--Fram---1910-12---Volu__4229/blob/242036c254a5ff483c59e5dc4c66a97f4486f70c/4229.txt#L12991-L13061) |
| `s60063` | 上午到新位置後，他們架起帳篷，也在雪上堆起觀測平台。<br>→ 上午到達新的位置後，他們搭起帳篷，也用雪堆出觀測平台。 | 新位置後被黏成新位之後；到達新的位置避免黏連，帳篷與平台仍並列，不虛構先後。 | [P07](https://github.com/GITenberg/The-South-Pole--an-account-of-the-Norwegian-Antarctic-expedition-in-the--Fram---1910-12---Volu__4229/blob/242036c254a5ff483c59e5dc4c66a97f4486f70c/4229.txt#L12991-L13061) |
| `s60070` | 漢森和布亞蘭德又向預測的南方外走；這樣仍要留下什麼？<br>→ 漢森和布亞蘭德又朝推定的南方走去；他們還得留下什麼？ | 外走被聽成歪走；改朝推定南方走去，兩個姓名及後半鉤子保留。 | [P07](https://github.com/GITenberg/The-South-Pole--an-account-of-the-Norwegian-Antarctic-expedition-in-the--Fram---1910-12---Volu__4229/blob/242036c254a5ff483c59e5dc4c66a97f4486f70c/4229.txt#L12991-L13061) |
| `s60077` | 他把完成遠征的消息寫進信裡，再放進小帳的袋子。<br>→ 他把完成遠征的消息寫進信裡，再把信放進小帳篷裡的袋子。 | 小帳被轉寫成小張；補為小帳篷裡的袋子，保留信件內容與存放動作。 | [P08](https://github.com/GITenberg/The-South-Pole--an-account-of-the-Norwegian-Antarctic-expedition-in-the--Fram---1910-12---Volu__4229/blob/242036c254a5ff483c59e5dc4c66a97f4486f70c/4229.txt#L13062-L13091) |
| `s60108` | 如果你也想看當事人的原文，兩份固定全文都放在說明欄。<br>→ 如果你也想看當事人的原文，兩份全文的連結都在說明欄。 | 固定全文屬製作措辭且被寫成連結置頂；改兩份全文的連結在說明欄，不聲稱置頂留言有連結。 | 節目說明／互動提問，無新增史實主張 |

## 固定來源與應注意的行錨

我重開 Amundsen 固定全文 `/tmp/s60-verify-amundsen-4229.txt`，SHA-256 `741b12f3e558a172bb03a1904df5479a130fd2208085b45c403911e71fdefe00`，對應 claims 釘住的 GITenberg commit `242036c254a5ff483c59e5dc4c66a97f4486f70c`。P03 原文是外觀很老、像已停止移動的冰川；其大裂縫幾乎填雪，雪標連線用來返程避險，故候選沒有把它們寫成新裂縫。P04 是帶狗前行、扶雪橇同時以指南針導向，不把人物唸成別名。P05 明記那天下午三點 drivers 同喊停，不能改成每天例行。P06 的 encircling 是三個方向外出，作者特別否認沿圓周繞一圈。P07 的位置、觀測平台與朝新找到的子午線方向走出都保留推定性；P08 明記信在帳內小袋，非小帳外或寄出。

**s60019 行錨需要協調者交給來源覆核者處理：**claims 現列 P02 L10180–10250，然而 `seized the trace` 是同一固定文本 L10164–10165，狗爪抓雪是 L10167–10175。既有行錨從前來支援的兩人開始，略晚於本句核心證據。全固定文本支持本句及候選，若套用此句，應以同一固定 commit 擴錨至 L10160–10250（或精確 L10164–10175），再獨立覆核；本提案未自行改 claims。

## 長度與後續關卡

機械按正文排除開場 s60001–008 與末尾 CTA s60108–110 計數：現稿 1966 漢字；若十四候選全採，正文 1999 漢字（淨增 33），以 325 漢字／分鐘估 6.049 → 6.151 分鐘。325 CPM 純漢字估算低於八分鐘，因此不以此速度估算聲稱達標；現有私有 timeline 快照 SHA-256 `ca916c3ac76167cbc4699f8a1a47fcb273b9c6842692b21466c719e15af56974`，按同一排除名單逐景相加為 15916 frames／30 fps＝530.53 秒（8.842 分鐘），現版實際時間軸正文已超過八分鐘。候選沒有刪掉事實或鉤子以縮短；新措辭重錄後仍須重新量測，不能沿用此舊音訊長度當作已達標。只採最終持續旗標的子集時仍需重算時間軸，不能假稱已量測。

套用後需以新雜湊重產 script、同步 claims、跑 lint，並按 curio skill 交全新讀者作敘事盲讀及必要來源／畫面差分覆核，再只重錄實際改動 ID、跑 check-audio。最多兩輪措辭重寫；仍有旗標依流程保留給音訊審核，不把自動轉寫相近或候選表當成站主已聽過。
