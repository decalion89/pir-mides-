# Paper 3 (PMC7669863): observed solid-liquid interface migration 0.40 um/s at 1200 C (t~1070-1460 s).
# Is this consistent with carbon-diffusion-controlled decarburization? D_C in austenite (Wells: D0~2.3e-5 m2/s, Q~148 kJ/mol),
# D_C in liquid Fe ~ 2e-9..8e-9 m2/s. Diffusion-controlled front: x = 2*lam*sqrt(D t), v = lam*sqrt(D/t); lam ~0.2-1.5.
import numpy as np
rng=np.random.default_rng(3); n=200000
T=rng.uniform(1180,1200,n)+273.15  # nominal 1200C, surface reading uncertain
D0=rng.uniform(1.0e-5,4.0e-5,n); Q=rng.uniform(140e3,155e3,n)
Dg=D0*np.exp(-Q/(8.314*T))
lam=rng.uniform(0.2,1.5,n)
t=rng.uniform(1070,1460,n)
v=lam*np.sqrt(Dg/t)*1e6
obs=0.40
r=obs/v
print("D_C(austenite) median %.2e m2/s"%np.median(Dg))
print("predicted front velocity um/s median %.2f (5-95%%: %.2f-%.2f)"%(np.median(v),*np.percentile(v,[5,95])))
print("ratio obs/pred median %.2f; P(ratio>=3)=%.3f; P(ratio<=1/3)=%.3f"%(np.median(r),np.mean(r>=3),np.mean(r<=1/3)))
# Linearity: over 1070->1460 s a sqrt(t) law changes slope by sqrt(1460/1070)
print("sqrt(t) curvature over window: x ratio %.3f vs linear %.3f -> 4 points cannot discriminate"%(np.sqrt(1460/1070),1460/1070))
print("Eq.(3) 'dL ∝ D t' is dimensionally inconsistent ([m] vs [m^2]); diffusion gives dL ∝ sqrt(D t).")
