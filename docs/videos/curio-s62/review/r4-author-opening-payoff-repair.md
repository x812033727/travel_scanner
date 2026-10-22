# S62 R4｜作者開頭與回收定稿

2026-10-22 UTC。**作者候選；R4 尚待獨立史料／書面畫面覆核及兩位全新正式盲讀，不可用於付費媒體。** R3 [獨立史料覆核](r3-independent-source-visual.md)通過，但[兩位正式盲讀合併](r3-formal-merge-audit.md)只得 9／13；共同未通過 `no_spoiler`、`payoffs`、`no_recap`、`no_detour`。本輪只修這四處。

## 有根據的定點修改

- s62005 把開場預告「更少點」改成十日晴夜隊形的問句；s62043–44 才揭示十日只見兩點且位於東側。
- s62006 指明十七日問題是「一點稍晚從另一點近旁顯出」；s62075–76 以原書的「我想兩點先前相接」回答。s62008 改問首夜三點是否全部，s62059 首次四點同時可見；s62062、s62084 清楚保留原書無法反推首夜少見哪一點、為何當晚沒分出的界線。十日遮擋與十七日貼近是作者各夜猜測，沒有移植成首夜確定機制。
- s62031 改回原書所見的黃道平行；s62061 改為十三日東西側角距，刪去兩句純計數重述。s62112 改成作者邀別的天文學家以準確鏡筒續算周期，來源新增 G15 [原書英譯 L1258–1265](https://github.com/GITenberg/The-Sidereal-Messenger-of-Galileo-Galilei--13-and-a-Part-of-the-Preface-to-Kepler-s-Dioptrics__46036/blob/6672b6c62a0f30e9bb9b84410ef48c6698c37ea5/46036-0.txt#L1258-L1265)；唯一固定 1880 年 Carlos 英譯連結仍在說明欄和研究表，從口播收尾移除。

## 可逆差分、綁定雜湊

[結構化 JSON 差分](r4-author-structured-diff.json)完整列出 R3→R4 的 **14 個** `video.json` leaf before／after；已以程式逐項正向套用、反向還原，確認與兩版 JSON 完全相等。[文字 unified patch](r4-author-text-diff.patch)涵蓋 `brief.md`、`research.md`、`script.md`、`claims.md`；在 R4 工作樹以 `git apply -R --check` 驗證可反向套用。

| 檔案 | R3 SHA-256 | R4 SHA-256 |
| --- | --- | --- |
| `brief.md` | `3351f74d2d1df831f63eae41f3c243cc27e507f6d6853247178f056f349ea382` | `9f63e8de4d158b2e4bdbfcc86579463274966d88bb548318e6bc4200615f4337` |
| `research.md` | `fc83424c3a0def641449cd17ad50b7d854412d70ad15de0afaf9fad30cd74795` | `442cbe52e4c92f962726f4940e182bd10bedb41417cb239ede9daf008c5ea74a` |
| `video.json` | `396e78030054ee6f8a4dca15c83be8e4361dd6530bb1c8b99e75cdb3e2922ebf` | `abed73ef3b14dcfc1b8ff1804f0234919d2f03cffa70a0b4c901a72ce6b14f92` |
| `script.md` | `e8f1179f11184dea4eedabddc30f6820305e2c0ef709f061b26484961d622110` | `8343a4f903fe4b405b1e6364cd67737ed7f3aead625b5fe713bf91c873c05c14` |
| `claims.md` | `2f57e934e6f85febcd7aea7080d2c188141d7000cf40cd8c2c41d5dbf4cca550` | `2edb12dd02afa0ed03744616fcb27e889498356709d4c1cf95be415c30914218` |
| `r4-author-structured-diff.json` | — | `6eb88e61d8e7220dc559302cf6b3e663fe7d392c0cb5cab9c3785fa0d7363164` |
| `r4-author-text-diff.patch` | — | `1a5d445208a789ab38e5a6a8d89362cd7678181953fbd6167e7613577f19aaec` |

固定 Carlos 英譯原始文字 SHA-256 仍為 `74fc9b817b64bc33415c6a44100c30f48952bc531d380682e5f4f1a26cc56fb5`。`script.md` 由官方 CLI 重產，`narrative_hash` **`dc5b230a7d70f26b`**，`speech_hash` **`6502097f52b320e8`**。

## 作者端驗證與交接

官方 `lint --slug curio-s62 --json`：**0 error、0 warning**；114 句與 114／114 同字主張列，每句都有固定原文行錨；110 張不重複原創插圖提示、4 張資訊卡、最多連續一張卡、7 章、13 組 setup／payoff。固定 5 秒片頭在濃縮開場後；21 秒片尾末 16 秒規劃 Studio 真正可點元素。以官方 `estimateTimeline`：250 CPM 開場 **47.47 秒**、正文 **10.244 分鐘**；較快 325 CPM 開場 **38.37 秒**、正文 **8.301 分鐘**。開場、片頭、片尾均不併入正文八分鐘門檻。正式 TTS 時長仍須另測。

`npm run check:tasks` exit 0，`git diff --check` exit 0；任務檢查顯示既有其他工作者的佔用／範圍警示，未由本輪造成。沒有 TTS、插圖、配樂、渲染、上傳、付款或虛構影片 ID。請新的獨立來源／畫面覆核者和兩位只讀同一 R4 劇本的正式盲讀者重驗；R3 的兩張票不延用。
