import numpy as np, wave, subprocess
from warp8 import T_of_v as M, DUR
SR=44100; N=int(SR*DUR); out=np.zeros(N); rng=np.random.default_rng(8)
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
# hum + drone like part 1 (until climax)
t=np.arange(N)/SR; vt=np.interp(t, __import__('warp8').TK, __import__('warp8').VK)
hum=(0.5*np.sin(2*np.pi*120*t)+0.25*np.sin(2*np.pi*240*t)); out+=hum*0.03*(vt<46)
for b in np.arange(0, M(46), 60/100):
    f=55 if int(b/(60/100))%8<6 else 52
    add(b, lp(tone(f,0.5,'saw'),0.05)*env(int(0.5*SR),0.01,0.18),0.3,raw=True)
sting(0.0,0.35,1.6); add(0.5, lp(tone(np.linspace(180,120,int(0.8*SR)),0.8,'saw'),0.1)*env(int(0.8*SR),0.05,0.5),0.15)
whoosh(3.5); thud(5.3); add(5.0, tone(np.linspace(300,250,int(0.5*SR)),0.5,'sq')*env(int(0.5*SR),0.01,0.3),0.08)
for st in (8.0,17.0,33.0,46.0,56.0): whoosh(st)
for i in range(6): popsnd(8.4+i*0.1,0.15,400,900,0.06)
add(12.0, lp(tone(np.linspace(110,80,int(1.0*SR)),1.0,'saw')*(1+0.2*np.sin(np.linspace(0,40,int(1.0*SR)))),0.08)*env(int(1.0*SR),0.05,0.5),0.3)
boing(13.5,0.35)
for i in range(4): ding(18.2+i*0.1,0.12,1568)
for st in (20.2,21.6,23.2): popsnd(st,0.3,250,800,0.12)
buzzer(26.3)
add(27.5, lp(noise(0.8),0.05)*(0.5+0.5*np.sin(np.linspace(0,50,int(0.8*SR)))),0.4)
d=span(33.2,36.5); add(33.2, lp(noise(d),0.5)*(0.4+0.6*np.abs(np.sin(np.linspace(0,25,int(d*SR))))),0.06)
for k in range(30): popsnd(37.2+k*0.12,0.05,rng.uniform(300,500),rng.uniform(700,1000),0.05)
d=span(41.0,45.5); ch=sum(tone(f,d) for f in (220,277.2,329.6,415.3)); add(41.0, ch*np.sin(np.linspace(0,np.pi,int(d*SR)))*0.25,0.25)
add(47.5, lp(tone(np.linspace(180,120,int(1.2*SR)),1.2,'saw'),0.1)*env(int(1.2*SR),0.05,0.8),0.2)
sting(47.5,0.25,1.5); boing(50.0,0.35)
for k,f in enumerate([392,370,349,330]): add(51.0+k*0.35, lp(tone(f*(1+0.02*np.sin(np.linspace(0,40,int(0.35*SR)))),0.35,'saw'),0.2)*env(int(0.35*SR),0.01,0.3),0.18)
for k in range(14): add(56.4+k*0.33, lp(noise(0.08),0.2)*env(int(0.08*SR),0.002,0.03),0.3)
d=3.0; ch=sum(tone(f,d) for f in (523.25,659.25,783.99,1046.5)); add(61.0, ch*np.sin(np.linspace(0,np.pi,int(d*SR)))*0.3,0.3)
thud(63.2,0.9); sting(63.2,0.35,2.5)
sfx=out/np.max(np.abs(out))
raw=subprocess.run(["ffmpeg","-v","error","-i","vo/vo8.mp3","-f","f32le","-ac","1","-ar",str(SR),"-"],capture_output=True).stdout
vo=np.frombuffer(raw,dtype=np.float32).astype(np.float64)
voice=np.zeros(N); voice[:min(N,len(vo))]=vo[:N]; voice=voice/np.max(np.abs(voice))*0.95
w=int(0.05*SR); e=np.sqrt(np.convolve(voice**2,np.ones(w)/w,mode="same"))
on=(e>0.02).astype(float); k=int(0.25*SR); on=np.clip(np.convolve(on,np.ones(k)/k,mode="same")*1.5,0,1)
mix=voice+sfx*0.42*(1-0.6*on); mix=mix/np.max(np.abs(mix))*0.95
fade=np.ones(N); fade[-int(0.5*SR):]=np.linspace(1,0,int(0.5*SR)); mix*=fade
with wave.open('audio8_vo.wav','wb') as wv:
    wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((mix*32767).astype(np.int16).tobytes())
print("ok")
