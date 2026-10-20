# S05 直式短片本機交接（2026-10-20）

`curio-s05-short-1` 用六拍分清陳壽正文「凡三往」、裴松之注引《魏略》的反向初遇，以及裴援〈出師表〉的判斷。片尾只保留《魏略》樊城故事的最初傳話人未見於這段注的問題；沒有把小說場面當史實。短片稿與獨立 SG35 查核見 [verify-20.md](verify-20.md)。

本機製作目錄：`/workspace/.video-work/shorts/curio-s05-short-1/8ebb0cf7dd84b596-1792475801085/`。

| 項目 | 現行結果 |
| --- | --- |
| `shorts.json` | SHA-256 `e48b28a92631fc36c1d0fd321fcc39a437ce64b5d1d9259051c5f2662e5d9e76`；六張來源長片關鍵影格的雜湊由 `from-episode --check` 通過。 |
| 成品 `script.json` | SHA-256 `44e8b50a65052bda78e5e78a842a6585acbbb79e16013ece981026249084f130`；獨立讀者核六句、六圖與四項 SG35 主張，`verify.json` 綁此 SHA、4/4 PASS。 |
| 試片 `upload/final.mp4` | SHA-256 `a1b6d0bac28565c7389423574f090b250fd2a62f8cf0cf46c529687765c50a60`；1080×1920、30 fps、31.57 秒。封面 SHA-256 `82d738dac2adb432b2dcbaed998722e605b620ecf670934267522ad881bf9bd8`。 |
| 聲音與畫面 | `check-audio` 6/6、0 flags；−14.03 LUFS、真峰值 −1.55 dBTP。製作者逐景查看六段中點；另一名工作者對精確 MP4 SHA `a1b6d0…` 的 contact sheet 與成片 2.5／18.5／29 秒獨立目視 **PASS**：直式主體、字卡、繁中字幕均在安全區，來源卷軸示意未見假字或現代物件。 |
| 四語字幕 | `caption-validation.json` SHA-256 `12e6d228acbf2ffac2abe92f16d1f585593689bef85cb75703ab2a4082aa0b58`；繁中／英／日／韓各六段，全部對齊 `timeline.json`、0 時碼錯誤。獨立讀者對四語六句及 SG35 正文／裴注／裴判斷／未知傳話者的語義層級覆核 **PASS**。 |
| 後台草稿 | `draft-report-receipt.json` SHA-256 `dbd37412751ba810b0c5581f8a751460b39851748317de12a6c3c907a2a8c3b1`；`client.report` 可逆建檔，讀回 `format=shorts`、`shorts_line=cut`、`source_slug=curio-s05`、`reviews=[]`、`youtube_video_id=null`。沒有呼叫 `submit`、`push` 或發布。 |
| 品管 | `qa.json` SHA-256 `c49015a4da1fe11090c3159ca8963f8f146e113ee15aa6db8d12be4109d00d58`，**10/13**。音畫規格、來源事實、精華政策、多語字幕、首尾回環等通過；`evidence` 因來源長片尚未 final approved，`metadata`／`links` 因沒有真實 YouTube 長片網址而未過。首末回環 PSNR 40.3 dB。 |
| 上架包 | `package.json` SHA-256 `61d2be04ef3365b0e89007e659706f978282a32ea12bdd52b5d67f7cd6196c49`，**3/4**；影片、四語字幕、封面與揭露欄位齊備，說明欄因尚無長片網址未過。這不是已可發布的包。 |

S05 長片分鏡的網站 owner 審閱仍為 `waiting for the owner`，因此長片 final approval 與 YouTube 影片 ID 均不存在。待長片成片通過站台審閱並取得真實上架網址後，讓短片工具從來源影片記錄產生完整連結，再在本目錄重跑 `qa`、`package`，確認全項通過與成片 SHA 未變後，才進入 Short 正式審核。不能填假網址或把草稿建檔當成核准。
