import numpy as np, wave, subprocess
from warp2 import T_of_v as M, DUR, GAP_AT, GAP
SR=44100; N=int(SR*DUR); out=np.zeros(N); rng=np.random.default_rng(2)
t=np.arange(N)/SR
def add(start, sig, g=1.0, raw=False):
    i=int((start if raw else M(start))*SR); j=min(N,i+len(sig))
    if i<N: out[i:j]+=sig[:j-i]*g
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
def squish(st,g=0.4):
    n=lp(noise(0.25),0.12)*env(int(0.25*SR),0.01,0.08); add(st,n,g); popsnd(st,0.25,500,180,0.18)
def ding(st,g=0.18,f=1568): add(st,(tone(f,0.4)+0.5*tone(f*1.335,0.4))*env(int(0.4*SR),0.002,0.12),g)
def whoosh(st): n=lp(noise(0.35),0.08)*np.sin(np.linspace(0,np.pi,int(0.35*SR))); add(st-0.15,n,0.55)
# creepy drone 0 .. M(52), and quieter after
for b in np.arange(0, M(52), 0.8):
    f=[55,55,58.27,52][int(b/0.8)%4]
    s=lp(tone(f,0.75,'saw'),0.04)*env(int(0.75*SR),0.02,0.3); add(b,s,0.3,raw=True)
pad=lp(tone(220,DUR,'saw')+tone(233.08,DUR,'saw'),0.02)*0.15
padmask=np.clip(np.minimum(t/2,1),0,1)*(t<M(52)); out+=pad*padmask*0.25
# s1 germ pops in lens
for k in range(9): popsnd(0.9+k*0.28,0.18,400,1100,0.08)
# scene whooshes
for st in (5,13,19,26,34,38,52): whoosh(st)
# s2 keyboards appear ticks
for i in range(30): add(5.1+i*0.06, tone(1200,0.03)*env(int(0.03*SR),0.001,0.01), 0.12)
for k in range(4): add(8.0+k*0.18, tone(880,0.12,'sq')*env(int(0.12*SR),0.002,0.08), 0.12)
whoosh(9.3)
add(10.7, tone(np.linspace(140,45,int(0.4*SR)),0.4)*env(int(0.4*SR),0.002,0.1),1.0); add(10.7,lp(noise(0.3),0.1)*env(int(0.3*SR),0.002,0.06),0.7)
# s3 counter ticks + ding
a,b=M(13.4),M(16.0)
for tt in np.arange(a,b,0.06): add(tt, tone(2000,0.02)*env(int(0.02*SR),0.001,0.006),0.1,raw=True)
ding(16.0,0.3,1318)
# s4 squish germs
for st in (20.5,22.0,23.5): squish(st,0.5)
# s5 cards
for st in (27.5,29.5,31.5): popsnd(st,0.35,250,800,0.12)
# s6
for i in range(10): popsnd(34.2+i*0.08,0.12,500,900,0.05)
add(35.6, lp(tone(140,0.4,'sq'),0.3)*env(int(0.4*SR),0.005,0.25),0.3)
# s7 tutorial
for st in (38.8,41.0,43.5,46.0,49.5): ding(st,0.22,1568)
add(39.3, noise(0.04)*env(int(0.04*SR),0.001,0.01),0.5); popsnd(39.3,0.3,900,300,0.1)
for k in range(10): add(41.4+k*0.16, lp(noise(0.1),0.3)*env(int(0.1*SR),0.002,0.04),0.25)
for k in range(25): add(41.6+k*0.06, tone(rng.uniform(2500,4500),0.02)*env(int(0.02*SR),0.001,0.008),0.06)
hd=M(46.0)-M(43.6); hs=lp(noise(hd),0.6)*(0.5+0.5*np.abs(np.sin(np.linspace(0,9,int(hd*SR))))); add(43.6,hs,0.12)
for k in range(5): add(46.2+k*0.65, lp(noise(0.35),0.15)*np.sin(np.linspace(0,np.pi,int(0.35*SR))),0.35)
for k in range(14): popsnd(49.6+k*0.17, 0.1, rng.uniform(600,900), rng.uniform(1200,1800), 0.05)
ding(50.4,0.2,2093)
# s8 twist: phone buzz + sting
for k in range(2):
    d_=0.35; bz=lp(tone(160,d_,'sq'),0.2)*(0.6+0.4*np.sign(np.sin(2*np.pi*30*np.arange(int(d_*SR))/SR)))*env(int(d_*SR),0.005)
    add(54.5+k*0.5, bz, 0.25)
st=sum(tone(f,2.2,'saw') for f in (55,58.3,110.4,116.7,164.8)); add(54.5, lp(st,0.08)*env(int(2.2*SR),0.01,0.9),0.35)
add(54.5, lp(noise(1.0),0.3)*env(int(1.0*SR),0.005,0.2),0.3)
# s9
popsnd(57.0,0.25,200,600,0.3)
for bb in np.arange(M(57.4),DUR-0.3,0.5): add(bb, tone(np.linspace(80,40,int(0.12*SR)),0.12)*env(int(0.12*SR),0.002,0.05),0.4,raw=True)
sfx=out/np.max(np.abs(out))
raw=subprocess.run(["ffmpeg","-v","error","-i","vo/vo2.mp3","-f","f32le","-ac","1","-ar",str(SR),"-"],capture_output=True).stdout
vo=np.frombuffer(raw,dtype=np.float32).astype(np.float64)
g=int(GAP_AT*SR); vo=np.concatenate([vo[:g],np.zeros(int(GAP*SR)),vo[g:]])
voice=np.zeros(N); voice[:min(N,len(vo))]=vo[:N]; voice=voice/np.max(np.abs(voice))*0.95
w=int(0.05*SR); e=np.sqrt(np.convolve(voice**2,np.ones(w)/w,mode="same"))
on=(e>0.02).astype(float); k=int(0.25*SR); on=np.clip(np.convolve(on,np.ones(k)/k,mode="same")*1.5,0,1)
mix=voice+sfx*0.42*(1-0.6*on); mix=mix/np.max(np.abs(mix))*0.95
fade=np.ones(N); fade[-int(0.4*SR):]=np.linspace(1,0,int(0.4*SR)); mix*=fade
with wave.open('audio2_vo.wav','wb') as wv:
    wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((mix*32767).astype(np.int16).tobytes())
print("ok")
