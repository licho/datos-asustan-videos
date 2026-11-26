import re,json,sys
src=open('src/script.js').read()
lines=re.findall(r'\["(\w*)", "([^"]+)", "([^"]+)"\]',src)
timing=json.load(open('src/timing.json'))
t=0;out=[]
for i,(_,sp,sub) in enumerate(lines):
    if timing.get('lines'): s=timing['lines'][i]['start'];d=timing['lines'][i]['dur']
    else:
        s=t;d=max(1.3,len(sp.split())/2.95+(0.45 if re.search(r'[.…?»]$',sp) else 0.3))
    out.append((i,round(s,3),round(d,3)));t=s+d
out[-1]=(out[-1][0],out[-1][1],round(out[-1][2]+3,3))
print(json.dumps(out))
