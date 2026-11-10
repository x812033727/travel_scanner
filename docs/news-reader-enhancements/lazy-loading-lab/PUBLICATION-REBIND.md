# 2026-11-10 公開證據套件重新綁定

**公開衍生收據，非新實驗。** 原始實驗時間、18 次結果、請求紀錄、幾何、圖片及截圖沒有改動。這次只讓套件可公開且可攜，移除個人本機路徑，重建受影響的檔案雜湊鏈。

## 變更與歷史界線

- `experiment/lab.cjs` 與 run 的 `runner.cjs` 只有 Playwright 套件解析那一行及說明註解改動；已機械還原該片段並確認與原 runner 位元組完全相同。未改 fixture、等待、捲動、請求、判定或實驗演算法；本次沒有執行 `run`。
- 公開 runner 由 `MOKAAIR_PLAYWRIGHT_ROOT` 或套件／目前工作目錄解析 `playwright/package.json`，不帶個人電腦 fallback。只驗語法與依賴解析，未宣稱此衍生檔當時執行過瀏覽器。
- runner → environment → receipt 依序重新綁定；公開 environment／receipt 明標 `PUBLICATION_DERIVED_NOT_NEW_EXPERIMENT`，保存原 hash、原始時戳及 PASS 的歷史語意。原無個資 environment／receipt／verification／brief 原樣留在 run 的 `original/`；含個人路徑的原 runner 仍只保留於私有原目錄。
- `sources.json` 的實驗檔位置改為套件相對路徑，更新實際變動檔的 bytes／hash 並保留 `original_sha256`。官方 HTML／抽出正文的位置以 `<home>` 明示私有保留；只列原取得狀態與原 hash，沒有複製官方全文。
- review 的原 v2 JSON 原樣保留為 `v2-check.original.json`；現行 JSON 明示衍生綁定、原審稿 hash 歷史與現行公開檔 hash。Markdown 審稿原歷史不改，只追加本次說明。
- `.gitattributes` 保留 `experiment/** -text`，並擴及雜湊綁定的文章、索引、作者註、review 與發行清單，防止 Git 對原位元組做換行正規化。

## 實際核對

- 原 verifier 位元組未改；實際執行後 **165／165 PASS**，不是複製舊 PASS。新 `verification.json` 的 `checkedAt` 是本次對帳時間，`inputReceiptSha256` 是公開衍生 receipt；原對帳另存。
- `article.md`、`draft.json`、原始結果與 CSV、兩份請求紀錄、fixture、預先規格、18 張 PNG 全部維持原 bytes。見 `PUBLICATION-MANIFEST.json` 的逐檔清單。
- 來源 hash 與公開實驗路徑逐一核對，無外部官方 HTML／抽出全文被帶入。fixture HTML 是本實驗自有頁面。
- Repo hygiene：已從現行 `tools/repo-hygiene.test.mjs` 逐字擷取實際 matcher，掃描本候選套件所有非二進位文字，零違規；收據在 `review-evidence/publication-hygiene.json`；這項是候選內容掃描，不替代 root 整合後的全 repo CI。

## 原／公開 hash 對照

下表中的原 hash 只指原始檔，不能用來聲稱已變動的公開檔仍有原 hash。新加入的原樣副本與其他未改檔，可由 manifest／原收據核對。

| 檔案 | 原 SHA-256 | 公開 SHA-256 |
|---|---|---|
| `.gitattributes` | `08bfc3c956177350e0db08c53fab240b6b99219da7f722f209907377695decda` | `546dd7dff02a6fdfc1963e1feca0aa9f87c070c487297b784d5d7e6949b6f595` |
| `AUTHOR-NOTES.md` | `932e656c9e1c1b371666d53882b2a2b0af91182e9d5a94cf832be364574cb37d` | `6769568fb3fcc81d48639d42b27dc1194c19251f957499c6a2054b1663f0f6de` |
| `review-1.md` | `561fc558b775b7a87c3d2c185c09addd2f640d5e8b172569318a3716bd877ec6` | `bf2df65358a429fbda5d066bf744a81aeb5c3d2deb1c82a3b361210120e36da9` |
| `sources.json` | `d18bb841a71613650f9497448b33c63cbe2dbe7519b6fdb66e92c3788495ec03` | `c06864de114729cf7672a53a362363aa16fa2e8398ccf05862582cd514ce6c7f` |
| `experiment/lab.cjs` | `15a5608e2c3eec0cbbb0f4d10f4b393750945b2c7660313d033d74c352e48025` | `cbea29f3c5218a763da52403622dbfcb259e71f6552e28a40e3b200836271ffb` |
| `experiment/README.md` | `893cc7ffc74cb5ad876d3084e21fd7de30e258f0429ced19407ec47b17ab4035` | `c645ad9fb806d08beb2ca1ddb0d8173d79b753f5057065d56eb12a0354ef4a9f` |
| `experiment/RESULTS-BRIEF.md` | `9fec3d2697333dda8f6b8bc38833b0f52e8e6f01e3046c0d0ecc7f753d0bcaa3` | `9e068b8b6e5dbe5c4311f868ee13864ec6fc3d0dae88f7ce800e567c8502d790` |
| `experiment/sources.md` | `a9f7aa0e1026941e4db3eb3a6ac3c45bfd83c095e45b0b23468c31db0aab380b` | `f85172b320b914225084b3318d572535de58325a68528763942713108acac2b3` |
| `review-evidence/v2-check.json` | `826f080b73f5c9b1b131e693e2f5f60ae8da65a79a25316544ea5ef59dc8000c` | `148fdad85dfe83ebfd46520bc0f9b8e71553ad21976df1b67eb97a89397da330` |
| `experiment/runs/2026-11-10T12-52-37-220Z/environment.json` | `4c81b4ffa5f1c739e019e12d6c75c13491b2fcad601021129c75920998e78731` | `bf9c0cbf113dc7a9edb2ca7ef7c6a482b139192c3f5fda138f40e8faedcb218b` |
| `experiment/runs/2026-11-10T12-52-37-220Z/receipt.json` | `ca402a83accabe19b73d89f41f799bebaf685dedb64e7d3e17a984b778dc41a9` | `4fff96b602a1733848c60930ad3c4d99fec897a270f1c9ea07480b09c75da0ee` |
| `experiment/runs/2026-11-10T12-52-37-220Z/runner.cjs` | `15a5608e2c3eec0cbbb0f4d10f4b393750945b2c7660313d033d74c352e48025` | `cbea29f3c5218a763da52403622dbfcb259e71f6552e28a40e3b200836271ffb` |
| `experiment/runs/2026-11-10T12-52-37-220Z/verification.json` | `37da1edc81639de577ef6719707d7063f815e6fa7212cac73ee4b344a62605cc` | `67743edd73fe02960b3943e4427ce529df0dd6f0d13057a44c06d87a64509ddc` |

`PUBLICATION-MANIFEST.json` SHA-256：`6cd1fbd1a785e4eec540f7ce2c0828476ee30426dc08da676592349884a0bc29`。清單不包含自身與本說明，以避免循環雜湊；hygiene 收據記錄掃描內容集合（不含收據自身）。

## 原始 verification 與中間重驗的區分

最終對帳發現整合目錄的 verification 是 2026-11-10T13:12:30.446Z 的中間重驗，不是原實驗 12:55:37.945Z 的首份驗證。`original/verification.json` 現在保存真正原私有檔，hash `fd46293cb7c807d623869a2eeab0cb66fd35320316199112cbc550147e27380f`；中間版本原樣保存為 `original/staging-verification.json`，hash `37da1edc81639de577ef6719707d7063f815e6fa7212cac73ee4b344a62605cc`。前述原／公開變更表的「原」指此次準備輸入；原實驗與中間重驗另由 manifest 的 `historical_original_copies`、`intermediate_staging_verification` 精確區分。來源／原 v2 review 所記 `fd46293c…` 始終指真正原驗證，沒有借用中間或公開衍生檔冒稱。

## 2026-11-10 Git index 位元組保護補正

Root 在暫存 index 對全部 71 筆清單核對時，只有 `.gitattributes` 因自身未設定 `-text` 而被 Git 正規化 CRLF，與發行清單不符。本次補上 `.gitattributes -text`；另在此證據套件範圍設定 `whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol`，讓普通 `git diff --check` 接受原本保留的 CRLF，同時保留尾端空白／檔尾空白／tab 前空白檢查。

只修改屬性檔與發行 metadata／hygiene 收據；原實驗演算法、environment／receipt／verification、文章、素材、請求與結果 bytes 全不變。本次不重跑 verifier，不將原 165 項證據對帳冒稱新一輪實驗或新測試；root 會在重新暫存後獨立核對 index 的精確 bytes。

前一公開 `.gitattributes` SHA：`ffac34cce7712d54a52015239b7c2547e34e05c05ac1e6bcb1f56e728659b46b`；補正後：`546dd7dff02a6fdfc1963e1feca0aa9f87c070c487297b784d5d7e6949b6f595`。前一 manifest SHA：`1242d6a69b18a559ac8143cdabf69321e8810dc7864afb3788e2d84c1852431b`。舊公開 metadata 位元組仍保留於私有 `publication-packaging-01/`，manifest 的 `packaging_revisions` 保存此次原／新綁定。最新 hygiene 收據會依此最終套件重新掃描，沒有拿舊掃描 hash 冒稱新檔。
