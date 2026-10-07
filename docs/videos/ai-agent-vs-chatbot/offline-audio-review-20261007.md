# AI 代理與聊天機器人：離線音訊證據

本次使用本機已快取的 Whisper small 盲轉寫，提供逐句差異與回聽線索。本子工作沒有呼叫付費供應商、下載模型、改動原音檔、原生 cache／journal／STOP 或核准。未做人工聽感確認，也沒有自行核准旁白。

以下是明確分開的三批音檔。V1 是原始合成；V2 是協調者依原生關卡重錄六句後的新素材。稿件全文與 speech_hash 在這兩批相同，時間軸及六個音檔已改變。V1 的診斷不能冒充 V2 的音訊審核。

| 批次 | 實際完成範圍 | 時間與收據 |
| --- | --- | --- |
| 原始完整掃描 | **55／142，未完成** | 2026-10-07T12:29:26.538110+00:00 收尾；核對自有程序後成功發送 CTRL_C；退出碼 3221225786、stderr 為 KeyboardInterrupt、complete_order=false |
| V1 優先疑句 | **14／14 完成**：重用6句既有盲轉寫，再盲轉寫8句 | 2026-10-07T12:34:23.435853+00:00、exit0；14個WAV先全部複製並核對完整SHA-256 |
| V2 優先疑句 | **3／3 全新盲轉寫完成**：ag093、ag125、ag097 | 2026-10-07T12:51:06.082878+00:00、exit0；3個實際WAV皆與V1雜湊不同，先固定來源、字典、時間軸及音檔 |

原始55句掃描結束，以及V1 14句交接時，全部142個原始WAV雜湊仍與起始manifest相同；narration、來源、時間軸及四個快取模型檔也一致。之後協調者已實際重錄六句，因此本文件不聲稱當前整批142個WAV仍等於V1。V1與V2的指定疑句快照和真實輸出都保留在Git外。

| 來源／模型綁定 | 完整值 |
| --- | --- |
| V1與V2 video.json SHA-256 | `905ac35021688b7ca80264f12afd6f8973b959317438538e2199bdb4536a058c` |
| speech_hash | `80b70c13bcc03e34` |
| lexicon SHA-256 | `862d277aaf4359e9e07b5f3281f59eabb240f5ea3227c174f692cf2d0237f675` |
| V1 timeline SHA-256 | `dd814aca675fe70a819917c1139dd8d80add41075cc99a2a81483f3b78f112f0` |
| V2 timeline SHA-256 | `7ab395bca9e9f7f9463a130570cde39a2e3297c1a06e1fc059f862a12dd15f41` |
| V1旁白與時間軸 | 原始音檔合計568.72秒；19,182 frames／30 fps，639.40秒 |
| V2時間軸 | 18,883 frames／30 fps，629.43秒 |
| 模型snapshot | `536b0662742c02347bc0e980a01041f333bce120`，Systran faster-whisper-small |
| 推論規格 | CPU、int8、cpu_threads=2、num_workers=1、beam_size=5、local_files_only=true |
| 提示 | 只有通用「以下是繁體中文的句子。」；無逐句稿、英文詞提示或hint文件 |
| 離線限制 | HF_HUB_OFFLINE=1、TRANSFORMERS_OFFLINE=1；socket連線函式阻擋。模型只收到快取模型路徑與WAV路徑 |
| Runtime | Python 3.14.6、faster-whisper 1.2.1、ctranslate2 4.8.2 |

## V1 14句：文字與音節比較

完成盲轉寫後才讀取凍結稿件比對。現有 matchKind 規則得到4 exact、2 sound、0 filler、8 unresolved。exact忽略標點、空白及NFKC；sound是現有國語讀音規則的同音判斷。這些不是人工聽感結論。

| ID／V1開始 | 預期讀法 | 實際盲轉寫 | 機械分類／回聽線索 |
| --- | --- | --- | --- |
| `ag003`／00:10.8 | 看到最後，你會有一張能自己使用的交辦清單。 | 看到最後,你會有一張能自己使用的交辦清單。 | exact；與來源按現有文字／同音規則一致；仍未確認自然度、口音、接句或整片聽感。 |
| `ag010`／00:41.8 | 代理會看工具回來的資訊，再決定下一步。 | 固定流程, 則照預先寫好的路徑逐向處理。固定代理會看工具回來的資訊, 再決定下一步。 | unresolved；回聽是否帶入上一句「固定流程…逐項處理」，以及在「代理」之前多說「固定」；兩個轉寫都出現額外內容。 |
| `ag090`／03:24.1 | 先用低風險任務練習，更容易看清它的能力。 | 先用低風險任務練習,更容易看清他的能力。 | sound；與來源按現有文字／同音規則一致；仍未確認自然度、口音、接句或整片聽感。 |
| `ag029`／03:47.0 | 我沒有直接把週一休館貼進答案。 | 我們又直接把週一修管貼進答案。 | unresolved；優先確認否定詞：「我沒有」與「我們又」會改變意思。音節規則記為 mei2→men2、you3→you4；休館／修管本身同音。 |
| `ag031`／03:55.6 | 這一步是實際查詢，不是模型憑印象補一句。 | 這部是實際查詢,不是模型憑印象補一句。 | unresolved；回聽「這一步」的「一」是否存在；盲轉寫省去一個音節。原生第二意見已由 Jev 0.80 接受，不能憑此診斷要求重錄。 |
| `ag093`／04:48.1 | 如果只摘一句週一休館，就會漏掉例外。 | 如果只加一句 週一修管 就會漏掉例外。 | unresolved；回聽「摘」zhai1 是否被讀成「加」jia1；休館／修管只屬同音字差異。 |
| `ag125`／05:20.6 | 交付物要保留日期和館名，不能只寫週一可去。 | 交付物要保留日期和管民 不能止血週一可去。 | unresolved；回聽「館名」的尾音，以及「只寫」是否清楚。多音字與連讀的機械聲調不能獨立證明讀錯；完整音節差異已保留。 |
| `ag097`／05:57.5 | 館方有步行建議，但我們未實測，也沒查天氣。 | 官方有不行建議 但我們未實測也沒查天氣。 | unresolved；回聽「館方」guan3 與「官方」guan1；步行／不行的字形差異本身同音。 |
| `ag047`／06:31.6 | 把待查寫出來，是完成品質的一部分。 | 把代查寫出來是完成品質的一部分。 | sound；與來源按現有文字／同音規則一致；仍未確認自然度、口音、接句或整片聽感。 |
| `ag048`／07:08.1 | 等等，固定流程也能查兩個頁面啊。 | 等等,固定流程也能查兩個頁面啊。 | exact；與來源按現有文字／同音規則一致；仍未確認自然度、口音、接句或整片聽感。 |
| `ag137`／07:52.9 | 等你看過成果，再決定要不要開更多動作。 | 等你看過成果,再決定要不要開更多動作。 | exact；與來源按現有文字／同音規則一致；仍未確認自然度、口音、接句或整片聽感。 |
| `ag107`／08:52.6 | 代理打開的網頁，可能有與任務無關的指令。 | 代理打開的網頁可能由與任務無關的指令。 | unresolved；回聽「有與」的連讀，區分有／由；字形及單字聲調計算不能單獨排除正常連讀或轉寫誤辨。 |
| `ag064`／09:11.2 | 你可以從一個小而能回查的任務開始。 | 你可以從一個小而能回查的任務開始。 | exact；與來源按現有文字／同音規則一致；仍未確認自然度、口音、接句或整片聽感。 |
| `ag076`／10:28.2 | 代理的價值，是依真實回饋選下一步。 | 代理的價值是以真實回饋選下一步。 | unresolved；回聽依／以的用字與聲調；原生第二意見已由 Jev 0.58 接受，此診斷不自行推翻該判斷。 |

未解決的差異可能來自實際旁白，也可能來自辨識器。`priority14/comparison.json`逐句保存帶聲調音節、取代、缺少及增加的差異；不得直接以文字差異改字幕、清除原生flags或宣稱旁白失敗。

## 原生第二意見：另有實際收據

協調者之後以原生 check-audio --second-opinion 消費這14句真實輸出。`20261007T123655Z-check-audio.stdout.log`記錄142／142已檢查、0句重新轉寫、1次Jev呼叫、8句由第二意見解除標記、6句仍低於0.5。該命令於2026-10-07T12:37:02.324852+00:00以exit1結束，表示仍有六句flags；不是整套旁白核准。

解除的八句為ag003、ag090、ag031、ag047、ag048、ag137、ag064、ag076；其中ag031為Jev 0.80、ag076為Jev 0.58，其餘六句為第二份轉寫按原生規則符合稿件。仍標記的六句為ag010、ag029、ag093、ag125、ag097、ag107，後續重錄由協調者與原生關卡處理。

這一段是已完成原生命令的歷史收據，不是把Whisper診斷自行當作Jev判決。當前旁白關卡、成片QA、上傳包及站主驗收以協調者的最新原生收據為準。

## V2 新三句

六句重錄後，V2三句的獨立盲轉寫得到2 sound、1 unresolved。它們使用當時新時間軸與新WAV，沒有套用V1音訊結果。

| ID／V2開始 | 預期讀法 | 實際盲轉寫 | 分類 | 新WAV SHA-256 |
| --- | --- | --- | --- | --- |
| `ag093`／04:40.0 | 如果只摘一句週一休館，就會漏掉例外。 | 如果只摘一句週一修館,就會漏掉例外。 | sound | `6475ca574eda2b025b475c8e2f7792bc229e051162a2c4b794edb065ee16dab4` |
| `ag125`／05:12.0 | 交付物要保留日期和館名，不能只寫週一可去。 | 交付物要保留日期和管明 不能止血周一可去。 | unresolved | `cdb499c280e4b67f9c2a249e72fb0fbf66226df5a9d047527c659f00d902cb45` |
| `ag097`／05:47.8 | 館方有步行建議，但我們未實測，也沒查天氣。 | 管方有步行建議 但我們未實測也沒查天氣。 | sound | `2b4c62bd9ba61fb0215bd807ba671b7db8cfc16475499e1b7f292e106d87edc7` |

V2 ag125的回聽重點仍是「只寫」：盲轉寫寫成「止血」。字形、聲調規則及模型輸出不等同於實際人工聽音；此文件不決定其原生判決或是否還要重錄。

## Adapter與防止錯用

V1 adapter已驗證14個原始request路徑的完整WAV SHA，再輸出逐檔真實heard；刻意改壞最後一個同名WAV時，exit2且stdout為空。不存在的hint文件也不影響輸出。

另有combined11查找證據：8句重用V1相同WAV的真實輸出，加上V2新3句，**不是11句重新ASR**。其adapter驗證model、transcript、frozen snapshots與current source／lexicon／timeline，再核全部requested WAV，任何一項不符都在輸出前停止。11個原始路徑與新3句subset皆已實測重現saved heard；最後一個WAV雜湊不符時，exit2、stdout0 bytes。它是補充provenance資料，不能宣稱已被原生消費。

V2三句獨立測試harness曾只將stdout CRLF轉LF、沒有同樣正規化原始transcript，導致其比較失敗。未修改其既有adapter或receipt；combined11後續測試對兩側newline採相同處理並通過，逐句文字未更動。協調者的實際native dispatch另有驗證收據。

## V1原始樣本測量

全部142個V1原始WAV都是48 kHz、mono、16-bit PCM，沒有全靜音檔案。以下七句各有1至5個樣本到達16-bit full scale；只列回聽尖峰提示，不能推論已可聽失真，也不自行觸發重買。這是V1測量，不能套用到已重錄的V2片段。

| ID | Full-scale樣本數 | V1原始WAV SHA-256 |
| --- | ---: | --- |
| `ag033` | 3 | `247f98e21940422dafe0290bac906103fe1ac23661b22386c82a5a9d4c373ad9` |
| `ag034` | 5 | `6845530d74d86f938dd754299ce7440a29e3272547cbf6a32ff5b9b861cf289e` |
| `ag044` | 1 | `ae6dc5ddf7cc32348397608e67586b8692047e2005bbae7dae43240d314ebe15` |
| `ag071` | 1 | `3211719141ffc91c1da6d2b41f1057931c57fe3722ec270ee72c5ba454beff4b` |
| `ag077` | 2 | `9deae3c31ad411db5e2ae13d946b383666dbe8b7597a9619122f4e9dc651ed7d` |
| `ag093` | 2 | `1348bab590702295676e0e2ab047233e3099b211f863fee3d523d83a1885e215` |
| `ag094` | 1 | `2863a0444769b247a6e7f4b8f036c2c7a263af9b992123b943b17cd79e497e3d` |

## 可驗證來源與metadata清單

本機evidence根目錄：`<home>/mokaair-work/ai-agent-continuation-20261007/offline-audio-evidence`。原始WAV、快照、模型、本機命令與逐句JSON都留在Git外。下列原生命令收據位於`<home>/mokaair-work/ai-agent-continuation-20261007/logs`。

| 檔案 | Bytes | SHA-256 |
| --- | ---: | --- |
| `metadata.json` | 75904 | `6a14f8d0884f7d481ee617c764a1a247db3d00265873bed594f1318f97c168c6` |
| `start.json` | 16969 | `a37d331c2cb18593ff9d185aa2bcafc5103abb93ac9cf2318996eb0e9f00c55e` |
| `child.json` | 16994 | `da46c0b1eedbb0aff0c6bbdb18f8a4fe05a0ec1f0a52da40d12023583d80b2a6` |
| `stop-request.json` | 32512 | `667ec24c453b37e32d479268540c8f75f1cccba6f763dc702e6d9becf905ba6b` |
| `exit.json` | 619 | `5f2d0ed1711ef4a38297f2c424b6cc729dd7198788cbd13ecc3924415c92ce13` |
| `transcripts.txt` | 3637 | `c30d99d40be21260715a374439341dcd2826a97059e1418504201a296417ab21` |
| `wav-inspection.json` | 79117 | `65d8383448dbf5ac8fd1f826531432b55893b548d8961cc751f4615052817c7c` |
| `source-input.json` | 36751 | `905ac35021688b7ca80264f12afd6f8973b959317438538e2199bdb4536a058c` |
| `timeline-input.json` | 48788 | `dd814aca675fe70a819917c1139dd8d80add41075cc99a2a81483f3b78f112f0` |
| `lexicon-input.json` | 3406 | `862d277aaf4359e9e07b5f3281f59eabb240f5ea3227c174f692cf2d0237f675` |
| `blind_transcribe.py` | 1316 | `8251632a76f9b544a6868df581f0638a5bc3ed8bdc2592a639d7e3b7399f1279` |
| `priority14\preparation.json` | 10164 | `ae4f95cda10ab5b6e337be363f2c6250020ea131c95990b3fe8437277b792160` |
| `priority14\start.json` | 2037 | `ac8bc0d48dc178aeb14d335b95f4377ff8ea36f3a9da6d84c86346974fd42910` |
| `priority14\child.json` | 1510 | `b5619bdd5aee47067bbd705e4eb8c36f3b02f3ae7c6b4beb74bd3e6fef7e2d27` |
| `priority14\exit.json` | 734 | `dab3cf375c27cf869404040be73a0408a069e42af60094abdcceeb413d63d884` |
| `priority14\transcripts.txt` | 968 | `25bdff7fcae92a5816780e0479197e82d783d975bdb3f652608a243fc6b3b5d0` |
| `priority14\comparison.json` | 23861 | `f424a919015269e43a0d5a0683ca7e28ff2b601c57f2e535b2d3e4c71cd6c555` |
| `priority14\listen-notes.json` | 1322 | `86f641149c11bb2268ba273454b510d84bb3b3776f21ff04e53bd2f6a119f838` |
| `priority14\receipt.json` | 14898 | `81f2a3a6be0c1f85c03ddf21e42c43f35622eaabf5c87d148e010c5bce91db45` |
| `priority14\adapter-validation.json` | 935 | `934aefe226522ca08715a3d2372007976bdde4fecb89f1993669d478cfeeeaa1` |
| `priority3-v2\metadata.json` | 7090 | `ffff3712f866d0fa73887b263563feb82c6484e6939199c4580c96fa9523093c` |
| `priority3-v2\start.json` | 888 | `fb16f52559ab75d022e1936adb339502bac1aa6cc46f868aafc90e16b867305b` |
| `priority3-v2\child.json` | 911 | `14ca65d491f0c5f6e88fe1ea59d5303b192cf06cbe6dd46d080922b902bcc601` |
| `priority3-v2\exit.json` | 581 | `d87a826cdf10889149faf1e138cb0cea1d0b8657d3e948511b20a8687ece9d5d` |
| `priority3-v2\transcripts.txt` | 207 | `c03d01dc0b2989528f06d924442f2426023b6938d4ee10cc603af6374525b381` |
| `priority3-v2\comparison.json` | 4030 | `a5825c17db7fb5d7570f98358aa3308f562664deadb8c766ec43629485bf98e7` |
| `priority3-v2\receipt.json` | 8727 | `49702ce290f8cba1ed22bbaa0be4e56e29d9ebfba251966b12a6bd448575942d` |
| `priority11-v2\transcripts.txt` | 714 | `116177ec7dba224d8db2bb5684c39ef8f31665e8f6f28937544737c73d1073d8` |
| `priority11-v2\receipt.json` | 15813 | `7c8ec7a44225178398336297eadb82b81ce9ff5857c64cd0a922f1b4de292380` |
| `priority11-v2\adapter-validation.json` | 703 | `0eb485bd4edfc683de2bac6fe0c720817a84b0db6ed1389194511aa8f9ab5d56` |
| `logs/20261007T123655Z-check-audio.stdout.log` | 4030 | `48dcdc5d81167dc9255352c533f77504e60e698097de783328b8d1f521663816` |
| `logs/20261007T123655Z-check-audio.exit.json` | 99 | `0894b0909412e75e2ab2963a49bf387953d0fa5a5b93577842421bc498d3c929` |
| `logs/20261007T123655Z-second-opinion-binding.json` | 1191 | `730b700360b9334e9318d8328074da9d80208b95ff17b9a1719076edf0b9606e` |
| `logs/20261007T123655Z-second-opinion-binding.exit.json` | 262 | `e3c03fb71a8fe45e3eaff92f196f1335ffbcc44c5bafee42920602cf85fe42e1` |

模型實際檔案：

| 模型檔案 | Bytes | SHA-256 |
| --- | ---: | --- |
| `config.json` | 2370 | `b55496ac7940a7ae47d2c01eab40edfd8701feec1229d9cce3b40014383fb828` |
| `model.bin` | 483546902 | `3e305921506d8872816023e4c273e75d2419fb89b24da97b4fe7bce14170d671` |
| `tokenizer.json` | 2203239 | `fb7b63191e9bb045082c79fd742a3106a12c99513ab30df4a0d47fa6cb6fd0ab` |
| `vocabulary.txt` | 459861 | `34ce3fe1c5041027b3f8d42912270993f986dbc4bb34cf27f951e34a1e453913` |

`metadata.json`保存全部142個V1原始WAV的bytes、完整SHA-256、樣本數及時長；每批start／child／exit保存實際程序與完整命令；transcripts是未修改的盲轉寫輸出；comparison在轉寫固化後才讀稿。priority3-v2 metadata另保存當時current source、lexicon、timeline與三個新WAV的完整快照綁定。

後續若稿件、字典、時間軸或任何指定WAV改變，舊輸出只能當作它原來那批音檔的證據；不覆寫舊receipts，不將舊輸出自動當成新音檔。人工回聽、旁白核准、成片核准與上架仍是各自的狀態。
