# S55 R7｜三格來源錨點獨立差分覆核

2026-10-20 UTC。**R6 的逐句主張表窄 HOLD 解除：三格錨點 PASS。** 這份裁決只核 `claims.md` 三處引用補齊；R6 已獨立通過的旁白史實與書面畫面未變。全新雙盲敘事、實際配音、生成插圖、站台審核與成片仍各自待驗。

| 現版檔案 | SHA-256 |
| --- | --- |
| `research.md` | `b30ea8f4021ebb27fc2f2b8f63c633e4dde00c5fcb52241daa3aa1fb18af371c` |
| `brief.md` | `2d917a17a5f008e5f7b7e1abefa8c5628ad1cf074422326d60d0c2e2dbebd14f` |
| `video.json` | `a0fb8f4b8cd69b69cae255e40a47d60288a9b4e72ca03e8bceed1c718653986b` |
| `script.md` | `c576649d18f34d6c23eb3d9324c0c0d7e62dcf1e498ee4929debd4074ed63899` |
| `claims.md` | `2a7a15dac246417cb9d77b0538a26e271be1291f708b476949b58454f92836c4` |

我重新從固定 Git 提交下載富蘭克林信的 1907 年轉錄 **F** 和 Marion 1870 年後出英文敘述 **M**，全檔 SHA-256 分別為 `0db153d94652cff6845a43763400907170bfd3c5388816529e6f57f58eb3400e`、`2e474f42015f2e0841826202772cb94b3bd6a72a3321bfb2796161a67d8340e5`，與 `research.md` 相同。M 不是 1783 年法文原件，且其自由飛行月份錯誤；此處只取它對修復次序的敘述，不用它判日期。

| ID | 新增錨點與直接支持 |
| --- | --- |
| `s55041` | [F 175–179](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L175-L179) 的 `One of 38 feet Diameter ... at the Expence of the Academy` 直接支持較大新球由科學院出資；原有 F 212–224 仍只作乘坐申請／勸等的錨點。 |
| `s55115` | [M 1589–1593](https://github.com/GITenberg/Wonderful-Balloon-Ascents--Or-The-Conquest-of-the-Skies--13-A-History-of-Balloons-and-Balloon-V__899/blob/c3f6d020de7d9a0ad864aabcf89138476680574e/899-0.txt#L1589-L1593) 明寫繫留時球破裂數處、收回後 `repaired in less than two hours`，再充氣升起，直接支持「修好後」。保留的 F／E 錨點仍負責繫留與後來自由航行的界線。 |
| `s55145` | 同一段 [M 1589–1593](https://github.com/GITenberg/Wonderful-Balloon-Ascents--Or-The-Conquest-of-the-Skies--13-A-History-of-Balloons-and-Balloon-V__899/blob/c3f6d020de7d9a0ad864aabcf89138476680574e/899-0.txt#L1589-L1593) 支持結尾「修好」；自由飛行及日期仍靠保留的 F／E／DATE 錨點，不從 M 的錯月重定日期。 |

僅從這三列的來源欄移除新增的三個連結，`claims.md` 精確還原 R6 SHA-256 `1d86d5a581eb7afe96575c6bd9a593a99a7c6e77be17706c145044d6b56c0c13`。其餘四檔 SHA 與 R6 一樣；因此沒有新口播或新畫面。獨立抽取核對 `video.json` 142 句與 `script.md` 142 句同序同文，前 140 句與 `claims.md` 140 列同 ID 同文；130 個插圖景、13 條伏筆。`lint --slug curio-s55 --json` 為 **0 errors／0 warnings**，`git diff --check`、`npm run check:tasks` 均退出 0（後者只見既有併行／過期認領警告）。
