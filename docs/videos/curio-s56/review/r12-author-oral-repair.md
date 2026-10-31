# S56 R12｜兩句口播窄幅修訂（作者交接，未獨立核准）

2026-10-20 UTC。R11 [音檢](r11-audio-gate/summary.md)在 154 句全檢與兩輪只重錄旗標句後仍有 `s56096`、`s56174` 兩旗標（9 → 2 → 2）；[原樣回條](r11-audio-gate/run-receipt.json)和 [口語交接](r11-audio-gate/oral-wording-handoff.md)保留。R12 **只改這兩句的旁白**，同步 `video.json`、`claims.md` 並從 `video.json` 重產 `script.md`。未修改畫面提示詞、章節、伏筆 ID、旁白之外的場景、`brief.md` 或 `research.md`；121 景、154 句、18 個 loops 未變。R11 的已合成音檔、史料／書面畫面、雙盲敘事與政策 PASS **均不能直接轉作 R12 PASS**。

| ID | R11 口播／最終轉寫問題 | R12 口播 | 原文與修詞理由 |
| --- | --- | --- | --- |
| `s56096` | 「可為了安心，他還是回旅館開始收行李。」→ ASR「她…收拾行李」 | **福斯特仍不放心，回旅館打包行李。** | F 的固定版 [L376–414](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L376-L414)寫「still to make my mind easy, I went to the Brigg’s House, and commenced packing」。明說姓名與「打包」保留動作和心理，也避開代詞同音字及「收／收拾」口語差。 |
| `s56174` | 「西岸大火隨後越河，與東岸新火連成一片。」→ ASR「東岸星火」 | **西岸大火隨後越河，跟東岸那片火勢連在一起。** | F 的固定版 [L349–383](https://github.com/GITenberg/A-Letter-from-the-Fire-Being-an-account-of-the-Great-Chicago-Fire_66472/blob/60c777551301c30942acf749d4bb37ca32752353/66472-0.txt#L349-L383)寫「it soon jumped the river too, and joined the new one」。緊前一句 `s56173` 已明說東岸另起之火；「那片火勢」回指它，不再讓「新火／星火」誤作一點小火花。沒有把飛火越河路徑說成親見。 |

上述原文仍是 Gutenberg 轉錄的 1923 年 Foster 家書抄本出版物，原信不存；兩個本機暫存全文 SHA-256 與 [research.md](../research.md) 相同：F `59d5d0740ecf20583374d499ab3aff481c000d45d20685b548490b90fc3062ee`、L `d1e6575eb2af0a36a99aacfc9c94817f38e460db81746cd4cc95199e18d1f011`。**此處是作者比對，不是獨立審查。**兩句對應的插圖提示詞仍只示意旅館外觀與兩岸火勢，沒有新增可讀原信、照片、精確火屑軌跡或現代消防設備。

## 精確凍結

| 檔案 | R11 SHA-256 | R12 SHA-256 |
| --- | --- | --- |
| `brief.md` | `09f731c13f1037c963aa5774b936a43e1a187b5c4ae8d09ba158581a705f1a52` | `09f731c13f1037c963aa5774b936a43e1a187b5c4ae8d09ba158581a705f1a52` |
| `research.md` | `59549e98e6ae258cedfc5b43e6684ecaa1102284d0dee13b0beef6443e4a6fb7` | `59549e98e6ae258cedfc5b43e6684ecaa1102284d0dee13b0beef6443e4a6fb7` |
| `claims.md` | `8edaf18bee138c3dc88dd2e38e7eebd2c27a9e24158dc0bed696fb4e53904a80` | `ca09512c0398c94578f2acaa748cdc13c4b5ebff79ac80b6107ca600d65f6b11` |
| `video.json` | `297b576499068e12fb937bc6032394cf9408f8543065b762a95c6b26ef89cd72` | `f54a4c830fb876e949f4f4910d025cb8f68331e40d27dc87ab9edf26f05bd479` |
| `script.md` | `38ef6dfdbb71bd0b59a441a4d41fc4a89b2b3aed288899a28ec902193b792d2c` | `65ae866c1761da1c83d0941a92569c7b85ec0fddda0de17adc157bbc8d046f4f` |

`script --slug curio-s56` 已重產，`lint --slug curio-s56` 是 **0 errors、0 warnings**，154 句、2,604 估算口播字元、約 12.6 分鐘。這是文字估計；R11 實測 12:11.10（開場 54.53 秒、正文 11:16.57）只供長度參考，**R12 仍未重新合成或實測**。

## 後續關卡

1. 另一位工作者按以上 **R12 五個 SHA** 重開來源，獨立核對兩句和書面畫面，並確認其餘主張、場景與來源邊界未被改壞。
2. 兩位未讀本交接及舊評票的讀者僅讀 **R12 `script.md`**，各自按正式 13 題盲評；用工具規定的 OR 規則正式合併，再對同版跑 Jev 政策。任何 HOLD 先修稿，不開付費語音。
3. 全部通過後才對 R12 做 `tts --dry-run`、新稿合成與 **154／154** 全句音檢；R11 兩旗標不得清空或偽作新版 PASS。`/workspace/.video-work/curio-s56/STOP` 留著，直到 R12 真正通過音檢與後續關卡。

沒有產生新圖片、配樂、字幕、Shorts、成片或 YouTube 連結，亦未聲稱站主核准。
