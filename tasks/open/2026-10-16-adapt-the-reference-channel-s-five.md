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
- 2026-10-17 站主：「先插隊做 B25 Seiko 一支試水溫，做好給我看片再決定其他四支」。主機 live 73887c1a6；`video-story-import --series brand-stories-adapt --limit 1 --episodes-per-day 1` 唯讀試跑只建 B25、零問題，站主選「匯入並開拍」後以同一檔（SHA ede1e5e5…）`--apply`（00:28Z）。工人 00:33Z 開始逐章撰稿。`drama_auto_approve_final=false`，成片停在站主看片關卡。B25 不在 `video_pilot_budgets`（只有 A01／B18 四個試作 slug），US$25 由人盯帳本；逐字稿獨立審查關卡也只綁試作 slug。
- 伺服器依作品建立時間挑下一份工作，卡住的 A01 試作作品（started、工作目錄 blocked）不擋別的作品：`series_max_in_flight` 是每部作品各算。
- 2026-10-17 B25 在說故事盲評卡了十幾輪：聽眾審稿照舊的盲評意見（owner_note）硬加「還記得開頭……」的假回呼、把鏡頭撐過 12 秒；手修七次後 round 19 通過。另修了盲評解析不認 `[id mm:ss]` 的錯（PR #1542，已部署）。
- 2026-10-17 #1548（發音字典釘選）上線後，已開工的故事在配音前卡 `STORY_LEXICON_MIGRATION_REQUIRED`；PR #1550 加了只給「已開始、尚無旁白」故事的遷移（`cli.mjs story-lexicon-migrate`），B25 乾跑 allowed 後套用，快照 097feb61…。
- 2026-10-17 站主：其他四集全部匯入、不限每天一集。`--limit 5` 試跑後套用（新增 A41、A42、C21、B26）；作品 episodes_per_day 改成 null。站主同意把全站 `drama.series_max_in_flight` 從 1 調成 2，讓兩集同時做——**五集做完後要改回 1**（它也影響 wedding-reckoning 等其他作品）。
- B26 不能畫任何藤子角色；C21 的數字在杜比 2026 財年 10-K（預計 2026-11）公布後要重核。
