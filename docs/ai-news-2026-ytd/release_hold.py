"""Own a host deployment hold across build, activation, publication and public QA.

Callers must hold the four existing host deployment locks. Never displace another
release. This task-local helper follows the shared host hold-file contract.
"""
import datetime,json,os
from pathlib import Path
HOLD=Path('/root/travel-scanner-deploy.hold')
def verify(release_dir,target,path=HOLD):
    lines=path.read_text(encoding='utf8').splitlines()
    data=json.loads(lines[1])
    assert data['target']==target and data['release_dir']==str(release_dir),'another release owns deployment hold'
    return data
def acquire(release_dir,target,path=HOLD):
    data={'target':target,'release_dir':str(release_dir),'owner':'codex-ai-news-ytd','phases':['prepare','activate','dry-run','publish','public-qa'],'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    first=f"codex-ai-news-ytd publishing {target[:12]} ({release_dir}); preserve until publication and public QA finish. Inspect release state before manual removal."
    assert len(first.encode())<=600
    try:fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o644)
    except FileExistsError:return verify(release_dir,target,path)
    with os.fdopen(fd,'w',encoding='utf8') as f:f.write(first+'\n'+json.dumps(data)+'\n')
    os.chmod(path,0o644)
    return verify(release_dir,target,path)
def clear(release_dir,target,path=HOLD):
    verify(release_dir,target,path);path.unlink()
