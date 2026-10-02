# 五類長片的剩餘階段與接續票

2026-10-02 08:12（Asia/Taipei）從本機任務原文、企劃入口及 Git／PR 資料重讀的快照；Git 基準為 `7c7a917bdc2592c84fb310a3e584f8a1d7c4be78`。此索引保留既有 task 的 ID、owner、status、scope 與未完成驗收，不替持有者釋出或結案。沒有查詢正式後台、生成媒體或核驗 YouTube 持久化狀態；正式進度須由對應產物與站主／平台紀錄證明。

## 目前完成到哪裡

所有五類長片的有效時長見[新版說明](README.md)、[企劃資料](plans.json)與[時長規格](policy.json)：原來較短的企劃以 10 分鐘製作，實際正文及成片至少 8 分鐘；品牌故事保留 13 分鐘製作目標與原 12–15 分鐘規格，AI 名詞保留 9–11 分鐘成片區間。Shorts 維持短片規格。

| 內容線 | 已保存／本次時長修訂的成果 | 仍須完成的階段 |
| --- | --- | --- |
| 第一季 100 題 | [題庫](../so-thats-why/episodes.json)、逐集查核與貼用文字包；新版 10 分鐘有效輸入 | 畫風片頭的真實關鍵影格與站主確認、三集試片與真實 Shorts／語言／上架包、14 集庫存與開播交接。題庫與大綱不代表 100 支完整正文或成片 |
| 第二季 92 採用包 | [92 份獨立審過的文字包](../so-thats-why/season2/README.md)、184 支 Shorts 文字、五語包裝及 proposed 排序；原 100 題處置為 92 採用、8 判重不採用、0 未決；新版六章合計 600 秒預算 | 完整長片逐字稿、配音、圖片、字幕、成片、實測媒體 QA、正式匯入、核准、排程與發布。文字票 `done` 的成果是製作文字包 |
| 第三季 100 候選題 | [100 題候選與題目查核](../so-thats-why/season3-topics.json)；新版 10 分鐘目標 | 原題處置、跨季去重、採用題的完整製作文字包與獨立審稿；之後才是正文與媒體。`checked` 尚未成為採用包或成片 |
| 品牌故事 100 題 | [100 個企劃與逐故事查核](../story-plans/brand-stories-100/README.md)、匯入包及順序提案 | A01／B18 試作、實際旁白與媒體、站主看成片、費用與清晰度實測，再做 1 支／日與 2 支／日的運轉驗收 |
| AI 名詞 81 項 | [系列及名詞庫](../ai-terms/README.md)；`terms.json` 當前為 77 `backlog`、3 `planned`、1 `covered`。token／上下文視窗／RAG 有文字交接 | 三集大綱及媒體關卡、實際 9–11 分鐘、語言與上架包、平台狀態及實測；之後再接名詞庫自動挑題。已覆蓋項目免重做 |

**473 是 `DURATION_PLANS_ONLY` 企劃項目數，不是 473 篇已完成逐字稿、473 次匯入或 473 支成片。** 第二季 92 包的文字審稿、第三季 100 題的題目查核、AI 試片票的 `review`，各自只證明對應階段。任何後台或平台的實際進度，都不能由這些標記推定。

## 第一季：片頭、三集試片與 14 集庫存

### 畫風與三秒片頭

[原票：`2026-09-28-sothatswhy-mascot-setting`](../../../tasks/open/2026-09-28-sothatswhy-mascot-setting.md)

| 欄位 | 原票值 |
| --- | --- |
| status／priority | `in-progress`／P2 |
| owner／claimed_at | `claude-opus`／`2026-09-28T06:50:53Z` |
| branch | `claude/knowledge-series-planning-v84n79` |
| scope | `docs/videos/so-thats-why/look.md` |
| depends_on | 無 |

原 DoD 已勾選[畫風文字規格](../so-thats-why/look.md)：固定插畫、色盤、negative、人物／logo 畫法及片頭／片尾／章節卡。**未勾選的是三張片頭關鍵影格生成、站主確認，以及選定檔名與 SHA256 記錄**，圖檔留 repo 外。原 ID 雖保留 `mascot`，站主已決定不用吉祥物；不可重新做吉祥物。舊 claim 並不等於釋出，續工仍交由原持有者協調。

### B08、S01、T01 三集試片

[原票：`2026-09-28-sothatswhy-pilot-3`](../../../tasks/open/2026-09-28-sothatswhy-pilot-3.md)

| 欄位 | 原票值 |
| --- | --- |
| status／priority | `open`／P2 |
| owner／claimed_at／branch | 均空白，未認領 |
| scope | `docs/videos/so-thats-why/README.md`、`docs/videos/so-thats-why/schedule.csv`、`docs/videos/sothatswhy-b08/`、`docs/videos/sothatswhy-s01/`、`docs/videos/sothatswhy-t01/` |
| depends_on | `2026-09-28-sothatswhy-explainer-preset`、`2026-09-28-sothatswhy-shorts-from-episode`、`2026-09-28-sothatswhy-mascot-setting`、`2026-09-26-video-dubs-worker` |

原 DoD 三項都未勾：完成三支長片、每支兩支 Shorts、五語 CC、四語配音與上架包；逐集記插圖數／重做、花費、token、站主審稿及審片時間、配音放不下的句數；用實測更新成本、產能、開播日與節奏，重排 `schedule.csv`。驗收入口是各集 `status` 已到上架包，且 README 數字有產物／帳本證據；仍須保留實際正文及成片至少 8 分鐘的新版門檻。

其中[每集切兩支 Shorts 的原票](../../../tasks/open/2026-09-28-sothatswhy-shorts-from-episode.md)為 `in-progress`、owner `claude-opus`，程式與文字項目已勾，**對真實長片跑 `from-episode` 出片仍未勾**，原票明確併到這三集試片。程式測試通過不能補勾真出片驗收。該票亦持有系列 README／automation 等 scope；試片接手前要查實際交接與碰撞。

### 首批 14 集庫存與開播交接

[原票：`2026-10-01-sothatswhy-season1-launch-buffer`](../../../tasks/open/2026-10-01-sothatswhy-season1-launch-buffer.md)

| 欄位 | 原票值 |
| --- | --- |
| status／priority | `open`／P2 |
| owner／claimed_at／branch | 均空白，未認領 |
| scope | `docs/videos/so-thats-why/launch/`、`docs/videos/so-thats-why/schedule.csv`、`docs/videos/so-thats-why/operations.md` |
| depends_on | `2026-09-28-sothatswhy-pilot-3` |

原 DoD 五項都未勾：

1. 寫 `launch/README.md`，記三集試片結果、站主選定的節奏／語言／費用上限、順序與未補授權；待定欄位維持待定。
2. 首批 14 集逐集庫存表，包含 source id、長片及兩支 Shorts slug、素材／QA／上架包雜湊與位置、語言、站主觀看結果及剩餘關卡。試片三集計入 14 集。
3. 取得具體生成授權後，14 集及各兩支 Shorts 完成媒體／語言檢查與站主驗收；未獲授權時保留可審閱提案與阻擋，本票不結案。
4. 更新 proposed 排程、長短片關聯、庫存低於 7 集的降頻規則及每 20 集數據檢討；沒有發布授權維持 `PROPOSED_NOT_SCHEDULED`，Studio id／公開時間需平台重讀才填。
5. 明確交接庫存完成、提案待批准、已排程或已公開哪個階段，記下一批、資源及站主審片容量。

原 Steps 的前 14 集提案為 **B08、S01、T01、A08、B06、S09、T05、S02、T02、A01、B01、S03、T03、A02**。D1 `2026-11-02` 是舊提案，不是已排程。原 scope 不包括逐集正文目錄；實際批次需要新增／改正文時，先用精確 scope 的票承接。

## 第三季：100 候選題轉製作文字包

[原票：`2026-10-01-sothatswhy-season3-production-packages`](../../../tasks/open/2026-10-01-sothatswhy-season3-production-packages.md)

| 欄位 | 原票值 |
| --- | --- |
| status／priority | `open`／P3 |
| owner／claimed_at／branch | 均空白，未認領 |
| scope | `docs/videos/so-thats-why/season3/`、`docs/videos/so-thats-why/season3-topics.json` |
| depends_on | [`2026-09-29-so-that-s-why-vet-the`](../../../tasks/done/2026-09-29-so-that-s-why-vet-the.md)，已 `done` |

原 DoD 五項都未勾：

1. `season3/README.md` 留 100 原 ID、查核報告、採用／延後／換角度／不採用處置與理由、批次及入口；未決處置未清完不能結案。
2. 每個採用題有完整製作文字包，包含來源／確認日、主張限制、章節大綱、畫面／縮圖注意、兩支 35–55 秒 Shorts 稿、長短片標題／說明與後台前提／備註。
3. 五語包裝與 proposed 排序獨立保存，不沿用第二季日期、不改前兩季題號或第一季排程。
4. 跨季重複有明確處置，不同代理完成查核與聽眾審稿；新事實重新找一手來源，保留包／審稿收據與原 `check` 入口。
5. 回寫 `season3-topics.json` 的包入口與處置，保留原查核及延後條件；沒有實際媒體／平台驗收時仍是文字包階段。

原票第 2 項寫「7–9 分鐘章節大綱」是舊規格，**後續按本次新版用 10 分鐘章節預算、實際正文及成片至少 8 分鐘**；Shorts 仍是 35–55 秒。小批次先查 S55／S50、A70／A29／A30、A58／A38 等重複，不以 100 候選題數直接推定 100 採用包。需要修改 `topic-checks` 時，原票要求另列精確 scope。

## 品牌故事：兩支試作與運轉驗收

### A01 輪子行李箱、B18 迴轉壽司試作

[原票：`2026-09-28-video-story-pilot`](../../../tasks/open/2026-09-28-video-story-pilot.md)

| 欄位 | 原票值 |
| --- | --- |
| status／priority | `open`／P1 |
| owner／claimed_at／branch | 均空白，未認領 |
| scope | `docs/videos/STORY.md` |
| depends_on | `2026-09-28-video-story-worker`、`2026-09-28-video-story-backlog`、`2026-09-28-video-story-api-policy-languages` |

原 DoD 四項都未勾：正式主機從清單做到兩支「可以上架」且站主看過成片；[故事路線](../STORY.md)填逐支長度、鏡數、圖數／重做率、階段秒數、帳本費用、訂閱 token 與 `final.mp4` 大小；用實測比較 1K／2K 清晰度及成本，由站主決定；卡點修復或開票，按實測更新上限。

原票驗收仍保留 **1920×1080、30fps、成片 720–900 秒、媒體 QA／motion 全過、每支總花費不超過 US$25**。既有[A01／B18 具體試作準備方案](../../work-status-2026-09-29-story-pilot-plan.md)有依賴與成本／授權交接；本次只核對原票與準備方案，原票的真影片與站主觀看驗收仍未勾。13 分鐘企劃與已查核故事不證明真旁白已達長度，原票留有估計語速與實際語速的差距。

### 日產一支七天，再日產兩支三天

[原票：`2026-09-28-video-story-rollout`](../../../tasks/open/2026-09-28-video-story-rollout.md)

| 欄位 | 原票值 |
| --- | --- |
| status／priority | `open`／P2 |
| owner／claimed_at／branch | 均空白，未認領 |
| scope | `docs/videos/STORY.md` |
| depends_on | `2026-09-28-video-story-pilot`、`2026-09-28-video-story-tidy-finished` |

原 DoD 四項都未勾：每天一支連續七天都進「可以上架」，沒有卡超過一天且磁碟／額度不持續惡化；改每天兩支後連續三天達量；保存這十天完成數、平均製作時間、費用及卡點；定下 50 天起始日並寫回路線文件與清單 README。**順序表不是實際日產收據**。此票與 pilot 同持有 `STORY.md` scope，不能平行認領互相覆蓋；先完成試作與清理依賴，再按當時具體授權操作。

## AI 名詞：已有三集文字，仍待試片與自動接續

### token／上下文視窗／RAG 三集試片

[原票：`2026-09-29-ai-terms-video-pilot`](../../../tasks/open/2026-09-29-ai-terms-video-pilot.md)

| 欄位 | 原票值 |
| --- | --- |
| status／priority | `review`／P2 |
| owner／claimed_at | `claude-fable-5-1`／`2026-09-30T00:04:26Z` |
| branch | `claude/ai-terms-pilot` |
| scope | `docs/videos/ai-terms`、`docs/videos/ai-term-token`、`docs/videos/ai-term-context-window`、`docs/videos/ai-term-retrieval-augmented-generation`、`docs/videos/lexicon.json` |
| depends_on | `2026-09-29-ai-terms-video-series-plan` |

原 DoD 四項都未勾：各集 brief／video／claims／verify 通過 lint，且大綱、旁白、分鏡、成片、上架各關核准；TTS 後實際 9–11 分鐘且 QA 11 項全過；三列回寫 `published` 或有卡點說明的 `in-production`，填 `video_id`；以實測更新系列成本／產能及場景配方。

已勾的是三集撰稿、查核、加長及聽眾文字審稿、字典與 Shorts **文字**。未勾的是站主選定頻道立場、大綱關卡之後的旁白／圖片／剪輯／字幕／成片／上架包及實測回寫。三份文字入口是[token](../ai-term-token/brief.md)、[上下文視窗](../ai-term-context-window/brief.md)、[RAG](../ai-term-retrieval-augmented-generation/brief.md)。`review` 只表示持有者的交接狀態，**不視為媒體 QA 全過或站主／平台驗收通過**；不得自行覆寫原 owner 工作。

### 從名詞庫接下一題

[原票：`2026-09-29-video-worker-takes-next-ai-term`](../../../tasks/open/2026-09-29-video-worker-takes-next-ai-term.md)

| 欄位 | 原票值 |
| --- | --- |
| status／priority | `open`／P3 |
| owner／claimed_at／branch | 均空白，未認領 |
| scope | `apps/api/app/video_automation/topics.py`、`apps/api/tests/test_video_automation_topics.py`、`docs/videos/AUTOMATION.md` |
| depends_on | `2026-09-29-ai-terms-video-pilot` |

原 DoD 四項都未勾：站上／搜尋候選不足或有對應開關時，按名詞庫 tier／suggested_order 回傳下一題並帶文章 slug、標題、影片代號及骨架，跳過已做題；讀不到／格式錯只記 notes，不影響原挑題；測試候選充足／不足／去重；[工人說明](../AUTOMATION.md)補接續行為。原票要求**先做完試片，確認規格可行再自動化**；把系列骨架塞進 tools 提示詞不在此 API 票 scope，需另列 tools 票。

## 下一張本機文字票的推薦

目前先完成 PR #1098 的 migration 順序、更新後的獨立覆核與 CI blockers。其後推薦接[第三季製作文字包票](../../../tasks/open/2026-10-01-sothatswhy-season3-production-packages.md)，不要再開一張競爭的 100 題票。

理由是：它為 `open`、owner 空白，唯一依賴 `vet-the` 已 `done`，成果可在本機用已查核候選題、小批次撰寫與獨立文字審稿完成；其原 DoD 不需要先取得媒體費用、正式設定或站主看成片，亦沒有 AI 試片票現有 owner 的交接阻擋。第一季庫存、品牌試作／rollout與 AI 自動接續都仍有真試片或正式驗收的依賴。

2026-10-02 本次查詢中，`tasks/open` 只有該票列 `season3/` 與 `season3-topics.json` scope，票尚未認領；所查 open PR 路徑摘要與 active 影片 worktree 沒有列出該 scope 的正在修改工作。這是當次 collision 證據，**不是鎖**；真正 claim 前須重讀最新 main、分支／worktree、open PR 與任務 scopes。

接手順序可直接沿原票：先在新 `season3/README.md` 記 100 原 ID 的處置與來源，對前兩季／品牌／AI 名詞去重，列小批次；逐批完成 10 分鐘大綱、兩支 Shorts、五語包裝、後台貼用文字及非作者審稿；再回寫採用入口與處置。不把候選題直接變成 100 次產片請求。

`season3-topics.json` 同時是本次[新版企劃](plans.json)的來源之一。後續合法改來源時，需在相應精確 scope 重建新版企劃、重新驗證並覆核受影響雜湊；不能讓本次 PR 的來源收據悄悄失效，也不能只換 hash 冒充重新審過。本文只是具體續工索引，未 claim 第三季、未寫逐集新稿、未執行任何付費或正式操作。
