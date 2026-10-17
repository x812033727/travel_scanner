---
id: 2026-10-16-adapt-the-reference-channel-s-five
title: Adapt the reference channel's five most-viewed stories as brand stories
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-adapt
claimed_at: 2026-10-16T17:19:00Z
created_at: 2026-10-16T17:18:24Z
completed_at:
branch: claude/youtube-content-adaptation-57a113
depends_on: []
scope:
  - docs/videos/brand-stories-adapt-20261017
---

# Adapt the reference channel's five most-viewed stories as brand stories

## Why

站主 2026-10-17 要求照參考頻道「黑猫研究院」的方式與故事敘述，挑他觀看最高的五個主題改編，內容與畫面都要比他好、觀看比他高，歸在品牌故事系列。

## Definition of done

- [x] 五集查核過的企劃、獨立審稿與可匯入的 stories.json（docs/videos/brand-stories-adapt-20261017）。
- [ ] 站主決定要不要開拍、排在 A01／B18 試作與已選五支的前或後、預算。
- [ ] 主機唯讀試跑匯入、核准後匯入，工人產出逐字稿、配音、插畫與成片，站主看片並上傳。

## Steps

- [x] 讀頻道「熱門」排序，前五名：Seiko 73 萬、米其林 44 萬、A4 紙 42 萬、杜比 39 萬、哆啦A夢 38 萬（2026-10-17）。
- [x] 五個撰寫代理各寫一集（B25、A41、A42、C21、B26），另五個代理逐來源獨立查核，全部 fixed。
- [x] build.mjs 編出 stories.json；check_story_file 五支零問題。
- [ ] 站主的三個決定（README 的〈製作前要站主決定的事〉）。
- [ ] 匯入與製作。

## How to verify

```bash
node docs/videos/brand-stories-adapt-20261017/build.mjs
```

## Notes

- 逐字稿在內建瀏覽器拿不到：YouTube 對未登入的 get_transcript 回 FAILED_PRECONDITION，timedtext 回空；他的結構改從說明欄、長度與標題歸納。頻道熱門排序可用 ytInitialData 裡「熱門」chip 的 continuation token 打 /youtubei/v1/browse 取得。
- caveats 不在故事雜湊裡；build.mjs 把編者 caveats 與查核 notes 合併，合計上限 800 字，編者那份只寫 notes 沒有的事。
- B26 不能畫任何藤子角色；C21 的數字在杜比 2026 財年 10-K（預計 2026-11）公布後要重核。
