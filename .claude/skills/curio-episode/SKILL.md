---
name: curio-episode
description: 奇聞檔案局（curio-*）與解說系列開工入口（2026-11-25 路線 B 雲端唯一正本）：所有創作規則、檢核表、教訓、角色設定圖、發音詞庫、題庫與單集定稿腳本皆以 Google 雲端硬碟 AI/備份/AI劇/_START-HERE.md 與 _規則/ 為唯一正本，嚴禁提交新集腳本或素材進 GitHub（0 GitHub Commit）。要做、重做、續做或修任何一集奇聞檔案局或原來如此事務所前，必先讀這個 skill 並執行 npm run vdrive -- pull-rules 拉取雲端最新正本規則，再搭配 youtube-video 工具指令執行 lint、配音與匯入。Make or remake a 奇聞檔案局 (curio-*) or explainer episode from the Google Drive SSOT rules with zero per-episode GitHub commits.
metadata:
  short-description: 奇聞檔案局／解說系列：雲端正本規則入口（npm run vdrive）與 0 GitHub Commit
---

# 奇聞檔案局／解說系列（curio-episode — 路線 B 雲端唯一正本）

> **2026-11-25 站主拍板（路線 B）**：所有規則、教訓、鎖定角色設定圖、發音表、題庫與單集定稿腳本（`video.json`、`script.md`、`brief.md`、`flow-shot-list.json`、`i18n/*.json`、`review/`）**一律以 Google 雲端硬碟為唯一正本（SSOT），單集製作 0 GitHub Commit**。

---

## 一、開工必跑第一步：從雲端拉取最新規則正本

不論你使用的是 Claude Code、Codex 或 Gemini（Antigravity），開工前**必須先拉取雲端最新正本規則**（寫入 `.gitignore` 忽略的本機快取，不會進入 Git）：

```bash
npm run vdrive -- pull-rules curio       # 奇聞檔案局 + 解說系列共用 + 通用（含 lexicon.json 與 ada-canon-v2.png）
npm run vdrive -- pull-rules explainer   # 一次拉奇聞 + 原來如此 + 共用
npm run vdrive -- status                 # 確認偵測到的雲端後端（本機掛載 / rclone / gdrive CLI）
```

若當前環境未掛載本機 repo，請直接讀取 Google 雲端硬碟：
- **總入口地圖**：`AI/備份/AI劇/_START-HERE.md`
- **解說共用總規**：`AI/備份/AI劇/_規則/解說系列共用/FLOW-PRODUCTION-RULES.md`
- **奇聞實戰檢核表**：`AI/備份/AI劇/_規則/奇聞檔案局/CURIO-FLOW-CHECKLIST.md`
- **系列教訓與設定圖**：`AI/備份/AI劇/_規則/奇聞檔案局/`（含 `curio-lessons.md`、`ada-canon-v2.png`）與 `_規則/解說系列共用/explainer-lessons.md`

> 舊版留在 repo 內的規則檔已凍結待遷出，若與雲端 `_規則/` 有差異，**一律以雲端 `_規則/` 為準**。

---

## 二、本機工作夾與工具驗證（0 GitHub Commit）

1. **獨立工作夾**：所有草稿與定稿腳本一律寫在被 `.gitignore` 忽略的本機目錄（如 `work/video-episodes/<slug>/`），**禁止寫入 `docs/videos/` 或提交到 GitHub**（`tools/video-drive-boundary.test.mjs` 會自動攔截）。
2. **腳本驗證**：使用 `--file` 直接檢查本機腳本，不需放進 repo：
   ```bash
   node tools/video/cli.mjs lint --file work/video-episodes/<slug>/video.json
   ```
3. **共用工具手冊**：配音、字幕、縮圖渲染與後台匯入指令的技術用法見 `.agents/skills/youtube-video/SKILL.md` 與 `tools/video/cli.mjs`。

---

## 三、交付雲端與上架後台

1. **成片盲審達標後直傳雲端（含 `腳本定稿/` 與 `SHA256SUMS` 0 差異驗證）**：
   ```bash
   npm run vdrive -- push-episode \
     --series curio \
     --path "<9大分類>/<代碼>/製作檔/<slug>" \
     --from work/video-episodes/<slug>
   ```
2. **推上網站後台審核與上架**：
   ```bash
   node tools/video/cli.mjs import --from <import_pkg>
   ```
   待站主在後台核准與勾選語言後，再執行 `--languages` 與 `--publish --clips ... --recordings ...`。

---

## 四、更新規則或新增教訓（樂觀鎖，不進 GitHub）

經站主確認要更新規則或補充系列教訓時，**不要修改 GitHub 上的舊檔**，改用樂觀鎖推回雲端 `_規則/`（會先比對遠端雜湊防止併發覆寫、自動備份舊版至 `_規則/_history/` 並追加 `_規則/CHANGELOG.md`）：

```bash
npm run vdrive -- push-rule <本機修改後檔案> \
  --target "奇聞檔案局/CURIO-FLOW-CHECKLIST.md" \
  --note "<修改原因摘要>"
```
