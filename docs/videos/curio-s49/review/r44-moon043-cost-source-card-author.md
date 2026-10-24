# S49 R44｜`moon043` 來源限定估價字卡作者凍結

2026-10-22 UTC。**書面候選；本輪沒有付費媒體或私人 manifest 重綁。**`moon043` 兩張原圖已分別因假提案字樣、空桌與年代畫風失準而 [R42](r42-moon043-first-native-stop.md)、[R43](r43-moon043-second-native-stop.md) HUMAN REJECT。改用來源字卡，不再為本景買第三張圖。

固定 Locke 名下 1859 年重印本 P05 L447–468 把 **七萬英鎊估價**及**國王允諾所需資金**寫進虛構報導；Jacoby 1902 的後出評論並不核實王室撥款。`moon043` 保留原旁白「報導估計要七萬英鎊，還寫國王允諾提供所需款項。」；畫面改為三行文字：上標「1859 重印本所載虛構報導」、主文「製鏡估價：七萬英鎊」、下標「故事還稱國王允諾出資；非真實撥款證據」。claims 同列明定這是中文意譯，並非 1835 原報、王室付款憑據或真工程帳冊。字卡不需要生成任何可能冒充史料的提案紙。

`moon043` 由 `shot` 改成 `big` 後，插畫比例變為 **116/128（90.625%）**，`big` 共 12 景、最多連續 2 張。原本含 `window` 的提示數 39/116 使全域 lint 出現一項比例警告；因此將**未畫的** `moon049` prompt 與 claims 畫面欄中單一光線詞 `warm window light` 同步改為 `soft indirect light`。該景仍是虛構報導中的 1830 年代成年工匠、模型鏡片和無字轉動架；來源 P05a、動作、旁白與 camera 不變。這是必要的書面視覺詞調整，不涉及既有 34 張 KEEP。

[逐字可逆差分](r44-moon043-cost-source-card-structured-diff.json) SHA-256 **`b96891d9001f30412318ece364c26412cbf74e445d4aef55afa69ffc0cc93b30`** 對 Git `e1203389c`：舊 `video.json` SHA `a8ff417f10c16f338e1c54889f2facc1adb667c9e666719e7cb764d8df3b8bbc` → 新 **`dd2dae850cdf455a01b9c99a01af2d9ef3370d81d11c7349f661d6a6220f8d9c`**；舊 `claims.md` SHA `830c773942487158451b16701e3edb85a56210ffbe9572e33dbafebe219ae234` → 新 **`70f0d9255397880586c96a49cbda77cf3ca722b68815455f29b6ac9f841c2ebb`**。只改 `scenes[39]`、`scenes[45].data.prompt` 和相同兩列 claims 畫面欄；逆填後兩檔逐位元還原，其他 127 景、全部 131 句、`script.md` SHA `82369f762cc64f70e300e2104a16af3b8e99f1e3296dd81a34152e967f0ecb0a` 和 `research.md` SHA `f5da15ac571478389b9b9920832f79434f83af0d312cb84747dcdb680a667750` 未改。新 `visual_hash=99b36fbfea602f3c`，`speech_hash=96f0b30e8cb408c7`；CLI lint **0 errors／0 warnings／131 lines**。

私人 STOP 在位、jobs `{}`；active manifest 尚綁 R43 的 `visual_hash=cac48ccf7b76a189`，SHA **`88bc9a66b04e212418d5261da3faf169fadcebf3a0fbba12f9ddf4c2d7a23ff6`**，34 KEEP 入選圖未更動。ledger SHA **`b6ba6f57fd69c85743396c7eaaf333c80057dc0c633a11d8b7bd663c5b39a850`**，實花 **US$1.2960／96 image／96 judge／0 預約**。此書面修訂使待畫景數預期由 83 減至 82；需非作者先核固定來源、逐字差分及 1920×1080 實際字卡。**PAPER PASS 前不重綁 manifest，也不付費畫 `moon044`。**整集 storyboard、網站聽音與成片仍 HOLD。
