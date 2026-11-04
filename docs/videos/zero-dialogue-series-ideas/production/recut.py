#!/usr/bin/env python3
"""Humor-gate recut (QA-2026-11-04): rewrite each episode's edit/plan.json from the cut lists below.
  python3 recut.py [slug ...]      (keeps the first plan as plan.v1.json; then run edit.py and qa_check.py)

A shot is (clip name, in, dur, [(sfx, at, gain_db)...], {options}); options are the edit.py ones
(hold, reverse, push, anchor, lights_out, music_off). A clip name is looked up in edit/ first (stills,
crops and other processed clips live there), then colab/clips/. "black" is a black card.
Why each change: QA-2026-11-04.md (two humor reviewers; gag drawn by both and funny >= 3 to pass).
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

W = Path("/root/mokaair-work/videos")
# Extra sound effects (ffmpeg lavfi), made into every episode's edit/sfx on demand.
EXTRA = {
    "inhale": ["-f", "lavfi", "-i", "anoisesrc=c=pink:d=0.7:a=0.5", "-af", "highpass=f=900,lowpass=f=5000,afade=t=in:d=0.6,afade=t=out:st=0.6:d=0.1"],
    "gurgle": ["-f", "lavfi", "-i", "sine=f=140:d=0.9", "-af", "tremolo=f=11:d=0.9,vibrato=f=7:d=0.8,afade=t=out:st=0.6:d=0.3,volume=6dB"],
    "poof": ["-f", "lavfi", "-i", "anoisesrc=c=brown:d=0.35:a=0.9", "-af", "lowpass=f=1200,afade=t=out:st=0.05:d=0.3"],
    "click": ["-f", "lavfi", "-i", "anoisesrc=c=white:d=0.04:a=0.8", "-af", "highpass=f=2500,afade=t=out:st=0.01:d=0.03"],
}

CUTS = {
 "wangjia-couple-e01": [
  ("s01-basket", 0.3, 1.0, [("splat", 0.2, 0)]),
  ("s02-dump", 0.2, 2.6, [("splat", 0.9, -4)]),
  ("s04-see", 0.4, 2.6, [("pop", 0.6, 0)]),
  ("s05-turn", 0.3, 2.4, [("tension", 0.0, 0)], {"hold": 0.5, "music_off": True}),
  ("s06-hung", 0.2, 1.8, [("wind", 0.0, -6)]),
  ("s07-street", 0.2, 2.6, [("wind", 0.0, -8), ("birds", 1.4, -6)], {"push": [1.0, 1.15], "anchor": [0.5, 0.4]})],
 "wangjia-couple-e02": [
  ("s01-perm-still", 0, 2.0, [("pop", 0.8, 0)]),
  ("s02-ignore", 0.3, 2.0, []),
  ("s04-twin", 0.3, 3.0, [("tension", 0.0, -4), ("pop", 0.4, -6)]),
  ("s05-buzz", 0.3, 1.7, [("buzz", 0.1, 0)]),
  ("s06-clutch", 0.05, 1.45, [("pop", 0.7, 0)], {"hold": 0.6})],
 "wangjia-couple-e03": [
  ("s01-tap", 0.3, 2.4, [("tap", 0.2, 0), ("pop", 1.4, -8)]),
  ("s02-door", 0.3, 2.4, [("lock", 1.9, 0)]),
  ("s03-cobweb", 0.3, 3.2, [("wind", 0.0, -8), ("birds", 0.4, 0), ("tension", 0.8, 0)]),
  ("s05-slipper", 0.3, 0.9, [("lock", 0.75, 0)], {"push": [3.5, 3.5], "anchor": [0.5, 1.0]}),
  ("s03-cobweb", 2.9, 1.5, [], {"hold": 1.1, "music_off": True})],
 "wangjia-couple-e04": [
  ("s02-game", 1.35, 2.0, [("buttons", 0.0, 0)]),
  ("s03-door", 0.3, 2.0, [("tension", 0.0, 0)]),
  ("s05-crib", 0.3, 1.8, [("musicbox", 0.0, 0)]),
  ("s06-crop", 0.9, 1.2, [("buttons", 0.0, 0)]),
  ("s07-mobile", 0.3, 2.8, [("musicbox", 0.0, -8), ("click", 2.0, 0)], {"hold": 0.8})],
 "wangjia-couple-e05": [
  ("s01-burrito", 0.3, 0.9, [("snore", 0.0, 0)]),
  ("s02-twitch", 0.3, 0.8, [("tension", 0.0, 0)]),
  ("s04-mega", 0.3, 2.8, [("pop", 0.3, -6)]),
  ("s03-petbed", 0.3, 2.6, [("birds", 0.0, -8)]),
  ("s05-towel", 0.4, 2.0, [("snore", 0.0, -4)], {"hold": 0.9, "music_off": True})],
 "raccoon-mischief-e01": [
  ("s01-crash", 0.2, 0.8, [("shatter", 0.0, 0)]),
  ("s02-key", 0.3, 0.8, [("keys", 0.1, 0)]),
  ("s03-still", 0, 2.6, [("crunch", 1.6, -4)], {"push": [1.45, 1.6], "anchor": [0.5, 0.55]}),
  ("s05-mama", 0.3, 2.4, [("keys", 0.0, -6)]),
  ("s04-lamp", 0.2, 2.6, [("sting", 1.2, 0), ("click", 2.1, 0)], {"hold": 0.7})],
 "raccoon-mischief-e02": [
  ("s01-crop", 0.3, 1.2, [("shatter", 0.0, 0)]),
  ("s02-key", 0.3, 0.6, [("keys", 0.1, 0)]),
  ("s03-chandelier", 0.3, 3.0, [("chime", 0.5, -6), ("click", 0.6, 0)]),
  ("s05-on", 0.2, 2.2, [("chime", 0.5, 0)]),
  ("s06-read", 0.3, 1.2, []),
  ("s05-on", 1.4, 0.6, [("click", 0.1, 0)]),
  ("s06-read", 1.5, 0.9, []),
  ("s07-dawn", 0.3, 3.0, [("sting", 2.2, 0)])],
 "raccoon-mischief-e03": [
  ("s01-kick", 0.3, 2.0, [("shatter", 0.0, 0)]),
  ("s02-key", 0.3, 0.7, [("keys", 0.1, 0)]),
  ("s03-frame", 0.3, 2.8, []),
  ("s04-remote", 0.3, 1.8, [("beep", 1.75, 0)], {"hold": 0.8, "music_off": True}),
  ("s05-anchor", 0.2, 1.8, []),
  ("s06-onions", 0.2, 2.0, [("beep", 0.0, 0)]),
  ("s07-off", 0.3, 3.0, [("tvoff", 0.0, 0), ("sting", 2.2, 0)])],
 "raccoon-mischief-e04": [
  ("s01-swing", 0.3, 2.8, [("shatter", 0.0, 0), ("boing", 0.4, 0)]),
  ("s02-key", 0.3, 0.6, [("keys", 0.1, 0)]),
  ("s03-hands", 0.3, 2.2, [("tick", 0.0, 0), ("tick", 0.9, -4), ("tick", 1.8, -4)], {"hold": 0.7}),
  ("s04-watch", 2.6, 2.0, [("tick", 0.0, -8)], {"push": [1.7, 1.85], "anchor": [0.5, 0.0]}),
  ("s05-spin", 0.3, 2.2, [("ratchet", 0.0, 0)]),
  ("s06-cuckoo", 2.3, 2.4, [("cuckoo", 0.2, 0), ("sting", 1.5, 0)], {"hold": 0.9})],
 "raccoon-mischief-e05": [
  ("s01-pot", 0.3, 2.8, [("crunch", 0.0, 0)]),
  ("s02-key", 0.3, 0.6, [("keys", 0.1, 0)]),
  ("s03-plant", 0.3, 3.0, []),
  ("s04-can", 0.3, 0.8, [("pour", 0.1, 0)]),
  ("s05-wet", 0.3, 1.8, []),
  ("s06-sprout", 0.3, 3.0, [("poof", 1.9, 0), ("sting", 2.0, 0)], {"hold": 0.6})],
 "influencer-piglet-e01": [
  ("s01-sunset", 0.2, 1.2, [("shutter", 0.9, 0)]),
  ("s03-pullback", 0.3, 3.0, [("recordscratch", 0.0, 0)]),
  ("s04-boyfriend", 0.3, 1.6, []),
  ("s05-photo", 0.2, 2.4, [("shutter", 0.0, 0)]),
  ("s06-again", 1.1, 2.2, [("crack", 1.2, 0)]),
  ("s07-sun", 0.8, 3.0, [])],
 "influencer-piglet-e02": [
  ("s01-snow", 0.3, 1.2, [("shutter", 0.9, 0)]),
  ("s03-rooftop", 0.3, 3.0, [("recordscratch", 0.0, 0), ("blender", 0.3, -6)]),
  ("s04-boyfriend", 0.3, 2.2, [("blender", 0.0, -4)]),
  ("s05-still", 0, 2.4, [("shutter", 0.0, 0)]),
  ("s04-boyfriend", 1.6, 0.9, [("inhale", 0.1, 0)], {"hold": 0.4, "music_off": True, "push": [1.9, 2.3], "anchor": [0.54, 0.16]}),
  ("s06-sneeze", 0.5, 3.0, [("sneeze", 0.0, 0)], {"hold": 0.8})],
 "influencer-piglet-e03": [
  ("s01-falls-still", 0, 1.2, [("shutter", 0.9, 0)]),
  ("s03-roof", 0.3, 3.0, [("recordscratch", 0.0, 0), ("pour", 0.3, -4)]),
  ("s04-boyfriend", 0.3, 2.8, [("pour", 0.0, -6)]),
  ("s05-crop", 0.3, 3.4, [("shutter", 0.0, 0), ("gurgle", 2.2, 0)], {"push": [1.0, 1.8], "anchor": [0.95, 0.0], "hold": 0.6})],
 "influencer-piglet-e04": [
  ("s01-sakura", 0.3, 1.2, [("shutter", 0.9, 0)]),
  ("s03-lot", 0.3, 3.0, [("recordscratch", 0.0, 0), ("blower", 0.3, -6)]),
  ("s04-boyfriend", 0.3, 2.2, [("blower", 0.0, -4)]),
  ("s05-photo-v2", 0, 2.4, [("shutter", 0.0, 0)]),
  ("s06-dump", 0.5, 3.6, [("whoosh", 0.2, 0), ("thud", 0.7, 0), ("poof", 2.9, 0)], {"hold": 0.8})],
 "influencer-piglet-e05": [
  ("s01-fireflies", 0.3, 1.2, [("shutter", 0.9, 0)]),
  ("s03-garage", 1.9, 1.8, [("recordscratch", 0.0, 0), ("hum", 0.3, 0)]),
  ("s04-boyfriend", 0.3, 2.2, [("hum", 0.0, -4)]),
  ("s05-photo", 0.2, 1.8, [("shutter", 0.0, 0)]),
  ("s06-tangle", 0.5, 1.5, [("whoosh", 0.2, 0)]),
  ("s04-boyfriend", 1.0, 0.9, [("powerdown", 0.2, 0)], {"push": [2.2, 2.2], "anchor": [0.68, 0.57], "lights_out": [0.45]}),
  ("s06-tangle", 2.0, 1.6, [("click", 0.3, 0), ("click", 0.6, 0)], {"lights_out": [0.3, 0.6], "music_off": True})],
 "shechu-hell-e01": [
  ("s02-pack", 0.2, 1.4, []),
  ("s03-crop", 0.3, 1.5, []),
  ("s04-turn", 0.3, 1.0, []),
  ("s05-fall", 0.5, 1.6, [("paper", 0.0, 0)]),
  ("s06-night", 0.3, 2.0, [("crickets", 0.0, -6)]),
  ("s07-again", 1.0, 2.4, [("dun", 1.8, 0)], {"hold": 0.6})],
 "shechu-hell-e02": [
  ("s01-present", 0.3, 2.6, []),
  ("s02-pupils", 0.3, 2.4, [("dun", 0.0, -6)]),
  ("s03-wiggle", 0.3, 2.0, []),
  ("s04-realize", 0.3, 0.6, [("tension", 0.0, 0)]),
  ("s05-wreck", 0.3, 3.0, [("crash", 0.0, 0), ("paper", 0.6, -4)]),
  ("s06-dot", 0.3, 2.6, [("dun", 1.6, 0)]),
  ("s02-pupils", 2.4, 0.6, []),
  ("black", 0, 0.5, [])],
 "shechu-hell-e03": [
  ("s01-slack", 0.3, 2.2, [("bell", 1.7, 0)]),
  ("s03-work", 0.3, 2.2, [("typing", 0.0, 0)]),
  ("s04-toy", 0.3, 2.0, [("bell", 0.0, -4)]),
  ("s05-relax", 0.2, 1.4, []),
  ("s06-shadow", 1.6, 2.0, [("dun", 0.4, 0)]),
  ("s07-perch", 0.3, 2.5, [("click", 1.3, 4), ("thud", 1.6, 0)], {"hold": 1.4, "music_off": True})],
 "shechu-hell-e04": [
  ("s01-knock", 0.3, 1.2, [("knock", 0.4, 0)]),
  ("s02-box", 0.3, 2.2, [("dun", 0.4, -6)]),
  ("s03-plead", 0.5, 1.8, []),
  ("s04-sink", 1.5, 2.6, [("gurgle", 0.6, -2)]),
  ("s05-clean", 0.3, 3.0, [("paper", 0.0, -4)]),
  ("s06-steal", 0.3, 2.6, [("dun", 1.6, 0)])],
 "shechu-hell-e05": [
  ("s01-sun", 0.3, 0.9, []),
  ("s02-sneak", 0.3, 2.2, [("dun", 0.0, -6)]),
  ("s03-return", 0.3, 1.4, [("dun", 1.3, 0)], {"hold": 0.8}),
  ("s04-keyboard", 0.3, 3.0, [("typing", 0.3, -10)]),
  ("s05-crop", 0.3, 1.1, [("aircon", 0.0, 0)]),
  ("s06-warm", 0.3, 2.2, []),
  ("s07-eye", 0.3, 3.0, [("dun", 1.2, 0)], {"hold": 0.6, "push": [1.06, 1.06], "anchor": [1.0, 0.5]})],
}


def clip_path(ep, name):
    if name == "black":
        return "black"
    for p in (ep / "edit" / f"{name}.mp4", ep / "colab" / "clips" / f"{name}.mp4"):
        if p.exists():
            return str(p)
    sys.exit(f"{ep.name}: no clip {name}")


def main():
    for slug in sys.argv[1:] or CUTS:
        ep = W / slug
        planf = ep / "edit" / "plan.json"
        if not (ep / "edit" / "plan.v1.json").exists():
            shutil.copy(planf, ep / "edit" / "plan.v1.json")
        plan = json.loads(planf.read_text())
        sfx = ep / "edit" / "sfx"
        shots = []
        for row in CUTS[slug]:
            name, cin, dur, cues = row[:4]
            opts = row[4] if len(row) > 4 else {}
            for c in cues:
                f = sfx / f"{c[0]}.wav"
                if not f.exists():
                    if c[0] not in EXTRA:
                        sys.exit(f"{slug}: no sfx {c[0]}")
                    subprocess.run(["ffmpeg", "-v", "error", "-y", *EXTRA[c[0]], "-ar", "48000", "-ac", "2", str(f)], check=True)
            shots.append({"clip": clip_path(ep, name), "in": cin, "dur": dur, **{k: v for k, v in opts.items() if v},
                          "sfx": [{"file": str(sfx / f"{c[0]}.wav"), "at": c[1], **({"gain_db": c[2]} if c[2] else {})} for c in cues]})
        plan["shots"] = shots
        planf.write_text(json.dumps(plan, indent=1))
        print(f"{slug}: {len(shots)} shots, {sum(s['dur'] for s in shots):.1f} s planned")


if __name__ == "__main__":
    main()
