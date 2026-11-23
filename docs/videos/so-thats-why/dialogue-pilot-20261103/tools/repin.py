# Re-pin shots the owner's storyboard depends on whose verdicts a keyframes run cannot keep (see the eye-check task notes).
import json,hashlib,sys
pins=json.load(open(sys.argv[1]))
for slug,ps in pins.items():
    W=f'/root/mokaair-work/videos/{slug}/'; M=json.load(open(W+'keyframes/manifest.json')); s=M['shots']
    for i,f in ps.items():
        f='keyframes/'+f; e=s.get(i,{})
        e.update(file=f, sha256=hashlib.sha256(open(W+f,'rb').read()).hexdigest(), needs_review=False,
                 accepted_with_problems=["pinned 2026-11-06 to the take checked by eye (eyes and identity); a keyframes run cannot keep its verdict"])
        s[i]=e
    json.dump(M,open(W+'keyframes/manifest.json','w'),ensure_ascii=False,indent=2)
print('repinned')
