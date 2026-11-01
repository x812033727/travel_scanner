"""e042's four missing pictures, Qwen-Image-Edit on RunPod, two seeds each. Appearance copied from production/cast.json."""
import json, os, sys
repo = sys.argv[1]
A = os.path.dirname(os.path.abspath(__file__))
R = f"{repo}/docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-dh"
cast = json.load(open(f"{repo}/docs/videos/series-plans/zhong-tian-qu-qi/production/cast.json", encoding="utf8"))
def look(cid):
    def walk(node):
        if isinstance(node, dict):
            if node.get("id") == cid and "appearance" in node:
                return node["appearance"]
            for value in node.values():
                found = walk(value)
                if found:
                    return found
        elif isinstance(node, list):
            for value in node:
                found = walk(value)
                if found:
                    return found
    return walk(cast)
STYLE = "3D Chinese donghua CG, Unreal Engine 5 cinematic render, stylized semi-realistic, detailed clearly CG skin, individually rendered hair strands, physically simulated cloth with wear, volumetric light"
def portrait(cid, ref):
    return ref, 1024, 1360, (f"Paint a new character portrait in exactly the same rendering style, lighting and framing as image 1, a different person from image 1. "
                             f"He is: {look(cid)}. Upper body, facing the camera, a calm expression, against a dark smoky blue-grey backdrop. {STYLE}.")
def place(ref, text):
    return ref, 1312, 736, f"Paint a new location in exactly the same rendering style and light quality as image 1, a different place from image 1. {text} Everything stands quiet and still in the early hour before anyone has arrived. {STYLE}."
ITEMS = {
 "xudalang-portrait-t1": portrait("xudalang", "xuyan-portrait-t1.png"),
 "zhouyuanwai-portrait-t1": portrait("zhouyuanwai", "sunzhanggui-portrait-t1.png"),
 "set-zhou-kezhan-t1": place("set-chalou-t1.png", "The front hall of a busy prefectural inn in warm daylight: a long dark wooden counter on the right with an abacus, a thick ledger and a row of wine jars, square tables and benches across the floor, red paper lanterns hanging from the beams, a wooden staircase up to the guest rooms on the left."),
 "set-gongyuan-t1": place("set-xianya-t1.png", "The registration desk outside a prefectural examination hall in grey morning light: a long table draped in dark cloth with stacked registers and an ink stone under a tiled gate roof, a tall vermilion gate with brass studs behind it, a stone-paved square in front."),
}
jobs = []
for name, (ref, width, height, prompt) in ITEMS.items():
    for seed in (420000, 420001):
        jobs.append({"id": f"{name}-{seed}", "reference_images": [f"{R}/{ref}"], "prompt": prompt, "width": width, "height": height, "seed": seed, "output_name": f"{name}-{seed}.png"})
json.dump({"jobs": jobs}, open(f"{A}/refs.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
print(jobs[0]["prompt"]); print(len(jobs))
