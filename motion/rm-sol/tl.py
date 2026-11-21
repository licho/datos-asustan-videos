import re,json,sys
src=open('src/script.js').read()
lines=re.findall(r'\["(\w*)", "([^"]+)", "([^"]+)"\]',src)
timing=json.load(open('src/timing.json'))
t=0;out=[]
for i,(_,sp,sub) in enumerate(lines):
    if timing.get('lines'):
        s=timing['lines'][i]['start'];d=timing['lines'][i]['dur']
    else:
        s=t;d=max(4.4 if i==0 else 2.6,len(sp.split())/2.95+0.35)
    out.append((i,round(s,2),round(d,2)));t=s+d
out[-1]=(out[-1][0],out[-1][1],round(out[-1][2]+3,2))
print(json.dumps(out)); print("total",round(out[-1][1]+out[-1][2],2),file=sys.stderr)
