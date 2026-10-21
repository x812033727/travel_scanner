# S05 單支 Short 撰稿與無付費預檢

日期：2026-10-20。此收據只覆核 `shorts.json` 腳本、固定史料與長片已驗收關鍵影格；沒有合成 Short 語音、編碼、上傳或假設站主已核准 S05 分鏡。

## 精確輸入與工具結果

- `docs/videos/curio-s05/shorts.json` SHA-256：`e48b28a92631fc36c1d0fd321fcc39a437ce64b5d1d9259051c5f2662e5d9e76`。單支 `curio-s05-short-1`，六拍 `hook → setup → turn → proof → payoff → loop`，旁白 6 句、146 字元；第一卡「誰先上門？」6 字。沒有訂閱、按讚或點連結口播。
- 長片 `video.json` SHA-256：`361d2836d0891a6994383cafb576c8761523056ddd7840f7b748000a5777e863`；已核圖片 manifest SHA-256：`6209e55e8fa48a89c199d12348e18ae9c47f30684396825b7245e303737e7344`。六景均為既有 `shot`，原尺寸檢視並選人物靠直式畫面中線的鏡頭。
- `node tools/video/shorts/cli.mjs from-episode --slug curio-s05 --workdir /workspace/.video-work/shorts --episode-workdir /workspace/.video-work --check`：`curio-s05: 1 Shorts valid; every keyframe matches its hash`。這是零付費靜態檢查，沒有執行 `build`。

## 六拍史料界線

| 拍 | 圖片 ID／SHA-256 | 可說範圍 |
| --- | --- | --- |
| 問誰先上門 | `visit-040`／`02610cf58a1e7ab6a9ed24b0fe6cee077abc99b9ba90277f908ca9656e0d733d` | 固定 [SG35-P1] 的正文與裴注確有相反主動者；插圖只作示意。 |
| 正文三往 | `visit-063`／`6feb4f79a2904bc5aa68baba8dd1f0dcb359b99f84cf7b98ea51dbc43ac202f6` | 陳壽正文「由是先主遂詣亮，凡三往，乃見」；不加每次日期或小說情節。 |
| 引文北行 | `visit-037`／`8c324152351ee0f27d0867919e7b565e8a38000a5662d7dec0501ba94305be44` | **裴松之註引《魏略》**，劉備屯樊城，諸葛亮北行見備；不歸給正文或裴本人的肯定。 |
| 分清文本層級 | `visit-061a`／`679d9672b9034cd4d8b08304d686c9f5cc22c0bd9f2d7d19368f0b18a48aee4a` | [SG35-P1] 明分「魏略曰」與「臣松之以為」；畫中空白卷物不冒充原本或可讀引文。 |
| 裴的判斷 | `visit-070`／`3338d9e728f33f6cab8c6023d6e4b323d0f0d21d3976c662b97093763fa6b5b5` | 裴援諸葛亮〈出師表〉「三顧臣於草廬之中」，判「則非亮先詣備，明矣」；這是裴的判斷，不說成現場實證。 |
| 異說來源未知 | `visit-075`／`e5fd07a7a56c19cb5e8e8ec55032ee5ab93b332c281ff6673fe7fd7dfffdad42` | [SG35-P1] 只標引書名，沒有交代《魏略》樊城故事最早來自誰；短片回到傳話來源的提問。 |

史料連結採 `video.json.sources` 已固定的卷三十五 Git commit；說明欄明記卡通是示意畫面。`source.url` 留待長片公開後由站台填入，沒有編造未上架的影片網址。

## 後續關卡

獨立讀者先對 7 句稿精確 SHA `34a6eb07…` 做 SG35-P1 原文、文本歸屬及六張圖核查，**PASS**，並指出片尾連問兩次傳話來源重複。現稿只刪最後的重複問句、正文及六圖均未改；同一讀者對刪句後精確 SHA `e48b28a9…` 再做窄覆核，**PASS**。Short 語音與媒體 `build` 等 S34／S28 既有聲線時段清空才開始；長片 S05 分鏡仍等網站 owner 審閱，不能把本 Short 的 `--check` 當成長片成片核准。
