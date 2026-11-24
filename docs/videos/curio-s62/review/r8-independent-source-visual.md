# S62 R8｜獨立固定史料與書面畫面重驗

2026-10-22 UTC。**PASS：R7 唯一暫緩的 `s62065` 晝夜衝突已修；R8 的 110／110 張書面插圖與 4／4 張資訊卡通過。** 這是凍結文字與提示詞審查，不是敘事盲讀，也未生成或驗收圖片、語音或成片。

| R8 凍結檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `5941ebf974ad67a9926d0b56311389fd8f820d14d47f31b3e55f1b1eb31b3021` |
| `research.md` | `7322d7269bfaba82a78cfde904fc94a65915e01dc3e0307a9e2ed6f0e92b62cb` |
| `video.json` | `c9f249ab7210fa4fb2cf2ac5206c57735ee19efcf0e846414bcfc06bb0745ace` |
| `script.md` | `c638b0d28cfbf6b398cd3bb541160685403bf3936fcd1613bc958921623e4326` |
| `claims.md` | `50f4b272576e90e3a172fd996fc27995223cd32cf0163264308109e6a3833c73` |

## 單景修復與史料界線

- 固定來源仍是 Galileo 1610 年出版的 *Sidereus Nuncius*，透過 Edward Stafford Carlos **1880 年英譯及編註**閱讀；[GITenberg 固定 commit `6672b6c62a0f30e9bb9b84410ef48c6698c37ea5`](https://github.com/GITenberg/The-Sidereal-Messenger-of-Galileo-Galilei--13-and-a-Part-of-the-Preface-to-Kepler-s-Dioptrics__46036/blob/6672b6c62a0f30e9bb9b84410ef48c6698c37ea5/46036-0.txt)的本機 raw SHA-256 重驗為 `74fc9b817b64bc33415c6a44100c30f48952bc531d380682e5f4f1a26cc56fb5`。譯者腳註、`[Sidenote:]` 與後世衛星名詞不冒稱 1610 年觀測者原話。
- [固定原文 L1374–1378](https://github.com/GITenberg/The-Sidereal-Messenger-of-Galileo-Galilei--13-and-a-Part-of-the-Preface-to-Kepler-s-Dioptrics__46036/blob/6672b6c62a0f30e9bb9b84410ef48c6698c37ea5/46036-0.txt#L1374-L1378)寫 **Jan. 15, third hour of the night**，四點全在木星西側；`s62065` 旁白「十五日入夜，四個點又都在木星西側」符合。新 `data.prompt` 寫 `soft candlelight on his hands, dark winter night beyond the window`，不再指示午後光線；四個窗外淡光點與當晚可見點數一致。燭光和筆記本是卡通示意，沒有聲稱它們是當年實物或原始觀測圖。
- R7 [獨立史料／畫面票](r7-independent-source-visual.md)已核對 114／114 句史料與行錨、109／110 個其餘提示詞及四張卡；其唯一 HOLD 是上述晝夜衝突。本次逐項查看全部 110 個提示詞及四卡，並以 R7 Git 版本作遞迴逐葉比較：`video.json` **只改 `scenes[64].data.prompt` 一個 leaf**；反向填回舊提示詞精確還原 R7 完整 JSON 位元組與 SHA `1c811dfb9561248e314f0a39a3510386a6188322521f2d1e6c403e03ab81de95`，正向重播亦精確得到 R8。`claims.md` **只改 `s62065` 畫面欄一列**；反向替換精確還原 R7 完整檔 SHA `8cac2b796808afc29fe600c758d84a046342c7a89e7520fc4dfa512b5477f5e3`。旁白、來源錨、其餘提示、卡、排序、`script.md` 均未改，故 R7 的逐句史料結論仍適用。

## 對齊與關卡

- 獨立逐項比對 `video.json`、`script.md`、`claims.md`：**114／114** 個 ID、旁白、順序同字；**110／110** 個 `shot` 提示與主張表同字且互不重複；**4／4** 張資訊卡標題／副文與主張表一致。主張表共 **134** 個來源行錨，皆指向同一固定 commit 的有效 raw 行號，每句至少一錨。四卡 `s62026`（一月七日東二西一）、`s62044`（一月十日只見兩點）、`s62060`（一月十三日西三東一）、`s62105`（最外側點的謹慎周期試估）與固定原文相合。
- 書面插圖 **110／114 = 96.49%**，其餘四卡最多連續一張；`look.preset` 是 `cute-mystery`。官方 `VIDEO_WORKDIR=/tmp/curio-s62-r8-audit-work node tools/video/cli.mjs lint --slug curio-s62 --json`：exit **0**，**0 errors、0 warnings**、114 lines、7 chapters。這項 lint 本身不能發現晝夜語義衝突，本票以原文與提示詞另行重驗。

**結論：R8 獨立固定史料承接與書面畫面 PASS。** `s62024`、`s62065`、`s62098` 若日後生成圖片，仍須看實圖核實可見點數；本票不替代兩位全新讀者對同一 R8 劇本的正式 13 題敘事盲讀，亦不構成 TTS、付費插圖、配樂或上傳授權。
