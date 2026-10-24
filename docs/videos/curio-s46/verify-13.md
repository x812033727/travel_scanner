# S46 R6｜共同盲讀失敗後的定點修稿（作者自查）

2026-10-20 UTC。[R5 兩名全新盲讀](verify-12.md)共同把 `no_recap`、`no_detour` 判 No，R5 敘事正式 FAIL。本稿是作者 R6 改稿及機械自查，**不是**獨立史料、書面畫面、雙盲敘事、網站或付費媒體通關。

## 精確 R6 候選

| 對象 | SHA-256 |
| --- | --- |
| Blackwell 1895 固定原書 `/tmp/curio-s48-blackwell-primary/65496-0.txt` | `b52caf559d763349953fe31101016cfb2d68662f152c28a564b6a6b93cac8ec6` |
| [brief.md](brief.md) | `937b11b91096e733e656465c75842fe7284bdb7ea07b64f994ebdf51d7b41d0e` |
| [research.md](research.md) | `99b8903431cb1e8a317513f260c33a5cd0d141aefec54b4c0a5ba205c126055d` |
| [script.md](script.md) | `12877154c9cc34c62385f31248e5c19db703e2655597761f39b445978af4bf4d` |
| [video.json](video.json) | `19eba5b4c06fc98520a5aa05fecdedf68c44871408a54fddc971932fae472f73` |
| [claims.md](claims.md) | `57a6488933197126309a13a7bcfbe5c9fb81814f914abb3004dfef7538061fb4` |

## 窄修及來源自查

| R5 盲讀意見 | R6 作者修訂和可重開來源 |
| --- | --- |
| 開場倒敘接不上、回到院長信時重講同一日期與程序 | `bkw009→010` 把學生表決前的醫師求教改成下一章第一個行動；`bkw042` 明說「回到開場那封信」，並給教師在本學期前晚才首次開會的新資訊。`bkw043` 加次日學生自行開會及兩條決議，`bkw044` 只說十月三日申請送達，不再重念十月二十日。原書 [L2153–2207](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2153-L2207)。 |
| 決議歡迎連三句、片尾未回題 | `bkw047–049` 分開原則、全班一致邀請、同學行為承諾；`bkw050` 改為她後來珍藏並抄到羊皮紙的具體新行動，來源同上。`bkw069` 僅指出晚年所稱「騙局」的受詞是**申請**，片尾 `bkw999a` 才從缺少逐人投票理由得出有界結論：「玩笑表決無從證實」，不臆測任何學生內心；原書 [L2436–2442](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2436-L2442)。 |
| 演示課與論文相鄰重述 | 合併 `bkw074/075`，刪 `bkw075`；`bkw078` 改為教授會否把要求告訴全班的具體鉤子，`bkw079` 直接回答，刪重複教授答應的 `bkw080` 與緊鄰解決後的 `bkw085`。`bkw109` 只說斑疹傷寒論文**題目**，`bkw110` 問誰先看完成稿，`bkw111` 回答 Dr Elder；loop 改 `bkw110→111`。原書 [L2361–2411](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2361-L2411)、[L2657–2674](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2657-L2674)。 |
| 住院董事七句支線與開場床頭卡承諾不符 | `bkw087` 明標 1848 年與另一個病房許可關卡；`bkw090–096` 縮至新許可、吉爾平提醒、分訪領頭人及獲准住院四句，刪 `bkw092/093/095`，未把「一致准許」說成正式逐人投票。`bkw007` 現明說卡片停寫、懸在**她如何繼續學**，loop 指向 `bkw103` 自行整理所見，不再預告一張卡讓她停步的未發生場面。原書 [L2517–2553](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2517-L2553)、[L2657–2674](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2657-L2674)。 |

改動畫面仍是**書面提示詞**，非實際生成圖：`bkw050` 一位成年女子抄寫無字決議與素色羊皮紙，對應原書「afterwards copied on parchment」；`bkw091` 一位成年董事閱空白申請，`bkw096` 室內柔和光線。其餘僅刪重述景、改口播，提示詞未宣稱原始信件、真實病歷、會議照片或手術畫面。需由另一人獨立核對。

## 形式與停手點

`script --slug curio-s46` 由精確 `video.json` 重產；`lint --slug curio-s46 --json` 為 **0 errors、0 warnings**。122 景、116 張 `shot`，卡片以外插圖比率 95.1%，124/124 句與 `claims.md` 的 ID、次序及逐字口播相同；18 組 `loops` 先設後收且 ID 仍存在。工具靜態估時全口播 12:00，首章約 0:47；正文 2,247 個漢字，以每秒 4.5 字、不計停頓估 **8:19.3**。這不是合成語音或影片時長；原創五秒品牌片頭、21 秒動畫片尾和最後約 16 秒 Studio 推薦／訂閱框仍只在製作規格中。`git diff --check` 無格式問題。

R6 下一關是**新的**獨立原書／逐句主張與書面畫面差分，及兩位未讀本稿的全新盲讀者各答官方 13 題；R5 PASS 不能轉移。尚未推站台大綱／劇本卡、TTS、買插圖或配樂，沒有成片、上傳或可點連結。媒體支出 US$0。
