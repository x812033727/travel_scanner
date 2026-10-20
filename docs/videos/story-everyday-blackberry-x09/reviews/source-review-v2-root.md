# X09 BlackBerry｜獨立來源審查（鎖版）

結果：**PASS（文字與來源）**。此審查只核對下列精確版本的主片文字、原生卡所需數字與來源邊界；不代表敘事盲讀、語音、插畫或成片已通過。

- `video.json` SHA-256：`9ff07b5087b202c1fa1b03ca636658bfa70dbf09661f1d4d2214c925fd7a7d7f`
- `shorts.json` SHA-256：`5f47562a9a8d804cb34456aaf2594c1e393f4566e5adf5b92430f69dde7be2c6`；兩支短片的文字、標題與來源亦於下段審查。
- 審查日：2026-10-20。審查者：Codex root，與 X09 撰稿代理不同。

我獨立由 SEC 重新下載並讀取五份原始 HTML；收到的檔案 SHA-256 與 `source-notes.md` 一致：FY2015 AIF `bd0e27d1d570459c64956cc0372e8ff5719f2b47bbbc6c45b4d6ac18ed4d75da`、FY2017 AIF `faae7366f1d2e1197ed599b513930ba078cc953732cc2f2c806692d581bfc55d`、FY2017 MD&A `8cf6de67e2accbfc508a79ffe4bafd85a74221a9c4905ec00a3902c39ffbf94b`、FY2020 10-K `54367d158e51eadd8cd8c17616f5ab363ecef92c9334c3d7244f5b2e4eee1230`、FY2025 10-K `d539463c905411aca1069a0e0f1e940970f5d75c4ca8fe4e419abcce3b8a6fca`。直接來源網址及定位在 `source-notes.md`。

| 稿中重點 | 原件核對與界線 | 判定 |
| --- | --- | --- |
| `x090201`–`x090218`：Classic、Passport、Foxconn 共同開發、BES12 跨系統、QNX 早已存在 | FY2015 AIF 的產品與 Enterprise Services 記述支持；沒有把當時合作開發說成全部硬體已外包。 | PASS |
| `x090301`–`x090321`：硬體及其他 US$884m→374m、舊服務費 US$779m→313m、軟服 US$497m→622m，總收入約 US$2.2b→1.3b | FY2017 MD&A「Consolidated Revenue」逐字列出數字及 US$510m／466m／125m 變動；軟服增額主要關乎 Good Technology、AtHoc 併購。稿未將收入誤作手機銷量或利潤。 | PASS |
| `x090401`–`x090429`：TCL、Optiemus、PT BB Merah Putih 分工，KEYone 於 FY2018 Q1 開始供貨，品質／安全／品牌準則與風險 | FY2017 AIF 的協議、Mobility Solutions、Production 與風險文字支持。稿用「可能受損」而未虛構已發生事故；`x090419`–`x090422` 亦保留舊機仍賣及一款公司設計、第三方製造新機的當時計畫，避免「從此絕不自行設計」的過度概括。 | PASS |
| `x090506`–`x090516`：手機授權依夥伴銷售是否超過最低量採不同收入認列，QNX 常按出貨單位收權利金 | FY2020 10-K 的 Mobility revenue-recognition 段明列 licensed products sales reported by licensees／低於門檻時依最低合約額與工程服務承諾在授權期間平均認列；QNX 章明列 units-shipped royalties、工具及維護。稿將兩者分開，沒有說成收現、淨利或 BlackBerry 親製手機。 | PASS |
| `x090601`–`x090610`：逾 2.55 億輛部署、QNX 部門 US$236.0m、較前財年 +US$20.6m 及權利金/Radar/開發席位/專業服務方向 | FY2025 10-K 原文支持；QNX 部門還含 Radar、Certicom、IVY。稿明說部署不是當年新車銷量，部門收入不是單一車用系統權利金；沒有硬把分項湊成總變化。 | PASS |

## 兩支 from-episode Shorts

Short 1（`story-everyday-blackberry-x09-short-1`）七個 shot ID 均存在；七句旁白與主片相應 scene 的 `lines.text` **逐字相同**。標題、headline 與說明的 KEYone／實體鍵盤／TCL 宣布、公司授權安全軟體與品牌、夥伴承擔硬體及各地客服、舊機當時仍賣，均由 FY2017 AIF 的 General Development、Mobility Solutions 與授權合約段支持；SEC 原文有 `handsets featuring the Company’s secure Android software`，亦支持其 Android 句。Short 2（`story-everyday-blackberry-x09-short-2`）七個 shot ID 及七句逐字引用也與主片相符；FY2017 MD&A「Consolidated Revenue」直接列出說明及卡面三組收入數字和 US$2.2b→1.3b，並將 US$125m 軟體服務增額主要歸因 Good Technology、AtHoc 併購。Short 2 的「軟體還沒補上」只對這兩個財年的已列收入差額，未稱長期失敗、手機授權因果或利潤。

兩支說明所列 SEC 連結各指向實際支撐原件，沒有填虛構長片網址；「完整事件請看本集長片」是待正式長片存在後才可上架的交叉導流文案。兩支文字／來源審查 **PASS**，但 25–55 秒實際配音長度、9:16 裁切、聲畫／CC 及可點連結仍未製作或驗收，不得把腳本當成已完成 Short。

`line-source-matrix.md` 對五份原件的主張指派與鎖版旁白相符。這些皆為公司申報，車輛部署量已以「公司稱」標示。FY2020 與 FY2025 HTML 原件超過部分正式工人單頁 3 MB 讀取上限；若日後轉正式自動工人，須提供可讀的原發行者摘錄或將對應主張標為 `reviewer_only`。下一關是兩位互不看彼此意見的敘事盲讀；任何主片或 Shorts 文字、卡片數字改動須重綁 SHA 後重審。
