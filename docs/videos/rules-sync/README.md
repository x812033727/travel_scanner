# 規則與教訓同步到雲端硬碟

站主 2026-11-10：「幫我規劃將教訓與規則都放雲端，共用區與每一個的個別的；共用區又有分是奇聞跟原來如此，還有個別的
AI劇」「這樣以後只要有一個更新就不怕漏了」。

**正本只有一份，在這個 repo。** 製作 session 讀的是 repo 裡的 skill 和文件，所以規則、教訓都改在 repo；雲端硬碟上是自動同步的
唯讀副本，每個檔案開頭都寫著正本在哪裡。不要在雲端硬碟改：下一次同步會把它換回 repo 的版本（被換掉的那份會進 `_舊版`）。

## 雲端上的樣子（`AI/備份/AI劇/`）

```
AI劇/
  _共用規則/                         ← 第 0 層：所有 AI 劇
    目錄.md                          ← 自動產生：每份副本 ← repo 正本
    規則/  animation-preproduction/、animation-camera/、animation-production/、minimax-h3-*/、BACKUP.md…
    教訓/  教訓.md（lessons/shared.md）、錯誤目錄、檢討、H3 教訓
  奇聞檔案局/_規則與教訓/             ← 第 1 層
    規則/  curio-episode/、history-curiosity/、解說系列共用/（explainer-series，和原來如此各放一份）
    教訓/  教訓.md、解說系列共用教訓.md、w03-lessons.md
    批次紀錄/
  原來如此事務所/_規則與教訓/          ← 第 1 層：so-thats-why/、解說系列共用/、教訓…
  種田娶妻打天下/_規則與教訓/          ← 第 1 層：設定、大綱、分鏡規則、第一季檢討…
  種田娶妻打天下（真人版）/_規則與教訓/ ← 第 1 層：r2 角色與場景設定、原作設定
  恁祖媽今年18/_規則與教訓/            ← 第 1 層：設定、各季、試鏡決定
  <劇>/<集數>/教訓/<slug>-NOTES.md    ← 第 2 層：單集的製作紀錄（NOTES、PRODUCTION-NOTES、production-record、lessons）
```

做一集時讀：`_共用規則/`、該劇的 `_規則與教訓/`、上一集的 `教訓/`。

## 以後怎麼更新

- **學到教訓**：寫進 `docs/videos/lessons/` 對應的那一份。所有劇都會遇到的寫 `shared.md`，奇聞和原來如此都會遇到的寫
  `explainer.md`，只跟一部劇有關的寫那部劇的（`curio.md`、`sothatswhy.md`、`zhong-tian-qu-qi.md`、`zhong-tian-qu-qi-r2.md`、
  `tai-nainai.md`）。單集的寫在那一集資料夾的 `NOTES.md`。
- **規則改了**：改 repo 裡的正本，合併後一小時內雲端就會更新。
- **教訓變成正式規則**：搬進規則檔，教訓檔留一行「已升為規則：<檔案>」。
- **新增一份規則檔**：在 `manifest.tsv` 加一列。放在 `watch.txt` 列出的位置卻沒有加的，`npm run test:docs-videos` 會失敗，
  PR 合併不了，所以不會漏。新增一部劇或一個系列：`watch.txt` 加它的規則資料夾，`manifest.tsv` 加去處，`lessons/` 加一份教訓。

## 對照表（`manifest.tsv`）

一列一條：`pattern`（repo 路徑，可用 `*`、`**`、`{a,b}`）、`drive`（雲端資料夾；結尾是 `.md` 就是指定檔名；`{episode}` 依資料夾名
算集數，規則和備份相同；`-` 是刻意不傳）、`except`、`note`。一個檔符合幾列就傳到幾個地方，所以共用的東西可以兩邊各放一份。
pattern 的固定開頭之後的路徑會原樣保留。

## 同步怎麼跑

```bash
node docs/videos/rules-sync/sync.mjs --dry-run      # 只列出會放哪裡
# 主機（rclone 只在 worker 映像裡）：
node docs/videos/rules-sync/sync.mjs --docker-image travel-scanner-video-worker:local --conf-dir /etc/travel-scanner/rclone-videos
```

- 讀 `origin/main`（先 fetch），不看工作目錄在哪個分支；也可以 `--ref` 指定。
- `rclone sync` 只動它管的資料夾：`AI劇/_共用規則/`、`AI劇/*/_規則與教訓/`、`AI劇/*/*/教訓/`。其他地方（成片、製作檔）一律不碰。
  這三種資料夾是同步專用的，不要手動放東西進去；放了會在下一次同步被移到 `_舊版`。
- 被換掉或 repo 已刪除的檔，移到 `AI劇/_舊版-規則同步/<UTC 時間>/`，不會真的刪。
- 同步後 `rclone check --one-way` 逐檔核對，印出 `rules-sync: N files, M copies at <commit>, D differences`；D 不是 0 就以非 0 結束。
- 對照表不完整（有檔沒去處、兩個檔要放同一處）時不同步、直接失敗。
- 主機每小時跑一次（root 的 cron，`flock` 防重疊），記錄在 `/var/log/rules-sync.log`。
