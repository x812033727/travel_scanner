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
外框位置（1920×1080）：影片框 (180,390) 與 (1020,390)，各 720×405；訂閱圓心 (960,920)，
半徑 95。Studio 設結束畫面時把元素對齊這些外框。

## 驗證

- 兩包 `branding --install … --dry-run` 都通過（片頭 5 秒／11.9 秒、片尾 21 秒）。
- 以正式 `wrapVideo` 把真實成片（ai-agent-vs-chatbot）最後 360 格正文夾進新片頭片尾：
  總格數 150＋360＋630＝1,140 格，整支 -14.8 LUFS。最後一句講完到正文結束靜音 1.77 秒，
  接著配樂淡入，約 2.8 秒後才出現按讚動畫。
- 畫面表檢查：圖示淡出後外框才淡入、色塊沒有方形邊、字標與原片尾同位置。
- `node --test tools/video/branding/*.test.mjs` 10/10。

## 尚未做

本紀錄只是素材準備與站主核定，不代表正式站已安裝。正式安裝、還沒核准長片的重製與
重新送審、第一次在 Studio 設結束畫面，都是之後各自的步驟，見票
`tasks/open/2026-10-12-lengthen-the-channel-outro-to-20.md`。
