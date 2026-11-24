# S38 R8j｜`pf006` 日期／人名卡獨立覆核

2026-10-21 00:39 UTC。**PASS：僅限 R8j 無新圖卡片替換及相鄰未畫鏡頭運鏡的書面覆核。整集原生插圖、網站核准與成片仍 HOLD。**我沒有撰寫這次改動，也沒有修改創作檔、私有媒體、帳本或 `STOP`，沒有付費呼叫。

## 版本、差分與已通過的圖

重新計算的 `video.json` SHA-256 為 **`cd28ba2255917a5040c8c84c3275959ca94b29934b5a892595b82e304e8eeb42`**，`visualHash` 為 **`3a63356704b7dedb`**。我從目前檔案的原始文字，獨立還原 `pf006` 原 `shot` 區塊及 `pf007` 原 camera；整檔 SHA-256 精確回到 R8i **`de27c08f77dd91e66703fcf5c875ee1ea787d34246b93bc6237af8c7fcd03861`**，還原版 `visualHash` **`79b6a9303fdfaeba`**。遞迴比較解析後 JSON，與[作者差分](verify-24-r8j-structured-diff.json)逐項相同，恰有八個葉節點：`scenes[5]` 的 `template` 與六個 `data` 增刪，及 `scenes[6].data.camera`。其他解析資料相等；每景旁白、line ID 與 chapter 都相等。

`pf006` 的原句「先回到兩天前。九月二日凌晨，女僕珍妮發現城裡有火。」與章節「九月二日凌晨，佩皮斯看過火又睡回去」對上 [script.md](script.md) 的第六景及 [claims.md](claims.md) 的 `D2a`。卡片寫 `1666．09．02`／`女僕珍妮`／`凌晨，倫敦城裡有火`；僅其模板／資料改為 `big`。未畫的 `pf007` 只把 camera `drift right` 改成 `pan left`，其餘提示詞、台詞均不變。`pf004/005` 的完整 JSON scene **原始位元組**與 R8i 相同，私有原生 JPEG 實測 SHA-256 分別仍為 **`82efccf4b92bc59da94688527fd43e9347ad45d271b048e0877a8f3337bb7921`**、**`34ff83a651a59ba9383091d33151ca4bce62c9d04d6f65bd4bc75dbf55e8c52c`**；現有 manifest 記兩者 judge `passed=true`、`needs_review=false`。這證明檔案與已收圖片未變；R8j 的逐景 request key／judge stamp 沿用仍須由工具核實，不能僅憑紙上比對聲稱快取已更新。

## 日期、卡片與節奏

獨立重取研究稿指定的 GITenberg 日記 `4200.txt`（commit `68fcf49f70ee793b989a6fd0464264d55beb4451`），SHA-256 **`3cd43a3c39ee72eb9c4a3657f1fcb1723afba291cedac176c65a39289483be5d`**。其 *September 1666* 下 `2nd (Lord's day)` 條目寫 Jane 約凌晨三時叫醒佩皮斯，告知她們看見城中大火；他覺得火遠，回去睡。故日期、Jane 名字與「凌晨，倫敦城裡有火」都有 `D2a` 支持。卡片沒有引入 Jane 的年齡、服裝、窗邊姿勢、確切火源或目擊地點。原旁白的「發現」沒有因卡片而擴張成更具體的目擊主張。

[Curio 系列規則](../../../.agents/skills/curio-episode/SKILL.md)規定三張圖與兩輪修詞仍失敗可改相關卡片，正文插圖至少 70%、連卡至多三張，卡片放日期／名字等插圖難表的資訊。先前的[原生停點](verify-23-r8i-final-native-stop.md)已有三次判退與兩輪修詞；本卡以日期、人名為核心。實測正文 **110／111＝99.1%** 是 `shot`，最長只 **1** 張連卡；`pf006` 的既有聲音時長為 **7.10 秒**，低於 15 秒卡片狀態上限。`node tools/video/cli.mjs lint --slug curio-s38 --json` 為 **0 errors／0 warnings**。系列文件另有一句「文字卡不是插圖失敗時的退路」，和它前述具體的三圖兩修後可改卡片規則不一致；本案只採前述窄例外，且卡面承載日期／人名，不把它推廣成其他失敗景的通用退路。

第一章開始於 0 frame，下一章 `pf006` 開始於 867 frame，以 30 fps 計 **28.90 秒**。卡片處於第二章，不能補足 30–60 秒濃縮開場的下限；在成片前仍須處理至少 **1.10 秒**的第一章節奏，並重新核對聲畫時間。

## 停點與有界續畫建議

私有 `/workspace/.video-work/curio-s38/STOP` 實測**存在**。`media-status` 讀值為 US$**0.2895**、17 image、15 judge、1 music，含 `pf003` 舊 US$**0.0035 reserved**；整集原有硬上限 US$**4.58**，本覆核不提高。`pf003` 無已收圖，不得清除預約或重送同一筆未確認付款；`pf006` 不再購圖。

若後續負責人按既有流程解除停點做有限原生試畫，先以工具檢查 `pf001/002/004/005` 的逐景 request key 與 judge stamp；對 `pf007` 起最多五個**指定且未畫**景各只作 `1 take + 1 judge`，逐張看原生 1280×720 與系列畫風，失敗立即停下修詞／審核。以既有單景最高 US$0.0135 估，五景新增最多 **US$0.0675**，ledger 連舊 reservation 至多 US$**0.3570**，仍低於 US$4.58。該方案不包含 `pf003` 或 `pf006`，也不代表全片已過畫面／網站關卡。只有在 30–60 秒開場、片頭片尾與連結、全景原生圖、聲畫 QA 及網站核准都各自完成後，才能標成影片完成。
