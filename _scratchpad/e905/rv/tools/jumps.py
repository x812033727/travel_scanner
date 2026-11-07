import subprocess,sys,numpy as np
for f in sys.argv[1:]:
    w,h=96,54
    raw=subprocess.run(['ffmpeg','-v','error','-i',f,'-vf',f'scale={w}:{h},format=gray','-f','rawvideo','-'],capture_output=True).stdout
    a=np.frombuffer(raw,np.uint8).reshape(-1,h,w).astype(float)
    d=np.abs(np.diff(a,axis=0)).mean(axis=(1,2))
    med=np.median(d); i=int(d.argmax())
    print(f.split('/')[-1], f"max {d.max():.1f} at {(i+1)/24:.2f}s  median {med:.1f} ratio {d.max()/max(med,0.3):.1f}")
