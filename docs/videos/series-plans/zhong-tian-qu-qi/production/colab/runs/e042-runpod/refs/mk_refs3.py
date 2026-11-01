"""The innkeeper and the registrar of e042: no picture held them, and they came out as cartoons."""
import json, os
A = os.path.dirname(os.path.abspath(__file__))
R = f"{A}/refs-dh"
STYLE = "3D Chinese donghua CG, Unreal Engine 5 cinematic render, stylized semi-realistic with realistic human proportions and a normal-sized nose and eyes, detailed clearly CG skin with pores and fine wrinkles, individually rendered hair strands, physically simulated cloth with wear, volumetric light"
def portrait(text):
    return (f"Paint a new character portrait in exactly the same rendering style, lighting and framing as image 1, a different person from image 1. "
            f"He is: {text}. Upper body, facing the camera, a calm expression, against a dark smoky blue-grey backdrop. {STYLE}.")
ITEMS = {
 "innkeeper-portrait-t1": portrait("an East Asian man of about fifty, thin with a narrow pinched face, small shrewd eyes, a thin moustache, greying black hair in a small bun on the crown, a plain grey-brown cotton long robe with black cloth oversleeves"),
 "registrar-portrait-t1": portrait("an East Asian clerk of about forty-five, a lean sallow face with sunken cheeks and heavy-lidded bored eyes, a short thin goatee, a black cloth cap, a plain dark green clerk's robe with a white inner collar, a writing brush tucked behind one ear"),
}
jobs = []
for name, prompt in ITEMS.items():
    for seed in (420000, 420001):
        jobs.append({"id": f"{name}-{seed}", "reference_images": [f"{R}/sunzhanggui-portrait-t1.png"], "prompt": prompt, "width": 1024, "height": 1360, "seed": seed, "output_name": f"{name}-{seed}.png"})
json.dump({"jobs": jobs}, open(f"{A}/refs3.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
print(len(jobs))
