import numpy as np, wave, subprocess
from warp14 import T_of_v as M, DUR
SR=44100; N=int(SR*DUR); out=np.zeros(N); rng=np.random.default_rng(14)
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
# spooky waltz organ-ish bass
for b in np.arange(0, DUR-1, 60/120):
    k=int(b/(60/120)); f=[73.4,73.4,69.3,65.4][(k//3)%4]*(1 if k%3==0 else 2)
    add(b, lp(tone(f,0.35,'saw'),0.06)*env(int(0.35*SR),0.005,0.12),0.2 if k%3==0 else 0.08,raw=True)
sting(0.0,0.3,1.6)
for st in (3.0,9.0,17.0,27.0,36.0,45.0,50.0,60.0): whoosh(st,0.4)
for k in range(5): add(M(3.3)+[0.0,0.7,1.7,3.0,3.4][k]*2, tone(900,0.05)*env(int(0.05*SR),0.001,0.02),0.15,raw=True)
for st in (9.0,17.0,27.0,36.0): ding(st+0.15,0.2,1318); ding(st+0.3,0.2,1760)
add(M(13.0), lp(tone(np.linspace(200,90,int(0.6*SR)),0.6,'saw'),0.1)*env(int(0.6*SR),0.01,0.3),0.2,raw=True)
popsnd(14.6,0.3,300,900,0.12)
for st in (18.5,19.6,20.8): ding(st,0.15,1568)
popsnd(23.0,0.25,400,800,0.1); thud(24.5,0.7)
popsnd(28.0,0.3,300,1100,0.12); boing(30.0,0.3); buzzer(30.4)
for k in range(8): popsnd(36.5+k*0.5,0.06,500+k*60,900+k*60,0.06)
d=1.2; add(41.0, tone(np.linspace(800,120,int(d*SR)),d,'sq')*env(int(d*SR),0.005,0.6),0.12); thud(41.0,0.6)
for st in (45.3,46.4,47.6): buzzer(st,0.18)
thud(55.0,0.7); buzzer(55.1,0.25)
d=2.5; ch=sum(tone(f,d) for f in (293.7,349.2,440.0,587.3)); add(60.0, ch*np.sin(np.linspace(0,np.pi,int(d*SR)))*0.3,0.22)
sfx=out/np.max(np.abs(out))
raw=subprocess.run(["ffmpeg","-v","error","-i","vo/vo14.mp3","-f","f32le","-ac","1","-ar",str(SR),"-"],capture_output=True).stdout
vo=np.frombuffer(raw,dtype=np.float32).astype(np.float64)
voice=np.zeros(N); voice[:min(N,len(vo))]=vo[:N]; voice=voice/np.max(np.abs(voice))*0.95
w=int(0.05*SR); e=np.sqrt(np.convolve(voice**2,np.ones(w)/w,mode="same"))
on=(e>0.02).astype(float); k=int(0.25*SR); on=np.clip(np.convolve(on,np.ones(k)/k,mode="same")*1.5,0,1)
mix=voice+sfx*0.42*(1-0.6*on); mix=mix/np.max(np.abs(mix))*0.95
fade=np.ones(N); fade[-int(0.5*SR):]=np.linspace(1,0,int(0.5*SR)); mix*=fade
with wave.open('audio14_vo.wav','wb') as wv:
    wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((mix*32767).astype(np.int16).tobytes())
print("ok")
