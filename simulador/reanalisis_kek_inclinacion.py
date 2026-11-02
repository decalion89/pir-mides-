"""Perfil de la inclinación con los 679 puntos de KEK, con la posición de los detectores libre (~30 min).

    cd simulador && PYTHONPATH=. python reanalisis_kek_inclinacion.py
"""
import time, json, numpy as np
from scipy.optimize import minimize
from piramide import reanalisis as ra
t=time.time()
datos=ra.cargar()
LIM=[(-10,45),(45,85),(10,60),(1,15),(0.8,8)]
def pen(v): return sum(100*(max(lo-val,0)+max(val-hi,0))**2 for val,(lo,hi) in zip(v[1:6],LIM))
res={}
for dxd in (-1.0,0.0,1.0):
  for dzd in (0.0,0.8):
    for dyd in (-0.6,0.6):
      r=ra.Reanalisis(datos,pos_h1=(7.1+dxd,-1.9+dyd,21.5+dzd))
      def fit(a, starts):
        best=None
        for s in starts:
          f=lambda v: r.chi2(ra.Corredor(v[0],v[1],v[2],v[3],v[4],ancho=v[5],inclinacion=a))+pen(v)
          o=minimize(f,np.array(s,float),method='Nelder-Mead',options=dict(maxiter=900,xatol=0.01,fatol=0.01))
          if best is None or o.fun<best.fun: best=o
        return best.fun,best.x
      for a in (0,10,18,26,35):
        c,v=fit(float(a),[(7.3,10,63,45,8,2),(7.3,15,62,36,8,1.6),(7.3,7,60,55,6,2.5)])
        key=a
        if key not in res or c<res[key][0]: res[key]=(c,list(v),(dxd,dyd,dzd))
      print('variante det',(dxd,dyd,dzd),{a:round(res[a][0],1) for a in res},'%.0fs'%(time.time()-t),flush=True)
best=min(v[0] for v in res.values()); ndf=679-6-18-3
esc=best/ndf
print('KEK: χ²min %.1f ndf %d χ²/ndf %.2f'%(best,ndf,esc))
for a in sorted(res): print('incl %d  Δχ2 %.1f  -> %.1fσ'%(a,res[a][0]-best,np.sqrt(max(res[a][0]-best,0)/esc)), 'params',np.round(res[a][1],1),'det',res[a][2])
json.dump({str(a):dict(chi2=res[a][0],params=res[a][1],detector=res[a][2]) for a in res},open('../resultados/08_reanalisis_kek_incl.json','w'),indent=1)
