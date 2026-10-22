# S53 R35｜`s53028` 九月十日來源卡獨立書面覆核

2026-10-22 UTC。**PASS，僅限此版 `s53028` 日期來源卡及對應 claims 註記。**我未參與 R35 作者修稿；本次只讀史料、R34 Git 版、現稿與私有狀態。沒有重綁圖單、製作媒體、付費呼叫或更動其他檔案。

## 固定史料與字卡

固定 1913 年 *San Francisco Relief Survey* 原文 `/tmp/s53-sf-relief/56217-0.txt` SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`。[D L4858–4864](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4858-L4864)先說建小屋取代帳棚、**1906 年** 8 月 1 日公布計畫並發包，接著原文是 `Building began September 10`；下一句說 9 月 16 日漢密爾頓廣場完成 20 棟。原書版權頁亦明記 1913 年。故主文「9 月 10 日，小屋開始興建」是該施工脈絡的合理意譯；上標「1906 年｜舊金山」補足原句省略的年份與地點，下標「1913 年《舊金山救濟調查》｜英語原文意譯」清楚區分事件年份與後出調查年份。下景 `s53029` 才講 9 月 16 日完成 20 棟，沒有混淆日期。卡片沒有施工人物、工具、工位、房型或偽造的 1906 年公文／現場圖像；一個日期事實也符合 Curio 來源卡用途。

## R34 → R35 精確範圍

我直接從 R34 Git commit `734bdbb3aaf49bb4018e3da1bd6df7d61a019079` 讀取舊檔，未用作者收據代替比對：

| 檔案 | R34 Git SHA-256 | R35 現行 SHA-256 |
| --- | --- | --- |
| `video.json` | `f98955b261259a0f687e409a043afe910fe7e9c38a7630e2b5a2d665ebda4997` | `dc3bfba35e527d0206a56e78c5784fd8eab7d5fe38c97c59d233280e7861df79` |
| `claims.md` | `0197cf312874d34cc31895dee05993275357bceac6d81b951fa73334a78841d0` | `85eb3ce65fbef3746cd30a311d9af067968b32e5f5152a9c8c24e53d0a1200f9` |
| `script.md` | `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc` | `64ffcd8c0e89c4596a7fd08d41bd74f8a16f55fbc9acc2f41d7f9b914ea300fc` |

`review/r35-s53028-source-card-structured-diff.json` SHA-256 `32355bff297359eea0cf52d88a2abb92c791705cc19636274c80645bad00618a`。124 景中僅 `scenes[21]` 由 `shot` 換成 `big`；該景舊／新完整物件與差分逐值相符，其餘 123 景相同。`claims.md` 132 行僅第 28 行 `s53028` 改動，舊／新整行也與差分相符。把差分的 `before` 場景放回現稿並依現有 JSON 格式序列化，逐位元組重現 R34 `video.json`；把 claims 新行反填舊行，亦逐位元組重現 R34 `claims.md`。126／126 句口播 ID 與文字完全相同；現稿 `speechHash=05c4d9a79a8708b4`，私人 `timeline.json` SHA-256 `c75c8bde15f7220862ba8083d6590b7b14bb71c456f896f7b58c13352c88a054`、`narration.wav` SHA-256 `08444d50c2f8b70a7079701e157397d9a7c23d08971727164df91a1101e281e1`。

我重新計算現稿 `visualHash=76b75a45d888af0b`。正文 123 景有 **112 個 `shot`，91.1%**，高於系列 70% 下限；`s53028` 兩側 `s53027`、`s53029` 均是 `shot`，全片卡片最長連續 **1 張**，低於最多 3 張。實跑 `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s53 --json`：exit 0，**0 errors／0 warnings／126 lines**。

## 私有圖單與停線

只讀重算有效 `keyframes/manifest.json` SHA-256 `591f027333b3f7cd9aec89fbfc2d3400d80bfa95ffdec3e5153ea47e5d1935c9`，仍綁 R34 `visual_hash=4d419236d18aa61f`；18 筆 KEEP 的所選實檔 SHA 全部吻合，沒有 `s53028`，尚未綁 R35。`media/ledger.json` SHA-256 `63af8309a74c3b4348ebb8e534c66910e383e3afbe8c2da386341aa478a18e41`；逐筆合計 **US$0.6345／48 image／47 judge／0 預約**，其中 `s53028` 已有三次 image 與三次 judge。`media/jobs.json` SHA-256 `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3`，`jobs={}`；`STOP` 在位。R34 第三／最後原圖已有獨立 HUMAN REJECT，故本卡片不借用該圖，也不開第四張。

**判定範圍到 R35 書面卡片為止。**R35 圖單回綁、任何下一景媒體、全片／網站關卡與發布均未在本次驗收。
