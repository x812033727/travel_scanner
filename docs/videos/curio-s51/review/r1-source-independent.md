# S51 R1｜獨立史料與書面畫面覆核

2026-10-20 UTC；另一位覆核者在**作者凍結後**，重新下載三份固定 Git 提交的原始文字，直接讀原文，再對本版 A 案 140 句旁白、逐句主張、137 個正文 `shot` 提示詞與企劃做覆核。這不是圖像生成驗收，也不是敘事盲讀、網站核准或原始紙本掃描認證。

| 凍結內容 | SHA-256 |
| --- | --- |
| `brief.md` | `82a2e4a3d7a240dd0f249eeeec3b3dffdf1446d9eb049432320e72fe6b6a1023` |
| `research.md` | `039ca3ecc3f5099537e51e48d0f1788faf0bdf9c5d254f2ae64dd5ff89b56459` |
| `claims.md` | `21dd50280e0d89ca998a9cf5a0820589b6ae5ffbf233e49ba988aa6dd477dad1` |
| `script.md` | `5b6c6d0924670033b379c40a00f4ae3991d920661a5479631e5ba2e3143de42b` |
| `video.json` | `1639fd758d59f44b7dbae66603f1148c3abf7dd6229f16b32b3c5b34bdcf20df` |

**固定原文重新下載成功。** [G：英國 1912 年正式調查的美國參院文件轉印電子文本](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt) SHA `5ac8c66266f84fb1fd01f50aab93044526c369df0d876c7e24dd20451f0053bd`；[B：Beesley 1912 年自述](https://github.com/GITenberg/The-Loss-of-the-S.-S.-Titanic--Its-Story-and-Its-Lessons_6675/blob/98d777343615ef35522ca8e04e451ec5d7f37eb3/6675.txt) SHA `58062b750f1737ac908af48f3ec81016353404631978dc419138a5a2ef7a5ce9`；[A：Gracie 1913 年自述](https://github.com/GITenberg/The-Truth-about-the-Titanic_67584/blob/a2cbb33f09c5ce0ff00a78581a56cb6756967c42/67584-0.txt) SHA `d9ab71205530a5df41dddf74090e598fcc4de06efba9eb234bffa07f20a61a1f`。獨立下載檔在 `/tmp/s51-independent-sources/`。這些是固定**電子轉錄**，沒有把 G 冒充為已逐頁驗看的原始掃描；G L3327–3329 與 L3509–3513 對停船經度的 `57/50` 不一致，所以旁白不報座標，也不把距離當測定值。

## 史料旁白：PASS

| 旁白 ID | 直接核到的原文及邊界 |
| --- | --- |
| `cal001–034` | G [L3292–3351](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3292-L3351) 記 4 月 14 日 19:30 冰山警告、約 22:20 停船、23 時前後船燈、Evans 說 Titanic 或在近處、送「停住且周圍有冰」、`Keep out` 及 Cape Race 強弱訊號、23:30 休班。G [L3192–3197](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3192-L3197) 說只有一名無線電員、睡著而未聽見求救；開場沒說船橋親眼認出船名。 |
| `cal035–049` | G [L3353–3427](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3353-L3427) 記 Groves 約 23:40 看見船燈減少，卻仍見航行燈；轉向可能遮燈，摩斯燈未獲可靠回訊，Gibson 起初把閃爍桅燈當摩斯又放棄。稿中「說／猜／可能」維持證詞層級，未斷言遠船全船熄燈。 |
| `cal050–075` | G [L3163–3197](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3163-L3197) 記 00:15 CQD、00:25 正確位置與「Come at once」、Carpathia 約 58 英里外回訊、Boxall 約 00:45–01:45 從 1 號緊急艇旁座發出**約八枚**白星點火箭且向遠燈打摩斯未得答；B [L1287–1305](https://github.com/GITenberg/The-Loss-of-the-S.-S.-Titanic--Its-Story-and-Its-Lessons_6675/blob/98d777343615ef35522ca8e04e451ec5d7f37eb3/6675.txt#L1287-L1305) 是 Beesley 本人從 Titanic 甲板見火箭，沒有聲稱他親見 Californian 船橋。 |
| `cal076–105` | G [L3420–3501](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3420-L3501)：Stone 說 01:10 向 Lord 報五枚、Lord 問是否公司訊號並讓他續打摩斯；Gibson 說又見三枚、約 02:05 報總數八枚；Lord 只記得一枚且不記得後續，三人的說法衝突；02:40 Stone 報夜船燈影消失；約 04:00 **另有一艘船**出現，Lord 一度混淆；約 06:00 才由無線電得知 Titanic 出事並啟航。劇本沒有從通報矛盾推斷 Lord 當時已知船名。 |
| `cal106–137`、`cal999a–c` | G [L3516–3550](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3516-L3550) 明說證人互相矛盾，但調查按停船、約八枚火箭、消失時刻**認定**所見為 Titanic；未找到吻合的第三船；根據船長目測及其他資料估可能較五英里更遠、但不超過八至十英里。G [L5670–5680](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L5670-L5680) 正式答覆「可抵達／未嘗試」。G 的「可能救許多人」是反事實推估，稿中沒有換算成確定救出人數。G [L3207–3223](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3207-L3223) 支持 Carpathia 收訊轉向與 04:10 接首艇，沒有說兩船航路同難度。B [L2612–2646](https://github.com/GITenberg/The-Loss-of-the-S.-S.-Titanic--Its-Story-and-Its-Lessons_6675/blob/98d777343615ef35522ca8e04e451ec5d7f37eb3/6675.txt#L2612-L2646) 同時提另一未知船說法，並主張暫緩對故意忽略的判斷；A [L578–649](https://github.com/GITenberg/The-Truth-about-the-Titanic_67584/blob/a2cbb33f09c5ce0ff00a78581a56cb6756967c42/67584-0.txt#L578-L649) 較強烈控訴，但那是 Gracie **事後**意見，旁白沒有沿用其船長心理與定距指控。 |

逐句機械校對：`video.json`、`claims.md`、`script.md` **140／140** 個 ID、次序及字面相同，無重複 ID，含三句片尾；137 個正文景全部是 `shot` 且每景有提示詞。`lint --slug curio-s51 --json` 為 **0 errors／0 warnings**。A／B 選案把 A 的單船值班線與 B 的倖存者跨船線明列，推薦 A 並公開界線；最快 325 CPM 的靜態開場約 36 秒、後段正文約 519 秒，只是估時，尚非音檢。片頭與片尾配置、史料和頻道 URL 已寫入企劃與 YouTube 說明文字；沒有真實私人上傳或可點片尾元素。

## 書面畫面：HOLD（只限提示詞）

逐讀 137 個 `data.prompt`，未見命名的 Lord 肖像、來源文件可讀字、地圖固定座標、五英里定值、實景照片或傷亡畫面；這些邊界可保留。以下是**書面畫面**的具體衝突，不把旁白來源 PASS 外推到它們：

1. `cal004/008/016/028/032/040/044/052/064/068/072/076/080/088/092` 的提示詞同時把事件或場景寫成 **at night／late at night**，又以 **pale dawn light** 照亮。對 23:30 摘耳機、00:45 火箭、01:10 船橋報告、02:05 再報總數等明確夜間時刻，這會畫成黎明並倒置時間感。`cal001/003/005/025/029/037/049/053/061/065/077/085/093` 等夜景也套入 `gentle grey skylight` 或 `soft overcast light`；至少應把含 `pale dawn light` 的夜景換為艙燈、月色或暗夜天光，並逐一確認其餘夜景不是白日陰天。
2. `cal089/091/092` 把 02:05 前後的**加州人號夜間船橋**同時寫為 `one inquiry clerk/historian` 在船橋桌旁讀證詞，`cal089` 甚至說 `by daylight`。史料裡那時是值班員的報告爭議，調查是在事後進行；應在畫面上選「當夜船橋」或「事後日間證詞桌」，不要混成船上正在審證。`cal067` 也把當夜 Titanic 甲板與白日 `records keeper` 同框，需明確分開敘事與資料示意。
3. `cal118–119` 說的是 Beesley **書中**對未知船與故意不理的保留意見，提示詞卻把一名倖存者放到 `1912 public hearing table` 寫筆記；已固定原文只證明書中陳述，並未證明 Beesley 曾在該英國調查桌發言或寫作。改成不定位於聽證現場的私人書桌／空白書頁示意即可。
4. `cal098` 是約 04:00 新船被見，提示詞寫 `at first light`；G [L3483–3495](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3483-L3495) 只給約四點，未給曙光；可用「before dawn／dark horizon」避免強加天色。`cal028` 的 `wireless needle`、`cal052` 的 `signal meter` 也不是已引用原文所證實的接收畫面；優先畫不帶可讀數值的耳機、電鍵與值班者，避免發明儀器所示訊號。

**結論：旁白史料 PASS，書面畫面 HOLD。** HOLD 只需修上列提示詞，不要求改 140 句口播或 A／B 企劃。修後應重新固定五個內容 hash，由另一人對提示詞差分覆核，再進站台／付費媒體關卡。兩名新讀者可以對**現行未改的旁白**做敘事盲評，但若後來更動台詞，須重盲；本次沒有做音訊、圖像實物或網站核准。
