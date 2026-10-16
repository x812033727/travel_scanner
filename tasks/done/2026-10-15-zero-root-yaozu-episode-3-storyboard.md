---
id: 2026-10-15-zero-root-yaozu-episode-3-storyboard
title: Zero-root Yaozu episode 3 storyboard
status: done
priority: P2
area: docs
owner: claude-opus-yaozu-e003
claimed_at: 2026-10-15T14:43:42Z
created_at: 2026-10-15T14:43:35Z
completed_at: 2026-10-15T14:52:36Z
branch:
depends_on: []
scope:
  - docs/videos/zero-root-yaozu-e003
---

# Zero-root Yaozu episode 3 storyboard

## Why

第 2 集分鏡寫完之後，接著寫第 3 集〈一村人等門〉的分鏡劇本：付任何首格或影片點數之前要先定。開頭要接住第 2 集最後一格（月光松林路、倒下的大松旁，阿猙剛把沒有刃的斧頭藏到背後說「剛好。」）。

## Definition of done

- [x] `docs/videos/zero-root-yaozu-e003/video.json`：44 鏡、約 107 秒（lint 估法）、lint 0 錯誤、drama_craft_check 30 項全過、shot_reading --strict 0 陷阱、shot_plan --strict 沒有問題、validate.mjs ok。
- [x] `brief.md`、`script.md`（工具產生）與給人讀的 `storyboard.md`（含每鏡的參考圖）。

## Steps

- [x] 照 season-01.json 第 3 集的 hook、mid_hook、turn、satisfaction、cliffhanger、spectacle、glamour_shot 排五段（力氣，大／燈河／仙門瞎了眼／退貨／饅頭）。
- [x] 角色沿用第 2 集的 lushi、azheng；新增 grandma（胡奶奶，Gacrux）、aunt（三嬸，Pulcherrima）、gui（歸伯，Enceladus）、tuantuan（團團，Leda）、sun（孫二，Zubenelgenubi），外觀照 setting.json／season-01.json 的 guest_cast 譯成英文。
- [x] 跑六個檢查並改到全過。

## How to verify

```bash
node tools/video/cli.mjs lint --file docs/videos/zero-root-yaozu-e003/video.json
node .agents/skills/youtube-video/scripts/drama_craft_check.mjs docs/videos/zero-root-yaozu-e003/video.json
node .agents/skills/animation-camera/scripts/shot_reading.mjs docs/videos/zero-root-yaozu-e003/video.json --route hailuo --strict
node .agents/skills/animation-preproduction/scripts/shot_plan.mjs docs/videos/zero-root-yaozu-e003/video.json --route hailuo --resolution 2k --strict
node tools/video/cli.mjs script --slug zero-root-yaozu-e003
node docs/videos/series-plans/zero-root-yaozu/validate.mjs
```

## Notes

- 估計 107 秒（lint 估法），細綱寫 115 秒；真人語速通常再長一成。台詞 id 是 e3a01–e3a36，跟 e1aNN、e2aNN 不撞。
- shot_plan（Hailuo H3 2K）：44 支都買 4 s；片段一次 2,112 點、期望 2,909、上限 4,224；風險 A 18、B 26、C 0（B 多半是說話的臉 speech.visible-mouth，另有 crowd、cast.three、action.fast）；小樣建議 s24–s26（錘子砸地、孫二投降、三嬸扛錘）。
- 為了不買 5 s，五句台詞縮短到估計 ≤ 3.5 s（4 s 減 0.5 s 尾巴把手）：s03、s22、s26、s31、s32。
- pace.spread 一度 1.8（< 2）：s02 改成 1 s 動作、s15 歸伯那句縮成「瞎了。」之後是 2.1。
- 名字比對：`shot_reading` 的 `nameOf` 只拿角色的 id 與中文名比對。「Lu Shi」讀不到 lushi（第 1、2 集都是這樣，畫外子句的對象讀成「某個人」而不是 lushi），本集提示詞改寫成 Lushi；新角色的 id 取成提示詞裡讀得到的那個英文字：Grandma Hu → grandma、Third Aunt → aunt、Old Gui → gui、Sun Er → sun。用 `offScreenRoles` 逐句驗過，全部讀回正確的 id。之後幾集沿用這幾個 id 與寫法。
- 孫二在 setting.json 沒有聲音；本集代理暫定 gemini:Zubenelgenubi，沒有試聽，等站主確認。
- 細綱的中段鉤子是「還沒開口說落選，三嬸就說仙門瞎了眼」：s13 的台詞寫成話沒說完（「三嬸，我……其實我沒——」），否則下一句「誰告訴你們的？」接不上。
- 中段鉤子估計落在 0:30–0:39（片長的三成左右），比細綱說的「一半左右」早；轉折與 public_vindication 在 0:44–1:07，正好在中段。
- 下一步：開拍鎖定（shot_plan／plan_lock）、首格（s01 用第 2 集 s36 的採用首格當構圖參考）、海螺影片、配音。

## 2026-10-16 鉤子＋3D 國漫改版

站主 2026-10-16：「一集應該要兩三個鉤子以上」，而且從第 1 集起改拍 3D 國漫（國漫 CG）。

- `look` 換成 3D 國漫（同第 1 集）；角色 id、外觀與聲音不動。
- 44 鏡刪成 40 鏡（一集上限），約 108 秒（shot_plan；lint 107 秒；細綱 115 秒，在 ±10 秒內），鏡號與台詞 id 從頭重編（s01–s40、e3a01–e3a35）。刪掉（舊號）：s02 裂木滾開、s07 石階全景（併進新 s06）、s21 陸拾轉開臉、s29 團團喊糖要便宜、s35 罈子放上桌、s42 奶奶摺字條（「臉色變了」併進新 s39 的 prompt）；新增 s23 石板燒紅、s32「您怎麼知道我今晚到？」。章節「燈河」不到 10 秒，併進「力氣，大」。全部買 4 s：片段一次 1,920 點、期望 2,664、上限 3,840；首格 40 張約 920 點；一次約 2,840 點。風險 A 15、B 25、C 0。
- 鉤子：0:04–0:10 三百盞燈打斷追問＋「等你。」／0:28–0:36「仙門那是瞎了眼！」「我算的。」／0:43 孫二「仙門退貨的回來啦！」／0:55 石板燒紅冒煙（season-01.json 第 3 集 hooks 也寫了「青石板一下子燒得通紅」）／1:11 沒有鉤的釣竿／1:17–1:19 奶奶不答怎麼知道他今晚到／1:29–1:31 奶奶一捏饅頭停住、掰開掉出靈石與字條；結尾 1:44 火苗舔上紙角。最長空檔約 18 秒。
- 改的台詞：「這哪是力氣大？阿猙哥，你——」→「這叫力氣大？阿猙哥，你——」；「三百盞……全亮了？」→「三百盞燈……全亮了？」；「是……在等我？」→「等我？」；「可我……沒選上。」→「可我……沒選上仙門。」；「拾兒回來啦！」→「拾兒回來啦！全村等你呢！」；「仙門瞎了眼！」→「仙門那是瞎了眼！」；「妳、妳怎麼知道？」→「妳、妳怎麼知道饅頭的事？」；「人回來就好。」→「人回來就好，菜還熱著。」；「傻孩子。」→「傻孩子，自己不吃。」；「石頭……會發光？」→「饅頭裡有發光的石頭？」；「又是字……我看不懂。」→「又是字……我一個都看不懂。」；「奶奶，上面寫什麼？」→「奶奶，上面到底寫什麼？」；新增「石板……怎麼燒紅了？」「您怎麼知道我今晚到？」。
- 不接觸：三嬸不再揉陸拾的頭髮（s28 改成把錘子掛回腰帶）。
- 過程：pace.spread 一度 1.8／2.0（< 2），把 s24 錘子砸地改成 1 s、s06 台詞縮成「等我？」之後過；s37 一度估 3.6 s 要買 5 s，台詞縮短後回到 4 s。
- 檢查：lint 0 錯誤、drama_craft_check 30 項全過、shot_reading --strict 0 陷阱、shot_plan --strict 沒有問題、script 重產；validate.mjs ok（10 季 600 集）。
- 等站主：refs 是真人劇照質感，3D 版要不要先重畫 3D 參考；石板燒紅會不會太早暗示三嬸的真身。
