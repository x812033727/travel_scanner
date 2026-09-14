"""One-time, scoped updates for the advanced tutorial release."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

def replace(relative, pairs):
    path = ROOT / relative
    text = path.read_text(encoding='utf-8')
    for old, new in pairs:
        text = text.replace(old, new)
    path.write_text(text, encoding='utf-8')

replace('tools/claude-code-series.test.mjs', [
    ('catalogue.entries.length, 60', 'catalogue.entries.length, 96'),
    ('expected.size, 61', 'expected.size, 97'),
    ('catalogue.groups.length, 10', 'catalogue.groups.length, 16'),
    ('catalogue.paths.length, 5', 'catalogue.paths.length, 12'),
    ('length: 60', 'length: 96'), ('all 61 native packs', 'all 97 native packs'),
])
replace('apps/api/tests/test_guide_series.py', [
    ('len(catalogue.entries) == 60', 'len(catalogue.entries) == 96'),
    ('len(catalogue.groups) == 10', 'len(catalogue.groups) == 16'),
    ('len(catalogue.paths) == 5', 'len(catalogue.paths) == 12'),
])
replace('apps/web/e2e/claude-code-series.spec.ts', [
    ('const evidence = fileURLToPath', 'const evidence = process.env.CLAUDE_SERIES_EVIDENCE ?? fileURLToPath'),
    ('all 60 published links', 'all catalogue links'),
    ('toHaveCount(60)', 'toHaveCount(catalogue.entries.length)'),
    ('all 61 pages render', 'all catalogue pages render'),
    ('test.setTimeout(180000)', 'test.setTimeout(300000)'),
    ('index < 59', 'index < catalogue.entries.length - 1'),
    ('["claude-md-guide", "hooks-getting-started", "templates-cheatsheet"]', '["claude-md-guide", "hooks-getting-started", "templates-cheatsheet", "project-rules-workshop", "hook-event-test-lab", "structured-cli-pipeline"]'),
])
replace('tools/claude-code-series/preview.mjs', [
    ('startSeriesPreview, hubPath }', 'startSeriesPreview, hubPath, packs }'),
    ('(61 draft packs,', '(${packs.size} draft packs,'),
])
replace('docs/claude-code-series/lessons/00.md', [('60 篇', '96 篇')])
for number, slug, label in [(20,'project-rules-workshop','專案規則工作坊'),(38,'skill-sop-workshop','Skill SOP 工作坊'),(41,'hook-event-test-lab','Hook 事件實驗'),(43,'mcp-local-server-workshop','自建唯讀 MCP'),(47,'worktree-integration-workshop','Worktree 衝突整合'),(51,'structured-cli-pipeline','JSON 自動化流程')]:
    path=ROOT/f'docs/claude-code-series/lessons/{number:02}.md'
    text=path.read_text(encoding='utf-8')
    link=f'article:claude-code-{slug}'
    if link not in text:
        path.write_text(text.rstrip()+f'\n\n準備好練習完整流程時，接著閱讀[{label}]({link})，使用獨立材料進行故障重現與成果驗證。\n',encoding='utf-8')

notes={
 'integration':('將第二階段 36 篇接入同一目錄、導覽、搜尋與可下載材料，保留第一階段驗證紀錄。',['96 篇清單、16 分組、12 路線已整合','產生全部內容包及封面，更新原始入口與六篇先備文章','驗證連結、API 發布邊界、手機版與程式碼複製'],'npm run test:tools; uv run python tools/claude-code-series/validate.py --output docs/claude-code-series/advanced/evidence/content-validation.json; 使用 advanced/playwright.config.mjs'),
 'labs':('為六組深入教學提供可獨立開始、具故障材料與參考結果的下載包。',['共用 Node 材料、實際 MCP stdio 及 Worktree 實驗已建立','36 篇快照與 6 組材料包完整、無 node_modules 或登入資料','從實際 ZIP 解壓縮執行成功與故障案例'],'node --test tools/claude-code-series/advanced/lab/tests/*.test.mjs; python tools/claude-code-series/advanced/package-labs.py'),
 'pilots':('以 61、67、73、79、88、91 六篇驗證深入教材格式與可執行範例。',['六篇完整正文已撰寫','核對字數、來源、程式碼與下載材料','在可用環境記錄真實操作，將登入受阻項目獨立標記'],'產生六篇內容包、執行內容與材料測試；實機紀錄在 advanced/evidence/claude-live-all.json'),
 'rules-skills':('完成 62–66、68–72 的規則與 Skills 深入實作。',['完成十篇正文與獨立材料','核對參數、規則來源、升級及還原案例','驗證內容包、站內引用、圖片和下載'],'內容驗證器、JSON/JavaScript 範例測試及 ZIP 測試'),
 'hooks-mcp':('完成 74–78、80–84 的 Hook 與 MCP 深入實作。',['完成十篇正文與故障案例','核對真實 SDK 協定、退出碼、授權與工具邊界','驗證內容包、站內引用、圖片和下載'],'本機 Hook 重播與 MCP client/server 協定測試；真實 OAuth 和外部操作另記狀態'),
 'workflows':('完成 85–87、89–90、92–96 的開發與自動化教學。',['完成十篇正文與可操作流程','提供工作流、取消、恢復、成本評估及總實作材料','驗證本機案例並明列外部裝置、CI 和帳號的待測範圍'],'本機模型、流程、Worktree 測試及整套預覽；不等同正式部署或公開'),
}
for suffix,(why,steps,verify) in notes.items():
    path=ROOT/f'tasks/open/2026-09-14-claude-advanced-{suffix}.md'
    content=path.read_text(encoding='utf-8')
    if 'Describe the problem' not in content: continue
    head=content.split('\n## Why',1)[0]
    body='\n## Why\n\n'+why+'\n\n## Definition of done\n\n'+ '\n'.join('- [ ] '+s for s in steps)+'\n\n## How to verify\n\n'+verify+'\n\n## Notes\n\n2026-09-14：使用者已授權開始第二階段實作。只進行本機教材與預覽，不匯入正式資料庫或發布。Claude CLI 2.1.233 的實際驗證遇到 OAuth 過期；已請使用者重新登入，持續完成獨立材料。\n'
    path.write_text(head+body,encoding='utf-8')
