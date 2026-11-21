# S38 R8s｜PF009／PF013 日記卡與 PF014 運鏡獨立覆核

2026-10-22 UTC。**書面 PASS：只放行 PF014 一次原生試畫與逐張原圖驗收。** PF009、PF013 換日記譯文卡的來源與版面邊界成立，但本票不把 R8r 兩張退件圖收回，也不放行更多圖片或全片。

## 引句與歷史層級

直接核對固定 `/tmp/curio-s38-pepys-4200.txt`，SHA-256 `3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`，1666 年 9 月 2 日日記 L65795–65819：

- **PF009** 的英文是 `and so went to bed again and to sleep`；「我又回到床上睡了」準確傳達回床再睡。前一景 PF008 已交代他誤判火離家很遠，卡片不新增火勢判斷。卡上標「佩皮斯日記・中文譯文」與 `1666．09．02`，沒有冒充中文原文。
- **PF013** 的英文是 `there I did see the houses at that end of the bridge all on fire`；「我看見橋那端的房屋全在火中」保留親見、橋端和房屋著火三層事實。日記此時只為 Michell 等人掛念；搭船後才見其屋燒毀。卡片沒有提早宣告這項後來的結果，也不再讓圖像模型畫出 1894 年 Tower Bridge。前後旁白仍有佩皮斯登塔、PF014 擔憂熟人、PF019 船上確認的時間次序。

我直接看過 R8q 已收 PF014 未裁切原圖，SHA-256 `b9e847d021298b92143ded0819bc27475a21fe13d4eb4462a53b5ea5948a4bda`：石欄上的人物低頭憂慮、遠處僅見煙柱，沒有可辨橋端房屋大火，不能複製到 PF013 假裝作其親見。PF014 本身仍可表現「掛念」，但 R8s 把它的 camera 改了，新圖要另驗。

## 逐位元組差分、版面及舊圖失效

現行 `video.json` SHA-256 `f3f49ce1fdd64ac11189dbe8b64bb7bc486e4c03566795a500f9f8b636f3de34`。獨立逐欄驗證 `verify-55-r8s-fallback-structured-diff.json` 的五個新值：`scenes[8].template`、`scenes[8].data`、`scenes[12].template`、`scenes[12].data`、`scenes[13].data.camera`。將五欄在原位復舊並用原檔相同格式序列化後，SHA-256 精確回到 R8r `f02fdd2bd769e746b2e76206152492593f66cec1ea48e40a07cd7bf236aaf015`；沒有旁白、章節、look、其餘 prompt 的隱性變動。`script.md`／`claims.md` SHA 仍是 `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`／`f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`。

正文 111 景中 `shot` **107／111 = 96.4%**；四張 `big` 卡，最長連卡是 PF006／PF007 **2 張**，符合插圖至少 70%、連卡最多 3 張。現行 `lint --json` 是 **0 errors／0 warnings**、112 句（含 outro）、約 10.016 分鐘。PF014 只由 `drift right` 改 `push in`，其 prompt、旁白與來源層級不變；但相機值進入圖片請求字串，舊 manifest 的 PF014 key `7c46410b56e9e8dc` 與已收 JPEG 都屬舊運鏡，**不得作 R8s 的新 key 圖**。舊檔保留稽核，PF014 暫為 HOLD。

已收 PF001–005、PF008、PF010–012 的**九張**現行 manifest entries 與 R8r 後備份逐項相同，九張所選檔案 SHA 各自符合 entry。STOP 在位；舊 manifest SHA `45e4c9ff1b3f0245bdc52ea80482b1f9e44ccc0a67964794722c9e40a9700d8a` 是 R8r 狀態，不能當 R8s 全局驗收。私有 ledger SHA `b6823292a9fbacaf4724d057cd71b86b16fb600cc5801e9c85734c1a82454144`，合計 **US$0.5695／37 image／36 judge／1 music**，另有未動的 PF003 US$0.0035 reservation；整集硬上限 **US$4.58**。

`NODE_USE_ENV_PROXY=1 VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs keyframes --slug curio-s38 --shot pf014 --takes 1 --dry-run` 只列 PF014、`Camera: push in`、MiniMax `image-01` ready、285／1072 字和約 US$0.01 新費用。只可在 EXIT 恢復 STOP 的邊界下跑 PF014 **一張**；完成後看未裁切原圖的成年人物、塔樓、擔憂、遠火、時代與系列畫風，核私有 ledger／manifest 和九張 KEEP 不變。PF009／PF013 不再購第四張，PF015–022 繼續停止。
