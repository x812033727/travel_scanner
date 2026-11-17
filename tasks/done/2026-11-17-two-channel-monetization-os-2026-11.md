---
id: 2026-11-17-two-channel-monetization-os-2026-11
title: Two-channel monetization OS 2026-11-17
status: done
priority: P2
area: docs
owner: claude-opus
claimed_at: 2026-11-17T17:00:42Z
created_at: 2026-11-17T17:00:33Z
completed_at: 2026-11-17T17:15:26Z
branch:
depends_on: []
scope:
  - docs/videos/channel-os-20261117
---

# Two-channel monetization OS 2026-11-17

## Why

站主 2026-11-17 給了 8 套 YouTube 策略提示詞，並決定分成兩個頻道：@Mokaair 只放奇聞與原來如此，新頻道放 AI 劇、AI 影片與 AI 解說。需要一套有數字依據的營利作業系統。

## Definition of done

- [x] `docs/videos/channel-os-20261117/` 有 README、每個頻道的定位與 100 題、90 天計畫，以及共用的爆款、演算法、製作、營利、分析五份。
- [x] 後續工作開成看板票。

## Steps

- [x] 讀報表分析與公開清單（`yt-dlp`）；查 YPP 現行門檻與 2027 改制、政策、競品。
- [x] 寫文件、開 5 張後續票。

## How to verify

`npm run check:tasks`；文件裡的數字都對得回 `channel-review-20261111-promotion` 或 YouTube 說明頁。

## Notes

- 雲端 session 沒有影片工具權杖，`youtube-reports` 讀不到。自然數字用 11-11 的分析。
- 奇聞 S 軸公開觀看看起來很高（中位數 1,550），但那是付費帶來的；自然觀看每支只有 29–119 次。
- 站台只能連一個 YouTube 頻道（`VideoYoutubeConnection` 有 `CHECK id = 1`）。
- YouTube 2027-02-01 起，新加入 YPP 的頻道要 8,000 小時（answer/12843009）。
