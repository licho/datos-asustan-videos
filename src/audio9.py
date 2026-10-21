import numpy as np, wave, subprocess
from warp9 import T_of_v as M, DUR
SR=44100; N=int(SR*DUR); out=np.zeros(N); rng=np.random.default_rng(9)
def add(st, sig, g=1.0, raw=False):
    i=int((st if raw else M(st))*SR); j=min(N,i+len(sig))
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
def popsnd(st,g=0.3,f0=300,f1=900,d=0.1): add(st, tone(np.linspace(f0,f1,int(d*SR)),d)*env(int(d*SR),0.002,d/2), g)
def ding(st,g=0.2,f=1568): add(st,(tone(f,0.4)+0.5*tone(f*1.335,0.4))*env(int(0.4*SR),0.002,0.12),g)
def whoosh(st,g=0.5): n=lp(noise(0.35),0.08)*np.sin(np.linspace(0,np.pi,int(0.35*SR))); add(st-0.15,n,g)
def buzzer(st,g=0.3): add(st, lp(tone(140,0.35,'sq'),0.3)*env(int(0.35*SR),0.005,0.2),g)
def boing(st,g=0.3):
    d=0.5; f=180+60*np.sin(np.linspace(0,25,int(d*SR)))*np.exp(-np.linspace(0,4,int(d*SR))); add(st, tone(f,d)*env(int(d*SR),0.002,0.2), g)
def thud(st,g=0.9): add(st, tone(np.linspace(140,45,int(0.4*SR)),0.4)*env(int(0.4*SR),0.002,0.1),g)
def sting(st,g=0.4,d=2.0):
    s=sum(tone(f,d,'saw') for f in (55,58.3,110.4,116.7)); add(st, lp(s,0.07)*env(int(d*SR),0.01,0.8),g)
def span(a,b): return M(b)-M(a)
t=np.arange(N)/SR
vt=np.interp(t, __import__('warp9').TK, __import__('warp9').VK)
for b in np.arange(0, DUR-1, 60/80):
    f=49 if int(b/(60/80))%8<6 else 46.2
    add(b, lp(tone(f,0.7,'saw'),0.04)*env(int(0.7*SR),0.01,0.25),0.25*(1-0.7*((vt[min(N-1,int(b*SR))]>=25)&(vt[min(N-1,int(b*SR))]<68))),raw=True)
sting(0.0,0.35,1.8); add(2.3, tone(np.linspace(900,700,int(0.6*SR)),0.6)*env(int(0.6*SR),0.01,0.3),0.12)
for st in (6.0,18.0,25.0,40.0,55.0,68.0,76.0): whoosh(st)
thud(15.5,0.8); sting(15.5,0.3,1.6)
for i in range(4): popsnd(11.5+i*0.08,0.15,400,900,0.06)
for k in range(10): popsnd(18.2+k*0.25,0.08,600,1200,0.05)
for i in range(4): ding(19.0+i*0.1,0.12,1568)
popsnd(20.5,0.3,250,800,0.12)
boing(30.0,0.3); add(35.0, tone(np.linspace(600,300,int(0.5*SR)),0.5)*env(int(0.5*SR),0.01,0.3),0.15); ding(35.3,0.2,2093)
popsnd(41.0,0.25,300,700,0.1); boing(48.0,0.35)
d=span(51,54); add(51, lp(tone(np.linspace(110,90,int(d*SR)),d,'saw'),0.06)*np.sin(np.linspace(0,np.pi,int(d*SR))),0.15)
for k in range(10): add(55.5+k*0.18, lp(noise(0.06),0.3)*env(int(0.06*SR),0.002,0.02),0.25)
buzzer(61.3)
sting(68.0,0.3,2.0); thud(69.0,0.8)
for k in range(10): add(72.0+k*0.12, lp(noise(0.05),0.3)*env(int(0.05*SR),0.002,0.02),0.3)
d=span(76,84); ch=sum(tone(f,d) for f in (220,261.6,329.6)); add(76, ch*np.sin(np.linspace(0,np.pi,int(d*SR))),0.12)
d=3.0; ch=sum(tone(f,d) for f in (523.25,659.25,783.99,1046.5)); add(88.0, ch*np.sin(np.linspace(0,np.pi,int(d*SR)))*0.3,0.3)
popsnd(88.0,0.3,300,1000,0.12)
sfx=out/np.max(np.abs(out))
raw=subprocess.run(["ffmpeg","-v","error","-i","vo/vo9.mp3","-f","f32le","-ac","1","-ar",str(SR),"-"],capture_output=True).stdout
vo=np.frombuffer(raw,dtype=np.float32).astype(np.float64)
voice=np.zeros(N); voice[:min(N,len(vo))]=vo[:N]; voice=voice/np.max(np.abs(voice))*0.95
w=int(0.05*SR); e=np.sqrt(np.convolve(voice**2,np.ones(w)/w,mode="same"))
on=(e>0.02).astype(float); k=int(0.25*SR); on=np.clip(np.convolve(on,np.ones(k)/k,mode="same")*1.5,0,1)
mix=voice+sfx*0.42*(1-0.6*on); mix=mix/np.max(np.abs(mix))*0.95
fade=np.ones(N); fade[-int(0.5*SR):]=np.linspace(1,0,int(0.5*SR)); mix*=fade
with wave.open('audio9_vo.wav','wb') as wv:
    wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((mix*32767).astype(np.int16).tobytes())
print("ok")
