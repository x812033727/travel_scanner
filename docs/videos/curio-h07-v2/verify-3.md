# H07-v2 獨立變更覆核（三）

- 覆核日：2026-10-18。
- 基準：`git show c9241d81a:docs/videos/curio-h07-v2/video.json`，SHA-256 `AFF4E3BF31F4734FA1829A963055A9D0595E9F345CC803D5FE36C9BE5DBC2C82`。
- 本次檔案：`video.json` SHA-256 `622D7EFC7B1EB2586DEEBEA4D999AEFD9C7C29736A9210A1EE7F0938B8C164FC`。
- 結論：**文字及來源卡覆核通過。** 93 景、93 句；65 個插畫鏡頭、27 張來源文字卡（`big` 17、`compare` 9、`steps` 1）及 1 個片尾。相較基準，所有景的順序、句 ID、句文、情緒及作品中繼資料逐項相同；`claims.md`、`research.md` 亦無差異。旁白未改，但整份 `video.json` 雜湊已變。

| 變更 | 覆核結果 |
| --- | --- |
| `h07-43592117`：插畫改為 `Marchioly` 來源卡，新增 C05 對應 | [Funck-Brentano 1899 所刊堂區簿轉錄](https://www.gutenberg.org/cache/epub/43231/pg43231-images.html)確作 `Marchioly`；卡片標明「19 世紀轉錄」與原簿已毀，沒有把拼讀冒充確證本名。 |
| `h07-18bcd1aa`：插畫改為 `Marchialy`／`Marchiel` 對照卡，新增 C05 對應 | [Topin 1870 書前摹本及註 645](https://www.gutenberg.org/cache/epub/70207/pg70207-images.html)作 `Marchialy`；[Funck-Brentano 所錄 Du Junca 邊註](https://www.gutenberg.org/cache/epub/43231/pg43231-images.html)作 `Marchiel`。卡片明說讀法不一、不能當確證本名；只新增既有 C05 的景別對應，未改 C05 內容。 |
| `h07-dfc7a42b`、`h07-4bc41163`、`h07-d9c5bfdb`、`h07-97c8ed9d`、`h07-b8b073e3`：五個插畫提示詞 | 只調整面罩布感、書房與檔案室道具、1693 年命令畫面；無新增可讀文件內容或新史實。`h07-b8b073e3` 移除易使觀眾誤以為布片已在 1693 年命令現場出現的道具。 |

此收據只證明上述檔案與來源文字的比對；插畫實際生成結果仍需逐圖確認沒有虛構可讀字樣。它不代表音訊、成片、時長、後台新版雜湊核准或上架已完成。
