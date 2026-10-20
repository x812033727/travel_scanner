# 結束畫面片尾素材準備（2026-10-12）

站主要片尾像 https://www.youtube.com/watch?v=P6FBmhdp_YA 那樣：最後約 20 秒留給
YouTube 結束畫面（其他影片、訂閱），並加配樂。站主的決定：

- 畫面由 repo 內的程式產生（`tools/video/branding/outro.mjs`），沿用品牌米白、綠、咖啡色。
- 配樂從 YouTube 音樂庫挑候選給站主選；站主選了 Telecasted〈Golden Hour〉。
- 結束畫面元素：「最新上傳」「最適合觀眾」「訂閱」，在 Studio 設一次、之後從影片匯入。
- 套用到新長片，以及還沒核准的長片（`--adopt-branding` 重製、重新送站主審）。Shorts 不變。
- 第一版預覽站主說「話還沒講完就被卡掉」。那是預覽切正文時多抓了 2 秒；真實成片最後一句
  在正文結束前約 1.8 秒講完（四支 10-07～10-08 成片實測 1.84–1.86 秒）。照站主要求，
  片尾開頭再加 1 秒定格停頓，配樂在停頓中從無聲淡入。修正版站主核定。

## 產物

外部目錄：`~/mokaair-work/channel-outro-20261012/`。媒體與音樂不進 Git。

| 項目 | 值 |
| --- | --- |
| 來源片尾（v2-cc，自正式站唯讀下載） | 90 格；`8d9546a6042bdc30e0ac597d4eb1452d9e84edc588424027df8f7378ccecf6b1` |
| 全頻道片頭（v2-cc） | 150 格；`50a53efa54fe5158a166390c7f46518c052be1af005f99a5f3c57e530b0bb67d` |
| 「原來如此」片頭 | 357 格；`208ff0300b463f6f71f9c059586837accbeb22e28a8eccc7dfad0af6145c5337` |
| 配樂 | Golden Hour – Telecasted，YouTube 音樂庫授權（不需註明出處），2:20 MP3 320 kbps；`ed4d3fabe4cd582366c12942997f3d5c8d5eec5142fecd0f4b594ca1cb106c39`；取 105.5–126.5 秒（曲子自然收尾） |
| 新片尾 outro.mp4 | 630 格／21 秒，-15.8 LUFS；`95ddd436524bb2117cd00093f806ba1d2d2feb1e22def0ac9d607ebf1a4ad123` |
| 全頻道包 `mokaair-brand-package-v3-endscreen` | branding hash `425e6800dde639fbaf6c5b529a459689c232ccbd2258bf156eb3b7ba79d04409` |
| 系列包 `mokaair-sothatswhy-bookends-v2-endscreen` | branding hash `f707b018be95e3488be964915bdd9494894e5cbd75f2ce39abb22a0cef6c1448` |

片尾時間：0–1 秒定格停頓（配樂淡入）、1–4 秒原按讚／分享／小鈴鐺、4–21 秒結束畫面底。
v4 在第 4–5 秒將按讚圖示淡出、卡框淡入；逐格檢查到第 5 秒才有清楚的卡框，
故可點元素使用最後 16 秒（第 5–21 秒），21 秒片尾素材本身不變。
v3 的外框位置（影片框 (180,390)／(1020,390) 各 720×405、訂閱圓心 (960,920) 半徑 95）
在 Studio 放不進去，已由下文 v4 取代。

## 驗證

- 兩包 `branding --install … --dry-run` 都通過（片頭 5 秒／11.9 秒、片尾 21 秒）。
- 以正式 `wrapVideo` 把真實成片（ai-agent-vs-chatbot）最後 360 格正文夾進新片頭片尾：
  總格數 150＋360＋630＝1,140 格，整支 -14.8 LUFS。最後一句講完到正文結束靜音 1.77 秒，
  接著配樂淡入，約 2.8 秒後才出現按讚動畫。
- 畫面表檢查：圖示淡出後外框才淡入、色塊沒有方形邊、字標與原片尾同位置。
- `node --test tools/video/branding/*.test.mjs` 10/10。

## 正式站安裝（2026-10-12 10:35Z）

站主選「現在安裝，重製先給清單」。兩包上傳到工作卷的 `_branding-incoming-20261012/`，
主機上 SHA 與本機相同；以 `docker compose … exec -T video-worker` 先 dry-run 再
`branding --install`（全頻道）與 `branding --series sothatswhy --install`。回讀
`branding --json`：全頻道 `425e6800…`（150／630 格）、系列 `f707b018…`（357／630 格）。
舊設定自動存入 `_branding/history/2026-10-12T10-35-01-804Z-a2762202….json` 與
`_branding/series/sothatswhy/history/2026-10-12T10-35-03-022Z-047ff12a….json`。
安裝時 worker 閒置、沒有全域 STOP、沒有部署暫停檔。

## 既有成片盤點（同一套 `adoptionRefusal` 規則，唯讀）

工作區有成片的 38 支：29 支已核准或已上傳、7 支是匯入／換版交接片（有上架包與 STOP），
都不動。符合的 2 支：

- `utah-stratos-data-center-9gw-who-said`：已重製。`assemble --adopt-branding` 16,128 格
  （150＋15,348＋630）、-14.1 LUFS、TP -1；`checks.branding` 為 `425e6800…`；final SHA 前綴
  `6f17e31dd1c5`。captions 重做、qa 9/11（未過的 pace 與 en/ja/ko 字幕是正文與語言的既有問題，
  與片尾無關），`review-push --gate final --manual-review` 回報 pending，等站主在後台審。
- `icann-ai-tld-agent-preorder-check`：工作區有 Codex 戰役 `production-resume-20261010-3603`
  放的 STOP，不碰。它已 pin 舊版，之後一般重組不會自動換新片尾；那邊釋放後要明確
  `--adopt-branding`。

## Studio 範本與 v4 對齊（同日稍晚）

站主登入 Mokaair 的 Google 帳號後（內建瀏覽器 `authuser=1`，頻道 `UCR0rRWT4blMDUwEMx-TZ57Q`），
在 `oxEtlA8GWas`（SynthID，8:50）設片尾範本時發現 v3 外框放不進 Studio：元素只能放在
安全區（預覽 480×270 的 y 35–228，即 1080p 約 y 140–912），訂閱鈕固定 296 px 不能縮放。
改排一列並由站主同意儲存：左「最符合觀眾喜好」影片 (109,371) 619×349、中訂閱
(812,402) 296×296、右「最新上傳」影片 (1190,371) 619×349，時間 8:45:03–8:50:03（最後 5 秒，
只蓋舊片尾與講完後的空白）。重新開啟編輯器回讀，三個元素與位置都在。

片尾外框改照這些位置畫（`SLOTS`，外框在元素外 5 px），站主看過樣片同意後安裝：
全頻道 `mokaair-brand-package-v4-endscreen`、系列 `mokaair-sothatswhy-bookends-v3-endscreen`，
outro.mp4 SHA `00eb9ccc8449fa8b47de0aab290b8aa7d55b09962c12a127e0f0c9c5f7834396`，聲音與時間同 v3。
猶他那支再用 v4 重組（16,128 格、-14.1 LUFS，final SHA 前綴 `ed292fecfd9a`）。第一次重送被
審片檔案區擋下（507 `video_review_store_full`：19.999／20 GB，大宗是 DevDay 換版 2.0 GB、
Codex 新聞審查 1.1 GB、戰役稽核 1.0 GB）。站主選擇把上限提高到 40 GB：主機 `.env` 加
`VIDEO_REVIEW_MAX_TOTAL_BYTES=40000000000`（改前備份於 `/root/env-backup-<UTC>`，維持 mode 600），
只重建 api 容器；`/health`、`/ready`、公開首頁 200。之後重送成功（manual pending）。
之前那筆 v3 成片的待審是否已被取代，沒有另外回讀確認；站主審片時看 final SHA 前綴 `ed292fecfd9a` 那筆。

新片上架：Studio「片尾」→「從影片匯入」選 `oxEtlA8GWas`，把三個元素的開始時間改成
影片長度減 16 秒。v4 第 4–5 秒仍是按讚圖示與卡框的交接；片尾第 5 秒（第 150 格）
才已清楚，依[逐格檢查紀錄](../../../tasks/done/2026-10-12-correct-v4-youtube-end-screen-timing.md)
設定。私人上傳後須在播放頁確認「最符合觀眾喜好」影片、訂閱及「最新上傳」影片都可點。

## 尚未做

youtube-video skill 上架清單的更新，見票 `tasks/open/2026-10-12-lengthen-the-channel-outro-to-20.md`。
