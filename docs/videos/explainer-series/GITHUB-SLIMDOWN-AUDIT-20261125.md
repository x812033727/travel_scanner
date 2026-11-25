# GitHub `docs/videos/` 瘦身與雲端覆蓋盤點報告（2026-11-25）

> **原則**：本報告僅盤點、不動 GitHub 任何檔案。實際刪檔前須逐項以 SHA-256 核對雲端硬碟已有最新一份（0 差異），並留意 VPS `rules-sync` 依賴的少量 `.md` 規則檔。

## 一、現況體檢總覽

- GitHub `docs/videos/` 總計：**`12,243` 檔、`1,577.47 MB`（1.58 GB）**。
- 前 4 大資料夾合計 **`1,406.82 MB`（佔 89.2%）**，絕大多數為巨型 JSON/HTML 題庫快照與 2–6 MB PNG 參考圖，**主機執行程式皆不需在 Git 裡存放它們**。

| 目標資料夾（GitHub） | 檔案數 | 大小 | 最大檔案樣本 | 雲端硬碟現況（`G:\我的雲端硬碟\AI\備份\AI劇\`） | 風險與搬遷前必做動作 |
| :--- | :---: | :---: | :--- | :--- | :--- |
| `docs/videos/so-thats-why/pool/` | 1,750 | **725.07 MB** | `index.html` (31.4MB), `pool.json` (26.7MB), `pool-records.json` (18MB) | 已有 `原來如此事務所\_共用\製作檔\題庫-原來如此事務所-20261113`（11/13 舊快照） | **先補備份**：把最新 `pool/` 以 SHA-256 同步到 `原來如此事務所\_共用\製作檔\題庫-原來如此事務所-20261125\`，核對 0 差異後即可自 GitHub 移除（可立刻省 **725 MB**） |
| `docs/videos/series-plans/zhong-tian-qu-qi/` | 1,838 | **347.61 MB** | `set-liuxi-he-t1.png` (6.4MB), `set-shiqiao-t1.png` (6.3MB) 等大量 PNG | 已有 `種田娶妻打天下\_共用\製作檔\zt-series-media*` 與 `zt-cg-shared` | **拆圖留文或先關 `rules-sync`**：`rules-sync` 目前引用該夾內約 22 個輕量 `.md`（< 1 MB）；其餘 **~345 MB 全是 PNG/JPG 圖片**，逐檔 SHA-256 備份至 `種田娶妻打天下\_共用\製作檔\series-plans-archive\` 後即可移出 GitHub |
| `docs/videos/series-plans/top40-2025-2026/` | 922 | **170.37 MB** | `set-gaozhong-xiaomen-t1.png` (2.6MB), `set-shenjia-chufang-day-t1.png` (2.6MB) | 已有 `恁祖媽今年18\_共用\製作檔\`（需確認是否含全部 PNG） | 同上：`rules-sync` 僅讀 `2025-01-tai-nainai/` 內約 14 個 `.md`；其餘 **~165 MB 圖片與未拍企劃**先 SHA-256 備份至雲端後即可移出 GitHub |
| `docs/videos/history-curiosity/pool/` | 424 | **163.77 MB** | `pool.json` (27.9MB), `pool-sources.json` (25.1MB), `index.html` (25MB) | 已有 `奇聞檔案局\_共用\製作檔\題庫-奇聞檔案局-20261113`（11/13 舊快照） | **先補備份**：把最新 `pool/` 以 SHA-256 同步到 `奇聞檔案局\_共用\製作檔\題庫-奇聞檔案局-20261125\`，核對 0 差異後即可自 GitHub 移除（可立刻省 **164 MB**） |
| **合計（前 4 大項）** | **4,934** | **1,406.82 MB** | — | 皆已有對應 `_共用\製作檔\` 結構，僅需補傳最新差異＋SHA-256 核對 | **安全清出約 1.40 GB（佔 `docs/videos/` 89%）** |

---

## 二、重要連動發現：`rules-sync` 單向同步機制

盤點 `G:\我的雲端硬碟\AI\備份\AI劇\_共用規則\目錄.md` 時發現：
- 目前 VPS 仍有自動排程 `docs/videos/rules-sync`，每小時把 GitHub 規則單向鏡像到 `AI劇/_共用規則/` 與各系列 `_規則與教訓/`（並將未在 GitHub 清單內的檔案搬到 `_舊版-規則同步/`）。
- **防呆做法（本次已落實）**：本次新增的 `FLOW-PRODUCTION-RULES.md` 與 `CURIO-FLOW-CHECKLIST.md`，除放進 `_規則與教訓\規則\` 方便立即查閱外，**正本已同步存於不受 `rules-sync` 覆蓋的 `_共用\製作檔\規則與規範\`**。
- **未來徹底去 GitHub 化的建議步驟**：
  1. 階段 A（零風險、先省 1.40 GB）：把上述 4 大項的靜態題庫池與 PNG 圖片補做 SHA-256 雲端備份後自 GitHub 移除，不動 `rules-sync` 引用的 36 個小 `.md`。
  2. 階段 B（規則完全雲端化）：如確認往後規則全部直接在雲端維護，再比照 2026-11-10 關閉 `VIDEO_BRANCH_MIRROR` 的做法關閉 `rules-sync`，之後 `_規則與教訓/` 就完全以雲端為單一權威。
  3. 階段 C（新集常態）：自 P02 Flow 起，所有新集盲審定稿腳本、`i18n`、審片報告一律直存雲端 `<代碼>\製作檔\<slug>\腳本定稿\`，永遠 0 GitHub Commit。

---

## 三、必須留在 GitHub 的最小清單（不可刪）

1. `apps/api/`、`apps/web/`、`ops/`（網站、後台、Docker 自動部署）
2. `tools/video/`（`cli.mjs`、`lint`、`import`、`templates.mjs`、`dubs`、`automation`）
3. `docs/videos/lexicon.json`（全域發音字典，極小）與 `tools/video/templates/theme.css`
4. 仍在 VPS `video-worker` 自動排程中尚未結案的 `docs/videos/<active-slug>/`（已結案且已走 `import` 的新集不進 GitHub）
