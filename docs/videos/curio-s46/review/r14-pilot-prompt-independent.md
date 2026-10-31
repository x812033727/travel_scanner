# S46 R14｜三景修訂提示詞獨立來源與書面畫面覆核

2026-10-20 UTC。由未撰寫三景提示詞的覆核者，比對[提示詞修訂](r14-pilot-prompt-repair.md)、原生圖首輪退件與固定的 Blackwell 1895 年自傳。**史料差分 PASS／書面畫面差分 PASS**；此判定僅准第二輪同三景試畫，並不表示生成圖、全片插畫或成片已過關。

| 精確檔案 | SHA-256 |
| --- | --- |
| 固定原書 `/tmp/curio-s48-blackwell-primary/65496-0.txt` | `b52caf559d763349953fe31101016cfb2d68662f152c28a564b6a6b93cac8ec6` |
| `brief.md` | `464c142a08b419cb1f30c6235629de7714589476d19c3b83a9f26cd04586c8f7` |
| `research.md` | `605e33a88488746102c4658f73462a3c906ba1ec67b8e0b1040eee2ed6ec50c9` |
| `claims.md` | `3bb23f35174a424e1f6981cd70926491edb521c758b562bb9a499d19298cfbe8` |
| `script.md` | `d5d01d3c96327060df9e7531aba796af45bedeaa25b8124c5993de528f7a8e40` |
| 修訂後 `video.json` | `790f04b477f0ad4c91f41e3e089e3c5c486addda36822140b0e2d85167f9f0a4` |

`git diff` 顯示只有 `bkw002/006/007` 三個 `data.prompt` 欄位更動，各一行；腳本、主張、音訊及其他場景均未改。原書是 [GITenberg 固定提交](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt)，屬自傳與書中信件轉錄，未核原始信件或場地照片。

| 景 | 原書與旁白 | 修訂提示詞差分裁決 |
| --- | --- | --- |
| `bkw002` | [P06 L2153–2177](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2153-L2177)記院長 1847-10-20 回信、附學生決議；旁白只說她拿著它，尚不知結果。 | 二十多歲成年女性、1840 年代長袖長裙與封好的**空白**信封，針對首圖人物衣裝及平紙問題；信封樣式、三角封舌和木桌只作時代卡通示意，不能指認為原信實物。圖面不顯示決議內容或票數。PASS。 |
| `bkw006` | [P10 L2361–2411](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2361-L2411)記被請暫離部分演示、致信教授、在前室等教授向全班讀信，再進講堂。 | 廣景從醫學院講堂朝開門處拍一位門外等候的成年女性，符合旁白懸念；弧形木長椅只是「amphitheatre」的示意佈景，非原教室還原。沒有畫手術、解剖、教授或同學動作。PASS。 |
| `bkw007` | [P13 L2657–2674](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2657-L2674)記床頭診療卡停填，原先卡在各病床床頭。 | 簡單病房、成年女性、床頭**空白**卡符合停填問題；灰泥牆、木床及卡夾是示意佈景，並非具證據的 Blockley 病房實景。沒有電子設備、可讀診療資料、病患苦難或醫療行為。PASS。 |

上表 P13 連結與 `research.md` 一致；提示詞沒有把自傳所述改成現代醫療建議或原物復刻。按[預定方案](r14-art-pilot-plan.md)，目前僅可對這三景各付費重畫一次，逐張以原生尺寸驗收。第二輪至少 **2/3 KEEP** 才能進入全片插畫；若低於門檻，即停此付費插圖方案。`git diff --check -- docs/videos/curio-s46/video.json` 通過。
