# S39 R2 作者修稿與獨立覆核交接

日期：2026-10-20。這是**作者自查**，不是獨立盲讀、史料或生成畫面通過報告，也不是語音、插圖或配樂開工核准。R1 獨立意見分別封存於 `/tmp/curio_s39_r1_fresh_blind_seal.md` 和 `/tmp/curio_s39_r1_source_visual_audit.md`；R1 的 [verify-1.md](verify-1.md) 雜湊對 R2 已失效。

## 鎖定版

| 檔案 | SHA-256 |
| --- | --- |
| `video.json` | `f4f57f1a1dd9642fdf39756133b15315d621b349561226d45a683f5832560e86` |
| `script.md` | `ad6e2a208bfba3a6b0fdd3e997e6fe911154e05d43d25f1bd2f726fa7c641dfd` |
| `claims.md` | `4607d070e16f74e8c9d87f665f68a2b8a4c4f83b37eed89847adf98445dbe7c4` |

已從同版 `video.json` 重生 `script.md`；89 句旁白與 `claims.md` 的 89 列 ID、字句一一相同。86 景都是非空白 `shot`，加 1 個片尾，插圖場景佔 86/87；12 個具體 `loops`。`cute-mystery`、Sulafat、系列配樂參數、空白書頁／非血腥插圖提示詞保持一致。估全片 **9:18**，片頭章止約 **00:38**、片尾章起 **08:59**，估故事正文 **8:21**；實際語音時長仍須後驗。

## R1 問題如何修

- 開場停在演員開口前；沿赴會、刺殺、古代敘述、莎劇、後世英譯腳註依次揭曉。刪去 R1 最後的遺體／遺囑岔路，章名改用具體事件。每段懸念有對應答案，不先讀莎劇全句或古代結果。
- `cs049–cs055` 明確是**蘇埃托尼烏斯同一段**：二十三次刺擊間無成句，第一刀時呻吟；後接 `etsi tradiderunt quidam` 的希臘語傳說。`cs036` 保留第一刀之前那聲「這是暴力」，`cs040` 分別標註普魯塔克刀後對卡斯卡的發話；沒有把沉默縮成第一瞬。
- `cs068–cs070` 區分莎劇的拉丁語問句、**英文**最後口頭台詞 `Then fall, Caesar!` 和其後 `Dies` 指示。`cs076–cs082` 把後世英譯正文與編者腳註分開，未把拉丁猜測倒寫入古代原文。
- `cs038–cs039` 不指定有異文的第一刀方位。`cs035` 的插圖改為**辛伯伸手抓袍**；德奇姆斯以短鬍子、馬爾庫斯以圓形銅別針作卡通視覺辨識，均非歷史肖像斷言。正文不描寫遺體搬運或遺囑中的刺客人數。[research.md](research.md) 的 `PL-B` 範圍已補馬爾庫斯聲望與等候段，莎劇欄也明確標出英文尾句。

## 已驗證與未通過的關卡

- `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s39 --json`：**0 error／0 warning**，估 9.3056 分鐘、89 句。
- `npm run test:docs-videos`：**236/236 通過**。
- `npm run check:tasks`：exit 0，僅其他既有任務的 stale／scope 警告。
- `tts --dry-run` 曾顯示 87 個待合成請求、約 2209 字；其後 R2 最後一句微修，該 dry-run 數值只能供規模參考，不是定稿報價。`keyframes --dry-run` 嘗試連站台報價時 `cannot reach https://mokaair.com: fetch failed`；`music --dry-run` 因尚無同稿 timeline 拒絕。**沒有送出付費生成。**
- 依 R1 站台曾報 90 張首次約 US$1.22、最多三次約 US$3.65，86 張若同單價，**估**首次約 US$1.17、最多三次約 US$3.49；另配樂約 US$0.08，合計約 **US$3.57**。這是比例預估，不是 R2 即時站台報價或支出授權；送單前仍須重新取得本版報價與核准上限。

## 下一關

全新讀者僅看本版 `script.md` 和 `narrative --slug curio-s39 --json` 的十三題，先封存逐題 yes/no 與具體證據，再讀本頁及來源。另一位獨立查核者以以上雜湊為準，重新開啟 [research.md](research.md) 所列固定全文，逐句覆核 89 句、86 個插圖提示詞及一對一映射；特別檢查蘇埃托尼烏斯一段的主敘述／希臘語傳說、兩個 Brutus 的辨識、普魯塔克英譯與莎劇英文尾句。兩關都通過後才進入本地委託的音訊關卡；任何稿件變動都需要新雜湊和新讀者覆核。
