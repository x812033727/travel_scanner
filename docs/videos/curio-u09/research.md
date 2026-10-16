# U09：紙帶上的「小綠人」——研究底稿

- 查核日期：**2026-10-16（Asia/Taipei）**。
- 階段：原大綱 A 已由站主核准；正式稿、`video.json` 與逐句證據索引已起草，待獨立覆核及劇本核准；未啟動付費製作。`brief.md` 為符合現行 lint 補三個格式小節，A／B 選項正文未改；原、新 SHA 與重新送審要求記在 `script-status.md`。
- 舊題庫僅作查找線索：`origin/claude/curio-topic-bank-second-batch`，提交 `949bb91fc85d41a53633d056062b27d87651e9d5` 的 `docs/videos/history-curiosity/topic-checks/U09.md`。本集沒有修改共享題庫，也沒有把舊查核日改成今天。
- 製作規則：已讀 `curio-episode`、`youtube-video`、`script-writing.md` 的故事／開場／十三題，以及 H01-v2 前 30 景、系列 README 與 look。

## 這一集回答什麼

1967 年劍橋收到的規律無線電訊號，為什麼會被叫作「小綠人」，又怎麼找到自然來源？

結檔為**存檔**：這項發現通向脈衝星。要保留的歷史層次是「辨認出規律訊號」「排查干擾與人工來源」「找到更多同類」「提出及驗證物理解釋」。不能把四件事縮成貝爾第一眼就認出一顆自轉中子星。

## 今天實際開到的來源

`opened` 指讀到文章、摘要或原件；HTTP 200 卻只有登入中轉頁不算讀到原文。以下不使用新聞轉述代替研究論文本身。直接抓取使用 `Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)`。

| ID | 來源、年份與網址 | 本次開啟狀態 | 用途與限制 |
| --- | --- | --- | --- |
| S01 | Cambridge，Louise Walsh 訪問 Jocelyn Bell Burnell，〈Journeys of discovery〉，[原頁](https://www.cam.ac.uk/stories/journeysofdiscovery-pulsars) | **opened**。瀏覽工具 403；同一公開頁用規定 UA 直接 GET 200，讀到完整問答。 | 當事人口述：LGM 是玩笑標記；1967-11-28 等間距脈衝；另一台望遠鏡因計算過境時間有誤，晚五分鐘才看見。晚年回憶的細節需標明來源性質。 |
| S02 | Churchill Archives Centre，〈Hunting pulsars / MISC 109〉，[舊入口](https://archives.chu.cam.ac.uk/?p=2930)、[現行頁](https://archives.chu.cam.ac.uk/collections/research-guides/misc-109/) | **opened**。舊入口轉址後 GET 200，讀到館方介紹與 Craig Mackay 2019-01-08 回憶。 | 館藏 1967-08-06 紙帶；同學描述檢查紙帶與尋找光學對應體；LGM 的玩笑性質。這是館方說明及回憶，並非所有原紙帶逐張驗證。 |
| S03 | S. Jocelyn Bell Burnell，〈Little Green Men, White Dwarfs or Pulsars?〉，1977 演講稿刊本；Cosmic Search 授權重刊，[全文](https://www.bigear.org/vol1no1/burnell.htm) | **opened**。全文可讀，頁尾明示原刊及授權重刊。 | 建造、人工讀圖、快紀錄、干擾排查、第二訊號與其後更多候選。是事後回憶，作者自己提醒相隔八九年。本文僅摘取本集所需，未複製長文。 |
| S04 | Antony Hewish，1974 Nobel Lecture〈Pulsars and High Density Physics〉，[官方 PDF](https://www.nobelprize.org/uploads/2018/06/hewish-lecture.pdf) | **opened**。瀏覽工具 403；直接 GET 200，249,156 bytes，讀取 PDF 印頁 177–179。 | 11 月 28 日、12 月的精密計時、人工來源疑慮、都卜勒、1968 年的解釋演變。這是 Hewish 自己的回顧，與 Bell 的回憶分開署名。 |
| S05 | Hewish、Bell、Pilkington、Scott、Collins，〈Observation of a Rapidly Pulsating Radio Source〉，Nature 217，709–713，1968-02-24；[出版頁](https://www.nature.com/articles/217709a0)、[Cornell 學術鏡像 PDF](https://hosting.astro.cornell.edu/~shami/psrintro/papers/HBP%2B68.pulsars.pdf) | **opened：原論文掃描**。出版頁轉登入中轉，未取得正文；Cornell PDF 536,855 bytes／5 頁，可下載。視覺檢查印頁 709 與 713。 | p.709 原摘要、作者、週期約 1.337 秒、另外三個來源、白矮星／中子星振盪候選；p.713 明說還需更多觀測。不能稱首篇論文已定案為自轉中子星。 |
| S06 | T. Gold，〈Rotating Neutron Stars as the Origin of the Pulsating Radio Sources〉，Nature 218，731–732，1968-05-25，[出版頁／DOI](https://www.nature.com/articles/218731a0)、[UBC 學術鏡像 PDF](https://phas.ubc.ca/~heyl/ASTR304_2003W/papers/gold.pdf) | **opened：獨立覆核者視讀學術鏡像印頁 731–732**。原撰稿者只取得出版方索引題名、日期與摘要；出版頁轉登入中轉。獨立覆核者另取得 UBC PDF，HTTP 200、881,630 bytes，讀取兩頁原件。 | p.731 摘要提出自轉波束；p.732 給出自轉論證，並保留發射機制仍不清楚的限制。原件標示 5 月 20 日收稿、5 月 25 日出版，支持開場「五月投出一篇兩頁論文」。不聲稱 Gold 是所有相關理論的唯一先驅，也不把提案寫成當場完成全部實證。 |
| S07 | NASA Science，〈Pulsars〉，頁面更新 2026-03-11，[原頁](https://science.nasa.gov/mission/hubble/science/science-behind-the-discoveries/hubble-pulsars/) | **opened**。讀到脈衝星、波束掃過視線、發現沿革段落。 | 今日的自轉中子星模型。全片只用「燈塔」一個比喻；不使用網頁中的現存數量、最快紀錄等會分散主線的數字。 |
| S08 | Cavendish Laboratory，訪問脈衝星研究者 Lucy Oswald，2026-02-11，[原頁](https://www.phy.cam.ac.uk/news/celebrating-women-in-science-meet-lucy-oswald-our-new-pulsars-researcher/) | **opened**。劍橋物理系全文問答可讀。 | 現行研究仍未完全解清發射波束的微觀機制；此限制不等於最初訊號身分未明。只作結論邊界查核，不另開現代天文學支線。 |
| S09 | University of Manchester / Jodrell Bank，Frontiers of Modern Astronomy，〈Observations of Pulsars〉，[§4.1](https://www.jb.man.ac.uk/distance/frontiers/pulsars/section4.html) | **opened**。正式稿階段於 2026-10-16 讀到 §4.1 色散與 §4.2 計時全文。 | 只補一個必要的白話機制：星際物質會令不同頻率脈衝的到達時間不同。不取本文其他觀測設備、個別脈衝星或數量作旁支。 |

本次原件辨識：S04 SHA-256 `796c3561bb98da011699ee60c06f7a7ba423bc4360f5635b688c1900d29ee579`；S05 SHA-256 `df2799809a5bb2eb87e1ebc7ad8ec6e688df2cc0861c9d764d8a1d3325dc3d2e`；S06 獨立覆核者回報 SHA-256 `77a83ec7ff66c36d7349b16c4c223ec58b38305f9a518958cb7296bbed2abfb1`。PDF 只作查核，沒有放進 Git 或當成影片素材授權。

正式稿補查：2026-10-16 原撰稿者重開 S03 授權全文、S07 NASA 頁面與 S06 UBC PDF，確認新增讀圖、錯過一次快紀錄、假期維持觀測與 Gold 減速預測的範圍；S06 全文此時亦由作者取得。企劃表保留先前誰取得哪些範圍的紀錄。新增主張編為 C25–C31；同一已查核主線未變。

## 故事可用的時間順序

1. **1967 年夏季，設備本來要找別的東西。** 新望遠鏡以無線電閃爍研究緻密電波源；Bell 參與建造，之後人工檢查紙帶。正文只留「要研究類星體」及讀圖工作，不把天線尺寸、電線里程、造價全唸一遍。[S01、S03、S05]
2. **8 月，記錄留下不合分類的小段訊號。** 館藏紙帶日期為 8 月 6 日。不要把「當天有記錄」加寫成當天下午幾點她立即發現，也不要說那時已看出規律脈衝。[S01、S02]
3. **加快記錄後，等待沒有立刻成功。** 原來的紙帶把細節擠得太密；Bell 回憶更快的紀錄器曾連續一段時間只留下雜訊。11 月 28 日才看清等間距脈衝。整集首次報週期在此：口播「大約一又三分之一秒」，卡片「約 1.337 秒」。[S01、S03、S04、S05 p.709]
4. **人造干擾很合理，卻被新的觀測逐項限制。** 脈衝跟著天空位置出現；另一台望遠鏡與獨立接收設備也接到訊號。Bell 後來回憶那次苦等，是把到達觀測位置的時間算早了五分鐘。把現代口述當成她的回憶來講，不編現場對話。[S01、S03]
5. **小綠人是玩笑代號，人工來源仍要檢查。** Bell 在 Cambridge 訪談說自己用 LGM 作玩笑標記；Hewish 的 Nobel 演講則記錄曾面對「外部文明在行星上發射」的可能並繼續計時。兩者可同時成立，不寫成團隊正式宣布遇到外星人，也不推定所有人的信念相同。[S01、S02、S04]
6. **12 月，計時與頻率變化把問題推向宇宙。** 觀測到的都卜勒變化符合地球運動；色散估計讓來源落在太陽系之外。這降低當時某些人工來源模型的可信度，不等於一個觀測能排除所有可能的外星文明。[S03、S04]
7. **聖誕節前，另一片天空也留下異常。** Bell 回憶凌晨在低溫下把接收設備恢復工作，抓到第二串約 1.2 秒間距的脈衝。她描述自己的鬆一口氣：同類來源不只一個了。這段只說聖誕節前，不硬寫精確日期。[S03]
8. **假期後，更多同類出現。** 首篇論文 p.709 明寫另外三個相似來源；故事由「一個無法分類的例外」變成「一類天體」。不將第四顆 0.25 秒數值和三四顆所有編號再堆進旁白。[S04、S05]
9. **1968 年 2 月，發表仍不等於解完。** 原論文摘要及正文提出白矮星或中子星的振盪候選，末段仍要求更多觀測。它不是一份已完成的「自轉中子星」答案書。[S05]
10. **5 月及其後，節拍有了新的物理解釋。** Gold 的自轉模型提供另一種時鐘：緻密星體旋轉，波束掃過視線。後續觀測支持這個方向；今日的脈衝星解釋沿用自轉中子星模型。把完整機制留給最後一章，不在開場先揭曉。[S04、S06、S07]

## 必須守住的區別

- **記錄日期／注意到異常／確認脈衝**不同。8 月 6 日紙帶不等於 11 月 28 日快紀錄。
- **週期規律／每一個脈衝都一樣**不同。圖上可畫週期間距，不把每次強度畫成完美一致的工整心電圖。
- **跟隨恆星時／跟著民用時鐘固定時刻**不同。口語說「跟著那片星空回來」，不要說「每天晚上同一個鐘點」。
- **LGM／LGM-1**：本集用當時可核實的 LGM；不拿後來常見的 LGM-1 作 1967 年正式天體名稱。
- **人為可能性／外星聯絡證據**不同。沒有解碼訊息、沒有收到語音，也沒有科學家正式對外宣布外星文明。
- **振盪／自轉**不同。2 月論文與 5 月解釋分開；也不說 5 月一篇論文當場證明全部機制。
- **個人回憶／共同決議**不同。Hewish 和 Bell 的感受及敘述要各自歸屬；不使用焚毀紀錄、保密陰謀等旁支。
- 1974 Nobel 與 2018 Breakthrough Prize 不進本集大綱。它們會把「這個訊號是什麼」改成「誰得到承認」的第二條主線。

## 視覺及聲音

保留 `cute-mystery` 與 MiniMax `image-01`。Bell、Hewish、Gold 等近代人物不生成本人臉孔或相似漫畫像；故事中的真人只以無可辨識面貌的剪影、手部與紀錄器關係呈現。可用無姓名的虛構檔案閱讀者表情作閱讀反應，但不可冒充 Bell，也不新增其遭遇或台詞。文字姓名與日期由卡片疊加。

原件能查閱不代表可重製影像。Cambridge 人物照片、館藏紙帶與 Nature 掃描本次都沒有取得素材授權；不要直接把查核截圖放入成片。模型畫的波形是示意，精確週期與實際圖形的引文只在合法卡片中處理。音效若模擬等間距滴聲，標「節拍示意」，不能稱當年錄音或直接播放原始無線電聲音。

## 後續門檻

大綱 A 及繁中製作費用上限 US$6／集、五集 US$30 已獲站主授權；正式稿尚待獨立史料覆核、只讀劇本十三題盲評及站主劇本核准。授權上限不等於本稿已通過內容關卡；本輪沒有付費呼叫、沒有後台劇本送審。多語、片段與額外音樂不在本次授權內。
