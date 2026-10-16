# 第 1 集〈問天石，零〉分鏡表

<!-- 給人讀的中文版；製作用的英文提示詞在 video.json。 -->

- 2026-10-16 改版：3D 國漫（國漫 CG）重拍版、一集七個片中鉤子（站主：「一集應該要兩三個鉤子以上」）。38 個鏡頭、四段（問天石／天才／醃菜罈／霧路），估計約 92 秒（shot_plan 估法；lint 估 91 秒；細綱 95 秒）
- 鉤子：【開場鉤子】0:00 手拍黑石、全黑＋「零——。」；【鉤子1】0:17 滿場哄笑只有雲知意不笑；【鉤子2】0:27–0:31 金紅光柱後嚴少淵「什麼味道？」；【鉤子3】0:45 嚴崇念珠停住「零靈根……哪來這把力氣？」；【鉤子4】0:55–0:57 醃菜被踢翻、陸拾握拳，嚴少淵把劍頂出一指「零靈根想動手？」；【鉤子5】1:00 雲知意擋在中間；【鉤子6】1:20「回家再打開。別讓人看見。」；【鉤子7】1:26 沒風的樹枝自己晃；【結尾懸念】1:30 倒掛猴臉「嘻。」。最長一段沒有鉤子的空檔約 17 秒（1:03–1:20）
- 爽點：前半 hidden_power（兩個執事拽不動他，0:42）；結尾 rescue（雲知意擋下、撿菜、塞饅頭）
- 每一鏡都買 4 s 片段（海螺 H3 2K，12 點／秒，48 點）＋一張首格（約 23 點）：片段一次 1,824 點、期望 2,534、上限 3,648；首格 38 張約 874 點；一次合計約 2,698 點
- 檢查：lint 0 錯誤、30 項結構檢查全過、分鏡讀取 --strict 0 陷阱、shot_plan --strict 沒有問題（C 級 0）
- 光：問天台是清晨冷光（s01–s30），山門與霧路是黃昏的灰藍霧（s31–s38）；3D 國漫的冷灰藍底色、暖色只留給金紅光柱

| 鏡 | 開始 | 秒 | 景別、運鏡 | 畫面 | 台詞 | 參考圖 |
| --- | --- | --- | --- | --- | --- | --- |
| **問天石** ||||||
| s01 | 0:00 | 1.3 | Insert of the hand on the stone, high angle, slow push in | 【開場鉤子】手掌拍上問天台中央一人高的黑色問天石，石頭一點光都沒有（不先拍全景，第一格就是手與黑石） | 嚴崇（畫外）：零——。 | set-wentian-terrace（石頭與白玉台） |
| s02 | 0:01 | 2.7 | Wide shot, high angle, locked | 問天台全景：雲海上的白玉圓台，陸拾背著醃菜罈孤零零站在黑石左邊；右邊前排的圓臉外門弟子指著他笑彎了腰，四周一圈弟子虛焦哄笑 | 外門弟子：零靈根也敢上山？ | set-wentian-terrace、lu-shi-turnaround |
| s03 | 0:04 | 2.7 | Medium close-up, locked | 陸拾在左、右手還按在石上，左手抓抓後腦，尷尬陪笑 | 陸拾：再、再按一次行嗎？ | lu-shi-portrait |
| s04 | 0:06 | 2.7 | Medium close-up, low angle, locked | 嚴崇坐在右邊高台上，仰角，拇指撥過一顆黑玉念珠 | 嚴崇：問天石，從不說謊。 | yan-chong-portrait |
| s05 | 0:09 | 2.5 | Close-up, slow push in | 陸拾在左，雙掌拍上石頭、整個人壓上去 | 陸拾：亮啊……給我亮啊！ | lu-shi-portrait |
| s06 | 0:11 | 2.5 | Insert of the two hands on the stone, locked | 兩隻手按在黑石上，指節發白，石頭仍是暗的；手慢慢滑下 | 外門弟子（畫外）：一點光都沒有！ | 無（手部插鏡） |
| s07 | 0:14 | 2.9 | Close-up, slow push in | 陸拾在左，低頭把額頭抵在冰冷的黑石上，四周還在笑（交代他上山的理由） | 陸拾：說好要寄錢回家的…… | lu-shi-portrait |
| s08 | 0:17 | 2 | Medium shot, slow push in | 【鉤子1】雲知意在右，四周的弟子虛焦哄笑，只有她不笑；她從隊伍裡往前走出一步停住，眼睛盯著畫外左邊的陸拾（無台詞） | — | yun-zhiyi-portrait、set-wentian-terrace |
| s09 | 0:19 | 2.5 | Medium close-up, low angle, locked | 嚴崇在右邊高台上，懶懶揮手像趕蒼蠅 | 嚴崇：零靈根，下一個。 | yan-chong-portrait |
| **天才** ||||||
| s10 | 0:21 | 2.7 | Wide shot, locked | 從人群背後拍：弟子讓出一條路，嚴少淵穿深紫金邊袍走上右邊的白玉階，陸拾小小一個站在左邊石旁 | 嚴崇（畫外）：少淵，讓他開開眼。 | yan-shaoyuan-turnaround、lu-shi-turnaround、set-wentian-terrace |
| s11 | 0:24 | 1.5 | Medium shot, slow push in | 嚴少淵在右，看都不看直直走過來，左邊的陸拾踉蹌退開讓路（兩人不接觸） | 嚴少淵：讓開。 | yan-shaoyuan-turnaround、lu-shi-turnaround |
| s12 | 0:26 | 1.5 | Insert of the pale hand on the stone, slow push in | 一隻戴玉戒、深紫金邊袖口的白皙手碰到石頭，金紅兩色光從黑石裡湧出 | 外門弟子（畫外）：雙色！ | 無（手部插鏡；yan-shaoyuan-turnaround 的袖口與玉戒） |
| s13 | 0:27 | 2.9 | Wide shot, low angle, tilt up | 【奇觀】仰角往上搖：金紅雙色光柱衝上雲層，滿地弟子的影子被照成金紅兩色，陸拾在左邊畫緣 | 嚴崇（畫外）：金紅雙色，百年一見！ | set-wentian-terrace、yan-shaoyuan-turnaround、lu-shi-turnaround |
| s14 | 0:30 | 1 | Close-up, locked | 陸拾的臉在左，被光柱照成金紅，退一步、抓緊背上醃菜罈的帶子（無台詞） | — | lu-shi-portrait |
| s15 | 0:31 | 2 | Medium close-up, locked | 【鉤子2】嚴少淵在右，從石頭轉過頭，皺著鼻子朝陸拾的罈子嗅了嗅 | 嚴少淵：什麼味道？ | yan-shaoyuan-portrait |
| s16 | 0:33 | 3.2 | Over-the-shoulder from behind Yan Shaoyuan on Lu Shi, locked | 過肩鏡：從嚴少淵背後（右邊畫緣是他的玉冠與紫袍肩頭），陸拾在左把罈子從背上甩到胸前抱緊 | 陸拾：我奶奶醃的菜，拜師禮。 | lu-shi-portrait、yan-shaoyuan-turnaround |
| s17 | 0:36 | 3.4 | Medium close-up, locked | 嚴少淵在右，抬下巴冷笑，往罈子甩一下袖子像撣灰 | 嚴少淵：鄉下醃菜，也配上問天台？ | yan-shaoyuan-portrait |
| **醃菜罈** ||||||
| s18 | 0:40 | 2.5 | Medium close-up, low angle, locked | 嚴崇在右邊高台上，伸兩根手指叫執事 | 嚴崇：來人，請他下山。 | yan-chong-portrait |
| s19 | 0:42 | 3 | Wide shot, locked | 【爽點】問天台全景：陸拾在中間抱著罈子，兩個褐袍執事一左一右拽罈子的繩耳；他肩膀一抖，兩人都踉蹌後退一步，他紋絲不動（執事只碰罈子的繩，不碰人）（無台詞） | — | lu-shi-turnaround、set-wentian-terrace |
| s20 | 0:45 | 3.2 | Close-up, slow push in | 【鉤子3】嚴崇在右，念珠停在指間，一邊眉毛挑起、身子前傾，眼神瞇起來盯著畫外左邊的陸拾 | 嚴崇：零靈根……哪來這把力氣？ | yan-chong-portrait |
| s21 | 0:48 | 3.4 | Medium close-up, locked | 陸拾在左抱著罈子，平靜又有點倔，把罈子抱高、轉身要往石階走 | 陸拾：挑了十年水。我自己會走。 | lu-shi-portrait |
| s22 | 0:52 | 2.9 | Insert of the boot and the jar, low angle, locked | 地面高度：深紫袍角下的黑靴一腳把罈子踢出手，罈子在白玉地上裂開、醃菜灑一地（不拍任何人受傷） | 嚴少淵（畫外）：那就帶著你的菜滾。 | 無（道具插鏡；yan-shaoyuan-turnaround 的靴與袍角） |
| s23 | 0:55 | 2.9 | Close-up, slow push in | 陸拾的臉在左，低頭看著一地的菜，臉僵住，右手在身側握成拳、慢慢抬眼 | 陸拾：奶奶醃了三個月的…… | lu-shi-portrait |
| s24 | 0:57 | 2.9 | Medium close-up, low angle, locked | 【鉤子4】嚴少淵在右、仰角，左手搭在腰間黑鞘長劍上，拇指把劍鍔頂出鞘一指寬就停，冷笑等他出手 | 嚴少淵：怎麼？零靈根想動手？ | yan-shaoyuan-portrait |
| s25 | 1:00 | 2 | Wide shot, slow push in | 【鉤子5】問天台全景：雲知意穿月白長袍從右邊走進來，背對陸拾擋在兩人中間，蹲下把菜撿回裂罈裡 | 雲知意：師兄，夠了。 | yun-zhiyi-turnaround、lu-shi-turnaround、set-wentian-terrace |
| s26 | 1:02 | 3.2 | Medium close-up, locked | 嚴少淵在右，低頭看畫外左邊的雲知意，冷笑收起，手離開劍、劍「喀」一聲落回鞘裡，退一步 | 嚴少淵：知意，妳替零靈根說話？ | yan-shaoyuan-portrait |
| s27 | 1:06 | 2 | Close-up, slow push in | 【顏值】雲知意跪在左邊，白玉簪被晨光照亮，雙手捧起裂罈，抬眼看畫外右邊的陸拾（慢推） | 雲知意：菜還能吃。 | yun-zhiyi-portrait |
| s28 | 1:08 | 2 | Two-shot, locked | 雙人鏡：雲知意在右起身，把裂罈放在左邊陸拾腳前的白玉地上，退一步（兩人不接觸）（無台詞） | — | yun-zhiyi-turnaround、lu-shi-turnaround |
| s29 | 1:10 | 2 | Close-up, locked | 陸拾的臉在左，耳朵紅了，抱著裂罈匆匆低頭道謝 | 陸拾：謝、謝謝妳。 | lu-shi-portrait |
| s30 | 1:12 | 1.7 | Medium close-up, locked | 雲知意在右，背後是虛焦的嚴少淵；她把臉從陸拾身上轉開、望向石階 | 雲知意：下山吧。 | yun-zhiyi-portrait |
| **霧路** ||||||
| s31 | 1:13 | 2 | Wide shot, locked | 黃昏，巨大的石砌山門，石階往下沒入霧和松林；陸拾背著裂罈（罈子繩套裡插著一根短竹扁擔，接第 2 集）獨自走出去（無台詞） | — | lu-shi-turnaround |
| s32 | 1:15 | 2.7 | Two-shot, slow push in | 山門下的霧中石階：雲知意在右高一階，往下一步，把布包的饅頭伸長手臂遞向左邊回頭的陸拾 | 雲知意：拿著，別在這裡吃。 | yun-zhiyi-turnaround、lu-shi-turnaround |
| s33 | 1:18 | 2.5 | Close-up, locked | 陸拾的臉在左，黃昏霧裡把饅頭抱在胸前，抬眼看她 | 陸拾：妳……為什麼幫我？ | lu-shi-portrait |
| s34 | 1:20 | 3.4 | Medium close-up, locked | 【鉤子6】雲知意在右，半轉身朝山門，回頭看一眼畫外左邊的陸拾，轉身走回霧裡 | 雲知意：回家再打開。別讓人看見。 | yun-zhiyi-portrait |
| s35 | 1:24 | 2.2 | Insert of the bun in the hands, locked | 一雙曬黑的手把布包的饅頭收進灰藍短打的前襟 | 陸拾（畫外）：留給奶奶吃。 | 無（手部插鏡） |
| s36 | 1:26 | 2 | Wide shot, high angle, locked | 【鉤子7】從松樹高處往下拍：霧中窄窄的石路，陸拾小小地走在彎曲的樹枝下；他頭頂一根長樹枝沒有風卻自己晃了起來（無台詞） | — | lu-shi-turnaround |
| s37 | 1:28 | 2 | Medium close-up, slow push in | 陸拾在左，背著裂罈與扁擔，停步抬頭看樹枝 | 陸拾：沒風啊……誰？ | lu-shi-portrait |
| s38 | 1:30 | 2.1 | Extreme close-up, locked | 【結尾懸念】一張灰毛猴臉倒掛下來，停在陸拾鼻尖前一寸，咧嘴笑（第 2 集 s01 從這一格接下去） | 山魈：嘻。 | lu-shi-portrait、shanxiao-design |

## 參考圖與連戲

- 參考圖都在 `_series/zero-root-yaozu/refs/`（`docs/videos/series-plans/zero-root-yaozu/production/refs.json`）。**這批定妝照、三視圖與場景圖都是真人劇照質感**；3D 國漫版要不要先重畫一套 3D 角色參考，等站主決定（見 brief.md）。在那之前，參考圖只拿來定臉、髮型、服裝與擺設，不拿來定質感。
- 外門弟子（dizi）沒有參考圖：s02 的首格定下他的臉（圓臉、白袍淡藍腰帶），之後只在畫外說話。
- 道具帳：醃菜罈在背上（s02–s15）→ s16 抱到胸前 → s19 執事拽它的繩耳 → s22 被踢裂 → s25 雲知意撿菜 → s28 放到他腳前 → s31 起裂罈綁回背上、繩套裡插著短竹扁擔（第 2 集 s02 從繩套裡抽出來）；饅頭 s32 遞出、s35 收進前襟（第 2 集 s07、第 3 集 s07／s16 都摸著這一團）。
- 不接觸：嚴少淵不再用肩膀撞陸拾（s11 陸拾自己退開），執事只拽罈子的繩耳（s19），罈子與饅頭都是放下或遞出、不手碰手（s28、s32）。
- 軸線：問天台上陸拾在左，嚴崇、嚴少淵、雲知意在右；霧路上雲知意在右（高一階），陸拾在左。
- 提示詞裡陸拾照第 1 集原本的寫法 Lu Shi（第 3 集起寫 Lushi）。
- shot_plan 的槓桿列了四個可以切素材的同鏡位（s09←s04、s17←s15、s18←s04、s29←s14），動作都不同，本集不切。
