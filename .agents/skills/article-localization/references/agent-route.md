# 路線 B：代理翻譯、逐語審稿、併入內容包、編譯成 bundle 發布

2026-09-24 `desk-cable-charging-organization` 走的路（票 `tasks/done/2026-09-24-localize-desk-cable-guide.md` 與 `tasks/done/2026-09-24-release-localized-desk-cable-guide.md`）。翻譯、審稿到內容 PR 都不需要把腳本灌進正式站容器，所以 Claude 在 auto 模式下做得完。desk-cable 當時用裸 `guides-import` 發布；PR #1273 之後，審過的一波用 `docs/article-localization/prepare_route_b_bundle.py` 編成 `publish_bundle.py` 讀的 schema-1 bundle，走它的 durable journal（§6）。編譯器的輸入格式、輸出與拒絕表以 `docs/article-localization/route-b-bundle.md` 為準。代理的共通規矩（UA、只寫工作目錄、不跑 git）照 skill `content-pipeline` 的「不變的規矩」。

## 1. 釘來源

從公開 API 抓已發布的 zh-TW，正規化後算雜湊；這個雜湊就是整批唯一的翻譯依據，寫進票，也是審稿收據每一列的 `source_sha256`（§3）。

```bash
curl -s -A "Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)" \
  "https://mokaair.com/api/travel/guides/life/<slug>?locale=zh-TW" > <WORK>/published-zh-TW.json
```

正規化：拿掉公開文件的 `version`、`published_at`、`modified_at`（它們是傳輸欄位，不拿掉雜湊就錯，batch009 第一版基準因此作廢），經 `GuideDocument.model_validate(...).model_dump(mode="json")`，再用 `app.guides.service.document_hash`。拿同樣方法算 repo 內容包的 `locales["zh-TW"]`：兩個值要相同，不同就表示後台改過或 repo 較新，先弄清楚再翻。

這份公開 API 投影只是翻譯的依據。發布時編譯器要的 baseline 必須是正式站快照建的（有資料庫 id 與版本），公開投影會被拒絕（§6）。

翻譯前把原文讀一遍找錯：站內連結連錯文章、事實過期。有錯先開原文修正票、發布成新版本，再以新版本為基準（desk-cable 就是先修「標記」的錯連，發布成 zh-TW v8 才翻）。

## 2. 翻譯、審稿、套用（每語三個角色）

| 角色 | 模型（實測） | 產出 |
| --- | --- | --- |
| 翻譯 | sonnet，每語一位 | 完整 GuideDocument JSON 與該語系的 SVG，自己渲染檢查 |
| 審稿 | opus，每語一位，沒參與翻譯 | 只交修正清單（逐句對照 zh-TW），標嚴重程度；標題疑慮另列 |
| 套用 | 第三個代理或協調者 | 套修正、重新驗證、重新渲染；審稿前版本留成 `*.pre-review.*` |

- 所有檔寫在 `<WORK>`（`tr/`、`review/`、`svg/`、`render/`），repo 不動。
- 同模板的兄弟文章已經五語上線時，樣板句（圖的頁首頁尾、圖說結尾句、hero alt 的 AI 標示與 credit）直接沿用已審過的譯法，並告訴審稿者這是刻意的。
- 文末站內連結的文字要逐字等於目標文章在該語系的**已公開**標題；目標沒有該語系就不要連。
- desk-cable 的審稿：en 10 筆、ja 13 筆、ko 12 筆、zh-CN 4 筆。嚴重的三筆在「共通坑」裡。
- 套用完、重新驗證與渲染之後，當場寫審稿收據（§3）；不要等到發布前才憑記憶補。

## 3. 審稿收據（`route-b-review-v1`）

編譯器只認這份收據，不從 `<WORK>` 裡的檔案推論「審過了」，也不會替你補；收據不能事後編造。一批一個 JSON 檔（例如 `<WORK>/review.json`），嚴格 UTF-8、不能有重複的鍵，頂層剛好三個鍵：

- `schema`：`"route-b-review-v1"`。
- `evidence_sha256`：私人證據（修正清單、渲染圖）的 SHA-256；證據本身留在 `<WORK>`。
- `targets`：每個 slug×語系一列，欄位剛好是下表這些，多一個或少一個都拒絕。

| 欄位 | 要釘什麼 | 編譯器拒絕的情況 |
| --- | --- | --- |
| `slug`、`locale` | 這一列審的是哪篇的哪個語系 | slug×語系重複、不支援的語系 |
| `status` | `"PASS"` | 其他任何值 |
| `translator` | 翻譯或套用修正的人／代理 | 空白 |
| `reviewer` | 另一位審稿者 | 空白，或與 `translator` 相同（忽略大小寫與前後空白） |
| `reviewed_at` | ISO 8601 時間，帶時區 | 沒有時區、時間在未來 |
| `source_sha256` | 翻譯依據的 zh-TW 正規化 `document_hash`（§1 的值） | 不等於發布前 baseline 的來源雜湊：審稿之後原文變了 |
| `document_sha256` | 套用修正後、要上線那份文件的正規化 `document_hash` | 不等於 candidate 內容包裡該語系的文件 |
| `assets` | 文件用到的每張圖，`"/guides/<slug>/<name>.<ext>"` 對 SHA-256；另外只准加文件所用 raster 的同名 SVG 母檔（`hero-en.jpg` 旁的 `hero-en.svg`） | 文件用到的圖沒列；列了文件沒用到的圖；圖與 candidate 或 baseline 裡的不同；文件用到的圖單張超過 300,000 位元組 |
| `checks` | `text`、`visual`、`glyph`、`links` 四項，全是 `true` | 少一項、多一項或任一項不是 `true` |
| `open_findings` | `0` | 大於 0，包括還沒解決的原文摘要疑問 |

- 兩個雜湊都用 `app.guides.service.document_hash` 算 `GuideDocument` 正規化後的文件，與 §1、baseline、publisher 同一個定義。
- 收據要涵蓋之後要發布的每個 slug×語系；編譯時可以選得比收據窄（一波、或少幾個語系），不能比它寬。
- 審稿之後文件再改一個字（包括為了 lint 改的），`document_sha256` 就對不上：重審、換一份收據。
- 有還沒解決的發現時，`open_findings` 留在大於 0，或把 slug 放進 `apps/api/app/guides/publish_holds.json`；兩者都會讓編譯器拒絕。

## 4. 併入內容包

- 先確認原內容包能用 `json.dumps(obj, ensure_ascii=False, indent=2)` 逐位元組重現；能的話只在 zh-TW 之後加四個 locale，diff 只有新增。不能重現就停下來，別讓序列化差異混進 PR。
- SVG 放 `apps/web/public/guides/<slug>/`，命名 `diagram-1-{en,ja,ko,zh-cn}.svg`（檔名小寫 `zh-cn`，locale 鍵是 `zh-CN`）。沒有字的 hero 五語共用；hero 有字時每語要 `hero-<l>.svg` 加渲染出的 1600×900 `hero-<l>.jpg`（batch024 的做法），原圖不動。
- 編譯器只收 `public/guides/<slug>/<name>.<ext>` 這種路徑：檔名只能是小寫英數加連字號，副檔名 `webp`、`jpg`、`png`、`svg`；單張圖不超過 300,000 位元組。
- 併入後再算一次 zh-TW 的正規化雜湊，與步驟 1 相同才算數；四個新語系的雜湊要等於收據的 `document_sha256`。

## 5. 檢查（從 `apps/api`）

```bash
<PY> -m app.guides.pack_cli lint --kind life
<PY> -m pytest tests/test_guides_content_pack.py -q
PYTHONUTF8=1 <PY> ../../docs/news-2026-batch-4/translation_checks.py <prefix> <slug>
CHROMIUM_BIN="<CHROMIUM>" <PY> -c "from pathlib import Path; from app.guides.pack_ingest import render_svg; render_svg(Path('<SVG>'), Path('<PNG>'))"
```

`translation_checks.py` 抓日文 Shift_JIS 編不出的漢字、韓文 KS X 1001 以外的音節、en／ko 裡引用了原文沒有的中文。每張 SVG 渲染後逐張看溢出、裁切、重疊、缺字。

## 6. 發布（另一張票，部署之後）

### 凍結 candidate（`route-b-candidate-v1`）

內容 PR 合併後，從合併提交的 Git blob（不是工作樹）在 repo 外做一份凍結副本：

```text
<CANDIDATE>/candidate-manifest.json
<CANDIDATE>/packs/<slug>.json                  # 完整五語 ArticlePack
<CANDIDATE>/public/guides/<slug>/<name>.<ext>  # 審過的文件用到的每張圖
```

```bash
git cat-file blob <COMMIT>:apps/api/app/guides/content/<slug>.json > <CANDIDATE>/packs/<slug>.json
git cat-file blob <COMMIT>:apps/web/public/guides/<slug>/<name>.<ext> > <CANDIDATE>/public/guides/<slug>/<name>.<ext>
```

- manifest 剛好四個鍵：`schema`（`"route-b-candidate-v1"`）、`source_git_commit`（那個合併提交的 40 位 hex）、`articles`（每篇 `slug`、`pack_path`、`pack_sha256`）、`assets`（每張 `path`、`sha256`）。
- 列出的每個內容包與圖都會重算雜湊，選沒選都一樣。路徑只能是 `packs/<slug>.json` 與 `public/guides/<slug>/<name>.<ext>`；`..`、絕對路徑、反斜線、符號連結都拒絕。
- 一份 candidate 可以放好幾波，這次上哪些由編譯時的 `--slug` 與 `--locale` 決定。

### 編譯、審 manifest、交給 publisher

1. 確認 live HEAD 已包含內容 PR（部署腳本 `--dry-run` 回 up to date 就不必部署）；沒有暫停檔、鎖空著、slug 不在 `apps/api/app/guides/publish_holds.json`。編譯器讀 repo 這份清單，publisher 在 dry-run 與兩個發布階段再讀部署版本的那份。
2. 部署之後重新匯出快照、用 `build_baseline.py` 建 baseline，輸出不改（`.agents/skills/article-localization/references/bundle-release.md` §1）。把 `export_snapshot.py` 灌進正式站容器會被 auto 模式分類器擋：切 Manual 讓站主逐次核准，或把那一行指令交給站主跑。內容 PR 部署後，選到的語系在 baseline 裡是 `repository-only`，它必須逐字等於審過的文件。
3. 在檔外算三個輸入的 SHA-256（`sha256sum`），從 `<ROOT>` 跑 SKILL.md 的編譯指令。`--output` 要是 repo 與 candidate 之外、還不存在的新目錄（上層目錄要已存在）；被拒絕時不留 manifest，修好輸入後換一個新目錄再跑。
4. 一起審 `release-manifest.json` 與 `route-b-provenance.json`：slug、語系、圖剛好是核准的這一波，雜湊與收據相同。每篇的 `locales` 與 `publish_locales` 都是選到的語系、`hub: false`，沒有原文修正；provenance 寫著 `"authorizes_production": false`，編譯成功不是同意。記下 manifest SHA-256，之後每一步都用這一個值；同樣的輸入編出位元組相同的輸出，另一個人可以重編比對。
5. 用有選項的提問讓站主同意，整庫 `pg_dump -Fc` 放主機 `/root/` 並確認 TOC 讀得出來。然後在正式站 API 環境照 `.agents/skills/article-localization/references/bundle-release.md` §5 依序跑 `publish_bundle.py` 的 `dry-run`、`drafts`、`publish-articles`、`publish-hubs`；bundle、baseline、manifest SHA、`--deployed-root`、actor、state 目錄全程不變。停下來就用同一個 bundle 與 state 目錄重跑，不換新目錄。
6. `guides-links-rebuild`（筆數應增加、dropped 0），五個語系各跑 `guides-links-check --locale <L>`；exit 1 可能來自別篇早就有的發現，看本篇有沒有。
7. 本機未登入跑 `verify_public.py`（五語，`--sitemap`），並把每個語系的公開 API 回應存成 `published-<locale>.json`，正規化雜湊要等於內容包。成功後重跑 publisher 什麼都不寫；之後再取的 baseline 會把新語系列為已存在，編譯器不會再編同一批。

編譯路線第一次寫正式站之前，要先在部署用的 API 映像上做隔離排演（票 `2026-10-05-rehearse-a-compiled-route-b-wave`）；`docs/article-localization/route-b-bundle.md` 把它和新快照、備份、部署、公開驗收一樣列為各自有票的發布關卡。

### 裸 guides-import（例外）

只用在編譯器 v1 與路線 A 都不收的情況（SKILL.md「先選路線」列的那幾種，例如選到的語系要帶 `aliases` 上線）。發布票先寫明為什麼不走編譯器，站主看過再開始；它沒有 journal，擋不住 dry-run 與 `--publish` 之間的來源變動。照 skill `content-pipeline` 的 `publish-runbook.md` §3–§5，`--locale` 只列要上的語系：

1. 預檢同上第 1 步。
2. `guides-import --slug <slug> --locale en --locale ja --locale ko --locale zh-CN --dry-run`：預期每個新語系一個 `create`、`publish: true`，taxonomy 只有預期的變化。另跑一次 zh-TW 的 dry-run，應是 `unchanged`。
3. 用有選項的提問讓站主選（例如「先 pg_dump 再發布 4 個語系」）；整庫 `pg_dump -Fc` 放主機 `/root/`，確認 TOC 讀得出來。
4. 同一指令換成 `--publish --actor-email <ACTOR_EMAIL>`；新語系走 `start_translation` 再 `publish_locale`，`created`／`published` 只有這幾個語系、`failed: null`。
5. 上面的第 6、7 步，然後再跑第 2 步的 dry-run：全部 `unchanged`、`publish: false`。
