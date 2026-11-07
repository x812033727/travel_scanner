# 奇聞檔案局重做規則（站主 2026-11-05／11-06 定案）

範例：W03 v3 的成品在
`/tmp/claude-0/-home-user-travel-scanner/da8d724d-688a-5de8-b279-1942feab337d/scratchpad/wt-backup/docs/videos/curio-w03-garmin-smartphone-pivot/`
（看 `video.json`、`v3-draft/script.md`、`v3-draft/structure-map.md`）。
黑貓研究院的 10 步結構分析在 `scratchpad/heimao/STRUCTURE.md`。

## 敘事
1. 拿掉一開場的濃縮劇情：觀眾一進來太跳、看不懂。
2. 照黑貓的 10 步排：鉤子 → 「今天我們就來聊聊……」 → 時代與起源（先鋪梗，介紹故事從哪來）→ ……（照 STRUCTURE.md）→ 收尾觀點 → CTA。
3. 鉤子也不能沒頭沒尾：鉤子要讓沒看過的人聽得懂在講什麼東西、為什麼怪。
4. 故事連貫：前面埋的梗後面要收；不跳時間、不跳主角。
5. 英文名照原文念（例：nüvi、ProNav、fēnix、9to5Mac），不音譯。
6. 不寫「我自己算的」這類話；比喻要讓人一聽就懂（W03 的「桌子」被站主退過）。
7. 只用這支片既有的研究與查核資料裡的事實（同資料夾的 research*.md、claims.md、script.md、verify*.md 等）。需要新事實時，標成【待查】，不要自己編。

## 畫面（每一景一張插圖，不用卡片、不寫字，因為要走全球市場）
1. 畫面跟這一句旁白一定要對上，梗要接得上；不一定要硬補，但不能各講各的。
2. 不要貓，也不要卡通貓。
3. 完全沒有字：字母、數字、logo、假字、漂浮的 ? 或 !、有記號的徽章。
4. 數字不入畫：不畫比例、箭頭、圖表。「七成」「多了一倍」改用質性比喻：鼓或扁的錢包、升起或洩氣的氣球、長大或枯萎的幼苗、正中或射偏的飛鏢靶、Ada 倒抽一口氣。精確數字只在旁白。
5. 會長字的東西（站主選 B 方案）：可以出現，但只能畫成固定的安全圖案：
   - 手機、導航機、筆電螢幕：只能有一條藍色路線、或一個白色大轉彎箭頭、或一個紅色定位釘；手錶只能有一顆紅色愛心；其他就畫黑螢幕或單一純色。
   - 年報、文件：很厚的一本，素色封面；紙張只能是空白的。
   - 箱子：素色灰箱，不畫紙箱。
   - 不畫地圖、招牌、標籤、號碼布、制服帽徽、儀表刻字。
6. 不能畫成臉的真人（創辦人、主管、具名的評論家或部落客）不要畫成人像；用 Ada 介紹、或物件比喻。一般人（「你」、開車的人、店員）可以畫成一個普通卡通人。
7. 解說員 Ada（characters: ["researcher"]）：只用在她自己說話（「我」）、轉折、需要人解說的句子，約占兩成。她不演別人的人生。每個 Ada 提示詞開頭固定：
   `Medium close-up of Ada with her wavy black bob with a side fringe and round red glasses`，後面一個動作、最多一個簡單道具，plain wall，soft daylight。
   這支片若原本沒有 Ada 的 characters 定義，照 W03 的 characters[0]（researcher）抄過去。
8. 沒有人的景加 `"nobody": true`；用不容易長臉的物件（素灰盒、錢包、金幣、氣球、紙飛機、玩具帆船、派、盆栽）。玩具車、衛星、雷達碟容易被畫上臉，別用在無人景。
9. 白天柔光；不要夜晚、檯燈、黃昏、發光（會畫成 3D）。
10. 提示詞 100–190 字元，一個主體、一個動作。不要負面句（no ...）。

## 節奏
每 5–8 秒換一張圖；每 30–45 秒一個小鉤子；總長維持原本的長度（不得短於 8 分鐘）。

## 第一批之後補充的預設（2026-11-06）
- 英文原名不在 docs/videos/lexicon.json：照原文寫進旁白，在 changes.md 列出要加進 lexicon 的詞（值填 null），lint 時在 lintbox 的 lexicon 副本加上即可。不要為了過 lint 改說法。
- 句長和換圖節奏衝突時，換圖節奏優先（每景 4–9 秒）。
- 只畫手、不畫臉的景可以用。
- 過世很久的歷史人物也一樣用物件代稱（固定一個代表物，例如帽子），不畫人像。
- 總長：在原片 ±1 分鐘內，且在 target_minutes 範圍內；超出就在 changes.md 列出可刪的景。
- lint：把 video.json、原 brief.md、docs/videos/lexicon.json 複製到 scratchpad/redo/lintbox/docs/videos/<slug>/ 再用 `--file` 跑。
- 原片本身超過 target_minutes 時：以 target_minutes 上限為準（不改 target_minutes 欄位），把刪掉的段落列在 changes.md。
- 用自己的 lintbox 子資料夾（scratchpad/redo/lintbox/<slug>/docs/videos/<slug>/），不要動別支片共用的 lexicon 副本。
- 角色表裡沒有任何景用到的角色（舊的歷史人物卡通）刪掉，免得被拿去畫設定圖花錢。
- 【待查】不要寫進 video.json 的台詞 text；台詞用不需新事實的安全版，【待查】只標在 script.md 和 changes.md。
- youtube.description 裡「歷史人物畫成卡通」之類的說法，改成「歷史人物不入畫，用物件代表」。subtitles.burn_in 設 false。
- 站主 2026-11-07：品質優先，長度可依內容拉長或縮短（S31-v2 目標改 15–16 分；S14-v2《五輪書》照時間放前面）。
- 刪工作資料夾前：narration.wav、audio/、dubs/*/body.m4a、captions/、縮圖、成片（>100MB 只推音軌）推到分支 docs/videos/<slug>/media/，ls-tree 確認後才刪，並傳給站主。
- 站主 2026-11-07：備份＝所有上架用的檔案＋重製會用到的所有檔案（每句錄音、每景插圖與 manifest、配音、字幕、時間軸、approvals、languages、縮圖、成片），推到分支確認後才刪。
- 上架包自檢一律用 package/check.mjs 的 readPackageReport(workdir)（review-push 用的同一支），不要自己呼叫 checkPackage：它的 brandingMatches 預設 true，會漏掉 checks.json 遺失。checks.json 也要列入備份。
- 配音的片頭片尾要讓 dub 工具自己加（需要 checks.json 的 branding 與 speech_hash），不要手接到 upload/dubs：languages 關卡讀的是 dubs/<locale>.m4a。送審後用 review-files --dry-run 對每個 dub_ 的 sha 跟本機檔案。
