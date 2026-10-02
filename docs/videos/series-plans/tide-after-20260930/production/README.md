# 潮退之後｜全季製作交接包

真人長劇，40集，每集目標55–62分鐘。production-v1，2026-10-02。劇本維持四篇各十集及原集名；用途是演員讀本、選角、勘景、導演分鏡、排通告與分組報價。

## 先開哪份

| 使用者 | 閱讀順序 |
| --- | --- |
| 主創／製片 | [全季劇本與時長索引](breakdowns/episode-index.md) → [各組交接](department-handoff.md) → [拍攝與報價底稿](shooting-plan.md) |
| 演員／編劇 | [全季可列印讀本](breakdowns/reading-copy.html)；每集原稿在 `scripts/ep-01.fountain` 至 `ep-40.fountain` |
| 導演／副導 | [首集逐場起拍方案](pilot-plan.md) → [逐場拆表](breakdowns/scenes.csv) → [角色故事日](breakdowns/cast-days.csv) |
| 美術／服化／道具 | [文件與螢幕製作單](props-artwork.md) → [道具拆表](breakdowns/props.csv) → [名冊與文件母版](document-master.json)及[可列印校樣](breakdowns/prop-proofs.html) |
| 場務／執行製片 | [景塊初分](breakdowns/blocks.csv) → [地點拆表](breakdowns/locations.csv) → [角色集次](breakdowns/cast-summary.csv)及[具詞角色](breakdowns/speaking-parts.csv) → [13項報價表](quote-sheet.csv) |
| 讀本／剪接 | [逐集計畫時間](breakdowns/timing.csv) → [逐場讀本紀錄空表](breakdowns/table-read.csv) → [原包裝與字幕規格](../packaging.md) |

Fountain中的 `[[SCENE ...]]` 是拆表資料，HTML讀本會隱藏；角色前的 `@` 是強制角色行。螢幕內可見演員亦計入有畫面角色；僅電話或畫外聲才記voice_only。影片／照片插入素材另排拍攝，不表示該演員必須到觀看者所在場地。可直接用支援Fountain的編劇軟體或純文字編輯器開啟；HTML在瀏覽器列印為A4或另存PDF即可。檔名、集號、場號三者一致，不需要另裝產線或媒體生成服務。

## 單一來源與重建

- [SPEC](SPEC.md)：共同劇本格式、節拍、容量及可交接的層級。
- [registry.json](registry.json)：固定角色、場地、道具；群眾與只聲音角色分開標。
- [calendar.json](calendar.json)：現代故事日期；2011／2013回憶另標歷史日。
- `scripts/`：對白與分場的唯一來源。`breakdowns/`由它產生，不能單獨手改。
- [document-master.json](document-master.json)：名冊、人名排序、尾頁差異和關鍵文件內容。
- 原[設定集](../setting.md)、[細綱](../outline.md)、[連貫性](../continuity.md)仍管情節與揭曉；原審稿報告保留為歷史版本。

在儲存庫根目錄執行：

```bash
python3 docs/videos/series-plans/tide-after-20260930/production/build_package.py
python3 docs/videos/series-plans/tide-after-20260930/production/build_package.py --check
```

只使用Python標準函式庫。第一行更新拆表與讀本；第二行檢查40集、場號、編號、日期、節拍、旁白集次、計畫時長及衍生檔是否一致。撰稿途中可加 `--partial` 看已存在的集數，它不會產生或宣告完整交付。自動檢查不能判斷演技、戲劇張力或真實片長，這些記在審讀與讀本紀錄。

`speaking-parts.csv`由實際角色臺詞行彙整，涵蓋未列入固定角色表的店員、保全、接線員等具詞小角色；同職務稱謂是否由同一演員飾演由副導確認，不可只按固定角色表估算全劇演員人數。

CSV採UTF-8與逗號分欄，同格多個編號以分號分隔；若試算表直接開啟時出現亂碼，以「從文字／CSV匯入」選UTF-8。按場號篩選即可回到同場Fountain。

`table-read.csv`是空白工作表：實際讀本另複製到具日期的檔案，避免重建時覆寫實測。`quote-sheet.csv`的3.4億基數是預算假設，報價欄刻意留空，不能當成已有供應商承諾。

## 從這一版到開機鎖稿

先以EP01做完整讀本、港邊聲畫測試和首輪報價，按 `pilot-plan.md` 回寫讀本修訂版。其餘逐批四集讀本，優先涵蓋2011景塊及29–31跨集火場。每場記臺詞、走位與兩者合併時間，不能把計畫分鐘照抄到實測欄。

開機版本需有：導演確認可拍的走位與鏡位、主創確認角色與揭曉、顧問對具體程序與道具回覆、製片確認演員／地點／效果報價及檔期、讀本證明每集容量在目標內。這些是實際製作的下一步；本包不把未發生的選角、勘景、讀本或簽約標成已完成。

如劇本改變角色是否到場、日夜、道具或效果，先改同場metadata再重建；如改故事日期，先改calendar並同步服化。特殊場面用專業團隊分拍，不能把文字中的火、水、奔跑動作直接當現場執行指令。
