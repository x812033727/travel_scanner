# Mokaair CC 提示版片頭／片尾素材準備

2026-10-01，站主要求在電影感片頭加入「開啟 CC」提示，並保留按讚、分享、
開啟小鈴鐺。新版素材已完成本機製作、畫面檢查與串接驗證；本紀錄不代表
正式品牌預設已換版。

## 選定畫面與時間

- 片頭維持 5 秒／150 格。沿用 v1 的光門、原 Mokaair Logo 與音效，在 Logo
  下方加入 CC 圖示及「開啟 CC 字幕」提示，不加入品牌標語。提示使用 70px
  深綠字，在 3.35–3.75 秒淡入，保留至片頭結束。
- 片尾維持 3 秒／90 格。沿用 v1 已有的「按讚、分享、開啟小鈴鐺」動畫。
- 共用規格為 1920×1080、30 fps、H.264／AAC、48 kHz 立體聲。
- 兩段合看的 8 秒展示影片只供預覽；安裝包仍是分開的 intro.mp4 與 outro.mp4。
  正文放在兩段之間，字幕仍延後 5 秒，正文總長仍增加 8 秒。

## 產物與驗證

外部目錄：`~/mokaair-work/channel-intro-20260930/brand-package-v2-cc/`。
package ID：`mokaair-brand-package-v2-cc`。媒體、圖片及完整本機收據不進 Git。

| 產物 | 格數／秒數 | SHA-256 |
| --- | --- | --- |
| intro.mp4 | 150／5 | `50a53efa54fe5158a166390c7f46518c052be1af005f99a5f3c57e530b0bb67d` |
| outro.mp4 | 90／3 | `8d9546a6042bdc30e0ac597d4eb1452d9e84edc588424027df8f7378ccecf6b1` |
| bookends-demo-preview.mp4 | 240／8 | `836c273857ac87d13cab7ac524474aca7c5deddce42555a428473d3a53714ceb` |

branding selection hash：
`a27622022d8d9e2f56221a81a1d7443ab241c40a37a515925784511f0416dcdd`。

- 三個 MP4 全部完整解碼通過。原 v1 的兩支影片、manifest 與字型來源均保持
  原 SHA。新版片頭的 236 個 AAC packets 的 bytes、PTS／DTS／duration 全同，
  decoded PCM SHA 亦全同；片尾完整沿用原 bytes。
- 實際檢視 4.6 秒全尺寸畫面與 390px 寬的畫面表。Logo／CC 提示無重疊或裁切，
  3.8、4.6 秒文字清楚；片尾三個圖示及標籤均完整。390px 是本機縮圖檢查，
  不代表實體手機或耳機播放驗收。
- branding CLI `--dry-run --json` 通過，結果 `installed: false`，未建立預設。
- 真實媒體 smoke 將新版與 10 秒測試正文串接成 540 格／18 秒影片。正文來源
  SHA 未變，三段 decoded audio 比對均為 0 mismatches，合計每聲道 864000
  samples；字幕起訖 5000／15000ms，接點為 5、15 秒。
- 既有 branding/core、assemble、installer 測試 14/14 通過；本次無程式碼修改。

外部可重現流程與收據：`render-assets.mjs`、`manifest.json`、
`qa/verification.json`、`qa/installer-dry-run.json`、
`qa/integration/evidence.json`。預覽另有 `preview.html` 與 `poster.png`。

## 套用界線

本次只準備新版素材與預覽，未更改正式 `_branding/current.json`、每支影片的
branding pin 或已核准成片，未重製、送審、上傳或發布影片。現有 v1 部署紀錄
見 `2026-09-30-channel-branding-v1.md`；它不代表本次 v2 已正式啟用。

新版正式安裝是另外一步。素材 hash 會改變，安裝後只影響首次製作的長片；
既有影片採用新版本須依 BRANDING.md 重新盤點及明確選定。
