# Paper 36 (PMC12508033): settlement ~2 mm and horizontal displacement ~0.9 mm; 'time-dependent' shallow displacement.
import numpy as np
rng=np.random.default_rng(36); n=200000
W=21305*9.81; Ap=10.0; q=W/Ap
print("equipment pressure %.1f kPa"%(q/1e3))
E=rng.uniform(15e6,25e6,n); nu=rng.uniform(0.3,0.35,n); B=np.sqrt(Ap); I=rng.uniform(0.8,1.1,n)
s=q*B*(1-nu**2)*I/E*1e3
print("elastic settlement under rig mm median %.1f (5-95%%: %.1f-%.1f) vs model/field ~2 mm"%(np.median(s),*np.percentile(s,[5,95])))
k=1.1e-8; Es=4.05e6; gw=9.81e3; cv=k*Es/gw
H=rng.uniform(2,8,n); t90=0.848*H**2/cv/86400
print("cv=%.1e m2/s; t90 consolidation days median %.0f (5-95%%: %.0f-%.0f) -> time-dependence over days-weeks plausible"%(cv,np.median(t90),*np.percentile(t90,[5,95])))
print("radii 0.30/0.325/0.35 m: increment 25 mm, range +/-7.7% (text says 50 mm increment, +/-5%)")
