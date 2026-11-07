import json,re,sys,pathlib,subprocess
sys.path.insert(0,'docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/tools')
import parse_script as P
cast=json.load(open('docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/cast.json'))
ids={c['id'] for c in cast['characters']}|{e['id'] for e in cast['extras']}
looks={(c['id'],s['id']) for c in cast['characters'] for s in c.get('shot_looks',[])}
sets={s['id'] for s in cast['sets']}
T='docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/tools'
for e in map(int,sys.argv[1:]):
    prob=[]; d=json.load(open(f'docs/videos/tai-nainai-e{e:03d}/shots-en.json',encoding='utf-8'))
    rows={s['id']:s for sc in P.parse(pathlib.Path(f'docs/videos/tai-nainai-e{e:03d}/script.md'))['scenes'] for s in sc['shots']}
    for k,v in d['shots'].items():
        p=v['prompt']
        if re.search(r'[一-鿿]',p): prob.append((k,'CJK'))
        if 'film still' in p.lower(): prob.append((k,'film still'))
        if len(p)>1000: prob.append((k,'long'))
        if not rows[k]['dialogue'] and not v.get('motion'): prob.append((k,'no motion'))
        prob+=[(k,'bad id',c) for c in v.get('characters',[])+v.get('ref_characters',[]) if c not in ids]
        prob+=[(k,'bad look',c,l) for c,l in (v.get('looks') or {}).items() if (c,l) not in looks]
        if v.get('set') and v['set'] not in sets: prob.append((k,'bad set',v['set']))
    chk=subprocess.run(['python3','-I',f'{T}/compile.py',str(e),'--check'],capture_output=True,text=True).returncode
    subprocess.run(['python3','-I',f'{T}/compile.py',str(e)],capture_output=True)
    lint=subprocess.run(['node','tools/video/cli.mjs','lint','--slug',f'tai-nainai-e{e:03d}'],capture_output=True,text=True).stdout.splitlines()[0]
    op='hook.opening:' in ' '.join(subprocess.run(['node','tools/video/cli.mjs','lint','--slug',f'tai-nainai-e{e:03d}'],capture_output=True,text=True).stdout.split('craft hook.opening30'))
    print(f'e{e:03d} shots={len(d["shots"])} check={"ok" if chk==0 else "DRIFT"} {lint} opening<4={op} problems={prob[:5]}')
