# S51 R4｜固定來源與書面畫面獨立差分覆核

2026-10-20 UTC。**R4 旁白史料窄 HOLD，僅 `cal107` 的調查時序／文件層級；新增的 `cal135/136` 書面畫面 PASS。**我未參與 R4 作者改稿，重新讀取三份固定電子轉錄，檢查 [作者凍結](../verify-4.md)所列的改句、主張錨點、企劃及 16 組伏筆，並核對整稿一致性。這是文字及提示詞檢查，沒有生成圖片、旁白、配樂或成片，也不代替兩位新讀者的敘事盲評。

三份直接使用的固定轉錄本位元組 SHA-256：G `/tmp/s51-independent-sources/british-report.txt` `5ac8c66266f84fb1fd01f50aab93044526c369df0d876c7e24dd20451f0053bd`；B `beesley.txt` `58062b750f1737ac908af48f3ec81016353404631978dc419138a5a2ef7a5ce9`；A `gracie.txt` `d9ab71205530a5df41dddf74090e598fcc4de06efba9eb234bffa07f20a61a1f`。它們與 `research.md` 固定版相符，都是電子轉錄，非原件掃描。R3 [完整來源與畫面覆核](r3-source-independent.md)及 [`cal061` 主張差分](r3-claims-diff-independent.md)對未改句的 PASS 界線仍適用。

| R4 內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `c31916177aea257b69a53415916241ade95a473d07b18db5cc4231a41b8363cb` |
| `research.md` | `039ca3ecc3f5099537e51e48d0f1788faf0bdf9c5d254f2ae64dd5ff89b56459` |
| `claims.md` | `38b59f59d0155cb8ecd82b3433a2914a810ab5e331eb0f935c3203cad60fe6f1` |
| `script.md` | `7d84f152e2051430ec5ca034e79a19f743061af221531232bb44292f94c0583c` |
| `video.json` | `fd6fc00c3db43f7da576292e62317eb61aaa685af8dcf2f59500865cb87eb492` |

## 改句與來源

| 景 | 核對結果 |
| --- | --- |
| `cal008` | **PASS。**白火箭之後是否有人啟航仍是提問，沒有先洩漏調查結果。[G 3182–3197](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3182-L3197)、[G 3420–3442](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3420-L3442)分別給出火箭及船橋觀察；不從問句推斷船長已辨名。 |
| `cal020/022` | **PASS。**[G 3338–3358](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3338-L3358)只記船燈與 Evans「我想 Titanic 在附近」及約五至七英里的船方估計。稿子把無線電員的附近推測與未靠目視辨名分開，沒有說遠船身份當場已確定。`cal020` 的「沒貼近到能看清船名」是遠距只見船燈的保守敘述，不作光學距離測量。 |
| `cal024/025` | **PASS。**[G 3340–3351](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3340-L3351)直接記加州人號「停住，周圍是冰」的訊息、鐵達尼號回話與干擾背景；沒有捏造更多對話。 |
| `cal061–064` | **PASS。**[G 3192–3197](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3192-L3197)支持單一無線電員睡去，不能等同船橋無人；[G 3420–3442](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3420-L3442)記值班者與白火箭；[G 3182–3187](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3182-L3187)直接記首枚約 00:45。`cal061` 已同列 R05/R07，口播沒有把兩船各自看見的時刻合併成精確同步。 |
| `cal106` | **PASS。**[G 3483–3501](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3483-L3501)記夜船影消失、清晨另一艘船、約 06:00 才知事故並啟航；下一步查船名是後來調查的問題，不把清晨新船說成夜船。 |
| `cal107` | **HOLD。**現稿「**幾個月後，英國正式調查逐一對照船橋證詞**」容易說成調查在幾個月後才開始；固定 G [L205–210](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L205-L210)明記 **4 月 23 日任命調查委員、5 月 2 日開庭**，距沉船僅十餘日。[G 143–166](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L143-L166)則明記**正式報告 7 月 30 日成文**，確是幾個月後；[G 3525–3542](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3525-L3542)正是報告對照證詞與火箭數的推論。`claims.md` 的 `cal107` 只連 R11，`research.md` R11 只連後段推論，沒有日期錨點。最小修法為「**到了七月底，英國正式調查報告逐一對照船橋證詞。**」並在 R11 或 `cal107` 同列 G 143–166 日期錨點；這既分清 5 月開庭與 7 月報告，也不改後文判斷。現有 `cal107` 公開聽證桌卡通示意本身可用，但若改說**報告**，改成日間後續證據／報告桌更不易把報告日期畫成當天開庭。 |
| `cal133–136` | **PASS。**[G 3207–3219](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3207-L3219)記卡帕西亞號 04:10 接上首艇時 `just daylight`；[G 3192–3197](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3192-L3197)與 [G 3427–3440](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3427-L3440)支持無線電漏收、Stone 說火箭通報後仍只獲「續打摩斯」回應，[G 5677–5680](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L5677-L5680)記最後沒有嘗試前往。[G 3473–3481](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3473-L3481)的船長與值班員證詞有矛盾；不把他**當夜已知船名**或能救人數當定論。B [L2636–2659](https://github.com/GITenberg/The-Loss-of-the-S.-S.-Titanic--Its-Story-and-Its-Lessons_6675/blob/98d777343615ef35522ca8e04e451ec5d7f37eb3/6675.txt#L2636-L2659)主張暫緩判斷蓄意忽略，A [L624–640](https://github.com/GITenberg/The-Truth-about-the-Titanic_67584/blob/a2cbb33f09c5ce0ff00a78581a56cb6756967c42/67584-0.txt#L624-L640)的指控是當事人事後解釋，稿子未誤作直接目擊。 |

## 畫面、對齊及界線

R4 新增的 `cal135` 是**匿名日間證據桌**上兩張無字耳機／訊號燈圖示卡，不是當夜原件或可讀調查書頁；`cal136` 是後來日間兩頁無字證詞示意，不指名、描出 Lord 肖像或假造原文；兩景**書面畫面 PASS**。其餘正文提示詞沿 R3 已獨立審的畫面邊界；新旁白與同景提示詞沒有新增明顯衝突。`cal107` 的公開聽證桌場景與調查本身相容，但上述稿句／日期錨點須先修；生成後仍要原尺寸檢查人物、船燈、火箭、錯字和文件。

機械核對：`video.json` **138 景、140 個不重複台詞 ID**，137／137 正文景是有非空提示詞的 `shot`；`claims.md` **140／140** 與 JSON 同 ID／同文同序，`script.md` **140／140** 口播同文同序，16 組 `loops`。`node tools/video/cli.mjs lint --slug curio-s51 --json` 為 **0 errors、0 warnings**；`git diff --check` 通過。這些靜態檢查不解除 `cal107` 的史料層級 HOLD，也不等於盲評或實際影片通過。

**下一步：**作者只修 `cal107` 的調查／報告時序與日期錨點，必要時同步一景提示詞，重生劇本、重算五份內容 SHA；另一位工作者按新雜湊獨立檢查該差分。新版兩位全新隔離讀者的劇本盲評、網站關卡與媒體製作仍待，不應把 R4 的史料或畫面標成全過。
