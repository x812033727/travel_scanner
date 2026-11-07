import sys,subprocess,pathlib,tempfile,json
sys.path.insert(0,'docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/tools')
import parse_script as P
def lines(path):
    d=P.parse(path); return [(x['speaker'],x['text']) for sc in d['scenes'] for s in sc['shots'] for x in s['dialogue']], [s['id'] for sc in d['scenes'] for s in sc['shots']]
for e in map(int,sys.argv[1:]):
    f=f'docs/videos/tai-nainai-e{e:03d}/script.md'
    old=subprocess.run(['git','show',f'HEAD:{f}'],capture_output=True,text=True).stdout
    tmp=pathlib.Path(tempfile.mkdtemp())/f'tai-nainai-e{e:03d}'/'script.md'; tmp.parent.mkdir(parents=True); tmp.write_text(old,encoding='utf-8')
    lo,io=lines(tmp); ln,inew=lines(pathlib.Path(f))
    kept=[i for i in io if i not in inew]; added=[i for i in inew if i not in io]
    sb=subprocess.run(['python3','-I','docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/storyboard-check.py',f],capture_output=True,text=True).stdout.count('ERROR')
    print(f'e{e:03d} dialogue_same={lo==ln} removed={kept} added={added} sb_errors={sb} first={inew[0]==io[0]}')
