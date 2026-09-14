"""Disposable native PostgreSQL 17 integration checks; no installed service or existing DB."""
import hashlib
import json
import os
from pathlib import Path
import secrets
import shutil
import socket
import subprocess
import sys
import re
import tempfile
import time
import urllib.request
import zipfile
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[5]
EVIDENCE=Path(__file__).resolve().parent
SOURCE='https://sbp.enterprisedb.com/getfile.jsp?fileid=1260491'
EXPECTED_URL='https://get.enterprisedb.com/postgresql/postgresql-17.11-3-windows-x64-binaries.zip'
resuming=len(sys.argv)>1
runtime=Path(sys.argv[1]).resolve() if resuming else Path(tempfile.mkdtemp(prefix='mokaair-postgres-')).resolve()
assert runtime.is_relative_to(Path(tempfile.gettempdir()).resolve()) and runtime.name.startswith('mokaair-postgres-')
archive=runtime/'postgres.zip'
receipt={'started_at':datetime.now(timezone.utc).isoformat(),'source':SOURCE,'scope':'disposable PostgreSQL, loopback only; guide and series integration tests','production_access':False,'steps':[]}
started=resuming
binary=runtime/'pgsql/bin';data=runtime/'data';pwfile=runtime/'test-password'
flags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0

def run(args,*,env=None,cwd=ROOT,timeout=60,log=None):
    # pg_ctl's Windows descendants may inherit pipe handles; use a file so
    # communicate() cannot wait indefinitely after pg_ctl itself has exited.
    with tempfile.TemporaryFile() as capture:
        result=subprocess.run([str(x) for x in args],cwd=cwd,env=env,stdout=capture,stderr=subprocess.STDOUT,timeout=timeout,creationflags=flags)
        capture.seek(0);output=capture.read().decode('utf-8',errors='replace')
    if log:(EVIDENCE/log).write_text(output,encoding='utf-8')
    receipt['steps'].append({'command':[str(x).replace(str(runtime),'<temporary-runtime>') for x in args],'exit':result.returncode,'log':log})
    if result.returncode:raise RuntimeError(f'{Path(args[0]).name} exited {result.returncode}: {output[-2500:]}')
    return output

try:
    if resuming:
        receipt['recovery']='Initial Windows pg_ctl capture pipe stayed open after successful server startup; resumed the same disposable cluster with file-based process output.'
        receipt['download']={'url':EXPECTED_URL,'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()}
    else:
      with urllib.request.urlopen(SOURCE,timeout=60) as response:
        assert response.url==EXPECTED_URL,response.url
        digest=hashlib.sha256();total=0;last=0
        with archive.open('wb') as target:
            while block:=response.read(1024*1024):
                target.write(block);digest.update(block);total+=len(block)
                if total-last>=32*1024*1024:print(f'Downloaded {total//1024//1024} MiB',flush=True);last=total
        receipt['download']={'url':response.url,'bytes':total,'sha256':digest.hexdigest()}
    if not resuming:
      with zipfile.ZipFile(archive) as package:
        for member in package.infolist():
            if not member.filename.startswith(('pgsql/bin/','pgsql/lib/','pgsql/share/')):continue
            target=(runtime/member.filename).resolve()
            assert target.is_relative_to(runtime)
            package.extract(member,runtime)
    password=pwfile.read_text(encoding='utf-8') if resuming else secrets.token_urlsafe(32)
    if not resuming:pwfile.write_text(password,encoding='utf-8')
    receipt['version']=run([binary/'postgres.exe','--version']).strip()
    if resuming:
        port=int(re.search(r'"-p" "(\d+)"', (data/'postmaster.opts').read_text(encoding='utf-8')).group(1))
        run([binary/'pg_ctl.exe','-D',data,'status'],log='postgres-start.log')
    else:
        run([binary/'initdb.exe','-D',data,'-U','tutorial_test','--pwfile',pwfile,'--auth=scram-sha-256','--encoding=UTF8','--locale=C'],log='postgres-init.log')
        with socket.socket() as probe:probe.bind(('127.0.0.1',0));port=probe.getsockname()[1]
    receipt['port']=port
    if not resuming:run([binary/'pg_ctl.exe','-D',data,'-l',runtime/'server.log','-o',f'-h 127.0.0.1 -p {port}','-w','start'],timeout=60,log='postgres-start.log')
    started=True
    env={**os.environ,'PGPASSWORD':password,'PGHOST':'127.0.0.1','PGPORT':str(port),'PGUSER':'tutorial_test'}
    run([binary/'createdb.exe','claude_tutorial_tests'],env=env)
    env.update({'DATABASE_URL':f'postgresql+asyncpg://tutorial_test:{password}@127.0.0.1:{port}/claude_tutorial_tests','RUN_INTEGRATION_TESTS':'1'})
    begun=time.monotonic()
    run([shutil.which('uv'),'run','pytest','tests/test_guide_series.py','tests/test_guides.py','-q','-r','fE','--junitxml',EVIDENCE/'postgres-tests.xml'],env=env,cwd=ROOT/'apps/api',timeout=600,log='postgres-tests.log')
    receipt['test_seconds']=round(time.monotonic()-begun,2)
    remaining=run([binary/'psql.exe','-d','claude_tutorial_tests','-Atc',"SELECT count(*) FROM pg_namespace WHERE nspname LIKE 'guides_test_%';"],env=env).strip()
    assert remaining=='0',remaining
    receipt['remaining_test_schemas']=0
    receipt['passed']=True
except Exception as error:
    receipt['passed']=False;receipt['error']=str(error)
finally:
    if started:
        try:
            run([binary/'pg_ctl.exe','-D',data,'-m','fast','-w','stop'],timeout=45,log='postgres-stop.log')
            receipt['stopped']=True
        except Exception as error:receipt['stopped']=False;receipt['stop_error']=str(error)
    if 'pwfile' in globals() and pwfile.exists():pwfile.unlink()
    receipt['finished_at']=datetime.now(timezone.utc).isoformat()
    (EVIDENCE/'postgres-validation.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'passed':receipt['passed'],'stopped':receipt.get('stopped'),'evidence':str(EVIDENCE/'postgres-validation.json')}),flush=True)
    # Keep only failed runtimes for diagnosis; never recursively remove an unverified path.
    if receipt.get('passed') and receipt.get('stopped'):
        assert runtime.is_relative_to(Path(tempfile.gettempdir()).resolve()) and runtime.name.startswith('mokaair-postgres-')
        for attempt in range(3):
            try:
                shutil.rmtree(runtime);receipt['temporary_runtime_removed']=True
                break
            except PermissionError as error:
                receipt['temporary_runtime_removed']=False
                receipt['cleanup_note']=str(error)
                time.sleep(1)
        (EVIDENCE/'postgres-validation.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0 if receipt.get('passed') and receipt.get('stopped') else 1)
