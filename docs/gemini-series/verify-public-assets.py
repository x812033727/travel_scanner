from pathlib import Path
import hashlib,json,urllib.request,concurrent.futures
from datetime import datetime,timezone
root=Path.cwd();out=Path(__file__).parent
m=json.loads((root/'docs/gemini-series/reviewed-files.json').read_text(encoding='utf-8'))
assets=[(name,row) for name,row in m['files'].items() if name.startswith('apps/web/public/') and not name.endswith('/hero.svg')]
def verify(item):
 name,row=item;url='https://mokaair.com/'+name.removeprefix('apps/web/public/')
 with urllib.request.urlopen(url,timeout=30) as r:
  data=r.read();digest=hashlib.sha256(data).hexdigest()
  assert digest==row['sha256'],f'Published asset differs: {url}'
  return {'url':url,'status':r.status,'sha256':digest,'bytes':len(data)}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(verify,assets))
assert len(results)==102
(out/'public-assets.json').write_text(json.dumps({'checkedAt':datetime.now(timezone.utc).isoformat(),'status':'passed','assets':results},indent=2),encoding='utf-8')
print('All 102 public images match the reviewed bytes, without cache-busting URLs.')
