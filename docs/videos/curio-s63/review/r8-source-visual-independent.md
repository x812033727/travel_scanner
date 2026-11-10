# S63 R8｜獨立史料與書面畫面覆核

2026-10-22 UTC。**PASS：R8 固定來源、旁白主張與書面畫面；阻擋 ID：無。**本回條只判讀史料、逐句主張、資訊卡與尚未生成的插圖提示，以及已標示的 loop 回收點；不評正式敘事 13 題、實際生成圖、聲音或成片。我未撰寫本集，也未生成或購買素材。

| 凍結材料 | SHA-256 |
| --- | --- |
| 作者提交 `4df3a297d8f2476c42e661fd5c1f9c16c612f1a4` 的 `video.json` | `c417bc8c6f0df78e9c4d8e910db038b6f4ea07c760cc7f3c2e69e98224f63f08` |
| `script.md` | `63caedb24623bd8339607dd5b11e249ce1a4e6691779279a6d8c64ef5bbd665e` |
| `claims.md` | `68c4139f38976d09b9b1b21bdb239eaa4ecb0ddd2f053b0ef445b971d636fe5e` |
| 固定原文 `/tmp/curio-s63-box-brown-1849.txt` | `6d80216184aaf20433e04aa8d1b6920076211304fcede4a095da3ef5bd62ada2` |

固定原文有 174,750 bytes、2,817 行，對應 `research.md` 釘住的 [GITenberg commit `a92658e80effa4cce03bb19c13e96ffaaae5fa2b`](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt)。[題名頁 L50–56](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L50-L56) 明說這是 Stearns 根據 Brown 本人事實陳述筆寫的出版敘事；不能當獨立人口統計、法律裁判或旅途錄音。

## R7 → R8 範圍

機械比對 R7 父提交 `f22b84e5f` 與 R8：父版三檔 SHA-256 分別為 `video.json` `423f78e9ff18b5b77b14a0ad2fbfe71053cf08aba051a640c53038aa012c2263`、`script.md` `0b5f9bad1330cf0ffbb30998a6e3799b3f88386ffda70867fc047b6a8f4ab408`、`claims.md` `ac6a96737c7e84bff49991801874285de2d2a78b637f4e98899e8b16a37942d7`，與 [R7 獨立覆核](r7-source-visual-independent.md)所列完全相同。JSON 頂層只改 `scenes`、`loops`；127 個同序場景中，只有 `s63053`、`s63125`、`s63126` 三個完整物件改動，**124 個逐欄相同**。`claims.md` 逐句列也只改這三個 ID；`script.md` 只改這三句旁白及重算的結尾雜湊。R7 對另外 124 景的史料與書面畫面判定因此按精確差異沿用；本回條重新核對三個變動 ID、loop 及相關企劃界線。

| ID | 本次獨立判定 |
| --- | --- |
| `s63053` | [B04 L1410–1418](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1410-L1418) 說妻兒被迫分離後，往日令被奴役者不敢逃走的理由對 Brown 已不存在。他的敘事也在 L1414 說決定不再忍受奴役。新句「布朗說……顧慮……已經消失」保留說話人與內心轉變，沒有再敘述路邊告別或假稱已逃走。轉向空門的單人插圖是未具體考證的心境示意，沒有冒充當時攝影。 |
| `s63125` | [B10 L1639–1642](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1639-L1642) 原文為 `I have been told`，接北方選民是南方兩倍；新句用「布朗還聽說」明示轉述，沒有把比例說成獨立人口統計。提示只畫講堂門口和無字長椅，不畫他投票、選票或可讀標語；長椅不是選民數字的視覺證據。 |
| `s63126` | [B10 L1642–1644](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1642-L1644) 的 `If I was one of them, and had any influence` 是假設；Brown 說在此條件下會主張推翻那些法律並建立更好的法律。新句以「若……會主張」維持未實現的假設。無字書與門口只是插圖，不顯示已制訂新法、持有法令或已得到法律保障。 |

`s63009` 未改的問題是貨箱能否把他送到安全的地方。唯一改動的該條 loop 將 payoff 由刪改後的 `s63125` 移到 `s63120`；後一句依 [B10 L1620–1626](https://github.com/GITenberg/Narrative-of-Henry-Box-Brown-Who-Escaped-from-Slavery-Enclosed-in-a-Box-3-Feet-Long-and-2-Wid__64992/blob/a92658e80effa4cce03bb19c13e96ffaaae5fa2b/64992-0.txt#L1620-L1626) 指明他**聽人說**原先奴役者仍可在自由州把他抓回。緊接 `s63121` 保留他不熟悉法律、依聽聞判斷的限定。這回答的是 Brown 當時自述的安全疑慮，不宣稱有確證的追捕或後來的法律結果。`s63125` 的聽聞比例與 `s63126` 的改革主張都沒有被當作安全已獲保障的 payoff。

`brief.md` 最後一段把疑慮與有條件改革主張分開，`research.md` B10 將選民比例標為聽聞而非統計，`visual-plan.md` 明禁投票、新法已通過和歷史照片的誤示；三者與現版稿和提示一致。標題、縮圖和 YouTube 說明仍問「出箱就安全？」並寫明原創插圖是示意；沒有新加不被固定文本支持的結局或日期。

## 對齊與機械檢查

- `video.json`、`script.md`、`claims.md` 各有 127 個同序 ID；127 句旁白、情緒欄逐字對齊，121 個 `shot` 提示與 claims 表逐字對齊，另有 6 張獨立資訊卡。三個新來源連結均指向上述固定 Git commit 及原文中的正確行號。
- `node tools/video/cli.mjs lint --slug curio-s63 --json` 完成：**0 errors／0 warnings**，127 lines。`git diff f22b84e5f 4df3a297d --check` 通過。

**結論：以上精確雜湊的 R8 史料、主張與書面畫面通過獨立覆核。**R7 PASS 僅作 124 個未改物件的對照，正式敘事 13 題須由其獨立盲讀流程另判。尚無實際插圖、旁白或成片可供實物驗收。
