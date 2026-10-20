# S53 R10｜章節銜接與重述修訂，作者五檔凍結

2026-10-20 UTC。[R9 隔離雙盲合併](r9-isolated-merge.md)對 `chapters_link`、`no_recap` 判 **HOLD**。本版只修兩處跨章提問與重複的日期、訪查鋪陳；R9 的[獨立來源 PASS](r9-source-independent.md)及所有 R9 盲評、合併檔案保持不變。這是作者候選稿，**不宣告 R10 獨立史料或敘事 PASS**。

## 精確五檔 SHA-256

| 凍結輸入 | R10 SHA-256 |
| --- | --- |
| [brief.md](../brief.md) | `8e44f47693dd75ad0a7509ab0f495c06adcc2e614b8c8bc09a51559d7202a27c` |
| [research.md](../research.md) | `2e61530c650852281402476041175154ee69c414daf7431d6aa0db352e7c3d22` |
| [claims.md](../claims.md) | `b5be9bbbf8c78cc87c32efcc0964afea1cb689a225b1a216184db750623b5f84` |
| [video.json](../video.json) | `6e271778492bdcd97e1ffb3ee700e99fe848f0fd8d077bb705a6972b3e29a9f5` |
| [script.md](../script.md)（CLI 重生） | `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc` |

## R9→R10 精確改動

只改八列旁白／主張：`s53043`、`s53083`、`s53099`、`s53100`、`s53101`、`s53102`、`s53103`、`s53104`；其中六條插圖提示詞隨新口播更新：`s53083`、`s53099`、`s53100`、`s53101`、`s53103`、`s53104`。`video.json` 另改兩個 loop：`s53083→s53084` 直接回收「搬出多少棟」；`s53100→s53101` 直接回收「訪查先拿什麼線索」。其餘 scene、卡片、`loops`、配樂、美術、開場與片尾未改。`brief.md`、`research.md` 完全保留 R9 hash。

| 位置 | 作者修訂及固定來源 |
| --- | --- |
| `s53038`／`s53043` | `s53038` 仍唯一報出 **1907-03-19** 完工日；`s53043` 不再重說該日期，只回答剩下「不到五個月」，並指出建屋已耗掉公地一年期限的大半。這是 [R L10450–10460](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10450-L10460) 的完工日與 [R L4934–4941](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4934-L4941) 的 1906-08-17 起一年期限的日期對照。 |
| `s53083→s53084` | 章末改問各官方營地**共搬出多少棟**，下一章首句的 5,343 棟統計卡直接回答。[R L4998–5001](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4998-L5001)。原 `s53086` 仍往前交代市內各區及周邊城鎮，不再被錯用為章首數字的 payoff。`s53083` 的無字小屋計數示意換掉舊 1907 年地塊地圖，避免時序倒退。 |
| `s53099→s53104` | `s53099` 改說部分小屋**數度易主**，是 [R L10502–10504](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10502-L10504) 新事實，不再預先講訪查員循地址找人。`s53100` 問最初可憑什麼找，`s53101` 以「開場提過的隔年八月訪查」點名回接 `s53008`，並**首次**說明循搬屋時留下的地址尋訪；[R L10194–10197](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10194-L10197)、[R L10502–10505](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L10502-L10505)。`s53102` 接三個月訪談與旁證，`s53103` 新增 1,137 棟待訪規模，`s53104` 問能取得多少較完整紀錄，`s53105` 才交代 680 份。提示詞改用無字所有權卡、封閉資料夾、地址卡、訪查資料夾等概念示意，不畫真實可讀名冊。 |

`s53082` 的 Lobos Square **1908-06-30** 和 `s53096` 的慈善搬修至 **1908 年六月下旬**保留原句；兩個六月事件及 `s53101` 接回開場的隔年八月，仍按原文先後。搬屋機械及個別家庭沒有被補造。

## 作者自查與下一關

從 R9 作者基線逐項比較：`video.json` 除上述八條口播、六條提示詞、兩個 loop 外無其他差分；`claims.md` 只改八個對應主張列。124 個場景、126 句旁白、16 個 loop，所有端點有效；126 個 `claims.md` ID／文字與 `video.json` 順序逐字一致，`screenplay(doc)` 與 CLI 重生的 `script.md` 位元組一致。`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s53 --json` 為 **0 errors、0 warnings**。

`estimateTimeline` 在 250／325 CPM 下，開場至 `s53010` 為 **49.93／40.53 秒**；排除開場及片尾的正文為 **595.77／485.37 秒**，最快約 **8 分 05 秒**。這是書面估算，實際 TTS 和成片時長尚未測量。另一位工作者須按以上五個 hash 對 R10 差分做獨立來源與書面畫面覆核；兩位未讀本版稿的讀者須各自完成官方 13 題盲評後再按 OR 合併。沒有合成語音、付費插圖、配樂、發布或付費媒體。
