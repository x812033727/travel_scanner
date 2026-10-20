# S44 語音初驗與四句清晰度修稿（2026-10-20）

這份紀錄接續 [verify-1.md](verify-1.md)。那份文件的「尚未產生媒體」描述當時狀態；本份記下其後的精確語音實驗與重新凍結版本。網站 `script` gate 仍顯示 **pending／waiting for the owner**；以下「本地委派決定」不表示網站或站主本人已核准。

## v5 旁白：生成與實測

v5 `video.json` SHA-256 `6572e05b1deb0ba86bbb7b3aea507e04ca8bc51af9af41e7432d9defd866c16c`，`script.md` SHA-256 `0b5053192d0ca3747811bb789dbde224bc83ba8307708b61f89843d075a37651`。兩位全新盲讀者對同一稿各 13/13 通過，獨立史料及文字畫面覆核詳見前一份紀錄。Jev 的**語音合成前**完整口播政策回條 `/workspace/.video-work/curio-s44/review/policy-pre-tts.json` SHA-256 `b63dd3f1c87f59ab2db67538a111c13f2ba15e1e5c0b2486c6ba8cca5f0b0330`，回報 `passed:true`、立場 0.79、建議 0.02、業配 0.04、解說片的示範項不適用。這不是成片 QA。

依使用者在本次對話的持續授權與根節點委派，寫下**本地**精確稿接受收據 `/workspace/.video-work/curio-s44/review/delegated-script-acceptance.json` SHA-256 `956ab7337b24d205986735dde144dbeaabbe1fd399665eacc3731f0b23a7dd93`，並明記網站仍 pending。TTS dry-run：Gemini Sulafat 96 請求、2,191 計費字元、服務可用。實際初錄 96/96 段，全部本輪生成，主旁白 **09:39.33**；濃縮開場約 **00:37.93**、其後故事正文 **08:43.33**、口播片尾 **00:18.07**。共用品牌動畫片頭與片尾仍未組片；長片、Short、連結都尚未產生。

`check-audio` 使用每句 Gemini 轉錄與一批 Jev 判讀，保留原稿，逐輪只對旗標補錄。下表都是完整 **96/96** 句查核；旗標存在時不可當成音訊通過。

| 輪次 | 新合成 | 逐字 | 同音／語助 | Jev 可接受 | 旗標 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 初錄 | 96 段／2,191 字元 | 71 | 10 | 5 | 10 |
| 一次定向補錄 | 10 段／213 字元 | 76 | 10 | 5 | 5 |
| 二次定向補錄 | 5 段／103 字元 | 76 | 11 | 5 | **4** |

三輪累計 111 次語音生成、2,507 計費字元；轉錄亦為 96＋10＋5 段，Jev 每輪各一次。舊版末輪主旁白約 **09:41**，`narration.wav` SHA-256 `137f7d538eb8eb5c95d0e2ed3c3bc706e1385aeede54b6cae07ca3b92fb2449d`，`timeline.json` SHA-256 `cdd7e9f1e357cf26b6c25b4b3ce16ec6a239277f6a3d7436b420b2d1b9df4dcf`，speech hash `74214d0739600efc`。末輪 `review/check.json` SHA-256 `4aa898228e25c91367420518be6729bd6eb2de57a344dbe6c9c36244c9b1fe7a`、`review/check-flags.json` SHA-256 `14dc7235f901389c32bbce735474f11d84050c91a8ae1449cd516021920d6031`。**四句仍未過音訊關卡**：`snow015` 的問／聞、`snow034` 的泵口／蚌口、`snow058` 的街泵／接縫、`snow062` 的街泵／界浜。原始逐句誤差與 Jev 分數在工作目錄，不把 ASR 分歧自動當成真人聽感結論。這個環境的 Whisper 程式可用，但模型未在本地；先前下載遭 403，無法提供可靠的獨立第二轉錄。因此停止重複補錄同字，改做窄幅清晰度修稿。

## v6 凍結版，待新稿驗證

只改 `snow015`、`snow034`、`snow058`、`snow062` 的說法，讓「街泵」說成「街上的水泵」，另把「問到」改成「查出」、把「泵口直飲」改成「直接從街上的水泵喝」。改動僅在 `video.json` 四句口播、重新產生的 `script.md` 和 `claims.md` 對應四列；畫面提示詞、資料卡、Short 取句、數字、片尾與來源 URL 均未改。前一版三檔封存於本次工作環境 `/tmp/s44-v5-audio-rewrite-archive/`。逐行原文與文字畫面**作者自查** `/tmp/s44-v6-audio-rewrite-source-visual-selfcheck.md` SHA-256 `e41382f948c56cf487a4ed9ed5df2859c3a6a606eadc470a21be68ea224f96a3`；它不充當獨立覆核。

| v6 對象 | SHA-256 |
| --- | --- |
| [video.json](video.json) | `801f0f6a7c45d004f2b318da144511cdf4a5c9b146c140f972b0b5cb3f962c84` |
| [script.md](script.md) | `8a7d10a3116a061e397490737b72e0c4ea73528953c51995cbf324f2969c6576` |
| [claims.md](claims.md) | `b111b81ef3a6a90b0430996fb3088e82bd8948082d489a93641189abde6658f4` |
| 官方新稿敘事盲讀固定題本 | `/tmp/s44-frozen-panel-v6.txt` SHA `9cfa8d1ae68e3bbe21e854421bcc8c99d92a6d1766ed654c94c9b9949ee88116` |

新稿 `lint` **0 error、1 個原有中性片尾口播 warning**，96 句估 9.6 分鐘。v5 的盲讀、政策與本地接受**不移植**到 v6；新稿須重新獲兩位來源隔離盲讀、獨立史料差分、Jev 政策、網站 script 送審，以及變動句的新語音與 0 flags 音訊關卡。即使音訊通過，網站 script 狀態也要如實記錄。**本版尚未產生任何新語音或圖片。**

## v6 獨立盲讀未過，v7 精確修稿待查

兩名不帶前版意見的全新讀者查同版 v6，A 的報告 `/tmp/s44-v6-blind-a.md` 在必答 12 題中 **10 yes／2 no**（`chapters_link`、`no_recap`），C 的報告 `/tmp/s44-v6-blind-c.md` **10 yes／2 no**（`chapters_link`、`payoffs`）。兩人都覺得開場 `snow007→008` 與理事會 `snow039→040` 銜接太慢；C 另指出登記的 `snow050→053` 伏筆以另一問句結束，A 指出正文最後和口播片尾第一句重講水路結論。兩人的作業說明均表示讀了 brief／script／video／寫作規範，**不稱為只讀 narrative panel 的證據**。v6 不通過敘事關卡，未要求新語音、插圖或政策判讀。

v7 只在 `snow008/040/041/044/053/054/snow999a` 七句做敘事修補：第二章第一句先接回拆把手的時序；理事會章首直接交代隔日拆把手、後一句說明史諾原文的限制；濟貧院飲水對照以有界線的解釋收束；章內新增兩個立即回收的短疑問維持鉤子密度；口播片尾回到標題的「已先下降／後續效果仍難判」。現有插圖提示詞、資料卡與媒體 clip ID 不變；Short 的 setup 鏡頭由 snow041 改取 snow040 的新版同句旁白，其餘七鏡不動，8/8 仍和長片逐字相同。調整兩個理事會 payoff ID，新增兩個短 loop，合計 20 組。來源文件另替 `snow015` 加上原本缺的 P03 訪查錨，替 1855 地圖的九月三十日端點補上 Snow 原版地圖圖註 L225–231。作者逐行來源／畫面自查 `/tmp/s44-v7-source-visual-selfcheck.md` SHA-256 `7a997fafb1e064e678ecde62b9288bac916a3b43962e59322990f9d09f68775f`；仍須獨立複核。

| v7 凍結對象 | SHA-256 |
| --- | --- |
| [video.json](video.json) | `6c109b30b2c929f16a4a2d3b5c24906a9b3372d5d964768af6507cb70335675c` |
| [script.md](script.md) | `35613826c22da36f83849ea1925eaab0863ddeafde7ad9fb548eda07280925db` |
| [claims.md](claims.md) | `0a8723920d369e097a91aa74c566481e33d3d26e10258f92a86075f1bbdc17d6` |
| [research.md](research.md) | `bac25df283524caf7bcb85c7a4ddd8b63cfabcc9c2cdc27ed2b7f9e879510c53` |
| [shorts.json](shorts.json) | `e02cebf91db594ebea769df122db7b92a2df5ccb835ddab17fa431301ce0cd16` |
| 官方盲讀固定題本 | `/tmp/s44-frozen-panel-v7.txt` SHA `a1b30251e98216ed8ea47d904c3551aa0b26da9c4a222da373ec72cb2e2dc020` |

v7 `lint` **0 error、1 個中性片尾口播訂閱警告**，新增的中段疑問使 open-loop cadence 警告回到 0，96 句估 9.8 分鐘。這仍是稿面估算。根節點獨立覆核 Snow 原文、v6→v7 七句史實差分、相關畫面文字、地圖日期和來源錨，於上述精確四檔 SHA **PASS**；收據 `/tmp/s44-v7-root-independent-source-visual.md` SHA-256 `cc18f06fef6a14341217fb2efe4fa7c72859a60bbbb4d77876fe8fed04da45e0`。這不等於敘事盲讀、實際插圖驗收、音訊或網站核准。

v7 的兩位精確盲讀、Jev 政策、網站 script 送審、新合成及音訊 0 flag 均待完成。政策一次性請求已備妥於 `/tmp/s44-v7-policy.mjs` SHA-256 `a7d67fa9e7bd1e45aff2e7d33ab6e9cab6b9d80d92f91fa0a632e268e9dbedab`，**尚未送出**。v5→v7 語音差分清單 `/tmp/s44-v7-tts-retake-plan.json` SHA-256 `a090da5f8e1692def12a19bbc3fd260e44e8e6ebf8412371e42a98793d96fecd`：96 句中 11 句字稿有變，預期 85 句可由快取重用，仍以正式 TTS dry-run 為準。v5 舊音訊屬舊 speech hash，**不能用來宣稱 v7 已有合格旁白**。付費插圖 0 張。

## v7 關卡、音訊實測及 v8 窄幅修稿

兩位新的獨立讀者只以 v7 精確稿和正式敘事題本判斷，各 **13/13 yes**：原報告 `/tmp/s44-v7-blind-a.md` SHA `9ae90627aad576ee2f846f52bacb62408083b91a0709a69e1476302461744802`、`/tmp/s44-v7-blind-b.md` SHA `36f10f638fdf8bd321d9659608f44efc94f814a5ea489d0fff094152127f1f43`。原判斷整理成工具要求的逐句引用格式，正規化過程不算第三位盲讀者；合併收據 `/tmp/s44-v7-formal-narrative-receipt.json` SHA `37d74e3f638230ed23b4633f45532977a153fa687de6be356b479b48ac16d187`，正式 `review/narrative.json` SHA `bb7a67857f8e476cde512fb4d1cb63d37617c1e21d6e9a7ed68abea69652fdb3`，`readers: 2`、`passed: true`。同版 `review/script-check.json` SHA `b9e1c72e16a559496db73e052ce5dde7067614d79551ded9495af2870699e8fa`。Jev 政策只送一次，`policy-pre-tts-v7.json` SHA `1da45c589b7fcf0b3506031ca001b65abcc91d0c03427807df8f6320741e76b4`，`passed: true`、立場 0.79、建議 0.02、業配 0.04。網站 `review-push --report-only` 成功，`--gate script` 提交 v7 仍 **pending**，`review-pull` 顯示 `waiting for the owner` exit 3；不是網站核准。

v7 TTS dry-run 報 96 句中 11 句需新合成、85 句快取可重用；實作亦是 **11 新／85 重用、305 計費字元**。首輪完整音訊檢查 96/96，有 3 旗標（snow015/053/058）；各補錄一次共 3 句／80 字元後仍 3 旗標；第三次各補錄 3 句／80 字元後 snow015 通過，但 snow053/058 仍未過。故 v7 累計本次新生成 **17 段／465 計費字元**，三輪完整或增量檢查均涵蓋 96/96，Jev 各一次。末輪 78 逐字、11 同音或語助、5 Jev 接受、**2 旗標**；`check.json` 封存 `/tmp/s44-v7-audio-final/check.json` SHA `c2129f9e966307960032a7a376bfdf48d593e9c561d32fb2d5d2dc413b3ade44`，`check-flags.json` SHA `908ce9f219339635dcdc228aec6bcffff52071d48589d8240b3666d0660d1e95`。末輪 `timeline.json` SHA `43669884282a2e4ab58f837a31dc30b3901f642a3af0fc6b70ca101c8e485f6c`，`narration.wav` SHA `009331132a48d92a3cb83abf7739289a90cead0ae8d23395882ed091887e663a`；實測總旁白 **09:52.97**、濃縮開場 **00:37.93**、其後正文 **08:54.10**、片尾口播 **00:20.93**。旁白長度達標，但因兩旗標，**v7 音訊關卡未通過**，沒有繪圖。

v8 只改 snow053、snow058 的口播說法和對應兩條來源列：snow053 避開「住民／註明、街泵／接泵」的誤辨，以 Snow 的院內井、公司供水、未往布羅德街取水寫清可能的飲水解釋；snow058 把「供人喝」改「給人喝」，避免被聽成「工人喝」而暗示所有工人飲用。插圖提示詞、資料卡、片尾、Short 和伏筆 ID 均未變。v7 前稿三檔封存 `/tmp/s44-v7-audio-repair-archive/`。作者原文與畫面文字差分 `/tmp/s44-v8-audio-wording-source-visual-selfcheck.md` SHA `00d12666b1219aa2bc6407f0308791693e0195ec1d4d3794b9e3ee5a57290926`，**尚待獨立覆核**。v8 `lint` 0 error、原有片尾警告 1，無超長單景警告。v8 精確稿：`video.json` SHA `3f600bae904c32d7530c948f530486dadef680053e55171ebed3653e760be586`、`script.md` SHA `1f0cf00dae1765c69612bdc5cf9370ecf3a5b2784dac22ebc77acb84ce39fabb`、`claims.md` SHA `f58391a912f40301b0ff7acb2df5562f8bc4f191f98c3dd6109e9c978d37c389`、固定盲讀題本 `/tmp/s44-frozen-panel-v8-final.txt` SHA `e08cb812f40b2665b3bb4fc2259f30ff48704c97f1fef19869c18390f05e553c`。新稿兩位盲讀、獨立來源、政策和語音均須重驗；v7 收據不可移植。v8 尚未合成、未畫圖。

## v8 精確稿與音訊關卡通過

兩位全新盲讀者讀同一 v8 精確稿：A `/tmp/s44-v8-blind-a.md` SHA `edefb9c5e3946376f606d3683ada288690d7999c526fa3b89b255411a2816f92` 為 **12/13**，僅 `no_recap` 答否；B `/tmp/s44-v8-blind-b.md` SHA `5dd997820af2fe17b4f48ec304ca8b300227a5c251eb43b0e55c8b45af4b2f46` 為 **13/13**。依系列雙讀規則，同一題兩人都答否才不過；保留分歧，不為單一否定再改稿。正式合併敘事 `review/narrative.json` SHA `6fb38b7f281a0561f6781a328b2edff1b897c9bbf88306749b14f58cb5c5c024`，`readers: 2`、`passed: true`；保留原讀稿與格式整理界線的收據 `/tmp/s44-v8-formal-narrative-receipt.json` SHA `5512e6b6bf6cf48d2ee435d939605d008eb2fd964800a4a3d1f6bd02ea564fb1`。根節點另查 Snow 原文兩句與原畫面文字，獨立差分 **PASS**，`/tmp/s44-v8-root-independent-source-visual.md` SHA `126e044d17c877bb32fe6100b863090ed22ce75ea3be1c862e47456e22be769a`。同版 `review/script-check.json` SHA `21001f2ec56669cec6f7c4ce07d0f146f8f4009e22fd8afd8d0515e7e2bb1fa0`。

Jev v8 全口播政策只送一次，`policy-pre-tts-v8.json` SHA `bd05e5262db181d00701ce5f12f3b84bc37e1b4ee685e4d641e626e6f020ac94`，`passed: true`、立場 0.79、建議 0.02、業配 0.04。依使用者持續授權與本地委派，v8 精確稿決定收據 `delegated-script-acceptance-v8.json` SHA `57df0d1bf6a2632365e9edad4ebc90bd7f0ab035c3152def5765bbee0bb9fa5a`，明寫網站**尚未核准**。網站 v8 `script`、`audio` 兩關都已推送；各自 `review-pull` 仍為 `waiting for the owner` exit 3，因此只稱 **pending**。

v8 TTS dry-run 報 96 句、僅 snow053/snow058 兩句需合成，63 計費字元；實作 **2 新／94 快取重用**。`check-audio` 查 **96/96**：80 逐字、11 同音或語助、5 Jev 接受、**0 旗標**，本輪只轉錄兩句、0 次新 Jev 歧義判讀。`review/check.json` SHA `d63ba0333f3c0546e4b336cce31405913831b5bb900971e2f09aea7e4e3f66cc`，`review/check-flags.json` SHA `a2906d32836a615dd313fbbdd70bc5bf7b5ba72aed6a0910a2bc1cfb5489210b`。實測 `timeline.json` SHA `74b09419c4d5bfe3a84f660d2abaa6573966a2f0c7c12d3f778116e305cdf730`、`narration.wav` SHA `c0d2f37f3145367c21d298c286c9229b4eda773872836692547181b565df2c48`、speech hash `bddbe0e15d4b011e`；總旁白 **09:53.93**、濃縮開場 **00:37.93**、其後正文 **08:55.07**、片尾口播 **00:20.93**。旁白及時長關卡通過，品牌動畫及實際插圖仍待合成。`keyframes --shot snow001,snow067,snow089 --takes 1 --dry-run`：三張 1K 原圖上限約 **US$0.04**，目前圖片花費 **US$0**；試畫交根節點執行與原尺寸驗收後再決定擴量。

## v8 首輪三景原圖失敗與 v9 提示詞修補

v8 第一輪 `keyframes --shot snow001,snow067,snow089 --takes 1` 產生三張 1K 圖，圖片帳本 **US$0.04**，manifest SHA `1a2047f787f697f904feecc862e13321a0578888a14185a76df3339679f00906`。根節點以原尺寸驗收 **KEEP 0/3**，完整收據 `/tmp/s44-v8-native-pilot.md` SHA `5ef18f7de54dcd27c2e2a91bb8f0b30e8d3ecbd4bc1ce486f4522494dfcb641a`：snow001 水變不透明亮黃、街泵變現代水龍頭；snow067 變現代東亞街道、紅容器與疑似機動車；snow089 雖機器評 10/10，人物卻站進井裡，和井外查看井壁的意圖矛盾。**首輪三張均不可用**，不能據機器分數開畫全片。

v9 限定只修這三景的 `data.prompt`：snow001 明寫透明無色杯水、鑄鐵長桿街泵、1854 年倫敦石板與喬治亞磚屋；snow067 明寫馬拉木車、木箱內直立軟木塞玻璃水瓶及同年代磚街；snow089 明寫成人站在井口**外**的鋪石上、身體在井沿上方看完整磚壁，僅用十九世紀中葉而不杜撰開井日期。只用正向物件和位置，不改 `look`，不用負面提示詞或畫風詞。作者對 Snow 原文 P02、P09、P13 的逐景文字畫面差分 `/tmp/s44-v9-prompt-source-visual-selfcheck.md` SHA `b027e030bcc7d401f9720e43973261f4a879b6337859404d0e5c40099e954523`；馬、木箱、軟木塞及工作者外觀屬插畫佈景，史諾未逐項描述，不當成檔案證據。v8 舊 `video.json` 封存 `/tmp/s44-v8-prompt-repair-archive/video.json`。

v9 `video.json` SHA **`7f4630de14c2b6e227e1fed713260e2795eba126415fa36f54a803a64535577a`**；生成的 `script.md` SHA 仍 **`1f0cf00dae1765c69612bdc5cf9370ecf3a5b2784dac22ebc77acb84ce39fabb`**，`claims.md`、`shorts.json` 也未變。精確 JSON 比對僅 snow001/067/089 三個提示詞不同；`narrativeHash` `af5acbd3dfaf6604`、speech hash `bddbe0e15d4b011e` 不變，v8 的**口播**盲讀、政策與 0 旗標音訊證據仍適用。`lint` 0 error、原有中性片尾 warning 1。v9 三景一試 dry-run：1K 原圖，新費用上限約 **US$0.04**；v9 尚未送出付費試畫，累計圖片花費仍 **US$0.04**。

網站 v8 `script` 與 `audio` 均仍 **pending**，從未有網站核准可宣稱失效。劇本檔雜湊與聲音雜湊沒變，但網站 v8 劇本預覽旁的三景畫面提示詞是舊版；待 v9 原圖驗收後須循正式流程更新預覽。首輪插圖 manifest 與任何後續分鏡決定不可套用到新提示詞；目前也沒有分鏡或成片核准。此處不執行網站重送、付費 v9 圖片或全 83 張生成。

## v9 修補試畫原圖驗收：S44 圖片硬停

根節點另以 Snow 原文逐字核對 v9 三個提示詞及保留畫面，獨立文字覆核 **PASS**：`/tmp/s44-v9-root-independent-source-visual.md` SHA-256 `bf0b1dc6c0d2f563cf60b7b1cb986fc608f6db965dfb4b00bc1b5d6f863ef0ff`。這僅核對要求畫什麼；生成後實圖另依原尺寸判斷。

v9 凍結 `video.json` SHA `7f4630de14c2b6e227e1fed713260e2795eba126415fa36f54a803a64535577a`，執行限定的 `keyframes --shot snow001,snow067,snow089 --takes 1`。本輪三張 1K 圖花 **US$0.04**，與 v8 首輪合計 **US$0.08**；本輪 manifest SHA `2eb0addd12253c7615f7927f42d0ed399d877386101f57a1bb3877470bdd519c`。根節點看原尺寸而非只看機器分數，收據 `/tmp/s44-v9-native-pilot-stop.md` SHA `e0d2ed4d8e1903b457e0e0e81a16a14411a4df7934f925bad0c72ffc90cb3c2f`：

| 景 | 原圖 SHA-256 | 原尺寸決定 |
| --- | --- | --- |
| snow001 | trim `f51517fc9bf2733c072e17fb6240ede7e45b9c8bcce871da66ef8cfdb59edfe0` | **KEEP**：舊式街泵、清澈杯水與醫生的概念畫面可用。 |
| snow067 | original `1f3bafce20224b58024b0c663ff8d8d5fa0e38f5cc4bf8464850435d078b991b` | **FAIL**：倫敦背景近寫實，馬車為 2D，司機消失；混合畫風不符系列。 |
| snow089 | original `4e875bd00331b600690e77cd4c69608ad160624904f18c8783abd1b1e69ac96b` | **FAIL**：磚地背景近寫實、人為 2D，深井變淺坑，工人跪地且沒有檢視井壁。 |

**v9 原圖 KEEP 1/3**，低於預先設定的 **2/3** 修補試畫門檻。**S44 付費插圖硬停**：不再買剩餘約 80 景或再重畫這三景，也不做 S44 分鏡、配樂、組片、上傳包或宣稱有成片。此結果是 MiniMax 實圖不能維持要求的史實訊息和系列畫風，並非權杖或語音工具未配對。v9 劇本 `script.md` SHA `1f0cf00dae1765c69612bdc5cf9370ecf3a5b2784dac22ebc77acb84ce39fabb`、speech hash `bddbe0e15d4b011e` 未變；已完成的來源查核、96/96 零旗標旁白與實測正文 8:55.07 仍可作為將來改路線的素材。網站 `script`、`audio` 尚為 **pending**，v8 網站畫面預覽仍是舊提示詞；未送 v9 網站更新，更沒有任何網站分鏡或成片核准。**沒有最終 MP4、上傳包、YouTube 網址或可點的 Studio 連結。**
