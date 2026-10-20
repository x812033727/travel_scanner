# S46 R8｜R7 獨立來源 HOLD 後的作者窄修

2026-10-20 UTC。R7 的另一位來源／書面畫面覆核者指出兩個 HOLD：標題與說明把「有些學生曾懷疑**入學申請**是敵校騙局」延伸成「那張票被說成玩笑」，但固定原書沒有記個別學生的投票理由；`bkw023` 畫了提問信，但五月二十七日 Blackwell 是親自與 Jackson 談話。其餘變動旁白與主張在該次覆核通過。本檔是 **R8 作者差分自查**，不冒稱新的獨立 PASS。

## 精確 R8 候選

| 對象 | SHA-256 |
| --- | --- |
| Blackwell 1895 固定原書 `/tmp/curio-s48-blackwell-primary/65496-0.txt` | `b52caf559d763349953fe31101016cfb2d68662f152c28a564b6a6b93cac8ec6` |
| [brief.md](brief.md) | `3e2640fb764c5ec58732a91170a7da0fd56fe479530b7219a3b8485b8acf55d0` |
| [research.md](research.md) | `99b8903431cb1e8a317513f260c33a5cd0d141aefec54b4c0a5ba205c126055d` |
| [script.md](script.md) | `53b0a0e601262558f68cdb754b341aaf18d9bfcaefab112ad334bf2691cd73c4` |
| [video.json](video.json) | `1f9e16b7b352f5e3ba5daf0353f8e427838134db04fc9291da6ba32972b7b32e` |
| [claims.md](claims.md) | `670ad3d5fbd611bfd9d6105037ec18bf7ad51ee6f980d2bb7930006f2aaf7fb0` |

## 差分與原書界線

| R8 修改 | 原書對照與限制 |
| --- | --- |
| `brief.md`、生成的 `script.md` 和 `video.json.youtube.title` 以「一八四七年那張學生歡迎票，能帶她走到醫學文憑嗎？」為主問；說明欄只寫「有些學生曾懷疑**她的入學申請**是敵校捉弄，沒有記下個別投票理由」。縮圖標題改「歡迎票？」；聲音提示也精確稱晚年所說「騙局」。 | [P07 L2181–2207](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2181-L2207) 書中轉錄學生一致歡迎的正式決議；[P11 L2436–2442](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L2436-L2442) 1895 回憶說有些學生疑她的**申請**是敵校騙局。兩段均不記投票者個別動機。「常被讀成全班惡作劇投票」沒有固定來源，已從說明欄刪去。 |
| `bkw023.data.prompt` 改為一人在 1840 年代辦公室桌旁**說話**，無信件或可讀文字。 | [P02 L1984–1995](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt#L1984-L1995) 是五月二十七日親訪 Jackson、當面說想學醫；沒有「提問信」。畫面只作卡通示意，不假冒原始現場或物件。 |

除此以外 121 句旁白文字、19 組 loop、全部主張對照、章節順序和時長設計都未修改；`claims.md`、`research.md` 雜湊與 R7 相同。`script --slug curio-s46` 已按 R8 JSON 重產 `script.md`，變動是標題；其餘旁白未變。

## 靜態檢查與停手點

`lint --slug curio-s46 --json` 為 **0 errors／0 warnings**。119 景、113 張 `shot`、121/121 句與 `claims.md` 按 ID／順序／字面吻合，19 組 loop；工具估全旁白 11:51、開場約 0:49，正文仍為 2,221 漢字，按每秒 4.5 字約 **8:14**。這些不是 TTS 或成片實測。`git diff --check` 無格式錯誤。

R8 須**另一位**按上述精確版重新確認兩個來源／書面畫面 HOLD，再讓兩名未讀過 S46 的讀者對同一版做完整盲讀；不可沿用 R7 其他項的結果推稱全片通過。原創 5 秒片頭、21 秒動畫片尾與末約 16 秒推薦／訂閱框仍是規格，未組片或啟用可點連結。沒有網站大綱／劇本核准，未製作付費 TTS、插圖、配樂或成片；媒體支出 US$0。
