# A01 r45 獨立窄範圍差異審查

**判定：PASS，僅限離線 r44→r45 差異。** 這不是 r45 全章故事、史料、畫面、配音或成片的正式複審，也不構成開拍、付費或上架核准。

- 凍結目標：`A01-editorial-candidate-20261019-r45`。
- r45 `manifest.json` SHA-256：`4bba4d5b429b6de634c3982aa01027b1d0befd84664aef640d533af0302d05ac`；讀回符合預期。
- 來源 r44 `manifest.json` SHA-256：`62cec617460b882309a48ca76c69615ec20789502538149cc94e47a632144190`。r45 manifest 所鎖定的 r44 三份審查報告仍與實體 SHA-256 相符：盲故事 `425c63d256a5578a7122355520be7589635dd8f261a2694837450158c69f7db1`、來源 `cdb5687bc114717d6399e60d813ba888aa87c3dd6ad9e69ad680fb19cf16a147`、畫面 `e6baa54e3d2de9a9b0969ea24a8d79cdccf29fdeb2b2997baa5b2a5ecfdd0cb2`。
- r45 `node build.mjs --check`：exit 0；51 scenes、53 lines、275 字／分鐘正文估時 424 秒、0 errors、40 warnings，並回報 `prior_three_main_warnings_resolved: true`。

## 差異與敘事判斷

比對 r44/r45 的 `candidate/script.md` 與 `candidate/video.json`，台詞只改三處：

1. `engine-patent-stow`（`script.md:122`，`r44l026`）把「怎麼過機艙窄走道、收進座位下。」改成「怎麼過機艙窄走道、收進座位下？」。這把已有的專利設計考量讀成待解問題，沒有提早揭露後段外袋原因。
2. `turn-fabric`（`script.md:176`，`r44l039`）把「另一個問題是，它能裝多少。」改成「另一個問題是，它能裝多少？」。問題承接耐用性之後的容量考驗；句內資訊未變。
3. `now-outro`（`script.md:227`，`r45out3`）在觀眾留言問題與訂閱邀請之間加入「資料來源放在說明欄，想追細節可以接著看。」這是查閱來源的 CTA，**不是新的歷史事實主張**；不需為這句另開史實查核，但原有 55 項史實 claim 仍為 `PENDING`。

重新以現行本機 lint 比對：r44 為 0 errors／43 warnings，r45 為 0 errors／40 warnings，沒有新增 warning。消失的三項分別是原結尾只有兩句，以及 03:02–04:41、04:41–06:24 兩段缺少開放問題。兩個問號的落點補上中段前進力；新結尾第三句處理來源入口。因果順序仍是 `now-stow-fail`（`script.md:202`）先見收納失敗，`now-pocket`（`:206`）才揭露擴充外袋和加放物品，`now-empty`（`:214`）再顯示取出物品後成功收好；章名沒有先說出外袋原因。

`candidate/claims.md`、`candidate/lexicon.json`、`source-alignment.json`、`source-map.json` 逐檔 SHA-256 與 r44 相同；`video.json` 的 loops、各場畫面資料與 prompts、sources、YouTube description、voice 設定、subtitles 設定在結構比對中相同。新 CTA 已是 `video.json` 的旁白 line，會進入後續語音與字幕時間軸。字幕設定維持 `burn_in=false` 的可切換字幕；實際配音及 CC 檔尚未製作或聽驗。說明欄模板雖未改字，但 `video.sources` 仍有六個來源 URL，現行 metadata 組裝邏輯會附上來源；交付前仍須讀回實際上架包，確認 CTA 指向可見的來源清單。

## 時長與界限

正文紙本估時在 275 字／分鐘仍是 **424 秒（7 分 04 秒）**，與 r44 相同；250／300 字／分鐘約為 461.2／392.2 秒。424 秒僅比七分鐘下限多四秒，因此實際 TTS、停頓、轉場及成片必須另行驗證 7–8 分鐘。此 PASS 只確認三處差異未破壞已鎖 Rollaboard 故事線及既有離線檢查；不能替代 r45 全量章節／媒體審查、未完成的史實查核、實際聲畫及上架前讀回。
