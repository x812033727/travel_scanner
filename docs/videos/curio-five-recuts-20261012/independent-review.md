# 五支四語新版片頭：獨立覆核

日期：2026-10-12（Asia/Taipei）。覆核者：Codex independent_review；未撰寫本次片頭或 speech runner。只讀取原始來源；本次覆核沒有付費呼叫、伺服器變更、上傳或發布。

## 最新成片抽查狀態

以下通過僅代表明列的有限靜態畫面抽查。五支均未在本紀錄宣稱站主完整播放、四語聽驗、上傳、發布或 Studio 可點擊片尾連結已設定。

| 影片 | 當前狀態 | 覆核者與證據 |
| --- | --- | --- |
| H02 羅阿諾克 | 有限畫面抽查通過；最後 16 秒起點已確認 | independent_review；`curio-h02/visual-reviewed.json` |
| H01 瑪麗・賽勒斯特號 | 有限畫面抽查通過；保留既有日文正文單句例外 | independent_review；`curio-h01/visual-reviewed.json` |
| H03 通古斯 | 整合者的三張圖抽查通過；本覆核者驗證證據綁定 | Codex root；`curio-h03/visual-reviewed.json` |
| U02 五十一區 | 修正版有限畫面抽查通過；完整比較卡與最後 16 秒起點已確認 | independent_review；新 final SHA `19933d6b22373dcfcf58d18debbd5e0403672ccc12c50f1136228d2ca47cf263`、`curio-u02/visual-reviewed.json` |
| L08 麥田圈 | 整合者的四張圖抽查通過；本覆核者驗證證據綁定 | Codex root；`curio-l08/visual-reviewed.json` |

下文的初始文稿結論、舊 contact 雜湊及修復發現保留為製作歷程；當前成片狀態以上表與各片雜湊綁定紀錄為準。

## 結論與範圍

五支影片的繁中、英文、日文、韓文共 144 句，已與凍結的完整 `video.json`、`intro-editorial.md` 逐句比較。文稿可進入旁白生成；沒有把原稿的未知結局改寫成定論，也沒有新增無來源的數字。此結論是文稿與靜態程式覆核，不是旁白聽辨、成片品管或站主驗收。

覆核時發現的兩項畫面問題與一項英文歧義，整合者已修正並回讀：

1. **H02 三歲生日不可配出生嬰兒。** `intro04` 四語的 scene 已由 `farewell-newborn` 改為 `route-third-birthday`，對應日期與未證實仍在世的字卡。
2. **不可從 keyframes 第一個檔名猜交付圖。** 實際打開 `route-third-birthday-1.jpg`，它是舊嬰兒床與吉祥物候選圖，而凍結現稿已是 quote 字卡。`recut.mjs` 已改成從 `segments.ffconcat` 對應的原交付 scene 片段取中間幀，記錄片段及 PNG 雜湊，不再優先採用候選 keyframe。
3. **U02 英文代名詞與地圖。** `intro01` 已把 `when it was already visible` 改為 `when the base was already visible`，消除「照片可見的是名字」的歧義。`intro02` 四語 scene 已改用 `secret-compare-versions` 的 1998／2013 對照卡，避免抽象卡通地圖看起來像 CIA 真實地圖。

## 文稿與語言

| 影片 | 四語覆核結果與界線 |
| --- | --- |
| `curio-h02` | 人數、懷特高興、刻字與缺少十字、航程未完成、三歲生日、黃銅戒指及未知主人均與完整稿相符。日韓文沒有把殖民者失蹤改寫成已知死亡；英文也保留未知去向。開場矛盾直接，結尾回到「讀懂卻找不到人」。 |
| `curio-u02` | 1955→2013 的 58 年限定在該次解密史書；另句保留 1967 年文件，沒有宣稱名字到 2013 年才第一次出現。2005 年申請與八年等待、偵察機反光與部分通報均與正文相符。三語自然保留對解密範圍的限制。 |
| `curio-h03` | 約兩千平方公里、1908 年、19 年後抵達、坑底老樹樁均有完整稿對應。八千萬棵以追問呈現，切科湖以仍有爭論的線索呈現；四語沒有把湖說成已證實撞擊坑。日韓文專業詞略正式但意義清楚。 |
| `curio-l08` | 1991 年、67／62 歲、記者看著製作、研究者誤判、工具與後來複雜化均保留來源範圍。沒有把所有國家的麥田圈都歸給兩人，也沒有把公開的動機收斂成唯一答案。結尾問題由正文兩種動機來源回收。 |
| `curio-h01` | 1872 年、十人、半年糧水、小艇失蹤、劍上疑似血跡被化驗否定、1701 桶中九桶空桶均相符。英文 alcohol、日文アルコール與韓文알코올 통保留工業酒精意義；新片頭不採用正文較確定的拖艇斷繩結論。 |

7–8 句的結構有具體事件與問句，沒有唸章節目錄或在片頭堆訂閱呼籲。30–60 秒、發音與四語逐句空白長度仍以合成實測為準，不能由文字覆核代替。

原始正文 H01 的 `answer-towed-boat`、`answer-rope-parts`、`answer-big` 敘事確定度偏高；U02 的原標題及正文部分「名字才印上文件」也比新片頭的限定寬。本次沒有修改原正文，亦不把新片頭覆核當作對全部既有正文的重新背書。整合者已收到此既有範圍事項。

## 外部交叉核對

除完整來源稿外，本次獨立打開以下來源，核對重點事實；沒有依頁面未載的新資訊擴寫：

- [NPS：1590 Rescue Voyage](https://www.nps.gov/fora/learn/historyculture/1590-rescue-voyage.htm)：返航日期、兩處刻字、往 Croatoan 的航程因天候未完成。
- [National Security Archive：The Secret History of the U-2 and Area 51](https://nsarchive2.gwu.edu/NSAEBB/NSAEBB434/)：2005 年申請、2013 年較少遮蔽版本、名字及地圖。
- [NASA：115 Years Ago, The Tunguska Asteroid Impact Event](https://www.nasa.gov/history/115-years-ago-the-tunguska-asteroid-impact-event/)：1908 年、1927 年抵達、中心直立受損樹幹及後續測繪；約兩千平方公里與其 830 平方英里量級相容。
- [TIME 1991 報導的 NAU 課程存本](https://www2.nau.edu/~gaud/bio372/class/readings/circ.htm)：兩人年齡、記者見證、研究者判斷與木板／繩／帽上鐵絲工具。
- [Smithsonian：Abandoned Ship, The Mary Celeste](https://www.smithsonianmag.com/history/abandoned-ship-the-mary-celeste-174488104/)：重新開啟作交叉核對；細項主張仍逐句對回完整來源稿的 scene／claims，不把概述當作所有推論的證據。

## speech.mjs 付費與來源保護

已讀取 runner、既有 `tts/client.mjs`、`speech-journal.mjs` 及五項離線測試，獨立執行 `node --test docs/videos/curio-five-recuts-20261012/speech.test.mjs` 得到 **5 passed／0 failed**。測試以本機合成波形與注入 client 執行，沒有網路或憑證呼叫。

- cohort 限定五個 slug、四語；語音沿用凍結原稿或原配音 timeline 的 provider／voice／performance。
- 所選 cohort 在第一筆付費前先驗證；每句一筆，`attempts: 1`，不從整段失敗自動轉買逐句。
- 每筆付費前建立持久 speech journal；未知／逾時結果再次執行仍 hold。已確認且尚未記入 caller cache 的回答可由 journal 恢復；已寫入 receipt 的音檔經 SHA 與 sample count 核對後重用。
- 來源稿、lexicon、原配音 voice source 綁雜湊；每句前檢查來源未變、輸出 STOP 與 locale lease。輸出目錄經既有祖先 realpath 檢查，不可落入 repo 或指定來源根目錄。
- 每個 locale 有 bounded 字數與服務額度預檢。四語對齊取每句最長原速樣本，不拉長語速；共同長度與大於三秒的額外空白另設 gate。
- 對齊 WAV／timeline／SRT／receipt 綁 shared manifest；音訊檢查重用已確認的逐句 transcription／Jev，SRT 變更也會拒絕。`owner_listened` 與 `full_video_approved` 保留 false。

這些檢查不代表供應商已計費多少，或目前 TTS 已生成完成；實際進度由各輸出 receipt／journal 決定。本覆核沒有重新送任何請求。

## recut.mjs 完整性檢視

重新讀取改成 scene midpoint 的版本。來源正文從第二章切入，保留完整 scene；字幕同樣切除舊片頭，拒絕跨剪點的 cue，再以新片頭與品牌片頭差值平移。四語新片頭都須具有 shared manifest 與音訊檢查綁定。正文音訊在新輸出 WAV 內逐樣本 hash 對比；正文畫面優先以 encoded packet hash 對比，必要時改以 decoded frame MD5 對比。最後檢查全部畫面可解碼、總幀數、AV 長度、四語 WAV 精確樣本數、響度／峰值及來源前後 SHA。

未發現阻擋目前隔離輸出路徑的靜態完整性問題。這是程式閱讀結論；尚不能把未執行的 `qa.json` 結果標成通過。字幕文字保留、正文不重編码的承諾，須由每支實際報告支持。成片仍需確認新片頭畫面、剪接處與片尾，YouTube 可點擊片尾連結必須由 Studio 設定，影片內圖案不等於連結已啟用。

## 覆核版本

- `intro-specs.json` SHA-256：`bf69b87b95ae44a1a07189a2ca949d3368a5b3fee79cba8a7f20d7a79600fbb7`
- `speech.mjs` SHA-256：`82da7582f5c366970089fe4b37062b7b15870830c1b7edabbf6252c724dc6c2c`
- `speech.test.mjs` SHA-256：`197bac72a9fa613d44e5774bd8f4e8b1f1e620705861712a619b3d79be118b93`
- `recut.mjs` 檢視版本 SHA-256：`70951c21b8f718bb9d72e0d6fe8c10de37398b936ee295e29c459e1e113d1bc0`

凍結完整稿位於 `C:/Users/x8120/mokaair-work/curio-five-recuts-20261012/sources/<slug>/video.json`：

| slug | SHA-256 |
| --- | --- |
| curio-h02 | `4dfe4d73dd458323949542ba5c22cd68a7838cbdc237b36543b07ea18620322e` |
| curio-u02 | `6c715331e64bf389f964aa16cdc312e88e141ec18acce15d5fea4a3c23d9a568` |
| curio-h03 | `a7e17af3914bedfbf1327219ef646a59a1625a26ac537914e1ea6d2a509afed6` |
| curio-l08 | `4f8d24e5395eb67d249735b0122c7962e26fd71a4fc07f38f3a2dbeed651db0c` |
| curio-h01 | `1f127829b3a0b5e86c74647e4ca7fcdcbfc1c6889c75de30148e7d2dd27fc796` |

## 合成後逐句第二意見

同日追加。使用本機 `Systran/faster-whisper-small` snapshot `536b0662742c02347bc0e980a01041f333bce120`，CPU／int8／beam size 5、`HF_HUB_OFFLINE=1`、`HF_HUB_DISABLE_TELEMETRY=1`。清除 `VIDEO_SECOND_OPINION_HINTS`；辨識器沒有收到預期文稿。繁中僅沿用 helper 固定的「以下是繁體中文的句子。」語言格式指示。此處是獨立 ASR 與語音文字分析，不是站主聽驗。

每份證據位於外部輸出 `<slug>/intro/<locale>/independent-review-20261012/`，含原始 stdout／stderr、音檔與模型檔 SHA、script SHA、原檢查 SHA 及 `evidence.json`。需要重錄者另保存舊 WAV 與 `original-check.json`。本覆核者沒有改寫原 `check.json`、片頭規格或現用音檔，也沒有呼叫付費服務。

| 影片／語言／句 | 第二意見與判定 |
| --- | --- |
| U02／ja／intro02 | Whisper 認出「計画史」；「乗りました／載りました」同讀のりました，數字相同。支持限定該 WAV 的正字法誤報解除。 |
| U02／ja／intro05 | 「航空／高空」同讀こうくう。支持限定該 WAV 的同音表記解除。 |
| U02／ja／intro06 | 「計画士／計画史」同讀けいかくし；第二 ASR 的非標準詞「塩盤」是えんばん同音表記，第一 ASR 已正確認出円盤。支持限定完整句及該 WAV 的解除，不增加通用同音規則。 |
| H03／en／intro04 | 第二 ASR 正確辨成 One suspicious pit；原 flags 的 Once a 是誤報。只差標點。 |
| H03／ja／intro03 | 兩份 ASR 分別得到クーリック及クリリック，都未支持稿定的クリク，不能用同音表記解除；建議限定重錄。 |
| H03／ja／intro05 | 兩份 ASR 都辨成 8000 本，原稿為八千万本；屬關鍵數字風險，必須重錄。 |
| H01／en／intro04 | 兩份 ASR 都得到 overturn，未支持原稿 overturned；建議限定重錄。 |
| L08／zh-TW／intro07 | 第一 ASR 刀哥、第二道哥；都未支持「格」的預期聲調，不冒稱完整同音。建議限定重錄或另有直接聽證後再判。 |
| L08／ja／intro05 | 「ひも／紐」「付けた／つけた」是書寫差，「野球帽／野球棒」同讀やきゅうぼう。支持限定完整句及該 WAV 的解除。 |
| L08／ko／intro07 | 第二 ASR 正確認出더그；其餘文字與原稿一致，只差標點，可精確解除。 |

H03 首輪同文字重錄仍被標記後，整合者提出下一次也是最後一次限定重錄，保持字幕正文不變，只使用下列等價 `say`。本覆核確認讀法正確：

- intro03：`十九年後、地質学者くりくがようやく現地へ。倒木をたどって隕石を探しました。`；くりく與稿定クリク同音。
- intro05：`倒れた木は、はっせんまんぼん。その数字はどこから来たのでしょう。`；はっせんまんぼん對應八千万本，即 80,000,000 棵。

核准的是保留舊修訂、原字幕及其他既有音檔的兩句發音修正；此文字覆核不預先宣告新合成通過。

## 限定修復工具的獨立檢查

`retake.test.mjs` 五項離線測試已由本覆核者執行通過：精確比對保留數值、獨立證據綁 WAV／模型、舊媒體與檢查快照、未知付費結果跨執行持續 hold，以及錯誤 WAV／其他 locale lease 在付費前拒絕。曾向作者指出 CLI 末行誤比 `speech_uncertain`，實際常數為 `video_speech_uncertain`；作者已改用匯入的 `SPEECH_UNCERTAIN`，本覆核重新讀取確認修正。

U02 的 reviewed-homophone 消費端另以隔離暫存資料測六個情境：固定證據包三句成功；修改辨識文字、slug、嵌入證據包位元、預期文字或 WAV 位元均無法解除。這些測試沒有改寫任何正式輸出；沒有加入通用的語意近似或同音字放行。

後續獨立執行 `node --test docs/videos/curio-five-recuts-20261012/prepare-h03-revision.test.mjs docs/videos/curio-five-recuts-20261012/retake.test.mjs`，得到 **8 passed／0 failed**。修訂測試涵蓋只准兩個等價 `say`、完整保留舊修訂與未變音檔、恰好兩筆待生成、阻止後續重錄、重入及已有第二次重錄時拒絕。另對實際新舊規格直接呼叫 validator，確認正確兩個 `say` 通過，改字幕數字、改成「はっせんぼん」、或多改英文均拒絕。

L08 日文固定證據包 SHA 為 `702b905940f02276660d3e91a9b3820658de72f838943b2311fb8fa323e08e05`；U02 日文包為 `7bb2df0a1f2d7c94c9683c619c5c050c8e75086a9808df3544e383730652a29e`。L08 實際消費端唯讀檢查回傳 `flags: [intro05]` 與 `resolved: [intro05]`，原報告旗標仍留存。

## L08 最後一句文字修訂

繁中 intro07 首次同文字重錄仍未清除「道格／道哥」疑慮。整合者提出最後一次單句修訂：`多年後，其中一位老先生還說，後悔把這件事告訴大家。`。已重新核對凍結完整稿的 `u597`：「他晚年說，後悔的是把這件事告訴了大家。」前文主詞為道格。新句弱化成兩人中的其中一位，沒有增加新事實，中文自然；其他語言保留道格不構成矛盾。

已讀取 `prepare-l08-revision.mjs` 並獨立執行其測試，**3 passed／0 failed**。它僅准這一處可見文字變更，驗證第一次重錄的 lineage 與尚未執行第二次重錄，保存全部舊 intro，保留其他音檔與 JA／KO 證據索引位元，只移除待修正的一句及已封存的舊繁中證據索引，重新要求共同對齊，恰好一筆待生成，並禁止後續追加重錄。本覆核批准文字等價與限定工具行為，不預先判定新音檔通過。

| 修復工具／規格 | 本次檢視 SHA-256 |
| --- | --- |
| retake.mjs | `765bb13cd6a43bd24e51c3c5165d105dc4084f72ef1723ddfe63c0330f79af44` |
| prepare-h03-revision.mjs | `a14a9e3df8a93b1f49bb310fddc03ccc875e16fb4dc4ee884619095863c33cdd` |
| h03-pronunciation-specs.json | `9ad54c2e7badc92bd9ce5c545ec22bf1c6fb99bd9b33b2a0b675c5b95d0b1685` |
| prepare-l08-revision.mjs | `3f20eaf79ec0baa473f39b6d2997267911e31d9c278b71bea8beafe0f5e3b7d8` |
| l08-wording-specs.json | `5b4c67388376b59e3977f7ae130d15e2457ecac4681700ed2740b20ad6d06821` |

## H02 實際成片的有限畫面抽查

已打開外部輸出 `curio-h02/visual-review/` 的 opening、boundaries、sources 三張 contact sheet。七句片頭所用畫面和交付來源一致；CROATOAN 字卡可讀，三歲生日正確使用文字卡，先前的嬰兒／搖籃不符已消除。片頭最後一格、品牌片頭首尾、正文首尾、新片尾首格均有完整畫面，抽查格未見黑畫面或毀損。這是圖片抽查，沒有取代完整動態播放、四語聽驗或站主驗收。

本次讀到的 `qa.json` 報告 `ok: true`、21657 畫格全部解碼、正文 encoded packet hash 相同，記錄成片 SHA 為 `1dbebfe0f224aef5cd1c5e1c9092553ff66b39678d2e9daafe5b8f0e15a2f8c0`。此處是報告讀回，沒有另跑完整編解碼。

標記「最後 17 秒」的起點抽查格仍是按讚／分享／小鈴鐺 CTA，尚未出現片尾連結的三個框；已告知整合者，精確 end-screen 起點須等 frame-level 邊界檢查後再定。其後中點及末格的兩個矩形與中間圓框清楚可見；圖案存在不代表 Studio 可點擊連結已設定。

| 抽查檔案 | SHA-256 |
| --- | --- |
| opening-01.jpg | `7a3af112b135cbc1c1de45e65583ffbeb5623645d6b4170184ff99b64217c304` |
| boundaries-01.jpg | `002d5cef8450d4d1f284e373647502b229fc592fa907f4555ad6b27da1d9dd07` |
| sources-01.jpg | `816ce0d226dfc401e94d4ebd399d3c84d6ce6c0050deb35bc0f8bab5adc2cc5d` |

## H02／U02 修正後片尾起點與 U02 畫面覆核

後續重跑 `contact-sheets.py --slug curio-h02` 及 `--slug curio-u02`，兩次均 exit 0。工具按照實際 `endscreen-setup.json` 抽格，並在抽取前後驗證成片 SHA 未變，產生新的 contact manifest。H02 的片頭 contact hash 與前次已讀取圖片相同；另外重新打開 H02 boundaries 及 U02 opening／boundaries／sources。

H02 的精確片尾連結起點改為 frame 21177（11:45.900）；U02 為 frame 22138（12:17.933）。兩者在起點、後續中點與末格都顯示兩個影片矩形與中間訂閱圓框，因此上一節的「最後 17 秒起點仍是 CTA」事項已由最後 16 秒設定解決，沒有改動成片位元。

U02 七句片頭的抽格與來源相符，航照和 1967 文件以來源字卡呈現，插畫仍明顯是卡通，不再把繪製地圖當作解密地圖證據。抽查的片頭、品牌、正文、片尾接點畫面完整，未看到黑格或毀損。保留一項非阻擋觀察：intro02 標題寫「1998 年版 vs 2013 年版」，所選的來源中點只顯示 1998 欄，右側未揭露；下方文字仍說明新公布名字與地圖。這是忠於已交付來源但未完整揭露比較欄的畫面，沒有由覆核者改圖或改片。

已將各片的實際 final SHA、contact manifest SHA、各張圖片 SHA、明確的有限抽查範圍及觀察寫入外部 `<slug>/visual-reviewed.json`。`owner_full_playback_verified`、`owner_listened`、`full_video_approved` 與 YouTube 連結驗證仍為 false。

| slug | limited review | final SHA-256 | contact manifest SHA-256 |
| --- | --- | --- | --- |
| curio-h02 | passed | `1dbebfe0f224aef5cd1c5e1c9092553ff66b39678d2e9daafe5b8f0e15a2f8c0` | `86d9af114f8870cd8cc922ff7d414e49569237cca926d8e73bdca5adc4a090c9` |
| curio-u02 | pending intro02 repair | `6b617d5d188ccc04d54b58d4e6c61144e3aac5faa8e0ed7a2402a3b48a47b409` | `bafad91bb0b192c6e69eb162960b8b75f45278f861f20375460b2cf8b26260f7` |

整合者看到上述 U02 比較卡觀察後，要求在交付前改取同一來源片段的完整揭露畫格，因此 U02 記錄已改為 `limited-still-review-pending-intro02-repair`。待選定的精確來源畫格經独立檢視並重新合成，再對新成片 hash 做畫面覆核；原音檔與字幕預定保持不變。H02 的修正後起點覆核結論不受影響。

已獨立打開 `u02-visual-probe/source-03.png` 與不同時間點的比較 contact sheet，確認同一已交付來源片段的第 316／395 格（10.533 秒）同時完整顯示兩欄，字體、下方重點及來源可讀，沒有可見淡出。重新計算 PNG SHA `becb63124329a0b7ae08294d76c7e40e8e15ba92ec84e195ec3165d0421d4b33` 與片段 SHA `9be25ef40f6d8e69c4c0a3d0ccd0d6fe4a24a2dc6a5fff0ac5beb5a7c06e01b1` 相符。核准這個精確替換畫格；U02 成片仍待新合成、QA 與新 contact 讀回。

## H01 實際成片的有限畫面抽查

已打開 H01 的 opening／boundaries／sources 三張 contact sheet，七句片頭與來源畫面相符；船、小艇吊鉤、化驗、木桶、空海面與酒館等插畫畫面完整，沒有這次 U02 發現的分欄揭露未完問題。片頭／品牌／正文／片尾接點抽格未見黑格或毀損。最後 16 秒起點 frame 21652（12:01.733）、中點及末格均顯示兩個矩形與中央訂閱圓框。

已重新計算實際 H01 `final.mp4` SHA，與 QA／contact manifest 相同：`4b6a4ba7d44437ba768c7b8eb9a974f914a908ab2b28cca8850668d2e1efff25`。Contact manifest SHA 為 `ba231311f8100f5f5fba77e649ccdfa60379fee2414906095666cd805326dadf`；各圖 SHA 與片尾設定 SHA 亦逐一讀回驗證。外部 `curio-h01/visual-reviewed.json` 記錄 `limited-still-review-passed`，不含完整播放或聽驗通過宣稱。

原日文正文註記逐字保留：`117/118 native clear + 1 exact owner-accepted mtua audio flag; preserve explicit exception, not native full PASS`。QA 報告這段原正文 PCM 未變；本次畫面覆核没有重新聽驗、解除或擴大該既有例外。

## H03 整合者畫面覆核的證據讀回

讀回 `curio-h03/visual-reviewed.json`，覆核者為 **Codex root**，狀態 `limited-still-review-passed`。整合者記錄已打開 opening／boundaries／sources 三張圖，七句新片頭與來源相符、接點未見黑格或毀損、正文第一張日期卡可讀，以及最後 16 秒起點已是片尾框。這是整合者的視覺判斷，本覆核者沒有把它改寫成第二次獨立看圖。

本覆核者另外重新計算 H03 實際成片 SHA，並驗證該 JSON 綁定的 QA、contact manifest 及三張圖位元雜湊全部相符：

| 證據 | SHA-256 |
| --- | --- |
| final.mp4 | `1d9a1991a24c7082c518543127598861f96d026cb89c3ab9ff17ced3768d30eb` |
| visual-reviewed.json | `5e1b2afc7e21d43549d3685cc17cc3a57e7344e5010c7d2ee7e7a3c23f7b67e1` |
| qa.json | `524077e81fbfeec87a52d9776e9a11739bbb70e778e0df8786c0c01947277111` |
| review-manifest.json | `08e7d563df17e8ec0d73d1b55080b85406ae3a1efbd96a6b79cd1e4526ef0436` |
| opening-01.jpg | `6cf820ff691c382253c755ab099ce5d25bb5efd8941e884c82c0977557fdb65b` |
| boundaries-01.jpg | `da8ec858a3ce4f5d1fed17a4f7cc4d88b1bef22ea3eab5912635c7b303d260c7` |
| sources-01.jpg | `652d3f3489323efa77a5b75d98fd48f2e88a0b55f825b8e45b966ecb1c8731a8` |

原紀錄中的完整播放、站主播放、站主聽驗、上傳及發布均為 false；這些界線維持不變。

## L08 整合者畫面覆核的證據讀回

讀回 `curio-l08/visual-reviewed.json`，覆核者為 **Codex root**，狀態 `limited-still-review-passed`。整合者記錄已檢視 opening 兩頁、boundaries 及 sources 共四張圖，八句片頭與來源相符、引文與照片卡完整可讀、接點及第二章標題正常，以及最後 16 秒起點已是片尾框。這些為整合者的視覺判斷，沒有冒列為本覆核者的第二次獨立看圖。

本覆核者已重新計算實際 L08 成片 SHA，並核對 QA、manifest 與四張圖 SHA 全部符合綁定：

| 證據 | SHA-256 |
| --- | --- |
| final.mp4 | `5cd592ac04bfc880e43a955bc2a40f2ffceaf82ca785492a3591fc108899aa07` |
| visual-reviewed.json | `3d0977551107d460178b75c15e4a11a797698e6b6d25e1f8e29158f4b93cb903` |
| qa.json | `829cfecd7e9fec99e8d1751f8836cfaf1aea2fd6bf946d1710664471d7fd9b56` |
| review-manifest.json | `f5e2cffa47c3e1d0918dfc751fe7a01dd50ebe2efc25527b4eb9184538ae5a8e` |
| opening-01.jpg | `b97e28e7734dda1bf6cc767c7e652a4a0760ba6327d5cd7afeefdbbc3ede969a` |
| opening-02.jpg | `aaae41f441a2b2a38284655fb25b06a61b04e31ece82c46ef5da6ea35fb0cb8e` |
| boundaries-01.jpg | `be3bb4217ceb515a24ebcba1564e9f5f30e876b00c88741fe1c963d07692fc3e` |
| sources-01.jpg | `d083476916cea03b12fa91cd2f534e98c8dcd7bd8b032a3c22c96b64be9528cf` |

原記錄的完整播放、站主播放、站主聽驗、上傳及發布仍全部為 false。

## U02 修正版最終有限畫面抽查

整合者通知重輸出與最後 16 秒設定／新 contact 完成後，本覆核者先確認 manifest 的 final SHA 已換成 `19933d6b22373dcfcf58d18debbd5e0403672ccc12c50f1136228d2ca47cf263`，再打開新 opening／boundaries／sources 三張圖。新片頭第 2 張卡完整顯示 1998／2013 兩欄，下方重點與來源仍可讀；QA 所載精確來源畫格為 316，PNG 與來源片段 SHA 都符合先前獨立核准的畫格。其餘六句畫面、片頭／品牌／正文／片尾抽查接點正常，未見黑格或毀損。

最後 16 秒的精確起點 frame 22138（12:17.933）、中點及末格都顯示完整的兩個影片矩形與中央訂閱圓框。重新計算實際新 `final.mp4`、QA、manifest、三張圖、片尾設定、來源 PNG／片段的 SHA 並核對成功；`qa.json` 讀回 `ok: true`。這是有限畫面覆核加證據綁定驗證，沒有在本步另跑完整編解碼或音訊聽驗。

`curio-u02/visual-reviewed.json` 已改為 `limited-still-review-passed`，`blocking_findings` 為空，並保留舊 final SHA 與 `intro02-comparison-card-incomplete` 的修復沿革。先前待比較卡修復的狀態已由這份綁定新成片的紀錄取代。

| 新版證據 | SHA-256 |
| --- | --- |
| final.mp4 | `19933d6b22373dcfcf58d18debbd5e0403672ccc12c50f1136228d2ca47cf263` |
| visual-reviewed.json | `e792ce60ea141790c619070eb8547d8875d64167fe6eb956145977538df54bda` |
| qa.json | `1511cfbe79897f24bd0e288f5c8827345aa880cecc7efe9d7f80a1dc46afca4a` |
| review-manifest.json | `eec95e508fe6988928be5563be813a6fcc19f1419797a64eb50f5f988e7dd907` |
| opening-01.jpg | `3b90269c1eef9eb8578f7510d39f3fc4668746355542935786d79843be814e2f` |
| boundaries-01.jpg | `b980c1daf061c84479599c46200e687a79b8c2fef4f5abe0b0ea52db4c48a3bd` |
| sources-01.jpg | `bb10f8096e19a08650504f9e17c7a2f7ccfe547513d14b842df3e87f90cad437` |

站主完整播放、站主聽驗、完整影片核准、YouTube 可點擊片尾連結與上傳／發布驗證均仍為 false；本覆核沒有改動媒體。
