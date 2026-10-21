import numpy as np, wave
from warp import T_of_v as M, v_of_T, DUR, GAP_AT, GAP
import subprocess
SR=44100; N=int(SR*DUR)
out=np.zeros(N); rng=np.random.default_rng(1)
t=np.arange(N)/SR
def add(start, sig, g=1.0, raw=False):
    i=int((start if raw else M(start))*SR); j=min(N,i+len(sig)); out[i:j]+=sig[:j-i]*g
def env(n, a=0.005, r=None):
    e=np.ones(n); na=max(1,int(a*SR)); e[:na]=np.linspace(0,1,na)
    if r: e*=np.exp(-np.arange(n)/SR/r)
    return e
def tone(f, d, wave_='sin'):
    tt=np.arange(int(d*SR))/SR
    ph=2*np.pi*np.cumsum(np.broadcast_to(f,tt.shape) if np.ndim(f) else np.full(tt.shape,f))/SR
    if wave_=='sin': return np.sin(ph)
    if wave_=='saw': return 2*((ph/(2*np.pi))%1)-1
    if wave_=='sq': return np.sign(np.sin(ph))
def noise(d): return rng.standard_normal(int(d*SR))
def lowpass(x, a):
    y=np.empty_like(x); acc=0.0
    for i in range(len(x)): acc+= a*(x[i]-acc); y[i]=acc
    return y
# fluorescent hum 0-50, faint
hum=(0.5*np.sin(2*np.pi*120*t)+0.25*np.sin(2*np.pi*240*t)+0.12*np.sign(np.sin(2*np.pi*120*t)))
vt=np.interp(t, __import__('warp').TK, __import__('warp').VK)
mask=np.where(vt<50,1.0,np.where(vt<52.4,0.0,0.4)); mask[vt>=56.5]=0
out+=hum*0.035*mask
# flicker buzz bursts
for k in range(0,int(50*12)):
    r=(k*2654435761)%97
    if r<6: add(k/12, noise(0.08)*env(int(0.08*SR),0.002,0.03), 0.08)
# ominous drone pulse 3-50
for b in np.arange(M(3),M(50),60/100):
    f=55 if int((b-M(3))/(60/100))%8<6 else 52
    s=tone(f,0.5,'saw'); s=lowpass(s,0.05)*env(len(s),0.01,0.18)
    add(b,s,0.35,raw=True)
# heartbeat 3-15
for b in np.arange(M(3),M(15),0.75):
    for off,g in ((0,1),(0.18,0.7)):
        s=tone(np.linspace(70,45,int(0.15*SR)),0.15)*env(int(0.15*SR),0.003,0.05)
        add(b+off,s,0.6*g,raw=True)
# scream at 1.5
sc=tone(np.linspace(950,420,int(0.8*SR))*(1+0.04*np.sin(2*np.pi*7*np.arange(int(0.8*SR))/SR)),0.8,'saw')
sc=lowpass(sc,0.25)*env(len(sc),0.02,0.5); add(1.5,sc,0.18)
add(1.5,lowpass(noise(0.6),0.2)*env(int(0.6*SR),0.01,0.3),0.12)
# whooshes at scene changes
for st in (3,8,15,25,32,42,50):
    n=noise(0.35); n=lowpass(n,0.08)*np.sin(np.linspace(0,np.pi,len(n))); add(st-0.15,n,0.6)
# switch click
add(9.4, noise(0.02)*env(int(0.02*SR),0.001,0.004),0.6)
# scrape 10.6-14.3 then thud
SD=M(14.3)-M(10.6); sc=lowpass(noise(SD),0.03)*(0.6+0.4*np.sin(2*np.pi*9*np.arange(int(SD*SR))/SR)); add(10.6,sc,0.5)
th=tone(np.linspace(90,35,int(0.5*SR)),0.5)*env(int(0.5*SR),0.002,0.12); add(14.3,th,1.0); add(14.3,lowpass(noise(0.3),0.1)*env(int(0.3*SR),0.002,0.06),0.8)
# zombie bangs on glass during s3
for b in np.arange(8.3,14,0.9):
    add(b, lowpass(noise(0.12),0.15)*env(int(0.12*SR),0.002,0.03),0.35)
# item pops + chime
for st in (15.6,17.2,18.7,19.7,21.1,22.5):
    p=tone(np.linspace(300,900,int(0.12*SR)),0.12)*env(int(0.12*SR),0.002,0.06); add(st,p,0.35)
    c=(tone(1568,0.3)+0.5*tone(2093,0.3))*env(int(0.3*SR),0.002,0.1); add(st+0.45,c,0.15)
# buzzers for X
for st in (26.5,27.6):
    bz=lowpass(tone(140,0.4,'sq'),0.3)*env(int(0.4*SR),0.005,0.25); add(st,bz,0.3)
add(28.5, tone(np.linspace(220,110,int(0.5*SR)),0.5,'saw')*env(int(0.5*SR),0.005,0.2),0.15)
# creak + fog hiss at 33
cr=tone(np.linspace(180,120,int(1.4*SR))*(1+0.15*np.sign(np.sin(2*np.pi*14*np.arange(int(1.4*SR))/SR))),1.4,'saw')
add(33.0, lowpass(cr,0.1)*env(len(cr),0.05,0.8),0.2)
hs=lowpass(noise(5),0.4)*np.linspace(1,0,int(5*SR)); add(33.3,hs,0.06)
# stamp at 37.6
add(37.6, tone(np.linspace(120,50,int(0.3*SR)),0.3)*env(int(0.3*SR),0.002,0.08),0.8)
# bonks
for st in (43.5,44.9,46.3):
    bo=tone(np.linspace(500,180,int(0.25*SR)),0.25)*env(int(0.25*SR),0.002,0.08); add(st,bo,0.6)
    add(st, noise(0.03)*env(int(0.03*SR),0.001,0.01),0.3)
# DING DONG door chime 52.4
for off,f in ((0,1318.5),(0.38,1046.5)):
    c=(tone(f,1.5)+0.4*tone(f*2.01,1.5)+0.2*tone(f*3.0,1.5))*env(int(1.5*SR),0.002,0.5); add(52.4+off,c,0.3)
# horror sting 53.3
d_=2.6; st=sum(tone(f,d_,'saw') for f in (55,58.3,110.4,116.7,164.8))
st=lowpass(st,0.08)*env(int(d_*SR),0.01,1.0); add(53.2,st,0.35)
add(53.2,lowpass(noise(1.2),0.3)*env(int(1.2*SR),0.005,0.25),0.35)
hi=tone(np.linspace(2000,2600,int(2*SR)),2,'saw')*env(int(2*SR),0.02,0.7); add(53.2,lowpass(hi,0.3),0.05)
# outro riser/pop
add(57.0, tone(np.linspace(200,600,int(0.35*SR)),0.35)*env(int(0.35*SR),0.005,0.2),0.25)
for b in np.arange(M(57.4),DUR,0.5):
    add(b, tone(np.linspace(80,40,int(0.12*SR)),0.12)*env(int(0.12*SR),0.002,0.05), 0.4, raw=True)
sfx=out/np.max(np.abs(out))
raw=subprocess.run(["ffmpeg","-v","error","-i","vo/vo.mp3","-f","f32le","-ac","1","-ar",str(SR),"-"],capture_output=True).stdout
vo=np.frombuffer(raw,dtype=np.float32).astype(np.float64)
g=int(GAP_AT*SR); vo=np.concatenate([vo[:g],np.zeros(int(GAP*SR)),vo[g:]])
voice=np.zeros(N); voice[:min(N,len(vo))]=vo[:N]
voice=voice/np.max(np.abs(voice))*0.95
# ducking envelope
w=int(0.05*SR); e=np.sqrt(np.convolve(voice**2,np.ones(w)/w,mode="same"))
on=(e>0.02).astype(float); k=int(0.25*SR)
on=np.convolve(on,np.ones(k)/k,mode="same"); on=np.clip(on*1.5,0,1)
mix=voice+sfx*0.42*(1-0.6*on)
mix=mix/np.max(np.abs(mix))*0.95
fade=np.ones(N); fade[-int(0.4*SR):]=np.linspace(1,0,int(0.4*SR)); mix*=fade
with wave.open('audio_vo.wav','wb') as wv:
    wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((mix*32767).astype(np.int16).tobytes())
print("ok", len(vo)/SR)
