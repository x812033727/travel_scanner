"""e917 fix2: s13 once more, now with a picture of A-ling whose hair is down. Same flow as fix1: retake.py from live/st1 (the d1
edits and fix1's s13 edits are applied first, taken unchanged from ../fix1/spec.json), mkjobs.py for the duration, the swapped
and absolute picture paths and output_path, preflight-prompts.py. Seeds 9171301/9171302, 6 s.

    python3 -I mkspec.py
    python3 -I ../../_scripts/retake.py <live>/st1 <live>/fix2 spec.json
    python3 -I mkjobs.py <live>/fix2
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix2/colab-jobs.json

Why: fix1's s13 (9171201, 9171202) and d1's 9171102 all draw a high bun with a wooden pin on A-ling's crown, the whole shot,
although the text lets her hair down: the one A-ling picture fix1 still sent, angles/aling-angle-a-l1, has that bun (so do
her portrait and angle-b), and the picture wins over the text. s12 and s14 around it have her hair loose. The cure is the
picture: live-action/screen-test-aling-loose.py (seeds 37027/37028) is a one-change edit of aling-angle-a-l1 with only the hair
changed (loose, parted in the middle, smooth over the top and back of the head, two wet sections over the front of both
shoulders to the chest, a few strands on her cheek); the coordinator's pick is filed as
refs-live/angles/aling-loose-angle-a-l1.png and sent here in aling-angle-a-l1's place (swap_pictures, absolute path). Everything
else is fix1's s13: the hair sentence kept as it is (it now agrees with the picture), Xu Yan's portrait and angle-a, the yard
picture swapped to set-xujia-yuan-huo-l1, her empty hands at her sides.

The picture may not exist yet when this is built: mkjobs.py then warns, and q-e917fix2.sh refuses to start without it.
"""
import copy
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
FIX1 = json.loads((HERE.parent / "fix1" / "spec.json").read_text(encoding="utf-8"))["shots"]
LOOSE = ("/home/user/zt-work/docs/videos/series-plans/zhong-tian-qu-qi/production/assets/refs-live/angles/"
         "aling-loose-angle-a-l1.png")

s13 = copy.deepcopy(FIX1["s13"])
assert s13.get("duration_seconds") == 6 and "aling-angle-a-l1.png" not in s13.get("drop_pictures", []), s13
assert any("two wet curtains" in new for _, new in s13["replace"]), "fix1's s13 hair sentence is not in ../fix1/spec.json"
s13["swap_pictures"] = dict(s13.get("swap_pictures", {}), **{"aling-angle-a-l1.png": LOOSE})
S = {"s13": s13}
(HERE / "spec.json").write_text(json.dumps({"seeds": [9171301, 9171302], "shots": S}, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
print(len(S), "shot ->", HERE / "spec.json", s13["swap_pictures"])
