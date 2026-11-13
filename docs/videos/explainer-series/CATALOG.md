# 奇聞檔案局與原來如此事務所：各集總表

由 `docs/videos/ai-drama-drive/catalog.py` 產生（2026-11-13 21:22 UTC），不要手改；要更新就重跑：

```bash
python3 docs/videos/ai-drama-drive/catalog.py   # 自動選用 rclone (videobackup:AI劇) 或 gdrive CLI
```

同樣的資料在 [`catalog.json`](catalog.json)，雲端硬碟 `AI劇/<系列>/_總表/` 有一份唯讀副本。
題庫與備份的紀錄在 [`../ai-drama-drive/BACKUP-LOG.md`](../ai-drama-drive/BACKUP-LOG.md)。

## 欄位從哪裡來

| 欄位 | 來源 | 要重製時怎麼用 |
| --- | --- | --- |
| 分類、雲端位置 | 雲端硬碟 `AI/備份/AI劇/<系列>/<分類>/<代碼>/` | 奇聞檔案局分 9 類（`H-歷史懸案` 等）、原來如此事務所分 7 類（`物理化學與日常材料` 等）。上架包（final.mp4、字幕、配音、縮圖、metadata.json）在集數資料夾第一層；`製作檔/` 是做片 session 傳的全部檔案；`主機檔/` 是主機重做片頭片尾時的輸入與輸出；`教訓/` 是該集 NOTES；`_舊版/<時間>/` 是被取代的舊檔 |
| slug、YouTube ID | 該資料夾的 `backup.json`（主機 worker 寫的） | 後台與 YouTube 用 slug 和 ID 找到同一支片 |
| 其他版本的 YouTube ID | repo 的交付紀錄（`catalog.py` 的 `IDS_FROM_DOCS` 列了出處）與 `video.json` 的 `youtube.video_id` | 2026-11 主機開始寫 `backup.json` 之前上傳的舊版、2026-10-12 的重剪版。後台才是正本，這裡缺的到後台「影片」查 slug |
| 公開 | `metadata.json` 的 `privacy_status` | 上架包要求的公開設定；實際是否已公開以 YouTube Studio 為準 |
| 版本 | slug 結尾（`-v2`、`-v3`；沒有就是 v1） | 重製版是新 slug；舊版的 docs 仍在 repo |
| 畫風 | repo `docs/videos/<slug>/video.json` 的 `look.preset` | `cute-mystery`（奇聞）與 `cute-cartoon`（原來如此）是系列現在的新版畫風，其他（`custom`）是舊版 |
| 縮圖版型 | `video.json` 的 `thumbnail.layout` | 奇聞 2026-11-10 起不寫就是新版 `e`；寫 `d` 是刻意保留舊版 |
| 旁白聲音 | `video.json` 的 `voice` | 目前兩個系列都是 Gemini `Sulafat` |
| 外語配音 | 雲端 `dubs/` 檔案日期 | 2026-11-12 前做的是 Gemini；當天起工具預設用 MiniMax，標「推定」，要確定看主機的配音 `timeline.json` 的 `voice_provider`（docs/videos/DUBS.md） |
| 片頭片尾 | `metadata.json` 的 `branding_hash` 前 12 碼 | 同一個 hash 是同一組片頭片尾；重做片頭片尾要換成現在那組 |
| repo 文件 | `docs/videos/<slug>/`，同一個代碼（H01、P14）的各版本都列 | 腳本、查核、brief、NOTES；沒有就是在主機或別的分支做的，查雲端 `製作檔/`。雲端資料夾沒有上架包時，畫風與旁白取最新版本的 `video.json` |

## 奇聞檔案局

共 62 列：已上架（有 YouTube ID）22 集。題庫在 `docs/videos/history-curiosity/pool`。

| 分類 | 雲端位置 | slug | 版本 | 狀態 | YouTube | 其他版本的 YouTube ID（repo 紀錄） | 公開 | 畫風 | 縮圖 | 旁白 | 外語配音 | 片頭片尾 | 成片日期 | 雲端有 | 舊版 | repo 文件 | 標題 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| H-歷史懸案 | `H-歷史懸案/H01` |  |  | 只有製作檔或教訓 |  | `curio-h01-recut-20261012=2gdgYmiYTSk`、`curio-h01=efSy-Jxq-s8` |  | cute-mystery（新版） | e（預設） | Gemini Sulafat |  |  |  | 教訓 |  | `docs/videos/curio-h01`、`docs/videos/curio-h01-v2`、`docs/videos/curio-h01-v3` | 瑪麗賽勒斯特號 10 人消失，1872 年勘驗官找不到理由？｜奇聞檔案局 |
| H-歷史懸案 | `H-歷史懸案/H02` |  |  | 只有製作檔或教訓 |  | `curio-h02-recut-20261012=4gJhMFqYqC4`、`curio-h02=6hswTvAftUA` |  | cute-mystery（新版） | e（預設） | Gemini Sulafat |  |  |  | 教訓 |  | `docs/videos/curio-h02-v2` | 羅阿諾克「消失的殖民地」：CROATOAN 到底是什麼意思？｜奇聞檔案局 |
| H-歷史懸案 | `H-歷史懸案/H03` |  |  | 只有製作檔或教訓 |  | `curio-h03-recut-20261012=JjM04OmwBjU`、`curio-h03=b98IdS1MB78` |  | cute-mystery（新版） | e（預設） | Gemini Sulafat |  |  |  | 教訓 |  | `docs/videos/curio-h03-v2` | 通古斯大爆炸：森林倒了，坑在哪裡？｜奇聞檔案局 |
| H-歷史懸案 | `H-歷史懸案/H04` |  |  | 只有製作檔或教訓 |  |  |  | cute-mystery（新版） | e（預設） | Gemini Sulafat |  |  |  | 教訓 |  | `docs/videos/curio-h04-v2`、`docs/videos/curio-h04-v3` | 佳特洛夫帳篷從裡面被割開，9 人離開真的是雪崩嗎？｜奇聞檔案局 |
| H-歷史懸案 | `H-歷史懸案/H05` |  |  | 只有製作檔或教訓 |  |  |  | cute-mystery（新版） | e（預設） | Gemini Sulafat |  |  |  | 教訓 |  | `docs/videos/curio-h05-v2`、`docs/videos/curio-h05-v3` | D.B. Cooper 跳機，FBI 查 45 年還沒真名？｜奇聞檔案局 |
| H-歷史懸案 | `H-歷史懸案/H07` |  |  | 只有製作檔或教訓 |  |  |  | cute-mystery（新版） | e（預設） | Gemini Sulafat |  |  |  | 教訓 |  | `docs/videos/curio-h07`、`docs/videos/curio-h07-v2` | 鐵面人是誰？黑絲絨面具的巴士底獄檔案｜奇聞檔案局 |
| H-歷史懸案 | `H-歷史懸案/H09` |  |  | 只有製作檔或教訓 |  |  |  | cute-mystery（新版） | e（預設） | Gemini Sulafat |  |  |  | 教訓 |  | `docs/videos/curio-h09-v2` | 艾爾哈特消失 89 年，2026 年那座島上找到了什麼？｜奇聞檔案局 |
| H-歷史懸案 | `H-歷史懸案/H24` | `curio-h24` | v1 | 已上傳 YouTube | [BJj0BEQnDGk](https://youtu.be/BJj0BEQnDGk) |  | private | cute-mystery（新版） | e（預設） | Gemini Sulafat | Gemini 8 語 | 416c8768d4d2 | 2026-11-08 | final.mp4、keyframes、recordings、timeline.json、教訓、製作檔 |  | `docs/videos/curio-h24` | 報紙說圖坦卡門的詛咒殺了 9 個人？醫師算完 44 個人的答案｜奇聞檔案局｜CC字幕 |
| L-都市傳說與消失地名 | `L-都市傳說與消失地名/L08` |  |  | 只有製作檔或教訓 |  | `curio-l08-recut-20261012=LQ0pV9vZdeA`、`curio-l08=mLxCEB_wSLk` |  | cute-mystery（新版） | e（預設） | Gemini Sulafat |  |  |  | 教訓 |  | `docs/videos/curio-l08`、`docs/videos/curio-l08-v2` | 為什麼 1991 年兩個英國老先生，承認麥田圈是他們做的？｜奇聞檔案局 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S01` | `curio-s01-v2` | v2 | 已上傳 YouTube | [gkl0vABh1_c](https://youtu.be/gkl0vABh1_c) |  | private | cute-mystery（新版） | e（預設） | Gemini Sulafat | Gemini 8 語 | 39d34ab0d563 | 2026-11-03 | final.mp4、主機檔、教訓 |  | `docs/videos/curio-s01` | 赤壁的火是曹操自己放的？八十萬大軍與他寫給孫權的兩封信｜奇聞檔案局｜CC字幕 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S02` | `curio-s02-v2` | v2 | 已上傳 YouTube | [WOYPoicmnJU](https://youtu.be/WOYPoicmnJU) |  | private | cute-mystery（新版） | e（預設） | Gemini Sulafat | Gemini 8 語 | 39d34ab0d563 |  | 主機檔、教訓 |  | `docs/videos/curio-s02` | 草船借箭不是諸葛亮？史書 38 個字裡，差點翻船的是誰｜奇聞檔案局｜CC字幕 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S03` | `curio-s03-v2` | v2 | 已上傳 YouTube | [cVGdU7yabfc](https://youtu.be/cVGdU7yabfc) |  | private | cute-mystery（新版） | e（預設） | Gemini Sulafat | Gemini 8 語 | 39d34ab0d563 | 2026-11-03 | final.mp4、主機檔、教訓 |  | `docs/videos/curio-s03` | 空城計那天，司馬懿根本不在？二二八年真正被唬住的是張郃｜奇聞檔案局｜CC字幕 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S04` | `curio-s04-v2` | v2 | 已上傳 YouTube | [mYry4W8dqWc](https://youtu.be/mYry4W8dqWc) |  | private |  |  |  | Gemini 8 語 | 39d34ab0d563 | 2026-11-03 | final.mp4、主機檔 |  |  | 周瑜真的被諸葛亮氣死？他 36 歲的死，史書只寫了四個字｜奇聞檔案局｜CC字幕 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S05` | `curio-s05-v2` | v2 | 已上傳 YouTube | [MVpNgwdSZMY](https://youtu.be/MVpNgwdSZMY) |  | private |  |  |  | Gemini 8 語 | 39d34ab0d563 | 2026-11-03 | final.mp4、主機檔 |  |  | 三顧茅廬反過來？同一卷史書的兩個版本，諸葛亮自己上門｜奇聞檔案局｜CC字幕 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S06` | `curio-s06-v2` | v2 | 已上傳 YouTube | [685u6uO2uZ8](https://youtu.be/685u6uO2uZ8) |  | private | cute-mystery（新版） | e（預設） | Gemini Sulafat | Gemini 8 語 | 39d34ab0d563 | 2026-11-03 | final.mp4、主機檔、教訓 |  | `docs/videos/curio-s06` | 關羽刮骨，華佗根本趕不上？小說那一幕晚了至少 11 年｜奇聞檔案局｜CC字幕 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S07` |  |  | 只有製作檔或教訓 |  |  |  | cute-mystery（新版） | e（預設） | Gemini Sulafat |  |  |  | 教訓 |  | `docs/videos/curio-s07` | 張飛長坂橋一聲吼，真相只有 65 個字？｜奇聞檔案局 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S08` | `curio-s08-v2` | v2 | 已上傳 YouTube | [IvogKaRemk8](https://youtu.be/IvogKaRemk8) |  | private |  |  |  | Gemini 8 語 | 39d34ab0d563 | 2026-11-03 | final.mp4、主機檔 |  |  | 木牛流馬真的會自己走？古文寫著「一腳四足」，卻沒附一張圖｜奇聞檔案局｜CC字幕 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S09` | `curio-s09-v2` | v2 | 已上傳 YouTube | [S-HraLI6z2g](https://youtu.be/S-HraLI6z2g) |  | private | cute-mystery（新版） | e（預設） | Gemini Sulafat | Gemini 8 語 | 39d34ab0d563 | 2026-11-03 | final.mp4、主機檔、教訓 |  | `docs/videos/curio-s09` | 桶狹間兩千打兩萬五千，信長的繞路奇襲是誰加的？｜奇聞檔案局｜CC字幕 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S10` | `curio-s10-v2` | v2 | 已上傳 YouTube | [ta-elJsT6Mg](https://youtu.be/ta-elJsT6Mg) |  | private | cute-mystery（新版） | e（預設） | Gemini Sulafat | Gemini 8 語 | 416c8768d4d2 | 2026-11-11 | final.mp4、keyframes、recordings、timeline.json、教訓、製作檔 | 2 | `docs/videos/curio-s10` | 敵在本能寺，光秀真的喊過？一句名言被改寫了 245 年｜奇聞檔案局｜CC字幕 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S11` | `curio-s11-v2` | v2 | 已上傳 YouTube | [OzUv1Dd2XBk](https://youtu.be/OzUv1Dd2XBk) |  | private | cute-mystery（新版） | e（預設） | Gemini Sulafat | Gemini 8 語 | 39d34ab0d563 | 2026-11-03 | final.mp4、主機檔、教訓 |  | `docs/videos/curio-s11` | 長篠三段擊真的有？三千挺鐵砲是誰一筆一筆加上去的｜奇聞檔案局｜CC字幕 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S12` |  |  | 只有製作檔或教訓 |  |  |  | cute-mystery（新版） | e（預設） | Gemini Sulafat |  |  |  | 教訓 |  | `docs/videos/curio-s12` | 關原之戰，家康真的開槍逼小早川倒戈？｜奇聞檔案局 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S13` | `curio-s13-v2` | v2 | 已上傳 YouTube | [QHMl7jN0lUE](https://youtu.be/QHMl7jN0lUE) |  | private | cute-mystery（新版） | e（預設） | Gemini Sulafat | Gemini 8 語 | 416c8768d4d2 | 2026-11-11 | final.mp4、keyframes、recordings、timeline.json、教訓、製作檔 | 2 | `docs/videos/curio-s13` | 真田幸村從沒叫過「幸村」？4 封親筆信，簽的都不是這兩個字｜奇聞檔案局｜CC字幕 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S14` | `curio-s14-v2` | v2 | 已上傳 YouTube | [SZXT8qfnmo8](https://youtu.be/SZXT8qfnmo8) |  | private | cute-mystery（新版） | e（預設） | Gemini Sulafat | Gemini 8 語 | 416c8768d4d2 | 2026-11-11 | final.mp4、keyframes、recordings、timeline.json、主機檔、教訓、製作檔 | 3 | `docs/videos/curio-s14` | 宮本武藏故意遲到兩小時？死後 9 年的碑文，連對手的名字都沒寫｜奇聞檔案局｜CC字幕 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S15` |  |  | 只有製作檔或教訓 |  |  |  | cute-mystery（新版） | e（預設） | Gemini Sulafat |  |  |  | 教訓 |  | `docs/videos/curio-s15` | 伊達政宗真的穿著壽衣去見秀吉嗎？｜奇聞檔案局 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S16` |  |  | 只有製作檔或教訓 |  |  |  | cute-mystery（新版） | e（預設） | Gemini Sulafat |  |  |  | 教訓 |  | `docs/videos/curio-s16` | 秀吉一夜城，其實在書裡蓋了快四百年？｜奇聞檔案局 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S17` | `curio-s17-v2` | v2 | 已上傳 YouTube | [9PFjkI2Zib4](https://youtu.be/9PFjkI2Zib4) |  | private | cute-mystery（新版） | e（預設） | Gemini Sulafat | Gemini 8 語 | 39d34ab0d563 | 2026-11-03 | final.mp4、教訓 |  | `docs/videos/curio-s17` | 信長真的說過「殺了牠」？三英傑的杜鵑三句，出處自己寫著假託｜奇聞檔案局｜CC字幕 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S18` | `curio-s18-v2` | v2 | 已上傳 YouTube | [rbA2JR7bIrc](https://youtu.be/rbA2JR7bIrc) |  | private | cute-mystery（新版） | e（預設） | Gemini Sulafat | Gemini 8 語 | 39d34ab0d563 | 2026-11-03 | final.mp4、主機檔、教訓 |  | `docs/videos/curio-s18` | 拿破崙其實不矮？驗屍量出 168 公分，矮子是誰畫出來的｜奇聞檔案局｜CC字幕 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S19` |  |  | 只有製作檔或教訓 |  |  |  | cute-mystery（新版） | e（預設） | Gemini Sulafat |  |  |  | 教訓 |  | `docs/videos/curio-s19` | 艾菲爾鐵塔 1909 年差點被拆？一份二十年合約的真相｜奇聞檔案局 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S20` |  |  | 只有製作檔或教訓 |  |  |  | cute-mystery（新版） | e（預設） | Gemini Sulafat |  |  |  | 教訓 |  | `docs/videos/curio-s20` | 蒙娜麗莎離開羅浮宮 867 天，警察憑什麼找上畢卡索？｜奇聞檔案局 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S21` |  |  | 只有製作檔或教訓 |  |  |  | cute-mystery（新版） | e（預設） | Gemini Sulafat |  |  |  | 教訓 |  | `docs/videos/curio-s21` | 鬱金香狂熱，其實沒那麼瘋？｜奇聞檔案局 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S23` | `curio-s23-v2` | v2 | 有上架包，未記 YouTube ID |  |  | private |  |  |  | MiniMax（推定） 8 語 | 416c8768d4d2 | 2026-11-13 | final.mp4、keyframes、recordings、timeline.json、主機檔、製作檔 | 1 |  | 航海鐘誤差在十海里內，兩萬英鎊為什麼被拆成兩半？｜奇聞檔案局｜CC字幕 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S24` | `curio-s24-v2` | v2 | 有上架包，未記 YouTube ID |  |  | private | cute-mystery（新版） | e（預設） | Gemini Sulafat | MiniMax（推定） 8 語 | 416c8768d4d2 | 2026-11-13 | final.mp4、keyframes、recordings、timeline.json、教訓、製作檔 | 1 | `docs/videos/curio-s24` | 阿基米德真的光著身子喊 Eureka？最早的紀錄晚了將近 200 年｜奇聞檔案局｜CC字幕 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S25` | `curio-s25-v2` | v2 | 有上架包，未記 YouTube ID |  |  | private | cute-mystery（新版） | e（預設） | Gemini Sulafat | Gemini 8 語 | 39d34ab0d563 | 2026-11-03 | final.mp4、教訓、製作檔 |  | `docs/videos/curio-s25` | 牛頓被蘋果砸到頭？1726 年他親口說的，只有掉下來｜奇聞檔案局｜CC字幕 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S26` | `curio-s26-v2` | v2 | 有上架包，未記 YouTube ID |  |  | private | cute-mystery（新版） | e（預設） | Gemini Sulafat | Gemini 8 語 | 39d34ab0d563 | 2026-11-03 | final.mp4、主機檔、教訓、製作檔 |  | `docs/videos/curio-s26` | 瑪麗皇后真說過「吃蛋糕」？書裡那一天，比她出生早 15 年｜奇聞檔案局｜CC字幕 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S27` | `curio-s27-v2` | v2 | 有上架包，未記 YouTube ID |  |  | private | cute-mystery（新版） | e（預設） | Gemini Sulafat | Gemini 8 語 | 39d34ab0d563 | 2026-11-03 | final.mp4、教訓、製作檔 |  | `docs/videos/curio-s27` | 維京人其實沒戴牛角？出土頭盔 0 件有角，角是誰戴上去的｜奇聞檔案局｜CC字幕 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S28` | `curio-s28-v2` | v2 | 有上架包，未記 YouTube ID |  |  | private | cute-mystery（新版） | e（預設） | Gemini Sulafat | Gemini 8 語 | 39d34ab0d563 | 2026-11-03 | final.mp4、主機檔、教訓、製作檔 |  | `docs/videos/curio-s28` | 司馬光砸的不是缸？最早那一筆，寫在他死後 30 年｜奇聞檔案局｜CC字幕 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S29` | `curio-s29-v2` | v2 | 已上傳 YouTube | [R44IsmWR3V0](https://youtu.be/R44IsmWR3V0) |  | private | cute-mystery（新版） | e（預設） | Gemini Sulafat | Gemini 8 語 | 39d34ab0d563 | 2026-11-03 | final.mp4、教訓 |  | `docs/videos/curio-s29` | 曹沖稱象是假的？孫權 210 年才有象可送，同一招還寫在佛經裡｜奇聞檔案局｜CC字幕 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S30` | `curio-s30-v2` | v2 | 有上架包，未記 YouTube ID |  |  | private | cute-mystery（新版） | e（預設） | Gemini Sulafat | Gemini 8 語 | 39d34ab0d563 | 2026-11-03 | final.mp4、keyframes、timeline.json、主機檔、教訓、製作檔 | 1 | `docs/videos/curio-s30`、`docs/videos/curio-s30-v2` | 唐僧其實是偷渡出國的？貞觀三年那張被撕掉的通緝公文｜奇聞檔案局｜CC字幕 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S31` | `curio-s31-v2` | v2 | 有上架包，未記 YouTube ID |  |  | private | cute-mystery（新版） | e（預設） | Gemini Sulafat | Gemini 8 語 | 39d34ab0d563 | 2026-11-03 | final.mp4、keyframes、recordings、timeline.json、教訓、製作檔 |  | `docs/videos/curio-s31` | 楊貴妃的荔枝，怎麼送到長安？｜奇聞檔案局｜CC字幕 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S34` | `curio-s34-v2` | v2 | 有上架包，未記 YouTube ID |  |  | private | cute-mystery（新版） | e（預設） | Gemini Sulafat | Gemini 8 語 | 39d34ab0d563 | 2026-11-03 | final.mp4、主機檔、教訓、製作檔 |  | `docs/videos/curio-s34` | 薛克頓的船困冰281天，28人憑什麼全部活著回來？｜奇聞檔案局｜CC字幕 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S37` |  |  | 只有製作檔或教訓 |  |  |  | cute-mystery（新版） | e（預設） | Gemini Sulafat |  |  |  | 教訓 |  | `docs/videos/curio-s37` | 79 年龐貝被埋，少年沒上船，憑什麼寫出船上的事？｜奇聞檔案局 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S38` | `curio-s38-v2` | v2 | 有上架包，未記 YouTube ID |  |  | private |  |  |  | Gemini 8 語 | 39d34ab0d563 | 2026-11-03 | final.mp4、主機檔、製作檔 |  |  | 倫敦大火燒到第三天，他為什麼把起司埋進土裡？1666 年的日記｜奇聞檔案局｜CC字幕 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S39` | `curio-s39-v2` | v2 | 有上架包，未記 YouTube ID |  |  | private |  |  |  | Gemini 8 語 | 39d34ab0d563 | 2026-11-03 | final.mp4、主機檔、製作檔 |  |  | 凱撒真說了「連你也，布魯圖斯」？六十多人的密謀，誰聽見了這句｜奇聞檔案局｜CC字幕 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S40` | `curio-s40-v2` | v2 | 有上架包，未記 YouTube ID |  |  | private |  |  |  | Gemini 8 語 | 39d34ab0d563 | 2026-11-03 | final.mp4、主機檔、製作檔 |  |  | 埃及豔后真的被毒蛇咬死？三位古代作者沒有一個看見｜奇聞檔案局｜CC字幕 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S42` | `curio-s42` | v1 | 已上傳 YouTube | [4m0Z_bCLRAk](https://youtu.be/4m0Z_bCLRAk) |  | private | cute-mystery（新版） | e（預設） | Gemini Sulafat | Gemini 8 語 | 416c8768d4d2 | 2026-11-09 | final.mp4、keyframes、recordings、timeline.json、教訓、製作檔 |  | `docs/videos/curio-s42` | 麥哲倫船隊 1522 年返航，天天寫的日記憑什麼少一天？｜奇聞檔案局｜CC字幕 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S43` |  |  | 只有製作檔或教訓 |  |  |  | cute-mystery（新版） | e（預設） | Gemini Sulafat |  |  |  | 教訓 |  | `docs/videos/curio-s43` | 達爾文差點因鼻子上不了船？1831 年他還自己放棄了兩次｜奇聞檔案局 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S44` |  |  | 只有製作檔或教訓 |  |  |  | cute-mystery（新版） | e（預設） | Gemini Sulafat |  |  |  | 教訓 |  | `docs/videos/curio-s44` | 倫敦霍亂，一小片街區十天死 500 多人，拆把手就止住了？｜奇聞檔案局 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S45` |  |  | 只有製作檔或教訓 |  |  |  | cute-mystery（新版） | e（預設） | Gemini Sulafat |  |  |  | 教訓 |  | `docs/videos/curio-s45` | 精神病院裡說實話誰信？1887 年女記者騙過醫師住進去｜奇聞檔案局 |
| S-歷史人物與名場面 | `S-歷史人物與名場面/S48` |  |  | 只有製作檔或教訓 |  |  |  | cute-mystery（新版） | e（預設） | Gemini Sulafat |  |  |  | 教訓 |  | `docs/videos/curio-s48` | 大東號把電纜掉進深海，隔了 13 個月，憑什麼撈回來？｜奇聞檔案局 |
| U-外星太空與未知訊號 | `U-外星太空與未知訊號/U02` |  |  | 只有製作檔或教訓 |  | `curio-u02-recut-20261012=NazQDspY5nk`、`curio-u02=uZ9TlblvrCw` |  | cute-mystery（新版） | e（預設） | Gemini Sulafat |  |  |  | 教訓 |  | `docs/videos/curio-u02`、`docs/videos/curio-u02-v2`、`docs/videos/curio-u02-v3` | 51 區藏了 58 年？1965 年員工通訊就登過它的冠軍｜奇聞檔案局 |
| W-商業與品牌奇聞 | `W-商業與品牌奇聞/B01` | `curio-b01` | v1 | 已上傳 YouTube | [J280HdRMKyk](https://youtu.be/J280HdRMKyk) |  | private |  |  |  | Gemini 8 語 | 416c8768d4d2 | 2026-11-08 | final.mp4、keyframes、recordings、timeline.json、製作檔 | 1 |  | 山葉鋼琴和山葉機車是兩家公司？分出去的營收反而是 5 倍多｜奇聞檔案局｜CC字幕 |
| W-商業與品牌奇聞 | `W-商業與品牌奇聞/B02` | `curio-b02` | v1 | 已上傳 YouTube | [HEjE4-K4Xmc](https://youtu.be/HEjE4-K4Xmc) |  | private |  |  |  | Gemini 8 語 | 416c8768d4d2 | 2026-11-09 | final.mp4、keyframes、recordings、timeline.json、製作檔 | 2 |  | Shimano 一台車都不賣，憑什麼年營收 4662 億日圓？｜奇聞檔案局｜CC字幕 |
| W-商業與品牌奇聞 | `W-商業與品牌奇聞/B03` | `curio-b03` | v1 | 已上傳 YouTube | [zBN57Bznxg0](https://youtu.be/zBN57Bznxg0) |  | private |  |  |  | Gemini 8 語 | 416c8768d4d2 | 2026-11-09 | final.mp4、keyframes、recordings、timeline.json、製作檔 | 1 |  | BBC 前後付 1.3 億鎊，Lonely Planet 為何賠著賣？｜奇聞檔案局｜CC字幕 |
| W-商業與品牌奇聞 | `W-商業與品牌奇聞/W01` | `curio-w01-dolby-licensing` | v1 | 已上傳 YouTube | [CBPfKa_sP_U](https://youtu.be/CBPfKa_sP_U) |  | private | cute-mystery（新版） | e（預設） | Gemini Sulafat | Gemini 8 語 | 416c8768d4d2 | 2026-11-09 | final.mp4、keyframes、recordings、timeline.json、教訓、製作檔 |  | `docs/videos/curio-w01-dolby-licensing` | 杜比不造電視也不造手機，憑什麼 93% 的錢都是授權費？｜奇聞檔案局｜CC字幕 |
| W-商業與品牌奇聞 | `W-商業與品牌奇聞/W02` |  |  | 只有製作檔或教訓 |  |  |  | cute-mystery（新版） | e（預設） | Gemini Sulafat |  |  |  | 教訓、製作檔 |  | `docs/videos/curio-w02-michelin-guide-stars` | 米其林 1900 年的免費小冊子，憑什麼讓城市付錢請它來評？｜奇聞檔案局 |
| W-商業與品牌奇聞 | `W-商業與品牌奇聞/W03` | `curio-w03-garmin-smartphone-pivot` | v1 | 已上傳 YouTube | [WocSVl9j5is](https://youtu.be/WocSVl9j5is) |  | private | cute-mystery（新版） | e（預設） | Gemini Sulafat | Gemini 8 語 | 416c8768d4d2 | 2026-11-07 | final.mp4、keyframes、recordings、timeline.json、主機檔、教訓 | 2 | `docs/videos/curio-w03-garmin-smartphone-pivot` | Garmin 七成生意被手機打趴？營收憑什麼還翻一倍｜奇聞檔案局｜CC字幕 |
| H-歷史懸案 |  | `curio-h06-v2` | v2 | 只在 repo（雲端硬碟沒有這集的資料夾） |  |  |  | cute-mystery（新版） |  | Gemini Sulafat |  |  |  |  |  | `docs/videos/curio-h06-v2` | 柏林運河救起的女人，真是安娜塔西亞嗎？｜奇聞檔案局 |
| H-歷史懸案 |  | `curio-h10` | v1 | 只在 repo（雲端硬碟沒有這集的資料夾） |  |  |  | cute-mystery（新版） |  | Gemini Sulafat |  |  |  |  |  | `docs/videos/curio-h10` | 富蘭克林遠征：船與人，如何從線索中被認出？｜奇聞檔案局 |
| H-歷史懸案 |  | `curio-h11` | v1 | 只在 repo（雲端硬碟沒有這集的資料夾） |  |  |  | cute-mystery（新版） |  | Gemini Sulafat |  |  |  |  |  | `docs/videos/curio-h11` | 伏尼契手稿讀不懂，究竟查清了什麼？｜奇聞檔案局 |
| H-歷史懸案 |  | `curio-h12` | v1 | 只在 repo（雲端硬碟沒有這集的資料夾） |  | `curio-h12=QJVtVFecm7I` |  | cute-mystery（新版） |  | Gemini Sulafat |  |  |  |  |  | `docs/videos/curio-h12` | 三個人失蹤後，燈塔的故事改了哪裡？｜奇聞檔案局 |
| M-奇異現象與自然 |  | `curio-m09` | v1 | 只在 repo（雲端硬碟沒有這集的資料夾） |  | `curio-m09=yGF95x3O9U0` |  | cute-mystery（新版） |  | Gemini Sulafat |  |  |  |  |  | `docs/videos/curio-m09` | 古人怎麼把天空裝進一個盒子？｜奇聞檔案局 |
| U-外星太空與未知訊號 |  | `curio-u09` | v1 | 只在 repo（雲端硬碟沒有這集的資料夾） |  |  |  | cute-mystery（新版） |  | Gemini Sulafat |  |  |  |  |  | `docs/videos/curio-u09` | 1967 年劍橋的怪訊號，為什麼叫「小綠人」？｜奇聞檔案局 |

## 原來如此事務所

共 20 列：已上架（有 YouTube ID）14 集。題庫在 `docs/videos/so-thats-why/pool`。

| 分類 | 雲端位置 | slug | 版本 | 狀態 | YouTube | 其他版本的 YouTube ID（repo 紀錄） | 公開 | 畫風 | 縮圖 | 旁白 | 外語配音 | 片頭片尾 | 成片日期 | 雲端有 | 舊版 | repo 文件 | 標題 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 人體感官與日常行為 | `人體感官與日常行為/P21` | `sothatswhy-p21-car-sickness` | v1 | 已上傳 YouTube | [rdNMK5mL7NI](https://youtu.be/rdNMK5mL7NI) |  | private |  |  |  | MiniMax（推定） 8 語 |  | 2026-11-12 | final.mp4、keyframes、recordings、timeline.json、製作檔 |  |  | 坐車看書，為什麼容易暈？｜原來如此事務所｜CC字幕 |
| 地球天氣與太空 | `地球天氣與太空/P02` | `sothatswhy-p02-cloud-rain` | v1 | 已上傳 YouTube | [rmQ9yD0I6tI](https://youtu.be/rmQ9yD0I6tI) |  | private | cute-cartoon（新版） |  | Gemini Sulafat | Gemini 8 語 | 82263266d425 | 2026-11-06 | final.mp4、keyframes、recordings、timeline.json、教訓、製作檔 | 5 | `docs/videos/sothatswhy-p02-cloud-rain` | 一朵雲裡約有 500 公噸的水，為什麼不會掉下來？｜原來如此事務所｜CC字幕 |
| 地球天氣與太空 | `地球天氣與太空/P04` |  |  | 只有製作檔或教訓 |  |  |  |  |  |  |  |  |  | 製作檔 |  |  |  |
| 地球天氣與太空 | `地球天氣與太空/P14` | `sothatswhy-p14-sky-colors` | v1 | 已上傳 YouTube | [5xf1VoDNXWo](https://youtu.be/5xf1VoDNXWo) |  | private | cute-cartoon（新版） |  | Gemini Sulafat |  | 82263266d425 | 2026-11-07 | final.mp4、keyframes、recordings、timeline.json、製作檔 |  | `docs/videos/sothatswhy-p14-sky-colors` | 同一道陽光，天空為什麼是藍的、夕陽卻是紅的？｜原來如此事務所｜CC字幕 |
| 地球天氣與太空 | `地球天氣與太空/P15` | `sothatswhy-p15-salty-sea` | v1 | 已上傳 YouTube | [YQmMeTzBMPk](https://youtu.be/YQmMeTzBMPk) |  | private |  |  |  | Gemini 8 語 | 82263266d425 | 2026-11-08 | final.mp4、keyframes、recordings、timeline.json、製作檔 |  |  | 河水一直流進海裡，海為什麼還是鹹？｜原來如此事務所｜CC字幕 |
| 地球天氣與太空 | `地球天氣與太空/P23` | `sothatswhy-p23-quake-alert` | v1 | 已上傳 YouTube | [jrKdMbdOscQ](https://youtu.be/jrKdMbdOscQ) |  | private |  |  |  | Gemini 8 語 | 82263266d425 | 2026-11-09 | final.mp4、keyframes、recordings、timeline.json、製作檔 |  |  | 地震已經發生，警報怎麼還能搶先？｜原來如此事務所｜CC字幕 |
| 數位科技與通訊工程 | `數位科技與通訊工程/P01` |  |  | 只有製作檔或教訓 |  |  |  |  |  |  |  |  |  | 製作檔 |  |  |  |
| 數位科技與通訊工程 | `數位科技與通訊工程/P11` | `sothatswhy-p11-old-battery` | v1 | 已上傳 YouTube | [pQHhfq3oXGE](https://youtu.be/pQHhfq3oXGE) |  | private |  |  |  | Gemini 8 語 | 82263266d425 | 2026-11-09 | final.mp4、keyframes、recordings、timeline.json、製作檔 |  |  | 電量還有，手機電池為什麼已經老了？｜原來如此事務所｜CC字幕 |
| 數位科技與通訊工程 | `數位科技與通訊工程/P13` | `sothatswhy-p13-gps-timing` | v1 | 已上傳 YouTube | [1LNOlJ-0938](https://youtu.be/1LNOlJ-0938) |  | private |  |  |  | MiniMax（推定） 8 語 |  | 2026-11-12 | final.mp4、keyframes、recordings、timeline.json、製作檔 |  |  | GPS 差一點時間，位置怎麼差那麼遠？｜原來如此事務所｜CC字幕 |
| 數位科技與通訊工程 | `數位科技與通訊工程/P29` | `sothatswhy-p29-https` | v1 | 已上傳 YouTube | [YIBsFTNnW7U](https://youtu.be/YIBsFTNnW7U) |  | private |  |  |  | MiniMax（推定） 8 語 |  | 2026-11-12 | final.mp4、keyframes、recordings、timeline.json、製作檔 |  |  | 網址多一個 S，資料在路上差了什麼？｜原來如此事務所｜CC字幕 |
| 物理化學與日常材料 | `物理化學與日常材料/P05` | `sothatswhy-p05-down-jacket` | v1 | 已上傳 YouTube | [BirHcIAlfz4](https://youtu.be/BirHcIAlfz4) |  | private | cute-cartoon（新版） |  | Gemini Sulafat | Gemini 8 語 | 82263266d425 | 2026-11-06 | final.mp4、keyframes、recordings、timeline.json、主機檔、教訓、製作檔 |  | `docs/videos/sothatswhy-p05-down-jacket` | 羽絨衣一點熱都不會產生，為什麼穿上就暖？｜原來如此事務所｜CC字幕 |
| 物理化學與日常材料 | `物理化學與日常材料/P06` | `sothatswhy-p06-bubble-film` | v1 | 已上傳 YouTube | [dgoHJAy5kM8](https://youtu.be/dgoHJAy5kM8) |  | private |  |  |  | Gemini 8 語 |  | 2026-11-10 | final.mp4、keyframes、recordings、timeline.json、製作檔 | 3 |  | 泡泡用方框吹也是圓的，顏色又從哪來？｜原來如此事務所｜CC字幕 |
| 物理化學與日常材料 | `物理化學與日常材料/P07` | `sothatswhy-p07-fridge-door` | v1 | 已上傳 YouTube | [Ntv0dahykjk](https://youtu.be/Ntv0dahykjk) |  | private | cute-cartoon（新版） |  | Gemini Sulafat | Gemini 8 語 | 82263266d425 | 2026-11-07 | final.mp4、keyframes、recordings、timeline.json、製作檔 |  | `docs/videos/sothatswhy-p07-fridge-door` | 冰箱門打開，房間為什麼不會變涼？｜原來如此事務所｜CC字幕 |
| 物理化學與日常材料 | `物理化學與日常材料/P18` | `sothatswhy-p18-pencil-diamond` | v1 | 已上傳 YouTube | [e3pnT3eLoUw](https://youtu.be/e3pnT3eLoUw) |  | private |  |  |  | Gemini 8 語 | 82263266d425 | 2026-11-10 | final.mp4、keyframes、recordings、timeline.json、製作檔 | 2 |  | 都含碳，鉛筆芯和鑽石怎麼差這麼多？｜原來如此事務所｜CC字幕 |
| 物理化學與日常材料 | `物理化學與日常材料/P20` |  |  | 只有製作檔或教訓 |  |  |  |  |  |  |  |  |  | 製作檔 |  |  |  |
| 生物動物與植物 | `生物動物與植物/P17` | `sothatswhy-p17-gecko-feet` | v1 | 已上傳 YouTube | [mtfFC-LhM0A](https://youtu.be/mtfFC-LhM0A) |  | private |  |  |  | Gemini 8 語 | 82263266d425 | 2026-11-09 | final.mp4、keyframes、recordings、timeline.json、製作檔 | 1 |  | 壁虎黏得住，怎麼又能走得動？｜原來如此事務所｜CC字幕 |
| 飲食與廚房科學 | `飲食與廚房科學/P08` | `sothatswhy-p08-popcorn-pressure` | v1 | 已上傳 YouTube | [D7CzOweULUs](https://youtu.be/D7CzOweULUs) |  | private | cute-cartoon（新版） |  | Gemini Sulafat | Gemini 8 語 | 82263266d425 | 2026-11-07 | final.mp4、keyframes、recordings、timeline.json、製作檔 | 2 | `docs/videos/sothatswhy-p08-popcorn-pressure` | 山上滾水煮得慢，玉米為什麼又會爆開？｜原來如此事務所｜CC字幕 |
| 建築交通與商業制度 |  | `sothatswhy-b26` | v1 | 只在 repo（雲端硬碟沒有這集的資料夾） |  |  |  | custom（舊版） |  | Gemini Sulafat |  |  |  |  |  | `docs/videos/sothatswhy-b26` | 為什麼超市常把牛奶放在最裡面？｜原來如此事務所 |
| 建築交通與商業制度 |  | `sothatswhy-t26` | v1 | 只在 repo（雲端硬碟沒有這集的資料夾） |  |  |  |  |  | Gemini Sulafat |  |  |  |  |  | `docs/videos/sothatswhy-t26` | 為什麼日本常端飯碗，韓國卻常放桌上？｜原來如此事務所 |
| 建築交通與商業制度 |  | `sothatswhy-t27` | v1 | 只在 repo（雲端硬碟沒有這集的資料夾） |  |  |  |  |  | Gemini Sulafat |  |  |  |  |  | `docs/videos/sothatswhy-t27` | 日本垃圾桶少？旅客調查說了什麼｜原來如此事務所 |
