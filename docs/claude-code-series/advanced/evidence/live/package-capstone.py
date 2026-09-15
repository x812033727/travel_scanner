"""Package and verify the actual model-authored result from a fresh directory."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

OUT=Path(__file__).resolve().parent
original=json.loads((OUT/'capstone-implementation.json').read_text(encoding='utf-8'))
repair=json.loads((OUT/'capstone-repair.json').read_text(encoding='utf-8'))
browser=json.loads((OUT/'capstone-browser.json').read_text(encoding='utf-8'))
assert original['passed'] and original['source_model_tests_unchanged'] and repair['passed'] and browser['passed']
directory=Path(original['directory'])
assert directory.name.startswith('mokaair-capstone-live-')
names=['app.js','index.html','style.css','model.js','filter.js','server.mjs','tests/model.test.mjs','tests/filter.test.mjs','acceptance.md','.claude/CLAUDE.md']
handoff=(directory/'handoff.md').read_text(encoding='utf-8')
correction='`loadItems()` 對非陣列、JSON 損壞、或項目欄位型別不符時，一律回復為空陣列（`[]`），確保畫面仍可操作。'
assert correction in handoff
handoff=handoff.replace(correction,'`loadItems()` 遇到非陣列或 JSON 損壞時回復空陣列；合法陣列中只移除欄位型別不符的項目，保留其餘合法項目。（Codex 依實作更正原交接文字。）')
handoff+='\n## 獨立驗收補充\n\n後續由 Codex 在內建瀏覽器驗證三種篩選、同名項目、刷新保存、360／390px、空白輸入與損壞 JSON 恢復。指定比較符號反轉已在 UI 重現，Claude 修正後相同獨立斷言轉綠。這些是本機與瀏覽器尺寸模擬，不是真實手機。原先 Claude 未經瀏覽器驗證的報告仍保存於 capstone-implementation.json。\n\n啟動：node server.mjs；停止：在該終端機按 Ctrl+C。使用專案規則與核心測試，不需要額外 Skill、Hook、MCP 或 SDK 來完成本次本機功能。未部署或推送遠端。\n'
readme='''# Claude 實際產生的第 96 篇本機成果

此包來自 lesson-96 starter。Claude Code 2.1.233（Sonnet）完成篩選、UI、保存與測試；指定故障由另一個 Haiku 工作階段修正。Codex 另作独立測試、瀏覽器驗收、乾淨解壓縮重驗，並更正 handoff 一句資料過濾說明。這不是替換教材 reference 的另一份手工完成版。

需要 Node.js 22 以上，不需要安裝依賴或資料庫：

```powershell
node --test tests/model.test.mjs tests/filter.test.mjs
$env:CAPSTONE_DIRECTORY=(Get-Location).Path
node --test verification/capstone-acceptance.test.mjs
node server.mjs
```

開啟輸出的 localhost 網址。按 Ctrl+C 停止該伺服器。課程 localStorage key 為 mokaair-capstone-96。沒有帳號、遠端同步、部署或私人資料。

原始模型操作與失敗／修正紀錄保存於教學儲存庫 advanced/evidence/live。手機寬度模擬已測，實體手機與跨裝置接續仍未驗證。
'''.replace('独立','獨立')
target=OUT/'capstone-result.zip'
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as pack:
    for name in names:pack.writestr(name,(directory/name).read_bytes())
    pack.writestr('handoff.md',handoff)
    pack.writestr('README.md',readme)
    pack.writestr('package.json',json.dumps({'name':'mokaair-capstone-verified-result','private':True,'type':'module','scripts':{'test':'node --test tests/model.test.mjs tests/filter.test.mjs','start':'node server.mjs'}},indent=2)+'\n')
    pack.writestr('verification/capstone-acceptance.test.mjs',(OUT/'capstone-acceptance.test.mjs').read_bytes())
clean=Path(tempfile.mkdtemp(prefix='mokaair-capstone-clean-')).resolve()
with zipfile.ZipFile(target) as pack:
    assert pack.testzip() is None
    for name in pack.namelist():assert (clean/name).resolve().is_relative_to(clean)
    pack.extractall(clean)
results=[]
for args in [['tests/model.test.mjs','tests/filter.test.mjs'],['verification/capstone-acceptance.test.mjs']]:
    run=subprocess.run([shutil.which('node'),'--test',*args],cwd=clean,env={**os.environ,'CAPSTONE_DIRECTORY':str(clean)},capture_output=True,text=True,encoding='utf-8',timeout=20)
    results.append({'command':'node --test '+' '.join(args),'exit':run.returncode,'output':run.stdout})
report={'checked_at':datetime.now(timezone.utc).isoformat(),'archive':target.name,'archive_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'files':names+['handoff.md','README.md','package.json','verification/capstone-acceptance.test.mjs'],'fresh_directory':str(clean),'checks':results,'verifier_corrections':['Handoff: mixed arrays retain valid items; malformed JSON/non-array returns empty. Added actual browser evidence and explicit server stop instructions.'],'passed':all(r['exit']==0 for r in results),'physical_mobile':False,'deployed':False}
(OUT/'capstone-clean-replay.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'passed':report['passed'],'sha256':report['archive_sha256'],'files':len(report['files'])}))
raise SystemExit(0 if report['passed'] else 1)
