import numpy as np, wave, subprocess
from warp22 import T_of_v as M, DUR
SR=44100; N=int(SR*DUR); out=np.zeros(N); rng=np.random.default_rng(11)
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
def sq(f,dd,duty=0.5):
    n=int(dd*SR); ph=(np.arange(n)*f/SR)%1.0
    return np.where(ph<duty,1.0,-1.0)*np.exp(-np.arange(n)/SR/(dd*0.9))
import warp22
bpm=140; step=60/bpm/2
mel=[330,0,392,0,440,392,330,0,294,0,349,0,392,349,330,0]
bass=[82.4,82.4,98,98,73.4,73.4,87.3,87.3]
for k,st in enumerate(np.arange(0,DUR-1,step)):
    v=warp22.v_of_T(st); g=0.8 if v>=62 else 0.55
    if 55.4<=v<57: continue
    f=mel[k%16]
    if f and k%32<28: add(st, sq(f*2,step*0.8,0.25), 0.05*g, raw=True)
    if k%2==0: add(st, sq(bass[(k//2)%8],step*1.8,0.5), 0.10*g, raw=True)
    if k%4==0: add(st, np.sin(2*np.pi*np.cumsum(np.linspace(150,40,int(0.1*SR)))/SR)*np.exp(-np.arange(int(0.1*SR))/SR/0.04), 0.3*g, raw=True)
    if k%4==2: add(st, lp(noise(0.04),0.6)*np.exp(-np.arange(int(0.04*SR))/SR/0.01), 0.12*g, raw=True)
def blip(st,g=0.25):
    add(st, sq(988,0.06,0.25),g); add(M(st)+0.06, sq(1319,0.1,0.25), g, raw=True)
def buzz(a,b,g=0.05):
    t0=M(a); t1=M(b); n=int((t1-t0)*SR); tt=np.arange(n)/SR
    f=220+30*np.sin(2*np.pi*7*tt); s=np.sign(np.sin(2*np.pi*np.cumsum(f)/SR))*(0.6+0.4*np.sin(2*np.pi*3*tt))
    add(t0, lp(s,0.25), g, raw=True)
# podadora
t0=M(0.3); t1=M(6.3); n=int((t1-t0)*SR); add(t0, lp(np.sign(np.sin(2*np.pi*55*np.arange(n)/SR)),0.1)*0.6, 0.12, raw=True)
buzz(6.0,13.0,0.09); buzz(44,57,0.07); buzz(57,64,0.07)
for st in (14.0,19.5,24.5,29.5,34.5,39.5): blip(st)
for st in (10.0,13.0,44.0,50.0,54.0,57.0,62.0,68.0): whoosh(st,0.35)
buzzer(2.6,0.3); buzzer(45.2,0.4); buzzer(51.0,0.4)
for k,f in enumerate([392,370,349,330,262]): add(M(55.4)+k*0.25, sq(f,0.24,0.5), 0.12, raw=True)
thud(63.2,0.6)
for k,f in enumerate([523,659,784,1047]): add(M(63.3)+k*0.1, sq(f,0.15,0.5), 0.15, raw=True)
for k,f in enumerate([523,659,784,1047]): add(M(68.2)+k*0.12, sq(f,0.18,0.5), 0.18, raw=True)
sfx=out/np.max(np.abs(out))
raw=subprocess.run(["ffmpeg","-v","error","-i","vo/vo22.mp3","-f","f32le","-ac","1","-ar",str(SR),"-"],capture_output=True).stdout
vo=np.frombuffer(raw,dtype=np.float32).astype(np.float64)
voice=np.zeros(N); voice[:min(N,len(vo))]=vo[:N]; voice=voice/np.max(np.abs(voice))*0.95
w=int(0.05*SR); e=np.sqrt(np.convolve(voice**2,np.ones(w)/w,mode="same"))
on=(e>0.02).astype(float); k=int(0.25*SR); on=np.clip(np.convolve(on,np.ones(k)/k,mode="same")*1.5,0,1)
mix=voice+sfx*0.42*(1-0.6*on); mix=mix/np.max(np.abs(mix))*0.95
fade=np.ones(N); fade[-int(0.5*SR):]=np.linspace(1,0,int(0.5*SR)); mix*=fade
with wave.open('audio22_vo.wav','wb') as wv:
    wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((mix*32767).astype(np.int16).tobytes())
print("ok")
