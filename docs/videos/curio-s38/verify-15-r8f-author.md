# S38 R8f｜三景提示詞定點採入（作者交接）

2026-10-21 00:10 UTC。**只將 `pf004/005/006` 的三句紙上候選，逐字採入 `video.json`；`STOP` 保留，未生成或核准新版圖片。** [R8e 原生退圖與帳本](verify-14-art-stop.md)及[另一位工作者的三景書面 PASS](verify-14-art-paper-independent.md)是這次窄改的依據，不代替對 R8f 精確差分的獨立史料／畫面覆核。

## 五檔凍結與結構化差分

| 創作檔 | R8f SHA-256 | 與 R8e 相比 |
| --- | --- | --- |
| `brief.md` | `fa297d70e016d88ba1a59bd92476be22eda3eefc09f36b2d08c0c82ab114643b` | 完全未改 |
| `research.md` | `f838518cf2c4ab23de91021ae6024d9431f907866c14301466ca0a06bb3ecdfe` | 完全未改 |
| `claims.md` | `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42` | 完全未改 |
| `script.md` | `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951` | 完全未改；已錄旁白不重唸 |
| `video.json` | `084ff89c7df3dbfc0c150263eec6d96c3dabf85fc1baacd864a7e40f41416616` | 僅三個 `data.prompt` 葉節點改動 |

[機器可讀完整前後字串差分](verify-15-r8f-structured-diff.json) SHA-256 `564e6372d39a9d920a83a0556abd2420818e521a4ff48a93cd3cea48965b6f92`，它把 Git 內 R8e `video.json` SHA `33eceef58a3d25414f28606b1737258b256ff8a4bd9687f739974e42c0bb12bc` 與 R8f 解析成 JSON，列出**恰好** `scenes[3].data.prompt`=`pf004`、`scenes[4].data.prompt`=`pf005`、`scenes[5].data.prompt`=`pf006`。把這三個新字串還原為舊字串後，整個解析 JSON 與 R8e 完全相同，包含 `look`、旁白、鏡位、場景順序、來源、品牌設定。三句新字串與[先前送審的紙上候選](verify-14-art-stop.md)逐字相同，沒有把 judge 風格修詞寫進單景。

`visualHash(video.json)` 由 **`14c64a52d7da49a6`** 改成 **`9dce146d046f75cf`**；`lint --slug curio-s38 --json` 為 0 error／0 warning。這個 visual hash 變動會使 R8e manifest 的整體分鏡綁定失效；舊 `pf004/005` 判退圖不可沿用為新方案 PASS，`pf006` 舊圖也不算新版圖片。`pf001/002` 自身的 prompt、鏡位、來源及已判 JPG 沒改，依工具逐景 request key 和 judge stamp 的搬移規則**應可沿用**；重開 `keyframes` 時仍須看它實際印出的 carryover 計數及 manifest 新 hash，不能只憑這句話宣稱重新核准。舊 `pf003` US$0.0035 未明 reservation 仍保留，不得補送同一不明付費請求。

## 停點與下一位獨立覆核者

私有 `/workspace/.video-work/curio-s38/STOP` **仍存在**。停前累計媒體 ledger US$0.2220，含圖片 12 take、judge 10 次、配樂 1 首及 `pf003` reservation US$0.0035，均在既定整集 US$4.58 累計上限內；沒有因本版改詞增加付費。網站手推 outline／script／audio 卡及真人試聽仍待決，本機委派記錄不能寫成網站站主核准。

請由未撰寫 R8f 的讀者，先以此版**五檔雜湊**與結構化差分覆核三景是否符合固定佩皮斯日記、相鄰旁白和 Curio 單人動作／時代提示詞規格；尤其 `pf004` 的寬景能否同時清楚保留一人、房屋和遠火，以及 `pf005` 不可把泛指讀者當成已證實的佩皮斯肖像。若差分查核 PASS，先另立付費試畫計畫、重查即時額度、ledger、網站關卡和 `STOP`；三景各最多一張第一輪原生圖及 judge，**三景 3／3 native KEEP** 才可考慮其餘景，任何退圖即停止放量。未通過前不得解除 STOP、續買圖片、配樂或稱 S38 成片已完成。

## 30–60 秒濃縮開場的後續修法

已錄 `timeline.json` 的第二章從 frame 867 開始，故第一章實長 **28.90 秒**，距 30 秒至少差 33 格。5 秒頻道片頭預設在第一章後，不能把它算入濃縮開場；也不應默默拉慢已核旁白、插入無聲空格或修改派生 timeline 來湊長。

**後續作者候選，尚未採入：**把 `pf003`「火追到什麼程度，才讓他選擇院子裡的泥土？」改寫成「**這天火已逼到塔街；它追到什麼程度，才讓他選擇院子裡的泥土？**」。[固定日記 D4a](research.md)明記 9 月 4 日火到 Tower Street，夜裡挖第二坑；加的句子提供同場時地，不預告 5 日房屋的結局。先作新的來源／敘事審稿並量實際 TTS；只有新版第一章實測 **900–1800 格**且正文仍至少 8 分鐘才採用。若採用，重新凍結劇本／主張或分鏡所需的雜湊、跑正式敘事／政策、只重錄改句、重做機器音檢和網站音訊審核，並重核畫面／分鏡綁定，最後才重新 assemble、captions、QA、上架包。這是**另一個版本的提案**，R8f 沒改這句，也沒有把 1.10 秒填進成片。

全頻道目前安裝 5 秒／150 格片頭、21 秒／630 格片尾；`cute-mystery` 解說長片未有 S38 branding pin 時由 `assemble` 預設把片頭放在第一章後。片尾最後 16 秒有兩個影片框與訂閱框，但真正可點的推薦影片及訂閱元素仍須私人上傳後在 YouTube Studio 設定；說明欄史料與頻道連結須於成片包驗收。
