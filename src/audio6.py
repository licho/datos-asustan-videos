import numpy as np, wave, subprocess
from warp6 import T_of_v as M, DUR
SR=44100; N=int(SR*DUR); out=np.zeros(N); rng=np.random.default_rng(6)
def add(st, sig, g, raw=False):
    i=int((st if raw else M(st))*SR); j=min(N,i+len(sig))
    if 0<=i<N: out[i:j]+=sig[:j-i]*g
def sq(f, d, duty=0.5, decay=None):
    n=int(d*SR); ff=np.broadcast_to(f,(n,)) if np.ndim(f) else np.full(n,f)
    ph=(np.cumsum(ff)/SR)%1.0; s=np.where(ph<duty,1.0,-1.0)
    return s*np.exp(-np.arange(n)/SR/(decay or d*0.9))
def nz(d, decay): n=int(d*SR); return rng.uniform(-1,1,n)*np.exp(-np.arange(n)/SR/decay)
# chiptune loop
bpm=140; step=60/bpm/2
mel=[330,0,392,330,440,392,330,0,294,0,330,294,262,294,330,0]
bass=[82.4,82.4,98,98,73.4,73.4,82.4,82.4]
for k,st in enumerate(np.arange(0,DUR-0.6,step)):
    f=mel[k%16]
    if f: add(st, sq(f,step*0.85,0.25), 0.10, raw=True)
    if k%2==0: add(st, sq(bass[(k//2)%8],step*1.8,0.5), 0.11, raw=True)
    if k%4==0:
        kick=np.sin(2*np.pi*np.cumsum(np.linspace(150,40,int(0.1*SR)))/SR)*np.exp(-np.arange(int(0.1*SR))/SR/0.04); add(st,kick,0.35,raw=True)
    if k%4==2: add(st, nz(0.05,0.015), 0.15, raw=True)
def jingle(st, notes, g=0.22, d=0.09):
    for i,f in enumerate(notes): add(st, sq(f,d,0.5), g, raw=False) if i==0 else add(M(st)+i*d, sq(f,d,0.5), g, raw=True)
def coin(st): jingle(st,[988,1319],0.18,0.07)
def hurt(st): add(st, sq(np.linspace(400,80,int(0.4*SR)),0.4,0.5), 0.22)
def roar(st): add(st, np.convolve(nz(0.8,0.3),np.ones(40)/40,mode='same')+0.4*sq(np.linspace(110,70,int(0.8*SR)),0.8,0.3), 0.45)
def powerup(st): add(st, sq(np.linspace(300,1200,int(0.5*SR)),0.5,0.25), 0.18)
def pow_(st): add(st, nz(0.15,0.04), 0.4)
def blip(st): add(st, sq(1500,0.05,0.5), 0.12)
jingle(0.0,[523,659,784,1047],0.22,0.1)
add(4.2, sq(1760,0.25,0.5), 0.15); roar(4.25)
hurt(11.1); hurt(30.2)
for s in (9.5,16.0,22.0,28.0,33.0): coin(s+2.0)
powerup(19.0); roar(29.2)
add(34.5, sq(np.linspace(600,150,int(0.7*SR)),0.7,0.5), 0.15)
for k in range(5): pow_(37.6+k*0.33)
for k in range(4): add(47.5+k*0.2, nz(0.08,0.03), 0.3)
for k in range(8): blip(52.0+k*0.667)
sfx=out/np.max(np.abs(out))
raw=subprocess.run(["ffmpeg","-v","error","-i","vo/vo6.mp3","-f","f32le","-ac","1","-ar",str(SR),"-"],capture_output=True).stdout
vo=np.frombuffer(raw,dtype=np.float32).astype(np.float64)
voice=np.zeros(N); voice[:min(N,len(vo))]=vo[:N]; voice=voice/np.max(np.abs(voice))*0.95
w=int(0.05*SR); e=np.sqrt(np.convolve(voice**2,np.ones(w)/w,mode="same"))
on=(e>0.02).astype(float); k=int(0.25*SR); on=np.clip(np.convolve(on,np.ones(k)/k,mode="same")*1.5,0,1)
mix=voice+sfx*0.38*(1-0.6*on); mix=mix/np.max(np.abs(mix))*0.95
fade=np.ones(N); fade[-int(0.4*SR):]=np.linspace(1,0,int(0.4*SR)); mix*=fade
with wave.open('audio6_vo.wav','wb') as wv:
    wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((mix*32767).astype(np.int16).tobytes())
print("ok")
