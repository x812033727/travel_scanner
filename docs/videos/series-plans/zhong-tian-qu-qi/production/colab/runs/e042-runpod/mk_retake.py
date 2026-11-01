"""e042 retake after reviewing the drafts against the storyboard, rebuilt by ref2manifest, two seeds each."""
import glob, json, os, subprocess, sys
repo, mk = sys.argv[1], sys.argv[2]
A = os.path.dirname(os.path.abspath(__file__)); R = f"{A}/retake"; os.makedirs(R, exist_ok=True)
H = f"{repo}/docs/videos/series-plans/zhong-tian-qu-qi/production"
REFS = "C:/Users/x8120/mokaair-work/videos/zhong-tian-qu-qi-e042-dh/refs/refs-dh"
ff = json.load(open(f"{H}/hailuo/ff-dh-e042.json", encoding="utf8"))
# The set picture pulls these shots out to a roomy view and copies the people into its background.
NO_SET = {"s06", "s09", "s13", "s32", "s34", "s35"}
for f in ff:
    if f["id"] in NO_SET:
        f["refs"] = [r for r in f["refs"] if "set-" not in r]
ff_path = f"{R}/ff.json"
json.dump(ff, open(ff_path, "w", encoding="utf8"), ensure_ascii=False)
# Unnamed speakers came out as cartoons with no picture to hold them; refs/mk_refs3.py painted one for each.
FACE = {"s18": ("innkeeper", "The innkeeper"), "s31": ("registrar", "The registrar"), "s33": ("registrar", "The registrar")}
KEEP = "the same rendering as the picture, not a cartoon."
S29 = "The registrar shown in <Picture 1> keeps exactly the same face, hair and costume as the picture; the location shown in <Picture 2> is the set, keeping its layout and props."
SET = "the location shown in <Picture 1> is the set, keeping its layout and props."
FIX = {
 "s02": "The paper of the window is whole and untorn. He crosses to the window inside the first half of the shot; both his hands push the wooden window frame and it swings wide open outward onto the moonlit night before the shot ends.",
 "s06": "The camera is inside the dark gate passage, its black arched walls framing the edges of the picture for the whole shot, and the four walk away from the dark into the blazing light. Beyond them the street is immense, crowded from edge to edge and running away to the horizon, far bigger than the four small figures.",
 "s09": "The framing stays a medium shot from the waist up from the first frame to the last. Her eyes are hidden under the brim in every frame. She moves right across the frame, and at the end the ox cart covers her from the chest down.",
 "s13": "The shot opens directly on this two-shot and holds it: both men from the chest up, their two faces large and side by side, filling the frame; the street stays blurred behind them. There is one Xu Dalang and one Xu Yan.",
 "s16": "The shot opens directly on this overhead view of the open ledger, which fills the frame from the first frame to the last; the room is never seen. The pages hold only faint wavy grey lines.",
 "s18": "He wears the same plain grey-brown long robe with black oversleeves as in the picture, his hair in a small bun. He looks like a real person, realistic proportions, not a cartoon. Behind him are the dark wooden lattice and red lanterns of the inn, blurred.",
 "s19": "The shot opens directly on this insert of the waist, which fills the frame from the first frame to the last; the room is never seen. At the end the brown-sleeved hand wraps from above around the thin grey-sleeved wrist, four fingers over the top and the thumb under it, gripping it hard; the two palms never meet.",
 "s20": "The thief is a skinny grown man of thirty with hollow cheeks and stubble, as tall as her shoulder, never a child. The framing holds both of them from the waist up, her jaw and red lips clearly in the light under the brim. Her twist bends him over and he staggers away out of the frame on screen left.",
 "s29": "He wears the same dark green clerk's robe and black cap as in the picture, realistic proportions, not a cartoon, sitting behind the table on screen right with the open register under his hand and his head down.",
 "s31": "He wears the same dark green clerk's robe and black cap as in the picture. He looks like a real person, realistic proportions, not a cartoon. The framing is his head, chest and hands, large in the frame, behind him a blurred vermilion gate under grey light.",
 "s32": "The shot opens directly on this close-up and holds it; his face fills the left two thirds of the frame. There is one man only; behind him is only a blurred red wall, with no other figure, no table and no hand in front of him.",
 "s33": "He wears the same dark green clerk's robe and black cap as in the picture. He looks like a real person, realistic proportions, not a cartoon. The framing is his head, chest and hands, large in the frame, behind him a blurred vermilion gate under grey light.",
 "s34": "His face looks straight ahead with his chin level from the first frame to the last, his eyes open and lifted above the camera. It is cold flat grey daylight, with no lit windows; behind him are only blurred grey standing figures in a queue. His topknot and hair are as in the pictures.",
 "s35": "The shot opens directly on this medium close-up and holds it; he stands alone in the frame from the chest up on screen right, and his eyes are hidden in the shadow of the brim, only his mouth and chin lit. Behind him are only blurred bareheaded scholars; no other straw hat anywhere, and nobody in the foreground.",
}
env = {**os.environ, "VIDEO_WORKDIR": R}
subprocess.run(["node", mk, f"{H}/hailuo/clips-dh-e042.json", ff_path, "42", R, "--refs", REFS, "--only", ",".join(FIX), "--seed", "420100", "--width", "960", "--height", "544"], check=True, env=env)
jobs = []
for path in sorted(glob.glob(f"{R}/ref-e042-part*.json")):
    for job in json.load(open(path, encoding="utf8"))["jobs"]:
        sid = job["id"]
        file = f"{R}/{job['prompt_file']}"
        text = open(file, encoding="utf8").read()
        if sid in FACE:
            name, label = FACE[sid]
            assert SET in text
            text = text.replace(SET, f"{label} shown in <Picture 1> keeps exactly the same face, hair and costume as the picture, in the same place.")
            job["reference_images"] = [f"{REFS}/{name}-portrait-t1.png"]
        if sid == "s29":
            assert SET in text
            text = text.replace(SET, S29).replace("<Picture 1> is referenced", "<Picture 1> and <Picture 2> are referenced")
            job["reference_images"] = [f"{REFS}/registrar-portrait-t1.png", *job["reference_images"]]
        at = text.find("overall_soundscape")
        head = text[:at].rstrip()
        text = head + " " + FIX[sid] + text[len(head):]
        open(file, "w", encoding="utf8", newline="\n").write(text)
        print(sid, [os.path.basename(x.replace(chr(92), "/")) for x in job["reference_images"]])
        for seed in (420100, 420101):
            item = {k: v for k, v in job.items() if k not in ("output_path", "output_name", "prompt_sha256")}
            item.update(id=f"{sid}-{seed}", seed=seed, output_name=f"{sid}-{seed}.mp4")
            jobs.append(item)
json.dump({"jobs": jobs}, open(f"{R}/retake.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
print(len(jobs), "jobs")
