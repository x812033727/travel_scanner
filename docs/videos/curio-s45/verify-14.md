# S45 R8｜作者來源差分與凍結收據

2026-10-20 UTC。這是 **R8 作者自檢**，不是獨立來源／書面畫面覆核，也不是兩名新讀者的敘事裁決。[R7 雙盲](verify-13.md)兩人共同把必答 `no_recap` 判 No，R7 敘事 **FAIL**；R7 不能進政策或付費媒體階段。本版專修其指出的重述、未回收問題和彈琴旁枝。

| 凍結輸入 | SHA-256 |
| --- | --- |
| `research.md`（1887 固定來源，未改） | `97b91f2344190fbc424fd29eca17da2bee372673bdc7fd36e7161e13ef31ab65` |
| `brief.md` | `965d4f46b1b90cad9d52882ca5187003c42ca9a897debc874fbc0937d5a40909` |
| `video.json` | `c3fa833ef6f60de7e3ef90e1fc7436d72add3c6a30d3756b6a97bfbaaa28d4ce` |
| `script.md`（由同版 JSON 生成） | `6210aa1a85ca1e69ee01a3cfe9ce5a970336b262cdc3beb8cd1e944f1da1603e` |
| `claims.md` | `ef580d790746cd89d3cdb2c526111ee3ed32e80e4cdd1eaefca09471abcdf344` |
| 本地原著 `/tmp/s45-bly-59899.txt` | `bc03f9cdb9a845bd4d9babaa8652c4c93e415dd09c7b54ca20c07143e5e2d5b3` |

原著對應 GITenberg commit `c3904b5064d2bafb7e13486489dfe98b560611b5`；[固定全文](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt)。站台與舊 `approvals.json` 裡的 A 案／劇本指向舊版雜湊；`brief.md` 本輪因換掉歌曲段與更新候選狀態而改版，**舊本地大綱雜湊註記不得冒充 R8 大綱核准**。站台 `hand_pushed` 卡仍 pending。

## 必查來源與敘事差分

| 場景 | R8 精確修訂／自檢 | 固定版原文 |
| --- | --- | --- |
| `bly055` | 用飯後依令在走廊列隊、鎖門打開才能回起居室，取代鋼琴段；這一動作連接餐桌與院內受管制的動線。畫面僅一名成人在普通走廊等門，沒有以 AI 圖重演集體監禁或上鎖者。 | [L1890–1893](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L1890-L1893) 的 `orders to form in line`、`doors ... unlocked`、`proceed back to the sitting-room`。 |
| `bly062–064` | 長談設問、她反映寒冷、醫師叫來 Grady **吩咐**多給衣物，下一景直接交代新的回應，不重述申訴；沒有說衣物已送達或病房變暖。三張圖分別示意普通會談入口、坐下反映、醫師向門口叫人。 | [L2425–2429](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L2425-L2429) 的 `long conversation`、`complaint of the cold`、`called Miss Grady ... ordered more clothing`。 |
| `bly097–098` | 返訪後她擔心陪審團不支持她；下一景按**她的書中說法**答「仍支持，報告建議改革」，同時明說未讀報告原件。文字卡是問句而非事實判決；空白文件插畫不是報告重製，也未再講「她出院、別人仍留下」。 | [L3143–3146](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L3143-L3146) 的 `I hardly expected`、`Yet they did`、`their report ... advises`；原始報告未取得。 |
| `bly999b` | 片尾改問觀眾在這份第一人稱記錄裡**哪一幕**最想另找證詞；這是可由觀眾回答的判斷，沒有假設已讀原始陪審團報告，也沒有拋出影片必須回答的新事實題。 | 問句是觀影選擇；`bly999a` 的 Bly 自述來源仍見[第十七章 L3043–3048](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L3043-L3048)。 |

`bly097→bly098` 加入第 18 條明確回收；其餘回收沿用舊版。`bly099` 與片尾首句沒有改動，請新讀者獨立判斷全段是否仍顯得重複。研究表 P09 保留鋼琴作為來源中確有的普通日常，**R8 影片沒有鋼琴畫面／口播**。

## 本地靜態核對與後續門檻

`node tools/video/cli.mjs script --slug curio-s45` 重新生成 `script.md`；`node tools/video/cli.mjs lint --slug curio-s45` 為 **0 errors、1 warning**：片尾口播未說訂閱，畫面仍保留 21 秒 `v4-endscreen` 的訂閱 CTA 與可點卡位；不為消警告重新加入口播銷售句。99/99 正文場景的 JSON 台詞、腳本及 `claims.md` ID 逐字相同，99/99 來源列有固定 commit 行號，18/18 回收順序合法；99 正文景中 96 張 `shot`，3 張文字卡。按 300 spoken units/minute 保守估計：濃縮開場 **40.40 秒**，其後至片尾前主體 **498.80 秒（8:19）**，純正片口播至片尾前 **539.20 秒（8:59）**；250 速率則開場 46.97 秒、主體 581.67 秒。實際 TTS 時長仍需測量，不能把估值當成完成影片。既有 5 秒片頭安排在第一章後，21 秒片尾安排在正文後；插畫、動畫和可點 YouTube 卡尚未生成／設定。

**下一關**：另一位工作者對上述精確雜湊做獨立來源／書面畫面差分；兩位此前未讀 S45 的隔離讀者對精確 `script.md`／`video.json` 做官方十三題新盲讀。來源和敘事都通過後，才更新站台卡與本地代理選稿註記、對新版本做一次分類正確的 Jev 政策判讀，再考慮 TTS／圖片。R6 兩份政策回覆仍都是 FAIL；R7、R8 沒有新政策 PASS，也沒有任何實際語音、插圖或配樂支出。
