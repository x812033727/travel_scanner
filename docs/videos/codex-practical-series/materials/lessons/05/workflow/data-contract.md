# 本課 v1 資料契約
文件 version=1；每項 id/title/completed。ID 唯一，title 可同名且須1..100非空白字元，completed是真正布林。
篩選、搜尋、刪除以 ID 保持資料與順序；不可以title當唯一值。不得刪測試、改成含糊成功條件。
儲存鍵 mokaair-codex-practical-v1，資料損毀時原值保留，禁止 localStorage.clear()。
