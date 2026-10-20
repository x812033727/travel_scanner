# S28 Short 1：直式裁切修鏡與媒體驗收

2026-10-20。原文稿收據在 [short-verify-1.md](short-verify-1.md)，其腳本雜湊 `97c5593e6af7e66efef815e7e7fec97850df7ba17fafa1f33b3b0d06340229dd` 是**修鏡前快照**。修鏡版 SHA-256 `092fed0c740d4b78f60dcb4e98ee7a667795958a382b7a15bbc39e4b96352d63` 僅改三個 `shot` ID，標題、史料、所有旁白與說明欄未動；這一版組片後有兩句辨音未過。現行 [shorts.json](shorts.json) 改寫了這兩句使語音核查過關，SHA-256 **`49cced53588315c1ac3bc2a94dc9337858cda521a4bf11f9540e6ca9708aed60`**。

## 9:16 中央裁切預覽

| 短片景 | 舊影格與問題 | 改用已核長片影格 | 文字與畫面的關係 |
| --- | --- | --- | --- |
| 2 | `jar-010` 把甕和石頭裁出畫面，只剩得救孩子 | `jar-013` | 石頭擊中水甕、水外湧，直接支援「拿石頭砸破水甕，救出孩子」的史書**插畫示意**；破口位置仍非史書實物細節 |
| 3 | `jar-017` 左右兩張臉被截、上方有黑帶 | `jar-016` | 直式中心留下一名孩子讀書的畫面，配合「七歲聽講《左氏春秋》」；畫面沒有可讀古書文字，不當史證 |
| 5 | `jar-020` 上方黑帶、兩人舉空白紙頁，年齡留白不清楚 | `jar-014` | 得救孩子、積水和遠處甕可見，回到「不能確定救人時恰好七歲」的事件；不替孩子或甕補實測身分／尺寸 |

保留 `jar-009` 開頭與結尾的石塊、破甕、水，`jar-019` 留在證據轉折；6 景合計 5 個不同已驗收影格。原長片關鍵影格 manifest SHA-256 `549576311bcea7dc29f211ba7e17058530c9b0e23cc11a91b873fa70c9e9dc90` 未變。替鏡由主代理提供中央裁切候選並覆看，沒有買新圖。旁白的史料界線已由獨立讀者通過；這次替鏡未增加新的事實主張。

更新後 `validate`、Curio 單支 `episodeShortsProblems`、CTA 與模擬有長片 URL 的 metadata 均 0 問題；`VIDEO_WORKDIR=/workspace/.video-work node tools/video/shorts/cli.mjs from-episode --slug curio-s28 --check` 回 `curio-s28: 1 Shorts valid; every keyframe matches its hash`。長片本身仍無 YouTube ID，正式上架包的第一行完整影片連結不能捏造。

## 兩次配音實測與改句

S34 製作人完成語音／ASR 後，S28 修鏡版第一支 server voice 成片為 **30.10 秒／903 格**，一次合成 8 句；直式六幕抽格由主代理獨立目視通過，8 張字幕卡無溢位，畫面 1080×1920／30 fps，聲音約 −14.03 LUFS／−0.94 dBTP，首尾 12 格回環 PSNR 40.95 dB。`check-audio` 8/8 中兩句被標：原 #4「接下來才寫破甕；救人句沒有重標年歲。」被辨成「救人劇……中標」，原 #7「完整對讀見長片。」被辨成「對局」。其餘 6 句沒有標記。

只定點重錄 #4、#7 一次，沿用其餘 6 句，第二支成片 **30.233 秒／907 格**；native 9:16 的首格、六幕中段與最後一格重新抽看，主體、標題、字幕和品牌水印均在畫面內，沒有黑帶或假古籍文字。第二輪 `check-audio` 仍是同兩句 flagged（辨成「救人，劇中沒有載明年歲」與「完整對局見長片」），因此不把 6/8 說成核音全過，也不重買第三次同一句。

改用更口語而同義的 #4「**傳記接著寫砸甕救人，卻沒有再說他當時幾歲。**」與 #7「**長片把這兩段原文擺在一起。**」。前者保留《宋史》先七歲讀書、後救人未再標歲的核心；後者指已完成長片的兩段原文對讀。主代理依既有 [research.md](research.md) 與 [claims.md](claims.md) 的固定《宋史》段落覆核，沒有新增年歲或現場斷言。這個中間稿 SHA-256 `586e971e165583f43185794ac504c31d7a6ea1aaa1ac532dd6acce0380b2a753`，`from-episode --check` 通過 5 個既有影格雜湊。

S05 製作者明確釋出語音時窗後，中間稿重建 30.9 秒、927 格，只補錄 2 句；核音 7/8，#4 已過，#7 的「長片」被聽作「常見」。最後只把 #7 換成「**完整影片把這兩段原文擺在一起。**」，主代理定點來源覆核通過。最終稿 6 景／8 句、`from-episode --check` 再通過，重建只補錄 1 句；先前三支返工成片和舊版 `verify.json` 都不作交付。

## 最終本機成片與查核

成片目錄：`/workspace/.video-work/shorts/curio-s28-short-1/548251b760589f50-1792476177526/`。以下 SHA-256 綁的是**最後版本**：

| 項目 | 結果 |
| --- | --- |
| `shorts.json`／製作後 `script.json` | `49cced53588315c1ac3bc2a94dc9337858cda521a4bf11f9540e6ca9708aed60`／`2968548e7e49a989d087e7ee032fa8d51f84d1092faada5bf441e863cb365eb9` |
| `upload/final.mp4` | `a281dae37cea5fd650bdf79897153c2fa9009d5d087619a66ff7ed3164a5507f`；31.00 秒、930 格、1080×1920、30 fps、H.264／AAC 48 kHz |
| 旁白與聲音 | `check.json` 8/8、0 flagged，僅最後一句一次補錄；約 −14.04 LUFS、真峰值 −0.97 dBTP |
| 直式視覺 | 成片目錄的 `native-vertical-review-grid.png` 抽首格、各幕中段、末格 8 張；石塊、甕、讀書孩子與得救孩子均留在中央安全區，無黑帶；8/8 字幕卡無溢位；封面等於首格，末格回首格 PSNR 40.88 dB |
| 史料 | 本機 `verify-current.json` 綁 `script.json` SHA，逐核 8 句；七歲屬《宋史》聽講《左氏春秋》句，救人段未重新標歲。主代理再次定點覆核最後 CTA，無新歷史主張 |
| 四語字幕 | `caption-validation.json`：zh-TW、en、ja、ko 各 8 cue、0 時碼問題，連續至 31.000 秒；主代理獨立逐 cue 對照四語語義 PASS |
| 後台草稿 | `draft-report-receipt.json`：可逆 `client.report` 建 `curio-s28-short-1`，`format=shorts`、`shorts_line=cut`、`source_slug=curio-s28`；讀回 `reviews=[]`、`youtube_video_id=null`，沒有送審或發布 |
| `qa.json` | SHA `ba4a0ad339867e979ce453833f784102b092672c51f73ea774674d139e7e1ebf`；11/13 通過。正確的 `cut` 立場規則、史料、聲音、四語字幕、直式版位等通過；`metadata`、`links` 僅因長片尚無真 YouTube URL 失敗 |
| `package.json` | SHA `119777e09db7f83889f203c80a8f72a5579baca0d164f59ad394b6a4b918fa`；3/4 通過，僅 `descriptions` 缺來源長片 URL；`metadata.json` 中 `source.slug=curio-s28`、未填假網址 |

第一次 QA 的立場項誤用了尚未建 Short 草稿時的教學影片規則，要求「有示範」而給 0.10；建立真實 `shorts_line=cut` 草稿後，不改已驗旁白重跑，精華規則通過。其餘兩項仍待來源長片的真實 YouTube ID；取得後從站台生成網址，重跑 QA 與 package，確認 MP4 SHA 不變，再進正式審核。不得以本次後台草稿或本機成片稱作已上傳。
