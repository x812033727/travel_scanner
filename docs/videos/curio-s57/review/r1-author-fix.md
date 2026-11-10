# S57 R1｜史丹利／李文斯頓作者候選交接

2026-10-20 UTC。這是**作者候選**，不代表全稿史料、畫面、敘事、政策、旁白或成片獲核准。獨立[題材來源可行性](../source-feasibility-1.md)的 A 案有條件 PASS 只涵蓋窄題材，不涵蓋下列逐句稿。

## 凍結的五檔

| 檔案 | SHA-256 |
| --- | --- |
| [research.md](../research.md) | `9663d4a0ea66b1fef3c6e3a0550b8b08cf169a68b1736ad6005d6408ac2cd667` |
| [brief.md](../brief.md) | `ded775a86c0353c44c6ea5cd53265f7d95a61b7539dd61d86eed007a3bac165e` |
| [claims.md](../claims.md) | `f62350da54fc1500576de402faffb87267286a93c9c7b21429b1664a5edf179e` |
| [video.json](../video.json) | `366123f3ace1668236d651bc6decbb9b27b744ed74409fd3d83040e31ade76bf` |
| [script.md](../script.md) | `2ea8113fcd872bf80b8342b2617deb043a4526b5cb43595c2cf532578ee1cdae` |

## 修訂與來源界線

- 固定版 S 是史丹利自己的**節錄**出版敘述，`Abridged` 在 [S33–40](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L33-L40)。固定版 L 是 Waller **身後編刊**的日記，不等於未經編輯的手稿。
- S [10270–82](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L10270-L10282)、[12425–43](https://github.com/GITenberg/How-I-Found-Livingstone--13-Travels-adventures-and-discoveres-in-Central-Africa-including-an-a__5157/blob/41828f7623e5ba1b0db0a4c96630bda15bb0b66e/5157.txt#L12425-L12443)及 L [5741–50](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5741-L5750)都記勸歸與先完成工作的選擇，詳細對白只歸史丹利；勸歸至少在二月補給前已發生，不能敘為開箱後第一次提起。
- 藥箱與藥品有 [L5806–10](https://github.com/GITenberg/The-Last-Journals-of-David-Livingstone-in-Central-Africa-from-1865-to-His-Death-Volume-II--of__17024/blob/bd976e865f60f2bc17628640378e4510969a94ad/17024-0.txt#L5806-L5810)支持。十二月底東行起點，L5458 記 12 月 27 日、L5779 回顧從 12 月 26 日行軍；口播／日期卡僅說「十二月底」。
- 相遇日：S 記 11 月 10 日、L 的相遇段有*斜體圓括號* 10 月 28 日；不把它叫方括號編者註，也不選任一精確日。全片僅說「1871 年晚秋」。地理水源連結是當事人當時假說，未畫成今日精確地圖。

## 作者實測

- `node tools/video/cli.mjs lint --slug curio-s57`：**0 errors／0 warnings**；14.5 分鐘估算、189 句、12 組開放與回收。開場章 00:00–00:44，之後插入既有 **5 秒頻道片頭**；故事正文 2,688 個漢字，按每分鐘 325 字的快語速下界為 **8.27 分鐘**。
- `video.json` 189 場景有 **170 個 cute-mystery 插畫鏡頭（89.9%）**與 19 張排版卡；逐句 [claims.md](../claims.md) 有 **189 列**對應固定文字行號。正文每 45 秒內有鉤子，書面畫面仍待獨立判定；實際生成插畫亦要逐張看。
- `npm run test:docs-videos`：**236 pass、0 fail**；`npm run check:tasks` 退出 0，僅有與本票無關的既有跨票及逾期警告。
- [brief.md](../brief.md)列 **21 秒固定 `v4-endscreen`**，最後 16 秒留兩個推薦連結與訂閱圈；真實可點元素待私人上傳取得 YouTube ID 後於 Studio 設定。說明欄附兩個固定全文 URL 和頻道連結；Shorts 須在長片定稿後節錄並回連，不填虛構上傳網址。

## 待辦關卡

請未參與撰稿者對這五檔作 **189／189 逐句來源與書面畫面覆核**，明確檢查日期、史丹利單方逐字敘述、身後編刊與編者轉述、在地人物與殖民措辭。另請兩位**新且無本集前情**的讀者各自只讀 `script.md` 和官方 `narrative --json` 的 13 題，投獨立原票後按流程合併；作者不自評。其後才可做政策及旁白開工檢查。**未呼叫付費 TTS、插圖或配樂，亦未作站主核准或成片宣稱。**
