# Paper 12 (PMC8639971): can (even exceptional) brown adipose tissue thermogenesis explain Fuegian cold tolerance
# 'without adequate clothing' (air ~0-9 C, wind, rain; canoe life)? Compare extra heat demand vs max BAT output.
import numpy as np
rng=np.random.default_rng(12); n=200000
A=rng.uniform(1.6,1.9,n)                 # body surface m2
Tair=rng.uniform(0,9,n)                  # Ushuaia mean temps rarely >9 C
Tsk=rng.uniform(22,28,n)                 # vasoconstricted mean skin temp
h=rng.uniform(8,20,n)                    # W/m2/K convective+radiative, light wind 1-5 m/s (no immersion)
clothing_factor=rng.uniform(0.6,1.0,n)   # partial cover (guanaco cape, grease) reduces loss
evap=rng.uniform(10,40,n)                # respiratory/evaporative, rain wetting W
loss=A*h*(Tsk-Tair)*clothing_factor+evap
BMR=rng.uniform(80,130,n)                # incl. elevated BMR reported for Alacaluf
deficit=np.maximum(loss-BMR,1)
mBAT=np.exp(rng.uniform(np.log(0.05),np.log(1.0),n))      # kg, generous upper for 'large depots'
pBAT=np.exp(rng.uniform(np.log(10),np.log(300),n))        # W/kg max (human in vivo ~ <50; rodent max ~300-500)
BAT=mBAT*pBAT
ratio=deficit/BAT
print("heat deficit W median %.0f (5-95%%: %.0f-%.0f)"%(np.median(deficit),*np.percentile(deficit,[5,95])))
print("max BAT output W median %.0f (5-95%%: %.0f-%.0f)"%(np.median(BAT),*np.percentile(BAT,[5,95])))
print("ratio deficit/BAT median %.1f; P(ratio>=3)=%.3f; P(ratio>=1)=%.3f"%(np.median(ratio),np.mean(ratio>=3),np.mean(ratio>=1)))
# conservative human-physiology prior: pBAT 10-60 W/kg, mBAT 0.05-0.5 kg
p2=np.exp(rng.uniform(np.log(10),np.log(60),n)); m2=np.exp(rng.uniform(np.log(0.05),np.log(0.5),n))
r2=deficit/(p2*m2); print("human-physiology prior: median ratio %.0f; P(>=3)=%.3f"%(np.median(r2),np.mean(r2>=3)))
