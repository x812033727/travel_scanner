"""Read-only PNG RGBA decoder for independent pixel evidence; writes no images."""
import hashlib, struct, zlib
from pathlib import Path

def desc(path):
 path=Path(path);b=path.read_bytes();return {'file':str(path),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def decode_rgba(path):
 b=Path(path).read_bytes();assert b[:8]==b'\x89PNG\r\n\x1a\n';pos=8;ids=[];header=None
 while pos<len(b):
  n=struct.unpack('>I',b[pos:pos+4])[0];k=b[pos+4:pos+8];v=b[pos+8:pos+8+n];crc=struct.unpack('>I',b[pos+8+n:pos+12+n])[0];assert zlib.crc32(k+v)&0xffffffff==crc
  pos+=n+12
  if k==b'IHDR':header=struct.unpack('>IIBBBBB',v)
  elif k==b'IDAT':ids.append(v)
  elif k==b'IEND':break
 assert pos==len(b)
 w,h,depth,color,compression,filtering,interlace=header;assert depth==8 and color in [2,6] and compression==0 and filtering==0 and interlace==0
 channels=3 if color==2 else 4;stride=w*channels;raw=zlib.decompress(b''.join(ids));assert len(raw)==h*(stride+1);rows=[];prev=bytearray(stride)
 for y in range(h):
  f=raw[y*(stride+1)];r=bytearray(raw[y*(stride+1)+1:(y+1)*(stride+1)]);assert f in [0,1,2,3,4]
  for x in range(stride):
   a=r[x-channels] if x>=channels else 0;u=prev[x];c=prev[x-channels] if x>=channels else 0
   if f==1:r[x]=(r[x]+a)&255
   elif f==2:r[x]=(r[x]+u)&255
   elif f==3:r[x]=(r[x]+((a+u)//2))&255
   elif f==4:
    q=a+u-c;pa=abs(q-a);pb=abs(q-u);pc=abs(q-c);r[x]=(r[x]+(a if pa<=pb and pa<=pc else u if pb<=pc else c))&255
  prev=r
  if channels==3:rows.append(bytes(c for x in range(w) for c in (*r[x*3:x*3+3],255)))
  else:rows.append(bytes(r))
 return {'width':w,'height':h,'color_type':color,'bit_depth':depth}, rows

def window_rgba(rows,rectangle):
 x,y,w,h=[rectangle[k] for k in ['x','y','w','h']];assert y>=0 and y+h<=len(rows);assert x>=0 and (x+w)*4<=len(rows[0]);b=b''.join(r[x*4:(x+w)*4] for r in rows[y:y+h]);assert len(b)==w*h*4;return b
