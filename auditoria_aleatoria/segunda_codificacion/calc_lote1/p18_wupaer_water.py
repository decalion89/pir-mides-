# Paper 18 (PMC7455698): check WI = 39.94*D13C - 560.36 arithmetic and compare inferred wheat water input with local rain.
import numpy as np
f=lambda D: 39.94*D-560.36
print("WI(15.8)=%.0f mm, WI(19.4)=%.0f mm (paper 71-215); D13C for mean 137 mm = %.2f"%(f(15.8),f(19.4),(137+560.36)/39.94))
# Farquhar D13C from d13C grain with d_air ~ -6.4 permil (pre-industrial)
for dp in (-25.3,-21.8):
    for da in (-6.6,-6.3):
        print(" d13C %.1f, d_air %.1f -> D13C %.2f"%(dp,da,(da-dp)/(1+dp/1000)))
rng=np.random.default_rng(18); n=100000
rain=71.4*rng.uniform(0.2,0.5,n)   # fraction of 71 mm annual falling during grain filling/spring season
WI=rng.uniform(71,215,n)
r=WI/rain
print("ratio inferred water input / seasonal rain: median %.1f; P(>=3)=%.3f -> supplementary water (irrigation or floodplain moisture) required"%(np.median(r),np.mean(r>=3)))
