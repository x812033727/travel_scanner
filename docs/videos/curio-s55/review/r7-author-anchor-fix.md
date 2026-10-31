# S55 R7｜作者單一用途來源錨點修正

2026-10-20 UTC。R6 [獨立史料與書面畫面覆核](r6-source-independent.md)判旁白史實與書面畫面 PASS，但 `claims.md` 因三列未直接連到所述細節而窄 **HOLD**。R7 作者只補那三列來源欄；**本檔不是獨立 R7 PASS 或敘事盲評**。

## R6 → R7 精確 SHA-256

| 作者檔 | R6 | R7 |
| --- | --- | --- |
| `research.md` | `b30ea8f4021ebb27fc2f2b8f63c633e4dde00c5fcb52241daa3aa1fb18af371c` | `b30ea8f4021ebb27fc2f2b8f63c633e4dde00c5fcb52241daa3aa1fb18af371c` |
| `brief.md` | `2d917a17a5f008e5f7b7e1abefa8c5628ad1cf074422326d60d0c2e2dbebd14f` | `2d917a17a5f008e5f7b7e1abefa8c5628ad1cf074422326d60d0c2e2dbebd14f` |
| `video.json` | `a0fb8f4b8cd69b69cae255e40a47d60288a9b4e72ca03e8bceed1c718653986b` | `a0fb8f4b8cd69b69cae255e40a47d60288a9b4e72ca03e8bceed1c718653986b` |
| `script.md` | `c576649d18f34d6c23eb3d9324c0c0d7e62dcf1e498ee4929debd4074ed63899` | `c576649d18f34d6c23eb3d9324c0c0d7e62dcf1e498ee4929debd4074ed63899` |
| `claims.md` | `1d86d5a581eb7afe96575c6bd9a593a99a7c6e77be17706c145044d6b56c0c13` | `2a7a15dac246417cb9d77b0538a26e271be1291f708b476949b58454f92836c4` |

## 三格來源欄的差分

1. `s55041` 保留原申請／勸等連結，另補 [F 175–179](https://github.com/GITenberg/Benjamin-Franklin-and-the-First-Balloons_43809/blob/f9f2c7e6a25ffbcea1b28955239796378b00ce29/43809.txt#L175-L179)，直接支持科學院為大球出資。
2. `s55115` 保留 F 與 E，另補 [M 1589–1593](https://github.com/GITenberg/Wonderful-Balloon-Ascents--Or-The-Conquest-of-the-Skies--13-A-History-of-Balloons-and-Balloon-V__899/blob/c3f6d020de7d9a0ad864aabcf89138476680574e/899-0.txt#L1589-L1593)，直接支持脫繩前已修復球體；M 仍標為後出記述。
3. `s55145` 同樣另補 [M 1589–1593](https://github.com/GITenberg/Wonderful-Balloon-Ascents--Or-The-Conquest-of-the-Skies--13-A-History-of-Balloons-and-Balloon-V__899/blob/c3f6d020de7d9a0ad864aabcf89138476680574e/899-0.txt#L1589-L1593)，直接支持結尾的「修好脫繩後」。

三列的 ID、旁白、其他來源和畫面註記均未改。把新增三個連結只從這三列來源欄反向移除，`claims.md` SHA 精確還原為 R6 `1d86d5a581eb7afe96575c6bd9a593a99a7c6e77be17706c145044d6b56c0c13`；四個其他作者檔也逐位元組維持 R6 SHA。`claims.md` 的 **140 列**與 `video.json` 同序同文，`script.md` 的 **142 句**（含 2 句片尾）與 JSON 同序同文；固定提交逐句連結增至 **161 個**。`VIDEO_WORKDIR=/tmp/curio-s55-r7-author node tools/video/cli.mjs lint --slug curio-s55 --json` 回 **0 errors、0 warnings**；工具估全稿 13.677 分鐘，文本未改。`git diff --check` 退出 0。

請由另一位工作者按 R7 SHA 獨立核對這三格來源差分，再讓兩位新讀者對同一未改的 R6／R7 劇本 SHA 分別盲評。沒有開始付費配音、插圖、配樂或成片。
