# H07-v2 前製狀態

這是 H07《鐵面人》的獨立系列畫風重製源稿。原版 `curio-h07` 的 `video.json`、旁白、插圖、成片與網址均不變。`build-video.mjs` 從原版已核對稿複製 100 景和 100 個句子 ID，明列 4 句敘事修正並嚴格比對其餘 96 句；`claims.md`、`research.md` 是原版在 2026-10-14 核實的來源筆記副本。原版兩輪覆核仍在 `../curio-h07/verify-1.md` 與 `../curio-h07/verify-2.md`，其畫面判定不直接核准本版新插畫。

## 本版分鏡

- 100 景：正文 99 景、outro 1 景；正文 74 張 `shot` 插畫、25 張數字／姓名／來源／條件卡。插畫比例 74／99 = 74.7%，最多連續 3 張卡。
- `series.json` 指向既有 `history-curiosity` 系列與 MiniMax `image-01`，和 H01-v2 相同的本機解說路線；不建立新作品或人物圖鑑。
- 15 張原版敘事卡改為插畫，原版 `screenshot` 改為有來源的 1698 年證據卡，因為漫劇格式沒有 screenshot 模板。每張 shot 只有一個可讀動作，場景 prompt 不重寫系列畫風；`look` 僅指定 `cute-mystery` 預設。
- 候選身分、四站與約 34 年維持條件說法；黑絲絨只綁 1703 年補記；鐵面具和雙胞胎畫面明置於劇場／小說語境；現代具名在世研究者不畫可辨肖像。
- 新版盲評退回原稿的第 4、5、8 題：第五章首句像分析目錄，開場與正文重述死亡簿無姓名，結尾又重述黑絲絨。已修正 `45164df0`、`baeadea2`、`029cafbf`、`926246b2`；`143be677` 恢復原句。第二輪獨立敘事檢查 11／11 通過，`verify-1.md` 的新句與分鏡史實覆核 PASS。舊 WAV 的最終重核為 zh／en／ja／ko 各 96／100 句可沿用，4 句須重新合成；收據在隔離工作目錄 `audio-transfer-recheck-71b47f50b481.json`，不代表新版音訊已完成。
- 74 張插畫與 25 張卡的獨立畫面查核指出空白姓名欄、原件展櫃、押送方向等問題；`build-video.mjs` 已改掉這些畫面並完成來源綁定重查，付費生圖後仍須逐張檢查。舊版 59 張插畫經聯絡表比對，沒有一張符合 `cute-mystery` 可直接沿用。`node tools/video/cli.mjs lint --slug curio-h07-v2` 實測為 0 errors、0 warnings，正文估約 9.4 分鐘。en／ja／ko 均已對齊新版 100 句與 7 章，4 句新增譯文經獨立覆核。

## 後續製作關卡

整集是 74 張全新插圖。`keyframes --dry-run --takes 3` 於 2026-10-15 顯示 MiniMax image-01 可用、首輪全部約 US$1、每張最多 3 次約 US$3、此版當時已支出 US$0；含少量補畫的整集上限提案為 **US$4，等待站主明確核准**。系列已定畫風，無需逐張重新選畫風。後台已收到新版大綱與劇本，`review-pull` 均回報 `waiting for the owner`；取得兩關核准後才合成 4 句新旁白與開始付費產圖，再評審與送站主分鏡審核。聲音、時間軸、字幕、上架包、後台批准和實際上傳各有自己的雜湊與收據，不能沿用原版核准。

新成片的第一章濃縮從 `0:00` 開始，頻道片頭插在第一章之後（`intro_at: after_first_chapter`）；片尾採 v4-endscreen。`branding.json` 的素材與位置 pin、`checks.json` 的 `intro_at_frame`、配音及字幕時間軸，應在成片階段核實。本階段只建立隔離工作目錄並複製已付費音檔；沒有付費產圖或完成新版成片。

2026-10-15 唯讀檢查：本機 `_branding/current.json` 的 id 為 `mokaair-brand-package-v4-endscreen`；來源沒有 `intro_at` 欄位，預設會解作 `start`。本版在首次 assemble 時必須明確採 `after_first_chapter`，不可只依 current 的預設。`isExplainer(video.json)` 已回傳 `true`，符合有旁白長片的片頭位置規則。
