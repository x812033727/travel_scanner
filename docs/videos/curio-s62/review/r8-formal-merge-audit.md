# S62 R8｜兩位正式隔離盲讀合併

2026-10-22 UTC。**正式 13 題合併：13／13 PASS。** R8 `script.md` SHA-256 `c638b0d28cfbf6b398cd3bb541160685403bf3936fcd1613bc958921623e4326`，`video.json` SHA-256 `c9f249ab7210fa4fb2cf2ac5206c57735ee19efcf0e846414bcfc06bb0745ace`。兩位全新讀者的[隔離回條 A](r8-isolated-blind-a.receipt.md)、[隔離回條 B](r8-isolated-blind-b.receipt.md)記錄：先讀固定正式 13 題面板 SHA-256 `15cfd34356840ae8036c91bc9d8b29f210be52aa761f28379a2bd9ed263fa5ad`，再只讀同一 R8 劇本，各自在看 CLI、資料或舊票之前封存原答。此合併不改原票或任何創作檔。

| 讀者 | 原票／官方綁定 SHA-256 | 個人判斷 |
| --- | --- | --- |
| A | `d0fca08115921b002e5eff6ab02959d72da2469fc7b31fc83590abead49b6ef1`／`dd833a046a6f46fda01d7bea52bf7673dd2809d7d3c736ef30ec39bf6908f33f` | **11／13 HOLD**；No `no_toc`、`no_recap`。 |
| B | `3404319488f314caffc37307521afed23a9a8d8349fb6c7b2fd2156d468efc98`／`9d28a88d30799afc75394d74286ef208194b956ecfd1f97fe996a8c3d60adc0f` | **13／13 PASS**；沒有 No。 |

我以官方 `panelVerdict` 重算兩份原票，結果逐欄等於各自 CLI stdout 及 round 1 官方紀錄；13 題 ID／題文一致，兩人 **26／26** 個引文均逐字對上目前 114 句中的對應 ID。兩份綁定均為 `narrative_hash=edc7d2005d74f93c`、`script_hash=5a78e1e249ba70941f3426628946c07f0db2a0547112f88cc26395ccdeb673af`、`panel_rules_sha256=5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`、`panel_narration_sha256=c55c979f774539c2932f18c417091b0804d6b40e569f276ccee180923ffbfe86`，且 `narrativeReviewMatches` 均為 true。

依官方 `mergePanelVerdicts([A, B])` 逐題 OR，**11 題兩人均 Yes**，`no_toc` 與 `no_recap` 各有 B 一位 Yes，所以沒有共同 No；[正式合併答卷](r8-formal-merged-answers.json) SHA-256 `172b6472bb926f75c1ac4ba835e4e696cb3f88e02c2261ed3749d249762b2ab2`，[含雙人原判斷的正式合併紀錄](r8-formal-merged-narrative.json) SHA-256 `83a5484d28ca40b9dc891ab028cca26edadb81bcc2e43fa024633f303084ed43`，記錄 `round=8`、`passed=true`、`failed=[]`、`advisory=[]`。以該答卷在全新獨立工作目錄重播：

```sh
node tools/video/cli.mjs narrative --slug curio-s62 --answers docs/videos/curio-s62/review/r8-formal-merged-answers.json --workdir /tmp/curio-s62-r8-formal-merge-b1fa0a6fc --json
```

CLI exit **0**、13／13 Yes，stderr 空白；[官方重播綁定](r8-formal-merge.official-replay.json) SHA-256 `6b17ed3bd4bc9c2338c857bbb1f840e1b4a917731b6187dc0e77a1a5e326ef80`，`round=1` 是這個空工作目錄的首次記錄序號，不是創作版次。stdout 和 exit 亦按 `r8-formal-merge.cli-*` 保存。

**保留 A 的單票編輯疑慮。** A 認為 `s62041` 的「回到開場那夜」像對觀眾宣告結構（`no_toc`），`s62104` 的木星環繞結論重述了 `s62051` 而未明示回呼（`no_recap`）。B 的 Yes 使這兩題依既定雙讀者規則通過；B 的引用分別在 `s62055`、`s62038`，未直接反駁 A 指出的兩句。這些疑慮應供站主審稿時參考，但不是本輪正式合併 HOLD，不得改寫 A 原票。

[R8 獨立史料／書面畫面重驗](r8-independent-source-visual.md)亦 PASS。**下一關仍是站主對大綱與稿子的選擇／核准，以及後續媒體關卡；本票不代表站主已核准或已產生任何付費素材。**
