# Paper 30 (PMC9485162): 5-km melt column, >380,000 km3, filled 'over a much shorter time scale than solidification',
# MZ cumulates (3 km) at ~1 cm/yr -> 300 kyr.
import numpy as np
print("Volume: 5 km*70,000 km2 + 1 km*30,000 km2 = %d km3 (paper 380,000); area quoted as '100,000 km3' = unit typo (km2)"%(5*70000+1*30000))
print("Duration: 3 km / 1 cm/yr = %.0f yr (paper ~300,000)"%(3e5/1))
rng=np.random.default_rng(30); n=200000
V=rng.uniform(3.0e5,3.8e5,n)            # km3
srate=np.exp(rng.uniform(np.log(0.5),np.log(2.0),n))/1e5   # km/yr (0.5-2 cm/yr)
Tsol=5.0/srate                          # yr to solidify 5 km column from floor
f=rng.uniform(0.05,0.3,n)               # filling time as fraction of solidification time ('much shorter')
flux=V/(f*Tsol)                         # km3/yr
LIPmax=np.exp(rng.uniform(np.log(5),np.log(20),n))  # km3/yr, upper documented LIP pulse emplacement rates (Deccan/CAMP peak pulses)
r=flux/LIPmax
print("required mean filling flux km3/yr median %.1f (5-95%%: %.1f-%.1f)"%(np.median(flux),*np.percentile(flux,[5,95])))
print("ratio to LIP peak-rate bound: median %.2f; P(>=3)=%.3f; P(>=1)=%.3f"%(np.median(r),np.mean(r>=3),np.mean(r>=1)))
# (A separate roof-heat-loss test is circular: the 0.5-2 cm/yr solidification rate already encodes heat loss, so any
# filling faster than solidification supplies heat faster than it is lost.)
