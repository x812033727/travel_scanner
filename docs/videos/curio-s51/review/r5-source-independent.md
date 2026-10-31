# S51 R5｜報告日期與結尾證詞的獨立差分覆核

2026-10-20 UTC。對 [R5 作者凍結](../verify-5.md)的精確檔案，**旁白史料 PASS、書面畫面 PASS**。本查核不替 R5 劇本雙盲、政策、站台或媒體簽核。

| 內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `dc63da9f3e730abe8dcc07e76a44cae1cd62ff0c9e6f246a55d1b858cdd2be38` |
| `research.md` | `039ca3ecc3f5099537e51e48d0f1788faf0bdf9c5d254f2ae64dd5ff89b56459` |
| `claims.md` | `88f1611b379dd230564aa44938439f818f31de6d227b3667bdf6e65e48028cfa` |
| `script.md` | `dcebb60865b561b5b38b5bb163fdd18b9961dbb26e1676903f47167fc4abba8d` |
| `video.json` | `1e8feed428c617ced77d251a328f1b75ba8d498cf103e11bee51720a6ee59b22` |

重開固定英國調查報告 `/tmp/s51-independent-sources/british-report.txt`（與 [R4 獨立覆核](r4-source-independent.md)相同位元組，SHA `5ac8c66266f84fb1fd01f50aab93044526c369df0d876c7e24dd20451f0053bd`）。G [L143–166](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L143-L166)寫正式報告日期 **1912-07-30**；[L205–210](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L205-L210)明列 **05-02 起已開庭**。R5 `cal107`「到了七月底，英國正式調查**報告**逐一對照船橋證詞」正確指後出的報告，避免 R4 把調查開始延至數月後的歧義；主張列已加入兩個日期錨點。畫面改為日間後續報告桌、無字頁與無標記冊，不把七月報告畫成五月開庭現場。

G [L3428–3435](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3428-L3435)以「**He states**」歸於值班員 Stone：他稱船長說繼續打摩斯，有消息就派實習生來報。R5 `cal135` 清楚先說「史東說」，沒有把此細節當多名證人一致直接聽見；調查報告 [L5677–5680](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L5677-L5680)確認加州人號沒有嘗試前往，故「當下沒有起航指示」與可見行動相容，不推斷船長心理。`cal136` 將 Stone 說五枚與船長只記得一枚的證詞差異接回前文；G [L3473–3481](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3473-L3481)記此矛盾，稿子仍不說船長當夜確知 Titanic 船名。`cal135` 的匿名日間證據桌、無字通話管／訊號燈／信差符號卡是後來整理證詞的示意，沒有捏造當夜可讀原件；`cal136` 原有無字兩頁亦合格。

查 140/140 台詞、主張列與重生劇本按 ID、順序、字面相同；137/137 正文 `shot` 提示詞非空且其餘內容沿 R4 已審界線。`lint --slug curio-s51 --json` 為 **0 errors、0 warnings**，`git diff --check` 通過。R5 的兩名新隔離讀者仍須就 `cal135/136` 是否真正回收問題、無重述作完整劇本裁決；此來源 PASS 不代替敘事 PASS。
