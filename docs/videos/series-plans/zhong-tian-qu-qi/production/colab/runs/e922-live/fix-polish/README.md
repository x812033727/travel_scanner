# 第 22 集真人版 fix-polish：上架前精修重拍（2026-11-21）

`review-zt/consolidated/retakes.json` 裡 e022 列 A 或 B 的只有 **s22（B）**；s33、s14、s17、s40、s06、s38、s20、s31 都是 C（交站主決定或有不花錢的修法），這一輪不寫。

- 種子 9229101、9229102；960×544 Ref2VA；1 鏡 2 支，共 12 秒。
- base：`picks.json` 的 s22 是 seed 9221101、`motion_from: d1` → `d1/prompts/ref-s22-9221101.txt`（d1 檔名帶種子，`st1` 不用找）。
- 產生：`python3 -I ../../_scripts/polish-build.py 22` → `~/mokaair-work/videos/zhong-tian-qu-qi-e922-dh/runpod/live/fixp/`。
- 台詞一字沒改（片段原聲，許硯說）。

| 鏡 | 審片問題（現在那支） | base | 改了哪些句子（舊 → 新） | 換圖 | 拿不準的 |
| --- | --- | --- | --- | --- | --- |
| s22 | 阿令剛說「她今晚會走」，許硯第一格咧嘴笑、之後整鏡嘴角帶笑說「她要走？她今天在城裡，到底見了誰？」，像在說笑；「她要走？」後停 1.75 秒（畫格條 `shots/s22.jpg`、`x/s22f.jpg`） | `d1/…/ref-s22-9221101.txt`，6 秒 | 構圖：「toward Aling off screen right」→「toward the young woman off screen right」（不點名畫外的人）；「the smile gone: brows drawn together, eyes darkening, lips moving low」→「從第一格起臉就因突然的擔心繃住：眉壓低往中間皺出深紋、眼睛瞇起發暗、咬緊下顎、嘴角拉平往下、嘴唇抿成一條緊直線」（拿掉 smile 字，冷臉逐部位寫）；筷子寫成「普通木筷，在胸前高度舉在半空」。動作：說話句加「低、快、緊繃，第二句緊接第一句一口氣說完」；加「說話全程眉皺、下顎緊、嘴角朝下」；「chopsticks stop in mid-air and he lowers them slowly to the table」→「拿筷子的手慢慢沉到桌邊」；「eyes moving from her to the doorway」→「眼睛從她臉上往更右邊、畫外暗著的灶房門滑過去」；結尾「keeps looking at the doorway」→「最後一個字說完嘴唇抿回一條緊直線、盯著灶房門、眉到最後一格都皺著」 | 不換：base 已經只送 `xuyan-angle-a-l1`（三張許硯圖裡唯一不笑的，教訓見 lessons〈xuyan-portrait-t1 與 angle-b 斜嘴笑〉） | ① 同一張不笑的圖、base 也寫了皺眉仍整鏡帶笑，這次只靠拿掉 smile 字與逐部位冷臉加三次重複，賭的是文字；② 「一口氣說完」能不能消掉 1.75 秒停頓要聽原聲，不行就剪接時把停頓剪短；③ 灶房門與阿令同在畫右，眼神移動幅度小，可能看不太出來（接受） |

## 三個檢查（2026-11-21）

- `polish-build.py 22`：0 錯，1 鏡 2 支 12 秒。
- `preflight-prompts.py …/fixp/colab-jobs.json`：0 error、0 warning。
- `h3r.sh check --manifest …/fixp/colab-jobs.json`：0 error、0 warning。

## 挑片時看

- 第 0 格起嘴角有沒有上揚、有沒有露牙（放大看 0、1.5、3、句尾、最後一格）。
- 兩句之間的停頓長度（原聲）；台詞是不是稿子原句。
- 眼睛是否朝畫外右、沒看鏡頭；筷子有沒有放下。
