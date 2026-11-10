# S60 R3｜四項敘事失敗的作者窄修

**狀態：**R3 作者候選，等待全新獨立盲讀與來源／畫面複核；這份作者票不是 PASS、站主核准或媒體製作授權。R2 兩位讀者的正式 OR 合併有 9/13 題通過，四個共同 FAIL 是 `no_spoiler`、`chapters_link`、`payoffs`、`no_recap`。本輪只修這四類問題，未動固定史料、片尾、配樂或媒體狀態。

| R2 失敗 | R3 作者修改 | 來源界線 |
| --- | --- | --- |
| `no_spoiler` | s60001–03 的 1 月 18 日濃縮場景只讓史考特隊伍遠望、走近小帳，停在未揭帳門；s60002 字卡刪去「五個名字」，s60003 畫面刪去拆讀短箋。s60006 把精確極點改成待解的問句。名單、轉寄請求、測位限制留在後文揭曉。首章章名與 `brief.md` A 案同步。 | 史考特固定日記 P11 先記遠處似石堆或帳篷，再記抵達、名單與短箋；開場不演出讀箋結果。阿蒙森 P08 記帳門離開前綁好；門前停格是示意，不冒充日記逐字動作。 |
| `chapters_link` | s60060 不再提前說抵達第二營，改問新路由誰帶直；s60061 立即以布亞蘭德領路回答。s60075 問為何不帶國王信，s60076 首句便引阿蒙森書中返程風險作答；`loops` 的回收 ID 同步改到 s60061／s60076。s60075–78 的畫面照拿信、望回程、放信的順序整理。 | 阿蒙森 P07 記 12 月 16 日布亞蘭德領前、阿蒙森在後查方向，稍後才到新位置；P08 明說回程長，恐不能親自報告。 |
| `payoffs` | s60055 改問三人沒有合用的隨身指南針，能否找回小帳；s60057 現有「三人都回營」便直接回答。s60055 畫面移除已被風雪蓋掉的腳印。 | 阿蒙森 P06 記指南針太重不便攜帶、太陽與腳印可能幫忙，也只確認三人回來；沒有指定每人實際採用何種返航方法，R3 不編造。 |
| `no_recap` | s60051 留下首次午夜觀測能否定位置的問題，刪掉第二次太陽高度原理；s60066 改成 P07 的薄雲下太陽可見、高度看似停住又跳動，畫面也改成薄雲觀測。s60073–77 收成「袋子 → 給國王的信 → 為何不帶 → 返程理由 → 報告內容與放信」，去掉 s60074／75 重複問同件事。 | P06 說首次午夜讀值不足以作最終定位；P07 直接記薄雲擾動和全天觀測；P08 記國王信與留信原因。 |

**核對與測試**

- 固定 A 全文 SHA-256 `741b12f3e558a172bb03a1904df5479a130fd2208085b45c403911e71fdefe00`，固定 S 全文 `ddf48b1e0fc296b4862bad161bada2797a964ac6e6c7a0a7306a0a73940f8b26`，本地重算相同；`research.md` 沒變。
- `node tools/video/cli.mjs script --slug curio-s60` 重生逐句稿；110 景的 `video.json` 旁白逐句與 `script.md`、`claims.md` 對齊，作者程式檢查 110/110。
- `node tools/video/cli.mjs lint --slug curio-s60 --json`：退出 0，**0 errors／0 warnings**；正文估算 10.731 分鐘、110 句、104 插圖景／6 卡／11 loops；第二章從 **00:46** 起，故濃縮開場 46 秒。完整 stdout 見 [R3 lint](r3-author-lint.json)，SHA-256 `606f1632cea731d25d4c89de2bd55431e65e60a5df6796d68586ffd5d56532da`。
- 逐欄位與逐檔完整 unified diff 見 [R2→R3 structured diff](r3-author-structured-diff.json)，SHA-256 `6625a4c06d8fd130a25511d77f987a9ba4950fd2349454c90003bc334951981b`。R2 正式合併輸入 SHA-256 `fd9c0aba4f14eedcd1106446a99b6eab5c7b2981807d447c8bc5346fd54372f6`。

| 檔案 | R2 SHA-256 | R3 SHA-256 |
| --- | --- | --- |
| `brief.md` | `357f2c2706bd1fca6c77e9ccad45771a745ddadc91ba41da4d73f656ab2c5acc` | `f177fe4e14067efb7cc8b6d0d1b817343c38ce5343271383ae8f9f7a48d4c8e1` |
| `research.md` | `e4ec4ac5abb2628d8c3efcabcf3a5beb8f33c5d2ce3ab92113e473a6bebd7689` | `e4ec4ac5abb2628d8c3efcabcf3a5beb8f33c5d2ce3ab92113e473a6bebd7689` |
| `claims.md` | `4d7bd1388b9382219623bb9ce454677edd2eca6415c05ec4ccb0bbbf59421909` | `23cc2d361374c54eb2e8c8270771c793dfa6772be99d88e14c4cc027c3eb22a0` |
| `script.md` | `1ac4ee6548edae5a61f507c4e99edd75f5a81668d9acfa418b0ec22de8ea8b91` | `50645fb31eda1b456521dae764d9d12e4ee47ee3efef18daba6fb6059e6000bc` |
| `video.json` | `bf8d95565857f0a8b976ef6f2d89e730fd88fabcab44201e75a05bd67dabba9c` | `93dfbedac1ae0e761d79802d6e7066811d9cf6cbb199ab80eb71d6d502d360c3` |

**後續關卡：**R3 需要未見本輪修稿的新讀者獨立回答十三題，另由獨立工作者核查新句與新畫面。沒有呼叫 TTS、插圖、配樂、PR、推審或 `approve`；STOP 與既有核准狀態未動。
