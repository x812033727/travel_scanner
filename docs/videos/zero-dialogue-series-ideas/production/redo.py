#!/usr/bin/env python3
"""Mark shots for a redo: new first-frame prompt (+ guards), new clip prompt, and delete the old outputs.
  python3 redo.py   (edits ff.json/prompts in each workdir from REDO below)"""
import json, os
from pathlib import Path
W = Path("/root/mokaair-work/videos")
PAW = " All of the animal's limbs are furry animal paws with no human fingers, no human hands, no human skin."
NOBODY = " The background is empty: no people, no other animals, no duplicate of the character."
H = "For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.\n\nintegrated_multimodal_description: [Shot 1] live-action. "
T = " One continuous shot.\noverall_soundscape: N/A\nnon_diegetic_music: N/A\n"
CLIPGUARD = " The character stays the same animal in the same clothes for the whole shot; its paws stay furry animal paws; no new character enters."
REDO = {
 "wangjia-couple-e01": {
  "s01-basket": ("Medium shot of a cozy living room: A-Fu the Corgi himself lies on his back on a grey sofa in his blue and white striped pyjamas, holding a phone above his face with both front paws, a plastic laundry basket full of wet dripping clothes sitting on his round belly. He is the only animal in the picture.",
                 "The Corgi shown in <Picture 1> keeps scrolling the phone with his paws while water drips from the laundry basket on his belly; he wiggles one hind paw lazily and does not look up. The camera holds a static shot.")},
 "wangjia-couple-e02": {
  "s03-antenna": ("Close-up of Zhenzhu the Shiba herself with a gigantic fluffy pink permed afro hairdo (no hair rollers), a frozen sweet smile.",
                  "The Shiba shown in <Picture 1> holds her pose; her smile tightens; a single strand of hair rises out of the huge pink perm like an antenna, and her head turns slowly toward the camera. Her lips remain closed. The camera pushes in with small amplitude at slow speed."),
  "s05-buzz": ("Medium shot of a living room doorway: Zhenzhu the Shiba herself stands upright in her pink floral dress; the fur on top of her head is clipped very short and flat in a neat buzz cut, clearly showing the shape of her head, no perm, no curlers, no hat; one paw rests on top of her short head.",
               "The Shiba shown in <Picture 1> rubs her short buzz-cut head with one paw and then strikes a proud pose toward the camera. The camera holds a static shot.")},
 "wangjia-couple-e03": {
  "s05-slipper": ("Medium shot of a closed white bathroom door at floor level: the door is open just a crack and a single pink fluffy slipper with a red Shiba paw inside pokes out through the gap onto the hallway floor; nothing else of the dog is visible.",
                  "The pink slipper shown in <Picture 1> pauses on the floor for a beat, then slowly slides back in through the gap and the door clicks shut. The camera holds a static shot.")},
 "raccoon-mischief-e02": {
  "s07-dawn": ("Low-angle medium shot of the living room ceiling in morning daylight: Doudou the young raccoon himself hangs in mid-air from the ceiling hook by the hood of his yellow hoodie, his feet dangling well above the floor, strings of crystal beads draped on him, two plain flashlights in his paws flickering weakly, an exhausted face.",
               "The young raccoon shown in <Picture 1> hangs from the ceiling hook, feet dangling in the air; the flashlights flicker and dim; his arms tremble with tiredness. The camera holds a static shot.")},
 "raccoon-mischief-e03": {
  "s04-remote": ("Medium shot of Papa raccoon himself sitting on the sofa in his blue knitted vest and reading glasses, holding a plain black TV remote in both front paws, pointing it forward. He is the only animal in the picture.",
                 "The father raccoon shown in <Picture 1> pauses, then presses the button on the remote with his thumb-paw, expressionless. The camera holds a static shot.")},
 "raccoon-mischief-e05": {
  "s04-can": ("Medium shot of Mama raccoon herself in her green knitted sweater and pearl necklace standing in the living room, holding a green watering can in both front paws and pouring water onto a big lump under the patterned rug at her feet. She is the only animal in the picture.",
              "The mother raccoon shown in <Picture 1> calmly pours water from the watering can onto the lump under the rug; the lump flinches. Her face stays expressionless. The camera holds a static shot.")},
 "influencer-piglet-e01": {
  "s03-pullback": ("Wide shot of an empty grubby back alley behind a Taiwanese night market in the afternoon, with nobody else in it: Fenfen the pink pig herself in her white lace dress and straw hat stands posing on an upside-down red plastic bucket; an orange heat lamp hangs from a bamboo laundry pole with its cable trailing to the ground; behind her a big blue plastic tarp hangs in waves from the right edge; a puddle on the ground; a stray cat beside the bucket.",
                   "The tarp shown in <Picture 1> ripples as if shaken from off screen right; the stray cat walks slowly past the bucket; the pig holds her pose perfectly still. The camera holds a static shot."),
  "s06-again": ("Wide shot of the same empty back alley with nobody else in it: Fenfen the pink pig herself in her white lace dress and straw hat stands on an upside-down red plastic bucket, glaring off screen to the right.",
                "The pig shown in <Picture 1> takes a deep breath and snaps back into a dreamy profile pose; the bucket cracks and she sinks a few centimetres into it, her smile frozen. The camera holds a static shot.")},
 "influencer-piglet-e02": {
  "s06-sneeze": ("Medium shot on a sun-baked concrete rooftop: Fenfen the pink pig herself, photorealistic, in a white knitted beanie and a white wool sweater, standing upright in a dreamy profile pose; the photo looks like real live-action photography, not a cartoon.",
                 "The pig shown in <Picture 1> holds her dreamy pose; suddenly a huge burst of shaved ice blasts into her from the right side and covers her completely in white ice; she stays frozen, smile unchanged. The camera holds a static shot.")},
 "influencer-piglet-e03": {
  "s01-falls": ("Close-up of Fenfen the pink pig herself in her white lace dress and straw hat with a pink ribbon, a dreamy profile smile, a beautiful jungle waterfall behind her in soft focus; both front hooves rest together at her chest.",
                "The pig shown in <Picture 1> holds her dreamy pose; mist from the waterfall drifts around her; the hat ribbon flutters; one thin stream of water arcs in from the right edge of the frame. The camera holds a static shot.")},
 "shechu-hell-e01": {
  "s02-pack": ("Medium shot of an empty small office with nobody else in it: A-Jin the Golden Retriever himself stands upright beside his grey desk in his white shirt and crooked blue tie, a brown briefcase strap already over his shoulder, a hopeful smile, the laptop on the desk closed.",
               "The Golden Retriever shown in <Picture 1> flicks his tie over his shoulder and tiptoes toward the right of the frame with his tail wagging. The camera holds a static shot."),
  "s05-fall": None},
 "shechu-hell-e02": {
  "s04-realize": ("Medium close-up of A-Jin the Golden Retriever himself in his white shirt and crooked blue tie in a meeting room, a small laser pointer held between his two furry front paws at his chest, his proud smile fading.",
                  "The Golden Retriever shown in <Picture 1> slowly turns his head toward the camera, his smile freezes, his ears droop and his eyes widen. The camera holds a static shot.")},
 "shechu-hell-e03": {
  "s02-ears": ("Medium close-up of A-Jin the Golden Retriever himself in his white shirt and crooked blue tie lounging in his office chair, his ears suddenly perked straight up, eyes wide, in an empty office with nobody else in it.",
               "The Golden Retriever shown in <Picture 1> freezes with his ears up, then his eyes dart left and right in alarm. The camera holds a static shot."),
  "s05-relax": ("Medium shot of A-Jin the Golden Retriever himself in his white shirt and crooked blue tie leaning back in his office chair at his grey desk, both furry front paws behind his head, a smug relieved grin, in an empty office with nobody else in it.",
                "The Golden Retriever shown in <Picture 1> lets out a long relieved breath and settles deeper into the chair with a smug grin. The camera holds a static shot.")},
 "shechu-hell-e04": {
  "s03-plead": ("Medium shot of A-Jin the Golden Retriever himself in his white shirt and crooked blue tie standing in an empty office with nobody else in it, holding up a sheet of paper with a simple hand-drawn rising arrow chart (no words, no numbers) between his two furry front paws, an earnest pleading face.",
                "The Golden Retriever shown in <Picture 1> lifts the chart a little higher and gives an earnest hopeful look, tail wagging slowly. The camera holds a static shot."),
  "s06-steal": ("Medium shot of an office floor: a cardboard box tied with a big red ribbon bow, and Boss Miao the chubby orange tabby cat himself in his grey suit and gold tie sitting inside the box, only his head and shoulders showing, expressionless. He is the only animal in the picture.",
                "The cat shown in <Picture 1> settles deeper into the box, closes his eyes contentedly and yawns once. The camera holds a static shot.")},
}
for slug, shots in REDO.items():
    w = W / slug / "colab"
    ff = json.loads((w / "ff.json").read_text())
    for sid, spec in shots.items():
        if spec is None:
            continue
        ffp, clip = spec
        for j in ff["jobs"]:
            if j["id"] == sid:
                lead = j["prompt"].split(". ", 1)[0] if j["prompt"].startswith("image 1") else ""
                j["prompt"] = (lead + ". " if lead else "") + ffp + PAW + NOBODY + " Photorealistic live-action photograph, vertical 9:16 frame. No readable text, no watermark, no logos."
                j["seed"] = 3
        (w / "prompts" / f"{sid}.txt").write_text(H + clip + CLIPGUARD + T)
        for f in (w / "ff" / f"{sid}.png", w / "clips" / f"{sid}.mp4", w / f"{sid}.detached.json"):
            if f.exists():
                os.rename(f, str(f) + ".old")
    (w / "ff.json").write_text(json.dumps(ff, indent=1))
    print(slug, [s for s, v in shots.items() if v])
