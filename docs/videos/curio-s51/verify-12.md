# S51 R11｜六句音訊易誤聽台詞的作者凍結

2026-10-20 UTC。[R10 三輪完整音檢](verify-11.md)在原版 134 句中仍留 `cal021/049/073/096/099/120` 六句 Jev 旗標；兩輪定點重錄已結束。本版只為這六句改成來源忠實、較不會被同音字誤聽的口播，並讓 `cal099` 書面分鏡對上新稱謂。這是**作者候選**，不是獨立史料、兩名新讀者、政策、網站劇本卡或新版音訊的 PASS。

| ID | R11 口播與修訂理由 | 固定來源界線 |
| --- | --- | --- |
| `cal021` | 「船長於是去問無線電員。」以來源具體動作避開「船橋／船長」同音誤聽。 | [G L3338–3342](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3338-L3342)明記船長到 Evans 房間詢問附近船隻；不因此確定目見遠船的船名。 |
| `cal049` | 「那麼，還有什麼訊號能讓別人明白，船上正在求救？」避開「危急／危機」同音差異，仍只是帶入下一章的問題。 | [G L3163–3197](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3163-L3197)分記無線電求救與白火箭；問句不稱加州人號已接到電文。 |
| `cal073` | 「英國調查報告說，波克索爾大約放了八枚火箭。」以人名直接作主語，移除「估他」造成的錯誤斷句。 | [G L3189–3193](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3189-L3193)原文為 `about eight`，保留約數。 |
| `cal096` | 「他再次保證，自己看到的火箭全是白色。」前兩句已明指史東，避開「史東／始終」同音誤聽。 | [G L3470–3474](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3470-L3474)是史東自述，不把船長的歧異記憶抹去。 |
| `cal099` | 「接班的大副，這時聽到夜班的火箭報告。」以確切職務避開「主官／主管」，同一景 prompt 的 `watch sailor` 改 `chief officer`。 | [G L3483–3491](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3483-L3491)明記史都華為接班大副，史東告知夜間火箭。 |
| `cal120` | 「若要靠比對時間推測遠船是誰，距離又能估得多準？」以自然問法避開「船名／船民」。 | [G L3525–3542](https://github.com/GITenberg/Loss-of-the-Steamship-Titanic-_39415/blob/1ca79cda2f11138809615859c7f80f80ffea951a/39415.txt#L3525-L3542)是調查以時序推斷船名並估距，不是當夜船橋看清船名。 |

固定 G 原文為 `research.md` 登記的 1912 年英國正式調查電子轉錄 `/tmp/s51-independent-sources/british-report.txt`，SHA-256 `5ac8c66266f84fb1fd01f50aab93044526c369df0d876c7e24dd20451f0053bd`。本版未改 `brief.md`、`research.md`、其餘 128 句、16 組伏筆、聲線、片頭片尾、音訊或任何站台資料。

| 內容檔 | R11 SHA-256 |
| --- | --- |
| `brief.md` | `ad22f35f5d9ff6a17e055f27b4b6eaaf921f22856b15445531db5a4caf087837` |
| `research.md` | `039ca3ecc3f5099537e51e48d0f1788faf0bdf9c5d254f2ae64dd5ff89b56459` |
| `claims.md` | `ce27dbd797c995ca367316f67b4ca0136cb21988bc9c1b84a07be842012abf8f` |
| `script.md` | `b0aed4b7b269130a717b290386b32f095b55c8a94a444db27221b1d2bf7f2c8e` |
| `video.json` | `02205af4ef7b94393c57307fd25209054f96f1f6148d60b6d73df746b55f2556` |

本地機械檢查：`claims.md`、`video.json` **134/134** 同 ID、同序、同文；CLI `screenplay(doc)` 與 `script.md` 逐位元一致；**131/131** `shot` 提示詞非空、**16/16** 伏筆在場；`node tools/video/cli.mjs lint --slug curio-s51 --json` **0 errors／0 warnings**；`git diff --check` 通過。最快 325 CPM 文字估時：前八景濃縮開場 **36.37 秒**，`cal009` 至 `outro` 前正文 **8:38.60**，全稿 **9:26.63**；這不是新版本的實測 TTS，R10 實測時長不能沿用為新版放行證據。

下一步：另一位工作者按上述五檔雜湊重新核六句來源、主張與改動的一景書面畫面；兩位全新只讀 R11 `script.md` 的讀者各答固定 13 題並正式合併。全部 PASS 後才重跑完整解說政策與網站劇本卡綁定，再只合成六句、完整查 134 句到零旗標。此前 **音訊、插圖、配樂、成片仍 HOLD**。
