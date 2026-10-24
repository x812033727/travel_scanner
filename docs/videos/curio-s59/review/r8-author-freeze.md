# S59 R8｜兩處重述窄修，作者凍結

2026-10-21 UTC。**作者預檢完成，等待全新獨立史料／書面畫面覆核與兩位隔離敘事盲讀；付費媒體 HOLD。** [R7 正式合票](r7-merge-policy/summary.md)固定 OR 12／13，唯一未過 no_recap：A 指 s59030 在命名回呼前重說開場的十八美元草圖；B 指 s59078 重說科學院請杜蒙塞爾試的開場動作，卻未接回開場。

| 凍結創作檔 | R8 SHA-256 |
| --- | --- |
| research.md | 39a48f08ca01dfa18009e9c1819684d03b92c52656952affd3266a574d88067d |
| brief.md | 9d68d7b4dad27f56b6dbc53f7890bc0db84590de3e445302f8f4836c286ac1e3 |
| claims.md | aeb0cd64b8ddeb992e70c3daa813f42d475718e707e82e62f0da4a7684d95f95 |
| video.json | f29d9f55dbea7ee52a19e6c885ed36f26f51b30fc7fe0fa4caa87b7ea9d3a33b |
| script.md | f0fd2a6069844fe99e994367f3fa8d27b36928231dc0695fd816762c18faf07b |

[結構化差分](r8-author-structured-diff.json) SHA-256 eef493356abffbb34927bb8f7d6a1f5e7537c5e34b7ee0036ac7a9647b13bcde。四個 video.json 葉節點與四個逐句表台詞欄逆換後，R7 的 video、claims 和工具生成 script 原始 SHA 均精確復原；research、brief、所有 prompt、所有卡片資料不變。visualHash 仍為 3e39a4b9868072e1；narrativeHash 從 f20dc827b7998950 改為 755facc75e73fc89。

作者只改 s59030、s59033、s59078、s59080：

- s59030 先以「還記得開場那張十八美元的草圖嗎？」明確接回開場，才說愛迪生畫下小機器；s59033 讓克呂西照圖做出原型，去掉第二次「開場那張」。
- s59078 先點名「開場輪到杜蒙塞爾」的換人測試，再提出如果新操作者也讓機器說話，腹語疑問會少一層；s59080 直接交代初試沒有做出剛才的效果，不再重述換人動作。
- 四句仍維持 [E5220–5241](https://github.com/GITenberg/Edison--His-Life-and-Inventions_820/blob/b100fab326616897d87d7e296672f5f916624d32/820.txt#L5220-L5241) 的愛迪生晚年自述與 [D7012–7018](https://github.com/GITenberg/Le-T-l-phone-le-Microphone-et-le-Phonographe_27574/blob/825f6fa891c8a23d957829a717c37a6af1dea2ae/27574-8.txt#L7012-L7018) 的杜蒙塞爾轉引來信層級；R7 書面畫面未改。這是作者的對源判斷，仍須另一位獨立覆核。

script CLI 重生 script.md，110 句、100 張 shot、10 張 big、12 組伏筆；正文扣除開場九句與末兩句為 2,627 漢字，以每分鐘 325 漢字最快估算 8.08 分鐘，全片工具估 13.37 分鐘。lint 0 error／0 warning，docs-video tests 236／236，check:tasks exit 0（既存長期認領警告）。這些是形式與作者檢查，不能代替新盲讀票。任何 R7 來源或敘事票都不能移作 R8 核准，站台旁白、圖片與成片關卡也尚未執行；沒有付費呼叫。
