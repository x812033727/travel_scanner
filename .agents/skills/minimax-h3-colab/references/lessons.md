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
