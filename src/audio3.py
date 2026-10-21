import numpy as np, wave, subprocess
from warp3 import T_of_v as M, DUR, GAP_AT, GAP
SR=44100; N=int(SR*DUR); out=np.zeros(N); rng=np.random.default_rng(3); t=np.arange(N)/SR
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
def whoosh(st,g=0.55): n=lp(noise(0.35),0.08)*np.sin(np.linspace(0,np.pi,int(0.35*SR))); add(st-0.15,n,g)
def buzzer(st): add(st, lp(tone(140,0.35,'sq'),0.3)*env(int(0.35*SR),0.005,0.2),0.3)
def sting(st,g=0.4,d=2.4):
    s=sum(tone(f,d,'saw') for f in (41.2,43.7,82.4,87.3,123.5)); add(st, lp(s,0.07)*env(int(d*SR),0.01,0.9),g)
    add(st, lp(noise(1.2),0.25)*env(int(1.2*SR),0.005,0.3),0.3)
# ocean: slow-modulated lowpassed noise until twist
sea_end=M(41)
oc=lp(rng.standard_normal(int(sea_end*SR)),0.02)
oc*=0.6+0.4*np.sin(2*np.pi*0.12*np.arange(len(oc))/SR)
out[:len(oc)]+=oc*0.9
# drone
for b in np.arange(0, DUR-3, 1.0):
    f=[49,49,46.25,51.9][int(b)%4]
    add(b, lp(tone(f,0.95,'saw'),0.035)*env(int(0.95*SR),0.03,0.45),0.32,raw=True)
# bubbles + rumble + reveal
for k in range(22): popsnd(2.6+k*0.15, 0.12, rng.uniform(300,500), rng.uniform(700,1200), 0.06)
rd=M(6.0)-M(3.8); add(3.8, lp(noise(rd),0.02)*np.linspace(0,1,int(rd*SR)), 0.9)
sting(6.0,0.45)
add(6.0, lp(tone(np.linspace(90,60,int(1.5*SR)),1.5,'saw'),0.05)*env(int(1.5*SR),0.05,0.6),0.4)
for st in (9.0,16.0,41.0,52.0): whoosh(st)
# underwater hum s3
hd=M(16)-M(9); add(9.0, lp(tone(65,hd,'saw'),0.02)*np.sin(np.linspace(0,np.pi,int(hd*SR))),0.25)
popsnd(13.0,0.2,150,90,0.4)
# steps
for st in (16.5,20.5,24.5,28.5,35.5): ding(st,0.22)
buzzer(17.1); buzzer(21.5)
sh=lp(noise(0.6),0.9)-lp(noise(0.6),0.2); add(22.3, sh*env(int(0.6*SR),0.05,0.3), 0.25)
popsnd(25.5,0.3,250,700,0.12)
ed=M(30.5)-M(28.6); add(28.6, lp(tone(np.linspace(70,140,int(ed*SR)),ed,'saw'),0.15)*np.linspace(0.3,1,int(ed*SR)),0.25)
add(30.5, lp(noise(1.0),0.35)*env(int(1.0*SR),0.002,0.3), 0.9)
add(30.5, tone(np.linspace(120,40,int(0.5*SR)),0.5)*env(int(0.5*SR),0.002,0.12), 0.8)
for k in range(10): popsnd(32.4+k*0.17, 0.18, 500, 160, 0.14)
fd=M(37.3)-M(35.6); add(35.6, lp(tone(np.linspace(120,180,int(fd*SR)),fd,'saw'),0.15)*np.linspace(1,0.4,int(fd*SR)),0.22)
popsnd(37.3,0.3,200,700,0.15)
# twist: eye opens
sting(47.2,0.55,3.0)
add(47.2, lp(tone(np.linspace(70,45,int(2*SR)),2.0,'saw')*(1+0.3*np.sin(2*np.pi*18*np.arange(int(2*SR))/SR)),0.06)*env(int(2*SR),0.03,0.8),0.45)
# CTA
popsnd(52.0,0.25,200,600,0.3)
for bb in np.arange(M(52.4),DUR-0.4,0.5): add(bb, tone(np.linspace(80,40,int(0.12*SR)),0.12)*env(int(0.12*SR),0.002,0.05),0.4,raw=True)
sfx=out/np.max(np.abs(out))
raw=subprocess.run(["ffmpeg","-v","error","-i","vo/vo3.mp3","-f","f32le","-ac","1","-ar",str(SR),"-"],capture_output=True).stdout
vo=np.frombuffer(raw,dtype=np.float32).astype(np.float64)
g=int(GAP_AT*SR); vo=np.concatenate([vo[:g],np.zeros(int(GAP*SR)),vo[g:]])
voice=np.zeros(N); voice[:min(N,len(vo))]=vo[:N]; voice=voice/np.max(np.abs(voice))*0.95
w=int(0.05*SR); e=np.sqrt(np.convolve(voice**2,np.ones(w)/w,mode="same"))
on=(e>0.02).astype(float); k=int(0.25*SR); on=np.clip(np.convolve(on,np.ones(k)/k,mode="same")*1.5,0,1)
mix=voice+sfx*0.42*(1-0.6*on); mix=mix/np.max(np.abs(mix))*0.95
fade=np.ones(N); fade[-int(0.4*SR):]=np.linspace(1,0,int(0.4*SR)); mix*=fade
with wave.open('audio3_vo.wav','wb') as wv:
    wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((mix*32767).astype(np.int16).tobytes())
print("ok")
