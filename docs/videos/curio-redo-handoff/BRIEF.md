# 重做一支奇聞檔案局：照黑貓 10 步重排 + 新畫面規則

你要重做一支影片的旁白結構和每一景的插圖提示詞。不要畫圖、不要跑 keyframes／tts、不要 commit、不要改原資料夾。

## 先讀
1. 規則書：scratchpad/redo/RULES.md（必讀，每一條都要遵守）。
2. 範例（已照規則做完的 W03）：scratchpad/wt-backup/docs/videos/curio-w03-garmin-smartphone-pivot/ 的 video.json、v3-draft/script.md、v3-draft/structure-map.md。
3. 黑貓 10 步：scratchpad/heimao/STRUCTURE.md。
4. 這支片的原資料夾（只讀）：video.json、script.md、brief.md、claims.md、NOTES.md、verify*.md、research*.md（有哪些讀哪些）。
（scratchpad = /tmp/claude-0/-home-user-travel-scanner/da8d724d-688a-5de8-b279-1942feab337d/scratchpad）

## 要產出（寫到 scratchpad/redo/<slug>/）
1. structure-map.md：原本每一段 → 新的 10 步位置，說明鉤子、起源、轉折、收尾怎麼排、前面埋的梗在哪裡收。
2. script.md：新旁白全文（繁中，照原片口吻；每句 25–42 字左右）。只用原資料夾已查核的事實；任何新事實或改寫後意思變了的數字，標【待查】並在 changes.md 說明。
3. video.json：從原 video.json 複製後改寫——
   - scenes 重排與改寫 lines（台詞 id 可以重新編，但格式照原檔）；保留原檔的其他欄位（look、voice、characters、chapters 等）並照新結構更新 chapters。
   - 每一景照 RULES.md 寫 data.prompt、需要時加 data.characters: ["researcher"]、無人景加 data.nobody: true。
   - 若原檔沒有 Ada 的 characters 定義，照 W03 的 characters[0] 抄過去。
   - 不用卡片 template；每景都是 shot。
4. changes.md：改了什麼、【待查】清單、預估總長（用原片每秒字數估），和不確定要站主決定的事。

## 完成前自檢
- 在 scratchpad/wt-backup 根目錄跑：
  `NODE_NO_WARNINGS=1 node tools/video/cli.mjs lint --file <你的 video.json>`（若沒有 --file 選項，就把檔案暫時複製到 scratchpad/redo/lintbox/docs/videos/<slug>/video.json 再用 `--slug` 搭配 `--root` 或照 cli 說明；做不到就寫進 changes.md）。
- 用腳本掃描所有提示詞，下列字一個都不能有：cat, kitten, sign, label, map, chart, graph, arrow pointing, number, badge, logo, cardboard, document with, page with, uniform, cap, puzzled, wondering, night, lamp, dusk, glow, satellite, radar, " no ".
- 檢查每個 Ada 提示詞都以規定句開頭。

回覆：新景數、Ada／無人景數、預估長度、【待查】條數、lint 與掃描結果。
