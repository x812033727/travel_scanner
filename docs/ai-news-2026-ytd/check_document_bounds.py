"""List schema violations in this batch without stopping at the first document."""
import json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];sys.path.insert(0,str(ROOT/'apps/api'))
from app.guides.content_pack import ArticlePack
from pydantic import ValidationError
errors=[]
for slug in json.loads((HERE/'slugs.json').read_text(encoding='utf8')):
    pack=json.loads((ROOT/'apps/api/app/guides/content'/f'{slug}.json').read_text(encoding='utf8'))
    try:ArticlePack.model_validate(pack)
    except ValidationError as e:errors.append({'slug':slug,'errors':e.errors(include_url=False)})
print(json.dumps(errors,ensure_ascii=False,default=str,indent=2))
