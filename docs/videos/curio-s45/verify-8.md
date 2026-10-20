# S45｜R6 時序與來源修訂自查：凍結送獨立覆核

2026-10-20 UTC。這是撰稿者的**本地自查與精確凍結候選**，不是獨立來源／畫面 PASS、兩位 R6 新讀者 PASS，亦不是站台 `hand_pushed` 大綱或劇本核准。R5 的兩位全新盲讀者分別評為 [13/13](/tmp/s45-r5-blind-a.md)、[12/13](/tmp/s45-r5-blind-b.md)；B 單獨判 `bly030` 的 `payoffs` 不夠明白。依雙讀者敘事規則，R5 敘事 PASS，異議保留。然而 [R5 獨立來源與書面畫面審查](verify-7.md) 判 **HOLD**；R6 按其逐項修復並處理該讀者異議。兩份 R5 盲讀不可移作 R6 簽核。

| R6 同組凍結輸入 | SHA-256 |
| --- | --- |
| `research.md` | `97b91f2344190fbc424fd29eca17da2bee372673bdc7fd36e7161e13ef31ab65` |
| `brief.md` | `e4a75c2afb0ad4a5070fb3d49fec186b95946fc31e9d3ed2a2bf72fe916c6437` |
| `video.json` | `bc79155385a70b0330e0efdce8ef49ad14af977c399095bc87cb7c43c639cd0f` |
| `script.md` | `a30602d0c05a2586407ced2d5203ba6c9b83104ed8dc0865a12688d1b0685951` |
| `claims.md` | `6723b91469253a7da203700315bdc555340965120c882f8532f9f43a2afe0511` |

唯一敘事一手文本仍是 Nellie Bly, *Ten Days in a Mad-House*（1887）[固定 GITenberg commit `c3904b5064d2bafb7e13486489dfe98b560611b5`](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt)；本地 `/tmp/s45-bly-59899.txt` SHA-256 `bc03f9cdb9a845bd4d9babaa8652c4c93e415dd09c7b54ca20c07143e5e2d5b3`。以下行號皆對此版本。

## R5 HOLD → R6 來源、敘事與畫面差異

| 場景 | R6 修訂與原文界線 |
| --- | --- |
| `bly011–014` | 改為選址按鈴 [L285–310](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L285-L310) → 暗後客廳等至少二十分鐘、助理才到 [L314–323](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L314-L323) → 單人房已滿、同意共住 → 她以出門時約七十美分中先付一晚三十美分，盤算錢用完可能被請走 [L325–337](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L325-L337)。`bly013→014` 直接答費用；取消 R5 將房費放在等候前、把暗處叫成後來房間的敘述。畫面由虛構櫃檯／登記簿改為後客廳等待、聽接待、持普通硬幣。 |
| `bly017–020` | 改為原定同房女性拒留、**另一位** Caine 太太陪 Bly 過夜 [L503–525](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L503-L525) → 近清晨裹毯 [L617–625](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L617-L625) → 醒後咖啡與一個 bun、回房再提行李 [L598–609](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L598-L609) → 助理 Mrs. Stanard 出門帶回兩警員、Bly 經警局到法院 [L643–690](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L643-L690)、[L718–738](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L718-L738)。原書把裹毯置於早餐段後**回述**；影片按事件時序。`bly017→018` 直接揭示陪伴者，`bly015→020` 回收找警員。畫面改夜間離房、毯子、早晨餐處，均一名成人一個普通動作。 |
| `bly030–031` | B 讀者在 R5 指出 Bellevue 是否仍假扮未明說。`bly031` 現直接答「繼續假扮」，再交代櫃檯拒答、隨車醫師說文件已備。原文她一度忘了**角色** [L1044–1058](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L1044-L1058)，其後又說在年輕醫師面前扮演很難 [L1321–1325](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L1321-L1325)；不說她未受檢查。新增 `bly030→031` 回收 metadata。 |
| `bly035` | 改「有些訪客**似乎**在找失蹤女孩」並用「她**被要求**露臉」，不替未指名者指派行為。[L1431–1438](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L1431-L1438)。 |
| `bly080` | 旁白未改；依她原文出外隨隊散步 [L3016–3023](https://github.com/GITenberg/Ten-Days-in-a-Mad-House-or-Nellie-Bly-s-Experience-on-Blackwell-s-Island-Feigning-Insanity-in__59899/blob/c3904b5064d2bafb7e13486489dfe98b560611b5/59899-0.txt#L3016-L3023)，提示詞把室內走廊改為普通室外步道，一人揮手，不重演來源中另位病人的倒地或強制。 |

`research.md` P03–P05 已改按事件時序並補 Bellevue 角色錨點；`brief.md` A 案與估時計數跟 R6 候選一致。除此之外沒有改其他旁白、歷史題名、書中星期日 9/25／星期一 9/26 的進島日期、返訪船與未宣誓陳述的來源界線。律師來源仍不與編輯作無憑連結；陪審團原始報告、診斷、預算一百萬美元及永久改革都未當已證事實。

## 本地驗證及下一關

- `node tools/video/cli.mjs script --slug curio-s45` 重生 `script.md`；`node tools/video/cli.mjs lint --slug curio-s45` 回報 **0 errors、0 warnings**。99/99 正文場景旁白逐字見於 `script.md` 與 `claims.md` 相同 ID 列；99/99 引文列都連到固定 commit 行號。正文 96 插圖景、3 來源卡，另有片尾；17 條先設伏後回收 `loops`。
- `estimateTimeline`：250 spoken units/minute 的濃縮開場 **46.97 秒**、正文 **573.47 秒（9:33）**、純劇本 **638.93 秒（10:39）**；300 的濃縮開場 **40.40 秒**、正文 **492.00 秒（8:12）**、純劇本 **548.20 秒（9:08）**。這些是文字估算，實際 TTS 尚未做，須以 `check-audio` 驗證正文至少八分鐘及成片時長。
- R6 現須由**另一位工作者**對上述精確雜湊做獨立來源／書面畫面差異覆核，並由**兩位真正全新、隔離研究與舊報告**的讀者對同版 `script.md`／`video.json` 做十三題盲讀。任何修改都要重凍結並重讀。站台 `hand_pushed` 大綱與劇本關卡、付費語音／插圖／音樂、原生圖片驗收、組片、上架和 Git 提交／推送均未在此階段執行。
