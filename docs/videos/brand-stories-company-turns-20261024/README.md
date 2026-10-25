# 品牌故事：大公司的轉彎（X01–X20）

2026-10-24 站主要求「將 PR 的 X 系列補足後上到後台，結束後關掉 PR」，並採用推薦做法：補到 20 集
（新選 X20），照 C 系列（#1778）以**暫停、只建 planned 列**的方式匯入影片後台。

X01–X15 原本是 Codex 的十五個前製 PR（#1619–#1640），X16–X19 只有分支沒開 PR。它們各自有
treatment、來源矩陣、逐句稿或本機試片，但都不是匯入器讀得懂的六章企劃列。這個資料夾把它們整理成
`episodes/Xnn.json`，每一集由另一個代理逐來源核對並以雜湊綁定（`episodes/reviews/Xnn.json`），
`build.mjs` 在二十份收據都通過後才編出 `stories.json`。`--draft` 產生的 `stories.draft.json` 只供結構
檢查，不可匯入。

匯入只建立系列與二十個 `planned` 集數列：不啟動工人、不付費生成、不上傳、不發布。原分支裡的本機試片、
逐句稿、盲評與插畫停點**不是**這裡的驗收，也沒有搬進 main；需要時從下表的分支與 commit 取回。

## 來源分支

| 集 | 題目 | 原 PR | 分支 | 封存時的 head |
| --- | --- | --- | --- | --- |
| X01 | Adobe Creative Cloud | #1619 | `codex/brand-story-adobe-cc-x01` | `1428ecd23877` |
| X02 | Domino's | #1620 | `codex/brand-story-dominos-x02` | `2d34a532b006` |
| X03 | Netflix | #1621 | `codex/brand-story-netflix-x03` | `c9aa9c85e2f4` |
| X04 | Beats | #1622 | `codex/brand-story-beats-x04` | `2c538c859e98` |
| X05 | Meta | #1624 | `codex/brand-story-meta-x05` | `ca8ad6237948` |
| X06 | WD-40 | #1623 | `codex/brand-story-wd40-x06` | `26d919702018` |
| X07 | GoPro | #1626 | `codex/brand-story-gopro-x07` | `0c12e711d243` |
| X08 | Target Canada | #1625 | `codex/brand-story-target-x08` | `9eadaa06efc3` |
| X09 | BlackBerry | #1629 | `codex/brand-story-blackberry-x09` | `e1f86518ee3f` |
| X10 | eBay／PayPal | #1627 | `codex/brand-story-ebay-paypal-x10` | `80b0ea7fd711` |
| X11 | FedEx | #1630 | `codex/brand-story-fedex-x11` | `02318624aeb7` |
| X12 | Peloton | #1633 | `codex/brand-story-peloton-x12` | `14c0a87f9eda` |
| X13 | Spotify | #1640 | `codex/brand-story-spotify-x13` | `5582424ad3d2` |
| X14 | Airbnb | #1634 | `codex/brand-story-airbnb-x14` | `1e9e455808f4` |
| X15 | Garmin | #1635 | `codex/brand-story-garmin-x15` | `db7121f6d4cd` |
| X16 | Starbucks | 無 | `codex/brand-story-starbucks-x16` | `a22710d6ec55` |
| X17 | Lululemon | 無 | `codex/brand-story-lululemon-x17` | `8bffa99c4e53` |
| X18 | Krispy Kreme | 無 | `codex/brand-story-krispy-kreme-x18` | `4f42a58cb1a1` |
| X19 | Uber | 無 | `codex/brand-story-uber-x19` | `825604299b11` |
| X20 | 本批新選 | 無 | 無 | 無 |

X15 Garmin 和百題題庫的 C15（`story-garmin-smartphone-pivot`）是同一個主角，原分支就是從那一題取材；
兩支 slug 不同，匯入不會衝突，但只該做一支。先開工的那支做完後，把另一支標成不做。

工人只讀不到超過 3 MB 的頁面與 PDF（頁面再長也讀全文）。X11 FedEx 的五份 10-K 都超過 3 MB；查核補了 2023-04-05
的新聞稿與 2024-08-31 季報兩頁工人讀得到的來源，其餘六條必查事實（據點數、風險文字等）仍是 `reviewer_only`。
開工前若找到小的官方頁面，補進來源、重查、重編。

## 規格

沿用品牌故事與 C 系列：`kind: story`、`format: drama`、MiniMax `image-01`、精確
`look: {"preset":"cute-mystery"}`；正文約 10 分鐘、至少 8 分鐘；每 30–45 秒一個鉤子；縮圖左上大字公司名；
圖裡不放商標、可讀字、真人長相。X 開頭的 id 只屬於 `brand-stories-company-turns` 這一部作品，類別可以是
`tech` 或 `everyday`。

## 怎麼重做

```bash
node docs/videos/brand-stories-company-turns-20261024/build.mjs --draft      # 結構
node docs/videos/brand-stories-company-turns-20261024/build.mjs --hash X05   # 查核收據要綁的雜湊
node docs/videos/brand-stories-company-turns-20261024/build.mjs              # 二十份收據都過才寫 stories.json
```

主機上先乾跑 `python -m app.cli video-story-import --series brand-stories-company-turns < stories.json`，
確認二十列都是 create、沒有衝突，再以完全相同的參數加 `--apply`，最後讀回系列 `paused`、二十集 `planned`、
零筆 `video_drama_requests`。
