# S45 R9｜23 句口語窄改：作者來源差分與凍結

2026-10-20 UTC。R8 的 [實音檢查](verify-17.md)兩輪後仍有 **23 官方旗標，音訊 HOLD**；獨立 Whisper 模型下載被代理 403 擋住，沒有第二路音證。R9 是**未配音的候選稿**，只調整這 23 句的字面以降低發音／轉寫歧義。這份文件是作者自檢，**不是**新版本的獨立史料覆核、兩位新盲讀者、Jev 政策或核准。R8 的 PASS 與媒體不能挪到 R9。

| R9 凍結輸入 | SHA-256 |
| --- | --- |
| `research.md`（未改） | `97b91f2344190fbc424fd29eca17da2bee372673bdc7fd36e7161e13ef31ab65` |
| `brief.md`（A 案輪廓未改） | `965d4f46b1b90cad9d52882ca5187003c42ca9a897debc874fbc0937d5a40909` |
| `video.json` | `f0a29e1116363409392af7dca68c32e6d7ec6f9a08fe937aaadb42e36cddecec` |
| `script.md`（由同版 JSON 重產） | `cd51d875c9ccee9b6d99caf4da66a06d0b8f8ac22f2160a8de0d8ad33905e2c8` |
| `claims.md` | `2af692f0b273a0a99e243042b8a8df55aae01ff5a6f58546f93846aa1eaa7400` |

以已保留的 R8 `review/check-r8-first.json` 所記**原稿逐句台詞**和 R9 JSON 比對，變動集合**恰是**第二輪 `review/check-flags-r8-after-risk-redo.json` 的 23 個 ID：`bly006/010/015/020/027/042/044/045/052/054/059/061/063/069/083/085/086/088/095/097/098/999a/999c`。沒有改其他 79 句、插圖提示詞、角色聲音、片頭／片尾視覺設定或 A／B 大綱；`claims.md` 只同步改寫後的逐景台詞，並為 `bly083` 加上出版物封面行號。全部指稱仍屬 Bly **1887 年第一人稱敘述**；影片沒有取得診斷、院方原始紀錄或陪審團報告原件。

## 原文覆看與逐段界線

固定來源是 GITenberg commit `c3904b5064d2bafb7e13486489dfe98b560611b5`，本地 `/tmp/s45-bly-59899.txt` SHA-256 `bc03f9cdb9a845bd4d9babaa8652c4c93e415dd09c7b54ca20c07143e5e2d5b3`。下表原文行號皆指這一版；每景的完整可點行鏈仍在 [claims.md](claims.md)。作者重新打開相關原文段落確認**語意**，尚待換人驗證口播及書面畫面。

| 改動 ID | R9 保留的事實與懸念 | 直接依據及限制 |
| --- | --- | --- |
| `bly006` | 一封送到病人手上的信引眾人追問；開場仍問原因，後文 `bly066–067` 回收。 | [第十五章 L2867–2870](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L2867-L2870)；不猜寄信者，也不說全院只收到一封。 |
| `bly010/015/020` | Bly 選化名與警察法院路徑，希望暫住處找警員；助理最後帶回兩名警員，她先到警局再到法庭。`bly015→020` 的問答仍成立。 | [第一章 L190–199](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L190-L199)、[第三章 L297–303](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L297-L303)、[第四章 L643–690](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L643-L690)、[L718–738](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L718-L738)。付款、夜間陪伴、翌晨早餐和找警員的次序未動。 |
| `bly027` | 她維持假扮，同時對醫師說自己沒病、想取回行李與回家。 | [第五章 L979–985](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L979-L985)；仍保留前後實際檢查，無「完全沒檢查」說法。 |
| `bly042` | 她說踏入島上病房後不再維持假扮，照平常說話行動。 | [第一章回顧 L223–227](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L223-L227)；這是 Bly 的自述，不能代替診斷。 |
| `bly044/045` | 醫師先問一位不會英語的女性；請護士翻譯，但護士只會一點德語，最後問到其丈夫的工作。問句由下一景直接回收。 | [第八章 L1640–1659](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L1640-L1659)；不把問話結果寫成醫學判定。 |
| `bly052/054` | 晚餐有麵包、果乾與 Bly 不喜歡的茶；一人先拿走她的麵包，另一名病人願分自己的，她婉拒。 | [第十章 L1854–1880](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L1854-L1880)；這是 Bly 對自己那餐的見聞，不作全院伙食定論。 |
| `bly059/061` | 她寫病人要做清潔工作；筆記本和鉛筆被取走，她多次要回未果，助理院長答應考慮卻未交還。 | [第十一章 L2137–2166](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L2137-L2166)；不推論私人物品制度的全貌。 |
| `bly063` | 友善是她對助理院長的評價；她向他反映寒冷，下一景只說醫師**吩咐**多給衣物。 | [第十三章 L2425–2429](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L2425-L2429)；沒有聲稱衣服已送達。 |
| `bly069` | 她反覆向醫師說自己應獲釋，得到更多懷疑，問題由 `bly070` 回答。 | [第十六章 L2929–2954](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L2929-L2954)。 |
| `bly083` | 她跨河回紐約；**後來**這本 1887 年書記下島上見聞，不聲稱在船上立即寫完。 | [第十六章 L3025–3034](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L3025-L3034)、[書名頁 L44–64](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L44-L64)；不補出院確定日期。 |
| `bly085/086/088` | 離院後不久她受大陪審團傳喚，宣誓後敘述從暫住處到獲釋；陪審團成員邀她再訪，她隨行搭船，看見新船。 | [第十七章 L3043–3068](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L3043-L3068)；`bly088` 的第一處差異仍由 `bly089` 新船回收。 |
| `bly095` | **按 Bly 記述**，一位未宣誓病人以「布朗小姐」稱她，說她離開後衣服、餐食及醫師探訪改善。 | [第十七章 L3089–3110](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L3089-L3110)；該病人當時不知道她的記者身分，不在引述裡替病人稱她「記者」。 |
| `bly097/098` | Bly 擔心院內返訪景象變了，陪審團會不支持她；下一景說**她的書記述**仍獲支持、報告建議她所提改革，同時明說本集未讀報告原件。 | [第十七章 L3143–3146](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L3143-L3146)；不是已獨立查到的陪審團報告。 |
| `bly999a/999c` | 片尾首句保留她希望促使外界改善院內生活的願望；末句只指向已在說明欄的原著固定連結。21 秒視覺片尾與訂閱卡仍在。 | [第十七章 L3043–3048](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L3043-L3048)；`video.json.youtube.description` 確有固定 URL，沒有口播要求訂閱。 |

## 本地一致性及待審事項

`node tools/video/cli.mjs script --slug curio-s45` 已重產同版腳本。`lint` **0 errors／1 已知 warning**：片尾口播不說訂閱，畫面 CTA 仍在；沒有為消警告重新引入 R6 被 Jev 懷疑的商業語氣。102/102 台詞在生成稿逐字相同、99/99 正文場景在 `claims.md` 同 ID 同台詞且有固定原文行鏈、18/18 `loops` 順序有效；正文 99 景中 96 張 `shot`、3 張文字卡。估時 300 spoken units/minute：濃縮開場 **39.80 秒**，後續主體 **505.00 秒（8:25）**；250 時開場 46.23 秒、主體 589.13 秒。這是新稿**估值**，R8 的實測 582.30 秒不能代替 R9 實音。

**下一關**：另一人重開固定原文對 R9 精確台詞與相同畫面做獨立差分；兩名真正新讀者各做官方十三題盲讀。若通過，才對**精確 R9** 做一次 `explainer` Jev 政策判讀、重送網站劇本卡並如實讀其 `hand_pushed` 狀態，然後再記本地精確選稿決定與重新合成。R8 劇本雜湊核准、政策、盲讀與音訊均對 R9 **失效**；本站也沒有 R9 站台核准。未通過前不做 R9 TTS、MiniMax、配樂、組片或發布。
