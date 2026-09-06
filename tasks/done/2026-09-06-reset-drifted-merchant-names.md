---
id: 2026-09-06-reset-drifted-merchant-names
title: 撤回 name_en 之後，既有的列還留著沒有出處的音譯
status: done
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T22:08:47Z
created_at: 2026-09-06T22:08:46Z
completed_at: 2026-09-06T22:31:52Z
branch: claude/merchant-name-reconcile
depends_on: []
scope:
  - apps/api/app/foods/trend_import.py
  - apps/api/app/cli.py
  - apps/api/tests/test_trend_import.py
---

# 撤回 name_en 之後，既有的列還留著沒有出處的音譯

## Why

`2026-09-06-merchant-english-names-unsourced`（PR #294）把七個查不到出處的英文名從
`trend_merchants.json` 移除了。但**正式站那七筆一個字都沒變**：

```
taipei-dong-qu-fen-yuan                  Dongqu Fenyuan       東區粉圓
tainan-jin-de-chun-juan                  Jin De Spring Rolls  金得春捲
kaohsiung-hao-shuang-huang-bu-zong-dian  Hao Shuang Huangpu   蠔爽 黃埔總店
...
```

原因和 [[2026-09-06-backfill-merchant-english-names]] 一樣，只是方向相反：`trend_import`
對看過的 slug 一律跳過，所以**加**英文名不會生效，**撤回**英文名也不會生效。

既有的回填指令幫不上忙——它只在 `name` 還等於檔案裡的中文名時才動手，而這七筆現在是英文名，
所以它回報「已經符合檔案」然後什麼都不做。它沒有回頭的路。

## Definition of done

- [x] 有辦法把「名稱既不等於檔案現在說的、也不等於檔案以前說的」那種列拉回檔案的說法。
- [x] 這個模式不會在沒有被要求時發動，因為它分不出「撤回造成的殘留」和「後台改的名字」。
- [x] 正式站那七筆回到招牌原文。

## Steps

- [x] `plan_english_name_backfill(..., reset_drifted=True)`：名稱對不上檔案時也列入變更。
- [x] CLI 加 `--reset-drifted`，說明裡寫明它分不出後台改名，要先看 dry-run。
- [x] 測試：撤回 `name_en` 之後，預設模式什麼都不做、`reset_drifted` 才把它拉回來。
- [x] 部署後在正式站先跑 dry-run——清單是**八**筆，不是七筆，見下。

## How to verify

```bash
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli backfill-merchant-english-names --reset-drifted
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli backfill-merchant-english-names --reset-drifted --apply
```

## Notes

**這個旗標分不出兩件事**：撤回造成的殘留，和後台管理員刻意改的名字。兩者在資料裡長得一樣。
所以它預設關閉，而且每次都先把每一筆變更印出來——套用前要有人看過那份清單。目前正式站沒有
任何一筆是後台改過的（回填的 dry-run 顯示 0 筆 renamed），所以這一次是安全的。

## Result（2026-09-07）

七筆都回到招牌原文了，第二次執行變更 0 筆，公開頁 200。

**但 dry-run 印出來的是八筆，不是七筆**，而多的那一筆會造成真正的資料損壞：

```
tainan-fu-sheng-hao | Fu Sheng Hao -> 富盛號
```

那是**兩家不同的餐廳共用一個 slug**。策展目錄裡它是福生小食店（英文名 Fu Sheng Hao），
trend 檔案裡同一個 slug 是富盛號。匯入程式保留了策展那一家，所以正式站是福生小食店——
套用下去會把它改名成別人的店。

已加防護（PR #297）：策展目錄擁有的 slug 一律不碰，理由和匯入程式本來就遵守的規則一樣，
兩個檔案對「這個 slug 是哪家店」的說法不一致。碰撞本身另開
[[2026-09-06-tainan-slug-collision]]——`slug_for()` 把富盛號和福生小食店都拼成
`fu-sheng-hao`，所以富盛號從來沒被匯入過也永遠不會，而匯入時只會讓
`skipped_existing_slug` 加一，沒有任何地方報告這件事。

**這就是為什麼那個旗標預設關閉、而且寫入前先印出每一筆。** 我在上一則說明裡寫過它分不出
「撤回造成的殘留」和「後台改的名字」，實際跑起來遇到的是第三種情況——我沒想到的那種。
