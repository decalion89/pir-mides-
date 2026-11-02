import sys, json, numpy as np
sys.argv=['x']
exec(open('alvarez_independiente/reconstruccion.py').read().split("o=(12.0,5.0,-6.0)")[0])
import reanalisis_alvarez as ra
from scipy.stats import norm
O=np.array((12.0,5.0,-6.0)); kf.opacidad=opacidad_remate(6.0,90.0)
A=ea.Alvarez(O,0,1.0); kf.opacidad=orig_op
m=np.maximum(A.N0.reshape(30,30),1e-6)
i,j=np.meshgrid(np.arange(30),np.arange(30),indexing='ij')
th=np.radians(45+3*i+1.5-90); ph=np.radians(45+3*j+1.5-90); r2=np.tan(th)**2+np.tan(ph)**2
Vc=V&(np.sqrt(r2)<0.7)
# ajuste de Poisson: log E = log m + a_i + b_j + c1 r2 + c2 r4  (IRLS con mínimos cuadrados ponderados)
filas=np.where(Vc.any(1))[0]; cols=np.where(Vc.any(0))[0]
idx=np.argwhere(Vc)
X=np.zeros((len(idx), len(filas)+len(cols)-1+2))
for k,(a,b) in enumerate(idx):
    X[k,list(filas).index(a)]=1
    jb=list(cols).index(b)
    if jb>0: X[k,len(filas)+jb-1]=1
    X[k,-2]=r2[a,b]; X[k,-1]=r2[a,b]**2
y=N8[Vc]; lm=np.log(m[Vc]); beta=np.zeros(X.shape[1]); beta[:len(filas)]=np.log(y.sum()/np.exp(lm).sum())
for _ in range(60):
    eta=lm+X@beta; mu=np.exp(eta); W=mu; zz=eta-lm+(y-mu)/mu
    beta=np.linalg.lstsq(X*np.sqrt(W)[:,None], zz*np.sqrt(W), rcond=None)[0]
mu=np.exp(lm+X@beta); z=(y-mu)/np.sqrt(mu); chi=float((z**2).sum())
print('ajuste independiente en el cono: chi2',round(chi),'n',len(y),'params',X.shape[1])
J=X*np.sqrt(mu)[:,None]; Q,_=np.linalg.qr(J)
perp=lambda x: x-Q@(Q.T@x)
rp=perp(z); kappa=float(np.mean(z**2))
P=kf.voxeles(8.0); en_cono=np.array([kf.fraccion_en_cono(q[None], origen=O) for q in P])>0
out={'chi2':round(chi,1),'n_casillas':int(len(y)),'n_parametros':int(X.shape[1]),'kappa':round(kappa,3),'detector':O.tolist(),'retranqueo_m':6.0,'z_remate_m':90.0}
for nombre,f in (('camara_tipo_rey',kf.camara_del_rey),):
    ok=np.array([ea.cabe(f(q)) and c for q,c in zip(P,en_cono)])
    S=[]
    for q in P[ok]:
        h=A.huella(f(q)); rel=np.where(A.N0>0,h/np.sqrt(np.maximum(A.N0,1e-12)),0.0).reshape(30,30)
        S.append(perp((rel[Vc])*np.sqrt(mu)))
    S=np.array(S); d=(np.sum((rp[None,:]-S)**2,1)-np.sum(rp**2))/kappa
    i0=int(np.argmin(d))
    rng=np.random.default_rng(70)
    Zmap=np.full((30,30),np.nan); Zmap[Vc]=z
    cal=ra.calibrar_nula(np.round(Zmap),rng)
    mins=[]
    for _ in range(1000):
        Rn=ra.campo_correlado(Vc,cal['sigma_nucleo_bins'],float(np.nanstd(Zmap))*cal['escala'],rng,cal['fraccion_correlada'],0.0)[Vc]
        Rp=perp(Rn); mins.append(((np.sum((Rp[None,:]-S)**2,1)-np.sum(Rp**2))/kappa).min())
    p=float(np.mean(np.array(mins)<=d[i0]))
    out[nombre]=dict(posiciones_en_cono=int(ok.sum()),excluido_95_en_cono=float(np.mean(d>=3.84)),excluido_5s_en_cono=float(np.mean(d>=25)),
                     minimo=round(float(d[i0]),2),donde=[round(float(x),1) for x in P[ok][i0]],p_global=p)
    print(nombre,out[nombre])
json.dump(out,open('../resultados/35_reanalisis_independiente_alvarez.json','w'),indent=1,ensure_ascii=False,allow_nan=False)
