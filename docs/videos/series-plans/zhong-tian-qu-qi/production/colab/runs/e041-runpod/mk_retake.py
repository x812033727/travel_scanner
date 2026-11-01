"""e041 retake after reviewing the drafts against the storyboard, rebuilt by ref2manifest, two seeds each."""
import glob, json, os, subprocess, sys
repo, mk = sys.argv[1], sys.argv[2]
A = os.path.dirname(os.path.abspath(__file__)); R = f"{A}/retake"; os.makedirs(R, exist_ok=True)
H = f"{repo}/docs/videos/series-plans/zhong-tian-qu-qi/production"
ff = json.load(open(f"{H}/hailuo/ff-dh-e041.json", encoding="utf8"))
# The set picture pulls these shots out to a roomy view; without it the framing holds (e040 s14, s50).
NO_SET = {"s02", "s05", "s13", "s23", "s24", "s26", "s27", "s30", "s33", "s35"}
SWAP = {
 # The shape was only named in s31 and s32, so s33 drew a double disc hanging from nothing.
 "s33": [("the white jade pendant lifted beside his cheek on its red cord", "his raised hand beside his cheek pinching a red cord, a flat oval white jade pendant about the size of a walnut hanging from his fingers")],
 # A named hand brings its owner's whole body into the background (e040 s54).
 "s32": [("Xu Yan's open palm", "a man's open palm"), ("Xu Yan speaks off screen", "a man's voice speaks off screen")],
}
for f in ff:
    for old, new in SWAP.get(f["id"], []):
        f["prompt"] = f["prompt"].replace(old, new)
    if f["id"] in NO_SET:
        f["refs"] = [r for r in f["refs"] if "set-" not in r]
    if f["id"] == "s32":
        f["refs"] = [r for r in f["refs"] if "set-" in r]
ff_path = f"{R}/ff.json"
json.dump(ff, open(ff_path, "w", encoding="utf8"), ensure_ascii=False)
FIX = {
 "s01": "The shot opens with Xu Yan already low in a crouch on his heels and he stays on both feet, never on his knees; he wears dark cloth shoes and Diao Qi wears black leg wraps and boots, no bare feet anywhere. Diao Qi's wrists stay tied with the hemp rope for the whole shot.",
 "s02": "The framing stays a close-up from the first frame to the last, his scarred face large on screen right; his two wrists stay tied together with thick hemp rope at the bottom of the frame, and they shake the fanning gesture while still tied; no table and no flame in the foreground.",
 "s05": "She stands upright and never sits; the framing stays a medium close-up from the waist up, her face and shoulders large on screen right; her right hand slides inside the left sleeve and stays there, and no blade is ever seen.",
 "s07": "Diao Qi sits on the floor against the sacks with his wrists tied for the whole shot and never stands. Xu Yan ends standing between them, his back to A-ling, facing Diao Qi. Everyone wears shoes, no bare feet.",
 "s09": "His jaw is set and his brows are low for the whole shot, with no smile. The door is half open in the first frame; he leans his weight into his palm and the door swings outward until it stands fully open at the end, the blue dusk light falling on his face.",
 "s13": "The framing stays a close-up from the first frame to the last: his round face fills the left half of the frame, one ringed hand at the bottom edge; the servants and the street stay small and blurred behind him.",
 "s23": "The framing stays a close-up from the first frame to the last: her face and shoulders fill the frame on screen right, the iron key at the bottom edge; the room stays dark and blurred behind her.",
 "s24": "The shot opens directly on this close-up and holds it. He is indoors for the whole shot: only the mud-brick wall and the lamp glow are behind him, never the sky, trees or the outside of a house.",
 "s26": "The shot opens directly on this medium close-up, her face and shoulders large in the frame from the waist up, and she keeps the proportions of a grown woman of eighteen. She rises fully off the stool to standing, and the abacus goes up over her head.",
 "s27": "The shot opens directly on this medium close-up: he is already standing, large in the frame from the waist up on screen left; his palm comes down on the table and the lamp flame jumps.",
 "s30": "The framing stays a medium close-up from the first frame to the last, his head, shoulders and hands large on screen left. A small dark oilcloth packet about the size of a palm is visibly stuck under the book; as the book lifts, it slips free and falls back into the box; his hands stop in the air and his eyes follow it down.",
 "s32": "The shot opens directly on this close view: from the first frame to the last the frame holds only one open hand and the jade pendant, very large; no face and no whole person is ever in the frame, near or far.",
 "s33": "The framing stays a close-up, his face large on screen left. The pendant is one flat oval disc that hangs from the cord pinched in his own fingers; the same hand turns it slowly in the candlelight.",
 "s35": "His head stays still and his face stays turned to the camera for the whole shot; only his eyes slide toward the window on screen right, while his fingers close over the pendant and tuck it into his sleeve.",
}
env = {**os.environ, "VIDEO_WORKDIR": R}
subprocess.run(["node", mk, f"{H}/hailuo/clips-dh-e041.json", ff_path, "41", R, "--refs", f"{H}/assets/refs-dh", "--only", ",".join(FIX), "--seed", "410100", "--width", "960", "--height", "544"], check=True, env=env)
jobs = []
for path in sorted(glob.glob(f"{R}/ref-e041-part*.json")):
    for job in json.load(open(path, encoding="utf8"))["jobs"]:
        sid = job["id"]
        file = f"{R}/{job['prompt_file']}"
        text = open(file, encoding="utf8").read()
        if sid == "s32":
            text = text.replace("Xu Yan", "the man")
        at = text.find("overall_soundscape")
        head = text[:at].rstrip()
        text = head + " " + FIX[sid] + text[len(head):]
        open(file, "w", encoding="utf8", newline="\n").write(text)
        print(sid, [os.path.basename(x.replace(chr(92), "/")) for x in job["reference_images"]])
        for seed in (410100, 410101):
            item = {k: v for k, v in job.items() if k not in ("output_path", "output_name", "prompt_sha256")}
            item.update(id=f"{sid}-{seed}", seed=seed, output_name=f"{sid}-{seed}.mp4")
            jobs.append(item)
json.dump({"jobs": jobs}, open(f"{R}/retake.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
print(len(jobs), "jobs")
