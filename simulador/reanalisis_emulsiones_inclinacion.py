"""Perfil de la inclinación del Gran Vacío con las emulsiones de Nagoya y sus variantes de robustez.

    cd simulador && PYTHONPATH=. python reanalisis_emulsiones_inclinacion.py   (~6 min)
"""
import time, sys, json, numpy as np
from scipy.optimize import minimize
from piramide import reanalisis_emulsiones as re_
from piramide.reanalisis import Corredor
LIM=[(-10,45),(45,85),(10,60),(1,15),(0.8,8),(0,0.06)]
def build(v,a=None):
    x,y,z,L,h,w,sg=v[:7]; inc=a if a is not None else v[7]
    return Corredor(x,y,z,L,h,ancho=w,inclinacion=inc), sg
def pen(v): return sum(100*(max(lo-val,0)+max(val-hi,0))**2 for val,(lo,hi) in zip(v[1:7],LIM))
def perfil_incl(e, opts, angs=(0,10,20,26,35)):
    def f(v,a=None):
        c,sg=build(v,a); return e.chi2_vacio(c,sigma=max(sg,0),**opts)+pen(v)
    def fit(a=None,starts=None):
        best=None
        for s in starts:
            v0=list(s)+([] if a is not None else [18.0])
            r=minimize(lambda v: f(v,a), np.array(v0,float), method='Nelder-Mead', options=dict(maxiter=1200,xatol=0.01,fatol=0.01))
            if best is None or r.fun<best.fun: best=r
        return best.fun,best.x
    st=[(7.3,10,63,45,8,2,0.033),(7.3,15,62,36,8,1.6,0.03),(7.3,7,60,55,8,2,0.035)]
    cf,vf=fit(None,st)
    res={'libre':(cf,float(build(vf)[0].inclinacion))}
    for a in angs:
        ca,_=fit(float(a),[tuple(vf[:7])]+st[:2]); res[a]=ca
    best=min([cf]+[res[a] for a in angs])
    return best,res
casos={
 'nominal': (dict(), dict()),
 'sin el corte 3': (dict(), dict(cortes=(0,1,2))),
 'sin el corte 0 (el peor medido)': (dict(), dict(cortes=(1,2,3))),
 'residuo de la Galería libre': (dict(), dict(residuo_galeria=True)),
}
out={}
for nombre,(kw_e,kw_c) in casos.items():
    t=time.time()
    e=re_.Emulsiones(x_ne1=13.0,x_ne2=3.0,**kw_e)
    best,res=perfil_incl(e,kw_c)
    cortes=kw_c.get('cortes',range(4)); zona=kw_c.get('zona',re_.ZONA)
    npts=sum(((e.d[(p,k,'vacio')][0]>=zona[p][0])&(e.d[(p,k,'vacio')][0]<=zona[p][1])).sum() for p in ('NE1','NE2') for k in cortes)
    nnuis=2*len(list(cortes))*(2 if kw_c.get('residuo_galeria') else 1)
    ndf=npts-8-nnuis; esc=best/ndf
    z={a:float(np.sqrt(max(res[a]-best,0)/esc)) for a in (0,10,20,26,35)}
    out[nombre]=dict(incl_libre=res['libre'][1],chi2_ndf=esc,sigma_vs={str(k):v for k,v in z.items()})
    print(f"{nombre:40s} incl.libre {res['libre'][1]:5.1f}°  χ²/ndf {esc:4.1f}  desfavorecida a: " + "  ".join(f"{a}°:{z[a]:.1f}σ" for a in (0,10,20,26,35)), f"({time.time()-t:.0f}s)", flush=True)
json.dump(out,open('../resultados/07_reanalisis_emulsiones_inclinacion.json','w'),ensure_ascii=False,indent=2)
