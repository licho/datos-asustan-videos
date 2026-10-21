import numpy as np, wave, subprocess
from warp5 import T_of_v as M, DUR
SR=44100; N=int(SR*DUR); out=np.zeros(N); rng=np.random.default_rng(5)
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
def popsnd(st,g=0.3,f0=300,f1=900,d=0.1): add(st, tone(np.linspace(f0,f1,int(d*SR)),d)*env(int(d*SR),0.002,d/2), g)
def ding(st,g=0.2,f=1318): add(st,(tone(f,0.4)+0.5*tone(f*1.335,0.4))*env(int(0.4*SR),0.002,0.12),g)
def whoosh(st,g=0.5): n=lp(noise(0.35),0.08)*np.sin(np.linspace(0,np.pi,int(0.35*SR))); add(st-0.15,n,g)
def buzzer(st): add(st, lp(tone(140,0.35,'sq'),0.3)*env(int(0.35*SR),0.005,0.2),0.3)
def span(a,b): return M(b)-M(a)
# night pad + ticking clock
pad=lp(tone(110,DUR,'saw')+tone(130.8,DUR,'saw')+tone(164.8,DUR,'saw'),0.015); out+=pad*0.12
for b in np.arange(0.0, DUR-0.5, 1.0): add(b, lp(noise(0.02),0.6)*env(int(0.02*SR),0.001,0.005),0.25,raw=True)
# zoom
add(2.0, tone(np.linspace(300,1500,int(0.7*SR)),0.7)*env(int(0.7*SR),0.02,0.5),0.12)
# chewing
for k in range(12): add(5.2+k*0.24, lp(noise(0.06),0.5)*env(int(0.06*SR),0.002,0.02),0.3)
# pellets plop
for i in range(20): popsnd(8.0+i/8,0.18,500,120,0.08)
popsnd(8.2,0.3,300,900,0.15)
# sneeze
add(11.4, lp(noise(0.6),0.6)*env(int(0.6*SR),0.01,0.15),0.8); add(11.2, tone(np.linspace(400,700,int(0.25*SR)),0.25,'saw')*env(int(0.25*SR),0.05,0.2),0.08)
# humidity beeps
for k in range(4): add(14.2+k*0.35, tone(1800,0.08)*env(int(0.08*SR),0.002,0.04),0.12)
for st in (5.0,14.0,19.0,43.0): whoosh(st)
for st in (20.0,24.5,29.0,33.5,37.5): ding(st,0.2)
# washer
d=span(20.0,24.4); add(20.0, lp(noise(d),0.05)*(0.6+0.4*np.sin(2*np.pi*3*np.arange(int(d*SR))/SR)),0.35)
# zipper
add(25.0, lp(noise(0.5),0.7)*(0.5+0.5*np.sign(np.sin(2*np.pi*40*np.arange(int(0.5*SR))/SR))),0.12)
# dehumidifier hum
d=span(29.0,33.4); add(29.0, lp(tone(120,d,'saw'),0.05)*np.sin(np.linspace(0,np.pi,int(d*SR)))**0.2,0.18)
# vacuum
d=span(33.5,37.4); add(33.5, (lp(noise(d),0.3)+0.3*tone(220,d,'saw'))*np.sin(np.linspace(0,np.pi,int(d*SR)))**0.2,0.18)
# birds + ay
for k in range(6): add(37.7+k*0.4, tone(np.linspace(2500,3500,int(0.08*SR)),0.08)*env(int(0.08*SR),0.002,0.03),0.08)
for k in range(4): popsnd(38.3+k*0.15,0.2,1400,700,0.1)
# creepy eyes
s=sum(tone(f,2.0,'saw') for f in (55,58.3,110.4)); add(43.5, lp(s,0.06)*env(int(2.0*SR),0.05,0.8),0.35)
sfx=out/np.max(np.abs(out))
raw=subprocess.run(["ffmpeg","-v","error","-i","vo/vo5.mp3","-f","f32le","-ac","1","-ar",str(SR),"-"],capture_output=True).stdout
vo=np.frombuffer(raw,dtype=np.float32).astype(np.float64)
voice=np.zeros(N); voice[:min(N,len(vo))]=vo[:N]; voice=voice/np.max(np.abs(voice))*0.95
w=int(0.05*SR); e=np.sqrt(np.convolve(voice**2,np.ones(w)/w,mode="same"))
on=(e>0.02).astype(float); k=int(0.25*SR); on=np.clip(np.convolve(on,np.ones(k)/k,mode="same")*1.5,0,1)
mix=voice+sfx*0.42*(1-0.6*on); mix=mix/np.max(np.abs(mix))*0.95
fade=np.ones(N); fade[-int(0.4*SR):]=np.linspace(1,0,int(0.4*SR)); mix*=fade
with wave.open('audio5_vo.wav','wb') as wv:
    wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((mix*32767).astype(np.int16).tobytes())
print("ok")
