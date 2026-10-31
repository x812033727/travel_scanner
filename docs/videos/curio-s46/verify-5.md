# S46 R3｜原文與書面畫面修補凍結（製作人自查）

2026-10-20 UTC。R2 [獨立覆核](verify-4.md)判史料旁白與書面畫面均 **HOLD**；這份 R3 紀錄是修稿者自查，**不宣稱獨立通過**。R2 的兩類問題均在付費媒體前修補；新劇本與提示詞仍須重新審核。沒有生成語音、圖片、配樂、Short 或成片，沒有網站推送或 Git commit。

## 精確 R3 版本

| 對象 | SHA-256 |
| --- | --- |
| [Blackwell 1895 固定原書](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt)，GITenberg commit `16787df4911754c8e0401d12c896b943768f5d8d` | `b52caf559d763349953fe31101016cfb2d68662f152c28a564b6a6b93cac8ec6` |
| [research.md](research.md) | `99b8903431cb1e8a317513f260c33a5cd0d141aefec54b4c0a5ba205c126055d` |
| [brief.md](brief.md) | `8012cab4d8c574a7b4f90f6e02d0ea1d2a96f63919c2377ac5c35de90bec9262` |
| [claims.md](claims.md) | `b4819dd7fcec82efa2df0946be167abea7b21bfd0f231711923f5e09c2c657a9` |
| [video.json](video.json) | `69d738e99fefc84840858d02e3a5b1aaccd4c77f5826f56d06ebd9d3bd0aa663` |
| [script.md](script.md) | `6db66fc2bc2f671c76d28982162d6c7c304c9722bbde41aed8a67e58c607c918` |

## 對 R2 HOLD 的逐項回應

| R2 問題 | R3 修改與需重核之處 |
| --- | --- |
| `bkw019` 的「他」把 Horner 的建議接成 Jackson 所說 | 明寫「霍納教授另建議她試費城兩所學校」，並在 [P02](research.md) 分清 Jackson 同事反對與 Horner 提議，原文 L1984–1998。 |
| `bkw090–096` 把 Blockley 院方協商寫成正式投票、Gilpin 的支持說太滿 | 改成院內黨派角力；Gilpin **友善接待並提醒**由他這名輝格黨人提案可能遭另兩派反對；Blackwell 分訪派別領頭人、交請願後回憶獲**一致准許住院**。沒有正式表決、選票或各董事逐人態度的旁白／畫面。P12 研究與 `claims.md` 界線同步修正，原文 L2517–2553。 |
| 引文範圍未包住原文事件 | P09 擴到 L2250–2338，涵蓋 `bkw067–068` 城裡注視與校門；P14 加 L2692–2695 的重返 Geneva，`bkw113` 逐景精確連結；`bkw127–128` 改連 L2890–2894 的來訪者與搭車離校。 |
| `bkw102` 在她入院前錯畫 Blackwell | 改畫**一名住院醫師**在 1840 年代病房填不可讀字的床頭卡，接 `bkw103` 的停填；此幕不出現 Blackwell。 |
| 時序性身分標籤錯置 | 申請期改用成年女子／醫學院申請者，登記入校後用醫學生或正在學醫的女子，領文憑後 `bkw127` 改用新畢業醫師。另將訪院畫面移出「學校走廊」，改為濟貧院行政走廊／董事辦公室。 |

仍須把 1895 年自傳中的院長信、學生決議、日記和家書當作**書中轉錄**；「騙局」只是在她晚年回憶中部分學生對**申請**的懷疑。1847 年學生決議寫一致通過，Blockley 醫院請願則只記獲一致准許；兩件事不能互換。

## 本地形式檢查及下個關卡

- `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s46 --json`：**0 errors／0 warnings**。同版 `script` 命令成功產稿，131/131 句與 `claims.md` 一致；逐景角色標籤及上述新行號已機械核對。
- 128 景正文有 123 景書面 `shot`（96.1%）及 5 景資料卡、18 組伏筆回收；濃縮開場 45.37 秒。工具估計開場後、口播片尾前正文 **688.9 秒（11:29）**、全口播約 12:31。正文 2,368 漢字，即以每秒 4.5 字且不計停頓朗讀仍約 **8:46**；正式長度待音軌實測。
- `npm run check:tasks`：2116 張任務票通過（既有跨票警告）。下一關請未參與修稿者對上述五檔精確雜湊重做史料與書面畫面覆核，再讓兩名**全新**讀者各自讀此版旁白並答正式 13 題。R1／R2 的舊盲讀不算此版通過。
