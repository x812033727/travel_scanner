# S46 R3｜獨立原文與書面畫面差分覆核

2026-10-20 UTC。以 [R2 獨立 HOLD](verify-4.md) 為逐項核對清單，重開同一份 1895 年 Blackwell 自傳，核對 R3 的修正文句、證據範圍和書面提示；並通查 131 句逐景主張、123 個 `shot` 提示的時序與角色身分。**史料旁白 PASS；書面畫面 HOLD**，因開場倒敘 `bkw008` 新換的角色稱呼與 1849 年場景矛盾。這是對以下精確版本的文字判定，尚無圖片或語音可驗。

## 固定版本與形式檢查

| 對象 | 本次重算 SHA-256 |
| --- | --- |
| 1895 年原書，GITenberg commit `16787df4911754c8e0401d12c896b943768f5d8d`，本地 `/tmp/curio-s48-blackwell-primary/65496-0.txt` | `b52caf559d763349953fe31101016cfb2d68662f152c28a564b6a6b93cac8ec6` |
| `research.md` | `99b8903431cb1e8a317513f260c33a5cd0d141aefec54b4c0a5ba205c126055d` |
| `brief.md` | `8012cab4d8c574a7b4f90f6e02d0ea1d2a96f63919c2377ac5c35de90bec9262` |
| `claims.md` | `b4819dd7fcec82efa2df0946be167abea7b21bfd0f231711923f5e09c2c657a9` |
| `video.json` | `69d738e99fefc84840858d02e3a5b1aaccd4c77f5826f56d06ebd9d3bd0aa663` |
| `script.md` | `6db66fc2bc2f671c76d28982162d6c7c304c9722bbde41aed8a67e58c607c918` |

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s46 --json`：0 errors、0 warnings。逐行比對 `video.json` 與 `claims.md`：129 景（123 `shot`、5 資料卡、1 outro）、131/131 句一致，131 個主張 ID 無重複；歷史主張連結均指向上述固定 commit。這些形式檢查本身不構成史料通過。

## R2 史料 HOLD 的 R3 結果：PASS

| R2 問題 | R3 核對結果 |
| --- | --- |
| `bkw019` 把 Dr. Horner 的提議接成 Dr. Jackson 的話 | 現明寫「**霍納教授另建議**她試費城兩所學校」；`research.md` P02 亦分清 Jackson 回報同事反對和 Horner 提議。固定原書 [L1984–1998](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L1984-L1998)吻合。 |
| `bkw090–096` 把 Blockley 派系協商寫成正式表決，過度推斷 Gilpin 已表態支持 | `bkw090–093` 現說董事分屬黨派、Gilpin 友善接待、若由他這名 Whig 提案恐遭另兩派反對；`bkw094–096` 說她分訪領頭人，請願交董事會後獲一致准許。`research.md` P12 和 `claims.md` 明列「未記正式投票」界線。這對應原書 [L2524–2542](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2524-L2542) 的 *unanimously admitted*，沒有把它混作 1847 年學生決議 [L2185–2204](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2185-L2204)。 |
| `bkw067–068`、`bkw113`、`bkw127–128` 引文缺口 | P09 及對應逐景連結已涵蓋鎮上凝視、校門避開批評 [L2326–2338](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2326-L2338)；`bkw113` 精確連 [L2692–2695](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2692-L2695)；`bkw127–128` 連訪客與離城 [L2890–2894](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2890-L2894)。 |

其餘未改的 R2 旁白仍在前次逐景核對的來源邊界內：十二所是申請數 [L2141–2151](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2141-L2151)；可能被拒用的公立資源與可用的私人藏書 [L2072–2089](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2072-L2089)；醫院床頭卡、熱病患者和地板床位 [L2657–2674](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2657-L2674)；考試與領文憑 [L2791–2805](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2791-L2805)、[L2840–2888](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2840-L2888)。核心句 `bkw083–085` 仍把部分學生懷疑**申請**是敵校騙局 [L2436–2442](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2436-L2442)，與書中轉錄的歡迎決議分開；沒有宣稱查過獨立校方原件。

## R3 書面畫面：HOLD

- **新問題 `bkw008`：開場倒敘的身分錯置。** 旁白是「一年多後，教堂裡還有一場文憑典禮」，提示也把人物放在 1840 年代教堂、文憑盒旁，卻新改稱 `one medical applicant in plain 1840s clothing`。Blackwell 1847 年到校登記成第 130 號學生 [L2214–2219](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2214-L2219)，1849 年 1 月 23 日在教堂領文憑 [L2845–2868](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2845-L2868)。這一幕應稱 `female medical student` 或 `adult woman in 1840s clothing`；`medical applicant` 適用的是較早寄申請階段。只需修提示，不必改此句旁白或其來源連結。

R2 其餘畫面 HOLD 已修：`bkw102` 現是她**入院前**的一名男性住院醫師寫無可讀文字的床頭卡；`bkw127` 在授文憑後改稱 `newly graduated woman physician`。申請期 `bkw015, bkw029, bkw036, bkw050` 改稱 applicant，領文憑前原先誤叫 physician 的 `bkw010, bkw024, bkw031, bkw045, bkw052, bkw059, bkw066, bkw073, bkw080, bkw087, bkw094, bkw101, bkw108, bkw115, bkw122` 已改為申請者或學醫女子；`bkw093–096` 的醫院辦公場景沒有票箱或投票動作。R1 修過的 `bkw030, bkw047–048, bkw054–055, bkw058, bkw107, bkw109` 仍維持其關門、男性學生、夜間、冷雨、紀念物、單人及地板床位界線。此處判的是**文字提示**；生成圖片仍須單獨檢查成年性別、年代、道具和假文字。

修正 `bkw008` 後，重算 `video.json` 和由它再生的 `script.md`、受影響文字檔雜湊，重跑 lint，請未參與修稿者只覆核新畫面版；R3 的史料 PASS 適用於此精確旁白，若改旁白則須重審。兩名**全新**敘事盲讀者及網站關卡尚未完成；本報告不核准媒體生成或上架。
