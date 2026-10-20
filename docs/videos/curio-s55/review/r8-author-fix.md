# S55 R8｜作者窄修與精確凍結

2026-10-20 UTC。[R7 來源錨點獨立覆核](r7-anchors-independent.md)為 PASS，但兩位新讀者的[官方 OR 盲評合併](r7-isolated-merge.md)為 **FAIL，12/13 Yes**；共同必答 No 僅 `no_recap`。A 另判 `no_detour` No、B 另判 `payoffs` No，這兩題按正式任一讀者 Yes 規則合併為 Yes，異議仍在 R7 原始票。本檔只記 R8 作者修訂及機械檢查，**不是 R8 獨立來源 PASS 或盲評**。

## R8 五檔 SHA-256

| 作者檔 | R7 SHA-256 | R8 SHA-256 |
| --- | --- | --- |
| `research.md` | `b30ea8f4021ebb27fc2f2b8f63c633e4dde00c5fcb52241daa3aa1fb18af371c` | `299b4ace9f8c5ea9d784b2d0296bdbf16c851108ae3b070264107f773cf9deeb` |
| `brief.md` | `2d917a17a5f008e5f7b7e1abefa8c5628ad1cf074422326d60d0c2e2dbebd14f` | `3ae5899e04018165eb7c7251a92053fab25a9128683f270abf1b3815b28fd932` |
| `video.json` | `a0fb8f4b8cd69b69cae255e40a47d60288a9b4e72ca03e8bceed1c718653986b` | `f64213fa0b8bbee6f8bfeaec12b4206c170f977d075fcef0668aae4fbc8816b8` |
| `script.md` | `c576649d18f34d6c23eb3d9324c0c0d7e62dcf1e498ee4929debd4074ed63899` | `50b59af8177a054e5049c1b94f31cef5838deef3837aec9d7d7c916514be0269` |
| `claims.md` | `2a7a15dac246417cb9d77b0538a26e271be1291f708b476949b58454f92836c4` | `3780c1bd241711cd36b71e93915e6b2a48a203096d98b7d9dabe5b6cacfe8392` |

## R7 → R8 差分

- `s55046` 的十月八日詳報未出只說一次。`s55047` 移除「詳報遲遲沒出版」的重述，保留並說清富蘭克林把手邊小冊子寄給 Banks、仍認為內容未達期待；畫面改為無可讀內容的小冊子寄出示意。
- `s55048` 刪除與乘員安全無直接關係的圖畫準確性說法，改用同一封當時信明標 **`It was supposed`** 的約兩百土瓦茲高度估計，口語換算為接近四百公尺；不寫成實測。畫面只示意聽來的凡爾賽高空球，不畫刻度，也不把富蘭克林放進現場。
- `s55049` 直接由這個估計高度問羊、鴨、公雞落地是否受傷，接 `s55050` 的非目擊歸屬及後續充氣、下降、公雞受傷結果。`claims.md` 三格文字、來源和畫面限制與 JSON 同步；`research.md` 的 P04、`brief.md` 的動物章與交接狀態同步。其餘史實、來源鏈接、伏筆、章節與媒體計畫沒有編修。

## 作者機械檢查與交接

用 `node tools/video/cli.mjs script --slug curio-s55` 自 `video.json` 重生 `script.md`。JSON **142 句**與 script **142 句**同序同文，前 **140 句**與 `claims.md` **140 列**同 ID 同文；**130 個 shot、13 組 loop、161 個固定提交逐句連結**。`VIDEO_WORKDIR=/tmp/curio-s55-r8-author node tools/video/cli.mjs lint --slug curio-s55 --json` 為 **0 errors／0 warnings**，工具估全稿 **13.753 分鐘**，不是實際配音時長。以最快 **325 漢字／分鐘**計，首章 **175 字／32.31 秒**，其後正文 **2655 字／8.17 分鐘**，仍高於八分鐘文字底線。`git diff --check`、`npm run check:tasks` 均退出 0；全任務檢查只見既有過期認領及並行範圍警告。

下一位請以這五個 R8 SHA **獨立查來源與書面畫面**，尤其是 `s55048` 的聽來高度與口語換算，再交兩位從未讀過 R8 作者／來源文件的新讀者各自盲評 13 題及官方 OR 合併。B 對 R7 `s55040` 遠距回收的少數異議留待新讀者檢驗；本輪只修來源可以支持的共同重述阻點及相鄰岔路。沒有開始配音、插圖、配樂或成片。
