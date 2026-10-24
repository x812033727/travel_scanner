# S38 R8s｜PF009／PF013 日記引句卡退路，PF014 運鏡單點解 lint

2026-10-22 UTC。R8r [第三輪未裁切原圖驗收](verify-54-r8r-two-native-stop.md)再次退掉 `pf009`、`pf013`。兩景各已歷三次付費原圖、兩輪提示詞修正；本輪停止為它們購圖。**R8s 僅把這兩景換成同一天的佩皮斯日記譯文引句卡，另將相鄰已收圖 `pf014` 的運鏡由 `drift right` 改為 `push in`。**旁白、章節、`look.preset=cute-mystery`、其餘已收提示詞與圖片檔均不變。

## 史料與畫面判斷

- `pf009`：9 月 2 日 [日記 L65795–65803](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65795-L65803)連著寫：他以為火在 Marke-lane 背後、離自己夠遠，`and so went to bed again and to sleep`。卡片標「佩皮斯日記・中文譯文」與 `1666．09．02`，只引「我又回到床上睡了」。前一景 `pf008` 已說明「以為火遠」；引句不把這個心理判斷寫成新證據。
- `pf013`：同日 [日記 L65803–65819](https://github.com/GITenberg/The-Diary-of-Samuel-Pepys---Complete_4200/blob/68fcf49f70ee793b989a6fd0464264d55beb4451/4200.txt#L65803-L65819)記佩皮斯登倫敦塔一處高台，`there I did see the houses at that end of the bridge all on fire`。卡片同樣標日期、來源與「中文譯文」，只引「我看見橋那端的房屋全在火中」。旁白補足登塔；卡片不指稱某戶在這時已確認燒毀，也不畫 1894 年才開通的 Tower Bridge。
- 原想逐字重用同章 KEEP `pf014`。已直接看過其**未裁切 1280×720 原圖**（SHA-256 `b9e847d021298b92143ded0819bc27475a21fe13d4eb4462a53b5ea5948a4bda`）：畫中只有遠方煙柱，人物低頭朝左下看，沒有橋端著火房屋或望火動作。它可服務 `pf014` 的「掛念熟人家」，但不足以呈現 `pf013` 的「登塔親見橋邊房屋著火」，故不以複製圖片冒充這項主張。

## 精確差分與已收圖狀態

[五欄可逆結構化差分](verify-55-r8s-fallback-structured-diff.json)逐欄記載 `pf009`／`pf013` 的 `template`、`data` 與 `pf014.data.camera` 舊新值。R8r `video.json` 基準 SHA-256 `f02fdd2bd769e746b2e76206152492593f66cec1ea48e40a07cd7bf236aaf015`；R8s 作者稿為 `f3f49ce1fdd64ac11189dbe8b64bb7bc486e4c03566795a500f9f8b636f3de34`。以結構化差分將五欄在原位換回舊值，已實際重建出逐位元組相同的 R8r SHA。`script.md`、`claims.md` SHA-256 仍分別為 `e59ec137e3de3871e3b0e5063d8f6504d3eb2adb5fe22265eb3faa3d613d5951`、`f9de8d2771b62cc327f4e599f002af8f3278cfb0f39dbed201e7fdc857201d42`。

把 `pf013` 改卡後，原本 `pf011`、`pf012`、`pf014` 的三張連續插圖都被運鏡規則歸為 `drift`，lint 指向 `pf014`。故**只改 `pf014` 的運鏡**為 `push in`：其塔上握欄、擔憂遠處煙柱的 prompt、旁白與來源意義完全不變。相機字串參與 MiniMax 完整提示詞與圖片 request key；**原 `pf014` KEEP 圖不能當成 R8s 新 request key 的合格圖，該景現在 HOLD，待獨立書面覆核後有界重畫並看原圖**。舊 JPEG 與圖單保留作稽核，不作為本輪成片入選。其他已收 `pf001`–`pf005`、`pf008`、`pf010`–`pf012` 九景的提示詞及所選圖不變；下一次圖片圖單仍須按新 `pictures_hash` 重新綁定，逐項核對 request key、judge stamp 與 SHA，不能沿用舊全局圖單作 R8s 通過證據。

## 僅書面檢查與停點

正文共 111 景，其中 **107 景 `shot` = 96.4%**；全片最長連卡 **2 景**（`pf006`／`pf007`），符合至少 70% 插圖及最多 3 張連卡。新增兩張引句卡分別隔著插圖，第一章節奏較密集，但兩句是日記內最能直接說明「又睡回去」與「在塔上親見火」的語句。`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s38 --json`：**0 errors／0 warnings**，112 句、約 10.016 分鐘不變。`keyframes --shot pf014 --takes 1 --dry-run` 只列出新的 `Camera: push in`、MiniMax ready、285/1072 字，無 image 或 judge 呼叫。

`STOP` 仍在 `/workspace/.video-work/curio-s38/STOP`；私有 ledger SHA-256 仍 `b6823292a9fbacaf4724d057cd71b86b16fb600cc5801e9c85734c1a82454144`，即 **US$0.5695／37 image／36 judge／1 music**，另有舊 `pf003` US$0.0035 reservation，低於本集 **US$4.58** 已核上限。舊 keyframe manifest SHA-256 仍 `45e4c9ff1b3f0245bdc52ea80482b1f9e44ccc0a67964794722c9e40a9700d8a`，綁 R8r 而非 R8s。**此頁只是作者稿；待另一位覆核者核對兩句翻譯、`pf014` 運鏡與失效邊界，才可在 EXIT 恢復 STOP 的單景範圍重畫 `pf014`。**`pf009`、`pf013` 不再畫第四次；`pf015`–`pf022` 尚未畫，第一章及全片未宣稱完成。
