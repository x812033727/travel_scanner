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
- **S24 阿基米德可優先查核。** 固定版維特魯威《建築十書》[英文譯本第九書序 9–12 節](https://github.com/GITenberg/The-Ten-Books-on-Architecture_20239/blob/67fd1f31ae255b0f32efe423a950203d9b25bbe8/20239.txt#L8012-L8053) 與[拉丁原文](https://github.com/GITenberg/Vitruvii-De-architectura-libri-decem_51812/blob/78eb1eed88044d5cac42a3dd811d5806e4e04cfb/51812-0.txt#L27276-L27313) 都可重開：原文 `currens identidem graece clamabat ευρηκα ευρηκα`，接著用 `dicitur` 交代同重量金銀塊與皇冠排水比較。兩版同樣記希羅的金冠、混銀指控、浴盆溢水及奔跑呼喊。維特魯威寫作於阿基米德之後，原文是傳述而非目擊證詞；不把「有人寫他喊了」說成「可證他當場真喊了」。
- **S24 人物脈絡另有獨立傳世文本。** [普魯塔克〈馬塞勒斯傳〉固定版](https://github.com/GITenberg/Plutarch-Lives-of-the-noble-Grecians-and-Romans_674/blob/6aea7c6d83ee3596f9106d2d832d705aa4ed4620/674.txt#L19090-L19133) 提到阿基米德應希羅請求將幾何構想變成機械；該段沒有金冠與洗澡場面。它可交叉核對兩人關係的傳述脈絡，**沉默不能當成浴盆事件不存在的證明**。此書完整文本本地 SHA-256 `11a1bb9a5d5a8436f2d4d7adf3ad91ec05bb8aef850e564ce255cf9ba2fabdd1`。
- **S24 R3 前期包已過獨立盲評。** R2 新讀者 13 題有 12 題「是」；`no_recap` 指出銀塊整件浸沒與取出後補水各講兩次。R3 刪除重複的 `ac045`、`ar203` 兩景，保留各一次完整說明，並讓量杯鏡頭明確畫水倒回盆緣。新的獨立讀者對 R3 劇本評為 **13／13**，史料、102 句旁白與 99 張插圖鏡頭配對通過，lint 0／0。R3 `script.md` SHA-256 `232d24e94abccafa1501a3924f86bd3f4bacacab745a75e27c489637119dd185`；R2 失敗收據已原樣存入 `narrative-r2-failed.json`。英、拉、普魯塔克三份固定來源可重開。估全片 9 分 12 秒、排除開場和片尾的正文 8 分 12 秒；**實測旁白時長尚待合成核對**，付費插圖依共用配額排程。

固定文本本地重開 SHA-256：S24 英譯 `7daafe23aeef2377fe9a99bc285c5dfc0673440487ab43f78387312b6799304d`、拉丁本 `b4fce89b0c304c7d1f26b299bf2dfcddbab8529c883f43ad1e75fae564daa861`；S25 Brewster 二手傳記 `ded5b6a706615f48b156dbf9f28ab18ac32edb32e16d25fedf1957eccbb94466`。

## Definition of done

- [ ] 七題各有來源可重開的研究或明確停拍理由，避免照候選題卡直接旁白。
- [ ] 可製作的各集有獨立劇本、來源對照、盲讀及真實媒體品質記錄。
- [ ] 完成影片有 1080p 成片、字幕、封面、QA 和 Private 上架包；影片公開上架由站主另行操作。

## How to verify

逐集檢查研究中引用的原文、`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs status --slug <slug>` 與實際上架包；`npm run check:tasks`。
