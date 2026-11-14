# 素材池驗證（2026-11-13，revision `2026-11-13-pool-4861`）

由 4,860 增至 4,861 個入選核心（[前版驗證](VALIDATION-4860.md) · [舊庫快照](checkpoint-4860.json)）：

1. **拆開 `E7006` 與 `E11012` 的誤合併（`2026-11-11-stw-pool-e7006-source-ref`）**：`E7006`（冰河退去後埋藏死冰延遲融化形成鍋穴，`SRC-2bc7ad5b83b3068d`）與 `E11012`（永凍土多邊形邊界冰楔退化下陷造成中央相對地形反轉，`SRC-f2de49ac9ccccc6e`）核心機制與成因位置不同，`E11012` 自己的原註亦寫明「與E7006埋冰鍋穴不同」。在 `dedup-decisions.json` 改判 `distinct`、`selection.json` 納入 `E11012`、`themes.json` 的 `G120` 改直接引用 `E11012`，使 `E7006` 不再掛無關的北極冰楔來源，`G120` 也不再掛大提頓鍋穴來源。
2. **補上單一來源引用排除機制（`excluded_source_refs`）**：在 `tools/video/so-thats-why/pool/core.mjs` 與 `render.mjs` 支援於 `dedup-decisions.json` 宣告具理由的 `excluded_source_refs`（核驗 canonical `candidate_id`、已知 `source_id`、非空 `reason`、選填 `origin`／`locator` 條件，並拒絕懸空規則或移除合格核心最後一筆來源），於 `DEDUP.md` 公開稽核紀錄。

## 本機檢查

- `node tools/video/so-thats-why/pool/cli.mjs build`、`check`：PASS（5,250 筆原題、5,090 個合併後核心、4,861 個入選、629 組題案、高相似待決 0）。
- `node tools/video/so-thats-why/pool/cli.mjs index` 連跑兩次：第二次 `UNCHANGED`（`writes: 0`）。
- `node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`：33 項通過。

這些檢查不代表完整製作稿或成片驗收，沒有做搜尋頁的瀏覽器檢查，也沒有讀遠端 CI。
