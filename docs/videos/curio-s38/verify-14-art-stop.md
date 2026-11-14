# S38 R8e｜續畫首輪停點與原生圖查核

2026-10-21 00:04 UTC。**STOP：新增兩張已判圖均不合格，第三張已付款下載但在 STOP 前未送 judge；不可續開整集隊列。** 本頁是目前實際媒體收據與尚未採入的修詞候選，沒有改 `video.json`、旁白或網站核准狀態。

## 開畫前綁定與額度

- 現行 `video.json` SHA-256 `33eceef58a3d25414f28606b1737258b256ff8a4bd9687f739974e42c0bb12bc`；`script.md` `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`；`claims.md` `f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`。`lint` 0 error／0 warning。[R8e 定點覆核](verify-13.md)已對這版 PASS。
- Git 內 R8d `video.json` SHA `b7aec196479b5e08656b26afc14a56035bfece3998cd90cad9707bf919ccf5ff` 的 `visualHash` `8cde515b6cc76612` 等於舊 manifest；R8e `visualHash` `14c64a52d7da49a6`。解析兩版場景，只有 `pf076/080/104` 的 prompt 改動；`pf001/002` 各自整景未變，原生檔 SHA 與舊 manifest 相符。工具實際印出 `2 of 2 drawn shots are unchanged and keep their verdicts`，新版 manifest 沿用兩張已通過的試圖，不曾再買。
- 開畫前 ledger **US$0.1915**，其中含舊 `pf003` 未有可用完成回條的 **US$0.0035 reservation**；故本次 `--shot` 明確排除 `pf003`。既有整集圖、judge、配樂累計上限 **US$4.58**。[R8d 收據](verify-12.md)記其來源，未提高上限。開畫前即時站台額度圖片 18,786／30,000、judge 20,088／30,000、配樂 62／100；額度足夠並不代表網站音訊卡核准。`review-pull --gate audio` 仍回 `waiting for the owner`；本機 `approvals.json` 的 outline／script／audio 是按站主委派作的**本機決定**，沒有任何人聲稱站主已實際聽完音檔。
- 指令原擬對 `pf004–pf111` 共 108 景各試 **1 take**，排除前兩張和 `pf003`；只跑到 `pf006` 時立刻寫入私有工作目錄的 `STOP`。原始 stdout 存 `/workspace/.video-work/curio-s38/review/r8e-first-pass-pf004-111.log`，SHA-256 `1545189e7472a649be86792a0cb767fe63e0d6c364d4c49b696a7f833766611a`。工具回 `stopped by the STOP file after 3 new keyframes`，沒有繼續買 `pf007–pf111`。

## 原生 1280×720 JPEG 判定

| 景 | 已付媒體與檔案 SHA-256 | 實際畫面、結論 |
| --- | --- | --- |
| `pf001/002` | 已有選定圖 `608203b99cd453ad7218d8c773c93ca92900997d2a9a73a1be44090cba60ccb0`、`5cff4f5806cc88ff4ffa5d78b59984f0cc5e618e6c8e998ad64cc20a4f84ea39` | **沿用原 PASS。** 兩位成年掘坑者、完整硬起司外形和土坑對上敘事。`pf002` 酒瓶口視覺含混，但瓶身直立，未見潑灑或和旁白抵觸；無須因無害卡通細節退件。 |
| `pf004` | `keyframes/pf004-1-trim.jpg` `9950577ce35c6117ada5d22f360451db6d5de3c45622cb4c00590fd92e21ef69`；image + judge **US$0.0135** | **REJECT。** Judge 7.59／10 不過：油畫式景深／模糊、非要求的全景。原圖人物幼童貌、屋頂很像東亞廟式曲檐，也不是 1666 倫敦住屋；會使「他的房子」的懸念地點誤讀。 |
| `pf005` | `keyframes/pf005-1.jpg` `cd2bad12bd19e3dc96d2a5bd0c53ba5054b032e2000889b41e89ae3bc79239d4`；image + judge **US$0.0135** | **REJECT。** Judge 9／10 仍因 style、時代細節不過；原圖中央是孩童、現代領帶衣著與辦公椅。這不是一位成年 1660 年代日記讀者。 |
| `pf006` | `keyframes/pf006-1.jpg` `6154fd9ca3b101cf2f4999937360319611e4f6b2debeee90263345fc5545a11e`；image **US$0.0035**，**0 judge** | **原生圖 REJECT，機器評審未送。** STOP 於圖片下載後、judge 前觸發；圖有孩童貌女僕、東亞式木屋頂與黑色電影畫框，不適合作 1666 年倫敦女僕珍妮的示意。圖片已在 media cache 記 ready job；新版 manifest 沒有 `pf006` 選圖，不能把它算作 judge PASS，也不再付費重生同一個不明請求。 |

本次新增 **US$0.0305**，累計 ledger **US$0.2220**：12 張 image take、10 次 judge、1 首已完成配樂，保留 `pf003` 唯一 **US$0.0035 reservation**，尚餘既定上限 US$4.3580。`pf006` 是已完成 image／待 judge 的快取，不是未核銷 reservation；其原生圖已因實質時代及年齡衝突退件。停點後只讀站台額度圖片 18,859／30,000、judge 20,161／30,000、配樂 62／100，屬跨集變動快照。此處的 STOP 因**畫質與歷史對應**，不是因額度。

## 後續僅供書面獨立覆核的修詞候選

下列完整 prompt **未寫入 `video.json`、未試畫或獲得獨立審核**。畫風仍只由原有 `look: {"preset":"cute-mystery"}` 指定，不在單景 prompt 加風格口令。三景先維持同一句旁白和同一來源；候選都只畫一位成年人做一個可見動作。倫敦建物與服飾只作內容相關的示意，不宣稱重建佩皮斯住所、其日記原件或女僕當時站的窗。

| 景 | 紙上候選 prompt | 史料及原生 KEEP 界線 |
| --- | --- | --- |
| `pf004` | `Wide shot in a walled London garden at grey evening light, one adult English householder in a plain 1660s wool coat points toward distant fire beyond low red-brick gabled rooftops, his intact house visible beside him and his face in three-quarter view` | [D5](research.md)之後才揭示房屋未燒；此景只留「會不會燒到」的懸念，不畫已毀或確定得救的結果。要有成人、完整房屋、英國磚砌斜屋頂和遠火，不能再出東亞曲檐或孩童。 |
| `pf005` | `Medium close shot at a plain oak table, one middle-aged English man with a short beard and a 1660s linen neckband reads an open page whose visible surface is blank, his other hand resting on the empty tabletop, soft candlelight against a brick wall` | [D4a、D6](research.md)未交代起司下落。讀者與空白頁只是概念，不能畫一塊已挖回的起司、可讀假日記或現代辦公家具；人物須顯然成年。 |
| `pf006` | `Medium shot at a wooden upper-floor casement of a red-brick London house before dawn, one adult household maid in a plain seventeenth-century linen coif and dark wool gown leans out and looks toward distant orange firelight, her mature face visible in profile` | [D2a](research.md)僅支持女僕珍妮叫醒佩皮斯看火，不支持她的確切年齡或那扇窗；這是成年、英國式居所的概念景，不作特定現場重建。 |

新作者若採用這些候選，須先另存新版 `video.json` 雜湊，讓未撰詞者重新核對**改動葉節點、原文來源及提示詞**，保留舊圖與帳本，重做小範圍三景原生圖片測試。**三景 3／3 native KEEP 才可解除 STOP**；仍失敗則另提方案，不續購整批。新的 `visualHash` 與分鏡核准須重新綁定；不得把上述紙上候選、機器分數或本機委派核准說成網站站主審核。

## 開場與片尾的組片前檢查

現行 `timeline.json` 第一章到第二章起點為 **867／30 = 28.90 秒**，較要求的 30–60 秒濃縮開場短 1.10 秒；尚未組片，不應把 5 秒品牌片頭灌入濃縮長度。`video.json` 不存 `intro_at`；新長片的品牌 pin 由 `assemble` 依 `isExplainer(cute-mystery)` 預設寫 `after_first_chapter`。全頻道目前已安裝的候選素材實測 **5 秒／150 格**片頭、**21 秒／630 格**片尾；片尾 6 秒原生影格可見左右兩個 16:9 影片框與中間圓形訂閱框，最後 16 秒供 Studio 元素。影片尚未私人上傳，這些框不是可點連結；須上傳後在 YouTube Studio 放兩支推薦影片與訂閱元素，並核對說明欄史料／頻道 URL。若要把 S38 的第一章延至至少 30 秒，應於 STOP 處理後規劃聲畫節奏並重跑受影響關卡，不能默默改凍結稿或靠片頭填時間。
