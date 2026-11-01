import sys, numpy as np
exec(open('alvarez_independiente/reconstruccion.py').read().split("o=(12.0,5.0,-6.0)")[0])
N9m=np.loadtxt('../datos/alvarez_1970/fig9_predichos.csv',delimiter=',',comments='#')
i,j=np.meshgrid(np.arange(30),np.arange(30),indexing='ij')
th=np.radians(45+3*i+1.5-90); ph=np.radians(45+3*j+1.5-90); r2=np.tan(th)**2+np.tan(ph)**2
Vc=V&(np.sqrt(r2)<0.7)
def analizar(m, O, retro, zcap, plantilla_alvarez=False, puntos=None):
    kf.opacidad=opacidad_remate(retro,zcap); A=ea.Alvarez(np.array(O),0,1.0); kf.opacidad=orig_op
    base=np.maximum(N9m,0.5) if plantilla_alvarez else np.maximum(A.N0.reshape(30,30),1e-6)
    filas=np.where(Vc.any(1))[0]; cols=np.where(Vc.any(0))[0]; idx=np.argwhere(Vc)
    ncol=len(filas)+len(cols)-1+(0 if plantilla_alvarez else 2)
    X=np.zeros((len(idx),ncol))
    for k,(a,b) in enumerate(idx):
        X[k,list(filas).index(a)]=1; jb=list(cols).index(b)
        if jb>0: X[k,len(filas)+jb-1]=1
        if not plantilla_alvarez: X[k,-2]=r2[a,b]; X[k,-1]=r2[a,b]**2
    y=N8[Vc]; lm=np.log(base[Vc]); beta=np.zeros(ncol); beta[:len(filas)]=np.log(y.sum()/np.exp(lm).sum())
    for _ in range(60):
        eta=lm+X@beta; mu=np.exp(eta); zz=eta-lm+(y-mu)/mu
        beta=np.linalg.lstsq(X*np.sqrt(mu)[:,None], zz*np.sqrt(mu), rcond=None)[0]
    mu=np.exp(lm+X@beta); z=(y-mu)/np.sqrt(mu); Q,_=np.linalg.qr(X*np.sqrt(mu)[:,None])
    perp=lambda x: x-Q@(Q.T@x); rp=perp(z); kap=float(np.mean(z**2))
    out=[]
    for q in puntos:
        h=A.huella(kf.camara_del_rey(q)); rel=np.where(A.N0>0,h/np.sqrt(np.maximum(A.N0,1e-12)),0.0).reshape(30,30)
        s=perp(rel[Vc]*np.sqrt(mu)); out.append(round(float((np.sum((rp-s)**2)-np.sum(rp**2))/kap),1))
    return round(float((z**2).sum())), out
cand=[np.array([24.4,16.4,60.0]), np.array([24.4,8.4,60.0]), np.array([16.4,16.4,52.0]), np.array([32.4,24.4,68.0])]
print('puntos: candidato y vecinos', [c.tolist() for c in cand])
print('PLANTILLA ALVAREZ   :', analizar(None,(12.0,5.0,-6.0),6.0,90.0,True,cand))
for O,retro,zcap in (((12.0,5.0,-6.0),6.0,90.0),((12.0,5.0,-6.0),4.0,100.0),((12.0,5.0,-6.0),8.0,80.0),((15.5,4.0,-0.5),6.0,90.0),((13.5,4.0,-3.0),6.0,90.0),((12.0,5.0,-6.0),0.0,136.0)):
    print('modelo propio',O,'retro',retro,'remate',zcap,':', analizar(None,O,retro,zcap,False,cand), flush=True)
