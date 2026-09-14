"""Hold host locks through scoped publication; clear hold only after public QA receipt."""
import fcntl,json,os,re,subprocess,sys
from pathlib import Path
from release_hold import verify,clear
target=os.environ['NEWS_RELEASE_SHA'];assert re.fullmatch('[0-9a-f]{40}',target)
base=Path('/root/mokaair-release-ai-news-ytd-'+target[:8]);phase=sys.argv[1]
handles=[]
for name in ['/var/lock/travel-scanner-deploy.lock','/root/mokaair-deploy.lock','/run/mokaair-manual-deploy.lock','/run/travel-scanner-deployer/deploy.lock']:
    handle=open(name,'a+');fcntl.flock(handle,fcntl.LOCK_EX|fcntl.LOCK_NB);handles.append(handle)
verify(base,target)
state=json.loads((base/'state.json').read_text());assert state['target']==target and state.get('activated_at')
def run(args):return subprocess.check_output(args,text=True).strip()
for service in ['api','web']:
    container=json.loads(run(['docker','inspect',f'travel_scanner-{service}-1']))[0]
    assert container['Image']==state[service+'_image'] and container['State']['Running']
if phase in ['dry-run','publish']:
    file=base/'source/docs/ai-news-2026-ytd/publish_batch.py'
    subprocess.run(['docker','cp',str(file),'travel_scanner-api-1:/tmp/mokaair-ytd-publish.py'],check=True)
    output=run(['docker','exec','-w','/app','-e','PYTHONPATH=/app','travel_scanner-api-1','python','/tmp/mokaair-ytd-publish.py',phase])
    result=json.loads(output);(base/f'publication-{phase}.json').write_text(json.dumps(result,indent=2))
    print(output)
elif phase=='finish':
    receipt=json.loads((base/'public-qa.json').read_text())
    assert receipt['release_sha']==target and receipt['locale_documents']==110 and receipt['desktop_mobile_pages']==220 and receipt['assets']==220
    assert receipt['all_passed'] is True
    state['publication_qa_completed']=receipt;(base/'state.json').write_text(json.dumps(state,indent=2))
    clear(base,target);print('PUBLICATION_QA_COMPLETE hold cleared for '+target)
else:raise SystemExit('Use dry-run, publish or finish')
