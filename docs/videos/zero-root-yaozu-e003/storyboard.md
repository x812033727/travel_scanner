# 第 3 集〈一村人等門〉分鏡表

<!-- 給人讀的中文版；製作用的英文提示詞在 video.json。 -->

- 2026-10-16 改版：3D 國漫（國漫 CG）重拍版、一集七個片中鉤子（站主：「一集應該要兩三個鉤子以上」）。40 個鏡頭（原本 44）、四段（力氣，大／仙門瞎了眼／退貨／饅頭；原本的「燈河」不到 10 秒，併進第一段），估計約 108 秒（shot_plan 估法；lint 估 107 秒；細綱 115 秒）
- 鉤子：【開場鉤子】0:00 斧背一敲松木裂成兩半「力氣，大。」；【鉤子1】0:04–0:10 陸拾的追問被坡下三百盞燈同時亮起打斷，阿猙「等你。」；【鉤子2】0:28–0:36 他話沒說完三嬸就說「仙門那是瞎了眼！」，團團「我算的。」還知道饅頭的事；【鉤子3】0:43 孫二「喲，仙門退貨的回來啦！」；【鉤子4】0:56 錘子砸裂的石板燒得通紅冒煙；【鉤子5】1:11 歸伯的釣竿沒有鉤「魚，自己會來。」；【鉤子6】1:17–1:19 奶奶一桌菜早擺好，「您怎麼知道我今晚到？」她不答；【鉤子7】1:29–1:31 奶奶一捏饅頭停住、裡面有個硬東西，掰開掉出發光靈石與字條；【結尾懸念】1:44 火苗舔上紙角。最長一段沒有鉤子的空檔約 18 秒（0:10–0:28）
- 爽點：前半 face_slap（三嬸搶先替他罵仙門，0:28）；中段 public_vindication（三嬸一錘、全村把孫二轟出村口，0:52–1:06）
- 每一鏡都買 4 s 片段（海螺 H3 2K，12 點／秒，48 點）＋一張首格（約 23 點）：片段一次 1,920 點、期望 2,664、上限 3,840；首格 40 張約 920 點；一次合計約 2,840 點
- 檢查：lint 0 錯誤、30 項結構檢查全過、分鏡讀取 --strict 0 陷阱、shot_plan --strict 沒有問題（C 級 0）
- 光：s01–s02 冷藍月光（接第 2 集），s03 燈籠亮起之後全是暖橘燈籠光，s31 起胡家院子是屋簷燈籠＋桌上油燈，s36–s37 靈石的淡藍光從下面打上臉

| 鏡 | 開始 | 秒 | 景別、運鏡 | 畫面 | 台詞 | 參考圖 |
| --- | --- | --- | --- | --- | --- | --- |
| **力氣，大** ||||||
| s01 | 0:00 | 1.7 | Two-shot, locked | 【開場鉤子】接第 2 集 s36：倒松旁的月光石路，陸拾在左（裂罈在背、扁擔插在繩套裡），阿猙在右高高站著，把藏在背後的鈍斧拿出來，斧背朝下對著橫在兩人之間的一截粗松木；一敲，木頭順著紋路裂成兩半 | 阿猙：力氣，大。 | a-zheng-turnaround、lu-shi-turnaround（構圖可參考第 2 集 s36 的採用首格） |
| s02 | 0:01 | 3.2 | Close-up, slow push in | 陸拾的臉在左、冷月光，瞪著畫面下方的裂木，猛抬頭看畫外右邊的阿猙、舉起一根手指要追問 | 陸拾：這叫力氣大？阿猙哥，你—— | lu-shi-portrait |
| s03 | 0:04 | 3 | Wide shot, high angle, slow push in | 【鉤子1】【奇觀】從陸拾（左）與阿猙（右）背後俯瞰坡下黑暗的山谷：三百盞燈籠同時亮起，從山腳一路連到村口，成一條暖橘色的河（無台詞） | — | lu-shi-turnaround、a-zheng-turnaround、set-changdeng-village |
| s04 | 0:07 | 2.7 | Close-up, locked | 陸拾的臉在左，暖橘燈光從下面漫上來，眼睛裡映著一點一點的燈；往坡邊踏一步 | 陸拾：三百盞燈……全亮了？ | lu-shi-portrait |
| s05 | 0:10 | 1.5 | Medium close-up, low angle, locked | 阿猙在右、仰角，燈光從下打亮額頭舊疤，看著畫外左邊的陸拾，把斧頭甩上肩 | 阿猙：等你。 | a-zheng-portrait |
| s06 | 0:12 | 1.5 | Medium shot, slow push in | 【顏值】兩排燈籠夾著往下的石階：陸拾在右快步往下走兩階，在燈籠河裡回頭（越過左肩看後面虛焦的阿猙），笑出酒窩，暖光打在曬成小麥色的臉上，馬尾髮尾被夜風吹散（併進原本 s07 的石階全景） | 陸拾：等我？ | lu-shi-portrait、a-zheng-turnaround、set-changdeng-village |
| s07 | 0:13 | 2.7 | Insert of the hand on the jacket, locked | 曬黑的手按在灰藍短打前襟、布包饅頭鼓起的那一團上，慢慢握成拳（想起自己沒選上） | 陸拾（畫外）：可我……沒選上仙門。 | 無 |
| s08 | 0:16 | 3.4 | Wide shot, locked | 村口：大老槐樹、刻紋石牌坊掛滿燈籠，底下站滿提燈的村民（虛焦）；三嬸在中間高舉燈籠擠到最前面，歸伯在左拿釣竿，團團在右拿糖葫蘆 | 三嬸：拾兒回來啦！全村等你呢！ | set-changdeng-gate、bi-sanniang-turnaround、gui-bo-turnaround、tuan-tuan-turnaround |
| s09 | 0:19 | 2.7 | Two-shot, locked | 石階腳下：阿猙在右站得高高的，陸拾在左縮在阿猙的胳膊後面；阿猙一大步往右讓開，把陸拾整個晾在燈光裡 | 陸拾：別、別喊那麼大聲…… | lu-shi-turnaround、a-zheng-turnaround、set-changdeng-gate |
| **仙門瞎了眼** ||||||
| s10 | 0:22 | 2.9 | Medium close-up, locked | 三嬸在右：紅布包頭、黑色鐵匠圍裙、腰帶上掛著鐵錘，一拐一拐往前一步，把燈籠伸向畫外左邊的陸拾 | 三嬸：躲什麼？讓三嬸瞧瞧！ | bi-sanniang-portrait、set-changdeng-gate |
| s11 | 0:25 | 2.7 | Close-up, slow push in | 陸拾的臉在左，頭垂得更低，兩手抓緊肩上的罈子背帶（鼓起勇氣要認錯） | 陸拾：三嬸，我……其實我沒—— | lu-shi-portrait |
| s12 | 0:27 | 2.7 | Medium close-up, low angle, slow push in | 【鉤子2】【爽點：face_slap】三嬸在右、仰角，濃眉一皺，空著的那隻拳頭往腰上一插 | 三嬸：仙門那是瞎了眼！ | bi-sanniang-portrait |
| s13 | 0:30 | 1.5 | Group shot, locked | 牌坊下三人：三嬸在右叉腰，歸伯在中間（斗笠蓑衣，釣竿的線末端只有一個空結、沒有鉤），團團在左靠著他的膝蓋，後面的村民虛焦；歸伯慢慢點一下頭，後面的人跟著點頭 | 歸伯：瞎了。 | bi-sanniang-turnaround、gui-bo-turnaround、tuan-tuan-turnaround、set-changdeng-gate |
| s14 | 0:32 | 2.9 | Close-up, locked | 陸拾的臉在左，一頭霧水地抬起頭看畫外右邊的三嬸，舉起一隻手掌 | 陸拾：等等……誰告訴你們的？ | lu-shi-portrait |
| s15 | 0:35 | 1.7 | Medium close-up, slow push in | 團團在右：包子頭紅繩、桃紅小襖，糖葫蘆含在嘴邊，用竹籤指著畫外左邊的陸拾 | 團團：我算的。 | tuan-tuan-portrait |
| s16 | 0:36 | 3.2 | Insert of the hand over the bun, locked | 曬黑的手一把壓住前襟的饅頭鼓包，想藏起來 | 團團（畫外）：饅頭要留給奶奶，對吧？ | 無 |
| s17 | 0:40 | 3.4 | Close-up, slow push in | 陸拾的臉在左，眼睛瞪大、臉一下紅了，兩手捂著前襟往後退半步 | 陸拾：妳、妳怎麼知道饅頭的事？ | lu-shi-portrait |
| **退貨** ||||||
| s18 | 0:43 | 3.2 | Wide shot, pan left | 【鉤子3】【轉折】從旁邊的小路看村口：孫二從右邊的黑暗晃進燈光裡，舊氈帽、扁擔挑著掛滿針線糖果的貨擔，一邊轉撥浪鼓；村民在左（虛焦） | 孫二：喲，仙門退貨的回來啦！ | s01-sun-er-portrait、set-changdeng-gate |
| s19 | 0:46 | 3.4 | Medium close-up, slow push in | 孫二在右，咧出一口白牙，身子往前探，撥浪鼓朝畫外左邊的陸拾晃 | 孫二：白吃十八年，還想當仙人？ | s01-sun-er-portrait |
| s20 | 0:50 | 2.2 | Insert of the hammer at the apron belt, locked | 黑色鐵匠圍裙的腰帶上掛著一把鐵錘，帶燙疤的手臂、袖子捲到手肘，一把把錘子抽出來 | 三嬸（畫外）：你再說一遍。 | 無（bi-sanniang-portrait 的手臂燙疤可參考） |
| s21 | 0:52 | 1 | Medium shot, locked | 【爽點：public_vindication】孫二在右、貨擔放在石板地上；鐵錘從畫面左邊砸下，落在貨擔旁一掌寬的石板上，石板裂開、貨擔跳起來（不碰到人，無台詞） | — | s01-sun-er-portrait、set-changdeng-gate |
| s22 | 0:53 | 2.5 | Close-up, locked | 孫二的臉在右，笑僵在臉上、氈帽被震歪，兩手舉到臉旁投降 | 孫二：三、三嬸，說笑的…… | s01-sun-er-portrait |
| s23 | 0:55 | 2.7 | Insert of the cracked paving stone, slow push in | 【鉤子4】石板地上一個星形裂口，就在貨擔旁、錘子砸下的地方；裂口邊緣像剛出爐的鐵一樣燒得通紅，冒起一縷細煙，紅光慢慢退成灰（三嬸的真身先不說破） | 陸拾（畫外）：石板……怎麼燒紅了？ | 無（道具插鏡；set-changdeng-gate 的石板地） |
| s24 | 0:58 | 3.4 | Medium close-up, low angle, slow push in | 三嬸在左、仰角，瞪著畫外右邊的孫二，把鐵錘扛上肩 | 三嬸：長燈村的孩子，你也敢笑？ | bi-sanniang-portrait |
| s25 | 1:01 | 1.5 | Medium close-up, locked | 歸伯在左，斗笠下的深皺紋與花白短鬍，把直立的釣竿慢慢放平，指向右邊黑漆漆的出村路 | 歸伯：送客。 | gui-bo-portrait |
| s26 | 1:03 | 3 | Wide shot, pan right | 村口：提燈拿掃帚的村民（虛焦）跟在舉錘的三嬸後面往右湧，孫二在右挑著貨擔跌跌撞撞逃出牌坊（無台詞） | — | s01-sun-er-portrait、bi-sanniang-turnaround、set-changdeng-gate |
| s27 | 1:06 | 2.5 | Close-up, slow push in | 陸拾的臉在左，眼眶濕了、嘴角發抖地笑，用袖背抹眼睛 | 陸拾：你們……都不笑我？ | lu-shi-portrait |
| s28 | 1:08 | 2.9 | Medium close-up, low angle, locked | 三嬸在右、仰角：紅布包頭、黑色鐵匠圍裙、臉頰紅潤，看著畫外左邊的陸拾，一甩手把鐵錘掛回圍裙腰帶（不再揉他的頭髮：兩人不接觸） | 三嬸：笑啥？菜都熱三回了！ | bi-sanniang-portrait、set-changdeng-gate |
| s29 | 1:11 | 3.2 | Insert of the fishing rod, locked | 【鉤子5】舊竹釣竿的竿梢背著燈光，細線垂下來、末端只有一個空結，沒有鉤；粗糙的手把竿子一提，空線甩進光裡 | 陸拾（畫外）：歸伯，您的釣竿沒有鉤？ | 無 |
| s30 | 1:14 | 2.2 | Medium close-up, locked | 歸伯在左，眼角的皺紋一擠，看著畫外右邊的陸拾，扛起釣竿轉身走進村裡 | 歸伯：魚，自己會來。 | gui-bo-portrait |
| **饅頭** ||||||
| s31 | 1:17 | 2.7 | Wide shot, slow push in | 胡家院子的夜：屋簷下掛燈籠，舊木方桌上幾碗家常菜和一盞油燈；胡奶奶坐在右邊長凳上，背挺得筆直，碗旁擱著磨亮的豆腐刀；陸拾從左邊院門跨進來，看見一桌菜愣住 | 胡奶奶：回來了？洗手，吃飯。 | set-hu-courtyard、lu-shi-turnaround、hu-nainai-turnaround |
| s32 | 1:19 | 3.2 | Close-up, slow push in | 【鉤子6】陸拾的臉在左，站在院門口，屋簷燈籠的光，盯著畫外右邊奶奶和一桌擺好的菜，慢慢往桌子走一步 | 陸拾：您怎麼知道我今晚到？ | lu-shi-portrait、set-hu-courtyard |
| s33 | 1:23 | 3.2 | Medium close-up, locked | 胡奶奶在右：銀白圓髻插木簪、深青大襟衫繫圍裙，油燈光，看著畫外左邊的陸拾，把一碗滿滿的飯推過去 | 胡奶奶：人回來就好，菜還熱著。 | hu-nainai-portrait、set-hu-courtyard |
| s34 | 1:26 | 2.9 | Insert of the bun on the table, locked | 打開的布巾上一顆圓圓的白饅頭，曬黑的手把它連布推到右邊奶奶的飯碗旁 | 陸拾（畫外）：這饅頭，我留給您的。 | 無 |
| s35 | 1:29 | 2.7 | Medium close-up, slow push in | 【鉤子7】胡奶奶在右，油燈光，兩手捧著饅頭在胸前，嘴角軟了一點；手指一捏，停住，眼神落到饅頭裡一個硬硬的東西上（掰開放到下一鏡） | 胡奶奶：傻孩子，自己不吃。 | hu-nainai-portrait |
| s36 | 1:31 | 3 | Insert of the broken bun, slow push in | 【揭曉】兩隻老手拿著掰開的饅頭，裡面透出淡藍的光；一顆發光的小靈石和一張摺起來的字條掉到桌上（無台詞） | — | 無 |
| s37 | 1:34 | 3.2 | Close-up, locked | 陸拾的臉在左，被靈石的淡藍光從下面照亮，另一側是油燈光，湊近桌子、嘴張開 | 陸拾：饅頭裡有發光的石頭？ | lu-shi-portrait |
| s38 | 1:38 | 3.4 | Insert of the slip of paper, locked | 曬黑的手把攤開的小字條舉到油燈旁，上面幾筆淡墨小到看不清；手把字條倒過來看（埋陸拾不識字） | 陸拾（畫外）：又是字……我一個都看不懂。 | 無 |
| s39 | 1:41 | 3.2 | Two-shot, locked | 隔著桌子的雙人鏡：陸拾在左探身過來，胡奶奶在右拿著剛讀完、摺好的字條，臉色一沉、嘴抿成一條硬線（併進原本 s42），油燈火苗在兩人之間；奶奶把字條舉向火苗 | 陸拾：奶奶，上面到底寫什麼？ | lu-shi-turnaround、hu-nainai-portrait、set-hu-courtyard |
| s40 | 1:44 | 3 | Insert of the lamp flame, slow push in | 【結尾懸念】油燈火苗，一隻老手捏著摺起來的字條一角懸在上面；火苗往上一舔，燒上紙角（無台詞） | — | 無 |

## 參考圖與連戲

- 參考圖都在 `_series/zero-root-yaozu/refs/`（`docs/videos/series-plans/zero-root-yaozu/production/refs.json`）。**這批定妝照、三視圖與場景圖都是真人劇照質感**；3D 國漫版要不要先重畫一套 3D 參考，等站主決定（見 brief.md）。在那之前參考圖只拿來定臉、髮型、服裝與擺設，不拿來定質感。胡奶奶的定妝照用 t1；孫二只有定妝照、沒有三視圖：s26 他在全景裡逃跑，首格不像就先畫一張他挑貨擔的全身當連戲參考。
- 三張場景圖都是黃昏或傍晚的光，本集全在夜裡：set-changdeng-gate、set-changdeng-village、set-hu-courtyard 只當空間與擺設的參考，光照 prompt 寫的燈籠與油燈重打。set-hu-courtyard 雞舍前的裂紋陶盆是第 4 集的聚靈盆，s31 入鏡就讓它留在角落，不要畫掉。
- s01 接第 2 集 s36：阿猙藏在背後的斧頭在 s01 拿出來，斧頭的樣子（長柄、舊鐵、鈍口）抄第 2 集 s29 的採用首格；陸拾的扁擔插回罈子繩套。原本 s02 裂木滾開的插鏡刪掉：s01 的動作已經把木頭劈開。
- 道具帳：鈍斧（s01、s05、s06）；三嬸的鐵錘先掛在圍裙腰帶上（s08、s10、s12、s13），s20 抽出、s21 砸地、s23 石板燒紅、s24 扛上肩、s26 舉著、s28 掛回去；歸伯的釣竿線末端只有空結（s08、s13、s25、s29、s30）；團團的糖葫蘆（s08、s13、s15）；饅頭在陸拾前襟（s07、s16、s17）→ s34 放上桌 → s35 掰開 → s36 掉出靈石與字條；字條上的墨跡永遠看不清（`no_text` 會扣分，要讀的字之後另外合成）。
- 人群：村口的村民一律寫成虛焦背景，不列角色、不給臉；每鏡列的角色不超過三個（s08、s13 是三人同框的全景，shot_plan 標 B 風險 crowd／cast.three，留著當重新交代空間的鏡頭）。
- 不接觸：三嬸不再揉陸拾的頭髮（s28 改成她把錘子掛回腰帶），錘子只碰石板不碰人（s21），孫二逃跑時村民只在虛焦背景追（s26）。
- 軸線：坡上陸拾在左、阿猙在右（s01–s05、s09）；村口對話陸拾在左、村民（三嬸、團團）在右（s10–s17、s27、s28）；孫二從右邊的路進來，與三嬸、歸伯（左）對峙（s18–s26），所以 s24、s25 的三嬸與歸伯換到左邊；院子裡陸拾在左、奶奶在右（s31–s40）。
- s03 從背後拍陸拾與阿猙，臉看不到：identity 題可能被扣，被扣就改成只把他們寫成畫面下緣的背影、`characters` 留空。
- 提示詞裡陸拾寫作 Lushi（第 1、2 集寫 Lu Shi）；新角色的 id 取成提示詞裡讀得到的一個字：Grandma Hu → grandma、Third Aunt → aunt、Old Gui → gui、Tuantuan → tuantuan、Sun Er → sun。
- 刪掉的鏡（舊編號）：s02 裂木滾開、s07 石階全景（併進 s06）、s21 陸拾轉開臉、s29 團團喊「下回糖要算便宜點！」、s35 罈子放上桌「醃菜……只剩半罈了」、s42 奶奶摺字條「奶奶？」；新增 s23 石板燒紅、s32「您怎麼知道我今晚到？」。
- shot_plan 的槓桿列了四個可以切素材的同鏡位（s24←s12、s27←s17、s28←s05、s30←s25），每一對的表情與動作都不同，本集不切。
