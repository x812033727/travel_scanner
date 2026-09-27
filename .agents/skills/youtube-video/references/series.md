# 長篇漫劇：作品、篇章、集（設計在 `docs/videos/SERIES.md`）

單集與作品走同一條流程（`docs/videos/DRAMA-FLOW.md` §二）：單集是一部 `kind = one-off`、只有一集的作品，文件只有一份故事聖經（`bible`）；長篇作品（`kind = series`）是一部約 100 集、分篇章的原創故事，一集接一集地做，文件是設定集 → 總綱 → 每篇細綱。站主只管故事：在每份文件與每集劇本的討論串裡問、要求改，滿意了核准，以及選語言與上架時間。其餘由工人與模型做。這份寫代理與工人在作品模式下多做的事（每一集的步驟在 `drama.md`）；名稱與流程照 `SERIES.md`。

## 名稱

| 站主看到的 | 內部 | 內容 |
| --- | --- | --- |
| 作品 | `series` | 名稱、前提、參考面向（world／bonds／structure／mood）、情感線尺度（`tone`）、風格預設、每集長度、預計集數、每篇集數、是否開放結局、備註；`kind` 是 `series` 或 `one-off` |
| 故事聖經 | `bible` | 單集（`one-off`）唯一的文件：前提、角色（外觀提示詞逐字沿用）、幕、**一個**大綱、素材、不做的事；核准後第 1 集直接 `ready`，沒有總綱與細綱 |
| 設定集 | `setting` | 世界觀與規則、人物表（外觀提示詞逐字沿用）、語氣與畫面、命名規則、長線謎團（含保留給續作的）、不做的事 |
| 總綱 | `outline` | 篇章劃分、每集一句話、前世／今生排程、謎團揭曉排程、全季張力地圖 |
| 篇章細綱 | `chapter` | 每集：開場鉤子、主要衝突、轉折、結尾懸念（類型）、埋下與回收（謎團 id）、張力曲線（五個 1–5）、出場角色、場景、主題句 |
| 劇本 | `script` | `docs/videos/<slug>/script.md`：場景、【角色】台詞、情緒；鏡頭提示詞在審核頁旁邊，不在檔案裡 |
| 討論串 | `messages` | 每份文件與每集劇本各一條（`video_drama_messages`）：subject `bible`、`setting`、`outline`、`chapter:<n>`、`script:<集數>`；每則寫誰說的（`owner`／`planner`／`writer`）、對哪一版說的（文件版本號，或 `script.md` 雜湊的前 12 碼）；站主的訊息還沒回覆時頁面顯示「等模型回覆」 |
| 前情 | `recap` | 每集完成後 150 字：發生了什麼、角色狀態、伏筆狀態 |

## 主幹（工人自動跑；站主在 `/admin/videos` 的「漫劇」分頁決定）

1. 站主建作品（或送出「新的漫劇」，伺服器就建一部 `one-off` 作品）→ 工人問 `GET /video/automation/series/next` → `setting`（單集是 `bible`）：企劃模型（variant `setting`／`bible`）寫文件 → `POST …/series/<slug>/docs` → 站主**討論／核准**：在文件的「討論」節問問題或要求改（工人下一輪回覆，要改就出新版本，見下面「討論串」），也可以退回（帶備註）或自己改，滿意了核准。退回就帶 `previous` 與 `owner_note` 重寫，最多 `series_doc_rewrites` 輪，之後停在待審讓站主自己改；討論出的新版本不算這個輪數。
2. `outline` 同上（討論／核准；subject `outline`）；核准後站上就有每一集的列（標題、一句話），狀態 `planned`。單集沒有這一步：故事聖經核准後第 1 集直接 `ready`。
3. `chapter`：一篇一份，同樣討論／核准（subject `chapter:<n>`），核准後那一篇的集數變 `ready`；下一篇在上一篇做到剩 `series_chapter_ahead` 集時先規劃，站主也可按「先規劃下一篇」（單集沒有這顆按鈕；直接呼叫 API 會被 409 `video_series_all_planned`「每一篇都已經規劃過了」擋下）。
4. `episode`：工人 `POST …/episodes/<n>/start`（影片 slug 是 `<作品>-e001` 這種），伺服器回請求列與脈絡（單集的脈絡把故事聖經當 `setting` 給、沒有 `chapter`）；工人寫 `series.json`（人物表、本集細綱、前情、謎團、設定全文）與 `brief.md`（不出大綱選項；`## 大綱` 只有選項 A，本機直接核准，備註「依故事聖經」或 `planned by chapter <n>'s approved outline`），然後照 `drama.md` 的步驟走：撰稿（作品的集用 variant `episode`；單集用一般漫劇提示）→ 查核（variant `episode`，多了張力與連貫性）→ 聽眾審稿 → **劇本關卡：討論／核准**（subject `script:<集數>`）→ 設定圖（沿用作品存檔，只畫新角色）→ 旁白 → 關鍵影格 → 分鏡 → 片段 → 配樂 → 合成（此時寫前情 `POST …/recap`）→ 字幕 → 成片 → 上架包 → 上架確認（`POST …/done`）→ 站上自動開下一集（單集沒有下一集）。

## 討論串（每個核准點都有）

- 站主在 `/admin/videos` 的文件面板或劇本卡片的「討論」節寫一句話並「送出」（`POST /admin/video-automation/series/<slug>/messages {subject, body}`；讀用 `GET …/messages?subject=`）。文件或劇本已核准的串只留紀錄，不再收新訊息（409）；這一集還沒開始（沒有影片 slug）時 `script:<集數>` 被 409 `video_drama_script_not_started` 擋下；開始後、劇本還沒寫出來前送的訊息會被工人代回「劇本還沒寫出來」。
- 工人每一輪在手上的影片推進之後、任何作品工作之前，先回一則：`GET /video/automation/series/messages/next` 拿最舊的未回覆訊息（連同整條串、文件最新版（劇本串則是那一集，劇本由工人從自己的 `video.json`／`script.md` 讀）、作品脈絡），文件交給企劃模型（variant `discuss`）、劇本交給撰稿模型（variant `discuss`），提示在 `.agents/skills/youtube-video/references/prompts/discuss.md`；答案 `{ reply, revised }`，`POST …/series/messages/<id>/answer {reply_md, revised?}`。手動做的代理照同一對端點。
- 站主問問題就只回答（`revised` 為 null）；要求改才出新版本，回覆裡列出改了什麼。**文件**的新版本由站上存成一個等站主核准的 `review` 版本，被取代的那版備註「討論後出了新版本」——不算 `series_doc_rewrites`，也不算每月草稿，沒有輪數上限。**劇本**的新版本由工人自己寫回 `video.json`（每句 id 保留、過 lint，撰稿模型最多修 3 次，仍不過就還原並在回覆裡說明），接著重跑查核與聽眾審稿、重寫 `script.md`、再送一次劇本關卡。
- 模型給不出可用的答案時，工人代它回一則「模型這一輪沒有給出可用的回覆（…）」，原始答案留在 `answers/discuss-<時間>.txt`，串停在那裡等站主，不自動重試。
- 討論不能動到上面已核准的文件（討論細綱時不能改設定集）：模型只建議，站主到那條串再說。

## 劇本關卡（`script`）

- `node tools/video/cli.mjs script --slug <slug>` 由 `video.json` 寫 `script.md`（只含敘事）；`review-push --gate script` 送審，payload 帶場景與提示詞、人物、`beats`、查核的 `coverage`（hook／conflict／turn／cliffhanger 各「有／弱／無」）與 `problems`。每一支漫劇都有這一關（`stepsFor`），在任何設定圖或片段花錢之前；漫劇設定的「劇本先給我看」（`series_script_gate`）關著時工人在本機核准。
- 關卡綁 `script.md` 的雜湊，而它只含場景順序、每句的 id／文字／說話者／情緒：look／keyframes／clips 自動修提示詞不會讓核准失效；旁白退回或討論改了台詞才要再看。
- 討論：站主在劇本卡片的「討論」節問或要求改（subject `script:<集數>`），撰稿模型（variant `discuss`）回覆或改 `video.json`，改了就重跑查核與聽眾審稿、再送一次；沒有輪數上限。
- 退回：撰稿模型以 FIX 模式（`fix.kind = "script"`，`owner_note`）重寫，重跑查核與聽眾審稿，再送一次；`MAX_PROMPT_FIX_ROUNDS` 輪後卡住。

## 一致性靠三件事

- **人物表逐字沿用**：`series.json` 的 `characters` 來自設定集（單集來自故事聖經）；撰稿把用到的角色逐字複製進 `video.json`，依 id 排序；`settle()` 會用設定集的版本覆蓋同 id 的角色，lint 擋掉任何差異與不在人物表裡的角色。`lookHash` 因此只在 cast 變動時改變。
- **設定圖沿用**：`<VIDEO_WORKDIR>/_series/<作品>/characters/index.json` 記每個角色核准過的設定圖（鍵＝id＋appearance＋sheet_prompt＋look）。`look` 先查存檔，有就當唯一候選並直接核准 look 關卡，只畫新角色；`review-pull` 核准 look 時把選中的圖存進去。
- **前情**：合成完成後查核模型（variant `recap`）寫 150 字摘要與狀態，`POST …/recap`；下一集的撰稿與查核拿最近 3 集全文、更早的一句話。

## 張力規格（寫在提示詞裡，`tools/video/automation/prompts.mjs` 的 `SERIES_INSTRUCTIONS`）

- 設定集要有衝突引擎：正道與魔道的結構性矛盾、雙男主各自的秘密與代價、每個門派世家想要什麼；長線謎團 8–12 個，開放結局時至少 3 個保留給續作。
- 總綱要有全季張力地圖：每篇賭注高過上一篇（個人→門派→天下）；中段一次翻轉世界觀的大揭露；每篇章末一個改變局勢的轉折；前世線倒敘插敘，每篇 1–2 集；每集一句話「回答一個問題、丟出更大的問題」。
- 篇章細綱每集：`hook`（20 秒內）、`conflict`、`turn`（中段）、`cliffhanger {type: danger|reveal|choice|reversal|emotion, text}`、`setups`／`payoffs`（謎團 id）、`tension`（五個 1–5，結尾 ≥ 4，不能一路平）；相鄰兩集懸念類型不同；每 3–4 集至少收一個伏筆；每篇最後一集的懸念改變觀眾對前面某件事的理解。工人在送審前自己檢查這些（`documentProblem`），不合就再要一次答案。故事聖經的 `outline` 是同一組欄位，只有一個。
- 撰稿：鉤子在第一、二個鏡頭內；轉折在中段；最後一場只做懸念，沒有總結；羈絆用動作與物件，不點明；只碰 `beats` 指名的伏筆，不碰保留的謎團。
- 查核：`coverage` 與 `problems` 顯示在劇本關卡最上面；另報 `similar_works`（與知名作品雷同之處）。

## 原創與版權

世界、人名、門派名、情節一律原創；提示詞明寫不得使用任何既有作品的人物、名詞、情節；查核有雷同檢查。每集都有站主核准的劇本與設定集（單集是故事聖經）當作者證據；合成內容揭露一律勾。

## 指令

```bash
node tools/video/cli.mjs auto                          # 工人：先推進手上的影片，再回一則討論、再做作品（含單集）的工作、再看舊的單集請求與排程草稿
node tools/video/cli.mjs script --slug <slug>          # 寫 script.md
node tools/video/cli.mjs review-push --slug <slug> --gate script
node tools/video/cli.mjs review-pull --slug <slug>     # 核准 look 時順手把設定圖存進作品存檔
node tools/video/cli.mjs look --slug <slug>            # 有存檔就沿用，只畫新角色
```

## 坑

- `series.json` 不在就 lint 警告、不擋；有但人物表對不上就擋。工人在 `draftEpisode` 寫它（單集也是），手動做的集要自己寫。
- 詞彙表是所有影片共用的（`speechHash` 含整份）：設定集階段就把人名、門派名、術語加齊（設定集與故事聖經 JSON 的 `lexicon`），之後少加。
- 作品文件的提示詞紀錄在漫劇設定子分頁的「目前的提示詞」依 variant 分開（`planner:setting`、`planner:bible`、`planner:discuss`、`writer:discuss` 等），不會蓋掉教學企劃的。
- 集數的 slug 固定為 `<作品>-e<三位數>`；作品 slug 最長 40 字；單集的作品 slug 是 `one-off-<請求 id 前 8 碼>`，影片就是 `one-off-<…>-e001`。
