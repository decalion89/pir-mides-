import numpy as np, exclusion_alvarez as ea, reajuste_alvarez as rj
from piramide import kefren as kf
N8,N9,v=rj.cargar(); N8=N8.reshape(30,30); V=v.reshape(30,30)
def chi_sep(m, iters=300):
    a=np.zeros(30); b=np.zeros(30)
    for _ in range(iters):
        E=m*np.exp(a[:,None]+b[None,:]); a+=np.log(np.maximum((N8*V).sum(1),1e-9)/np.maximum((E*V).sum(1),1e-9))*(V.sum(1)>0)
        E=m*np.exp(a[:,None]+b[None,:]); b+=np.log(np.maximum((N8*V).sum(0),1e-9)/np.maximum((E*V).sum(0),1e-9))*(V.sum(0)>0)
    E=m*np.exp(a[:,None]+b[None,:]); return float((((N8-E)**2/np.maximum(E,1e-9))[V]).sum())
def chi(x,y,z):
    A=ea.Alvarez(np.array([x,y,z]),0,1.0); return chi_sep(np.maximum(A.N0.reshape(30,30),1e-6))
res=[]
for x in (9,12,15,18,21):
    for y in (-4,0,4,8,12):
        c=chi(x,y,-0.5); res.append((c,x,y)); print(x,y,round(c))
res.sort(); print('mejor', res[:3])
c,x0,y0=res[0]
fino=[]
for x in np.arange(x0-2,x0+2.1,1.0):
    for y in np.arange(y0-2,y0+2.1,1.0):
        for z in (-0.5,-3.0,-6.0):
            fino.append((chi(x,y,z),x,y,z))
fino.sort(); print('fino', [(round(a),b,c,d) for a,b,c,d in fino[:5]])
