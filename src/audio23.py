import numpy as np, wave, subprocess
from warp23 import T_of_v as M, DUR
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
import warp23
# pad espacial: acordes lentos
chords=[(110,164.8,220,261.6),(98,146.8,196,246.9),(87.3,130.8,174.6,220),(98,146.8,196,233.1)]
seg=4.0
for k,st in enumerate(np.arange(0,DUR,seg)):
    n=int((seg+1.5)*SR); tt=np.arange(n)/SR
    e=np.minimum(1,tt/1.2)*np.minimum(1,(seg+1.5-tt)/1.5)
    sig=sum(np.sin(2*np.pi*f*tt)*(0.5 if i==0 else 0.3) for i,f in enumerate(chords[k%4]))
    sig+=0.15*np.sin(2*np.pi*chords[k%4][3]*2*tt)*np.sin(2*np.pi*0.3*tt)
    add(st, sig*e, 0.09, raw=True)
for st in (5.0,12.0,22.0,31.0,40.0,45.0,48.5,56.0): whoosh(st,0.4)
for st in (5.6,12.8,22.6,48.5): thud(st,0.6)
for st in (8.5,10.3,15.0,37.0,42.0): ding(st,0.18)
for k in range(11): popsnd(8.5+k*0.15*1.0,0.08,600,900,0.05)
for k,st in enumerate((27.5,28.6,29.6,30.4)): popsnd(st,0.2,300,120,0.12)
buzzer(18.0,0.15)
add(M(52.2), tone(880,0.12,'sin')*env(int(0.12*SR),0.002,0.05), 0.2, raw=True)
sfx=out/np.max(np.abs(out))
raw=subprocess.run(["ffmpeg","-v","error","-i","vo/vo23.mp3","-f","f32le","-ac","1","-ar",str(SR),"-"],capture_output=True).stdout
vo=np.frombuffer(raw,dtype=np.float32).astype(np.float64)
voice=np.zeros(N); voice[:min(N,len(vo))]=vo[:N]; voice=voice/np.max(np.abs(voice))*0.95
w=int(0.05*SR); e=np.sqrt(np.convolve(voice**2,np.ones(w)/w,mode="same"))
on=(e>0.02).astype(float); k=int(0.25*SR); on=np.clip(np.convolve(on,np.ones(k)/k,mode="same")*1.5,0,1)
mix=voice+sfx*0.42*(1-0.6*on); mix=mix/np.max(np.abs(mix))*0.95
fade=np.ones(N); fade[-int(0.5*SR):]=np.linspace(1,0,int(0.5*SR)); mix*=fade
with wave.open('audio23_vo.wav','wb') as wv:
    wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((mix*32767).astype(np.int16).tobytes())
print("ok")
