"""Record local completion and hand back claims; merge-only done status is unchanged."""
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[3]
ids=['2026-09-14-claude-code-advanced-curriculum',*[f'2026-09-14-claude-advanced-{name}' for name in ['integration','labs','pilots','rules-skills','hooks-mcp','workflows']]]
for identifier in ids:
    path=ROOT/f'tasks/open/{identifier}.md'
    text=path.read_text(encoding='utf-8')
    assert 'owner: codex-claude-advanced' in text
    if identifier.endswith('advanced-curriculum'):
        header=text.split('---',2)[:2]
        text='---'+header[1]+'---\n\n# Claude Code 深入教學第二階段：課程與驗收交付\n\n## Why\n\n使用者在課程規劃後授權開始製作。保留 36 篇任務書，交付完整文章索引、來源與逐篇驗證紀錄，並維護本機預覽與真實環境測試的界線。\n\n## Definition of done\n\n- [x] 36 篇原稿、36 包快照與六組合集均可由目錄取得\n- [x] 編輯清單已轉成 96 篇正式系列資料；97 頁可本機預覽\n- [x] 來源、材料雜湊、瀏覽器與逐篇驗證表已整理\n- [x] 未通過的 Claude／裝置／外部服務操作另列待辦\n\n## How to verify\n\npython tools/claude-code-series/advanced/audit-delivery.py；見 docs/claude-code-series/advanced/evidence/delivery-checks.json。舊 advanced/validation.json 保留規劃階段歷史結果。\n\n## Notes\n'
    else:text=text.replace('- [ ]','- [x]')
    text+='\n2026-09-14 本機交付：36 篇正文、96 篇系列與 97 頁預覽；內容錯誤／警告皆 0，36 ZIP 共 81 項檢查，六篇試作各 21 個工具測試，9 類瀏覽器案例、73 個相關前端測試通過。API 87 通過／77 PostgreSQL 案例跳過；工具全套 51 通過，最終系列重驗 11 通過。build、lint、typecheck、i18n、Ruff 與 mypy 通過。\n\n驗證紀錄：docs/claude-code-series/advanced/evidence/delivery-checks.json；完整目錄：docs/claude-code-series/advanced/README.md。Claude CLI 2.1.233 五次主流程嘗試因 OAuth 到期失敗；真實手機、遠端 OAuth、Teams、外部 CI、排程和 SDK 呼叫未完成，後續見 claude-advanced-live-validation 任務。\n\n本批尚未開 PR／合併、部署、匯入或公開。完成本機成果後 release，保留 open 待審查；不使用代表合併完成的 done。原先第一階段任務封存變更與 .codex/ 均保持原狀。\n'
    path.write_text(text,encoding='utf-8')
    subprocess.run(['node','tools/tasks.mjs','release',identifier],cwd=ROOT,check=True)
