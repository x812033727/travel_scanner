# S50 R4｜測量員敘述窄修與作者凍結

2026-10-20 UTC。依 [R3 獨立來源／書面畫面 HOLD](r3-source-independent.md)，只窄修 `fire008/073/078` 口播與 `claims.md` 同列，以及 `fire073` 一條待畫提示詞。這是**作者自檢**；不是 R4 獨立來源 PASS、正式雙盲敘事 PASS 或網站／媒體核准。

| R4 內容檔 | SHA-256 |
| --- | --- |
| `brief.md`（同 R3） | `60040a61dcf7b2b4b62bba30773537d4c559104724a7f6d83926082211d983e1` |
| `research.md`（同 R3） | `109557d74963733a6b8b3715739d49ec1d68648f5f34a7c9e10d52a9f940e6c7` |
| `claims.md` | `41ebfffe54f72c0fda9f1fd563d90613efb2dbb6757e2d49a8f2e832558b4805` |
| `script.md`（工具重生） | `81766925948a74b1915ae86754e1ca01db1c187c3cdd092d73970e2137435e23` |
| `video.json` | `0fa7b40caee68e8d475827ca551d14b15eac14d7f85fec68c0497cd4f80d7a1f` |

R3 覆核者核對固定 A 1667 刊本 [L148–168](https://github.com/textcreationpartnership/A63385/blob/4ac29739d661a1c7f2a34f51ffb8a1811176f146/A63385.xml#L148-L168)：它列測量員的城牆內外受損與未燒面積，**沒有**記他們進街、開始工作之日或使用量尺。R4 改為：

| ID | R4 口播／畫面差分 |
| --- | --- |
| `fire008` | 「測量員後來留下城區受損數字；一間麵包屋，真的毀了倫敦嗎？」只預告後出的數據；不畫或聲稱他們進街。原有高處望城的卡通示意提示詞未動。 |
| `fire073` | 「同一本證詞集還記下測量員的另一組數字：燒過的土地。」接在 `fire072` 的刊本日期後，不設定量測開工或完成時點。提示詞改為一人翻無字印本，移除用尺量紙。 |
| `fire078` | 「若不看未燒的數字，後面的房屋總數就容易被聽成『整城都沒了』。」這是對 A 同段未燒面積與房屋總數的解讀，不再稱具體量尺動作；原有未損街屋的卡通示意未動。 |

`node tools/video/cli.mjs script --slug curio-s50` 重生逐句稿，敘事短碼 `19413b33ed23e68f`、語音短碼 `9a6ba286b2cd0bd3`。直接解析五檔：`video.json`、`claims.md`、`script.md` 的 **119/119** 個 ID、文字與順序全相同且 ID 不重複。`lint --slug curio-s50 --json` 為 **0 errors／0 warnings**、119 句、2,438 spoken units；`git diff --check` 通過。`estimateTimeline` 含場景停頓，250／300／325 CPM 的 8 景濃縮開場約 **48.2／41.4／39.0 秒**，開場後至 `fire116` 正文約 **643.1／552.6／520.3 秒**；最快估速仍超過 8 分鐘，尚非實測語音。

R3 對其餘直接 Pepys、Vincent 與 A 刊本事實、書面畫面的獨立覆核結論不因這四個字串改動自動覆蓋新版；須由另一人對 R4 差分再核。Gazette `fire037` 和 London Museum `fire108` 仍只依 P17 既有查核，代理 CONNECT 403 下未直接重開原站。R4 需兩名真正隔離、**只讀精確劇本**的新讀者正式盲評後，才能考慮網站及 TTS；此輪沒有圖、配樂、成片或上傳。
