# S46｜本地前製驗證（非獨立審核與站台核准）

查核日：2026-10-20。推薦 A 案已做成完整本地候選稿。此文件記錄製作人自查，沒有冒充獨立史料審核、兩名盲讀者或站台批准。此版凍結後如修改任一候選檔，須更新雜湊，並重做相關審查。

## 固定原文與候選版本

- Elizabeth Blackwell, *Pioneer Work in Opening the Medical Profession to Women*（1895），[GITenberg 固定提交](https://github.com/GITenberg/Pioneer-Work-in-Opening-the-Medical-Profession-to-Women_65496/blob/16787df4911754c8e0401d12c896b943768f5d8d/65496-0.txt)：提交 `16787df4911754c8e0401d12c896b943768f5d8d`，原始 TXT SHA-256 `b52caf559d763349953fe31101016cfb2d68662f152c28a564b6a6b93cac8ec6`。此書已逾 130 年，引用少量史料短語；影片不用外部圖像或原件翻拍。
- [research.md](research.md)：`ffcab3d4559ef2ded2ddb741e39f3e03042fcbfed801c94e1b2f9dba9925163f`。
- [brief.md](brief.md)：`e8ebaad61c4443571f796263e9b956e5e97169cd0bb3d1717fd5faa1deb2ff20`。
- [claims.md](claims.md)：`e384c77d062fb0270ed3f880efac4561ec1626b731c499bfa9d261caccac6c13`。
- [video.json](video.json)：`897bb692f49a93a3a5707ecb27fe92828db0cf8ee9ec69fe7206aad55ab94199`。
- [script.md](script.md)：`7f7d31168408abae311e114abc9d212dd71536a69519a206dbf8c0eee4153fe3`，由同版 `video.json` 的 `script` 命令產生。

## 查核焦點

原書 1847 年院長信與全班決議是 1895 年回憶錄中的**轉錄**；1895 年作者說的是部分學生曾懷疑**她的申請**為敵校騙局。這不能證明表決是惡作劇，也不能反推每人的真實投票動機。醫院董事的全票是另一場表決。劇本逐句對應 P01–P14，並以 1849 年日記中的正式文憑收束入學承諾，未說她是世界第一位女醫師。

## 形式與可製作性

- `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s46 --json`：**0 errors／0 warnings**。八章、13 組伏筆回收。`script --slug curio-s46` 已成功產稿。
- 128 景正文中有 **123 景單人 `shot`（96.1%）**、5 景少量有來源卡；131/131 旁白句在 `video.json`、`script.md`、`claims.md` 逐字一致。提示詞不要求現代裝置、群眾、手術、可讀假信或真實人像；插圖仍須先做原生樣圖及人工檢視。
- 工具估計口播 **10:40**：濃縮開場 **44.6 秒**，開場後至口播片尾前的故事正文 **579.1 秒（9:39）**，口播片尾約 **16.4 秒**。時長不是合成語音的實測。規劃把既有五秒原創片頭接在濃縮開場後，並在正片後接既有 21 秒 `v4-endscreen`；可點的兩部推薦片及訂閱圈須私人上傳後在 YouTube Studio 設定並試點。
- `npm run test:docs-videos`：236/236 通過。`npm run check:tasks`：驗證 2116 張任務票通過，另列既有逾期認領與跨票範圍警告。`git diff --check`：通過。

## 待通過關卡

尚需未參與寫稿者對**同一凍結版**逐句檢查史料和 128 景文字／畫面界線，並由兩名全新讀者各自盲讀原旁白、回答正式題本。這些完成後才依站主「採推薦」指示做透明標示的本地大綱／劇本選擇；站台審核狀態仍如實保留。尚未生成 S46 語音、圖片、配樂、短片或成片，亦未上傳或設定可點連結。
