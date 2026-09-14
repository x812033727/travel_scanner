"""Independent source-fidelity check; reports suggestions, never changes files or publishes."""
import asyncio,json
from pathlib import Path
from pydantic import BaseModel,Field
from app.cli import SessionFactory
from app.admin.service import load_runtime_settings
from app.ai.gemini import GeminiStructuredProvider
from app.ai.structured_output import gemini_response_schema
ROOT=Path(__file__).resolve().parent
class Issue(BaseModel):
    pointer:str
    issue:str
    correction:str
class Review(BaseModel):
    issues:list[Issue]=Field(max_length=20)
INSTRUCTIONS='''Check this edited Traditional Chinese article against the supplied verified_facts.
Use ONLY those facts for product/news claims, never your memory or unprovided sources. Editorial
scenarios and advice are original and do not require a source unless presented as observed performance,
guaranteed behavior, actual product mechanics or vendor statements. Flag unsupported product/privacy/
medical/legal/technical guarantees, invented real-world statistics, incorrect reasoning, contradictory
examples and missing access restrictions. Do not flag harmless style or dates stated in different formats.
Don't propose blanket bans on automation; require actions match user authorization and available controls.
No new product facts. Return specific substantive issues only, with exact JSON pointer within document,
and COMPLETE replacement text in Taiwan Traditional Chinese. Do not rewrite nonproblematic fields.
Do not publish anything. Empty issues is appropriate for faithful content.'''
async def main():
    async with SessionFactory() as session:settings=await load_runtime_settings(session)
    provider=GeminiStructuredProvider(settings.hotspot_guide_gemini_api_key,settings.hotspot_guide_gemini_base_url,settings.hotspot_guide_gemini_model,timeout_seconds=240,max_output_tokens=20000)
    (ROOT/'original-reviews').mkdir(exist_ok=True);sem=asyncio.Semaphore(2)
    async def review(file):
        slug=file.stem;target=ROOT/'original-reviews'/file.name
        if target.exists():return
        source=json.loads((ROOT/'research'/file.name).read_text());draft=json.loads(file.read_text())
        async with sem:
            result,usage=await provider.structured(Review,gemini_response_schema(Review),INSTRUCTIONS,{'verified_facts':source['verified_facts'],'document':draft['document']})
        target.write_text(json.dumps({'slug':slug,'usage':usage,'issues':[i.model_dump() for i in result.issues]},ensure_ascii=False,indent=2))
        print('REVIEWED '+slug+' issues='+str(len(result.issues)),flush=True)
    try:await asyncio.gather(*(review(f) for f in sorted((ROOT/'drafts').glob('*.json')) if 'january-september-index' not in f.name))
    finally:await provider.close()
asyncio.run(main())
