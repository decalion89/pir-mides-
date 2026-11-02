# Paper 10 (PMC8160351): 6 mm and 10 mm metallic inclusions explained by 'supersaturation of the colloidal metal-glass
# system' -> agglomeration. Compare (A) Brownian (colloidal) coagulation growth time with (B) gravitational settling of
# coarse scraps, against a secondary-furnace melt time of hours to ~2 days.
import numpy as np
rng=np.random.default_rng(10); n=200000
kB=1.380649e-23
T=rng.uniform(1000,1150,n)+273.15
eta=np.exp(rng.uniform(np.log(30),np.log(3000),n))   # Pa s, Roman soda-lime glass ~1000-1150 C
phi=np.exp(rng.uniform(np.log(1e-3),np.log(3e-2),n))   # metal volume fraction (0.1-3 vol%, overdose)
r0=np.exp(rng.uniform(np.log(5e-9),np.log(5e-7),n))    # colloidal particle radius 5-500 nm
R=rng.uniform(3e-3,5e-3,n)                              # final radius 3-5 mm
tmelt=np.exp(rng.uniform(np.log(3*3600),np.log(48*3600),n))
# Smoluchowski Brownian coagulation, constant kernel K=8kT/(3eta): mean volume grows as v/v0 = 1 + K n0 t/2
K=8*kB*T/(3*eta); n0=phi/(4/3*np.pi*r0**3)
t_need=( (R/r0)**3 - 1)*2/(K*n0)
ratioA=t_need/tmelt
print("A) Brownian coagulation to mm size: t_needed median %.1e yr; ratio t_needed/t_melt median %.1e; P(>=3)=%.3f"%(np.median(t_need)/3.15e7,np.median(ratioA),np.mean(ratioA>=3)))
# Even total metal in reach: a 10 mm sphere needs metal from volume Vs/phi
print("   glass volume to source one 10 mm sphere by colloid: median %.0f cm3"%(np.median((4/3*np.pi*(5e-3)**3)/phi)*1e6))
# B) Stokes settling of coarse scrap (radius 0.1-1 mm) through ~10-30 cm crucible melt
a=np.exp(rng.uniform(np.log(1e-4),np.log(1e-3),n)); drho=rng.uniform(6000,6800,n); H=rng.uniform(0.1,0.3,n)
v=2/9*drho*9.81*a**2/eta; tB=H/v
ratioB=tB/tmelt
print("B) Stokes settling of 0.1-1 mm scraps: time median %.1f h; P(t_settle<=t_melt)=%.3f"%(np.median(tB)/3600,np.mean(ratioB<=1)))
