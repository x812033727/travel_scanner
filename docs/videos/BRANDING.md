# 頻道片頭與片尾

Mokaair 選定一組 1920×1080、30 fps 的固定素材：5 秒／150 格無標語片頭，
以及 3 秒／90 格的按讚、分享、開啟小鈴鐺片尾。音軌沿用原素材的音效。
媒體和選定的 `manifest.json` 留在 repository 外；Git 只保存工具、測試及規格。

## 安裝與採用

素材包包含 `intro.mp4`、`outro.mp4`、`manifest.json`。manifest 範例：

```json
{
  "schema_version": 1,
  "package_id": "mokaair-brand-package-v1",
  "assets": [
    { "role": "intro", "file": "intro.mp4", "frames": 150, "sha256": "<完整 SHA-256>" },
    { "role": "outro", "file": "outro.mp4", "frames": 90, "sha256": "<完整 SHA-256>" }
  ]
}
```

```bash
node tools/video/cli.mjs branding --install /outside/repo/brand-package-v1 --workdir /video-work --dry-run
node tools/video/cli.mjs branding --install /outside/repo/brand-package-v1 --workdir /video-work
node tools/video/cli.mjs branding --workdir /video-work --json
```

安裝先核對每個素材的 SHA、格數、尺寸、幀率與音軌，再複製到
`<workdir>/_branding/<branding_hash>/`，最後原子更新 `_branding/current.json`。
舊的 current 設定保留在 `_branding/history/`。安裝不改動既有影片、不送審，也不發布。

第一次 `assemble`／`compile` 的長片採用當時的 current，成功成片後在該片工作目錄
寫入 `branding.json`。之後只讀這份 pin；更新 current 不會讓舊片重新排隊。
沒有 pin 的既有成片保持原樣；`--force` 也不表示改用新品牌素材。

已由站主選定、仍未核准的既有成片，明確指定採用：

```bash
node tools/video/cli.mjs assemble --slug VIDEO --workdir /video-work --adopt-branding
node tools/video/cli.mjs captions --slug VIDEO --workdir /video-work
# 有選多語配音時，先重建配音再產字幕；既有有效逐句 TTS 快取會沿用。
node tools/video/cli.mjs dub --slug VIDEO --workdir /video-work --locale en,ja,ko
node tools/video/cli.mjs captions --slug VIDEO --workdir /video-work
node tools/video/cli.mjs qa --slug VIDEO --workdir /video-work
```

只有新成片通過品管後，才重新執行 `review-push --gate final --manual-review`。
這次重製使用 `--manual-review`：仍執行並保存機械品管，送審時將報告放在
`manual_review_qa` 而非供自動核准讀取的 `qa`，並標註需站主重新審看。
不改動全站自動核准設定；之後一般新片仍按站主既有政策送審。
新 MP4 必須重新由站主看過，原本的 MP4 核准不會核准另一組 bytes。
`--adopt-branding` 拒絕 Shorts、已上傳／已結束、已有成片或發布核准紀錄、已有上架包的影片。
合集使用 `compile --adopt-branding`，不呼叫 `assemble`。

## 時間軸與檔案

| 檔案 | 時間軸／責任 |
| --- | --- |
| `timeline.json`、`narration.wav` | 正文，保持 TTS 快取與旁白核准不變 |
| `build/body.mp4` | 本次包裝前的正文；SHA 寫入 checks，供合集核對 |
| `final.mp4` | 片頭＋正文＋片尾；影片規格與響度再次檢查 |
| `checks.json` 的 `branding` | 素材 hash、150／90 格偏移、正文格數及正文檔 SHA |
| `captions/manifest.json`、`upload/metadata.json` | 綁定 `branding_hash`，拒絕沿用別版時間軸 |
| `dubs/<locale>/narration.wav` | 配音正文；fit 仍對正文窗口計算 |
| `dubs/<locale>/timeline.json`、上傳音軌 | 包含片頭片尾的實際時間軸與相同音效 |

字幕與第二章以後的章節延後 5 秒；第一章從 `00:00` 開始，包含片頭。
不另外建立只有 5 秒的章節。配音最後一句字幕在正文結束時截止，片尾不殘留正文字幕。
總格數增加 240；敘事節奏的品管仍只計正文。

合集先核對各集已核准 `final.mp4` 的 SHA，再核對 `checks.branding.body_sha256`，
只拼接正文。各集字幕先扣掉自己的片頭時間，放入合集後，再加合集自己的片頭時間。
完整合集只播放一次頻道片頭與一次頻道片尾。

## 上線紀錄

程式修改、素材安裝、正式 worker 啟用、既有片重製、重新送審與發布是不同步驟。
本規格不是部署或發布收據。正式套用前重新取得候選清單，排除已核准、已發布、
已刪除及 Shorts，並核對是否有同時運作的影片／語系 worker。
將實際套用 slug、前後成片 SHA、字幕／章節／音軌驗證、新的待審紀錄及回讀結果
保存在外部工作目錄。API/檔案檢查不能代替站主驗看或手機驗聽。

## 已核准、尚未上傳的長片換版

已核准成片使用獨立的 owner renewal 流程。它保留原核准決策與附件，將舊的
final／publish／languages／dubs 標為 superseded，再建立必須人工審看的新 final。
不使用 `--force` 改 pin、不刪除批准紀錄，也不由一般 import 偷換已核准語言包。
已記錄 YouTube id、上傳／同步歷史、排程、刪除紀錄或進行中的 VPS job 仍會拒絕。
`on YouTube` 是產線的下一步；只有單一明確 `on_youtube.done=false` 才表示尚待上傳。
正式執行前還需核對完整頻道影片與外部操作紀錄，避免漏掉未回填的人工上傳。

候選目錄至少包含 `meta.json` 與 `final.mp4`，可附 `thumbnail.png`／`.jpg`／`.jpeg`
及 `zh-TW.srt`。先把原核准完整影片、保留正文與新 branding pin 放在 repository 外，
以工具憑證暫存附件。下列操作會寫入網站附件儲存，正式站須另獲明確授權：

```bash
node tools/video/review/renewal.mjs stage \
  --from /outside/candidate --out /outside/new-staged-directory \
  --original /outside/original-approved-final.mp4 \
  --body /outside/retained-body.mp4 --branding /outside/branding.json
```

`stage` 讀取目前原 final id/hash，核對原檔、正文與片頭片尾 SHA，檢查新片長是
正文加新片頭片尾，產生預覽並分段暫存附件。它只在全新的輸出目錄建立
`renewal-candidate.json` 和檔案副本；不 report、送審、核准或改原工作區。
正文 hash 是來源追溯，片長檢查不等於證明畫面或聲音完全相同，仍需人工審看。

站主在後台影片詳情的「成片換版」選取該 JSON，可另選同目錄 `preview.mp4`。
預覽先在瀏覽器核對收據的大小與 SHA，再本機播放；不會因選檔自動上傳。
按「核對目前審核」、填換版原因，再按「送出新版，交由我審看」。送出前重新 GET
版本與原 final id/hash，POST 只送一次；之後再次 GET 影片確認新 id/hash 確為 manual
pending 才顯示成功。版本衝突或不明網路結果須回讀現況，不自動重試。

需要 CLI 時可用 `submit --receipt /outside/staged/renewal-candidate.json --reason TEXT`，
站主目前 session 只由 `MOKAAIR_OWNER_SESSION` 讀取，不能存入收據或貼到終端紀錄。
預設 `MOKAAIR_SITE=https://mokaair.com`；憑證只送往驗證過的 origin，不跟隨 redirect。
網站操作較適合一般站主。新 final 待審後仍須於審片卡確認畫面、CC 提醒及片頭正文接點，
人工核准與後續上傳是另外的決策。

**本階段沒有自動切換正式 worker 的工作目錄。** 新 final 核准後，舊工作區仍會被
producer 的 final SHA、branding、原語及外語字幕偏移／章節驗證擋住。只有具備完整
可信 timeline/checks 的新套件才可送出帶新 final id 與 source manifest 的
publish／languages／dubs；canonical gate proof 的 SHA 也必須等於送審附件。
純外部 imported／legacy 成片不得假造 timeline；合集先保持停止接續。
正常工作區採用、外部人工上架包交接與合集來源驗證另列
[換版核准後交接任務](../../tasks/open/2026-10-01-hand-off-owner-approved-renewed-finals.md)。
建立待審入口不代表這些影片已完成交接、上傳或發布。
