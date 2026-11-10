# AI 劇的雲端硬碟備份：所有東西都放 AI劇/<名稱>/<集數>/

站主 2026-11-10 重新規劃的備份規則，管四個系列：種田娶妻打天下（3D 原版與真人版）、恁祖媽今年18、
原來如此事務所、奇聞檔案局。之後新開的劇也照這份。

主機的影片備份怎麼複製上架包，在 [`BACKUP.md`](BACKUP.md)。這份管的是**整個製作過程的所有檔案**：
誰負責傳、放在哪裡、怎麼核對，還有舊的 `transfer/*` 分支怎麼收進來。

## 站主的規則（原話）

- 「每部劇統一放 AI劇/<劇名>/<集數>/」（2026-11-10）。
- 「備份都要備份到所有東西，之後需要重製可能的所有東西」（2026-11-10）。內容照兩份分支規則：AI 劇是 #2047 的
  `docs/videos/drama/BACKUP-BRANCHES.md`，奇聞與原來如此是 [`explainer-series/BACKUP-BRANCHES.md`](explainer-series/BACKUP-BRANCHES.md)。
  差別只在目的地從分支改成雲端硬碟。
- 種田的真人重拍版（`-r2`）「當成另一部劇」；同一集的改版放同一個資料夾，舊版進 `_舊版/`。
- 製作檔由**做片的 session 直接傳雲端硬碟**，不由主機 worker 從 GitHub 搬。
- 舊分支先照對照表搬到雲端硬碟，核對完整後**刪除分支**。

## 放在哪裡

全部在 `G:\我的雲端硬碟\AI\備份\AI劇\` 底下（雲端路徑 `AI/備份/AI劇/`）：

```
AI劇/
  種田娶妻打天下/                  ← zhong-tian-qu-qi-e001…（3D 原版，含 r2 先做的 3D 重做）
    _共用/                         ← 參考圖各輪、試鏡、音效庫、配樂庫、小樣、腳本、不屬於單一集的 scratchpad
      製作檔/<來源>/…
    第033集/
      final.mp4、字幕、配音、縮圖、metadata.json…   ← 上架包：主機 worker 照 BACKUP.md 複製
      clips/、recordings/、recut/、keyframes/…       ← 完整層級：主機 worker
      製作檔/<來源>/…                                ← 其他所有東西：做片的 session（這份的主題）
      _舊版/<時間>/…                                 ← 被新檔取代的舊檔
      _舊版/<slug>/…                                 ← 整支被新版本取代的舊版本（-v2 出來後的 v1）
    第001-005集/                   ← 合集
  種田娶妻打天下（真人版）/         ← zhong-tian-qu-qi-e001-r2…
  恁祖媽今年18/                     ← tai-nainai-e001…
  原來如此事務所/
    第012集/                       ← 後台有集數的
    P17/                           ← 沒有集數的用代碼（sothatswhy-p17-gecko-feet）
  奇聞檔案局/
    H01/  W01/  S10/               ← curio-h01、curio-w01-dolby-licensing、curio-s10-v2
```

- **集數**：`第033集`；合集是 `第001-005集`；沒有集數的用 slug 裡的代碼，例如 `H01`、`P17`。什麼都沒有時用 slug。
- **`製作檔/<來源>/`**：一個來源一個子資料夾，原樣保留，不同來源的同名檔不會互相蓋掉。session 傳的，來源寫工作資料夾的名字
  （例如 `_live-e901`、`zhong-tian-qu-qi-e901-dh`、`_scratchpad`）；從舊分支搬來的，來源寫分支名（例如 `zt-live-e001`）。
- **資料夾名稱**：劇名在後台「備份位置」卡的「資料夾名稱」可以改，預設是上面那幾個。已經備份過的集數不跟著改名。
- **Shorts** 照舊放 `Shorts/<系列>/`；偶的江湖、品牌故事等不在 AI劇 的系列照舊。

## 要傳什麼

**一集重做、重拍某一鏡、回頭查決定時可能用到的東西，全部都傳。** 分不清要不要的，就傳。

| 放在 | 內容 |
| --- | --- |
| `<集數>/製作檔/` | 每一支草稿（包括沒選中的）與它的提示詞、log；挑片清單、剪點、裁切；精修前後各版；剪進成片的片段（帶模型原聲）；全部錄音（逐句、各語言、重錄的）；該集配樂；剪接表；交出去的成片連同字幕、預覽、手機版；後台匯入資料夾；審片截圖；交接筆記；當時的 `docs/videos/<slug>/` 快照 |
| `_共用/製作檔/` | 音效庫、配樂庫、試鏡與參考圖各輪（包括沒選中的）、小樣、腳本、不屬於單一集的 scratchpad、合輯 |

不傳的只有：密碼與權杖、可以重新安裝的套件（`node_modules`、`.venv`）。工具會重建的中間檔也傳：站主的規則是「所有東西」，
重建要花錢或重建出來不一樣（隨機的音效、重新生成的配樂）時，就只剩這一份。

## 什麼時候傳

- 每過一關傳一次（分鏡、成片、上架、語言批次），之後產生的檔補傳到同一個資料夾。
- 交給站主或送上後台的檔，**交出去之前**先傳。
- session 結束前一定要傳一次：雲端 session 的容器隨時會被收掉。

## 怎麼傳：`todrive.sh`

[`ai-drama-drive/todrive.sh`](ai-drama-drive/todrive.sh)：

```bash
docs/videos/ai-drama-drive/todrive.sh <工作資料夾> "<目的地>/AI劇/<名稱>/<集數>/製作檔/<工作資料夾名>"
```

- 用 `rclone copy --checksum`，**永遠不刪雲端上的檔**。雲端已經有同名但內容不同的檔，先移到 `_舊版/<時間>/` 再放新的。
- 傳完用雜湊逐檔核對，印出 `todrive: N files, M differences`；M 不是 0 時以失敗結束，要重傳到 0。
- 連結保留成連結，不跟進去；大檔整個傳，不切塊（雲端硬碟單檔上限 5 TB）。
- 目的地不在 `AI劇/` 底下就拒絕執行。

**雲端硬碟的權限**（不要把主機的權杖發給 session：那把是整個雲端硬碟的完整權限，`root_folder_id` 只設定起點，不是權限邊界）：

| 在哪裡做片 | 怎麼寫雲端硬碟 |
| --- | --- |
| Colab | `from google.colab import drive; drive.mount('/content/drive')`，站主用自己的帳號登入；目的地寫 `/content/drive/MyDrive/AI/備份/AI劇/…` |
| Claude Code 雲端 session | 站主另建一把備份用的 rclone 權杖，放在 session 的環境變數或 secret，指向 `TODRIVE_RCLONE_CONFIG`；目的地寫 `<remote>:AI劇/…`（remote 鎖在 `AI/備份`）。權杖不進 repo、不貼進對話 |
| 站主的電腦 | 目的地直接寫 `G:/我的雲端硬碟/AI/備份/AI劇/…` |

## 怎麼確認完整

1. **逐檔核對**：`todrive.sh` 印的 differences 是 0。
2. **涵蓋檢查**：另一個**沒參與製作**的代理，對同一個工作資料夾與目的地跑 `todrive.sh --check`，結果是 0。
   工作區的每一個工作資料夾都要有一個對應的目的地；只做逐檔核對不夠（種田第 1 集曾漏掉另開的 `_live-e901`）。
3. **重剪一次**：換成精簡版、或刪本機檔之前，只用雲端硬碟上的檔還原到空資料夾、重剪一次，跟交出去的成片逐位元相同。

刪本機工作資料夾要三樣都成立，再加上站主在後台的關卡都決定了。

## 舊的 transfer/* 分支

四個備份 repo（`drama-backup-zt`、`drama-backup-tn`、`mokaair-video-backup`、`mokaair-video-backup-sothatswhy`）裡的
132 條分支，約 158 GB，照 [`ai-drama-drive/legacy-branches.tsv`](ai-drama-drive/legacy-branches.tsv) 搬到 `<集數>/製作檔/<分支名>/`
（站主 2026-11-10 確認）。歸法：

- 種田：`zt-cg-eNNN`、`zt-eNNN-media`、`-parity`、`-refs` 歸 3D 原版；`zt-e9NN-media*`、`zt-e001-r2-media`、`zt-cg-e001`～`e006`
  是 r2 slug 先做的 3D 重做（檔案都在 `runpod/`），也歸 3D 原版的第 1–6 集；`zt-live-eNNN` 歸真人版；`zt-shared`、`zt-live-pilot`
  歸真人版 `_共用/`；`zt-series-media*`、`zt-cg-shared` 歸 3D 原版 `_共用/`。
- 一條分支包含多集的（`zt-e031-e032-media`、`zt-e043-e048-*`、`zt-e049-e052-*`、`zt-import-dubs-review-20261107`、
  `backup-sothatswhy-p02-p05`、`-p07-p14`）：依路徑裡的集數拆到各集，看不出集數的放 `_共用/`。
- 整個 repo 副本的五條（`zt-e001-r2-work`、`zt-e043-e048-audio`／`-cutlogs`、`zt-e049-e052-audio`／`-cutlogs`）：只取比 main 多的檔。
- `.partNN` 切塊接回原檔（有 `.SPLIT` 的核對 sha256）再傳。
- `tn-series-assets` 裡的種田音效庫照搬。

搬家在主機上跑（主機的 rclone 權杖寫雲端硬碟、`gh` 讀私人 repo），一條分支做完逐檔核對；全部做完由另一個代理對每條分支做
涵蓋檢查（分支最新一版的每個檔都在雲端硬碟、雜湊相同）。兩樣都是 0，把要刪的分支列給站主，站主同意後才刪。
GitHub 刪分支之後不會馬上釋放 repo 空間。

主機 worker 的分支鏡像（[`BACKUP.md`](BACKUP.md)〈AI 劇的分支鏡像〉）2026-11-10 關掉，它從沒成功跑過。
