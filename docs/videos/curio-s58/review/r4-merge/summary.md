# S58 R4｜正式雙盲敘事 OR 合併診斷

2026-10-21 UTC。**敘事 HOLD：兩位新盲讀者各為 11／13 YES，正式固定 OR 合併仍為 11／13 YES。** 兩票共同否定必答題 `chapters_link` 和 `no_recap`。另見 [R4 獨立史料／書面畫面覆核](../r4-source-independent.md)：三個窄範圍仍 HOLD。未修改五份 R4 創作檔，未進入語音或插圖付費步驟。

| R4 凍結檔 | SHA-256 |
| --- | --- |
| `research.md` | `0adab42902bd00393a4b7c945a4b37a9eae4f61e79cbbd2710085713f8643132` |
| `brief.md` | `8d0d42c6c5cf1de97ee8b497db3d298540b9fc21e1fe3bcee024b749c8960e08` |
| `claims.md` | `f0e340870fa7389224932ca732950fb990b4bdebcf4baaabf2d93fa3d994edc1` |
| `video.json` | `78960f72a00a5fcc245896d680bc18f9481cef6c472dd9fc94d82ad80ae7e547` |
| `script.md` | `b9451d33643dccd8ffc84f4a6f93074f4500adb50855f7a5529d9620eeaa8d0c` |

## 原票、正式合併、CLI

[A 原票](raw-ballot-a.md)和[B 原票](raw-ballot-b.md)逐位元組複製自 `../r4-blind-a.md`／`../r4-blind-b.md`，SHA-256 各為 `965de7b59b68e381db7486aa3d79071de7a058d34f4b05ce5c59aa0190e071b1`、`f0380deb62cd71f4ea66d1ac11d9c7fd1f11c049dfbe98b34139f2337a7f4be0`。用[轉錄程式](build-merge.mjs)依官方 `NARRATIVE_PANEL` 順序建立 [A](ballot-a.json) 和 [B](ballot-b.json) 答卷；[稽核](merge-audit.json)記載原票理由、對應場景、所有雜湊與官方 `PANEL_RULES_SHA256=5d71fef2cf3831dc33c0c32b2b297f633c47bfe41fbad18865ae08ed0c91cb75`。

官方 `mergePanelVerdicts` 的固定 **OR** 規則：任一帶場景 ID 的 YES 可令該題通過；兩位皆 NO 才不過。[合併答卷](merged-answers.json) SHA-256 為 `63279bd72dd43b78e3e3c6477a194492521da2a78228aae0ea71362c50e3ed4e`，11 YES、2 required NO、0 advisory NO。[CLI 執行收據](cli-status.json)在隔離 `/tmp` 工作目錄以前後 SHA 確認五檔未變；[原樣 stdout](cli.stdout.json)、[stderr](cli.stderr.txt)、[退出碼](cli.exit-code.txt)、[官方紀錄](official-narrative-record.json)均封存。正式命令 `node tools/video/cli.mjs narrative --slug curio-s58 --answers docs/videos/curio-s58/review/r4-merge/merged-answers.json --workdir /tmp/curio-s58-r4-merge-formal-TWX8IH --json` 得 **exit 1、`passed:false`、兩個 required fail**。官方紀錄 SHA-256 `43b9d65e5b82d67f8dd6addc6ab277454dfcc52e7bdfe2a6b1f90832267c382a`、`narrative_hash=47b3ce24d3bb651f`。

## R5 窄修目標

| 阻擋 | 兩票共同證據 | 修訂方向 |
| --- | --- | --- |
| `chapters_link` | `s58107` 章末問一鳥可帶幾片，`s58108` 下一章首句又問一次；A 亦指出 `s58055` 的器材留存問題與 `s58056` 的衣物開頭銜接弱。 | 下一章首句直接從上一問推到一片容量的新事實，避免重問；第二車章首從倖存器材與換裝搬運的因果接入。 |
| `no_recap` | `s58079` 說 Dagron 抵 Tours，`s58080` 緊接重說抵 Tours。 | 卡片保留抵達日期；後句直接推進他手上的既有薄膜樣本與當地紙郵務工序。 |

R4 的來源覆核另指出 `s58071` 酒桶提示詞把桶放在稅卡前、`s58089` 一幅圖要求兩動作、`s58141` 畫實際裝載材料且 `s58142` 把**請求的氣球寄回方式**寫成已證實運輸。R5 作者須同修這些項目，並重對齊 `claims.md`／`script.md`；新五檔另立 SHA，重新交非作者來源與兩位新盲讀，不能沿用 R4 原票放行。
