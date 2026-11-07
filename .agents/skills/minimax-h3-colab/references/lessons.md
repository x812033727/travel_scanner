# 實跑教訓（2026-10-28／29，《種田娶妻打天下》第 31 集）

第一次在雲端 session 用這條路做一整集時踩到的坑，照「先看哪個再決定怎麼做」排。數字是當天 A100 高 RAM（6.77 CU/hr）量到的。
票 `2026-10-28-31-colab-h3` 有逐小時的紀錄。

## 1. 畫風與臉：有 3D 定妝照的作品走 Ref2VA，不畫首格

- **Qwen-Image-Edit 畫的首格到不了海螺那種寫實 CG**：三輪提示詞（海螺長稿、短指令、短指令＋整段畫風＋20 步 base）、單人特寫、提示詞寫死
  「同一張臉、毛孔、次表面散射」，皮膚還是平滑、臉偏圓、偏動畫電影。髮型與服裝像，臉不像，觀眾會覺得換了演員。這是模型傾向，不是提示詞問題。
- **H3 reference 模式直接吃定妝照，畫出來就是定妝照那種質感**（`<Picture N>` 給角色定妝照＋場景圖）。所以有 3D 定妝照的作品，片段用
  Ref2VA（`production/colab/ref2manifest.mjs` 那種清單），首格那一步省掉；首格路線留給要先審構圖、或要當靜圖的鏡。
- **1920×1088 比 1344×768 更守得住臉**：低頭、轉頭那幾格在 768p 會柔化成別人，1088p 守住。代價：6 秒一支約 12–17 分鐘、1.5–2 CU
  （768p 約 4–5 分鐘、1 CU）。同一個 seed 換解析度構圖會變。`hero` profile（20 步）對臉沒有幫助，別為了臉開它。
- **角度臉參考有小幫助**：每個角色「定妝照＋從舊集首格裁出來的 2 張不同角度臉」（`refs-dh/angles/<id>-angle-*.png`），最多九張；
  裁到臉，不要帶舊版服裝（唐小棠的舊抹胸）。沒有舊首格的角色只給定妝照也能用。
- **Qwen 場景圖的否定句會被畫成字**：提示寫「empty location plate」仍畫出村民；改寫成大寫的 `NO PEOPLE AT ALL` 重畫，模型直接把這幾個字畫成一塊牌子
  釘在渠邊，人照樣在、井坑還多了水。場景圖不要用否定句，寫正面的「只有工具靜靜擺著、清晨還沒有人來」那類描述；
  畫出來有人就留著用，靠片段正文的人數句壓住（「He is the only person in the frame」）。
- **Qwen 首格若還要用**：提示詞要短指令式、對應表放最前面（「Put the woman from image 1 into the yard from image 2…」），海螺那種 2,500 字長稿
  會把人物沖掉（整張只剩場景）；場景參照圖會壓過文字（要「斷流」就別給有水的場景圖）；表情會抄定妝照（要怒就寫 change his expression to anger）。

## 2. Ref2VA 正文少了什麼就會出什麼錯

- **沒寫構圖就沒有構圖**：gen-dh 的片段正文只有動作與運鏡（構圖本來交給首格），Ref2VA 拿到會自己決定景別——分鏡要特寫、扇子掉地，
  出來是全身遠景、扇子在手。把首格提示詞「, 16:9 frame.」之前那段構圖放進錨句後面（`Initial composition: …`）。
- **沒寫人數就會有分身**：單人特寫的背景常再畫一個同一人（定妝照是全身、鏡頭是特寫）。寫 `He is the only person in the frame; no second copy
  of anyone appears.`（雙人寫 `Only these 2 people are in the frame…`）。
- **表情會抄定妝照**：定妝照都是笑臉，第 32 集旱災裡王二牛舉鋤衝壩、說「一整天了」都在笑（s01、s18）。錨句補一句
  「Facial expressions follow the action and lines described below, not the reference pictures: the pictures fix the face, hair and costume only,
  never the mood.」（ref2manifest 現在自動加），正文再把當下的情緒寫明（furious、worn out）。
- **光有那句還壓不住：笑寫在角色錨句裡**（第 33 集 s08、s09，兩條路線都笑著扛梁）。`cast.json` 寫許硯「eyes that crinkle when he grins …
  a slightly mischievous smile」、王二牛「a wide white-toothed grin」，王二牛的定妝照本身就是露齒大笑；這幾個字每鏡都進錨句，蓋過「表情跟動作走」。
  錨句只寫長相，不寫表情（2026-10-30 起 cast.json 已改）；要的表情在正文用正面寫法寫出來：`his face strained, brows knitted, teeth gritted`、
  `his brows draw down, his eyes narrow, his lips press into a thin line`。兩鏡重抽第一次就對。
- **道具要寫大小**：「the old roof beam」畫成鋤頭柄或長竿；改成 `a heavy old roof beam, a squared dark weathered timber as thick as a man's thigh`
  才是梁，而且真的扛在肩上。
- **錨句的髮型跟定妝照不合時，低解析度照字畫**：許硯的錨句寫「loosely tied back」，定妝照是頭頂髮髻；960×544 草稿就把髻畫掉。錨句照圖寫
  （`gathered up into a topknot on the crown`）。
- **參考圖裡的人就會被畫進畫面**：鏡裡「看著阿令走遠的許硯」若把阿令的定妝照也給了，模型可能先拍阿令遠景再切到許硯（鏡內出現切點）。
  畫外的人不給參考圖、正文寫 off screen。
- **角度臉參考裁太緊會生出沒有身體的頭**：王二牛的角度臉只裁到頭部，Ref2VA 畫出一顆飄在溪床上的頭（s24）。角度臉要含肩膀，
  正文點明 `his whole body from head to feet in the frame`，或乾脆只給全身定妝照。
- **場景參照圖會壓過劇情**：斷流的溪給了有水的場景圖，前 1–2 秒溪裡有水、之後才龜裂（像縮時）。劇情改變場景狀態的鏡（乾、燒、塌）不給場景圖。
- **分鏡裡的「畫邊一截肩膀」會被放大成主角**：寫了 `a strip of Xu Yan's shoulder at the frame edge`，出來是許硯的背影當主體。畫外的人連局部都別寫，
  或寫成 `only a hand and a bowl enter from the edge`。
- **夜景要寫光線不變**：錨句只保外觀與場景，6 秒內冷月光會漂成暖日光；motion 補 `the cold moonlight and deep blue night stay unchanged`。
- 外貌段逐字放進錨句、放在動作之前，每鏡同一段字（domoai 的 H3 一致性指南）；`cast.json` 的 appearance 直接貼。

## 3. 連線：1012 不是 runtime 死了，是 CLI 放棄了

- `colab exec` 跑 12 分鐘的片段時，Colab 的 runtime 代理每隔一陣子送 WebSocket close code **1012（server_draining）**（一天四次，99–784 秒後），
  代理狀態 `recentRelayFailures` 看得到。**runtime 本身還活著**（之後 `assignments` 還在），kernel 也還在算；是 CLI 把斷線當失敗、上游 runner
  整批放棄，之後沒人再連，runtime 約 30 分鐘後被 Colab 當閒置關掉。Pro+ 的 24 小時是真的，別怪配額。
- **解法：`scripts/h3_detached.py`**——把筆記本的 code cell 串成腳本上傳，在 runtime 用 nohup 背景跑（ComfyUI 成了它的子程序，kernel 重啟
  也不死），本機每 60 秒用幾秒的短 exec 讀 log 與 pid，看到 `H3_DETACHED_DONE` 就 `colab download`。斷一次連線只損失一次輪詢。
  一整集用它連跑 36 鏡，每支 14–21 分鐘（含偶爾一次輪詢逾時）。
- 真的被 Colab 收走（session `not found`、`assignments` 空）就重開 session 接著跑；已下載的片會被跳過，不重扣。
- **Hugging Face 下載會 429**（xet CDN「Too Many Requests」），筆記本的下載格一倒後面的格全是 NameError，整批 failed；
  重跑同一個 session 即可（抓到的檔留在 `/content/ComfyUI/models`）。`images.py`／runner 看到 429 應該自己重試一次（還沒做）。
- **`colab exec` 也會無聲掛住**：Qwen 場景圖批次跑到第五張，CLI 收到一格的 execute_reply 之後就只剩每分鐘一次 ping（`~/.config/colab-cli/colab.log`），
  等不到 idle 狀態，會一直等到 `--timeout`（30 分鐘）才倒。`refs.progress.json` 的 `updated_at` 超過 7 分鐘沒動就是這個：`kill` 那個 `colab … exec` 的 pid，
  批次會把那張記 failed、其餘 cancelled 然後結束，再用 `--only <剩下的 id>` 同一個 session 重跑（約 2 分鐘一張，白扣的只有那一張）。
- `colab restart-kernel` 會連 ComfyUI 一起殺（它是 kernel 的子程序）；中斷一支正在算的片用它最快。

## 4. 雲端 session 本身的限制

- **Bash 工具的背景指令最多 2 小時**，整集 7 小時的批次要 `setsid nohup … & disown` 脫離；worker 或容器重啟仍會把它帶走，重啟後檢查
  `pgrep -f h3_detached.py`、沒了就重跑（它會跳過已完成的）。
- **`pkill -f <樣式>` 會殺到自己**：樣式出現在自己那條 bash 的命令列裡，結束碼 144。用 `for p in $(pgrep -f …); do kill $p; done` 或先 pgrep 再 kill pid。
- 每次 `bootstrap.sh patch` 會先 `git checkout` 還原上游再套 profile；在快取副本上手改的東西都會被還原（畫布上限現在由 patch_notebook 套，
  不用手改）。
- 兩本筆記本共用一個 session：Qwen 筆記本先啟動的 ComfyUI 沒裝 VideoHelperSuite，H3 筆記本沿用它會缺 `VHS_VideoCombine`。session 一開先
  `colab exec` 把 ComfyUI 與 VHS clone 好，Qwen 啟動的 ComfyUI 就帶著 VHS。
- 上游 runner 把 `output_name` 的「.」換成「_」再接 `_<id>.mp4`（`s10-t1.mp4` → `s10-t1_mp4_s10.mp4`）；直接寫 `output_path`。
- **雲端剪接的面板全是方框**：`assemble-v4.mjs` 的字型寫死 Windows 的微軟正黑體，Linux 上 drawtext 退成沒有中文的字型；
  現在非 Windows 用文泉驛正黑、`ZT_FONT` 可指定。剪完先看一格面板再送後台。
- 影片工具權杖的配對碼存在主機 Redis、10 分鐘有效，部署會讓它失效；部署完重跑 `login --colab`。後台卡片叫「影片工具權杖」。

## 5. 錢與時間（一天的帳）

| 項目 | 數字 |
| --- | --- |
| A100 高 RAM 費率 | 6.77 CU/hr |
| 冷啟動（裝 ComfyUI、抓模型） | 約 10 分鐘；Qwen 兩組約 29 GiB、H3 Ref2VA int8 約 20 GiB |
| Qwen 首格（8 步）／（20 步 base，1920×1088） | 40 秒–1 分 45 秒／1 分 20 秒–2 分 46 秒 |
| H3 FL2VA 6 秒 1312×736／1920×1088 | 約 4 分鐘／約 13 分鐘 |
| H3 Ref2VA 6 秒 1344×768／1920×1088 | 約 8 分鐘／12–17 分鐘 |
| 被收走或放棄的 session | 每次約 1–2.5 CU 白扣 |
| 一集 37 鏡 Ref2VA 1088p 估 | 約 70 CU，加重拍約 90 CU，GPU 約 8 小時 |

## 6. 三段式路線接 Ref2VA（2026-10-30，第 33 集小樣）

站主看過 s08、s09、s21 兩條路線並排後，第 33 集起用 **路線 A**：Ref2VA 960×544 `hero` 草稿 → σ0.5 補細節 → SeedVR2 7B 到 1920×1080，
全在 G4。數字與並排在 `three-stage.md` 第七節，逐段帳在票 `2026-10-30-zhong-tian-e033-g4-pilot`。

- **後兩段不改動作也不救臉**：草稿裡漂掉的臉、畫掉的髮髻，一路帶到 1080p。審片與重抽都在第一段做，那時一支約 0.5 CU；
  過了第二段才發現就要三段重付。
- **重抽每鏡給兩個 seed**：s08 一個 seed 讓許硯雙手撐膝、梁只在二牛肩上，另一個對；s09 剛好相反。兩支草稿約 1 CU，比重跑三段便宜。
- **「小幅度推近」常推過頭**：s09 三支草稿有兩支從近景推到大特寫，加 `the framing stays a close-up of his face from start to end` 只好一點。
  要鎖景別就寫 static shot。
- **路線 B（1088p 原生）不是全面輸**：s08 的彎膝、髮髻比 A 準；但 s09 推過頭帶廣角變形、s21 前景多出被裁的大人。A 一支約 0.9 CU，B 在 A100 約 1.8 CU。
- **`h3_detached.py` 帶 `COLAB_GPU=G4` 曾開成 A100**：它用 `h3.sh start` 開 session，而上游 `runner.py start` 的 `--gpu` 預設 A100、不讀
  `COLAB_GPU`。2026-10-30 起 `h3.sh start` 沒給 `--gpu` 就補 `--gpu "$COLAB_GPU"`（票 `2026-10-30-h3-sh-start-ignores-colab-gpu`）。
  開跑後仍用 `colab sessions` 看一眼 `Hardware:`。`h3_detached.py` 跑完**不會停** session，自己 `h3.sh stop`。
- **第二、三段同一個 session 接著跑**（`refine --session X` 再 `upscale --session X`，最後 `stop`）：少一次冷啟動，兩鏡兩段 15 分鐘、2.2 CU。
- 第三段的輸出叫 `<id>_1080.mp4`，不是 `<id>.mp4`；找檔時別以為沒產出。
- **只給場景圖的特寫（insert）會先畫一段場景空景**（第 33 集 s04、s17、s27）：參考圖只有一張場景圖時，模型開場先把那張圖原樣畫出來，
  0.5–0.8 秒後才跳到正文寫的特寫，等於鏡內多一個剪點；s27 結尾還把畫好的圖紙抽走。正文加「The shot opens directly on this close insert
  from its very first frame」救得了 s04（兩個 seed 一個對），救不了 s27（兩個都還有）。這種鏡剪接時剪掉頭尾最省，或改走首格路線。
- **特寫鏡不給全身定妝照**（第 33 集 s32、s37）：給了全身定妝照＋角度臉，即使寫了「He is the only person in the frame; no second copy」，
  畫面還是一張特寫臉加一個站在旁邊的全身許硯。只留兩張角度臉（`<Picture N>` 重新編號）後兩鏡四個 seed 都只剩一個人。
- **劇情要乾就拿掉有水的場景圖**（第 33 集 s38，新渠的場景圖畫的是有水的渠）：正文寫 dry channel，出來渠裡有水；拿掉場景圖、正文補一句
  `the channel bed beside him is bone-dry cracked mud from end to end` 後兩個 seed 都乾。第 2 節「場景參照圖會壓過劇情」的又一例。
- **角度臉若是舊服裝，特寫要留全身定妝照**（第 35 集 s07、s14）：唐小棠的角度臉是從第 1–30 集首格裁的，穿舊版低領；特寫只給角度臉時
  低領被畫回來。`ref2manifest.mjs` 的 `PORTRAIT_ALWAYS` 讓她的特寫保留定妝照；換過服裝的角色都要加進去。
- **只給場景圖的特寫不一定是跳接**（第 34 集 s04、s12）：有時是從場景遠景開始、手和道具從畫面外伸進來，`route-a/headtrim.sh` 偵測不到剪點就原樣保留，
  這種可以用；真正的跳接（第 33 集 s17、第 35 集 s01、s05、s36）用它剪掉開頭。
- **劇情要乾、但這鏡只有那張有水的場景圖時**（第 36 集 s07、s34、s39）：場景圖不能拿掉（Ref2VA 至少要一張），只在正文補乾的句子；有人物圖的鏡頭才拿掉場景圖。

## 7. 雲端 session 跑整集時的操作教訓（2026-10-30／31，第 33–35 集）

- **第二、三段一律 `--detached`**：`refine.py`、`upscale.py` 的 `colab exec` 一掛幾分鐘，一晚卡六、七次（20、55 分鐘各一次）。`--detached` 用
  `colab_detached.py` 在 runtime 背景跑、本機短輪詢，第 34 集切換後第二段 24 支沒再卡過。第一段用 `h3_detached.py`（`route-a/st1.sh` 已改）。
- **SeedVR2 筆記本以前會重算整個 session 看過的片**（`s3_in/` 不清空，第二批算十支）：2026-10-30 已修，舊 session 上的 `/content/s3_in` 要清掉。
- **兩個 G4 session 可以同時跑**：一集補細節、下一集畫草稿，扣點約 20 CU/hr，日曆時間少一半。
- **執行中的 bash 腳本不要原地改**（`open(p,'w')` 或 `>`）：bash 邊執行邊讀檔，迴圈之後的收尾（停 session、殺看門狗）會被跳過，session 一直開著扣點。
  要改就寫新檔再 `mv`（`sed -i` 也是換檔，安全）。
- **`pgrep -f` 會比對到啟動它的那個 shell**：背景指令把整段 heredoc 放在 `bash -c` 的命令列裡，等「某腳本結束」的迴圈會永遠等下去。
  比對 pid（`$!`）或用 `pgrep -x`，不要用腳本名稱的字串。
- **`kill` 時別用 `pkill -f <字串>`**：同一個道理，會把自己這個 shell 一起殺掉（exit 144）。

## 8. 草稿審片學到的（2026-10-31，第 37–38 集）

- **沒有定妝照的配角會變成卡通比例**：城門守衛、隊長這類只寫在提示詞、沒有參考圖的人，近景常出大頭、誇張五官（第 38 集 s28、s42），
  跟有定妝照的主角放在一起就跳戲。寫這種鏡頭要加一句「realistic 3D CG proportions like the other characters of the series, a normal-sized
  head and natural features, never a cartoon caricature」；常出場的配角就畫一張定妝照。
- **說擔心的台詞會笑**：唐小棠說「燒得太厲害，藥壓不住」（第 38 集 s05）、餵藥（s30）、喊「滾出去！」（第 37 集 s29）都笑出來；她的定妝照是笑臉。
  有台詞的鏡頭，表情要寫成「整個鏡頭都 worried／furious，never smiling」，只寫情緒形容詞壓不過定妝照。
- **病人會被畫成健康的**：發燒的小禾被扶起來餵藥（第 38 集 s30），模型讓她坐直、抱著兔子、眼睛睜開。要寫「limp, eyes half closed, too weak to
  hold anything」，並把道具放到別處。
- **只有場景圖的手部特寫會換錯人**：第 38 集 s31 餵藥的手變成許硯的藍灰袖子、小禾變成短髮男孩。插入鏡要寫明「只有誰的哪個部位在畫面裡、
  手上是什麼顏色的袖子、不出現誰」。
- **上一鏡上了馬，下一鏡要再說一次**：第 38 集 s15 阿令已經上馬，s17 又站在地上牽馬。動作接續的狀態要寫成「already mounted for the whole shot」。
- **跳躍、越過障礙要指定機位**：s26 跳過拒馬沒拍到。寫「the camera keeps the whole jump in frame from the side」，讓整個弧線留在畫面裡。
- **道具形狀要寫清楚**：「broad curved sabre」被畫成直的日本刀（第 37 集 s37）；寫成「a heavy single-edged dao with a wide curved blade, not a straight sword」。
- **加一句修正句不一定救得回來**（第 38 集重抽結果）：笑臉（s05）和上馬接續（s17）一次就修好；配角卡通比例（s28、s42）、
  跳過拒馬（s26）、插入鏡換人（s31）重抽一次都只好了一半。這三種要從根上改：配角畫定妝照、跳躍拆成起跳與落地兩鏡、
  插入鏡給一張同角色的參考圖，不要只靠提示詞。
- **只有場景圖的插入鏡，手若是「滑進」畫面就沒有硬切**（第 36 集 s07），`headtrim.sh` 找不到切點；用 `stage-clips.sh NN sNN@秒數`
  固定從第幾秒開始。
- **一大群火把會被畫成沒有人拿、像液體一樣流**（第 36 集 s34、s39，站主 2026-10-31：「火把怪怪的，沒看到人，移動速度超快」）：
  「river of torches pours / rolls / spreads」這類比喻會被照字面做成會流動的火光，幾秒內就流過整片山與田；「hundreds of torches」沒提到人，
  就是一片插在地上的火把。要寫成「每一支火把都被一個走著的人高舉著，火光下看得到人影」，速度寫「slow steady walk」，
  並寫明整個鏡頭只前進一小段、到不了哪裡。
- **不該出現的人，要從參考圖拿掉，不是只在提示詞說「不在畫面」**（第 39 集 s14）：白大夫的馬上特寫帶著阿令的三張參考圖，
  第一次兩人並排坐著，重抽加了「A-ling is not in the frame」還是讓她站在路上。參考圖裡有誰，模型就會把誰畫出來；
  特寫只留那一個人的圖，提示詞裡提到另一個人的字（連「她的頭髮從旁邊掃過」）也一起拿掉。同理，第一段重複出現同一個人
  （第 39 集 s16 兩個許硯、s46 兩個刁七）加「appears only once… no second copy」一次就好。

## 9. 畫定妝照與場景圖（2026-11-01，第 42–60 集的 25 張）

Qwen-Image-Edit-2509（`h3.sh images`，`lora: false`、20 步、CFG 4、空白 latent）拿一張現有的圖當 image 1「同畫風、不同的人／地方」。

- **image 1 會被抄：臉、服裝、光腳、背景都會。** 第一批用刁七的定妝照（全身、光腳、臉上有疤）當參考，周員外、杜鐵、魏珣都長成刁七的臉、
  全部光腳；用祠堂（牆上一排有字的牌位）當場景參考，每張場景都長出亂碼匾額。換成鄭伯（海螺時期的半身照、深藍煙霧背景）與州城書院門口（匾額是空的）
  之後，臉與服裝才照外貌段畫。挑參考圖：跟要畫的人同類型的衣著、沒有疤或道具、沒有字；提示詞寫「a completely DIFFERENT person with a different face, age, build and costume」。
- **光腳要寫鞋。** 「cloth shoes on his feet」加進去才不光腳；「not smiling」壓住參考圖的笑臉。
- **場景提示詞裡出現的人就會被畫出來**：「a queue of scholars」「dense crowds」「steps where two people could sit」「a busy street beyond」都畫了人。
  寫成空的（「an empty sunlit street beyond」「three low stone steps」）。「no people」這類否定句沒用，第 32 集 jingkeng／xinqu 就是。
- **不要字要正面寫**：「Every plaque, board, banner and wall is plain and blank, bare wood and bare plaster」，並把會帶字的東西寫成別的
  （「a plain bare wooden beam above the doorway」取代匾額）。
- **人物的道具照字面畫**：冷鐵「a short dagger hidden in his right sleeve」被畫成手上拿刀；只寫看得見的東西。「black runner's cap」被畫成兜帽，
  要寫形狀（「a small round black cloth cap sitting on top of his head, his whole face clearly visible」）。
- **冷啟動那一張最容易斷線**：`colab exec` 從裝 ComfyUI、下載 29 GiB 模型到畫完第一張要十幾分鐘，連兩次 `Connection was lost`、一張都沒畫出來。
  `h3.sh images --detached`（`colab_detached.py`，跟 refine／upscale 一樣）之後沒再斷過。一張 1088×1920 或 1920×1088、20 步約 1.3 分鐘；
  冷啟動約 10–15 分鐘。每次新 session 都要重新冷啟動，所以一批放同一個 manifest。
- 先用 `--only` 試四張（兩人兩景）看參考圖對不對，再跑整批。
- **Hugging Face 429**：沒有 `HF_TOKEN` 時下載模型是匿名的，連開幾個 session 之後被限流（`CAS Client Error … 429 Too Many Requests`），腳本死了
  runtime 卻還開著在扣 CU，輪詢只回「no answer」。看 `progress.json` 的 `log_tail`，停掉本機那一輪，用 `--session <同一個>` 重跑（已下載的模型還在），
  跑完自己 `h3.sh stop`。
- **`latent: "image1"` 的縮放**：新版 ComfyUI 的 `ImageScaleToTotalPixels` 要 `resolution_steps`，補了之後輸出仍是照面積換算的尺寸（1248×1664 變 1272×1704），筆記本的尺寸檢查就丟掉整張圖。現在改用 `ImageScale` 縮到畫布本身。只改一處的編輯（例如剃掉多畫的鬍子：image 1 用那張圖、`latent: image1`、「Edit image 1: remove … Keep everything else exactly the same」）一次就對。
- **背景跑時輪詢一直「no answer」**：遠端腳本已經死了（429、斷言失敗），輪詢卻收不到回應，本機就一直等、runtime 一直扣 CU。超過預期時間就自己用 `colab exec --session <名> --file <讀 /content/qie_<id>.log 的小腳本>` 看遠端 log，ComfyUI 已畫好的圖在 `/content/ComfyUI/output/`，可以直接 `colab download`。
- **新 runtime 的第一個 exec 會等 kernel 啟動**：`colab_detached.launch` 原本 120 秒就放棄（2026-11-01 兩次），已放寬到 540 秒。
- **跟既有定妝照同風格的做法**：畫布用 3:4（1248×1664），image 1 用海螺時期的胸像。同類型的人（官員）一次就對（褚知府）；不同類型的人會抄 image 1 的臉，
  先用「Replace the man in image 1 with a completely different man … Keep only the render style …」畫對人（會變全身），再把胸口以上裁下當 image 1、
  原本的胸像當 image 2 重畫（`production/colab/runs/refs-e042-e060/round4-refs4.json`）。

## 10. 站主定的領口標準（2026-11-02）

唐小棠「高領、不能透、不能露胸」的規矩，站主看過第 45 集 s33、s36（立領扣到喉嚨、開襟外罩下露出抹胸上緣與一塊胸口皮膚）後說「這種露胸程度還好，也蠻不錯的」。這個程度可以用，不必重抽也不必裁；衣料透明、低領露出乳溝、抹胸滑落這類更露的才重抽。

## 11. 信件與手部插鏡（2026-11-04，第 54 集）

- **信件插鏡要抽整段影格看，不能只看四格縮圖。** 第 54 集 s03 縮圖上信很小，第一輪判「小而可接受」；逐格看才發現後半信被接住、信面一列列清楚的假字。
  有信、紙、告示的鏡頭，用 `fps=2` 抽整段再判。
- **「雙手拿著白紙」會畫成西裝。** s40（夜裡河灘上拿白紙的手）第一輪是西裝袖加白襯衫袖口；改寫「宋式交領棉袍寬袖、沒有袖口、沒有現代衣物」重抽兩次仍是白袖口，
  其中一個還有西裝褲和皮鞋。最後改成「只拍紙與兩邊指尖，畫面裡沒有袖子、手腕、手臂、腿和鞋」才乾淨（retake4 的 540401）。
  手部插鏡一律看袖口；寫法直接把袖子排除在畫面外，比描述袖子可靠。
- **喊出來的短台詞會被畫成字幕**（第 53 集 s05）：開拍前就用 `extras.json` 的 `_replace` 把「「哥！」」這類短喊改成「張嘴喊」，第 55 集 s25、s27、s38 這樣先處理。

## 12. 製作前每鏡要寫清楚的事，與開拍前的自動檢查（2026-11-05，第 1 集重製版 r2）

**檢討**：r2 第一批 70 支草稿裡，辦公室兩鏡許硯穿古裝、二牛三鏡背上多一個大甕。不是劇本沒寫，是**角色的外貌文字和這一鏡要的樣子打架**：
產生 prompt 的程式把 `cast.json` 的外貌整段貼進每一鏡，模型照文字畫，不照參考圖。許硯的現代西裝參考圖配上「髮髻、書生袍、布鞋」的文字，畫成古裝；
二牛的外貌寫著「肩上扛著鋤頭或扁擔」，每鏡都畫扁擔，有時再自己掛上東西。試拍 s05 已經出現過大甕，只是沒選那支、沒回頭改描述。

**製作前，每一鏡要逐項寫清楚、並跟 prompt 全文對過**（不是只看劇本那一列）：

| 項目 | 要寫什麼 | 這季踩過的坑 |
| --- | --- | --- |
| 服裝 | 這鏡每個人穿哪一套；跟平常不同就用 `cast.json` 的 `shot_looks`（`character_looks`），不要只換參考圖 | r2 s01–s02 古裝進辦公室 |
| 道具 | 誰手上、肩上、背上有什麼；角色的**基本外貌不寫道具**，要扛東西的鏡才選有道具的 look | r2 二牛的扁擔與大甕 |
| 畫面裡有誰 | 人數與各自位置；誰背對、誰只露肩；畫外的人寫 off screen | 第 54–56 集的分身 |
| 每個人的動作 | 起點、預備、主動作、收勢；站著不動的人也要給一個進場、一步或手部動作 | r2 s22 第一次動量 3.3 |
| 運鏡 | 一個；說話的近景不要只寫固定，至少慢推或環繞 | r2 對話近景動量 2–5 |
| 文字與紙 | 信、告示、履歷寫成背面、摺著、虛焦或側邊；不寫內容 | 第 54–56 集的假字 |
| 唐小棠 | 近景寫下巴以上；中景以上寫襦裙一件闔上 | 第 55 集 s39、第 56 集 s27 |
| 台詞 | 短喊不加引號（會變字幕）；內心獨白標成嘴閉著 | 第 53 集 s05 |
| 秒數 | 台詞總長 + 動作 ≤ 片段秒數；長的鏡直接買 9–12 秒，不靠慢放 | r2 加台詞後五鏡要重畫 |

**修正**：`cast.json` 給許硯加 `shot_looks: modern`，二牛的基本外貌拿掉扁擔、另開 `pole` look；`ref2manifest.mjs` 用到 modern 參考圖時改貼 modern 的外貌文字。

**開拍前的自動檢查**：`colab/runs/_scripts/preflight-prompts.py` 讀每一支 job 的 prompt 全文，`st1-ep.sh` 與 `retake-run.sh` 送出前自動跑，ERROR 就不送（`PREFLIGHT=0` 跳過）：
現代參考圖配古裝文字、`<Picture N>` 數目不對是 ERROR；基本外貌裡的道具、五字以內的短喊、沒寫空白或虛焦的紙、唐小棠近景沒寫下巴以上或襦裙闔上、
有名字卻沒掛參考圖的人是 warning，審片時逐條決定。拿 r2 已經畫好的那批去跑，它抓到了這次的古裝與扁擔。
外貌描述裡也不要寫否定句（「no topknot」）：模型常把否定的東西畫出來，檢查程式也會誤判。

## 13. 真人風格的試鏡（2026-11-06，《恁祖媽今年18》，票 `2026-11-06-tai-nainai-screen-test`）

第一部走真人風格的作品，開角色之前先做的試鏡：Qwen-Image-Edit 畫定妝照與場景圖 16 張，Ref2VA 跑第 1 集五鏡（真人四鏡、3D 一鏡對照），G4，合計約 13.8 CU。
提示詞、seed 與進度檔在 `docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/screen-test/`（`build.py` 從 `cast.json` 產生、`runs/` 是實際送出的）。

**結果**：真人可行，站主看草稿後說 3D 不行。Ref2VA 吃真人胸像，五鏡的臉都守住定妝照，同一個人換鏡不漂；說話鏡嘴有動。九十六歲以十八歲為 image 1 畫，看得出同一家人的長相。

**第一部作品還沒有任何定妝照時**：`h3.sh images` 至少要一張參考圖。用一張空白中灰底（`build.py` 自己寫的 PNG）當 image 1、提示詞寫「image 1 is only a blank mid-grey canvas: take nothing from it but the plain grey backdrop」，`latent: empty`，可以畫出人。

| 症狀 | 原因 | 怎麼辦 |
| --- | --- | --- |
| 定妝照畫成全身、臉很小（Ref2VA 認臉就弱） | 外貌段寫了鞋、褲、裙、手交疊、背挺直，模型照字面把全身畫出來 | 胸像只貼頭肩看得到的部分（`build.py` 的 `bust()`，用整字比對：「ring」不能吃掉「wearing」「earrings」）；加「A tight head-and-shoulders casting portrait… no hands, no legs, no feet」 |
| 十八歲畫成三十多歲 | 「East Asian young woman of eighteen」不夠 | 外貌段前面加「a young girl of eighteen with a youthful teenage face… clearly a teenager and not an adult woman」；還是偏二十出頭，選 take 時看 |
| 場景圖上下黑邊、角落像浮水印的字 | 提示詞寫了「film still」「establishing shot of a film set」 | 改「photograph」「empty room」，加「fills the whole frame edge to edge: no black bars, no letterbox」；畫壞的可以裁黑邊再放回 1920×1088 |
| 祠堂牆上掛軸、牌匾帶假字；左右擺反 | 「ancestral tablets」「hanging scroll」會帶字；左右只寫一次不夠 | 寫「No hanging scrolls, no calligraphy」、牌位寫「plain blank wooden」；另加一句「Layout seen from the doorway: … LEFT wall … RIGHT side」。擺位第二輪仍然擺反，場景圖要多抽幾張 |
| 片段裡燈的亮度、景別不照正文（燈 1 畫成亮的；要近景給全景） | Ref2VA 照參考圖的場景與光走，正文只寫「a bean-sized dim flame」拉不動 | 每個燈的分數各畫一張場景圖給 Ref2VA；景別一定要準的鏡改走首格路線 |
| 細到一道皺紋的連戲記號畫不出來，還多畫一枚戒指 | 模型不會穩定畫「只有一道」的細節；戒指的描述同時出現在兩隻手的上下文 | 劇本的記號改成看得見的（光、插鏡、白髮），不要靠每鏡畫中 |
| 片段裡的辮子數照正文、不照定妝照（定妝照兩條，片段一條） | Ref2VA 正文的外貌段把它拉回來 | 好事，但定妝照還是要重畫對；不要靠正文修參考圖 |
| 同一個 runtime 先跑 `h3.sh images` 再跑 H3：`ComfyUI 缺少節點：['VHS_VideoCombine']` | 出圖的筆記本先啟動了沒有 VideoHelperSuite 的 ComfyUI，H3 筆記本「使用已啟動的 ComfyUI」 | 出圖與片段分兩個 session（`h3.sh stop` 再 `start`）；第二、三段可以接在片段的 session |
| `output_name: "r1/x.png"` 存成 `r1-x.png` | `images.py` 把斜線換成連字號 | 後續步驟讀 `r1-<id>.png` |
| 冷啟動下載模型 `429 Too Many Requests`，runtime 一直開著扣點 | 匿名下載 Hugging Face 被限流（第 9 節） | 停掉本機那一輪，同一個 `--session` 重跑就過了；這次損失約 2 CU |
| 換裝時眉間畫出紅色刀疤；臉上的「水漬」畫成瘀青；壽衣、睡袍畫成 V 領 | 外貌段寫了「a scar-like deep wrinkle」「water marks on her face」，模型照字面畫傷口與污漬；「robe」本身就會帶出交叉領 | 外貌不寫像傷的比喻（改「one deep vertical frown line… the same colour as the rest of his skin」）；濕身只寫頭髮與衣服濕、臉上乾淨；長袍寫「HIGH stand-up collar closed to the throat」，兩次仍是 V 領的話換成「long buttoned house dress」之類不是 robe 的字 |
| 監看腳本把「PROMPT 長度 1429 字元」當成 429 | grep 只寫了 `429` | 比對 `Too Many Requests` |

**換裝要同一張臉**：同一個角色的兩個 look 分開畫會是兩個人；用選定的基本款當 image 1、`latent: image1`、只寫「Change only …」（`docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/tools/refs.py looks`）。九十六歲也用十八歲那張當 image 1 畫老。

**2026-11-07 補畫（`refs-r5`、`refs-r6`）**：
- 胸像畫成全身，是外貌裡的 jeans、sneakers、wheelchair、「about 180 cm tall」把鏡頭拉遠；`refs.py` 的 `bust()` 要把這些字也濾掉（玉琴從全身變成剛好的胸像）。
- 不寫 robe、改寫「pyjama-style house top … buttoned all the way up」之後就沒有 V 領，但畫出來是睡衣的小翻領，不是立領；要立領得另外描述領子本身。
- 外貌改好、又明寫「no scar, no red mark」之後，兩張裡仍有一張畫出紅色刀疤：這種字一次出兩張再挑，別只出一張。
- 手部插鏡的第二個狀態（淺紋）要以第一個狀態那張（老人紋）當 image 1、`latent: image1`、只改皮膚；從灰底重畫會多出一枚戒指、手勢也對不上。
- 每張圖在 G4 上約 1 分鐘，冷開機（下載 20 GB 模型）約 10 分鐘；12 張用了約 4 CU。images 要先 `h3.sh start --session`，或加 `--new-session --stop-on-complete`，否則送出就是「Session not found」。

**時間與點數（G4，暖機後）**：胸像 1248×1664 約 1.3 分／張；Ref2VA 960×544 `hero` 6 秒約 2.1 分／支（含冷啟動的第一支 5.2 分）；第二段 σ0.5 五支約 14 分。
站主同一天定：片段先做到 1312×736（第二段），不跑 SeedVR2，剪接時整支放到 1920×1080。
