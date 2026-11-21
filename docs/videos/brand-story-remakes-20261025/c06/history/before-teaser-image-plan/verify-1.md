# C06 Play-Doh｜r3 獨立來源與書面配鏡差分查核

查核者：`/root/c06_r3_source_delta`。未撰寫或修改中文稿，未讀任何敘事盲讀、讀者答案或 panel 投票。

**SOURCE PASS／WRITTEN VISUAL PASS。** 本輪實核 r2→r3 只刪四句四景；重新閱讀全部163句及137個書面 shot prompts，另1個outro為編輯收束。所有存續 scene 完整物件、claims、逐句證據與配鏡映射均與已綁 hash 的 r2 相同。逐句與逐景結果在獨立 JSON 收據中。

## 綁定輸入

| 輸入 | SHA-256 |
| --- | --- |
| video.json | `45057c33f3c6efa3510c5c27f1f9c03172ba7ebbea5a2914ac0b01e0693e0a13` |
| script.md | `a5a00dab26911197bbd96faaf5fef760396d3eaabd68e45a3072bff350683817` |
| narration-only.json | `4773cd50bd7c5a21910106a57b02b48ce7a7f24111a69698657ce25cf341b70b` |
| claims.json | `270cf9419dc401d2a6381363fbd187cb0bf09f01cdc5c3a114eb8eb10d10e926` |
| reviews/source-r3-independent.json | `4344facd461d0b53fa034d7e5ac0a49e1f96e75f24604bff56e5e93c2b3fe0b0` |

## 實際差分

刪除 `c6so121`、`c6so122`、`c6sb17a1`、`c6sb17a2` 及其四景；未新增或改寫任何存續旁白／prompt／鏡頭／燈光。所有非 scenes 的 video 欄位、原研究與來源目錄維持原樣。claims 與 source-anchors 對應刪除，沒有懸空 loop 引用。script 只有版本標題與四句刪除。

逐一覆核兩個刪除接點：`c6so112→c6so131` 仍由清潔需求下滑接到尋找另一雙手；`c6sb172→c6sb17b1` 仍先說充分乾硬後不能重揉，再比較預先選色與乾硬後繪色。刪除未拿走來源歸屬、條件或關鍵證據。

## 重開實際來源

沿用當日已實際 HTTP200 讀取的原件快取，本輪重新開啟原件、重算 raw/text bytes SHA，閱讀所引段落與專利全文相關處；P1 原始掃描第3、4頁另以影像重讀。未宣稱新發網路請求。

| 原件 | 實際 bytes | 原件 SHA-256 |
| --- | ---: | --- |
| H1 | 35397 | `12c3a40ee1f8b19012447903cfbcad820ee55bc6e80fde8cd494b948b164ee78` |
| H2 | 36534 | `faf0487550b58005ae7f073583ab5a07f9cdabab37cc769e966884d3be8d8cfc` |
| H3 | 34631 | `59479f5fd92ec190bccbf0dad30d3be50d096ccab14b36ad5f8e5b193f1a1392` |
| K1 | 314017 | `e703d65813edf4c52278228a431f9394b953f88cd3e96239b15bf2252ad2a209` |
| M1 | 415288 | `704a6072eefcdab78b8a1d52ee49c23d936ac67a5ace7b3566cdc1f14db42fc4` |
| M2 | 399913 | `5295caa008a71a3c7a618974131735d7c316022171ef4868e4278b9a93969b77` |
| P1 | 699681 | `725a8c64f41c4eedd8c69202e047e19f447f49eadd3adcb1e8708c0faaab27f6` |

M2實際快取為5295caa…，不同於作者早期研究目錄7139f858…；本輪依已重開實際快取第162段，不冒用早期bytes。G2沒有可用raw cache且本稿未引用；G1/H4/H5也沒有被現稿引用，未用它們替旁白補證。

來源界線維持：1933／1949／1955是公司或館方後出回顧；Kay身分由K1/M1支持；M1與M2同屬The Strong。1960申請與1965核發分開，保型是claim9；混合、立即密封、可選binder及薄膜假說皆保留專利範圍。最長三年須密閉保存並玩後放回，是文本聲稱；乾硬不可重揉不是所有今日產品規格。2024數字是年出貨罐數；2026成人定位、噴霧保存數月是公司公告，不是本次實測。

所有圖為匿名概念示意，硬黏土困難後才是柔軟材料；沒有品牌人物肖像、可讀偽史料、顯微實驗或已驗收生成圖的主張。

## 範圍

這份 verify-1 只確認上述 r3 四輸入的來源與書面配鏡。**不授予站主批准、敘事盲評、實際時長、媒體 QA 或字典發音批准**；無付費、provider、後台或 git 動作。歷史 r2 收據與 verify 未修改。
