"""Regression check: CRLF/LF checkouts yield identical archives; binary stays intact."""
from pathlib import Path
import hashlib
import importlib.util
import json
import tempfile
import zipfile

source=Path(__file__).with_name('package-labs.py')
spec=importlib.util.spec_from_file_location('package_labs',source)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
root=Path(tempfile.mkdtemp(prefix='mokaair-archive-portability-'))
text='繁體中文\n  const text = "quotes";\n'
binary=b'\x00\xff\r\n\x89'
for name,body in [('linux',text),('windows',text.replace('\n','\r\n'))]:
    module.archive(root/f'{name}.zip',{'article.md':body,'starter/model.js':body.encode(),'fixture.bin':binary})
assert (root/'linux.zip').read_bytes()==(root/'windows.zip').read_bytes()
with zipfile.ZipFile(root/'windows.zip') as archive:
    assert archive.read('fixture.bin')==binary
    assert archive.read('article.md').decode()==text
    assert archive.read('starter/model.js').decode()==text
result={'passed':True,'same_archive_for_lf_and_crlf':True,'binary_bytes_preserved':True,'sha256':hashlib.sha256((root/'linux.zip').read_bytes()).hexdigest(),'scope':'Deterministic archive function on equivalent Windows/Linux text checkouts; real 36 ZIPs are checked separately.'}
out=module.ROOT/'docs/claude-code-series/advanced/evidence/live/archive-portability.json'
out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))
