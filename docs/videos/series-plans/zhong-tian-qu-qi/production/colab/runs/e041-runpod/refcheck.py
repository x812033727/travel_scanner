"""Per shot: which pictures the manifest sends, against the people the storyboard puts on screen."""
import glob, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
A = os.path.dirname(os.path.abspath(__file__))
NAMES = {"許硯": "xuyan", "阿令": "aling", "秦霜": "qinshuang", "唐小棠": "tangxiaotang", "刁七": "diaoqi", "錢員外": "qianyuanwai", "王二牛": "wangerniu", "韓伯": "hanbo"}
rows = {}
for line in open(sys.argv[1], encoding="utf8"):
    m = re.match(r"\| (s\d\d) \|(.*)", line)
    if m:
        rows[m.group(1)] = m.group(2).split("|")[4].strip()
for path in sorted(glob.glob(f"{A}/st1/ref-e041-part*.json")):
    for job in json.load(open(path, encoding="utf8"))["jobs"]:
        pics = [os.path.basename(x.replace("\\", "/")).replace(".png", "") for x in job["reference_images"]]
        have = {n for n in NAMES.values() if any(n in q for q in pics)}
        scene = rows[job["id"]].split("；")[0]
        seen = [v for k, v in NAMES.items() if k in scene and not re.search(k + r"[^，。；]{0,4}(畫外)", scene)]
        miss = [x for x in seen if x not in have]
        print(job["id"], len(pics), sorted(have), ("MISS " + ",".join(miss)) if miss else "ok")
