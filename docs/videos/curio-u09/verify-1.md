# U09 正式劇本獨立史料覆核（第 1 輪）

- 覆核日：2026-10-16（Asia/Taipei）。覆核者未參與 U09 正式稿撰寫。
- 對象：`video.json` SHA-256 `CCD845B56DAE53A5828DFD1B93881D273E8BDA963D74B61327F074ACAC9FE50D`；101 景、102 句、91 個插畫鏡頭、9 張內容卡、1 個片尾。102 句均無 `say` 覆寫。
- 抽取索引：所有旁白逐句文字與主張 ID 見 [script-evidence.md](script-evidence.md)；本表逐一核對 C01–C31，另核對每張內容卡、縮圖、`youtube` 標題、說明與標籤。`claims.md` 是作者自查，不作獨立證據。
- 結果：31 項史料／科學主張 **CONFIRMED**，0 項 CHANGED，0 項 NOT FOUND。E01 為編輯邀請，OUT OF SCOPE。沒有尚待解決的事實阻擋；本輪未改稿，無須事實查核第 2 輪。敘事盲評與站主劇本核准是其他關卡。

## 本輪實際查閱的來源

| 代號 | 來源與直接網址 | 本輪讀取狀態 | 用途與限制 |
| --- | --- | --- | --- |
| A | Bell Burnell 1977 第一人稱回憶，[Cosmic Search 授權重刊](https://www.bigear.org/vol1no1/burnell.htm) | HTTP 200，全文可讀 | 1967 工作流程、紙帶、排查、聖誕節前後；她在文首提醒回憶已隔八九年。 |
| B | [Cambridge University 訪談](https://www.cam.ac.uk/stories/journeysofdiscovery-pulsars) | 指定 editorial UA 直接 GET 200，553,893 bytes；一般瀏覽工具 403，搜尋索引可讀原文段落 | LGM 玩笑、11 月 28 日、另一台設備晚五分鐘；後年口述，不當作實驗日誌。 |
| C | [Churchill Archives Centre 館藏說明](https://archives.chu.cam.ac.uk/collections/research-guides/misc-109/) | HTTP 200，正文可讀 | 館藏 1967-08-06 紀錄及同儕回憶；未取得複製原紙帶影像的權利。 |
| D | [Hewish 1974 Nobel lecture 官方 PDF](https://www.nobelprize.org/uploads/2018/06/hewish-lecture.pdf) | 指定 editorial UA 直接 GET 200，249,156 bytes、10 頁；本輪抽讀印頁 177–179；一般瀏覽工具 403 | 11 月 28 日、地球公轉引起的都卜勒、早期模型；這是 Hewish 的回顧，與 Bell 分開歸屬。 |
| E | [Hewish 等，Nature 217 (1968) 709–713](https://hosting.astro.cornell.edu/~shami/psrintro/papers/HBP%2B68.pulsars.pdf)；[出版資訊](https://www.nature.com/articles/217709a0) | Cornell 原件學術鏡像 HTTP 200／5 頁；出版頁轉身分驗證，未把轉址當讀到正文；原件此前已由獨立企劃覆核者視讀印頁 709、713，本輪再對出版索引及原件校對 | 1.337 秒、另外三來源、五位作者、白矮星／中子星振盪候選；首篇不是自轉模型定案。 |
| F | [Gold，Nature 218 (1968) 731–732 原文學術鏡像](https://phas.ubc.ca/~heyl/ASTR304_2003W/papers/gold.pdf)；[出版資訊](https://www.nature.com/articles/218731a0) | UBC HTTP 200，881,630 bytes／2 頁；本輪抽取原文核對，原件學術鏡像先前亦已視讀；出版頁索引可讀，正文轉身分驗證 | 1968-05-20 收稿／05-25 出版、自轉波束、能量損失及週期逐漸變慢的有條件預測。 |
| G | [NASA Science：Pulsars](https://science.nasa.gov/mission/hubble/science/science-behind-the-discoveries/hubble-pulsars/) | HTTP 200，更新標示 2026-03-11 | 今日中子星自轉、波束掃過視線及減速；不拿今日模型倒寫成 1968 年 2 月結論。 |
| H | [Cambridge Cavendish：Lucy Oswald 訪談](https://www.phy.cam.ac.uk/news/celebrating-women-in-science-meet-lucy-oswald-our-new-pulsars-researcher/) | 原頁搜尋索引讀到 2026-02-11 完整相關答句；一般瀏覽工具未取全文，作者曾直接 GET 200 | 今日電波波束微觀產生機制仍有研究空白，並非來源身分未明。 |
| I | [University of Manchester／Jodrell Bank：Observations of pulsars](https://www.jb.man.ac.uk/distance/frontiers/pulsars/section4.html) | HTTP 200，教學正文可讀 | 頻率相關色散與計時；不說真空光速因頻率而變。 |

## 逐項主張判定

「位置」列包含主要句 ID；同一主張在其他句／`scene.data` 的完整對照見逐句索引。`A`–`I` 指上表來源與讀取狀態。沒有改字，故最後一欄均為原文保留。

| # | 主張 | 位置（句 ID／卡片） | 來源 | 判定／前→後 |
| --- | --- | --- | --- | --- |
| C01 | 1967 Bell 是劍橋博士生，參與望遠鏡工作 | `96e528ee`、`8748fb3d` | A、B | CONFIRMED／不變 |
| C02 | 設備原來研究類星體的電波變化 | `6acf7c94` | A、B、E | CONFIRMED／不變 |
| C03 | 每日人工檢查約 30 公尺紙帶；96 英尺換算約 29.26 公尺 | `1631f62b`、`daily-paper.data` | A | CONFIRMED／不變 |
| C04 | 館藏有 1967-08-06 初始訊號紀錄，不等於當時已辨識脈衝 | `96e528ee`、`8748fb3d`、開場視覺 | B、C | CONFIRMED／不變 |
| C05 | 異常小段在同一片天空的紀錄中重現，並非每次都在 | `a183b99a`、`449bbb4c`、`54c3000a` | A、B | CONFIRMED／不變 |
| C06 | 換快紀錄器後連續數週只留下接收器雜訊 | `e3e46d77`、`0c47ad34`、`8d87d7e4`、`efd6c54a` | A、B、D | CONFIRMED／不變 |
| C07 | 1967-11-28 首次清楚記到規律脈衝 | `718638d1`、`ba179597`、`november-detection.data` | B、D | CONFIRMED／不變 |
| C08 | 第一來源約 1⅓ 秒，論文數值約 1.337 秒 | `fdeda684`、`measure-period.data` | A、B、E | CONFIRMED／不變 |
| C09 | Hewish 首先懷疑人造干擾是合理排查 | `f58aba8f`、`37c4b04a` | A、D | CONFIRMED／不變 |
| C10 | 異常依天空位置／恆星時重現，不是民用鐘點不變 | `d15db021`、`01625c23`、`2f1bf500` | A、D | CONFIRMED／不變 |
| C11 | 另一台望遠鏡及獨立接收系統同樣量到脈衝 | `cb83227e`、`a0f8a979`、`eea8a036` | A、B | CONFIRMED／不變 |
| C12 | Bell 回憶第二設備晚五分鐘是過境時間計算錯誤 | `90259fa2`、`f76bb3e1`、`41b5eb07`、`2ec7abc8` | B | CONFIRMED／不變；明說「後來回憶」 |
| C13 | LGM 是 Little Green Men 玩笑代號，非正式外星宣告 | `e205076e`、`e3ef1239`、`99a55420`、`nickname.data` | B、C | CONFIRMED／不變 |
| C14 | Hewish 曾考慮遠方行星人工發射並繼續計時 | `aae6c002`、`5c699592` | D | CONFIRMED／不變；只歸於 Hewish |
| C15 | 計時變化符合地球公轉，未量到想找的額外行星運動 | `3d181765` 至 `1cf70848` | A、D | CONFIRMED／不變；沒有聲稱排除一切外星生命 |
| C16 | 色散估計顯示訊號來自太陽系外 | `1dfdcacf`、`2f829cd6`、`6461789b`、`outside-system.data` | A、D、I | CONFIRMED／不變 |
| C17 | 聖誕節前第二方向：低溫故障、恢復接收、約 1.2 秒；假期情節 | `fe66ab8a` 至 `dbb65c4a`、`second-period.data` | A | CONFIRMED／不變；作當事人回憶而非確日 |
| C18 | 後續確認合計四個相似來源 | `e72ed59d`、`9bc5a454`、`9410e2e4`、`confirm-more.data` | A、E | CONFIRMED／不變；沒有說同晚發現四個 |
| C19 | 1968-02-24 Nature 首篇論文與五位署名 | `049813c5`、`86806d23`、`paper-published.data` | E、Nature 當期目錄 | CONFIRMED／不變 |
| C20 | 2 月原論文考慮白矮星／中子星振盪，仍待更多觀測 | `3ecdf437` 至 `8f3ddd39`、`oscillation-candidates.data` | E、D | CONFIRMED／不變；未混同 5 月自轉提案 |
| C21 | Gold 5 月兩頁論文提出自轉中子星模型 | `2b58a7d7`、`b6d2d02b`、`724570c6` | F | CONFIRMED／不變；「投出」有 5 月 20 日收稿支持 |
| C22 | 自轉波束掃過視線才接到一次脈衝 | `59adb0ea`、`a856f45a`、`2d4ca310`、`2a37c45e` | F、G | CONFIRMED／不變 |
| C23 | 規律性本身不足判定智慧來源，本集後續證據支持自然解釋 | `1cf70848`、`336cd716`、`2a37c45e`、`f28a86d7` | A、E、F、G 的編輯推論 | CONFIRMED／不變；有限推論與站主觀點一致 |
| C24 | 波束產生的細部物理仍是研究問題 | `57dd9251` | H、G | CONFIRMED／不變 |
| C25 | 人工讀圖是當時熟悉新設備及辨別干擾的方法 | `634a9fab`、`7ccdf4c3`、`40de40ee` | A | CONFIRMED／不變 |
| C26 | Bell 曾去聽演講而錯過一次快紀錄，翌日例行紙帶見異常 | `ae51ed79`、`d5b03c7d` | A | CONFIRMED／不變 |
| C27 | 接收器敏感，Hewish 再觀察時也見脈衝 | `b872d2af`、`8e99187b`、`5315a9f5` | A、D | CONFIRMED／不變 |
| C28 | 團隊考慮並排除人類雷達經月球反射 | `6de2f659`、`0e6c77f2` | A | CONFIRMED／不變；未編具體檢查步驟 |
| C29 | 星際物質使不同頻率的接收時間有差 | `a88f7286` | I、A | CONFIRMED／不變 |
| C30 | Bell 對兩個同頻文明來源的推論；Hewish 假期補紙墨 | `e747682c`、`22561e92` | A | CONFIRMED／不變；前者歸於 Bell 的推論 |
| C31 | Gold 有條件預測自轉能量損失使週期逐漸變長 | `8ac591de` | F 原文末段；G | CONFIRMED／不變；旁白說「預測」，沒有冒充當場觀測 |
| E01 | 觀眾問題與訂閱邀請 | `3ecfc37e`、`259da0ce`、`subscribe.data` | 企劃 | OUT OF SCOPE／編輯語句不變 |

## 其他畫面、上架文字及聽感

- 9 張內容卡的日期、96 英尺／約 30 公尺、1.337 秒、1.2 秒、四個來源、作者名及振盪候選，已與同表 C03、C07–C08、C13、C16–C20 交叉核對。91 個 shot 的 `data.prompt` 是示意場景、無新增可檢驗的日期／數字；沒有把現代人物畫成可辨認肖像。縮圖只提出節拍疑問，未偷放結論。
- `youtube.title` 的 1967 劍橋與 LGM 有 A–C 支持；`description` 分開 LGM 玩笑、2 月振盪與 5 月 Gold 自轉，且揭露 AI 插畫不是史料影像；`tags` 的人名、主題、年份與正文一致。沒有冒稱取得館藏紙帶、Nature 掃描或人物照片的素材授權。
- 站主觀點「綽號與規律數字不能代替來源檢驗」在 `brief.md` 明列；結尾只作有證據界線的編輯推論。沒有虛構站主個人觀測或親身經驗。
- 逐句聽感：`2a37c45e` 稍長，合成時要留意斷句；這不是事實錯誤。口播沒有 URL、括號、拉丁專有名詞直念或「經查證／根據官方文件／本影片」式查核報告口氣；`Nature`、LGM、Gold 等英文字只在卡片／後台文案或中文口語對應處。開場沒有先揭自轉結論。
- `node tools/video/cli.mjs lint --slug curio-u09`：**0 errors／0 warnings**；預估 10.1 分、102 句、2,076 口播單位。此為文字估時，尚無實測音訊。
- 可能隨時間變動的是 C24 對發射機制的研究現況；本輪以 2026-02-11 Cambridge 訪談核對，發片前若久置需再查。其餘日期為歷史記錄。沒有更改任何事實，因此不觸發「超過三項事實改動」的第 2 輪門檻。
