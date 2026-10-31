# S53 R9｜固定來源與書面畫面獨立差分覆核

2026-10-20 UTC。**PASS**，僅限 R9 精確稿的來源、逐句主張及書面畫面；敘事盲評、語音與實際圖片須另驗。我未撰寫 R9 稿件。

| 檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `8e44f47693dd75ad0a7509ab0f495c06adcc2e614b8c8bc09a51559d7202a27c` |
| `research.md` | `2e61530c650852281402476041175154ee69c414daf7431d6aa0db352e7c3d22` |
| `claims.md` | `11f814d0f01ddeb7ec0d1a705d1f7c30b55506a512919249bf70eaae099c692f` |
| `video.json` | `7dec1a984c326ae9c44860b14993fbe6c1d1e606368e80594968c9e2194862f1` |
| `script.md` | `dd5a82bbe3a036210ad03a2125e049f9d370a4119dabff746fe0150ee240345e` |

我重新下載 `research.md` 指定的 [1913 年 *San Francisco Relief Survey* 固定版本](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt)，原文位元組 SHA-256 `d627ed287d8a93b9c00225ea47dbdc4f97c36089a890192a602b993c3c185b72`，與研究檔及先前獨立覆核相同。

| R8→R9 差分 | 獨立結論 |
| --- | --- |
| `s53003` | 原文 [L4972–4985](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4972-L4985) 說符合條件的住戶可自費搬走其房屋；「有住戶要帶走的，是自己住的整棟小屋」不聲稱所有人成功搬走，也不暗示已知搬運機具。畫面是匿名公園工作者指向小屋，沒有冒充保存的照片。 |
| 刪 `s53041` | 原句重提找地；`s53040` 的公地期限接 `s53042` 的剩餘時間問題，`s53043` 隨即回答，刪句不抹去來源事實。找地條件由未改的 `s53068→s53069` 首次完整說出，並與原文 [L4972–4985](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4972-L4985) 一致。 |
| `s53093→s53094a` | 原文 [L4998–5011](https://github.com/GITenberg/San-Francisco-Relief-Survey-the-organization-and-methods-of-relief-used-after-the-earthquake-__56217/blob/dabb1ee570c9d5d5992d7eda7aafe215ce025567/56217-0.txt#L4998-L5011) 明記地產公司申請成批收購，部門拒絕，理由是避免延續營地生活；新版提案、提問、回覆三句順序及歸屬正確。`s53093` 匿名地產商遞出**無字概念提案**，沒有把插畫當存世史料。 |

與已追蹤 R8 版直接比較，`claims.md` 僅上述列更替／刪除；`video.json` 僅相同 scene 台詞、`s53093` 概念提示詞及刪景；`script.md` 對應台詞與刪景後的序號重編。`brief.md`、`research.md` 未改；其餘部分沿用 [R8 獨立來源覆核](r8-source-independent.md)。逐列程式對比目前 126 個 `video.json` 口播 ID／字串與 126 個 `claims.md` 列完全一致，沒有重複 ID 或殘留 `s53041`。`lint --slug curio-s53 --json` 為 **0 errors、1 narrative warning**；警告是三個不同 1908 年事件重述年份，與本次來源差分無關。結論不代替 R9 的獨立敘事雙盲。
