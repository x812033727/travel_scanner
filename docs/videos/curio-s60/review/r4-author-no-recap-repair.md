# S60 R4｜片尾重述的作者窄修

**狀態：**R4 作者候選，等待全新獨立盲讀與來源／畫面複核；這份作者記錄不是敘事 PASS、站主核准或媒體製作授權。R3 正式雙讀者 OR 合併通過 12/13 題，唯一共同 FAIL 為 `no_recap`。兩位讀者都指出相鄰 s60106–s60107 重說國王信未獲送達證明。本輪只處理這一處。

**改動：**刪去 s60107「所以能存檔的是留信、找到和收下；送達國王仍待別的證據。」及其對應畫面、claims 列。保留 s60106「他的日記後來被找到；這兩份文本沒有追到國王信的最終送達。」作為唯一清楚的來源邊界。開場 s60008 的「信件證據終點」loop 回收 ID 由 s60107 改為 s60106；接下來直接邀請觀眾查看兩份固定全文。s60101 仍承載史考特收下短箋的日記答案。沒有新增史實主張、改動日期或移動其他旁白；刪去的比較兩本書畫面亦不再留作錯位視覺。`brief.md`、`research.md` 和固定史料沒有修改。

**核對與測試**

- `node tools/video/cli.mjs script --slug curio-s60` 重生逐句稿。109 景旁白與 `script.md`、`claims.md` 逐句對齊，作者程式檢查 109/109；已無 s60107 孤列或 loop 指向。
- `node tools/video/cli.mjs lint --slug curio-s60 --json`：退出 0，**0 errors／0 warnings**；正文估算 10.618 分鐘、109 句、103 插圖景／6 字卡景／11 loops。第二章從 **00:46** 起，濃縮開場仍為 46 秒。[完整 lint stdout](r4-author-lint.json) SHA-256 `f2cd2415e62428a62397d4f3c0f5b18fabe316c6699af0dc2ba91f8a06572670`。
- [R3→R4 structured diff](r4-author-structured-diff.json) SHA-256 `08808457816ba26d09d082926d2d8721817a634ada1a529e807bf1708d5aacc8` 記錄刪除場景完整物件、loop 欄位前後值、各檔前後 hash 與完整 unified diff；對三個變動檔逐一做了正向與反向 patch 回放，結果 hash 相符。R3 正式合併輸入 SHA-256 `ca1ec671fa19d0142d0a2a34c3d5b8cc8f234fa24aaffeaae7a2e1e7b91b124e`。

| 檔案 | R3 SHA-256 | R4 SHA-256 |
| --- | --- | --- |
| `brief.md` | `f177fe4e14067efb7cc8b6d0d1b817343c38ce5343271383ae8f9f7a48d4c8e1` | `f177fe4e14067efb7cc8b6d0d1b817343c38ce5343271383ae8f9f7a48d4c8e1` |
| `research.md` | `e4ec4ac5abb2628d8c3efcabcf3a5beb8f33c5d2ce3ab92113e473a6bebd7689` | `e4ec4ac5abb2628d8c3efcabcf3a5beb8f33c5d2ce3ab92113e473a6bebd7689` |
| `claims.md` | `23cc2d361374c54eb2e8c8270771c793dfa6772be99d88e14c4cc027c3eb22a0` | `3a1bc97deb2be249b4b5fe2a90fd51f0d4ac8625c2e5fbc73a02e921276d6a88` |
| `script.md` | `50645fb31eda1b456521dae764d9d12e4ee47ee3efef18daba6fb6059e6000bc` | `f09ce432bfdec71135e44bc9ed3ad6f48119e95e01b2acd318fda13f8bda9dd1` |
| `video.json` | `93dfbedac1ae0e761d79802d6e7066811d9cf6cbb199ab80eb71d6d502d360c3` | `c0a474072ffa37604dfe2acb9a46f600cac37c9815da5b4b692e213f560fd8ac` |

**後續關卡：**R4 交由未見作者修稿的新讀者獨立回答十三題，並由獨立工作者核查來源與畫面。沒有呼叫 TTS、插圖、配樂、PR、推審或 `approve`；STOP 與既有核准狀態未動。
