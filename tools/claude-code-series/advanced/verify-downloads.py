"""Run actual archive contents in new temporary directories and save honest receipts."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

ROOT=Path(__file__).resolve().parents[3]
DOWNLOADS=ROOT/'apps/web/public/tutorials/claude-code/advanced'
EVIDENCE=ROOT/'docs/claude-code-series/advanced/evidence'

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--quick',action='store_true');parser.add_argument('--only',nargs='*',type=int);args=parser.parse_args()
    root=Path(tempfile.mkdtemp(prefix='mokaair-downloads-')).resolve()
    rows=[]
    node=shutil.which('node');npm=shutil.which('npm.cmd' if os.name=='nt' else 'npm')
    env={k:v for k,v in os.environ.items() if k!='NODE_TEST_CONTEXT'}
    try:
        for archive in sorted(DOWNLOADS.glob('lesson-*.zip')):
            number=int(archive.stem.split('-')[-1])
            if args.only and number not in args.only:continue
            destination=root/f'lesson-{number}'
            with zipfile.ZipFile(archive) as source:
                names=source.namelist()
                assert all((destination/name).resolve().is_relative_to(root) for name in names)
                assert all('node_modules' not in name and '/run-data/' not in name for name in names)
                assert all(name in names for name in ['article.md','README.md','expected-results.md','reset.md','starter/package-lock.json','reference/package-lock.json'])
                source.extractall(destination)
            row={'number':number,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'checks':[]}
            for variant in ['starter','reference']:
                project=destination/variant
                result=subprocess.run([node,'--test','tests/model.test.mjs'],cwd=project,env=env,capture_output=True,text=True,encoding='utf-8',timeout=20)
                expected=1 if number==85 and variant=='starter' else 0
                assert result.returncode==expected,(number,variant,result.stdout,result.stderr)
                row['checks'].append({'variant':variant,'command':'node --test tests/model.test.mjs','exit':result.returncode,'expected_exit':expected,'output':result.stdout+result.stderr})
                for test_file in ['tests/filter.test.mjs','tests/stats.test.mjs']:
                    if not (project/test_file).exists():continue
                    result=subprocess.run([node,'--test',test_file],cwd=project,env=env,capture_output=True,text=True,encoding='utf-8',timeout=20)
                    assert result.returncode==0,(number,result.stdout,result.stderr)
                    row['checks'].append({'variant':variant,'command':'node --test '+test_file,'exit':0,'output':result.stdout})
            if not args.quick and number in {61,67,73,79,88,91}:
                project=destination/'starter'
                installed=subprocess.run([npm,'ci','--ignore-scripts','--no-audit','--no-fund'],cwd=project,env=env,capture_output=True,text=True,encoding='utf-8',timeout=120)
                assert installed.returncode==0,installed.stderr
                result=subprocess.run([node,'--test','tests/*.test.mjs'],cwd=project,env=env,capture_output=True,text=True,encoding='utf-8',timeout=40)
                assert result.returncode==0,(number,result.stdout,result.stderr)
                row['checks'].append({'variant':'starter','command':'npm ci --ignore-scripts; node --test tests/*.test.mjs','exit':0,'output':result.stdout+result.stderr})
            rows.append(row)
            print(json.dumps({'number':number,'passed':True,'checks':len(row['checks'])}),flush=True)
        EVIDENCE.mkdir(exist_ok=True,parents=True)
        target=EVIDENCE/('downloads-quick-tests.json' if args.quick else 'downloads-tests.json')
        target.write_text(json.dumps({'passed':True,'archives':rows,'platform':os.name,'real_claude_operations':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    finally:
        temp=Path(tempfile.gettempdir()).resolve()
        assert root.is_relative_to(temp) and root.name.startswith('mokaair-downloads-')
        shutil.rmtree(root)

if __name__=='__main__':main()
