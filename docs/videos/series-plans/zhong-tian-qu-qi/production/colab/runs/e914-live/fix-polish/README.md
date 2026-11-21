# 第 14 集真人版 fix-polish：上架前精修重拍（2026-11-21）

依 `/root/mokaair-work/review-zt/RETAKE-BRIEF.md`。審片：`review-zt/reports/e014.txt`、`consolidated/retakes.json`（e014 tier A、B 共六鏡：s40、s42 嚴重；s11、s13、s03、s37 中等）。
種子 9149101、9149102，960×544 Ref2VA。只寫了提示詞與 spec，沒有送出任何工作。tier C（s12、s27／s30／s32／s33 竹簾、s20、s01、s41）不在這批。

base：`picks.json` 沒有 `motion_from` 欄，六鏡的 `draft` 都在 `d1/out/`，所以 base 是 `d1/prompts/ref-sNN-<選中的種子>.txt`
（d1 兩個種子的提示詞逐位元相同，已 cmp）。

| 鏡 | tier | 審片問題 | base | 改了哪些句子（舊→新） | 換圖 | 拿不準的 |
| --- | --- | --- | --- | --- | --- | --- |
| s40 | A（嚴重） | 唐小棠背影站定、平舉紙；許硯 4 秒每格都在笑；前一鏡 s39 的秦霜、阿令與許硯手上的白紙全部憑空消失 | `d1/prompts/ref-s40-9141102.txt`，6 秒 | ① 加秦霜、阿令的外貌錨句（照 s03、s39 base 原句）。② 光：`low golden evening sunlight slanting straight in…` → `low golden evening sun raking in from the right opening, deep amber light low across the floor and the faces`（審片 note 要的傍晚光）。③ 唐小棠：`two looped buns` → `two round buns shaken half loose from running`，緞帶垂到背上；`has just stumbled in … stops short … one hand on the post` → 第一格就是衝勢未停、身體前傾，左手攥著揉皺的紙舉在肩高（紙背空白朝鏡頭）。④ 許硯：`the white sheet still raised beside his face` 改成寫死「自己那張書頁大、霧面、全空白的白紙兩手舉在臉旁肩高」；表情 `startled: brows jumping up, his smile gone` → 先是展示紙的暖、亮眼，再「眉一跳、往中間皺，眼睛睜大盯著她，嘴收成一條緊線，下顎繃」（整份沒有 smile 字）。⑤ 新增中景：許硯右邊退一步、比他小一點略虛焦，秦霜（空手垂身側）與阿令（左手陶水壺，接 s38、s39）並肩，臉朝畫右看她：秦霜眉壓低、下顎繃，阿令瞇眼、抿嘴。⑥ `exactly two people` → `exactly four people, each appearing exactly once`，點名三人、唐小棠照舊只寫背影不點名。⑦ 動作：原本「右手撐柱、再把紙往前一舉」兩拍 → 只留一拍：最後半步踉蹌、右掌拍上木柱撐住、肩起伏，紙一直舉著；許硯在拍柱那一下眉一跳、白紙仍舉著；秦霜、阿令站著不動盯著她。⑧ 不說話句擴成三個人都閉嘴 | 拿掉 `xuyan-angle-b-l1`；加 `qinshuang-portrait-l1`、`aling-portrait-l1`（共 5 張：許硯定妝＋角度 a、秦霜、阿令、`set-gongpeng-l2`） | 畫面四個人（三張臉＋不點名的背影），preflight 只算點名的三人所以沒報 `four`，但 Colab 仍可能多畫一個人或把秦霜畫兩次；兩支都分身就退回只留阿令、秦霜出畫。「把紙往前一舉」改成第一格就舉著，衝進來的力道只靠前傾與拍柱；拍柱可能拍得很輕。秦霜、阿令的位置照 s39（阿令在許硯右邊），不是稿子寫的「開口內」——開口在畫右、鏡頭背後那側，照稿子放會被唐小棠的背擋住或出畫。光仍受 `set-gongpeng-l2`（午後亮光）影響，可能還是偏白天，剪接 grades 仍要試傍晚調色 |
| s42 | A（嚴重） | 開頭 0–0.5 秒許硯的手捏著告示一角，像他遞給她；之後只有兩人，沒有人對告示有反應 | `d1/prompts/ref-s42-9141102.txt`，6 秒 | ① 加秦霜、阿令錨句、同 s40 的光句。② 唐小棠的紙：`up at chest height in both hands toward the young man` → 從第一格就兩手舉著、半臂遠、在她左肩旁（畫左）露出來，轉向他、紙背空白朝鏡頭，手指捏皺紙邊。③ 許硯：`the white sheet in his hands`（d1 被畫成他的手捏著她的紙）→ 第一格自己的白紙就垂在左手、貼大腿，右臂直垂身側，「他的手與她的紙之間一直隔著一步空地與斜光」；表情 `stricken` 保留並補「眼睛盯著她的紙、嘴抿成一條線」。④ 中景加秦霜、阿令（位置句與 s40 一字不差），臉朝她的紙，秦霜眉壓低、阿令瞇眼抿嘴。⑤ 動作：拿掉「許硯慢慢把白紙放低」（放低的手正是 d1 碰到她紙的那隻），只留她捏紙、紙發抖；許硯站著不動、眉再皺緊；秦霜、阿令不動盯著紙 | 同 s40（5 張） | 同 s40 的四人風險。稿子 c42 的「前景是許硯手上那張白紙（對光看得到柳葉）」與「她對著自己唸」沒拍（真人版定案：紙背朝鏡頭、從她背後拍）。`turned toward him so he can read it` 可能讓模型想畫正面，但正面朝許硯、鏡頭看不到 |
| s11 | B | 「我是從很遠很遠的地方來的」整句露牙大笑、像講笑話 | `d1/prompts/ref-s11-9141102.txt`，6 秒 | ① 表情：`caught by his own mouth: brows up, lips moving…, then eyes flying wide` → 脫口而出的空白錯愕：眉高而不動、眼睜大盯著她、嘴角平而微往下、臉頰不動、嘴照常對字。② 台詞後補 `in a flat, even voice, as if the words come out of him by themselves`。③ 動作：`opens his mouth as if to laugh it off, but the words come out first; afterwards his eyes go wide and he swallows`（laugh 一字就讓他笑）→ 只有一拍：最後一個字出口嘴一閉成一條緊線、用力吞一下（喉嚨動一次）。④ 尾句 `the brows stay drawn`（跟眉高矛盾）→ 嘴維持那條線、眼睛維持睜大到最後一格 | 無 | 審片改寫句的「先尷尬半笑再空白」沒照寫：半笑會被拉成整鏡笑（d1 正是這樣），所以「想打哈哈」只留在聲音的平直與表情的錯愕裡 |
| s13 | B | 「遠到騎馬走不到……我自己也回不去了」整鏡溫暖的笑；背景多一盞大燈籠、掛著葫蘆，跟 s10／s11／s14 不是同一段牆 | `d1/prompts/ref-s13-9141101.txt`，6 秒 | ① 拿掉兩處 `faint closed-lipped smile`（d1 兩個種子都照笑整鏡）；表情改成疲憊空洞的臉：眉放鬆、眼皮沉、眼神空、嘴角平而微垂、輕聲對字。② 背景 `behind him only the cracked earthen wall` → 跟 s11 同一句 `…and one small candle flame in an iron holder`。③ 動作：`gives a faint closed-lipped smile that drains away …; his eyes drift past her …; the smile does not come back` → 只留一拍：說話時視線慢慢越過她的肩，飄到畫右走廊暗的那一端並停住；說完嘴合成平軟的一條線，眼神空空停在暗處 | 無 | 稿子 c13 與 RULES 寫「嘴閉著笑一下馬上收掉」，這版**完全不笑**（偏離稿子，理由：寫了笑就收不掉）；站主若要那一下笑，只能剪接時接受 d1 開頭或另抽。燈籠、葫蘆來自場景圖 `set-xujia-zoulang-l1` 的牆面，背景句只能減少機率 |
| s03 | B | 臉朝畫左、眼睛卻斜看畫右；刀是細長帶彎尖的刀，跟 s01 不是同一把 | `d1/prompts/ref-s03-9141102.txt`，6 秒 | ① 視線：`her face three-quarter to screen left toward the young man off screen left` → 臉四分之三側朝畫左、鼻尖朝畫左、眼珠也轉到朝畫左的眼角、順著刀身看他。② 刀：`a dark iron blade two fingers wide and only a little longer than a palm, a thick blunt back and a nicked cutting edge` → 小長方形鐵刃、兩指寬、只比手掌長一點、**方平的刀頭**、直而厚的刀背、直而有缺口的刃、整把比前臂短，胸口高平舉；`its edge pointing` → `its square tip pointing`。③ 動作：`sinks one finger's width, her eyes waver once, then the knife lifts back level` → 刀沉一指寬，眼神往下閃一次、立刻回到他臉上變硬、下顎再繃（拿掉刀再抬回去那一拍） | 無 | 刀頭寫成方的會更接近 s01 的方頭寬刃，但 s01 那把本身偏大（tier C，未重拍）；這把小刀跟 s01 仍可能不完全一樣。墳仍是 `set-zhulin-fen-l3` 的鱗片土丘（s01、s09 同圖不重拍，換圖反而本集內不一致） |
| s37 | B | 石木匠摸的是吊在木桿上垂下的大白布，不是許硯那張一尺見方的紙；畫面沒有柳葉 | `d1/prompts/ref-s37-9141102.txt`，8 秒 | ① `the edge of the white sheet reaches into the frame from the left, held by hands off screen`（d1 長成桿上的布）刪掉，構圖改寫死：畫左近前景一張書頁大、薄、霧面、挺的小方白紙，由一雙藍灰袖（布條綁起）的年輕男人的手從畫左邊進來捏著遠端兩角，舉在他臉的高度，只入鏡手與前臂；夕光透過紙，紙心一片淡而細長的柳葉形比較亮，其餘空白；透紙的暖光落在他臉上。② `He is the only person in the frame` → 只有他一張臉，另外只有畫左那雙手與前臂（照 s39 的寫法）。③ 動作：`reaches out a thick finger and thumb and rubs its edge…, then slowly shakes his head`（兩拍）→ 他用粗拇指與食指捏住同一張紙的近端右緣、邊說邊慢慢搓，眼睛看紙中間的柳葉，那雙手仍捏著遠端兩角（拿掉搖頭）。④ 尾句 `lips press flat and the jaw sets, the brows stay drawn` → 嘴抿起來微微發抖、眼睛仍含淚看著紙 | 無（考慮過加 `prop-liuye-zhi-xin-l1`，沒加：那張是整面紙＋描線葉脈＋兩束纖維線，會把近景拉成整張紙的插鏡，柳葉樣子也跟 s36 透光的亮葉形不同；s36 只靠文字就畫出柳葉） | 「手伸向對方會變牽手」：他的手與許硯的手都在同一張紙上，可能碰在一起；寫了兩人各捏紙的兩端。光從他身後的開口來、紙在他面前，「透紙的光照在他臉上」物理上不完全對，靠模型取捨 |

## 總草稿

6 鏡 × 2 種子 = 12 支，76 秒（s40、s42、s11、s13、s03 各 6 秒，s37 8 秒，都照 base；沒有加長）。

## 檢查（2026-11-21）

```bash
cd /home/user/zt-work/docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs
python3 -I _scripts/polish-build.py 14          # e914: 6 shots, 12 drafts, 76 s
python3 -I _scripts/preflight-prompts.py /root/mokaair-work/videos/zhong-tian-qu-qi-e914-dh/runpod/live/fixp/colab-jobs.json   # 0 error(s), 0 warning(s)
cd /home/user/zt-work && bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh check --manifest /root/mokaair-work/videos/zhong-tian-qu-qi-e914-dh/runpod/live/fixp/colab-jobs.json   # 0 error(s), 0 warning(s)
```

另外掃過六份提示詞：沒有 smile／laugh／grin／teeth／notice／letter；`never the mood. ` 與 `One continuous shot.` 各一次。

## 挑片時要看

- s40／s42：秦霜、阿令有沒有在、有沒有分身或多一個人；許硯手上那張白紙在不在（s40 舉在臉旁、s42 垂在左腿邊）；s42 第一格許硯的手有沒有碰到唐小棠的紙；許硯有沒有笑；唐小棠的頭有沒有轉；三張臉的嘴是否全閉（兩鏡都是錄音）；光是不是傍晚金色。
- s40 接 s41：s41（未重拍）開頭許硯白紙在臉旁、表情已收，所以 s40 結尾許硯應該已不笑、紙還舉著。
- s11、s13：整鏡有沒有笑；s13 背景還有沒有大燈籠與葫蘆。
- s03：眼睛是不是看畫左；刀是不是方頭短刃。
- s37：紙是不是一張小方紙（不是布）、看不看得到柳葉、兩人的手有沒有握在一起。
