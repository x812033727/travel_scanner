import json,sys
vf=json.load(open('vf-final.json'))
M=json.load(open('music.json')) if len(sys.argv)>1 else None
def sx(f,at,off,gain,to=None):
    d={"file":f,"at":at,"off":off,"gain":gain}
    if to: d["to"]=to
    return d
sfx=[
 # beds
 sx("Wind","s01",0,-32,"s01"), sx("hooves_trot","s01",0,-28,"s01"),
 sx("Wind","s02",0,-38,"s06"), sx("fire-1","s02",0,-46,"s06"),
 sx("fire","s07",0,-46,"s18"), sx("Wind","s07",0,-42,"s18"),
 sx("Wind","s19",0,-38,"s20"),
 sx("Wind","s21",0,-26,"s21"), sx("Wind","s22",0,-30,"s22"), sx("fire-1","s21",0,-44,"s22"),
 sx("Wind","s23",0,-38,"s23"), sx("fire","s24",0,-44,"s32"), sx("Wind","s24",0,-44,"s32"),
 sx("Wind","s33",0,-37,"s38"),
 # s01 arrival
 sx("creak3","s01",6.05,-32),
 # s02 Xiaohe runs in
 sx("footstep_wood_000","s02",0.1,-30), sx("footstep_wood_000","s02",0.38,-31), sx("footstep_wood_000","s02",0.66,-32), sx("cloth1","s02",0.9,-30),
 # s03 picks up the bedroll
 sx("rustle03","s03",1.0,-26), sx("cloth1","s03",2.4,-28), sx("rustle03","s03",3.6,-30),
 # s04 candlestick shoved into his hand
 sx("cloth2","s04",1.4,-30), sx("impactMetal_light_000","s04",1.75,-32),
 # s05 abacus behind door 1, whetstone behind door 3
 sx("impactWood_light_000","s05",0.2,-36), sx("impactWood_light_001","s05",0.32,-37), sx("impactWood_light_000","s05",0.44,-36), sx("impactWood_light_001","s05",0.62,-38), sx("impactWood_light_000","s05",0.74,-37),
 sx("drawKnife1","s05",2.6,-38), sx("drawKnife2","s05",3.4,-38), sx("drawKnife1","s05",4.2,-37), sx("drawKnife2","s05",5.0,-37), sx("drawKnife1","s05",5.8,-38),
 # s06 pushed down the corridor
 sx("cloth1","s06",5.0,-28), sx("footstep_wood_000","s06",5.25,-30), sx("footstep_wood_000","s06",5.7,-31), sx("footstep_wood_000","s06",6.2,-31), sx("footstep_wood_000","s06",6.75,-32),
 # s07 door hinge, steps in
 sx("creak1","s07",0.9,-28), sx("footstep_wood_000","s07",1.6,-32), sx("footstep_wood_000","s07",2.15,-33),
 # s08 steps to the table
 sx("footstep_wood_000","s08",0.5,-32), sx("footstep_wood_000","s08",1.0,-33),
 # s09 sits, abacus pushed across
 sx("impactWood_light_001","s09",1.4,-30), sx("wooden_01","s09",2.5,-32), sx("impactWood_light_000","s09",2.62,-36),
 # s10 page turn, finger on paper
 sx("bookFlip1","s10",0.55,-26), sx("paper_02","s10",3.0,-38), sx("paper_02","s10",5.5,-38),
 # s12 her beads stop
 sx("impactWood_light_000","s12",0.15,-34), sx("impactWood_light_001","s12",0.3,-34), sx("impactWood_light_000","s12",0.48,-35),
 # s13 ledger turned and pushed to her
 sx("bookFlip2","s13",3.1,-26), sx("paper_04","s13",4.0,-30),
 # s14 a run of beads, stop, one pressed
 *[sx("impactWood_light_00%d"%(i%2),"s14",round(0.05+0.13*i,2),-28-(i%3)) for i in range(9)],
 sx("impactWood_light_001","s14",1.95,-31),
 # s16 nose rub
 sx("cloth1","s16",0.8,-34),
 # s17 the stack of books lands
 sx("bookPlace1","s17",3.3,-18), sx("impactWood_medium_000","s17",3.32,-24),
 # s18 stands, picks up the bedroll, hand on the door
 sx("impactWood_light_000","s18",1.1,-30), sx("rustle03","s18",7.4,-24), sx("cloth2","s18",8.0,-28), sx("creak2","s18",8.9,-30),
 # s19 door shut, back against it, rubs brow, steps off
 sx("door_close_01","s19",0.0,-24), sx("impactWood_light_001","s19",0.2,-30), sx("cloth1","s19",3.6,-36), sx("footstep_wood_000","s19",5.8,-33), sx("footstep_wood_000","s19",6.35,-34),
 # s20 two knocks, door ajar
 sx("impactWood_light_000","s20",4.3,-22), sx("impactWood_light_001","s20",4.75,-22), sx("creak1","s20",6.9,-26),
 # s21 window paper in the wind
 sx("rustle03","s21",0.5,-30), sx("rustle03","s21",2.2,-31),
 # s22 window shut
 sx("creak3","s22",6.9,-30), sx("impactWood_medium_001","s22",7.55,-22),
 # s23 whetstone behind the door stops as he pushes
 sx("drawKnife1","s23",0.3,-32), sx("drawKnife2","s23",1.1,-32), sx("drawKnife1","s23",1.9,-32), sx("drawKnife2","s23",2.7,-33), sx("drawKnife1","s23",3.5,-33), sx("drawKnife2","s23",4.3,-34), sx("drawKnife1","s23",5.1,-34),
 sx("creak2","s23",7.2,-26),
 # s24 blade to the neck: the accent
 sx("drawKnife2","s24",0.9,-20), sx("impactMetal_heavy_000","s24",1.1,-24), sx("impactSoft_heavy_000","s24",1.1,-26),
 # s25 hands up
 sx("cloth1","s25",1.0,-30),
 # s26 fingers tighten on the grip
 sx("drawKnife1","s26",3.0,-38),
 # s27 turned round, back hits the door
 sx("cloth2","s27",0.4,-28), sx("impactWood_medium_000","s27",0.65,-24),
 # s28 hand over the scar
 sx("cloth1","s28",1.1,-28),
 # s29 picks up the bedroll
 sx("rustle03","s29",5.4,-28),
 # s31 bedroll spread on the floor
 sx("rustle03","s31",1.8,-24), sx("impactSoft_heavy_000","s31",2.2,-30), sx("cloth1","s31",2.8,-28), sx("cloth2","s31",3.6,-28),
 # s32 the blade lowered
 sx("drawKnife1","s32",1.0,-38),
 # s33 quilt thrown on him
 sx("cloth2","s33",0.7,-26), sx("impactSoft_heavy_000","s33",0.95,-22), sx("rustle03","s33",1.1,-30),
 # s35 turns over
 sx("cloth1","s35",1.7,-28), sx("cloth2","s35",2.2,-28),
 # s36 quilt over his head
 sx("cloth1","s36",1.6,-28), sx("rustle03","s36",2.3,-24), sx("cloth2","s36",3.2,-30),
 # s37 palm on the door
 sx("impactWood_light_001","s37",1.65,-26), sx("creak3","s37",1.85,-36),
 # s38 quilt pulled down
 sx("rustle03","s38",0.2,-28),
]
edit={
 "tempo":1.0,"grades":{},"default_grade":"dh","finish":"vignette=angle=PI/5,format=yuv420p","names":{},
 "punch":False,"slow_max":1.1,"interpolate":False,"duck_ratio":3.5,"duck_release_ms":900,
 "sfx_dirs":["<VIDEO_WORKDIR>/_series/zhong-tian-qu-qi/sfx"],"name_whoosh":"swish-9",
 "music": M or [],
 "sfx":sfx,"frame_round":True,"clip_voice":True,
 "voice_skip":{"s07":1.0,"s30":0.5},
 "voice_until":{"s18":5.6},
 "clip_af":{"s03":{"from":0,"af":"alimiter=limit=0.7:attack=1:release=50:level=false"},"s17":{"from":0,"af":"alimiter=limit=0.7:attack=1:release=50:level=false"}},
 "voice_off":["s09","s12","s16","s19","s33","s34","s35","s36"],
 "min":{},
 "line_at":{"zq909a04":1.0,"zq909a08":0.5,"zq909a09":0.8,"zq909a11":1.2,"zq909a14":0.37,"zq909a18":0.3,"zq909a20":0.3,"zq909a31":0.37,"zq909a32":0.37,"zq909a33":1.0,"zq909a34":0.1},
 "vf":{k:vf[k] for k in ["s07","s08","s09","s10","s12","s13","s15","s17","s18"]},
}
json.dump(edit,open(sys.argv[2] if len(sys.argv)>2 else 'edit-v0.json','w'),ensure_ascii=False,indent=1)
