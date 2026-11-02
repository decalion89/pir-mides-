"""Ajuste conjunto emulsiones + KEK con un mismo corredor (~25 min).

    cd simulador && PYTHONPATH=. python reanalisis_conjunto.py
"""
import time, json, numpy as np
from scipy.optimize import minimize
from piramide import reanalisis as ra, reanalisis_emulsiones as re_
t=time.time()
E=re_.Emulsiones(x_ne1=13.0,x_ne2=3.0)
K={det:ra.Reanalisis(pos_h1=(7.1+det[0],-1.9+det[1],21.5+det[2])) for det in ((0.0,0.0,0.0),(1.0,0.6,0.8),(-1.0,0.0,0.0),(0.0,0.0,0.8))}
S_E, S_K = 3.9, 1.69          # χ²/ndf de cada conjunto por separado (escala de errores)
LIM=[(-10,45),(45,85),(10,60),(1,15),(0.8,8),(0,0.06)]
def pen(v): return sum(100*(max(lo-val,0)+max(val-hi,0))**2 for val,(lo,hi) in zip(v[1:7],LIM))
def chi(v,a,kk):
    x,y,z,L,h,w,sg=v
    c=ra.Corredor(x,y,z,L,h,ancho=w,inclinacion=a)
    return E.chi2_vacio(c,sigma=max(sg,0))/S_E + K[kk].chi2(c)/S_K + pen(v)
res={}
for a in (0,10,18,26,35):
    best=None
    for kk in K:
        for s in [(7.3,10,62,45,8,1.8,0.03),(7.3,15,60,36,6,2,0.03),(7.3,5,58,50,9,1.6,0.035)]:
            r=minimize(lambda v: chi(v,float(a),kk),np.array(s,float),method='Nelder-Mead',options=dict(maxiter=900,xatol=0.01,fatol=0.01))
            if best is None or r.fun<best[0]: best=(r.fun,list(r.x),kk)
    res[a]=best
    print('incl',a,'chi2 conjunto (escalado) %.1f'%best[0],'params',np.round(best[1],2),'det KEK',best[2],'%.0fs'%(time.time()-t),flush=True)
m=min(v[0] for v in res.values())
print('Perfil conjunto:', {a:round(float(np.sqrt(max(res[a][0]-m,0))),1) for a in res})
json.dump({str(a):dict(chi2_escalado=res[a][0],params=res[a][1],det_kek=res[a][2],sigma=float(np.sqrt(max(res[a][0]-m,0)))) for a in res},open('../resultados/09_reanalisis_conjunto_inclinacion.json','w'),indent=1)
