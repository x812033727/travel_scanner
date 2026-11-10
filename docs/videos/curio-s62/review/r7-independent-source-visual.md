# S62 R7｜獨立固定史料與書面畫面覆核

2026-10-22 UTC。**HOLD：114／114 句旁白的史料與錨點通過；110 張書面插圖中 109 張通過，`s62065` 有一處明確的晝夜衝突。** 我沒有參與 R7 作者修訂，也不作敘事盲讀。本票只審凍結文字、資訊卡和提示詞；沒有生成或驗收圖片、語音或成片。

| R7 凍結檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `5941ebf974ad67a9926d0b56311389fd8f820d14d47f31b3e55f1b1eb31b3021` |
| `research.md` | `7322d7269bfaba82a78cfde904fc94a65915e01dc3e0307a9e2ed6f0e92b62cb` |
| `video.json` | `1c811dfb9561248e314f0a39a3510386a6188322521f2d1e6c403e03ab81de95` |
| `script.md` | `c638b0d28cfbf6b398cd3bb541160685403bf3936fcd1613bc958921623e4326` |
| `claims.md` | `8cac2b796808afc29fe600c758d84a046342c7a89e7520fc4dfa512b5477f5e3` |

固定來源是伽利略 1610 年出版的 *Sidereus Nuncius*，透過 Edward Stafford Carlos **1880 年英譯及編註**閱讀；[GITenberg commit `6672b6c62a0f30e9bb9b84410ef48c6698c37ea5`](https://github.com/GITenberg/The-Sidereal-Messenger-of-Galileo-Galilei--13-and-a-Part-of-the-Preface-to-Kepler-s-Dioptrics__46036/blob/6672b6c62a0f30e9bb9b84410ef48c6698c37ea5/46036-0.txt)的 raw 檔重新核對為 SHA-256 `74fc9b817b64bc33415c6a44100c30f48952bc531d380682e5f4f1a26cc56fb5`。譯者腳註、`[Sidenote:]` 和後世衛星名稱沒有被當成 1610 年作者原話。

## 史料與 R7 回呼

- 逐句讀 `video.json` 的 **114／114** 句，對照 `script.md`、`claims.md` 和固定原文 G01–G15 的適用段落。114 個場景 ID、旁白、順序逐字一致；`claims.md` 的 **134** 個固定 commit 行錨均落在 raw 檔有效行號，每句至少一錨。鏡筒、逐夜可見點數、東西方向、角距、近點消失與重現、遠星比較、最外軌道的謹慎半月試估、尚未計出各軌道及邀人續測，皆符合原文；十日及二十三日的遮擋仍明說是作者的猜測。
- R6→R7 的 `video.json` 實際只改 `s62041`、`s62042` 兩個旁白 leaf；`claims.md` 為 `s62042` 新增 G05 行錨，110 個提示詞和 4 卡未改。`s62041` 的「回到開場那夜」明示回呼開場 `s62004` 的一月九日雲天；「想核對木星是否真的走錯，卻拿不到九日的新位置」忠於作者先怕木星違反計算、盼下夜再看卻被雲阻的次序。[L1301–1309](https://github.com/GITenberg/The-Sidereal-Messenger-of-Galileo-Galilei--13-and-a-Part-of-the-Preface-to-Kepler-s-Dioptrics__46036/blob/6672b6c62a0f30e9bb9b84410ef48c6698c37ea5/46036-0.txt#L1301-L1309)不支持九日實際見到新點，R7 也沒有這樣說。
- `s62042` 只說**觀測圖**由八日跳十日，沒有說原書文字完全略過九日。八日三點全在西側的 **Fig. 2** 見 [L1294–1299](https://github.com/GITenberg/The-Sidereal-Messenger-of-Galileo-Galilei--13-and-a-Part-of-the-Preface-to-Kepler-s-Dioptrics__46036/blob/6672b6c62a0f30e9bb9b84410ef48c6698c37ea5/46036-0.txt#L1294-L1299)，九日雲阻見 L1307–1309，十日只見東側兩點的 **Fig. 3** 見 [L1311–1315](https://github.com/GITenberg/The-Sidereal-Messenger-of-Galileo-Galilei--13-and-a-Part-of-the-Preface-to-Kepler-s-Dioptrics__46036/blob/6672b6c62a0f30e9bb9b84410ef48c6698c37ea5/46036-0.txt#L1311-L1315)。G04＋G05 雙錨準確。下一句 `s62043` 才揭十日點數，沒有提前透露。

## 書面畫面：一處須修

**`s62065` 暫緩。** 旁白「十五日入夜，四個點又都在木星西側」及固定原文 [L1374–1378](https://github.com/GITenberg/The-Sidereal-Messenger-of-Galileo-Galilei--13-and-a-Part-of-the-Preface-to-Kepler-s-Dioptrics__46036/blob/6672b6c62a0f30e9bb9b84410ef48c6698c37ea5/46036-0.txt#L1374-L1378)均明確是**夜間第三時辰**。同景 `data.prompt` 卻寫「`four faint glimmers appear outside ... overcast afternoon light across his hands`」：畫面同時指示四點在窗外顯現及午後光線。這會把明確的夜間觀測畫成白日事件，屬於系列 skill 所列的「旁白說夜晚、圖畫成白天」矛盾。只須將 `s62065` 的光線改為夜光／室內燈光，並同步更新 `claims.md` 對應的書面畫面欄；旁白、錨點、卡片與其他提示詞無須為此改寫。修訂後重凍結雜湊、跑 lint、重核這一景即可。

其餘 **109／110** 個提示詞及 **4／4** 張資訊卡均按各景旁白與來源核對：一月七日東二西一、一月十日只見兩點、一月十三日西三東一、作者對最外軌道的周期試估，卡片文案均在原書界線內。插圖是單人／無字道具的卡通示意，沒有把未見星點指認為特定現代衛星、把雲夜畫作測量夜，或要求模型生成可讀原始星圖。`s62024`、`s62065`、`s62098` 若日後生成圖片，仍須逐張核實可見點數；本票沒有原生圖片。

## 可重跑檢查與範圍

- 官方 `VIDEO_WORKDIR=/tmp/curio-s62-audit-work node tools/video/cli.mjs lint --slug curio-s62 --json`：exit **0**、**0 errors／0 warnings**、114 lines、7 chapters。畫面晝夜衝突是人工語義覆核發現，lint 未報。
- 110／114 = **96.49%** 原創且互不重複的 `shot` 提示，4 卡，最多連續一張卡；`claims.md` 的提示／卡片文案逐項與 `video.json` 一致。`look` 是原樣 `cute-mystery`，音樂設定符合系列值。
- 官方 `estimateTimeline`：250 CPM 開場 **46.53 秒**、正文 **10.181 分鐘**；325 CPM 開場 **37.63 秒**、正文 **8.254 分鐘**，即使扣最後訂閱句仍 **8.171 分鐘**。這是未測 TTS 的文字估算；固定 5 秒片頭及 21 秒片尾不計入正文。
- `npm run check:tasks` exit 0（既有其他任務持有時間和範圍重疊警告）；`git diff --check` exit 0。本票沒有付費媒體、上傳或站方核准。

**結論：R7 新回呼、全部旁白與史料錨點 PASS；書面畫面總關卡因 `s62065` 單景 HOLD。** 敘事盲讀由另兩位只讀 R7 劇本的讀者獨立處理；本票不代替其結果。
