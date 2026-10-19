# S03 音檔覆核後終稿與旁白

日期：2026-10-19。現行 `script.md` SHA256 `2234d642112d0e8322555d46c37ddd08ab978db614b76c45d5b3229128a624b1`，`video.json` SHA256 `f5c2873b475e544d1d6c13c2136f8635d40218bdbc11c56e305cfe2a0d83e80b`，narrative hash `11a95e26a6291430`。終稿 101 句、88 張插畫，估 9.1 分鐘；實際 Gemini Sulafat 旁白 **09:36**。`lint --slug curio-s03` 為 0 errors／0 warnings。

## 音檔訂正

第一版旁白逐句核對 103/103，21 句被標出；只重錄那 21 句後剩 7 句。它們多涉及不常見人名、同音字或措辭；例如「郭沖第三事」被轉寫成「國中第三冊」。嘗試以本機 `faster-whisper` 作第二轉寫，但模型下載受此環境代理 HTTP 403 阻擋，故沒有把第二轉寫說成已通過。依 `curio-episode` 的「重錄仍錯就改句」程序，改寫 `ef023`、`ef053`、`ef054`、`ef080`、`ef088`、`ef100`，刪去重複的 `ef076`。改句後僅 `ef100` 仍把「琴聲」轉寫成「情深」；該句也重複片尾主旨，遂連同一張重複畫面刪除。最後一次合成重用已付費的 100 個請求，新增請求 **0**。

現行旁白重新跑 `check-audio --slug curio-s03`：**101/101 句已核對，92 句逐字相符，8 句僅同音字或語助差異，1 句經 Jev 判為可接受，0 flagged**。證據在 `VIDEO_WORKDIR/curio-s03/review/check.json` 與 `check-flags.json`，後者 `flags` 為空。現行 speech hash `c9fe465a170aed16`。所有媒體與權杖都在 `/workspace/.video-work/curio-s03/`，未進 Git。

## 終稿敘事與來源

改寫後的第一個版本由未參與撰稿的讀者盲讀 13/13 通過，並逐句核 `ef023`／`ef053`／`ef054`／`ef080`／`ef088`；刪 `ef076` 不改主張。最後刪 `ef100` 後，**另一位全新讀者**只讀現行旁白和 13 題，再以精確 SHA 作答，`narrative --answers` **13/13 通過**。原始逐題回答見 [`narrative-answers.json`](narrative-answers.json)，工具結果在 `VIDEO_WORKDIR/curio-s03/review/narrative.json`。該讀者另核 `ef099`→`ef101`：小說的琴聲與裴松之「難曰」的史料界線、片尾銜接均無缺口。現行 `script` 本機關卡重新綁定上述 SHA，批准註明站主是廣泛委託，未逐字審稿。

MiniMax `keyframes --takes 3 --dry-run` 對**現行 88 張**報一輪約 **US$1.19**，最多三輪 **US$3.56**；本集插圖目前 US$0，付費生圖仍依主代理排程協調。這是估價，不是已購買素材或已完成影片。
