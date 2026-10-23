# C14 CamelBak｜v3 I01 字卡獨立覆核

- 審查者：`codex-c14-v3-visual-recheck`；2026-10-23（Asia/Taipei）。未撰寫本次作者微修，未讀或簽署純旁白盲評。
- 對象：draft [PR #1695](https://github.com/x812033727/travel_scanner/pull/1695) 的作者微修 commit `7caee78c81d62142e90450a766f1c858fdd512a9`；檢查時 PR HEAD `8015896ff94b5f531f2d53d55df384e1b22f93c1`。後一 commit 沒改受審 script／notes／visual MD／JSON；不審其盲評內容。
- 結論：**v3 視覺文字 PASS**，限 I01 修復、O10 搭配、`visual-plan.md` 同步說明和未變的其餘鏡頭。這解除 [v2 獨立來源／視覺收據](independent-v2-source-visual-delta-review.md)所記的 **I01 畫面 HOLD**；不改寫該輪的 61 句來源 PASS，也不判純旁白、TTS、圖像或成片通過。後續再動受審檔案須按新 SHA 另審。

## 版本綁定

| 檔案 | 本輪直接計算的 SHA-256 |
| --- | --- |
| `treatment.md` | `078DC1D77C46EB49BB6F27F60535F22775781E5963783BDA7C1F7625B1A8700E` |
| `source-matrix.md` | `F8CF68AA36264DF18CDBE6ECD698D4AF1F22E405DEAADA8ED275B7685050587E` |
| `script.md`（未改） | `6F52F13283B8B14941D40A0DBE19D299B8266824A33E22201EEB99C700B25119` |
| `script-source-notes.md`（未改） | `6627DC1CDAA301B80B30C087BF3DC746DA1F60032BB29C05EA2047C95F0C9EBD` |
| `visual-plan.md`（v3） | `2BC2EF8407AE25206F28A2A165A97DAD21BC6D5A4008CF04D22A754BBC517130` |
| `visual-plan.json`（v3） | `99505E762A954FDED2FE119B7B475649510F2329C3782B45130492AA4AADF039` |

`git diff ba25e4aad 7caee78c8 -- visual-plan.md visual-plan.json` 顯示 JSON 僅 I01 `post_text` 由「公司回顧：成立於 1989 年｜不是原型比賽日期」改成「**公司回顧：1989 年成立**」；MD 只改版次、O10→I01 說明和審查停線。61 句口播、來源筆記和其他 60 鏡文字／時長無變動；本輪沒有重做完整逐句來源審查。

## I01／O10 與卡片規則

- **O10 PASS**：口播與後製卡分別為「品牌把這場騎乘記在一九八九年；這是多年後的回顧，不是當年賽事紀錄」及「品牌多年後回顧：騎乘 1989」。此歸屬直接對應 [CamelBak NZ 的事後品牌故事](https://camelbak.co.nz/pages/about-us)；仍不把較晚專利的 1988 組合或商標 first-use 聲稱當同一場比賽的日期。
- **I01 PASS**：口播只說品牌與母公司把成立年份記為 1989；新版卡只說「公司回顧：1989 年成立」，符合 [CamelBak 公司歷史](https://www.camelbak.com/company-history.html)與 [Compass Diversified 2014 Form 10-K](https://www.sec.gov/Archives/edgar/data/1345122/000134512615000005/codi-12312014x10k.htm)第 533–535 行。它不再否定 O10 的 1989 品牌回憶，也不以公司成立年替比賽獨立定年。
- **MD／JSON 配對 PASS**：`visual-plan.md` 第 24 行按 O10→O11→I01→I03 說明且逐字引新 I01 卡。JSON 的 I01 是 `kind: card`、只含 `post_text`／規劃時長，沒有圖像 prompt 或 motion。卡片是一項年份與出處，合乎 [curio-episode skill](../../../../.agents/skills/curio-episode/SKILL.md) §卡片只放插圖說不清的數字／名字／出處；實際 12 張卡、最多連續 2 張，低於最多 3 張規則。最長單卡紙上 11.3 秒，低於 15 秒卡片節奏停線。
- **其餘畫面範圍未變**：JSON 仍有 61 個唯一行 ID，同序對上 61 句；49 插圖、12 卡、精確 `look: {"preset":"cute-mystery"}`、MiniMax `image-01`，插圖 prompt 未見品牌／人名或 `cute`、`mystery`、`cartoon`、`chibi`、`style` 等畫風 token。v3 只動 I01 卡，v2 收據其餘逐鏡文字 PASS 的適用檔案內容未改。

正文 505.4 秒、插圖 397.5 秒／78.7%、最長單卡 11.3 秒均為**紙上估計**。沒有 TTS 實測，正文 ≥480 秒、實際插圖比例、圖像品質、盲評和站主劇本／分鏡採用均不由此 PASS；沒有付費、匯入、上傳、發布或合併。
