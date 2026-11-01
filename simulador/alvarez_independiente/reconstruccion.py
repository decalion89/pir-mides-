import numpy as np, exclusion_alvarez as ea, reajuste_alvarez as rj
from piramide import kefren as kf
N8,N9,v=rj.cargar(); N8=N8.reshape(30,30); V=v.reshape(30,30)

def L_convexo(o, dirs, retro, zmin, zmax):
    k=kf.TAN_CARA
    n=np.array([[k,0,1],[-k,0,1],[0,k,1],[0,-k,1],[0,0,-1],[0,0,1]],float)
    hc=kf.ALTURA - k*retro
    c=np.array([hc,hc,hc,hc,-zmin,zmax])
    nd=dirs@n.T; hol=c-n@o
    with np.errstate(divide='ignore',invalid='ignore'): t=hol[None,:]/nd
    ts=np.min(np.where(nd>1e-12,t,np.inf),1); te=np.max(np.where(nd<-1e-12,t,-np.inf),1)
    L=np.clip(ts-np.maximum(te,0),0,None); L[~np.isfinite(L)]=0
    L[np.any((np.abs(nd)<=1e-12)&(hol[None,:]<0),1)]=0
    return L

def opacidad_remate(retro, zcap):
    def f(o, dirs):
        Ltot=(L_convexo(o,dirs,retro,0.0,kf.ALTURA_ACTUAL) + L_convexo(o,dirs,0.0,zcap,kf.ALTURA_ACTUAL)
              - L_convexo(o,dirs,retro,zcap,kf.ALTURA_ACTUAL))
        X=kf.DENSIDAD*Ltot*100.0
        if o[2]<0: X=X+2.3*(-o[2])/np.clip(dirs[:,2],1e-6,None)*100.0
        return X
    return f

def chi_sep(m, iters=300):
    a=np.zeros(30); b=np.zeros(30)
    for _ in range(iters):
        E=m*np.exp(a[:,None]+b[None,:]); a+=np.log(np.maximum((N8*V).sum(1),1e-9)/np.maximum((E*V).sum(1),1e-9))*(V.sum(1)>0)
        E=m*np.exp(a[:,None]+b[None,:]); b+=np.log(np.maximum((N8*V).sum(0),1e-9)/np.maximum((E*V).sum(0),1e-9))*(V.sum(0)>0)
    E=m*np.exp(a[:,None]+b[None,:]); return float((((N8-E)**2/np.maximum(E,1e-9))[V]).sum())

orig_op=kf.opacidad
def chi(o, retro, zcap):
    kf.opacidad=opacidad_remate(retro,zcap)
    try:
        A=ea.Alvarez(np.array(o),0,1.0)
    finally:
        kf.opacidad=orig_op
    return chi_sep(np.maximum(A.N0.reshape(30,30),1e-6))

o=(12.0,5.0,-6.0)
print('sin remate', round(chi(o,0.0,136.0)))
best=[]
for retro in (1.0,2.0,3.0,4.0,6.0):
    for zcap in (90.0,100.0,110.0,120.0):
        c=chi(o,retro,zcap); best.append((c,retro,zcap)); print(retro,zcap,round(c),flush=True)
best.sort(); print('mejor',[(round(a),b,c) for a,b,c in best[:4]])

from scipy.ndimage import gaussian_filter
def chi_suave(o, retro, zcap, sig):
    kf.opacidad=opacidad_remate(retro,zcap)
    try: A=ea.Alvarez(np.array(o),0,1.0)
    finally: kf.opacidad=orig_op
    m=A.N0.reshape(30,30)
    if sig>0: m=gaussian_filter(m, sig, mode='nearest')
    return chi_sep(np.maximum(m,1e-6))
print('--- con dispersión (σ en casillas de 3°)')
res=[]
for sig in (0.0,0.3,0.5,0.7,1.0):
    for retro,zcap in ((6.0,90.0),(8.0,80.0),(0.0,136.0)):
        c=chi_suave((12.0,5.0,-6.0),retro,zcap,sig); res.append((c,sig,retro,zcap)); print(sig,retro,zcap,round(c),flush=True)
res.sort(); print('mejor',[(round(a),b,c,d) for a,b,c,d in res[:3]])

print('--- diagnóstico del residuo')
kf.opacidad=opacidad_remate(6.0,90.0)
A=ea.Alvarez(np.array((12.0,5.0,-6.0)),0,1.0); kf.opacidad=orig_op
m=np.maximum(A.N0.reshape(30,30),1e-6)
i,j=np.meshgrid(np.arange(30),np.arange(30),indexing='ij')
th=np.radians(45+3*i+1.5-90); ph=np.radians(45+3*j+1.5-90)
r2=np.tan(th)**2+np.tan(ph)**2
def ajuste(m, extra=None, iters=400):
    a=np.zeros(30); b=np.zeros(30); c=np.zeros(0 if extra is None else len(extra))
    for _ in range(iters):
        base=m*(np.exp(sum(cc*e for cc,e in zip(c,extra))) if extra is not None else 1)
        E=base*np.exp(a[:,None]+b[None,:]); a+=np.log(np.maximum((N8*V).sum(1),1e-9)/np.maximum((E*V).sum(1),1e-9))*(V.sum(1)>0)
        E=base*np.exp(a[:,None]+b[None,:]); b+=np.log(np.maximum((N8*V).sum(0),1e-9)/np.maximum((E*V).sum(0),1e-9))*(V.sum(0)>0)
        if extra is not None:
            E=base*np.exp(a[:,None]+b[None,:])
            for k,e in enumerate(extra):   # paso de Newton por coordenada (Poisson)
                g=((N8-E)*e)[V].sum(); H=(E*e*e)[V].sum(); c[k]+=g/max(H,1e-9)
    base=m*(np.exp(sum(cc*e for cc,e in zip(c,extra))) if extra is not None else 1)
    E=base*np.exp(a[:,None]+b[None,:]); z=(N8-E)/np.sqrt(np.maximum(E,1e-9))
    return float((z[V]**2).sum()), z, c
chi0,z,_=ajuste(m)
print('sin términos radiales', round(chi0))
for nombre,ex in (('r2',[r2]),('r2,r4',[r2,r2**2]),('r2,r4,r6',[r2,r2**2,r2**3])):
    c,zz,cc=ajuste(m,ex); print(nombre, round(c), np.round(cc,3))
# ¿dónde está el residuo? por anillos de r y cerca de las diagonales (aristas)
R=np.sqrt(r2)
for lo,hi in ((0,0.3),(0.3,0.6),(0.6,0.8),(0.8,1.0),(1.0,1.5)):
    s=V&(R>=lo)&(R<hi); print('anillo tan',lo,hi,'chi2/bin',round(float((z[s]**2).mean()),2),'n',int(s.sum()))
diag=np.minimum(np.abs(np.abs(np.tan(th))-np.abs(np.tan(ph))),9)
for lo,hi in ((0,0.05),(0.05,0.15),(0.15,9)):
    s=V&(diag>=lo)&(diag<hi); print('dist. a la diagonal',lo,hi,'chi2/bin',round(float((z[s]**2).mean()),2),'n',int(s.sum()))

print('--- solo la zona central')
N9m=np.loadtxt('../datos/alvarez_1970/fig9_predichos.csv',delimiter=',',comments='#')
for corte in (0.6,0.7,0.8):
    Vc=V&(R<corte)
    def aj(m,extra=None,iters=400):
        global V
        Vg=V; V=Vc
        try: return ajuste(m,extra,iters)
        finally: V=Vg
    c_m,z_m,_=aj(m,[r2,r2**2])
    c_a,z_a,_=aj(np.maximum(N9m,0.5))
    n=int(Vc.sum())
    print(f'tanθ<{corte}: casillas {n} | nuestro modelo independiente chi2={c_m:.0f} (chi2/n={c_m/n:.2f}) | plantilla de Alvarez chi2={c_a:.0f} (chi2/n={c_a/n:.2f})')
