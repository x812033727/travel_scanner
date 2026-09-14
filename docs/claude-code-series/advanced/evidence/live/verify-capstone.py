"""Ask Claude to implement the synthetic capstone in an isolated starter directory."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
import zipfile

ROOT=Path(__file__).resolve().parents[5]
OUT=Path(__file__).resolve().parent
archive=ROOT/'apps/web/public/tutorials/claude-code/advanced/lesson-96.zip'
directory=Path(tempfile.mkdtemp(prefix='mokaair-capstone-live-')).resolve()
with zipfile.ZipFile(archive) as package:
    for member in package.infolist():
        if not member.filename.startswith('starter/') or member.is_dir():continue
        target=(directory/Path(member.filename).relative_to('starter')).resolve()
        assert target.is_relative_to(directory)
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(package.read(member))
def git(*args):return subprocess.run(['git',*args],cwd=directory,capture_output=True,text=True,encoding='utf-8',check=True)
git('init','--quiet');git('config','user.name','Mokaair Tutorial Lab');git('config','user.email','tutorial-lab@example.invalid');git('add','.');git('commit','--quiet','-m','Synthetic starter baseline');git('switch','-c','codex/capstone-verification')
baseline=subprocess.run([shutil.which('node'),'--test','tests/model.test.mjs'],cwd=directory,capture_output=True,text=True,encoding='utf-8',timeout=20)
assert baseline.returncode==0
acceptance='''# 合成待辦篩選驗收
- filter.js 匯出 filterTodos(items, mode)，支援 all、active、completed；未知 mode 回傳全部。
- 保留完整來源資料，以 id 操作；篩選不原地修改輸入。同名待辦分別切換。
- 在 index.html 加入有名稱的「全部」「未完成」「已完成」按鈕；選取狀態清楚。
- app.js 渲染時才篩選；保留原有 #todo-title、#todo-form、#todo-list、#message。
- 加入課程 localStorage 保存，key 為 mokaair-capstone-96；刷新後保留項目。
- 儲存損壞時回復可操作的空清單；文字以 textContent 顯示，不當作 HTML。
- 保留新增、切換、刪除、空白／過長輸入驗證，360–390px 不應整頁水平溢出。
- 新增 tests/filter.test.mjs 驗證資料，維持原有模型測試不變。
- 完成後 handoff.md 說明檔案、測試、localStorage key、停止方式與未測項目。
- 不裝套件、不連外部服務、不部署、不提交或推送；只修改本臨時專案。
'''
(directory/'acceptance.md').write_text(acceptance,encoding='utf-8')
prompt='''閱讀 acceptance.md 與目前程式，直接完成這個合成待辦網站的篩選、畫面及保存需求。先做資料與測試再接 UI。既有 tests/model.test.mjs 不得改寫。可執行 node --test tests/model.test.mjs tests/filter.test.mjs。不要讀取 reference 或任何其他資料夾；沒有 reference 可用。不可啟動常駐伺服器、安裝依賴、建立其他代理、執行 Git、使用外部服務。只用 Read、Write、Edit、Glob、Grep 與允許的 node --test。最後寫 handoff.md，清楚說明瀏覽器尚未實測。'''
command=[shutil.which('claude'),'-p','--model','sonnet','--output-format','stream-json','--verbose','--include-hook-events','--max-budget-usd','2.00','--max-turns','30','--no-session-persistence','--setting-sources','project','--strict-mcp-config','--mcp-config','{"mcpServers":{}}','--tools','Read,Write,Edit,Glob,Grep,Bash','--allowedTools','Read,Write,Edit,Glob,Grep,Bash(node --test *)','--disallowedTools','Agent','--permission-mode','dontAsk']
report={'started_at':datetime.now(timezone.utc).isoformat(),'directory':str(directory),'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'cli_version':subprocess.check_output(['claude','--version'],text=True).strip(),'model_override':'sonnet','prompt':prompt,'acceptance':acceptance,'baseline':{'exit':baseline.returncode,'output':baseline.stdout},'passed':False,'scope':'Actual Claude-authored local feature; browser and specified fault recovery recorded separately'}
(OUT/'capstone-implementation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
begin=time.monotonic()
try:
    run=subprocess.run(command,cwd=directory,input=prompt,env=os.environ.copy(),capture_output=True,text=True,encoding='utf-8',timeout=300)
    events=[json.loads(line) for line in run.stdout.splitlines() if line.startswith('{')]
    (OUT/'capstone-implementation-events.json').write_text(json.dumps(events,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    result=next((e for e in reversed(events) if e.get('type')=='result'),{})
    required=['filter.js','tests/filter.test.mjs','handoff.md']
    changes=git('status','--porcelain').stdout
    diff=git('diff','--','app.js','index.html','style.css','model.js','tests/model.test.mjs').stdout
    files={name:(directory/name).read_text(encoding='utf-8') for name in ['filter.js','tests/filter.test.mjs','handoff.md','app.js','index.html','style.css'] if (directory/name).exists()}
    report.update({'exit':run.returncode,'seconds':round(time.monotonic()-begin,2),'result':result,'stderr':run.stderr[-2000:],'changes':changes,'diff':diff,'files':files,'source_model_tests_unchanged':not git('diff','--','tests/model.test.mjs').stdout,'passed':run.returncode==0 and not result.get('is_error',True) and all((directory/name).exists() for name in required)})
except subprocess.TimeoutExpired as error:
    partial=error.stdout or b''
    if isinstance(partial,bytes):partial=partial.decode('utf-8',errors='replace')
    (OUT/'capstone-timeout.txt').write_text(partial,encoding='utf-8')
    report.update({'passed':False,'error':'300 second timeout','seconds':round(time.monotonic()-begin,2)})
(OUT/'capstone-implementation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'passed':report['passed'],'directory':str(directory),'seconds':report.get('seconds'),'result':report.get('result',{}).get('subtype')}))
raise SystemExit(0 if report['passed'] else 1)
