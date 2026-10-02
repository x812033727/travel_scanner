# 知識科普與小故事：既有企劃與接續票

2026-10-01 整理，基準為 `origin/main` 的 `2596ce7fb5cd832baab2c496fe0ae72962698a4c`。本頁從 repository 的企劃、查核紀錄及任務檔恢復入口；票的狀態是當次看板快照，接手前仍須查看最新 main、PR、worktree 與實際產物。沒有在本次查詢正式後台、工人、YouTube 或付費生成結果。

## 已保存的企劃

| 內容線 | 舊企劃與數量 | 規格／接續入口 |
| --- | --- | --- |
| 知識科普：「原來如此事務所」第一季 | [系列規格](so-thats-why/README.md)、[100 集題庫](so-thats-why/episodes.json)、[五語標題](so-thats-why/titles.json)、[播放清單](so-thats-why/playlists.md)；100 列都是 `fact-checked`，各列 `fact_check` 指向 week1–week15 的完整包 | 商業品牌、生活科學、旅遊文化、科技 AI 各 25 集；8–10 分鐘插畫解說（至少 8 分鐘），每集兩支 Shorts；[每日流程](so-thats-why/operations.md)、[畫風與片頭](so-thats-why/look.md)、[縮圖](so-thats-why/thumbnails.md) |
| 知識科普：第二季 | [100 個候選題](so-thats-why/season2-topics.json)，100 列都是 `checked`；各列 `check` 指向 topic-checks 的題目查核紀錄 | 題目查核已完成，尚須在選題排程時補完整大綱、兩支 Shorts 稿及後台貼用包；見新接續票 |
| 知識科普：第三季 | [100 個候選題](so-thats-why/season3-topics.json)，100 列都是 `checked`；各列 `check` 指向 topic-checks | 和第二季一樣屬於候選題庫；不能把 `checked` 寫成已出片或已排程 |
| 非虛構小故事：品牌、日用品、隱形標準 | [故事路線設計](STORY.md)、[100 個故事企劃與查核](story-plans/brand-stories-100/README.md)、[匯入包](story-plans/brand-stories-100/stories.json)、[50 天順序表](story-plans/brand-stories-100/SCHEDULE.md) | 日常用品 40、亞洲品牌 40、科技軟體 20；12–15 分鐘、只有旁白、卡通靜態圖加運鏡，`format: drama`、`kind: story`；先試 A01 輪子行李箱、B18 迴轉壽司 |
| 獨立直式小故事／漫劇精華 | [Shorts 三條內容線](SHORTS.md)、[直式製作票](../../tasks/open/2026-09-28-video-shorts-worker-drama.md) | 獨立小故事是 `shorts_line: drama`、`source_slug` 空白；從既有故事或漫劇切出的短篇填來源。這條線已有製作票，本次未另造一份題庫 |
| 相關科普：「AI 名詞十分鐘」 | [系列規格](ai-terms/README.md)、[81 個名詞](ai-terms/terms.json) | 約 10 分鐘、不編集數；前三個 token／上下文視窗／RAG 已有文字交接，接續既有試片票 |

以上是 300 個科普題目（第一季完整包、後兩季候選題）＋100 個非虛構故事，另有 81 個 AI 名詞。數量是各清單的列數，跨系列有主題重疊，不能當成 481 支互不重複、已製作的影片。

## 已有票，沿用原交接

| 待辦 | 當次狀態 | 任務 |
| --- | --- | --- |
| 科普片頭三張關鍵影格與站主確認 | in-progress；舊 claim，仍有未勾驗收 | [畫風與片頭（id 保留 mascot，但已決定不用吉祥物）](../../tasks/open/2026-09-28-sothatswhy-mascot-setting.md) |
| 科普每集切兩支 Shorts | in-progress；程式項目已勾，真實出片仍待試片 | [from-episode](../../tasks/open/2026-09-28-sothatswhy-shorts-from-episode.md) |
| 科普 B08、S01、T01 三集試片與實測 | open；依賴前兩張票與配音工人 | [前三集試片](../../tasks/open/2026-09-28-sothatswhy-pilot-3.md) |
| 品牌故事 A01、B18 試作與站主看成片 | open | [兩支故事試作](../../tasks/open/2026-09-28-video-story-pilot.md)、[既有具體試作方案](../work-status-2026-09-29-story-pilot-plan.md) |
| 品牌故事日產 1 支七天，再日產 2 支三天 | open；依賴試作完成 | [品牌故事 rollout](../../tasks/open/2026-09-28-video-story-rollout.md) |
| 直式小故事製作與比例貫穿產線 | open；依賴 Shorts 工人與漫劇試作 | [直式製作](../../tasks/open/2026-09-28-video-shorts-worker-drama.md)、[Shorts 工人](../../tasks/open/2026-09-28-video-shorts-worker-lab.md) |
| AI 名詞前三集成片、實測、語言與上架驗收 | review；文字完成不等於成片完成 | [AI 名詞試片](../../tasks/open/2026-09-29-ai-terms-video-pilot.md) |
| AI 名詞自動接續 | open；依賴 AI 名詞試片 | [工人接名詞](../../tasks/open/2026-09-29-video-worker-takes-next-ai-term.md) |

舊票的 owner、claim 與 scope 保留。claim 過期不表示工作不存在；本頁不替其他持有者結案或釋出。完整產線依賴以各票 `depends_on` 為準。

## 本次補上的缺口

| 新票 | 交付範圍 | 前置 |
| --- | --- | --- |
| [第一季首批庫存與開播交接](../../tasks/open/2026-10-01-sothatswhy-season1-launch-buffer.md) | 以試片實測規劃首 14 集庫存、長片與 Shorts 對應、語言與素材收據、發布提案及後續檢討入口 | 三集試片完成；正式操作與費用仍依已授權範圍執行 |
| [第二季完整製作包](../../tasks/open/2026-10-01-sothatswhy-season2-production-packages.md) | 從 B/S/T/A 26–50 的已查核候選題分批補選題、完整包、兩支 Shorts 稿、五語包裝及 proposed 排序 | 第二／三季題目查核票已 done；逐批交接並檢查跨季重複 |
| [第三季完整製作包](../../tasks/open/2026-10-01-sothatswhy-season3-production-packages.md) | 同上，範圍為 B/S/T/A 51–75，優先序 P3 | 題目查核票已 done；不能自動沿用第二季日期或重複切入點 |

候選題轉製作包是文字工作，可以先進行；是否採用、何時生成與發布，在對應試片／開播交接確認。新票不重做已完成的 300 題查核，不重開品牌故事 pilot／rollout，也不把程式合併當正式驗收。

## 接手方式與狀態界線

1. `npm run tasks -- list` 讀最新隊列；依 task-board 技能查本地 worktree、遠端分支與開著的 PR，再 claim 對應票。
2. 科普先完成畫風／真實 Shorts 與三集試片；品牌故事沿用 A01／B18 方案及原試作票；AI 名詞沿用原三集文字產物與試片 owner 交接。
3. 第一季的 `schedule.csv` 全部是 `PROPOSED_NOT_SCHEDULED`，D1 暫定 2026-11-02；它是舊提案，不能據此宣稱已在 Studio 排程。後兩季也未因題庫查核而取得發布日期。
4. 改稿需重新核對來源、查核及受影響的雜湊；媒體、聲音、上架包、站主觀看與平台持久化逐項留收據。部署、設定、匯入、付費生成與發布依當時具體授權處理。

## 查核依據

- 第一季：[第 36–100 集查核交接](../../tasks/done/2026-09-29-so-that-s-why-fact-check.md)；前 35 集與其餘集的包都可由 `episodes.json.fact_check` 找到。
- 第二／三季：[200 候選題查核交接](../../tasks/done/2026-09-29-so-that-s-why-vet-the.md)，包括 S50/S55、A29/A30/A70、A38/A58 等排程時須處理的重疊。
- 品牌故事：[100 故事企劃完成票](../../tasks/done/2026-09-28-video-story-backlog.md)。
- AI 名詞：[系列與名詞庫完成票](../../tasks/done/2026-09-29-ai-terms-video-series-plan.md)。

本次驗證清單數量、狀態、指向的本地查核檔及本頁連結，並跑 `npm run check:tasks`；未重新查證題目中的外部事實。
