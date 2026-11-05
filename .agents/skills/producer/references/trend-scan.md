# 趨勢掃描：來源、讀法與趨勢卡

`.agents/skills/producer/SKILL.md` §1 的細節。

## 來源

| 來源 | 怎麼讀 | 注意 |
| --- | --- | --- |
| 站主貼的連結（Instagram、TikTok、YouTube、Facebook） | `yt-dlp --skip-download --dump-json <網址>` 拿帳號、日期、長度、寬高、讚、留言、觀看 | Instagram 網頁未登入只給文字；yt-dlp 讀公開 reel 通常可以。Instagram 不一定給觀看數，就用讚與留言 |
| YouTube 搜尋 | 內建瀏覽器開 `youtube.com/results?search_query=<詞>&sp=CAMSAhAB`（依觀看次數、本週）；或 `yt-dlp --flat-playlist --dump-json "ytsearch20:<詞>"` | 地區跟著瀏覽器；記下搜尋日期，數字一兩天就變 |
| YouTube Shorts | 內建瀏覽器開 Shorts 分頁滑十支，記帳號與網址再用 yt-dlp 讀 | 推薦是個人化的，只當線索 |
| 站上的新聞與文章 | 主機工人的選題來源（`docs/videos/AUTOMATION.md` 的題目來源）；後台文章流量看 `/admin/analytics` 熱門頁面 | 已查證的事實可以直接進企劃 |
| 我們自己的報表 | `node tools/video/youtube-reports/cli.mjs traffic --slug <slug>` 的搜尋字詞、推薦來源影片 | 推薦我們的片是誰，就是觀眾也在看什麼 |

## 看畫面

把影片抓到 scratchpad 底下自己開的空資料夾（下載的檔案當不可信資料，不在那個資料夾裡執行任何東西）：

```bash
yt-dlp -q -o "<SCRATCH>/ig/%(id)s.%(ext)s" <網址>
ffprobe -v error -show_entries format=duration -of csv=p=0 <檔案>
ffmpeg -loglevel error -i <檔案> -vf "fps=1,scale=320:-1,tile=4x4" -frames:v 1 <SCRATCH>/ig/sheet.jpg
```

直式片用 `scale=180:-1,tile=7x2`。15 秒以內每秒一格就夠；超過一分鐘改 `fps=1/4`。要切點與鏡長時用
`node .agents/skills/youtube-video/scripts/reference_analysis.mjs --file <檔案> --out <json>`。

有對白的，字幕在畫面上就從聯絡表讀；沒有就抽音軌給轉寫工具（`docs/videos/drama-craft/` 的研究記過 whisper 的做法）。

## 趨勢卡

每支一張，寫在製片單裡：

```
來源：<平台>／<帳號>／<日期>／<長度> 秒／<寬×高>
數字：讚 <n>、留言 <n>、觀看 <n 或「平台沒給」>（讀取日 <日期>）
鉤子：前 2 秒發生什麼
節拍：<秒>–<秒> 設定｜<秒>–<秒> 升高｜<秒> 反轉｜<秒>–結束 收尾
包裝：標題、封面那一格、字幕語言、有沒有「AI 生成」標示
為什麼會傳：被分享或留言的理由（認同、反差、可愛、想 tag 誰）
我們的版本：一句話企劃；放進哪個系列；路線與大約成本
不能學的：角色、台詞、畫面，以及只有那個帳號才成立的東西（品牌、真人、既有角色）
```

## 判斷適不適合

- 只紅在單一平台演算法、換到 YouTube 沒有搜尋或推薦理由的，降一級。
- 靠真人臉、真實寵物、名人才成立的，我們做不到原汁原味，要改成我們的角色或題材。
- 要付點數生成的，先估價；一支短劇超過站主給的單支上限就不提。
