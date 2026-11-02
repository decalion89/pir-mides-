# Paper 24 (PMC7582844): zeolite + coarse quartz (0.5-2 mm) filter at reservoir ingress purifying drinking water of the
# 58,000 m3 Corriental reservoir, removing microbes 'because of 3-4 A pores'.
import numpy as np
rng=np.random.default_rng(24); n=200000
# (1) size exclusion: bacteria 0.5-2 um vs zeolite micropores 0.3-0.4 nm
print("bacterium/pore size ratio: %.0f-%.0f -> micropores cannot sieve microbes"%(0.5e-6/0.4e-9,2e-6/0.3e-9))
# (2) hydraulic: storm inflow vs filter area. Catchment not given in main text: assume 5-60 ha unpaved; runoff coeff 0.2-0.6,
# design rain intensity 20-80 mm/h. Pathogen-removing (slow-sand / biofilm) loading 0.1-0.4 m/h; even 'rapid' 5-15 m/h.
A=np.exp(rng.uniform(np.log(5e4),np.log(6e5),n)); Cr=rng.uniform(0.2,0.6,n); i=rng.uniform(0.02,0.08,n)
Q=Cr*i*A   # m3/h
slow=rng.uniform(0.1,0.4,n); rapid=rng.uniform(5,15,n)
Af=np.exp(rng.uniform(np.log(5),np.log(100),n))   # plausible ingress filter area behind dry-laid walls, m2
r_slow=(Q/slow)/Af; r_rapid=(Q/rapid)/Af
print("peak inflow m3/h median %.0f (5-95%%: %.0f-%.0f)"%(np.median(Q),*np.percentile(Q,[5,95])))
print("required/available filter area, slow-sand rates: median %.0f; P(>=3)=%.3f"%(np.median(r_slow),np.mean(r_slow>=3)))
print("required/available filter area, rapid rates (no pathogen removal w/o coagulant): median %.1f; P(>=3)=%.3f"%(np.median(r_rapid),np.mean(r_rapid>=3)))
# (3) annual volume filtered through the filter in 1 year at slow-sand rate if bypass is allowed
