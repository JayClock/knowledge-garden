import json,re
d=json.load(open('.pi/tmp/shapes.json',encoding='utf-8'))
for r in d['data']['results']:
    st=r.get('format',{}).get('style','')
    t=(r.get('text') or '').replace('\n',' ')[:30]
    pos=re.search(r'margin-left:([-\d.]+)pt;margin-top:([-\d.]+)pt;width:([\d.]+)pt;height:([\d.]+)pt',st)
    path=r['path']
    print(path.split('/')[3], pos.groups() if pos else None, '|', t)
