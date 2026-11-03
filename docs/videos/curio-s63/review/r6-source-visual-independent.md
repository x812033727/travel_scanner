# S63 R6｜獨立史料與書面畫面覆核

2026-10-22 UTC。**PASS：R6 凍結候選的前製史料與書面畫面關卡；無阻擋句 ID。**本回條只審旁白、固定來源錨點及尚未生成的插圖提示，不是正式敘事盲讀、實際圖片或聲音驗收，也不是付費媒體及上架准入。

| 凍結材料 | SHA-256 |
| --- | --- |
| 作者提交 `51b08ae3dc07cb4b8499f3c1e95aff2797305b49` 的 `video.json` | `8f8903a7ec270c61636953a7d675840a838604c268132722658c05b26f2dbf68` |
| `script.md` | `dfafdb178646575cc4cefab9c14621284835299caf1c75f3eea86e7835d82bd9` |
| `claims.md` | `10a28deb76976f1b7c32eb4ab0188c6fda33e93d1914d2d1536c1ecd7eb9c18e` |
| 固定 Brown／Stearns 原文 `/tmp/curio-s63-box-brown-1849.txt` | `6d80216184aaf20433e04aa8d1b6920076211304fcede4a095da3ef5bd62ada2` |

## 獨立比較範圍

固定原文為 174,750 bytes、2,817 行，與 `research.md` 所釘 [GITenberg commit `a92658e80effa4cce03bb19c13e96ffaaae5fa2b`](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt) 的原文雜湊一致。題名頁 L50–56 說明正文是 **Brown 自述事實、Charles Stearns 筆寫**；以下的「布朗說」指這份經筆寫的出版敘事，不代表獨立貨運、社會統計或法律紀錄。

直接比對 R5 父版與 R6：R5 三檔的 SHA 分別為 `video.json` `118430ef07ca7ac2e6d7c198088bdd1ef312755e126fef15ea2b310475a39adf`、`script.md` `dee3cb408979b3ca7dff85fb00e63915c2e54e555a0ee22e776e28fc97556c0f`、`claims.md` `5b616ce92afd61feed9264e57da240388619588e636550a91e93a315e2d6a9fc`，均與已存檔的 [R5 獨立覆核](r5-source-visual-independent.md)吻合。JSON 結構比較顯示頂層僅 `scenes` 改動；只有 `s63002`、`s63004`、`s63052`、`s63106`、`s63126` 五個完整場景物件改動，其餘 **122/127 場景物件逐欄相同**。`claims.md` 與 `script.md` 也各只有這五個 ID 的逐句列改動，另各有非逐句狀態文字或產生雜湊更新。因此 R5 對其餘 122 句的來源及畫面覆核仍按精確差異適用；以下五句另核對原文。

## 五個變動 ID

| ID | 原文、旁白與畫面判定 |
| --- | --- |
| `s63002` | [B09 L1569–1572](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1569-L1572) 先寫接收者害怕開箱，稍後才有人敲問。開場改成門邊一人猶豫，畫面雙手收回、箱子仍關著；一人代表當時在場者，不捏造敲箱或開箱先後。 |
| `s63004` | 同段原文在敲箱後才有 `Is all right within?` 和 Brown 的 `All right`。開場「裡頭還能發出人的聲音嗎」是停在結果前的疑問；沿用的手懸於封箱蓋上方畫面未提前回答或打開箱子。 |
| `s63052` | [B03 L1388–1394](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1388-L1394) 緊接道別寫 `not an imaginary scene`、`not a fiction`、`an every-day reality at the South`。旁白明說「布朗提醒讀者」，保留它是經 Stearns 筆寫的倡議性陳述，不把「每天」當獨立統計。路邊只留一名成年人，隊伍已出畫；不重畫三個孩子或編造他們去向。 |
| `s63106` | [B09 L1569–1572](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1569-L1572) 的 `at length one of them rapped upon it` 支持一人此時終於敲箱。封箱上單人指節輕敲的示意不讓箱提前打開；`s63107` 問、`s63108` 回、`s63109` 開蓋的順序仍與原文一致。敲箱在正文此處首次實際發生。 |
| `s63126` | [B10 L1622–1638](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1622-L1638) 說 Brown **聽別人說**當地人不讓他被帶回，或會為他違法；同段仍說若聽來的法律屬實，他並不安全。旁白保留轉述層次與法律疑慮，沒有寫成真有群眾違法相救、法律已改或他取得法律自由。單人停在麻薩諸塞講堂門檻光影間的畫面只呈現未定的安全感，沒有演出相救或追捕。 |

這五句與 `visual-plan.md` 新增的開場、路邊及講堂界線一致。開場不再演出敲箱；家人告別後不重說孩子數；片尾以 Brown 聽到的保護說法及仍在的疑慮收束。這是對來源與書面畫面的一致性觀察，**不是**對 R5 `no_recap`、`payoffs` 題目投出 R6 正式盲讀票。

## 對齊及機械檢查

- `video.json`、`script.md`、`claims.md` 各有 127 個同序 ID，127 句旁白逐字一致；121 個 `shot` 提示與 claims 表逐字一致，另有 6 張分開的資訊卡。claims 表的 144 個逐句來源連結均指向固定 Git commit，行號範圍均落於原文 2,817 行之內。
- 開場 `s63001`–`s63009` 為 **175 漢字／約 32.3 秒**；正文 `s63010`–`s63126` 排除開場及 CTA 為 **2,682 漢字／約 8.25 分鐘**，均按每分鐘 325 漢字估算；實際配音尚未量測。
- `node tools/video/cli.mjs lint --slug curio-s63 --json` 完成，**0 errors／0 warnings**、127 lines；`git diff HEAD^ HEAD --check` 通過。

**結論：上述凍結 R6 旁白、固定來源與書面畫面沒有剩餘阻擋項，可交由兩位全新正式敘事盲讀者評估。**R5 盲讀 HOLD 與本次來源 PASS 不互相取代；若再改旁白、來源錨點或插圖提示，須以新雜湊重查。尚無生成圖片、配音、成片、Short 或上架收據。
