import json,sys,wave,re,statistics
slug=sys.argv[1]; ids=sys.argv[2:]
W=f"/root/mokaair-work/videos/{slug}"
v=json.load(open(f"/home/user/wt-prod/docs/videos/{slug}/video.json"))
txt={l["id"]:l["text"] for s in v["scenes"] for l in s["lines"]}
def units(t): return len(re.sub(r"[\s，。、：；？！「」『』《》（）,.!?:;\-—…·]","",t))
def dur(i):
  w=wave.open(f"{W}/audio/{i}.wav"); return w.getnframes()/w.getframerate()
rates={i:units(t)/dur(i) for i,t in txt.items()}
m=statistics.median(rates.values()); print(f"median {m:.2f} u/s")
for i in ids: print(i, f"{dur(i):.2f}s", f"{rates[i]:.2f} u/s", f"{rates[i]/m*100:.0f}%", txt[i])
