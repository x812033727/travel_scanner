# S53 R11｜三景成年與時代線索，作者定稿

2026-10-22 UTC。依 [R10 非付費預檢](r10-next-art-paper-preflight.md)，我只修 `s53001`、`s53003`、`s53010` 的 `data.prompt`，使 1907 年小屋與 1906 年火災兩段的主體明確為成年人物、衣著符合時代，且各景只有一個動作。這是**作者候選**；尚非獨立史料／畫面 PASS，也不是原生圖或網站分鏡核准。

[逐字差分](r11-three-prompt-structured-diff.json)列出三個舊／新提示詞。R11 `video.json` SHA-256 為 `df63d7d13d5f440dfbf190bf7c527a99f4eae3ee21aafae6b27aae23d7c253dd`；將三個新字串各換回舊字串，即逐位元恢復 R10 SHA-256 `6e271778492bdcd97e1ffb3ee700e99fe848f0fd8d077bb705a6972b3e29a9f5`。共 124 景，其他 121 景、台詞、運鏡、章界、伏筆、音樂與 `cute-mystery` 預設皆未改。`brief.md`、`research.md`、`claims.md`、`script.md` SHA-256 分別仍為 `8e44f47693dd75ad0a7509ab0f495c06adcc2e614b8c8bc09a51559d7202a27c`、`2e61530c650852281402476041175154ee69c414daf7431d6aa0db352e7c3d22`、`b5be9bbbf8c78cc87c32efcc0964afea1cb689a225b1a216184db750623b5f84`、`64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc`。R10 的 126 句語音文字未改，先前的技術音檢仍指向同文口播；分鏡版本則須重新驗收。

`s53001` 與 `s53003` 的 1907 年六月廣場、仍在原地的小屋，據 1913 年調查回顧；沒有畫成實際搬屋機械，也沒有替匿名人物造姓名。`s53010` 只畫一名年代服飾的居民望向遠方火煙，沒有假造可識別的當事人或傷亡。臉、服裝、姿勢、天光皆為概念插畫，不當原始照片或有據可考的具體場景。另一位審稿者須按固定史料及相鄰台詞覆核這些邊界。

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s53 --json` 退出碼 0，0 error／0 warning。私有 `STOP` 存在；本輪沒有付費圖、judge 或配樂。網站 outline／script／audio 卡、人耳聽審仍待站主，不冒稱完成。

## 委派整集媒體上限

站主已要求按推薦方案繼續而毋須逐項詢問，故本集記錄**圖像、圖像評審與一首配樂合計 US$4.78** 的累計停線。即時 `keyframes --takes 3 --dry-run` 對 116 景報價首輪約 US$1.57、每景最多三次約 US$4.70；`music --dry-run` 對 600 秒配樂報約 US$0.08。私有帳本目前 US$0.00、0 圖、0 judge、0 音樂、0 預留，網站單片 US$200 為伺服器護欄，**不是**本集委派上限。報價或帳本變動若使總額將超過 US$4.78，先保留 STOP 並修訂方案，不再加買。獨立書面核對通過前不啟動付費；之後先每次一景、各一張原生圖，直接看 1280×720 原圖及 judge，再決定是否擴大。
