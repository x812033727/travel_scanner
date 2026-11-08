# AI 劇的審片：從付錢前到送上後台

這份是共用區：任何一部 AI 劇，一集從「提示詞寫好」到「送上後台、站主看過」之間要過的每一關，照順序寫：誰做、看什麼、用什麼工具、結果怎麼處理。
工具只寫在哪裡、抓什麼，不抄程式碼。

- 分鏡怎麼寫才少出錯：[`WRITING.md`](WRITING.md)（第十二節是分鏡本身的三道檢查，這份從分鏡交出去以後開始）。
- 備份：[`BACKUP-BRANCHES.md`](BACKUP-BRANCHES.md)。出過什麼錯：[`LESSONS.md`](LESSONS.md)。
- 只有某一部要多看的項目（角色、道具、場景的特別規則）在個別區：
  種田 [`production/REVIEW.md`](../series-plans/zhong-tian-qu-qi/production/REVIEW.md)、
  祖媽 [`production/REVIEW.md`](../series-plans/top40-2025-2026/2025-01-tai-nainai/production/REVIEW.md)；
  站主對各部的決定在同一個資料夾的 `RULES.md`。

審片的人與做片的人要分開：做的人看自己挑的片會漏掉站主一眼就看到的事（種田 r2 第 4 集：木匣忽大忽小、門與鍋的距離變了、主角出門看不到黑影，
每一鏡單看都沒問題）。所以下面標「獨立」的關卡，都由**沒參與做這一集的代理**來做；它只讀不改、不花錢。

## 總覽

| 順序 | 關卡 | 誰 | 花錢嗎 | 不過怎麼辦 |
| --- | --- | --- | --- | --- |
| 0 | 分鏡的三道檢查 | 寫稿者、程式、獨立審稿 | 否 | 改分鏡（`WRITING.md` 第十二節） |
| 1 | 付錢前的預檢 | 製作端、程式 | 否 | ERROR 不送；warning 逐條決定 |
| 2 | 站主點頭花錢 | 站主 | — | 估價超過上限先停 |
| 3 | 挑草稿 | 獨立代理 | 否 | 標 RETAKE 重抽，或 KEEP |
| 4 | 精修前的連戲審 | 製作端跑表、獨立代理審 | 否 | 重抽，修好再一起精修 |
| 5 | 剪完的自動檢查 | 程式 | 否 | 照每個工具的修法 |
| 6 | 剪完的人工三項 | 製作端 | 否 | 改混音、剪點或重抽 |
| 7 | 獨立成片審查 | 獨立代理 | 否 | 嚴重、中等要修，輕微接受 |
| 8 | 表情審查 | 獨立代理 | 否 | 重拍最嚴重的，其他交站主 |
| 9 | 交站主 | 站主 | — | 站主決定接受、修或重拍 |
| 10 | 送上後台與確認（`import`） | 製作端 | 否 | 抓回來比對，缺就補 |
| 11 | 站主核准成片 → 語言 → 上架包（`import --publish`） | 站主、製作端 | 否 | 看輸出的 `missing`，缺就補送 |
| 12 | 上 YouTube | 站主 | — | 第 11 節 |
| 13 | 備份與刪本機 | 製作端、另一個代理 | 否 | `BACKUP-BRANCHES.md` |

修正的範圍（種田站主 2026-11-07）：**嚴重與中等都自己修好再給站主，輕微的接受**。挑片後一次、剪完後一次，兩次獨立審片。

## 1. 付錢前的預檢

每一批提示詞送出去之前，讀**每一支提示詞的全文**（不是只看分鏡那一列），把會花錢的錯擋在送出前。

| 工具 | 在哪 | 抓什麼 |
| --- | --- | --- |
| `preflight-prompts.py` | [`zhong-tian-qu-qi/production/colab/runs/_scripts/`](../series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/preflight-prompts.py) | ERROR：參考圖跟服裝字打架（現代裝的圖配古裝字）、`<Picture N>` 數目不對、一個人的圖片清單重複或指到沒送的圖。warning：基本外貌裡的道具、五字以內的短喊、沒寫空白或虛焦的紙、有名字卻沒參考圖的人、群眾沒寫朝代衣著、酒瓶酒杯、插鏡開頭不是特寫、皮膚上的小東西、只寫「不笑」沒寫別的臉、「不畫面板」與空中藍光、一鏡四個以上有名字的人（`four`）、送了會笑的參考圖卻要嚴肅臉（`smile-ref`）、起身說話沒寫頭上留空（`headroom`）。**角色名對照表寫死在種田的角色**，別的劇要先改對照表 |
| `shot_reading.mjs` | [`.agents/skills/animation-camera/scripts/`](../../../.agents/skills/animation-camera/scripts/shot_reading.mjs) | 鏡頭的運鏡、方向、軸線讀法是否跟模型讀的一樣（見 `animation-camera`） |
| `h3.sh check`、`refine.py --check` | [`.agents/skills/minimax-h3-colab/scripts/`](../../../.agents/skills/minimax-h3-colab/scripts/h3.sh)（Colab 路線） | manifest 格式、參考圖數、草稿格數要是 17k+5（39、56、73、90…）才進精修 |
| 系列自己的轉換檢查 | 祖媽 [`production/tools/compile.py --check`](../series-plans/top40-2025-2026/2025-01-tai-nainai/production/tools/compile.py)、`node tools/video/cli.mjs lint --slug <slug>` | 中文分鏡改了英文沒跟上、台詞說話人對不上 `cast.json`、節奏警告 |

- ERROR 不送。warning 由製作端逐條決定接受或改；決定寫進該集工作單。
- 預檢只能擋錯，不能替分鏡補內容。預檢抓到同一類錯很多次，回頭改分鏡與 `WRITING.md`。
- **花錢前給站主估價**：這一批幾支、幾秒、約多少錢；一集的上限照系列 `RULES.md`。重抽會讓一集超過上限時先停下來問。

## 2. 挑草稿（獨立挑片）

每鏡通常抽兩個種子。挑片直接交給獨立代理，製作端不先自己挑（種田第 6 集起這樣做，2026-11-08 起兩個系列都照這樣）。

**給它的東西**：分鏡（`script.md`）、每鏡兩個種子的整段格子（例如 `fps=0.7` 一條）、送出的提示詞、參考圖。

**每一鏡照這個順序問**：

1. **稿子這一列寫的動作有沒有發生**：誰做了什麼、東西最後在哪裡、這一鏡最後的樣子對不對。兩支都沒有，就是重抽，不是挑比較好的那支。
   （種田第 2、3 集只比哪支好看，送審後獨立審片各挑出十幾處動作沒演出來）
2. **露臉的鏡先看表情**：稿子要的臉有沒有出來；不能笑的鏡有沒有笑（只要有一格在笑，就看能不能剪掉）。
3. **人**：人數、有沒有分身、臉與服裝跟參考圖一樣、不該在的人有沒有出現、沒有參考圖的配角是不是卡通比例。
4. **道具與場景**：大小、樣子、在誰手上；場景格局；有沒有字、面板、發光、時代錯誤的東西。
5. **鏡中跳鏡**：看最後一兩格，不只看第一格（約一成的片段會在鏡中跳成全景或別的場）。
6. **頭尾**：說話時臉有沒有出畫；開頭有沒有閃一下別的畫面。

**免費的機器輔助**：精修前在本機跑 [`cuts.py`](../../../.agents/skills/minimax-h3-colab/scripts/cuts.py)（或 `h3.sh cuts`）找鏡中硬切，只看報告；
報告的切點換成剪點。剪過的草稿要停在 17k+5 格才收得進精修。

**每一鏡回一行**（例如 `review-picks.tsv`）：

| 寫法 | 意思 |
| --- | --- |
| 種子編號 | 用這支。剪點、裁切（`start@秒`、`end-before@秒`、`crop=`）只寫給這一支 |
| `RETAKE` ＋ 英文改寫句 | 兩支都不行，照改寫句重抽。`refine-prep.py` 會把這一鏡從精修清單拿掉 |
| `KEEP` | 這輪兩支都不行，但**之前已經有可用的那支**，維持舊的。不要寫 RETAKE，否則成片會少一鏡（種田真人版第 1 集 fix5） |

- 挑片理由只寫選中那一支的剪點；挑片檔怎麼排、工具怎麼讀，照系列的工具（種田的 `refine-prep.py` 見種田 [`REVIEW.md`](../series-plans/zhong-tian-qu-qi/production/REVIEW.md) 第八節）。
- **重抽前先看參考圖是不是問題本身**（兩頂帽子、腰上多一把刀、一直在笑）；是圖的問題就改圖或拿掉那張圖。
- **改字只改一次**，第二輪還錯就改鏡頭設計（`WRITING.md` 第十一節）。三輪都錯就用最接近的版本，剪接時補救。
- 挑片時看「說的是不是劇本那句」：評片前先讀那一鏡的稿子，每一條「錯」都先對過動作欄再說（種田真人小樣 s25 差點把照稿演的當成錯重拍）。

## 3. 精修前的連戲審（草稿一輪）

挑完、**精修前**先做一次（種田站主 2026-11-07：「這些在審片時應該要看到吧？」）。在這一輪抓到要重抽的錯，省一輪精修。

- 跑 [`continuity-sheets.py`](../series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/continuity-sheets.py) 的草稿模式（輸入選中的草稿資料夾，檔名 `sNN.mp4`）：
  一場一張圖，每鏡頭、中、尾三格照剪接順序排。
- 交給獨立代理，照下面第 6 節的清單逐場看。要重抽的重抽，再一起精修。

## 4. 剪完的自動檢查

剪完一定照這個順序跑，每個都要到 0 或寫明為什麼接受：`cut-qa.py` → `cut-jumps.py` → `audio-qa.py` → `continuity-sheets.py` 自己看一遍 → 獨立審片 → 修 → 送審。
工具都在 [`zhong-tian-qu-qi/production/colab/runs/_scripts/`](../series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/)，讀剪接工具（`assemble-v4.mjs`）寫的 `final.log` 與 `<stem>.lines.json`。

| 工具 | 抓什麼 | 怎麼修 |
| --- | --- | --- |
| `cut-qa.py CUT_DIR` | 片段不夠長、最後一格停住（held）；鏡頭切兩半再放大（punch，看起來像頓一下）；同一支片段用在好幾鏡；整集動量中位數與靜止幀比例（目標 ≥ 7、≤ 15%）；整集與配音的響度（−14 LUFS ±1、峰值 ≤ −1 dBTP）；幀率（24）；超過 0.2 秒的黑畫面；字幕太快讀不完（中文每秒超過 9 字）；配音加速超過 1.30 倍或句尾被切 | 片段買長一點或重抽；改剪接表 |
| `cut-jumps.py CUT_DIR` | 一鏡之內的硬切：片段開頭或結尾閃一下別的畫面（場景圖、全景）。每鏡中間一格看不到 | 開頭的用 `stage-clips.sh NN sNN@秒` 從跳完之後起剪；結尾的只有片段比鏡頭短才剪得掉，否則重抽或買長 |
| `audio-qa.py CUT_DIR VIDEO_JSON` | 台詞跨到下一鏡（畫面上的人在說話時是 FAIL）、兩句重疊、被片尾切掉、被配樂蓋過（不到 −30 LUFS，或比前一秒的配樂高不到 3 dB）、超過 4 秒沒有台詞（只是提醒） | 改台詞位置、拆鏡、壓配樂。**它不判斷嘴型與聲音合不合臉，那要站主聽** |
| `continuity-sheets.py CUT_DIR VIDEO_JSON OUT` | 不抓錯，只畫表：一場一張、每鏡三格。對著分鏡看同一道具大小樣子、地點的相對位置與距離、誰看什麼被看的在不在那邊、同場的光與衣服 | 有一項不對就重抽那幾鏡 |

**交站主前，製作端先開聲音把整集從頭到尾看一遍**，特別看畫面上的人說話時嘴有沒有動、聲音像不像同一個人（種田 [`storyboard-rules.md`](../series-plans/zhong-tian-qu-qi/production/storyboard-rules.md)〈收工前要用聲音看一遍〉）。

自動檢查抓不到的三件事，**合成後、交站主前另外做**（祖媽第 1 集 2026-11-07：兩輪審片都過了，站主一看就看到鈴聲聽不到、門外亮得像白天、手跟紙黏在一起）：

1. **招牌音效**：每個招牌音效那一秒用 `ebur128` 或 50 ms RMS 量，要明顯比前後高；位置要對到畫面上的動作。
2. **手**：有手拿、遞、塞東西的鏡，那一段逐格看（約 0.08 秒一格）。
3. **夜景**：窗、門外、天空有沒有亮成白天。

另外兩件換片段時一定要重做的事：

- **每次換片段（重抽、換種子、改剪點），音效與名牌的時間都要照新片段重量**。從舊版複製來的剪接表，音效時間是照舊片段的動作算的
  （種田真人版第 1 集：打雷早 4 秒、踹門早 0.8 秒、放碗早 3.5 秒、拍胸早 6.3 秒，動作那一刻反而沒聲音）。
- **字幕起點**：用模型原聲的劇，字幕要從模型實際開口的時間算；片段前面有一聲雜音字幕就會提早（種田 s12 早 4.3 秒）。
  有面板的鏡，面板上沒有的系統句要另外列字幕。剪接表的寫法（`voice_skip`、`subtitle_lines`）見種田 [`REVIEW.md`](../series-plans/zhong-tian-qu-qi/production/REVIEW.md) 第八節。

## 5. 獨立成片審查

剪完、自動檢查與人工三項做完以後，另開一個沒參與製作的代理審成片。**給它的說明就是這一節**，加上系列的 `REVIEW.md`（含〈站主已經定案〉那一節）。
種田的 [`independent-review.md`](../series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/independent-review.md) 是較早、較窄的版本
（只給稿子、連戲表與三個檢查結果，清單 7 項，路徑寫死 `zhong-tian-qu-qi-eNNN-r2`），不要只給它；下面的「給它的東西」與第 8 項以這一節為準。
實際的報告可以參考種田真人版第 1 集的 [`cut-review.md`](../series-plans/zhong-tian-qu-qi/production/colab/runs/e901-live/cut-review.md)（第 1 輪）與 [`cut-review-2.md`](../series-plans/zhong-tian-qu-qi/production/colab/runs/e901-live/cut-review-2.md)（第 2 輪）。

**給它的東西**：分鏡（`script.md` 或 `storyboard.md`）、`video.json`、成片、`final.log`、`lines.json`、字幕、剪接表、混音圖、參考圖、
連戲表、三個自動檢查的結果（它不重複）、上一輪的審片報告、**站主已經定案、不再列為要修的事**。

**它怎麼看**（照實際做法）：

- 整片解碼後每鏡抽格（例如 0.5 秒一格的總表）；有動作的地方加密到 8 fps；手的段落逐格看。
- 用 faster-whisper 聽寫整片與每一句，對台詞與字幕；聽不清的句子列出來。
- 同一角色的每句量基頻與頻譜距離，找聲音像換了一個人的鏡（只能當提示，標「不確定」交站主聽）。
- 招牌音效量 50 ms RMS 的峰值與前後底噪。
- 臉、紙、道具的關鍵格抽全解析度，跟參考圖比。

**逐場對著分鏡看的清單**：

1. **道具**：同一個東西每鏡大小、形狀、顏色一樣（一本書大的匣子一直是那麼大；刀身不變；紙一直摺著或空白）；在分鏡寫的手上或位置。
2. **地點**：每鏡的格局與距離一樣（門、灶、桌、院門、井、籬笆在同一邊）。
3. **視線與反應**：有人看什麼或對什麼反應，那個東西在他看的方向、在前後鏡看得到；反應鏡在分鏡寫的位置。**說話的人看著對方，不對鏡頭講；全員面向鏡頭排排站也算錯**（站主 2026-11-08：「很多幕都是看前面 不會面對對方說話」）。挑草稿時也要看這條。
4. **人**：人數對；沒有人出現兩次；臉、頭髮、衣服跟參考圖一樣；該在的人都在；**表情照稿**（寫「不笑」卻笑是問題）。
   領口、裸露照系列的標準（兩部不同，見各系列 `REVIEW.md`）。
5. **故事**：每鏡演出那一列寫的動作；每場的結尾成立；問句在分鏡寫的地方得到回答。
6. **不該畫出來的**：紙或招牌上的字、畫進畫面的系統面板、發光的眼睛、時代錯誤的東西、皮膚上的斑點、卡通比例的人、閃一下別的畫面；
   夜景的窗、門、天空亮得像白天。
7. **靜止格子看不到的**：每一隻拿、遞、收東西的手逐格看；量每個招牌音效那一秒對前後的音量；台詞放在鏡頭開頭、動作在結尾的鏡，指出聲音比畫面早了幾秒。
8. **聲音與字幕**：字幕出現的時間跟開口對得上；系統聲、心裡話、畫外、背影的台詞，畫面上沒有在動的嘴；同一角色的聲音前後像同一個人。

**它回什麼**：一張清單，最嚴重的在前。每一項寫：

- 鏡號與成片秒數（另寫「片段秒數」＝成片時間減該鏡在 `final.log` 的起點，方便下剪點）；
- 問題是什麼、分鏡寫的是什麼；
- 修法：剪（`stage-clips.sh NN sNN@秒`、`start-after`、`end-before`）、改混音或字幕時間、用改寫句重抽，或接受；
- 拿不準的標「不確定」。沒有問題的場直接說沒問題。不稱讚、不重講劇情。

**嚴重程度**：

| 等級 | 意思 | 例子（種田真人版第 1 集） | 處理 |
| --- | --- | --- | --- |
| 嚴重 | 觀眾一定看得到、看了會出戲，或這場戲的重點不成立 | 眼睛整個發藍光；粥從空碗倒出來；紅紙一格之間變成紙筒；結尾那一眼沒有成立 | 一定修 |
| 中等 | 看得出不對，或讓情緒、交代變弱 | 門框上有寫字的紅紙；音效比動作早好幾秒；字幕早 4 秒；開頭一秒抬頭破壞後面的「第一次抬眼」 | 修；要重拍又超預算的交站主 |
| 輕微 | 小、在背景、沒對焦，或劇本的小偏差 | 背景小匾上一個模糊的字；草編兔子樣子不一樣；台詞講完畫面多停兩秒 | 接受，順手能修就修 |

**不花錢的修法優先**：先列出不用重拍就能修的（剪點、音效位置與音量、字幕時間、名牌出現時間、把放不下的系統句移到下一個沒有嘴的鏡），
做完再決定哪些要重拍。重拍的一律寫成「重抽 sNN，台詞不變，動作改寫成：…」，台詞是模型原聲的鏡要整句重拍。

**第二輪起**：先放一張表，逐項寫上一輪每一項的現況（已修好／只修好一半／沒修／依站主定案接受），再列新的問題。
最後寫結論：「可以給站主看」或「先做哪幾項不花錢的修改」，以及「交給站主決定的」。

## 6. 表情審查

露臉的鏡多、又是真人版時，另外做一次逐鏡表情審查（種田站主 2026-11-08：「我發現有些角色都沒表情，應該每個都要有表情，除非是劇情要求要沒表情」）。
範例：種田 [`expression-review.md`](../series-plans/zhong-tian-qu-qi/production/colab/runs/e901-live/expression-review.md)。

- **素材**：選中的草稿（精修保留同一段表演），只看剪接用到的那段；每鏡每 0.5 秒一格，臉小的鏡裁臉放大。
- **對照**：`video.json` 每句台詞的情緒、每鏡實際送出的提示詞、參考圖。
- **評等**：OK／偏平（有一點但讀不出情緒）／沒表情（像定妝照）／錯（演成別的情緒）。劇本要冷臉、低頭、背影的算 OK，註明「劇本要求」；插鏡、背影寫「不適用」。
- **一張總表**：鏡、成片起點、角色、劇本要的、畫面上（寫秒數）、評等；再統計各評等的鏡數。
- **排先後**：情緒重點不見的（開場鉤子、一場的高點、角色第一句台詞、下一場的動機）列嚴重；情緒不對、觀眾會覺得怪的列中等；偏淡但不是重點的接受。
- **找原因**：讀實際送出的提示詞：情緒有沒有進英文？只寫了形容詞？收尾句把臉鎖回參考圖？臉太小？把原因與改寫句交給分鏡（`WRITING.md` 第四節）。
- 只能剪掉的（開頭一秒在笑）寫剪點；其他交站主決定重拍哪幾鏡。

## 7. 交給站主

**怎麼交**：用第 8 節的 `import` 把成片送上後台，站主在 `/admin/videos` 那一集的成片審核卡上看、核准或退回。還在改、不想送上後台的版本，先給預覽檔請站主看。

**交出去的**：

- 預覽版成片（加上手機版）；
- 兩輪審片與表情審查的結果，以及哪些已經修好；
- **要站主決定的清單**，每項寫清楚選項與花費：要重拍才能修的、會超過預算的重抽、聲音要站主聽的（同一角色聽起來像兩個人、口音、念錯字）、審片標「不確定」的、
  觀眾在不在意要站主判斷的（例如臉跟其他鏡不太像）。指到某一格就寫成片秒數。

**站主決定的**：接受、修（不花錢）、重拍哪幾鏡、預算要不要提高、聲音能不能用。

- 站主說的話原文記進該集的票與系列的 `RULES.md`；同樣的問題以後不再列為要修（審片 brief 的「站主已經定案」清單）。
- 站主指的是哪一張、哪一支不清楚時，把候選並排、標好名字問一句，不要猜了就往下做。
- 製作端的建議站主照做之後才發現建議錯了，馬上說、收回（例如重拍其實照稿演對的鏡）。

## 8. 送上後台、核准成片與上架包

送上後台有兩次 `import`，中間是站主核准成片與決定語言。順序不能換（種田第 32、34 集踩過，[`種田 production/README.md`](../series-plans/zhong-tian-qu-qi/production/README.md) 第 3 節第 5 條）：

1. **送成片**：`node tools/video/cli.mjs import --from <匯入資料夾>`。匯入資料夾放 `final.mp4`、`meta.json`、字幕、封面。
   後台已經有同 slug 的舊版時加 `--force` 蓋過去，舊檔移到匯入資料夾的 `cg-old/` 之類，不刪。
2. **送上去以後抓回來比**：`review-files --slug <slug> --out <資料夾> --gate final`，封面與字幕逐位元相同，成片比長度與畫面；三樣都在才算送上後台。
   在後台影片清單也逐項確認成片、字幕、封面都在。這是刪本機檔案的兩個條件之一（另一個是備份核對，見 `BACKUP-BRANCHES.md`）。
3. 站主看成片（第 7 節），核准。
4. 站主在那一集的語言面板勾語言；有勾的話 `import --from <匯入資料夾> --languages` 送語言批次，等站主核准（第 9 節）。
5. **站主核准成片以後，送上架包，連同重剪需要的檔**：

   ```bash
   node tools/video/cli.mjs import --from <匯入資料夾> --publish \
     --clips <剪進成片的片段資料夾> \
     --edit <這一集的剪接表 json>
   ```

   - `--clips` 指**剪進成片的那一份片段，帶模型原聲的**。種田真人版是 `_live-e90N/zhong-tian-qu-qi-e90N-dh/clips/`（`sNN-t1.mp4`，接好聲音、剪好頭尾）；
     不要指精修資料夾 `runpod/a/st2/refined`，那裡的片段沒有聲音，原聲就丟了。
   - `--edit` 指 repo 裡的剪接表，例如 `docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e901-live.json`。
   - 錄音、`cut/*.log`、配樂、首格是從 `--clips` 的**上一層**找的（`audio/`、`audio-<語言>/`、`cut/`、`music/`、`first-frames/`）；錄音不在那裡就加 `--recordings <資料夾>`。
   - 看輸出的 `missing`：有缺就補好再送。核准後的上架包加不進片段，所以要一次送齊。
6. 站主核准上架包。

**每一次送的東西會進雲端硬碟的哪裡**（主機 worker 從審核區取回，照 [`BACKUP.md`](../BACKUP.md)〈匯入的影片〉）：

| 送法 | 帶上去的 | 雲端硬碟裡 |
| --- | --- | --- |
| `import` | 成片、字幕、封面、`metadata.json` | 那一集的資料夾 |
| `--languages` | 核准的外語字幕、說明、配音、各語縮圖 | `captions/`、`descriptions/` 等 |
| `--publish --clips … --edit …` | `--clips` 裡每支 `<鏡>.mp4`（最多 120 支）；上一層的 `audio/`、`audio-<語言>/` 打包成每種語言一個錄音檔加 manifest；`cut/*.log`、`music/*.mp3|wav`、`--edit` 的剪接表（這類最多 40 個、名稱最多 28 字、只收文字、json、mp3、wav）；`first-frames/*`（最多 400 張） | `clips/`、`recordings/`、`recut/`、`keyframes/`（完整層級才有） |

沒送 `--publish` 的話，雲端硬碟只有上傳包。分支裡有、雲端硬碟今天還拿不到的東西（沒選中的草稿、精修、提示詞、挑片檔、系列共用檔），見 [`BACKUP-BRANCHES.md`](BACKUP-BRANCHES.md)〈雲端硬碟〉。

封面不要沿用畫風不同的舊季封面（第 10 節）。

## 9. 語言與多語 CC

- 每支影片先只有繁體中文。成片核准後，站主在 `/admin/videos` 那一集的語言面板勾每種語言要不要做標題說明、CC、配音；工人只做勾了的，做好一批送一張語言卡給站主核准。
  做法與規則在 [`youtube-video` 的 `publish.md`](../../../.agents/skills/youtube-video/references/publish.md)〈語言：每支影片由站主選〉與 [`LANGUAGES.md`](../LANGUAGES.md)。
- 送語言批次要在送上架包**之前**（第 8 節第 4 步）。
- 漫劇的配音目前灰掉，只能勾標題說明與 CC（`publish.md`）。
- 各系列的外語決定：種田只做中文原聲加多語 CC，八語配音先停（種田 [`RULES.md`](../series-plans/zhong-tian-qu-qi/production/RULES.md) 第三節）；祖媽還沒定（祖媽 [`RULES.md`](../series-plans/top40-2025-2026/2025-01-tai-nainai/production/RULES.md) 第八節）。
- 合輯的語言照 [`COMPILATIONS.md`](../COMPILATIONS.md)。

## 10. 標題、說明、封面

通用規則在 [`publish.md`](../../../.agents/skills/youtube-video/references/publish.md)〈標題〉〈說明欄〉：給 3 個候選、頻道上限 36 個全形字等值、系列名當後綴；漫劇的集數可以寫（lint 帶 `numbered: true`）。

- **標題格式**：`<這集的鉤子>｜<劇名> 第N集`。種田重製的集數加「（重製版）」並帶「| CC字幕」，例如 `…｜種田娶妻打天下 第1集（重製版） | CC字幕`。各系列的格式寫在系列 `RULES.md`。
- **說明**：第一行是鉤子，第二行寫給誰看；外語的標題說明走第 9 節的語言批次。
- **封面**：1280×720、2 MB 以內。換畫風重做的集數不用舊畫風的季封面，從這一集的片段抽一格主角同框的畫面，加片名與集數（種田真人版第 1 集）。
- 站主要決定的欄位（合成內容揭露、兒童專屬、公開時間）交給站主，代理不代填。

## 11. 上 YouTube

- **誰按**：站主。代理準備好上架包，在 Studio 登入、公開與排程是站主的事。
- **什麼時候**：上架包核准、勾的語言都做好或略過以後，影片進「可以上架」。站主也可以先在 Studio 傳成私人、貼網址，排程等語言做好才送出（`publish.md`〈語言〉）。
- **API 不能用時**（配額用完、還沒過稽核）：照 [`MANUAL-UPLOAD.md`](../MANUAL-UPLOAD.md) 的手動模式下載檔案、複製文字，在 Studio 上傳。
- 上架以後，主機才會把這一集備份到雲端硬碟並在核對後刪主機上的檔（[`BACKUP.md`](../BACKUP.md)）。

## 12. 工具在哪裡

審片工具放在種田的資料夾，祖媽借用同一份（祖媽第 2、3 集的工作備份 `transfer/tn-e003-work` 裡有 scratchpad 複製的 `cut-qa.py`、`cut-jumps.py`、`audio-qa.py`、`continuity-sheets.py` 與 `assemble-v4.mjs`）。
路徑相對於 `docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/`，除非另外寫明。
2026-11-08 以前，標「這個 PR 帶進 main」的檔只在種田的工作分支 `claude/trusting-shannon-g7dl74`；PR #2047 原樣帶進來，合併後就在 main 上。

| 工具 | 在 main 上嗎 | 備註 |
| --- | --- | --- |
| [`cut-qa.py`](../series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/cut-qa.py) | 這個 PR 帶進 main | |
| [`cut-jumps.py`](../series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/cut-jumps.py) | 這個 PR 帶進 main | |
| [`audio-qa.py`](../series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/audio-qa.py) | 這個 PR 帶進 main | |
| [`continuity-sheets.py`](../series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/continuity-sheets.py) | 這個 PR 帶進 main | |
| [`independent-review.md`](../series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/independent-review.md)（獨立審片 brief） | 這個 PR 帶進 main | 較早的版本，以第 5 節為準 |
| [`preflight-prompts.py`](../series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/preflight-prompts.py) | 這個 PR 換成工作分支的新版 | 新版多了 `four`、`smile-ref`、`headroom`、`skin`、`glow`、`smile`、圖片清單檢查；拿掉了 `collar`（站主 2026-11-07 低領可以） |
| [`retake.py`](../series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/retake.py) | 這個 PR 換成工作分支的新版 | 新版多了 `drop_pictures` |
| `storyboard-check.py` | 有 | 種田工作分支反而沒有（分支開在它合進 main 之前） |
| `.agents/skills/minimax-h3-colab/scripts/cuts.py` | 有 | 種田工作分支沒有 |
| `camera-feel.py`、`colab/route-a/stage-clips.sh`、`headtrim.sh` | 有 | |
| [`hailuo/assemble-v4.mjs`](../series-plans/zhong-tian-qu-qi/production/hailuo/assemble-v4.mjs) | 這個 PR 換成工作分支的新版 | 新版多了 `clip_voice`、`voice_skip`、`subtitle_lines`、`move_lines`、`slow_shot`、`flash`，並寫 `<stem>.lines.json`。預設慢放上限仍是 1.25，每集的剪接表要寫 `"slow_max": 1.1`（[`README.md`](README.md)） |
| [`hailuo/edit-dh-e901-live.json`](../series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e901-live.json) | 這個 PR 帶進 main | 種田真人版第 1 集的剪接表 |
| [`live-action/refine-prep.py`](../series-plans/zhong-tian-qu-qi/production/live-action/refine-prep.py)、[`stage.py`](../series-plans/zhong-tian-qu-qi/production/live-action/stage.py)、[`pilot.py`](../series-plans/zhong-tian-qu-qi/production/live-action/pilot.py)、[`screen-test.py`](../series-plans/zhong-tian-qu-qi/production/live-action/screen-test.py) | 這個 PR 帶進 main | 真人版的挑片轉精修、組片段、提示詞、定妝照 |
| `colab/runs/e901-live/` 的 [`cut-review.md`](../series-plans/zhong-tian-qu-qi/production/colab/runs/e901-live/cut-review.md)、[`cut-review-2.md`](../series-plans/zhong-tian-qu-qi/production/colab/runs/e901-live/cut-review-2.md)、[`expression-review.md`](../series-plans/zhong-tian-qu-qi/production/colab/runs/e901-live/expression-review.md) | 這個 PR 帶進 main | 審片報告的範例 |
| [`route-a.md`](../../../.agents/skills/minimax-h3-runpod/references/route-a.md)（RunPod skill） | 這個 PR 換成工作分支的新版（323 行） | 共用區引用的「runpod〈…〉」各節都在第 134 行以後 |
| `.agents/skills/animation-camera/scripts/shot_reading.mjs` | 有 | |
| 祖媽 `production/tools/compile.py`、`parse_script.py`、`refs.py` | 有 | 祖媽的轉換與參考圖工具 |

工具要給別的劇用之前，先查寫死的地方：`preflight-prompts.py` 的角色名對照表（`NAMES`）、`audio-qa.py` 把說話人 `xitong` 當系統聲。
