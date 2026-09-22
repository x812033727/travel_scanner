# 交接範本

狀態放兩個地方：**持久工作區**的 `STATE.md`（協調者自己的真相來源，隨手更新）和**批次 docs 目錄**裡的檔案（進 repo，給下一個人）。session 的 scratchpad 會消失，什麼都不要只放在那裡；交接時整份複製出來。持久工作區是 repo 外的一個固定資料夾（例如使用者家目錄下一個專用目錄），路徑寫進票的 Notes。

## `<WORKDIR>/STATE.md`

```markdown
# 協調者狀態（<日期> 起，session「<名稱>」）

計畫檔：<路徑>（已核准／草稿）。本檔是接手用的真相來源；scratchpad 綁 session，不要把狀態放那裡。

## Worktree 與票
| 線 | worktree | 分支 | 票 | 狀態 |

## 環境
venv：<worktree>/apps/api/.venv（uv sync --frozen 已跑）。Chromium：<路徑>。

## 工作區佈局
<WORKDIR>/<slug>/（pack.json、diagram-1.svg、images.json、notes.md、report.md、verify-N.md）；helper 腳本 <WORKDIR>/_tools/<slug>/。

## 波次
| 波 | slug | 撰稿 | 查核 1 | 查核 2 | ingest | 備註（時效列、共用數字、要重查的日期） |

## 裁決紀錄
- <日期> <裁決一句話>（理由；適用哪些 slug）

## ingest 當天要重查的列
| slug | 事實 | 日期 | 怎麼處理 |

## 共用數字組
| 組 | 數字 | 出現在哪些 slug | 不得出現在 |

## 額度紀錄
- <時間>：5 小時窗 x%、週 y%；用了哪個模型做哪個角色

## 接手的人先做什麼
1. 讀這份與票；2. `git fetch`，看分支與 PR；3. 對照波次表把「派出」但沒有 report.md 的 slug 當未完成處理。
```

## 批次 docs 目錄（進 repo）

`README.md`

```markdown
# <批次名稱>
## 清單          ← 表：# | 規格 | kind | destination_id | topics | display_order | valid_until
## 給撰稿者：通用規則
### 本批與上一批不同的地方   ← 只寫差異，其餘指向上一批 README 與 ERRATA
### 撰稿當天必須重查的時效事實 ← 表：slug | 事實 | 日期 | 撰稿時怎麼處理
### 「讀不到的官方站」更新
### 工作區與檢查指令        ← 一行指向 .agents/skills/content-pipeline/SKILL.md 的指令段
## 給協調者：收件步驟
## 淘汰或延後的題目（可選）
```

`FOLLOWUPS.md`

```markdown
## 1. 有日期或條件觸發的複查   ← 表，上線 PR 開成票
### 建議的開票分組
## 2. 既有文章要補的反向連結
## 3. 既有文章的錯（已開票）
## 4. 查過、決定不處理的
```

`ERRATA.md`：規格發出後的更正與裁決，每條一個標題，寫清楚「原本怎麼寫、改成什麼、為什麼」。

五語系新聞批次另有 `HANDOVER.md`，骨架照 `docs/news-2026-batch-4/HANDOVER.md`：每個子批次一節「現況」與「留給站主決定的事」、「還沒做完的事」、「定下來、接手的人不要再翻案的決定」、「學到的（寫給下一個協調者）」。差異檔 `agents/DELTA-<批次>.md` 開頭一句「這份文件的規則優先於各垂直規格裡與它衝突的句子」。

## 票（`tasks/open/<id>.md`）

票的檔案就是交接。停手前把 Steps 打勾、Notes 寫上工作區路徑、STATE 檔位置、還沒做的事，然後 `npm run tasks -- release <id>`；合併後 `npm run tasks -- done <id>`。
