import sys,re,glob,os
from xml.etree import ElementTree as ET
src=sys.argv[1]; out=sys.argv[2]
for f in glob.glob(os.path.join(src,'PMC*.xml')):
    t=ET.parse(f).getroot()
    # remove ref-list
    for parent in t.iter():
        for c in list(parent):
            if c.tag in ('ref-list',):
                parent.remove(c)
    parts=[]
    def walk(e):
        if e.tag in ('title','p','caption','td','th','label','disp-formula','tr'):
            parts.append(' '.join(''.join(e.itertext()).split()))
            return
        for c in e: walk(c)
    walk(t)
    open(os.path.join(out,os.path.basename(f)[:-4]+'.txt'),'w').write('\n'.join(parts))
