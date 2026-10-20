---
id: 2026-10-19-curio-s-series-next-seven
title: Extend the Curio history video production queue to twenty episodes
status: in-progress
priority: P3
area: docs
owner: codex-gpt6-history-series
claimed_at: 2026-10-19T21:20:00Z
created_at: 2026-10-19T21:20:00Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s20
  - docs/videos/curio-s21
  - docs/videos/curio-s22
  - docs/videos/curio-s24
  - docs/videos/curio-s25
  - docs/videos/curio-s27
  - docs/videos/curio-s36
---

# Extend the Curio history video production queue to twenty episodes

## Why

站主在原先約十支之外要求更多歷史系列影片，並授權依建議持續製作。現有本線十三支為 S02、S03、S04、S05、S06、S07、S08、S19、S23、S26、S28、S30、S34；S01、S09、S18 另有工作者認領，不在本票重做。先增加七個各自可獨立製作的候選集，使本線有二十支的明確範圍。

## Proposed next seven

| 集數 | 暫定問題 | 查核起點與風險 |
| --- | --- | --- |
| S20 | 蒙娜麗莎失竊時，畢卡索為何被問話？ | 1911–1913 年報刊與審訊記錄；區分畢卡索、阿波里奈爾與真正竊賊。 |
| S21 | 鬱金香狂熱到底有多瘋？ | 當代成交與契約紀錄、近代經濟史研究；避免把「沒有經濟影響」說滿。 |
| S22 | 維京人何時到過北美？ | 蘭塞奧茲牧草地考古與 1021 年年輪測年論文；分開「在場年份」與首次抵達。 |
| S24 | 阿基米德真的喊過 Eureka 嗎？ | 維特魯威文本及寫作年代；傳說與實驗可行性分層。 |
| S25 | 牛頓的蘋果有打到頭嗎？ | 斯圖克利回憶與牛頓手稿；分開掉落故事與撞頭插畫。 |
| S27 | 維京人的頭盔有角嗎？ | 館藏實物、十九世紀舞台造型；不能從少數出土物概括所有戰士。 |
| S36 | 波士頓真的被糖漿淹過嗎？ | 1919 年事故報告、審訊與當代報刊；傷亡和速度等數字逐一查來源。 |

這些只是題目卡，尚未完成來源重開或腳本簽核。先挑可直接取得一手資料的一題做完整前製；若來源無法核對，保留記錄並換題。每支依 `curio-episode` 流程通過獨立讀稿、逐句史料、語音、插圖、成片與上架包關卡。

### 2026-10-19 來源可行性試查

- **S25 牛頓蘋果暫緩前製。** 在這個雲端環境，Royal Society、Newton Project、Wikisource 與 Gutenberg 原站請求均遭網路代理回覆 403，尚無法重開斯圖克利回憶錄原稿。可重開的 [Brewster 1831 年傳記固定版](https://github.com/GITenberg/The-Life-of-Sir-Isaac-Newton/blob/698dea96e3e5ed08ae46d5d693433ae7d97a6e0b/53311-0.txt#L10317-L10319) 只是較晚的二手論述，書中作者說他未找到蘋果故事的可靠根據；不能因這段話就推翻後來被找到的斯圖克利手稿，也不能用網頁轉引原稿冒充已核對的一手資料。補齊可重開的手稿或可信全篇校錄前，不寫 S25 劇本。
- **S22 維京 1021 年暫緩前製。** [《Nature》原研究 DOI](https://doi.org/10.1038/s41586-021-03972-8)、Nature 原站與 Crossref 的全文／目錄請求在此雲端遭代理回覆 403；試查 PMC、Europe PMC 亦被 403 阻擋。GitHub 以 DOI 與論文全題檢索尚未找到可固定、可重開的全文。尚不能逐項核對年輪訊號、木片數量與「1021 年在場」的推論範圍；補到原研究或可信完整校錄前，不把題目卡的年份推成「首次抵達」並不寫劇本。
- **S36 波士頓糖漿災難暫緩前製（2026-10-20）。** LOC 報紙查詢、Chronicling America、Boston Public Library、麻州官方入口、Internet Archive 與 Google Books 在此雲端均遭 CONNECT 403，未取得 1919 年當代報刊、事故報告或審訊原文；GitHub 搜尋僅見現代轉述或空 OCR 倉庫。21 死、約 150 傷、35 mph 流速及事故原因均無可重開一手根據，尚不足支撐八分鐘以上逐句核對的故事。保留題目卡，不寫企劃、劇本或生成媒體；重開條件與逐項收據見 [`curio-s36/research.md`](../../docs/videos/curio-s36/research.md)。
- **S27 維京頭盔暫緩前製（2026-10-20）。** 丹麥、挪威與英國的館藏入口、Europeana 及 1876 年首演設計稿入口在此雲端都遭 CONNECT 403，未取得可核年代的維京頭盔原件或歌劇服裝原稿。1889 年 Du Chaillu 的可重開文本把較早的有角岩畫、跨地區青銅盔與其「維京時代」敘述並列，同一文本又稱岩畫遠早於羅馬；這是十九世紀書籍跨年代並置材料的證據，不能證明維京人戴角或「1876 歌劇是唯一源頭」。1913 年 Mawer 的軍備概述沒有角，沉默也不能作全稱否定。題目卡的起源論先保留待核，不寫企劃／劇本／媒體；完整收據與重開門檻見 [`curio-s27/research.md`](../../docs/videos/curio-s27/research.md)。
- **S20 蒙娜麗莎失竊暫緩前製（2026-10-20）。** 可重開 [1913 年 Armand Dayot 編《Le musée du Louvre》原文](https://github.com/GITenberg/Le-musee-du-Louvre-tome-2-of-2_54835/blob/4a9656edddcc1fc67b169145e04766d93969c7a7/54835-0.txt#L4617-L4652)：當時書籍已把畫列為 Salon Carré 的珍寶，並說找回後觀眾更多；它不提供畢卡索／阿波里奈爾警詢、佩魯賈供述、確切逐日時間或「四根釘子」。Gallica／BnF、羅浮宮、Chronicling America、Uffizi 等當代材料入口均遭代理 CONNECT 403，GitHub 搜尋亦未找到可重開警詢或報刊原文。未滿足八分鐘逐句查核的來源門檻，不寫企劃／劇本／媒體。完整查核與恢復條件見 [`curio-s20/research.md`](../../docs/videos/curio-s20/research.md)。
- **S24 阿基米德可優先查核。** 固定版維特魯威《建築十書》[英文譯本第九書序 9–12 節](https://github.com/GITenberg/The-Ten-Books-on-Architecture_20239/blob/67fd1f31ae255b0f32efe423a950203d9b25bbe8/20239.txt#L8012-L8053) 與[拉丁原文](https://github.com/GITenberg/Vitruvii-De-architectura-libri-decem_51812/blob/78eb1eed88044d5cac42a3dd811d5806e4e04cfb/51812-0.txt#L27276-L27313) 都可重開：原文 `currens identidem graece clamabat ευρηκα ευρηκα`，接著用 `dicitur` 交代同重量金銀塊與皇冠排水比較。兩版同樣記希羅的金冠、混銀指控、浴盆溢水及奔跑呼喊。維特魯威寫作於阿基米德之後，原文是傳述而非目擊證詞；不把「有人寫他喊了」說成「可證他當場真喊了」。
- **S24 人物脈絡另有獨立傳世文本。** [普魯塔克〈馬塞勒斯傳〉固定版](https://github.com/GITenberg/Plutarch-Lives-of-the-noble-Grecians-and-Romans_674/blob/6aea7c6d83ee3596f9106d2d832d705aa4ed4620/674.txt#L19090-L19133) 提到阿基米德應希羅請求將幾何構想變成機械；該段沒有金冠與洗澡場面。它可交叉核對兩人關係的傳述脈絡，**沉默不能當成浴盆事件不存在的證明**。此書完整文本本地 SHA-256 `11a1bb9a5d5a8436f2d4d7adf3ad91ec05bb8aef850e564ce255cf9ba2fabdd1`。
- **S24 R3 前期包已過獨立盲評，語音待複聽。** R2 新讀者 13 題有 12 題「是」；`no_recap` 指出銀塊整件浸沒與取出後補水各講兩次。R3 刪除重複的 `ac045`、`ar203` 兩景，保留各一次完整說明，並讓量杯鏡頭明確畫水倒回盆緣。新的獨立讀者對 R3 劇本評為 **13／13**，史料、102 句旁白與 99 張插圖鏡頭配對通過，lint 0／0。R3 `script.md` SHA-256 `232d24e94abccafa1501a3924f86bd3f4bacacab745a75e27c489637119dd185`；R2 失敗收據已原樣存入 `narrative-r2-failed.json`。英、拉、普魯塔克三份固定來源可重開。`script` gate 只記錄既有委託下繼續配音的授權，**站主尚未親自閱讀劇本或聽過音檔**。配音實測全片 9:24.93、排除開場和片尾的正文 **8:24.10**；逐句檢查 102／102，有 7 個轉寫差異待複聽，音訊 gate 未核准。無人聲配樂已生成，帳本 US$0.08；付費插圖 0 張，依共用配額暫緩。證據見 [`verify-4.md`](../../docs/videos/curio-s24/verify-4.md)、[`verify-5.md`](../../docs/videos/curio-s24/verify-5.md)。

- **S24 R4 七句改寫後語音零旗標。** 對 R3 的七個轉寫疑點只改同七句口語，獨立讀者先盲讀確切新版劇本 **13／13**，再核英、拉、普魯塔克固定原文及畫面，來源通過；`script.md` SHA-256 `2ab08047be6dbc800ef54f02b6e9321518324f9ce8e0aaea0265430242c724af`，`video.json` SHA-256 `d3ed093b47ae63237d94f059b30cd6fcb484a13fe83b08149578e49169f28a47`，lint 0／0。Gemini 只合成 7 句、沿用 95 句；全 102 句 `check-audio` **0 旗標**、退出碼 0，實際正文 **8:25.73**。劇本及新版音檔已送站台 gate，音訊仍 **pending**，不能稱站主已親自試聽；沒有購買插圖。證據及音檔／逐句報告雜湊見 [`verify-6.md`](../../docs/videos/curio-s24/verify-6.md)。下一步：獨立全片提示詞預檢、排共享 MiniMax 生圖、逐張目視、再剪輯及品管。

- **S24 99 景提示詞獨立預檢通過。** 只改 82 個提示詞，增加希臘化時期敘拉古、奧古斯都時代羅馬作者及羅馬時期希臘作者的服飾／場景錨點，移去不實的控訴書和折屏，分開滑輪與未知齒輪；正文文字及已過零旗標的語音沒有改。獨立讀者查出並覆核 `crown-r2-021` 整頂冠沒入水下、`crown-052`／`crown-060` 各自明寫滿水起點後，對確切 `video.json` SHA-256 `59624d323f19dc99bb04de6ded3e2c118b00dd11c7bf0727cfc37fae710302d7` 判 **PASS**，lint 0／0；三輪 99 張 MiniMax 插圖上限約 US$4.01，加已付配樂約 US$4.09。**付費圖仍 0 張**。依 [`visual-preflight-r1.md`](../../docs/videos/curio-s24/visual-preflight-r1.md)，下一步排共享配額生圖及逐張原尺寸目視。

固定文本本地重開 SHA-256：S24 英譯 `7daafe23aeef2377fe9a99bc285c5dfc0673440487ab43f78387312b6799304d`、拉丁本 `b4fce89b0c304c7d1f26b299bf2dfcddbab8529c883f43ad1e75fae564daa861`；S25 Brewster 二手傳記 `ded5b6a706615f48b156dbf9f28ab18ac32edb32e16d25fedf1957eccbb94466`。

## Definition of done

- [ ] 七題各有來源可重開的研究或明確停拍理由，避免照候選題卡直接旁白。
- [ ] 可製作的各集有獨立劇本、來源對照、盲讀及真實媒體品質記錄。
- [ ] 完成影片有 1080p 成片、字幕、封面、QA 和 Private 上架包；影片公開上架由站主另行操作。

## How to verify

逐集檢查研究中引用的原文、`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs status --slug <slug>` 與實際上架包；`npm run check:tasks`。
