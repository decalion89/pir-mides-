# Paper 1 (PMC7545160): can 16S amplicon templates (515F/806R ~291 bp; qPCR 349F/806R ~457 bp)
# survive as relic/extracellular DNA for 24-127 kyr at Toshan (N Iran) burial temperatures?
# Kinetics: Allentoft et al. 2012 (bone): k(13.1C)=5.5e-6 /site/yr, Ea~127 kJ/mol (depurination, Lindahl).
# Generous mineral/dryness protection factor 1-1000 (log-uniform).
import numpy as np
rng=np.random.default_rng(1); n=200000
R=8.314
k13=np.exp(rng.uniform(np.log(2e-6),np.log(1.5e-5),n))     # /site/yr at 13.1 C (CI-ish)
Ea=rng.uniform(100e3,140e3,n)
T=rng.uniform(14,19,n)+273.15   # MAT Gorgan/Toshan ~17 C; buried 1-26 m -> ~MAT
prot=np.exp(rng.uniform(np.log(1),np.log(1000),n))
k=k13*np.exp(-Ea/R*(1/T-1/286.25))/prot
N0=np.exp(rng.uniform(np.log(1e9),np.log(1e10),n))   # initial 16S copies/g in an active topsoil
obs=1.9e7   # max copies/g observed below 7.5 m (paper)
for L,lab in [(291,'amplicon 515F/806R'),(457,'qPCR 349F/806R')]:
    for t in [24e3,127e3]:
        surv=np.exp(-k*L*t)
        need=obs/N0
        ratio=need/np.maximum(surv,1e-300)
        print(f"{lab} t={t/1e3:.0f} kyr: median surviving fraction={np.median(surv):.2e}; "
              f"P(surv < needed {np.median(need):.1e})={np.mean(surv<need):.3f}; P(ratio>=3)={np.mean(ratio>=3):.3f}")
# protection factor needed for surviving fraction >= obs/N0 (no protection baseline)
k0=k13*np.exp(-Ea/R*(1/T-1/286.25))
for L in (291,457):
    for t in (24e3,127e3):
        need=obs/N0
        pf=k0*L*t/(-np.log(need))
        print(f"L={L} t={t/1e3:.0f}kyr: protection factor needed median={np.median(pf):.0f} (5-95%: {np.percentile(pf,5):.0f}-{np.percentile(pf,95):.0f}); unprotected P(fail)={np.mean(np.exp(-k0*L*t)<need):.3f}")
