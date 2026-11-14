# 原來如此事務所：教訓

只跟原來如此事務所有關的教訓。所有 AI 劇都會遇到的寫在 `shared.md`，奇聞和原來如此都會遇到的寫在 `explainer.md`。

寫法：一條一段，最新的放最上面。開頭寫日期、哪一集（slug）、誰發現的，接著寫發生什麼、為什麼、下次怎麼做。
已經變成正式規則的，搬進規則檔，這裡留一行「已升為規則：<檔案>」。

這份會自動同步到雲端硬碟 `AI劇/原來如此事務所/_規則與教訓/教訓/教訓.md`（docs/videos/rules-sync）。

- **2026-11-12，P29，站主決定：空間不足就完全備份到雲端再刪。** 容器的磁碟額度用完（ENOSPC）時，配音做到一半停掉、speech-journal 留下「已送出、沒有回應」的請求要手動 `forget`，輔助 worktree 也建不起來。
  站主：「如果空間不足就完全備份到雲端就可以刪除了，只要記得完全備份不要漏了就好」。刪本機工作目錄前：`todrive.sh` 傳完，再 `rclone check <本機> <雲端> --one-way` 要印 `0 differences found`，而且 `matching files` 等於 `find <本機> -type f | wc -l`，兩個都對才刪。
  已核准、已上傳或等 YouTube ID 的集數先刪（要用再 `rclone copy` 拉回，排除重複的同名子資料夾、build、segments）。長步驟開始前先看 `df -h /root`，剩不到約 3 GB 就先清。
- **2026-11-12，P06／P18，站主發現：重送上架包之後，八語也要重送。** 站上組 YouTube 語言包時，只認綁在「目前這份上架包」的語言批次（`apps/api/app/video_youtube/language_package.py`）。
  上架包因為換縮圖重送、開了新的一份之後，之前核准的八語還綁著舊上架包，站主一核准新上架包就看到「已選取的 en 配音尚未核准，請先完成語言包」。
  順序：`package` → `review-push --gate publish` → `review-push --gate languages`，兩關都請站主核准。換縮圖能進到已核准的上架包，是因為 metadata.json 記了 `thumbnail_sha256`（2026-11-12）。
- **2026-11-12，P06／P18／P21／P13，站主決定：亮底縮圖的字不能碰到人。** 亮底版（PR #2078）大字固定 150px，放不下才縮，所以西方語言一行 10 個字母左右就伸到右邊 38% 的插圖裡
  （英文 10 字母約到 925px，人通常從 800–950px 開始）。九語縮圖畫完先量：用正式出圖程式把 `h1`／`.sub` 塗成洋紅、藏掉插圖再截圖，找最右邊的洋紅像素
  （副標加 28px 底框）跟人物左緣比；超過就把那一語的 `thumbnail.text` 縮成每行 6–9 個字母（例：`Same\n**carbon?**`、`Blue dot\n**jumped?**`），副標約 28 字以內。
  繁中、日、韓、泰幾乎不會超過。已核准八語的集數不改翻譯檔（雜湊會變），只在出圖時覆寫，把九張直接交給站主（雲端硬碟 `<集數>/縮圖-亮底-20261112/`）。
  主體在中間或全身很小的鏡頭不適合當縮圖：P13 從全身的 `kid-dot-puzzled` 換成半身的 `kid-main-q`，換法照下面 P06 那條。
- **2026-11-11，sothatswhy-p21-car-sickness，接手 session：有旁白之後不要增刪行。** 為了 check-audio 把開頭一句拆成兩句，所有行號往後移，tts 的 159 個請求全部重錄（0 reused），
  check-audio 又標出 25 句（多半是聽寫雜訊）。改說法時只改那一行裡的字。另外：「內耳」常被聽成「那兒」，介紹之後改說「耳朵裡面」；「報告」會被聽成「罷工」；「猜」會被聽成「才」（P06、P18 也一樣）。
- **2026-11-11，站主決定：稿子不用硬寫，8 分鐘下限保留。** 「稿子不用硬寫，品質為主，流暢的內容才重要」；同一天也說「8 分鐘下限也幫我留著好了」（PR #2069）。兩句一起讀：內容講完、講順就停，不灌水；素材撐不到 8 分鐘、要硬補的題目不開拍，放後備（`docs/videos/so-thats-why/material-20261111/README.md`）。P06 為了 2,050 字下限，盲評時刪了 120 度的岔題又得補字，就是要避免的情況。已升為規則：dialogue-pilot README §9「長度」。
- **2026-11-11，sothatswhy-p06-bubble-film，站主決定：語速調快。** 規則是 ≥ 4.5 字／秒，P06 只有 3.74；Gemini 配音沒有語速參數，style 寫「一秒四到五個字」講不到。
  用 P06 全稿只換 style 實測三種：3.74、4.39、4.95；站主聽過選 4.39 那種（「像節目主持人，一秒五個字以上，句與句緊接、不拖長尾音」），原來如此的門檻改成 4.3。
  寫法在 dialogue-pilot README §4；`tts` 結尾會印語速。style 要寫得比目標快（寫「一秒五個字以上」才講到 4.4），模型會打折扣。
- **2026-11-11，sothatswhy-p06-bubble-film，站主發現：縮圖的人被字擋住。** 系列縮圖 `subject: "right"` 只取插圖正中約 38% 寬放在右邊；
  `kid-wand` 的小問偏左，九語縮圖都只看得到欄杆和一隻手。換成 `kid-square-q`（人和方框都在中間）。下次挑縮圖鏡頭前，先用 PIL 把候選圖裁中間 38% 看一次。
  換 `thumbnail.data.shot` 會改到 visual_hash，插圖、分鏡、組裝都變「過期」：`keyframes --shot <那一景>`（不畫新圖）→ 用累積的 `pins.json` 再 `repin`
  → 重新核准分鏡 → `clips` → `assemble`，成片位元不變，成片核准仍有效。上架包已核准時，`review-push --gate publish` 不會把新縮圖送上站
  （票 `2026-11-10-review-push-a-changed-thumbnail-never`），新縮圖要直接交給站主。
- **2026-11-10，sothatswhy-p06-bubble-film，接手 session：插圖提示詞的三個坑。** (1) 代理寫的重畫提示詞常含 `no text`，`build_scenes.py` 的 `BANNED` 會擋，
  改成正面描述（clean empty corners、plain unmarked bottle、plain bare ears）；每條 ≤ 840 字，所長鏡頭要以 Waist-up／Head-and-shoulders 開頭。
  (2) 小問鏡頭寫「台灣公寓客廳」容易畫成真人照片；畫風字放最前面、背景寫 plain flat pale cream background，再用 `--seed-offset` 換種子。
  (3) 不要修圖蓋假字（會弄壞輪廓線），換種子重畫比較快。所長的黑髮是刻意的（灰髮那句會畫成灰色頭套），代理建議加回灰髮時不要採用。
- **2026-11-10，sothatswhy-p06-bubble-film，接手 session：`pins.json` 要指 `-trim.jpg`。** 插圖有紙邊時，工具的 `file` 指向 `<景>-<take>-trim.jpg`（P06 有 89 景）；
  pins 寫成原圖會用到有紙邊的版本。repin 後把跟檔案對不上的 `margins` 拿掉。
- **2026-11-10，sothatswhy-p06-bubble-film，接手 session：新容器缺的東西。** 換容器後 `tts` 沒有沿用舊錄音（153 句全部重錄，費用很少，但 check-audio 要重跑、旁白要重新核准）；
  系列設定圖要先從 `docs/videos/so-thats-why/series-sheets/characters` 還原到工作目錄的 `_series/sothatswhy/characters/`，`look` 才會沿用；
  配樂 `sothatswhy-bed-r2.m4a` 從雲端硬碟 `原來如此事務所/_共用/製作檔/sothatswhy-shared/_music/` 取回放到 `_music/`（核對 sha256）；
  repo 的 Playwright 若比容器內建的新，`render` 找不到瀏覽器，把 `/opt/pw-browsers/chromium_headless_shell-<內建版>` 連結成 repo 要的版本號，不要另外安裝。
- **2026-11-10，sothatswhy-p06-bubble-film，接手 session：長時間的步驟會被背景時限停掉。** 背景指令預設 30 分鐘、最多 2 小時；116 景 × 3 take 的插圖約 4.5 小時。
  用 `setsid nohup … & disown` 脫離 shell 跑，再用 until 迴圈等完成檔；`keyframes` 重跑會保留已畫的景。雲端硬碟備份不要跟 render／assemble 同時跑（會出現 differences），等寫檔的步驟結束再傳。
- **2026-11-11，sothatswhy-p21-car-sickness，接手 session：session 閒著時容器會被收回，脫離的程序跟著死。** 監看的 until 迴圈到 2 小時被停掉之後，
  session 沒有任何在跑的背景指令，容器在半小時內兩次重開（`uptime` 0 分鐘、沒有 node 程序、沒有完成檔），`setsid` 的插圖也一起沒了。
  工作目錄 `/root/mokaair-work` 與 repo 都還在，`LEASE` 記的是舊 boot id，直接重跑 `keyframes` 就從斷點接著畫。長步驟跑著時一定要同時有一個
  harness 追蹤的背景監看（`run_in_background`，上限 2 小時，到期就再開一個），只靠 `send_later` 排的檢查不夠：它在閒著的容器重開後才觸發。
- **2026-11-11，sothatswhy-p21-car-sickness，接手 session：站上還沒有這一集的紀錄時，qa 的 policy 會要「有示範」。** 站上判定要不要問示範，看的是
  `VideoProject` 那一列的 category／format（`apps/api/app/video_automation/judge.py` `policy_questions_for`）；沒有那一列就當教學片問，
  P21 第一次 qa 得「有示範 0.23」沒過。`video.json` 寫的 `explainer`／`drama` 要推過一次才進站：先跑
  `review-push --slug <slug> --report-only`（不送任何關卡），再跑 qa，就變「有示範：不適用（解說）」。成片最後淡出的那 1.6 秒會被
  silencedetect 算成最長空檔，不是台詞之間的空檔，看時間點再判斷。

- 2026-11-13（P26）：MiniMax M Plan 是 5 小時一窗（UTC 00、05、10、15、20 點起算）加每週一窗。一集 90 景 × 3 張的關鍵畫面在 04:41 用完當窗（回 2067 Token Plan usage limit），05:00 換窗後就恢復。長的 keyframes 或八語配音之前先跑 `node tools/video/cli.mjs minimax-quota`，看 `general` 的 `current_interval_remaining_percent` 與 `end_time`；不夠就把剩下的鏡頭排到下一窗，不要升級方案或買點數（站主決定）。
- **2026-11-12～13，sothatswhy-p20-microwave-metal、sothatswhy-p26-plane-window：製圖的教訓。**
  - **角色描述照設定圖寫，連檢查的人也一樣。** P20 的放大檢查 brief 抄了舊描述「所長灰挑染」，四個代理照著放行，分鏡評分才抓到「角色一致 4」。
    所長是一色黑髮低馬尾、圓框眼鏡、耳後黃鉛筆；灰挑染、耳環、口紅、像小孩都算走樣。小問是黑色齊下巴鮑伯頭；棕髮、馬尾、丸子頭、雙辮、運動服都算走樣。
    `CHARACTERS` 的 appearance 字串不能改（設定圖用它當鍵），所以要在每個鏡頭的提示詞與檢查 brief 裡寫對。REWRITE 裡別留 "grey streak"。
  - **有效的尾句。** 所長：`glossy hair in one even jet-black colour tied in a low ponytail at the nape, small bare earlobes, natural lips, round black glasses centred over her eyes`；
    小問：開頭寫 `Flat 2D cartoon illustration … chibi cartoon girl`，髮型寫 `short straight bob ending evenly at her jaw all the way round`（擋馬尾與丸子頭，也擋照片風）。
  - **同一個鏡頭所長三輪都走樣，就改成物件特寫。** P20 的 chief-stop 改成鐵絲提把特寫、P26 的 kid-tank-q 改成方窗角裂縫特寫，第一張就過；
    把 `chief(`／`kid(` 換成 `obj(`、拿掉 REWRITE，台詞不動，劇本與旁白的核准都還在。
  - **兩個東西並排對照畫不出來。** 「方洞紙條裂、圓洞紙條沒事」畫了四輪都反或缺一邊；改成單一條紙「方洞的角裂到紙邊」才成。對照放到兩個相鄰鏡頭各畫一個。
  - **道具要跟台詞同一個。** 小問講自己的紙捲飛機時，圖模型會換成玩具客機，評分扣「圖文相符」；提示詞每次都寫出同一句道具描述（P26 的 `TUBE`），不要寫 toy airliner。
  - **抽象的「力」用具體的東西代。** 水流繞石頭、迴紋針、氣球、銅棒玻璃棒都畫得好；「應力擠在角上」可以用幾條短藍線擠在尖角，但不要畫箭頭或色圖。
  - **禁字會藏在別的字裡。** `paperclip` 含 paper、`notch` 含 no、`clamps` 含 lamp；setrw.py 的 BANNED 用 `\b` 抓不到，代理要改寫成 `wire office clip`、`V-shaped groove`。
  - **`--seed-offset` 上限 30**；一個鏡頭重畫第三輪起用 20 以上，避免撞到舊種子。站台 502 或容器重開時，從 log 找出還沒畫的鏡頭只重跑那些，別整批重來（浪費 MiniMax 額度）。
  - **放大檢查 brief 要寫清楚多輪後的標準**：第三輪起只有走樣、假字、重複角色、手臉壞、與台詞相反才算 bad，其餘給 ok 並註明，不然會一直重畫小瑕疵。
- **2026-11-13，從奇聞檔案局 c14 的教訓（PR 2068，shared.md／curio.md）借來、本系列也適用的：**
  - 只畫手的鏡頭容易冒出整張臉；說明書頁、錶面、刻度會長出字或數字。本系列的「手拿剪刀修圓角」「手指指裂縫」這類鏡頭，放大檢查時特別看有沒有多出臉；書和手冊寫成闔上的。
  - 模型畫不出指定的數量、傾斜或方向（三根手指、天平傾一邊、箭頭指哪裡）；換成不靠那個動作也對得上台詞的畫面（P26 的「三倍」改成圓洞兩側擠滿藍線）。
  - MiniMax 額度用完有兩種訊息：`answered 2067`，以及結束碼 4 的 `rejected the key or balance (The Token Plan usage limit…)`；都看 `minimax-quota` 的 `remains_time` 等下一窗，不必問站主。
  - 本系列選用 judge 退件的 take 是寫 `pins.json` 再跑 repin.py（每次 `keyframes` 之後都要重跑），不用 `keyframes import`；若改用 import，先改提示詞、跑 keyframes，最後才 import，中間不再改提示詞，否則 manifest 會被重建、匯入的圖全丟。
- **2026-11-13，P06／P21／P13／P29／P04／P01／P20：雲端容器合成的成片沒有片頭片尾。** 新容器沒有 `_branding/`，`assemble` 照做不擋，
  成片長度等於旁白（`checks.json` 的 `metrics.frames` 等於 `timeline.json` 的 `total_frames`；有包的話多 357＋630＝987 格）。
  站主上架後才發現。`branding --pull --series sothatswhy` 目前回「工人還沒安裝或 API 沒掛工作區」，所以改從雲端硬碟還原：
  `rclone copy "videobackup:AI劇/原來如此事務所/_共用/製作檔/sothatswhy-shared-archive/branding/" /root/mokaair-work/videos/_branding/`
  （`mokaair-sothatswhy-bookends-v3-endscreen`，hash 8226326…，intro 357 格、outro 630 格，核對 sha256），
  再用 `node tools/video/cli.mjs branding --series sothatswhy --json` 確認 selection 有東西。新容器開工時跟 `_series`、`_music` 一起還原。
  合成後檢查 `metrics.frames − total_frames = 987`；不是就停下來。已送審未核准的用 `assemble --adopt-branding` 重做（再跑 captions、qa、review-push）；已上傳的工具會拒絕，由站主決定要不要重傳。
- **2026-11-13（P26）：重用種子編號時會看到舊的 `-trim.jpg`。** 同一個鏡頭第二次用同樣的 `--seed-offset` 重畫，新圖沒有紙邊就不會產生新的
  `-trim.jpg`，舊一輪留下的 `<景>-21-trim.jpg` 還在；放大檢查若「有 trim 就用 trim」，看到的是舊提示詞的舊圖（P26 三個改成物件的鏡頭被判成
  「還是所長比手勢」）。挑檔時 trim 比原圖舊就用原圖（mkround 已改成比較修改時間）；釘選前檢查沒有 pin 指向比原圖舊的 trim；每輪換一個沒用過的種子區段更省事。
- **2026-11-13：雲端硬碟改成分類資料夾。** PR #2093 把原來如此的集數搬進 7 類：`AI劇/原來如此事務所/<分類>/<Pxx>/製作檔/<slug>/`
  （例如 `數位科技與通訊工程/P29`、`物理化學與日常材料/P06`、`地球天氣與太空/P04`、`人體感官與日常行為/P21`），舊的 `原來如此事務所/Pxx/` 已不存在。
  備份或還原前先在 7 個分類裡找到那一集（`_總表/` 有 catalog），不要再傳到 `原來如此事務所/Pxx/`；新集數放進對應分類，傳完重跑 `catalog.py` 更新 `_總表/`。
  還原時讀到「directory not found」先找分類，不要以為備份不見了。
- **2026-11-14：刪台詞或改縮圖字樣後，`clips` 會說關鍵畫面過期。** 插圖綁的 `visual_hash` 包含每景的台詞編號與縮圖資料，所以只刪句也會讓
  keyframes manifest 過期。不用重畫：挑一個 judge 通過、沒問題的鏡頭跑 `keyframes --shot <那一景>`（印「N 景不變、沿用」與「0 keyframes generated」），
  再跑 repin.py 並重新核准分鏡，`clips` 就能繼續。整集不加 `--shot` 跑會重試所有 needs_review 的鏡頭，花錢。
- **2026-11-14：平行代理不准用 `git stash`。** 補內容時兩個代理為了比對 lint 前後跑了整個 repo 的 `git stash`／`pop`，把另一個代理寫到一半的
  P04 檔案收走又還回來，`pop` 撞衝突時要手動合併。多個代理同時改不同集時，比對前後請複製檔案到 scratchpad，或用 `git diff`／`git show HEAD:<path>`，不要動共用的工作樹狀態。
- **2026-11-14：刪句或插句時，句子編號要固定。** 改稿代理有的照順序重編（P13、P29、P20），有的用 `cut()`／`add()` 或 `p125a` 這種插號保留舊編號（P06、P01）。
  重編的集數翻譯雖然能照文字搬到新編號，配音卻整條重新合成（P13、P29 八語 `0 reused`），新音軌一變長就要再縮翻譯；保留編號的只重配改到的句子。
  以後刪句用 `cut()` 讓那一句不進 video.json、插句用 `add()` 或字尾字母，舊編號一律不動。
