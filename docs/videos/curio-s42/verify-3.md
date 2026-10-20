# S42 語音誤讀八句修復與精確版查核（2026-10-20）

## 修訂範圍與固定來源

本輪只改 `md043`、`md053`、`md065`、`md068`、`md069`、`md070`、`md072`、`md083` 八句口播及 `claims.md` 對應八列；`claims.md` 末段另更新站台關卡實況。`video.json` 的其餘欄位、幕序、畫面、字幕以外的媒體設定都未變。修改前 `video.json` SHA-256 `fa187588a94836e994205a500e1a673fa83473b404c54672071316fb27ccbf4e`、`script.md` `3a0f9748ae41cfebf9853a9fcf3413dd6937b464bdb6b8210e1b335d72db0677`、`claims.md` `b25ef409a2c2bfd9e3662d43eb7001e52337464c888759bd32cfafd1b8d745a9`。修改後依次為 `f2ac5565a573e8992e8206cc295314b3e4d8db3bdf4950b74dad1e8404b097f2`、`ddccd9cdf418412bbcaa5159ae9ad6fe6acb4cabbde76a70640405e65b5d7b4c`、`eb8a377a46d53ad7e018526dcb6da49099767c22eb506d4ff7e26ba86d8cd5c3`。

依 [research.md](research.md) 固定的 1874 英譯編纂本，讀 `/tmp/s42-74723-0.txt` 原文共 11,810 行，SHA-256 `d5c8c5548d57576da07be543263e06f2a20c71f6431222a6c28dc2e5338f9a5c`。這不是船員親筆原頁。逐句差分如下；`claims.md` 已更新為新稿的逐字句，跨 Q09／Q12、Q13／Q12、Q14／Q12 的列補上第二份來源。

| 幕 | 新句保留的史實及原文行號 | 音訊問題的修法 |
| --- | --- | --- |
| `md043` | 皮加費塔記特立尼達號進水、卸貨尋漏，仍未找出漏口，6033–6040；它留下修理，6057–6063。 | 去掉被念作「開敞」的「開場」。 |
| `md053` | 留在帝多雷的人託船員帶信、維多利亞號載六十人出發，6079–6088；皮加費塔自稱每天寫下當天日子，6541–6543。 | 用「一天天寫下的航行記錄」取代被念作「日記」的「日期」，不聲稱現存親筆頁。 |
| `md065` | 船上星期三、岸上星期四，6536–6543。 | 保留對照，去掉被誤念的「開場」與地名。 |
| `md068` | 皮加費塔後來的向西解釋，6543–6547；阿爾博當時以為算錯一天，8760–8761。 | 前句已指名兩位作者，此句避免重念易錯人名。 |
| `md069` | 小艇第二次取米，連十三名船員被扣，6549–6550。 | 去掉會被誤念的「開場」；數字與事件未變。 |
| `md070` | 船員懷疑連大船會被俘，隨即開船，6550–6552；星期差的疑問見 6536–6547。 | 用「那一天的疑問」避免「星期」誤作「星旗」。 |
| `md072` | 維多利亞號從帝多雷出發共六十人，6087–6088；隨船抵達聖盧卡爾只剩十八人，多數病著，6558–6561。 | 上下文已說維多利亞號，省去會誤作船名的「帝多雷」；仍限於隨船抵港人數。 |
| `md083` | 阿爾博記當時相信船上算錯一天，8760–8761；只有皮加費塔在 6543–6547 寫向西繞行的二十四小時解釋。 | 去掉易錯作者名與「西航」，改寫精確請求雜湊，避免碰原請求。 |

## 目前已驗證

- `script --slug curio-s42` 重新生成稿本；`lint --slug curio-s42` 為 **0 errors、1 warning**，提醒片尾沒有口播訂閱。片尾中性收束沿用先前通過政策預檢的方向，沒有在本輪加入商業文案。
- 差分程式逐幕比較 Git 基準與本輪 JSON，確認恰好八句 `text` 改動，其他 `video.json` 欄位完全一致。`claims.md` 八列與 `video.json` 逐字相符；`git diff --check` 通過。
- 設定 `NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 VIDEO_WORKDIR=/workspace/.video-work` 後，`tts --dry-run` 顯示 86 個請求中**只有這八句待合成**，估計 214 Gemini 計費字元，網站回覆 `gemini:Sulafat ready`。
- `md083` 原 502 的 `speech-journal/ac8ad4385d8f2a5fde8e24640f53eb41d75dd83e11417b8ae09f2417d6de5e52.json` 仍為 `held`，檔案 SHA-256 `1e67cb7b3f1fac33dee40b19d61fe7cd7dfe0c81cc986e0f600d09f44a79dd13`。不得重送同一精確請求或清除 journal；供應商是否計費仍未知。
- 精確新稿的完整口播政策預檢已由站台 Jev 回 `PASS`：`script.md` SHA-256 `ddccd9cdf418412bbcaa5159ae9ad6fe6acb4cabbde76a70640405e65b5d7b4c`、請求 SHA-256 `3d8de8a640f123493b2832388a8dae2c627378eaab0d9c884d89caf05669133e`、立場 `0.79`、建議 `0.01`、業配 `0.02`。原始回條 `/tmp/s42-voice-policy-r1.json` SHA-256 `7adbd70409b8c39c984d0ff1a7abcfb3187a7b17a037ed1e49c83e3a940f3ed7`。這只是合成前政策預檢，不代替正式成片 `qa`。

## 敘事盲讀與站台劇本關卡

新稿凍結於 `/tmp/s42-voice-panel-r1.txt`（SHA-256 `8c5e68a81eafa831f46e1a35b57e501c02934759523fb56a8b569c9996cc5bc5`）。兩位未讀過前稿的獨立讀者各答十三題：讀者 A 的紀錄 SHA-256 `44c26fe7a02daec4704f7983c085c0187c83af40bbae7dd3b264343d892ff946`，12／13 YES，唯一 NO 是 `no_recap`，認為 `md051`、`md072` 的六十人數字重複；讀者 B 的紀錄 SHA-256 `9e93c72b6428befa00d58c6f0a07f4db3b39571845c7d4a8cd24ea996aa1db68`，13／13 YES。兩份紀錄均與精確新版相符，依官方 `mergePanelVerdicts` 規則合併為 13／13 PASS，保留個別讀者的異議。正式合併紀錄 `/workspace/.video-work/curio-s42/review/narrative.json` SHA-256 `497efbc083358c99567f8ccc8ab80ebeb134caf659fafaeccbc38ea9337cbc3d`，`round=3`，綁定 `script_hash=cba0d697a03d926234474bc234d61e4dc2388a010f2e585c09c978233620a5b6`；`script.md` 檔案 SHA-256 如上。

`review-push --gate script` 已將新版送站台；`review-pull --gate script` 回覆舊版批准已失效，**新版等待站主決定**。這是手動送審的影片，站台沒有自動核准。本輪沒有把 pending 寫成站主批准。

## 語音、查音與剩餘關卡

合成前再次 `tts --dry-run`：86 個請求中只八句需合成，約 214 計費字元。正式 `tts` 成功合成 `md043`、`md053`、`md065`、`md068`、`md069`、`md070`、`md072`、`md083` 八句，沿用其餘 78 句快取，旁白長 09:35。合成後乾跑為 86 個請求、零待合成、零計費字元。舊 `md083` held request SHA-256 `ac8ad4385d8f2a5fde8e24640f53eb41d75dd83e11417b8ae09f2417d6de5e52` **沒有重送或清 journal**；該 journal 的檔案 SHA-256 仍是 `1e67cb7b3f1fac33dee40b19d61fe7cd7dfe0c81cc986e0f600d09f44a79dd13`。先前 HTTP 502 是否向供應商計費仍未知。

`check-audio` 查完 86／86 句：63 句辨識逐字一致、21 句只有同音字或語助差、2 句經 Jev 判定可用、**0 flagged**；本次只重辨八句，沒有新增 Jev 判斷請求。八句新錄音均為 `exact` match。精確查核檔 `/workspace/.video-work/curio-s42/review/check.json` SHA-256 `9297967fa6c976133ea8181eddfd6bbf2b0304c7c1fcb24abda61f19cf2517ba`，空旗標檔 `check-flags.json` SHA-256 `988f3a9f3d565f008c99924dd30eb9b376ef1db919aaaa6769349bb3882dc4e9`；時間軸 `timeline.json` SHA-256 `ce20d63649d95c55a76ba493b1f4aab09bf63dda3ef66631cce4203d815b4d6e`。

`review-push --gate audio` 已送站台；`review-pull --gate audio` 回覆 **等待站主決定**。站上大綱 A 已正式選定，新版劇本及語音的站主關卡仍 pending。插圖、配樂、成片、最終 `qa` 未做，沒有聲稱完成這些關卡。
