"""e938 fix5: the coordinator's four retakes after REVIEW 3 (s18 s19 s20 s29) and the two shots the new saddle drags along (s30 s32)
(fix5 prep agent, 2026-11-24; owner: "fix what is wrong; tell me only what cannot be fixed; quality first"). Why in plan.md.

    python3 -I mkspec.py                       # -> spec.json (6 shots, seeds 9381701/9381702)
    python3 -I mkjobs.py <live>/fix5           # -> <live>/fix5/prompts/*.txt, retake.json, colab-jobs.json (12 jobs, 76 s)
    python3 -I <scratchpad>/tools/check938f5.py <live>/fix5   # check938.py's assertions, rewritten for these six shots
    python3 -I ../../_scripts/preflight-prompts.py <live>/fix5/colab-jobs.json
    python3 -I <repo>/.agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix5/colab-jobs.json

The base of each job is the job the cut uses now (../picks-final.tsv): d1 9381101 for s18 s19 s29 s30 s32, fix1 9381302 for s20,
exactly as sent (mkjobs.py checks the sha256 and that every edit of the base round's spec.json is in it). So the d1 appended
pictures ride along (the horse prop in s18 s20 s29 s30 s32, Tang Xiaotang's night hair reference in s18; last, with their
sentence, the header unchanged). Bought at the base length (= r2.py BUY). Each replace is asserted to be in the base once.

The saddle: the cut's horse wears a western saddle with a bright horn (REVIEW 3 A19), and it shows wherever the saddle is empty
or in plain view: s29 after she dismounts, s30 at the left of the frame, s32 in the middle of the wide. Changing s29 alone would
make the next two shots jump back to the western saddle, so the same sentence goes into all five horse shots of fix5, written as
the thing it is (rule 18: no negated nouns), with no bright metal word in it.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
LIVE = pathlib.Path("/root/mokaair-work/videos/zhong-tian-qu-qi-e938-dh/runpod/live")
SEEDS = [9381701, 9381702]
BASE = {"s18": ("d1", 9381101), "s19": ("d1", 9381101), "s20": ("fix1", 9381302), "s29": ("d1", 9381101),
        "s30": ("d1", 9381101), "s32": ("d1", 9381101)}
DUR = {"s18": 8, "s19": 8, "s20": 5, "s29": 5, "s30": 6, "s32": 6}  # = the base jobs = r2.py BUY
STATIC = "The camera holds a static shot."
PUSH = "The camera pushes in with small amplitude at slow speed."
SADDLE_OLD = "an old plain brown leather saddle on a folded dark cloth"
SADDLE_NEW = ("a low flat old saddle of plain dark brown leather stretched over a plain wooden frame, its front low, smooth and "
              "rounded, all of it dark and worn, on a folded dark cloth")


def basetext(sid):
    rnd, seed = BASE[sid]
    return (LIVE / rnd / "prompts" / f"ref-{sid}-{seed}.txt").read_text(encoding="utf-8")


def once(sid, s):
    assert basetext(sid).count(s) == 1, (sid, s[:80])
    return s


S = {sid: {"duration_seconds": DUR[sid], "base": list(BASE[sid]), "replace": []} for sid in DUR}
for sid in ("s18", "s20", "s29", "s30", "s32"):
    S[sid]["replace"].append([once(sid, SADDLE_OLD), SADDLE_NEW])

# s18: the horse walks out of the yard gate (REVIEW 3 A16, cut short and covered with galloping hooves). Now it gallops from the
# first frame, seen from behind and a little to the side, right to left, out through the clear left half of the gateway (the leaf
# hangs on the right post, swung back inward, so the left half is the open way). Tang Xiaotang stays as d1 wrote her: from behind,
# two buns, head still, her night hair reference last.
S["s18"]["replace"] += [
    [once("s18", "already riding away from us into the gateway, never the lens, well clear of the young woman;"),
     "already at a full gallop from the first frame, seen from behind and a little to the side, racing from the right toward "
     "the clear left half of the gateway, never the lens, well clear of the young woman;"],
    [once("s18", "A-ling digs her heels in and the horse bursts out through the gateway into the dark, its shoulder knocking the "
                 "half-swung slatted gate leaf back against the wall,"),
     "The horse gallops flat out through the clear left half of the gateway and away into the dark, its hooves pounding, never "
     "slowing, A-ling crouched low over its neck,"],
    [once("s18", PUSH), STATIC],
]

# s19: a plush bear floats in front of the bed (REVIEW 3 A13; the reviewers saw a teddy where the text said "a small woven straw
# rabbit beside her pillow"). The rabbit is written once, small, flat, of straw, on the pillow at her cheek; no other toy is named
# and none is denied. The one flame on the stool, written as the only flame. Static, so his knees stay in the frame.
S["s19"]["replace"] = [
    [once("s19", "a small woven straw rabbit lying beside her pillow,"),
     "one small flat rabbit woven of pale dry straw, the size of her palm, lying on the pillow right beside her cheek,"],
    [once("s19", "the warm light of the one small flame on the low stool at the foot of the bed falling on them from the left;"),
     "the warm light of the one small flame on the low stool at the foot of the bed falling on them from the left, the only "
     "flame in the room;"],
    [once("s19", PUSH), STATIC],
]

# s20: fix1 9381302 runs at the camera three-quarter front (bible rule 41: side or side-rear only). Strict profile, the camera
# square to the road and level with it, the road parallel to the bottom of the frame; full gallop and A-ling flat over the neck
# from the first frame; the road written dark (the beaten earth as dark as the field), never pale.
S["s20"]["replace"] += [
    [once("s20", "low-angle wide shot from the side of the road at ground height, side-on: a long line of tall dark poplars across "
                 "the frame against the deep blue night sky and a pale beaten earth path along their foot running across the frame "
                 "from the right edge to the left;"),
     "low-angle wide shot from the side of the road at ground height, the camera square to the road and level with it, in "
     "strict profile: a long line of tall dark poplars across the frame against the deep blue night sky and a beaten earth path "
     "along their foot, dark grey under the moon and as dark as the field, running straight across the frame parallel to its "
     "bottom edge from the right edge to the left;"],
    [once("s20", "coming in at the right edge, seen side-on, its legs stretched long,"),
     "coming in at the right edge, seen exactly side-on in strict profile, its whole body broadside to the camera, its head "
     "toward the left, its legs stretched long,"],
    [once("s20", "crouched low over its neck, framed full figure;"), "crouched flat over its neck from the first frame, framed full figure;"],
    [once("s20", "The horse gallops flat out across the whole frame from right to left along the path at the foot of the poplars,"),
     "The horse gallops flat out across the whole frame from right to left along the path at the foot of the poplars, always "
     "broadside to the camera and always at the same distance from it,"],
]
# s29, s30, s32: only the saddle (above); everything else as the d1 take the cut uses, its camera included.

(HERE / "spec.json").write_text(json.dumps({"seeds": SEEDS, "shots": S}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(S), "shots ->", HERE / "spec.json", f"({sum(DUR.values())} s per seed, {2 * sum(DUR.values())} s)")
