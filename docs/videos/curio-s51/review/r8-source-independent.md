# S51 R8｜史料、逐句主張與書面畫面獨立差分覆核

2026-10-20 UTC。對下列**精確 R8 五檔**，判 **旁白史料 PASS、逐句主張 PASS、書面畫面 PASS**。我從 [R7 獨立基線](r7-source-independent.md)與當時交給盲讀者的 R7 純旁白快照 `/tmp/s51-r7-narrative-current.json` 核實 R7→R8 的實際差分，再直接讀固定 1912 年英國調查原文；[R8 作者收據](../verify-8.md)只用來定位，不作證據。這不是本版兩名讀者的敘事裁決，也不是生成圖片驗收。

| 精確內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `dbb931dcccfddc12a6705c33ae79ed8d6e44cbdd33352675b2e29ca64360897c` |
| `research.md` | `039ca3ecc3f5099537e51e48d0f1788faf0bdf9c5d254f2ae64dd5ff89b56459` |
| `claims.md` | `240314a9c838f49d10c5efb184b56e6fc67ad5287471ab6c69d9cff58fef79a8` |
| `script.md` | `7886cad66f1b223494baf728ce985daca5214f3e4663d75e31344f03555cd11b` |
| `video.json` | `b0be4e53cd80dbc304fdd659261b18d8f8bbd8f064adaeb99a8641706d1c5060` |

三份固定原文位元組仍吻合研究登記：英國正式調查 G `/tmp/s51-independent-sources/british-report.txt` SHA `5ac8c66266f84fb1fd01f50aab93044526c369df0d876c7e24dd20451f0053bd`、Beesley B SHA `58062b750f1737ac908af48f3ec81016353404631978dc419138a5a2ef7a5ce9`、Gracie A SHA `d9ab71205530a5df41dddf74090e598fcc4de06efba9eb234bffa07f20a61a1f`。R8 未改研究與 B／A 原著的旁白；保留 R7 對目擊、事後報告歸納及不能確定反事實人數的分界。

| R8 變動 | 獨立原文核對與界線 |
| --- | --- |
| 刪 `cal032` | G [L3340–3354](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3340-L3354)記唯一無線電員 Evans 約 23:30 休班；[L3182–3197](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3182-L3197)記加州人號沒收到鐵達尼號求救電文、該員已睡。刪掉正文再次摘耳機的 `cal032` 不漏失必要事實：開場 `cal004` 已有 23:30 動作，`cal033` 說沒有第二人接班，未改的 `cal060` 具體回呼並首次揭曉漏收。主張表 `cal060` 仍有 R03／R05 錨點，不推成整個船橋都無人。 |
| `cal053` 與 `cal054` | G [L3163–3173](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3163-L3173)記 00:15 的 CQD、00:25 前算出正確船位，隨後發「Come at once」求援；同報告的各船收報附表 [L5269–5281](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L5269-L5281)更直接記 00:25 報**修正後位置**與立即求援。因此 `cal053`「幾分鐘後……補發船的位置」與 `cal054`「報文還催……立刻來援」各自有支持，不必再念 `cal046` 已說的撞冰。這是報告重建的通信時序，不聲稱加州人號當晚收到。 |
| `cal134` | G [L3428–3435](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3428-L3435)將白火箭通報與「有新消息派實習生再報」歸於 **Stone 自述**。新句「還記得史東通報火箭嗎？他說船長還交代了什麼？」只問其後證詞中的新細節，由未改的 `cal135` 回答；沒有把 Stone 的話寫成 Lord 本人獨立證實，也不再重說 `cal133` 的 Carpathia 救援。主張表的 R07 錨點及限語符合原文。 |

我將 R7 盲讀 payload 的 136 句與 R8 JSON 的 135 句按 ID、字面比較：**只刪 `cal032`，只改 `cal053/054/134`，沒有新增或其他改句**。以 Git 中 R5 的分鏡提示詞及 [R7 獨立差分](r7-source-independent.md)核對：五張被刪的提示詞為 `cal032/034/109/113/137`，唯一留存文字改動是 R6 的 `cal106` `desk`→`table`；R8 新增刪去 `cal032` 景，**其餘 132 個 `shot` 提示詞逐字保留**。`cal053` 的無字船位紙、`cal054` 的後來日間證據桌與 `cal134` 的無字路線卡只作卡通示意，不冒充可讀原件、當夜船員已認船名或真實路線重建。這些是**書面提示詞**判斷，生成後仍須原尺寸審視。

獨立解析 `video.json` 得 **133 景、135/135 個唯一台詞 ID**；`claims.md` **135/135** 同 ID／同序／同文，`screenplay(doc)` 與 `script.md` 逐位元一致；**132/132** 正文 `shot` 提示詞非空，**16/16** 伏筆 setup/payoff 存在且順序正確。`lint --slug curio-s51 --json` 回報 **0 errors、0 warnings**；`git diff --check -- docs/videos/curio-s51` 通過。最快的 325 單位／分文字估時：首八景 **36.37 秒**、其後正文到片尾前 **520.93 秒（8:40.93）**；這不是實測 TTS。

**裁決：R8 旁白史料 PASS、逐句主張 PASS、書面畫面 PASS。** 只綁上表五檔。`video.json` 的 YouTube 說明仍寫「獨立史料覆核及成片製作仍待完成」；前半句在此審核後過時，上架前須依後續狀態改寫並重綁雜湊。兩位全新隔離讀者的敘事、政策、站台、TTS、插畫和成片仍須各過自己的關卡；本報告不聲稱其完成。
