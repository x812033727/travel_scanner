# 五部約兩小時的原創漫劇｜Claude 版企劃包（2026-09-28）

站主要五部各約 120 分鐘、目標破百萬點閱、鋪陳與緊湊感都要好的漫劇，並同時請 Codex 規劃五部，之後比誰的點閱率高、劇情好。這裡是 Claude 版：五部原創故事，每部都是 [`docs/videos/BINGE.md`](../../BINGE.md) 的一鍵合集（40 集 × 3 分鐘、四篇各 10 集、hybrid 畫面、做完接成一支長片），文件用產線的 `body_md`／`body_json` 形狀交付，全部通過工人自己的 `documentProblem`／`retentionProblem`。Codex 版在 [`../binge-five-20260928/`](../binge-five-20260928/README.md)（分支 `codex/five-binge-story-plans`）；兩批的比法在 [`COMPARE.md`](COMPARE.md)。

這是製作企劃，不是成片：沒有建立後台作品、沒有生成圖片與聲音、沒有上架；百萬點閱是目標，不是交付保證。

## 五部

| 順序 | 作品 | 題材／主角 | 一句話 | 為什麼有機會破百萬 |
| --- | --- | --- | --- | --- |
| 1 | [開服第一天，她的天賦叫讀檔](reload-first-day/README.md) | 系統遊戲／女主 | 全城覺醒職業，只有她的天賦是「讀檔」；她死三十次拿下首殺，但每次讀檔都在吃掉她記得阿嬤的方式 | 站主給的參考影片就是這個題材；「讀檔」是一句話能懂又沒人做過的機制，每一次死而復來都是爽點，代價是記憶，情感線自帶淚點；反派的「存檔」與她的「讀檔」是同一套規則的兩面，結局用規則反殺 |
| 2 | [重生回落槌前一秒](before-the-hammer/README.md) | 重生復仇／女主 | 她把一壺熱茶倒進八千萬的假盞，當眾否定自己的簽名；師兄還在數錢，她已磨好刀 | 鑑寶打臉是華語網文長銷類型；「注熱茶見釐光」是一個三秒就能看懂、每集都能重複用的當眾驗真儀式；國寶是假的、廚房茶杯是真的，第 20 集翻轉可分享 |
| 3 | [三針](three-needles/README.md) | 都市歸來／男主 | 被逐出家門七年，他背著針包回來時全家正在賣掉百年藥堂；一針下去，看不起他的人全閉嘴 | 歸來打臉加神醫是最穩的男頻組合；三針之限與第四針借命給了每一次出手代價；「死了七年的女孩其實活著」讓第 20 集重寫整部前提 |
| 4 | [她替公主試毒十年](taste-of-the-throne/README.md) | 女帝崛起／女主 | 嘗使嘗出太后的毒、皇帝的病、井裡的藥，最後嘗出自己的血脈 | 「試毒女官」是宮鬥裡沒被用爛的視角，舌頭就是偵探；每天喝的解毒湯其實是毒，公主一直知道，第 20 集把前面所有保護都變成利用；結局廢除嘗使，是一句話能講完的收尾 |
| 5 | [符師與他的鬼](ghost-at-his-side/README.md) | 自訂／雙男主留白 | 搭檔死後一年回來坐在他桌上：「沈大人，你袖子裡有我。」只有他看得見的鬼，兩人聯手查全城的命被誰借走 | 站主偏好的仙俠雙男主羈絆與鬼怪符籙；「只有他看得見」是最強的兩人戲設定；借命符讓每個案子都是倒數；「你活的是他的命」翻轉後，燒符與不燒符就是整部的情感 |

每部目錄：`source.mjs`（作者唯一編輯的檔）與 `build.mjs` 產生的 19 個檔案——`setting.md`／`.json`、`outline.md`／`.json`、`chapter-01..04.md`／`.json`、`documents.json`（六份待送件）、`series-request.json`（`SeriesIn`）、`continuity.md`、`packaging.md`／`.json`、`README.md`、`manifest.json`（來源與每個檔的雜湊）。

## 五部共同的緊湊規格

這批把「鋪陳好、看起來緊湊」寫成可以檢查的規則，`validate.mjs` 每一條都擋：

- **第一句就是鉤子**：每集 `hook` 是能直接說出口的一句話，≤ 28 字（產線量到 8 秒就退件，28 字約 6 秒，留餘裕），40 句不重複；沒有片頭卡、沒有前情。
- **10 秒衝突、30 秒第一個爽點、每集至少兩個爽點**，第一個在前半；爽點寫成觀眾看得到的畫面或聽得到的那句話，不寫「她很厲害」。
- **爽完就來更大的麻煩**：主角不能連兩集只挨打；三集連贏會被警告。
- **最後一句就是懸念**：懸念分五型，相鄰兩集不同型（跨篇也算）；第 10／20／30／40 集必須是揭露或反轉，改變觀眾對本篇某件事的理解。
- **第 18–22 集之間正好一次翻轉世界觀**（五部都放在第 20 集，約 60 分鐘處），讓前一小時的畫面換一種意思。
- **每條謎團都有帳**：8–12 條長線謎團，埋下、推進、揭曉的集數寫在設定集，細綱的 `setups`／`payoffs` 必須對上；任何連續四集至少收一條。全部在第 40 集前收完（`open_ended: false`，不留續作懸案）。
- **第 1 集的動作在第 40 集倒過來演一次**（倒茶揭假→倒茶喝真；吞毒閉嘴→自己吃第一口；掌心寫「走」→寫「留」；忘掉的生日→記回來；血寫的符→燒掉的符）。
- **每部一個會自己製造爽點的機制**（讀檔、釐光、三針、舌頭、借命符），規則在第一篇立好，結局用它翻盤，不靠新設定救場。
- **人物與場景逐字沿用**：角色外觀是 ≤ 800 字元的英文提示詞、每集逐字複製；聲音是 Gemini 內建聲音的擬定 casting（旁白 Sulafat），開拍前先試聽；場景有固定辨識物，讓關鍵影格跨集一致。

## 怎麼餵進產線

1. **建作品**：`<slug>/series-request.json` 就是後台「漫劇」分頁一鍵開拍表單送的 `SeriesIn`（`POST /api/v1/admin/video-automation/series`）。`hands_off` 預設 `false`，所以建立後不會有工人自己開始花錢；要全自動就在作品頁把「免關卡」打開。建立前先照 [`references/series.md`](../../../../.agents/skills/youtube-video/references/series.md) 的「坑」調預算（片段秒數、圖片、每月集數、同時在做的集數）。
2. **餵文件**：`<slug>/documents.json` 的六份（設定集、總綱、四篇細綱）各是 `{kind, chapter_number, body_md, body_json}`。兩條路：站主在作品頁「自己改」（`PUT …/series/<slug>/docs/<kind>[/<n>]`，`approve: true`）直接放進去當核准版；或讓工人自己企劃、再拿這裡的版本比對。`body_json` 的形狀就是企劃提示詞要求的形狀，加了 `answer`、`carry`、`world_flip` 等產線忽略的欄位給撰稿與查核用。
3. **先做前三集校準**：任何一部都先做第 1–3 集（約九分鐘），用 `retentionNumbers` 量鉤子與第一個爽點的實際秒數、看重做率與花費，再決定五部的順序；不要五部同時送進付費生成。
4. **合集**：40 集完成後由產線接成 `<slug>-full`；合集 `video.json` 的 `compilation` 把 `chapter_cards` 與 `outro` 關掉，一口氣看到底，YouTube 章節照實際時間軸；`packaging.md` 的三組標題與三組縮圖給 YouTube 的標題／縮圖測試用。

## 檢查與重建

從 repo 根目錄：

```bash
node docs/videos/series-plans/claude-binge-five-20260928/build.mjs            # 由 source.mjs 重建每部的 19 個檔
node docs/videos/series-plans/claude-binge-five-20260928/validate.mjs --write-report
node --test docs/videos/series-plans/claude-binge-five-20260928/validate.test.mjs
```

`validate.mjs` 先跑工人的規則（`tools/video/automation/series.mjs` 的 `documentProblem` 與 `retentionProblem`），再跑上面那一節的規則，最後比對產生檔是否過期；結果在 [`validation-report.json`](validation-report.json)。機械檢查證明的是結構與節奏規格，不是故事好不好看；好不好看用 [`COMPARE.md`](COMPARE.md) 的盲讀與上架數字來比。作者契約在 [`AUTHORING.md`](AUTHORING.md)。
