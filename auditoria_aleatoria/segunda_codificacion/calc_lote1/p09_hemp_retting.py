# Paper 9 (PMC9132974): could hemp retting in small Lake Slone supply enough allochthonous organic matter
# to drive eutrophication/anoxia? Lake dimensions not given in paper: core at 8.0 m water depth; 'small lake area and volume'.
# Assume area 2-10 ha, mean depth 3-6 m. Retting releases soluble/pectic fraction of straw (~8-20% of dry mass) as BOD.
import numpy as np
rng=np.random.default_rng(9); n=200000
A=np.exp(rng.uniform(np.log(2e4),np.log(1e5),n)); z=rng.uniform(3,6,n); V=A*z
O2=rng.uniform(8,12,n)*1e-3      # kg/m3 saturation
hyp=rng.uniform(0.3,0.6,n)       # hypolimnion fraction of volume in summer
O2inv=V*hyp*O2                   # kg O2 available below thermocline
frac=rng.uniform(0.08,0.20,n)    # degradable soluble fraction released
bod=rng.uniform(1.0,1.2,n)       # kg O2 per kg organic matter
straw_needed=O2inv/(frac*bod)/1000  # tonnes of dry straw per season to deplete hypolimnetic O2
yield_=rng.uniform(2,5,n)        # t straw/ha historic
ha=straw_needed/yield_
print("hypolimnetic O2 inventory median %.2f t"%(np.median(O2inv)/1000))
print("straw needed to deplete it per season: median %.1f t (5-95%%: %.1f-%.1f) = %.1f ha of hemp"%(np.median(straw_needed),*np.percentile(straw_needed,[5,95]),np.median(ha)))
print("P(needed > 20 ha of hemp, implausible for a village)=%.3f"%np.mean(ha>20))
