import numpy as np, wave, subprocess
from warp4 import T_of_v as M, DUR, GAP_AT, GAP
SR=44100; N=int(SR*DUR); out=np.zeros(N); rng=np.random.default_rng(4); t=np.arange(N)/SR
def add(start, sig, g=1.0, raw=False):
    i=int((start if raw else M(start))*SR); j=min(N,i+len(sig))
    if 0<=i<N: out[i:j]+=sig[:j-i]*g
def env(n,a=0.005,r=None):
    e=np.ones(n); na=max(1,int(a*SR)); e[:na]=np.linspace(0,1,na)
    if r: e*=np.exp(-np.arange(n)/SR/r)
    return e
def tone(f,d,w='sin'):
    n=int(d*SR); ff=np.broadcast_to(f,(n,)) if np.ndim(f) else np.full(n,f)
    ph=2*np.pi*np.cumsum(ff)/SR
    return {'sin':np.sin(ph),'saw':2*((ph/(2*np.pi))%1)-1,'sq':np.sign(np.sin(ph))}[w]
def noise(d): return rng.standard_normal(int(d*SR))
def lp(x,a):
    y=np.empty_like(x); acc=0.0
    for i in range(len(x)): acc+=a*(x[i]-acc); y[i]=acc
    return y
def popsnd(st,g=0.3,f0=300,f1=900,d=0.1,raw=False): add(st, tone(np.linspace(f0,f1,int(d*SR)),d)*env(int(d*SR),0.002,d/2), g, raw)
def ding(st,g=0.2,f=1318): add(st,(tone(f,0.4)+0.5*tone(f*1.335,0.4))*env(int(0.4*SR),0.002,0.12),g)
def whoosh(st,g=0.5): n=lp(noise(0.35),0.08)*np.sin(np.linspace(0,np.pi,int(0.35*SR))); add(st-0.15,n,g)
def buzzer(st): add(st, lp(tone(140,0.35,'sq'),0.3)*env(int(0.35*SR),0.005,0.2),0.3)
def giggle(st,g=0.22):
    for k in range(4):
        f=1100+k*90; add(st+k*0.11, tone(f*(1+0.08*np.sin(np.linspace(0,30,int(0.08*SR)))),0.08)*env(int(0.08*SR),0.003,0.03), g)
def slide(st,f0,f1,d,g=0.18): add(st, tone(np.linspace(f0,f1,int(d*SR)),d)*env(int(d*SR),0.01,d), g)
def boing(st,g=0.3):
    d=0.5; f=180+60*np.sin(np.linspace(0,25,int(d*SR)))*np.exp(-np.linspace(0,4,int(d*SR)))
    add(st, tone(f,d)*env(int(d*SR),0.002,0.2), g)
# playful marimba loop (pentatonic), whole video
notes=[523.25,587.33,659.25,783.99,880.0,783.99,659.25,587.33, 523.25,659.25,783.99,659.25,587.33,523.25,440.0,523.25]
bass=[130.81,130.81,146.83,146.83,164.81,164.81,146.83,146.83]
step=0.25
for k,b in enumerate(np.arange(0.2, DUR-1.0, step)):
    f=notes[k%16]
    m=(tone(f,0.3)+0.3*tone(f*4,0.3))*env(int(0.3*SR),0.002,0.07)
    if k%2==0 or k%16 in (5,11): add(b,m,0.10,raw=True)
    if k%4==0:
        bb=bass[(k//4)%8]; add(b, tone(bb,0.4)*env(int(0.4*SR),0.003,0.15),0.16,raw=True)
# s1 bridge crash
add(0.4, lp(noise(0.9),0.08)*env(int(0.9*SR),0.003,0.35),0.8)
for k in range(3): boing(0.6+k*0.25,0.25)
for k in range(3): slide(3.6+k*0.6,400,1400,0.5)
giggle(5.5); giggle(6.6,0.18)
# s2
whoosh(9.0); popsnd(9.0,0.35,200,600,0.15); popsnd(10.0,0.3,300,800,0.12)
for k in range(3): ding(11.5+k*0.12,0.12,2093+k*200)
# s3
whoosh(14.0); popsnd(14.0,0.35,250,700,0.15); giggle(17.0); giggle(17.6,0.18); giggle(18.3,0.15)
# steps
whoosh(20.0)
for st in (21.0,26.0,31.0,37.0,42.0): ding(st,0.2)
boing(23.8,0.3); buzzer(28.5)
slide(31.4,500,1800,0.6,0.2); add(32.2, lp(tone(np.linspace(200,140,int(0.6*SR)),0.6,'saw'),0.1)*env(int(0.6*SR),0.02,0.4),0.15)
giggle(34.0)
buzzer(38.2); add(39.2, lp(tone(np.linspace(110,90,int(0.6*SR))*(1+0.05*np.sin(np.linspace(0,60,int(0.6*SR)))),0.6,'saw'),0.15)*env(int(0.6*SR),0.02,0.3),0.25)
whoosh(43.0,0.6); slide(43.0,900,300,0.6,0.15)
rd=M(49.0)-M(45.0); add(45.0, lp(noise(rd),0.5)*np.sin(np.linspace(0,np.pi,int(rd*SR)))**0.3,0.10)
# s5 / s6
whoosh(49.0); ding(50.5,0.2,2637); giggle(53.0,0.28); giggle(53.5,0.22)
popsnd(54.0,0.3,200,600,0.3)
sfx=out/np.max(np.abs(out))
raw=subprocess.run(["ffmpeg","-v","error","-i","vo/vo4.mp3","-f","f32le","-ac","1","-ar",str(SR),"-"],capture_output=True).stdout
vo=np.frombuffer(raw,dtype=np.float32).astype(np.float64)
voice=np.zeros(N); voice[:min(N,len(vo))]=vo[:N]; voice=voice/np.max(np.abs(voice))*0.95
w=int(0.05*SR); e=np.sqrt(np.convolve(voice**2,np.ones(w)/w,mode="same"))
on=(e>0.02).astype(float); k=int(0.25*SR); on=np.clip(np.convolve(on,np.ones(k)/k,mode="same")*1.5,0,1)
mix=voice+sfx*0.42*(1-0.6*on); mix=mix/np.max(np.abs(mix))*0.95
fade=np.ones(N); fade[-int(0.4*SR):]=np.linspace(1,0,int(0.4*SR)); mix*=fade
with wave.open('audio4_vo.wav','wb') as wv:
    wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((mix*32767).astype(np.int16).tobytes())
print("ok")
