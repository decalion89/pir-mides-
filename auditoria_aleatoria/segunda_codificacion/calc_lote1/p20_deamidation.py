# Paper 20 (PMC8032661): are 'more advanced but highly variable / incomplete' deamidation levels in ancient milk proteins
# physically consistent? Solution kinetics (Robinson & Robinson; 37 C, pH 7.4): median Gln half-time 6100 d, Asn 60 d.
import numpy as np
rng=np.random.default_rng(20); n=200000
Ea=rng.uniform(80e3,100e3,n); T=rng.uniform(8,20,n)+273.15
slow=np.exp(Ea/8.314*(1/T-1/310.15))      # slowdown factor vs 37 C
age=np.exp(rng.uniform(np.log(500),np.log(8000),n))
for name,th in (("Gln",6100.),("Asn",60.)):
    thy=th/365.25*slow
    rem=np.exp(-np.log(2)*age/thy)
    print(f"{name}: half-time at burial T median {np.median(thy):.0f} yr; remaining fraction after 500-8000 yr median {np.median(rem):.2e}; P(remaining>0.5)={np.mean(rem>0.5):.3f}")
# => solution kinetics predict near-complete deamidation; observed partial/variable values imply matrix-bound (dry/mineral)
# kinetics orders of magnitude slower -- consistent with the paper's own caveat that rates are not for archaeological conditions.
