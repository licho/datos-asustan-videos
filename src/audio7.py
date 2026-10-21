import numpy as np, wave, subprocess
from warp7 import T_of_v as M, DUR
SR=44100; N=int(SR*DUR); out=np.zeros(N); rng=np.random.default_rng(7)
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
def span(a,b): return M(b)-M(a)
# light curious music loop (plucky)
notes=[392,0,466,392,523,0,466,392,349,0,392,349,311,0,349,392]
for k,b in enumerate(np.arange(0.2,DUR-1,0.25)):
    f=notes[k%16]
    if f: add(b,(tone(f,0.25)+0.3*tone(f*2,0.25))*env(int(0.25*SR),0.002,0.06),0.09,raw=True)
    if k%4==0: add(b, tone(98,0.35)*env(int(0.35*SR),0.003,0.12),0.15,raw=True)
for k in range(3): add(0.1+k*0.5, tone(1200,0.08)*env(int(0.08*SR),0.002,0.03),0.12)
for i in range(4): popsnd(2.5+i*0.1,0.18,300,800,0.08)
add(5.0, lp(noise(1.6),0.15)*np.sin(np.linspace(0,np.pi,int(1.6*SR)))**0.5,0.6)
for i in range(10): popsnd(5.4+i*0.15,0.08,900,1500,0.05)
for i in range(6): popsnd(8.5+i*0.08,0.15,400,900,0.06)
for k in range(3): add(9.5+k*0.18, tone(880,0.12,'sq')*env(int(0.12*SR),0.002,0.08),0.1)
boing(11.5,0.35)
whoosh(13.0); popsnd(13.6,0.35,200,1200,0.25)
add(14.5, lp(tone(np.linspace(300,500,int(0.6*SR)),0.6,'saw'),0.25)*env(int(0.6*SR),0.01,0.4),0.15)
whoosh(17.0); add(17.0, tone(np.linspace(300,1500,int(0.6*SR)),0.6)*env(int(0.6*SR),0.02,0.4),0.1)
whoosh(20.0)
for st in (20.5,23.0,27.0,35.0,41.0): ding(st)
add(21.1, tone(np.linspace(800,100,int(0.5*SR)),0.5)*env(int(0.5*SR),0.002,0.3),0.2); popsnd(21.7,0.25,900,300,0.1)
for i in range(14): popsnd(23.3+i*0.25,0.07,rng.uniform(600,900),rng.uniform(1200,1700),0.05)
for k in range(3): add(27.6+k*1.3, lp(noise(0.4),0.15)*np.sin(np.linspace(0,np.pi,int(0.4*SR))),0.35)
buzzer(28.5); ding(31.0,0.25,2093)
d=span(35.2,37.3); add(35.2, lp(noise(d),0.4)*(0.5+0.5*np.abs(np.sin(np.linspace(0,30,int(d*SR))))),0.1)
buzzer(37.5); buzzer(41.5,0.35); boing(43.5,0.35); boing(43.9,0.25)
popsnd(47.0,0.3,200,600,0.3)
sfx=out/np.max(np.abs(out))
raw=subprocess.run(["ffmpeg","-v","error","-i","vo/vo7.mp3","-f","f32le","-ac","1","-ar",str(SR),"-"],capture_output=True).stdout
vo=np.frombuffer(raw,dtype=np.float32).astype(np.float64)
voice=np.zeros(N); voice[:min(N,len(vo))]=vo[:N]; voice=voice/np.max(np.abs(voice))*0.95
w=int(0.05*SR); e=np.sqrt(np.convolve(voice**2,np.ones(w)/w,mode="same"))
on=(e>0.02).astype(float); k=int(0.25*SR); on=np.clip(np.convolve(on,np.ones(k)/k,mode="same")*1.5,0,1)
mix=voice+sfx*0.42*(1-0.6*on); mix=mix/np.max(np.abs(mix))*0.95
fade=np.ones(N); fade[-int(0.4*SR):]=np.linspace(1,0,int(0.4*SR)); mix*=fade
with wave.open('audio7_vo.wav','wb') as wv:
    wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((mix*32767).astype(np.int16).tobytes())
print("ok")
