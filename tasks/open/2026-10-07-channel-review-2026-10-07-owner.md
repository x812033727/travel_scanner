---
id: 2026-10-07-channel-review-2026-10-07-owner
title: Channel review 2026-10-07: owner decisions and Studio checklist
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-07T15:24:59Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/channel-review-20261007
---

# Channel review 2026-10-07: owner decisions and Studio checklist

## Why

2026-10-07 對 @Mokaair（開台 11 天、18 支、3 位訂閱、742 次觀看）做了一次完整診斷，報告在 `docs/videos/channel-review-20261007/README.md`。結論：訂閱換算（約 0.4%）在同類頻道的中位數到 P75 之間，異常的是觀看量；產線把答案抽掉再把人送回文章；觸及的槓桿（頻道頁、站內互導、Shorts、縮圖主體、上架節奏）都還沒拉。報告 §2.4 列了 12 條互相矛盾、不拍板兩邊都不會動的決定，§6.1 列了站主本週在 Studio 與後台要做的事，§6.3 是之後四週要看的五個數字與門檻。這張票是把那些「只有站主能做」的事收在一處，不是工程票。

## Definition of done

- [ ] 站主對 §2.4 的 12 條逐條寫下決定（縮圖放不放 logo／介面截圖、固定吉祥物、每章一個 screencast 景、一支一個比喻世界、燒 zh-TW 字幕、片頭長度、系列名後綴不編號、節奏在 DESIGN／STORY／HANDS-OFF 三選一等），存成 `docs/videos/channel-review-20261007/DECISIONS.md`，拍板的項目各自開工程票。
- [ ] §6.1 的 Studio 清單做完：橫幅標語與說明前 45 字改成 AI 工具題、頻道關鍵字、未訂閱者預告片、3 個系列播放清單並勾官方系列、精選區塊、18 支置頂留言與結束畫面、第三個 hashtag 統一；開 Studio 自動配音；配樂床與音效組放進 `_music`／`_sfx` 並填 `slides_music_track`／`slides_sfx_set`。
- [ ] 把 `2026-09-27-ai-video-batch-first-week-analytics` 的範圍擴到已公開的 18 支，匯出曝光／CTR／前 30 秒留存／平均觀看比例／訂閱來源／流量來源，照 §6.3 的門檻判讀，結果寫回本目錄。
- [ ] 寫下頻道級的觀眾定義與立場（正式站 `channel_stance` 自 09-29 起空白），之後每支企劃先決定系列再寫稿。

## Steps

- [ ] 讀 `README.md` §1（一頁摘要）與 §2.4、§6。
- [ ] 逐條拍板、寫 DECISIONS.md；需要工程的另開票並在這裡列出票號。
- [ ] 四週後用 §6.3 的五個數字回答：縮圖 B 版有沒有 Winner、常青題 vs 新聞題的首 7 天曝光、哪個時段觀眾在線、哪些題目的觀眾會留下來。

## How to verify

`DECISIONS.md` 存在且 12 條都有「決定／不做／之後再說」三選一；Studio 頻道頁有預告片、至少 3 個播放清單、關鍵字非空；`/zh-TW/videos` 頁列出影片（見 `2026-10-07-public-videos-api-list-videos-the`）。

## Notes

同日開的工程票：`2026-10-07-public-videos-api-list-videos-the`（站內互導）、`2026-10-07-video-script-rules-outro-with-a`（結尾三句與數字說出口）、`2026-10-07-video-thumbnails-one-subject-six-characters`（縮圖 QA 與版型）、`2026-10-07-video-metadata-title-length-lint-description`（標題 lint、說明欄、UTM、hashtag）。報告的限制：沒有音檔、沒有 Studio 後台數據、樣本極小，所有「這條壓低了訂閱」都只是假設，§7 有完整清單。
