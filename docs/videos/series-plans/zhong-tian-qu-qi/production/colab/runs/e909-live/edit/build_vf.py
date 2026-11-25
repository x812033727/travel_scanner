import json
exec(open('mkvf.py').read().split("S={")[0])
S={
 's07': None,
 's08': window('w8',[(700,78,898,238)],150),
 's09': window('w9',[(320,10,500,170),(810,0,960,240)],150),
 's12': window('w12',[(545,75,705,225)],150),
 's13': window('w13',[(490,36,705,185),(870,0,960,205)],150),
 's17': window('w17',[(585,66,808,218)],150),
 's18': window('w18',[('track',[(0,603,0,795,124),(1,605,40,791,182),(2,615,104,797,240),(3,628,122,810,259),(4,641,128,824,266),(5,649,130,832,269),(6,655,130,839,269),(7,665,126,850,265),(7.5,683,115,872,255),(8,711,104,905,246),(8.5,746,109,945,254),(9.2,790,112,960,258)])],95),
}
# s07 bedroll: purple-mauve -> grey-blue (luma kept), only mauve pixels (b>=g, r>g) inside a box that follows the roll
keys=[(0.8,215,175,300,290),(1.0,220,180,312,292),(1.5,270,180,358,305),(2.0,265,190,402,318)]
X0,Y0=420,330; W,H=400,335
xa=lin([(k[0],k[1]*KX-X0) for k in keys],0); xb=lin([(k[0],k[3]*KX-X0) for k in keys],0)
ya=lin([(k[0],k[2]*KY-Y0) for k in keys],0); yb=lin([(k[0],k[4]*KY-Y0) for k in keys],0)
Lm="(0.3*r(X,Y)+0.59*g(X,Y)+0.11*b(X,Y))"
mask=(f"clip((b(X,Y)-g(X,Y)+12)/8,0,1)*clip((r(X,Y)-g(X,Y)-8)/8,0,1)*clip((T-0.75)/0.1,0,1)"
      f"*clip((X-({xa}))/14,0,1)*clip((({xb})-X)/14,0,1)*clip((Y-({ya}))/14,0,1)*clip((({yb})-Y)/14,0,1)")
bed=(f"split[bd0][bd1];[bd1]crop={W}:{H}:{X0}:{Y0},format=rgba,geq=r='0.82*{Lm}':g='0.95*{Lm}':b='min(255,1.18*{Lm})':a='255*{mask}'[bd2];[bd0]format=rgba[bd3];[bd3][bd2]overlay={X0}:{Y0},format=yuv420p")
S['s07']=bed+","+window('w7',[(555,110,745,258)],150)
S['s10']=json.load(open('vf-all.json'))['s10']
json.dump(S,open('vf-final.json','w'),indent=1)
