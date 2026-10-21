import numpy as np, wave, subprocess
from warp13 import T_of_v as M, DUR
SR=44100; N=int(SR*DUR); out=np.zeros(N); rng=np.random.default_rng(13)
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
for b in np.arange(0, DUR-1, 60/90):
    k=int(b/(60/90)); f=[55,55,65.4,49][(k//4)%4]
    add(b, lp(tone(f,0.6,'saw'),0.04)*env(int(0.6*SR),0.01,0.25),0.22,raw=True)
sting(0.0,0.35,1.8); add(0.2, lp(noise(2.5),0.03)*np.linspace(0.2,1,int(2.5*SR)),0.25,raw=True)
buzzer(2.6)
for st in (5.0,10.0,17.0,24.0,31.0,38.0,44.0,50.0,58.0): whoosh(st,0.4)
add(M(6.0), lp(noise(1.6),0.04)*np.linspace(0.1,1,int(1.6*SR)),0.25,raw=True)
thud(8.0,1.0); add(M(8.0), lp(noise(0.8),0.1)*env(int(0.8*SR),0.002,0.3),0.6,raw=True)
add(M(10.0), lp(noise(2.5),0.04)*np.linspace(0.2,1,int(2.5*SR)),0.2,raw=True)
d=span(14,14.6); add(14, tone(np.linspace(800,2400,int(d*SR)),d)*np.linspace(0.2,1,int(d*SR)),0.12)
thud(15.6,1.0); add(M(15.6), lp(noise(1.2),0.12)*env(int(1.2*SR),0.002,0.5),0.7,raw=True)
popsnd(17.0,0.3,300,900,0.12)
for k in range(16): add(M(21.1)+k*0.04, (tone(rng.uniform(2500,5000),0.15)*env(int(0.15*SR),0.001,0.04)),0.2,raw=True)
add(M(21.1), lp(noise(0.5),0.4)*env(int(0.5*SR),0.001,0.15),0.5,raw=True)
sting(24.0,0.3,2.2); boing(27.6,0.35)
popsnd(33.2,0.3,500,200,0.15)
ding(35.1,0.2,1318); ding(35.6,0.2,880)
for k in range(10): popsnd(38.6+k*0.2,0.08,700,1300,0.05)
ding(39.0,0.25,1568)
buzzer(47.3)
add(M(50.3), lp(noise(1.5),0.05)*np.linspace(0.1,1,int(1.5*SR)),0.2,raw=True)
thud(52.2,0.9)
d=3.0; ch=sum(tone(f,d) for f in (523.25,659.25,783.99,1046.5)); add(55.0, ch*np.sin(np.linspace(0,np.pi,int(d*SR)))*0.3,0.25)
boing(58.5,0.3); popsnd(61.0,0.3,300,1000,0.12)
sfx=out/np.max(np.abs(out))
raw=subprocess.run(["ffmpeg","-v","error","-i","vo/vo13.mp3","-f","f32le","-ac","1","-ar",str(SR),"-"],capture_output=True).stdout
vo=np.frombuffer(raw,dtype=np.float32).astype(np.float64)
voice=np.zeros(N); voice[:min(N,len(vo))]=vo[:N]; voice=voice/np.max(np.abs(voice))*0.95
w=int(0.05*SR); e=np.sqrt(np.convolve(voice**2,np.ones(w)/w,mode="same"))
on=(e>0.02).astype(float); k=int(0.25*SR); on=np.clip(np.convolve(on,np.ones(k)/k,mode="same")*1.5,0,1)
mix=voice+sfx*0.42*(1-0.6*on); mix=mix/np.max(np.abs(mix))*0.95
fade=np.ones(N); fade[-int(0.5*SR):]=np.linspace(1,0,int(0.5*SR)); mix*=fade
with wave.open('audio13_vo.wav','wb') as wv:
    wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((mix*32767).astype(np.int16).tobytes())
print("ok")
