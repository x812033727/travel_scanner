# B18 Row10：獨立來源與口播邏輯審查

- 審查日：2026-10-17；審查者：Codex `/root/b18_script_scene_alignment/b18_route_b_plan_review`，未編寫本 Row10 候選。
- **結論：HOLD；P1 0、P2 1。** 十筆事實的離線 schema 檢查通過，六個文字欄位的來源界線可追溯；但 `must_verify[9].attributed` 與固定第三版全文 T06 的口播歸屬不一致。此收據不是可匯入企劃、正式 reviewer JSON 或影片核准。
- 受審候選：`B18.json` SHA-256 `73a00f868eb625161cd2a0e9d3692138071b596a3b0c67dfa78d0c6bec3d332f`，`routing-amendment.json` `163a55afba504989cd8be35caddd3d0e7aa10c7cb326b19eb1a0f523ec8f3d44`，`delta.json` `616812d1923f4380d380f1c17868bf111363dff09f7a599aed3067cf5efe120b`，`verification.json` `5c69894e4d4fd0272bb65cfa78766367702f60a74acd7a0f080ac236cdb5f3b7`，`build.mjs` `c8b9b4c7fd2dd1eb1f523f581d4944d1e0807428ca676ff35120fd66002017a9`，`README.md` `0ffe04ec61e7f24a5fe65e5fcd93370cd577fd74b8d16dbf60565ca31f1257a8`，`sha256.json` `d8daa122fd4da608427119c1b7167e4b3485573837060048618962412b4f8863`。Canonical story SHA-256 `3510e058c3112c0c4eef388f4659c1884b41bb6d3e78122a80a1c1cfc8360691`。
- 固定對照：父版 row `c9aab2d7c9ebc1e0bb23d779a411deae9f9526b0f8ef7720af74754031ed3681`；第三版全文 `7b2865668d8cdd21a87cd813b015ebc0088f3728712181063768d9323200e8c1`，其獨立審稿 `603f0a5340b197cc6cbe527991e63bb1629c4f1245e780fdb3981109dea871d4`。現行 `tools/video/story-plans/plan.mjs` SHA-256 `5ec625989c2aa9f86ea837b6c03f189554746618825292ad1c30fad1b6988de5`；`tools/video/automation/story-prompts.mjs` SHA-256 `aa6facb5683aceb2af5b98ad3ce2d0ce6d87e84bd9afaad0b3e3cf2cd18c6fa2`。

## 六欄位及來源核對

| 欄位 | 獨立判讀 |
| --- | --- |
| `chapters[hook].point` | 第三個開場問句改成後場至客席，對應已審全文 H02 與 T04 回收；轉角堵帶掉盤、萬博西口站前出店由 J-Net21 記載。這只是 row beat，舊 hook scene 尚未更新。 |
| `chapters[turn].point` | 將 1967 授權展店放在萬博前、1972 特定權利期滿放在其後，未寫成所有權利到期或同一家公司／機器不斷改裝；盤色亦未硬定年份。和全文 T01–T06 的路線相容。 |
| `must_verify[4].claim` | [日本法院官方判決](https://www.courts.go.jp/assets/hanrei/hanrei-pdf-13913.pdf)理由 P8 L476–495 記獲准使用餐台與標示的**訴外元祿**在 1967 年開仙台直營首店、東京錦糸町連鎖首店；P10 L574–578 記第 579776 號權利 1972 年期滿、其後有與原告無關的多家公司營業。兩段雖是複合事實，均限於同一法院判決與清楚的兩個時間點；原告與訴外公司、特定權利與所有權利均分清。來源 [3] 是 PDF，正式新 row 審查收據須列 `reviewer_only: [4]`。 |
| `must_verify[9].claim` | [發明協會沿革](https://koueki.jiii.or.jp/innovation100/innovation_detail.php?eid=00026&age=high-growth&page=keii)同頁分別記後場製作／直線送盤、後來多價盤與以盤色或裝飾區分價位。文字以「不同店在不同階段」限制，沒有推成首店改裝或所有店同時採用；兩個子主張均只引來源 [2]。**口播歸屬仍有下列 P2。** |
| `sources[2].supports` | 加入同頁盤色／裝飾、郊區大店與家庭用餐，仍保留與法院 1972 年認定衝突的 1978 年說法僅作版本註記；沒有把來源衝突當新定論。 |
| `sources[3].supports` | 加入法院 P8 L476–495 授權訴外公司展店，並保留 P10 L574–578 的特定權利判定和另一權利未判期滿的界線。 |

## P2：複合 fact 9 的口播歸屬不能同時保留原稿

`B18.json/must_verify[9]` 為了沿用一個 [2] 來源、維持 10 筆上限，將後場直線送盤與盤色定價合為一筆，且沿用 `attributed: true`。現行撰稿／查核提示 `story-prompts.mjs` 第 39–40、171–173 行要求被標記的**整筆 fact** 在旁白中說明是誰的說法。固定第三版全文 T04 明說「發明協會記錄」，但 T06 直接說盤色或裝飾區分價位，沒有可聽見的來源歸屬；T06 製作註還把這些稱作非 attributed 事實。僅在字卡或製作註標 [2] 不等於旁白歸屬。若照 Row10 匯入，正式 verifier 可能改寫 T06，破壞固定全文與其 SHA 審稿；若不改，則違反 fact9 的審稿規則。須另出後繼候選解決此粒度問題，並對最後位元組重新審查。

## 邊界與後續

直接以 `STORY_KEYS`／`storyProblems` 重算，本候選 `must_verify` 為 **10** 筆、schema 問題為 0，story SHA 與候選 verification 一致；`build.mjs --check` 亦通過。舊 row 審查 `story_sha256` 不符新 row，**不能沿用**，新審查收據仍須按最後 SHA 另寫。父版 85 景和 65 個 claim ID 都保持原位、全是 `UNCHECKED`；`t3` 與 `t18` 的新 fact 路由仍只是離線 amendment。沒有新 85 景／88 句、逐章 verifier、聽眾審稿、TTS、畫面、CC 或成片。此審查沒有主機、付費媒體、匯入、上傳或發布操作。
