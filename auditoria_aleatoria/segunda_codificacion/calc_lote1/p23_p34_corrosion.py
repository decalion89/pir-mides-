# Papers 23 (PMC11742038, bronze coins) and 34 (PMC10966001, polyaniline/mild steel): internal arithmetic of Tafel tables and
# physical bound: in quiescent aerated ~3.5% NaCl, corrosion at OCP is cathodically limited by O2 diffusion i_lim = 4 F D C / delta.
import numpy as np
F=96485.
def sg(ba,bc,i): return ba*bc/(2.303*(ba+bc)*i)
def cr(i_uA,EW,rho): return 3.27e-3*i_uA*EW/rho
print("== Paper 23 (bronze, EW~32.5, rho~8.8) ==")
t23=[('BD',.148,.172,5.82e-4,59.2,6.76,None),('P',.244,.229,3.19e-4,160.5,3.72,44.9),('S1',.161,.131,2.16e-4,145.1,3.34,50.6),
     ('S2',.113,.151,1.03e-4,272.4,2.39,64.6),('S3',.167,.313,9.97e-6,6921,0.15,97.7)]
i0=5.82e-4; cr0=6.76
for s,ba,bc,i,rp,c,e in t23:
    print(f"{s}: Rp(Stern-Geary)={sg(ba,bc,i):.0f} vs {rp}; CR(from icorr)={cr(i*1e6,32.5,8.8):.2f} vs {c}; "
          f"E%(Eq.1 icorr)={(1-i/i0)*100:.1f} vs {e}; E%(from CR)={(1-c/cr0)*100:.1f}")
print("== Paper 34 (mild steel, EW 27.92, rho 7.87) ==")
t34=[('blank',.617,1.00,5.871e-4,249,5.34,None),('10',.529,.275,0.962e-4,521,2.23,58.23),('25',.425,.254,0.953e-4,579,1.84,65.54),
     ('50',.311,.201,0.812e-5,826,0.97,81.83),('100',.213,.182,0.786e-5,899,0.23,95.69)]
i0=5.871e-4; cr0=5.34
for s,ba,bc,i,rp,c,e in t34:
    print(f"{s} ppm: Rp(SG)={sg(ba,bc,i):.0f} vs {rp}; CR(icorr)={cr(i*1e6,27.92,7.87):.3f} vs {c}; E%(icorr)={(1-i/i0)*100:.1f} vs {e}; E%(CR)={(1-c/cr0)*100:.1f}")
print("EIS Rp (Table 5): 23-198 ohm cm2 vs Tafel Rp 249-899; EIS IE 84.7-98.4% vs PDP 58.2-95.7%")
rng=np.random.default_rng(23); n=200000
D=rng.uniform(1.8e-9,2.4e-9,n); C=rng.uniform(0.18,0.24,n)   # mol/m3 O2, air-saturated 3.5% NaCl 20-25 C
delta=np.exp(rng.uniform(np.log(1e-4),np.log(5e-4),n))        # m, quiescent cell diffusion layer 0.1-0.5 mm
ilim=4*F*D*C/delta*1e2   # uA/cm2 (A/m2 *100)
print("O2 limiting current uA/cm2 median %.0f (5-95%%: %.0f-%.0f)"%(np.median(ilim),*np.percentile(ilim,[5,95])))
for lab,i in (("P23 BD",582),("P23 P",319),("P23 S1",216),("P34 blank mild steel",587.1)):
    r=i/ilim; print(f"  {lab}: icorr {i} uA/cm2 -> ratio icorr/i_lim median {np.median(r):.1f}; P(>=3)={np.mean(r>=3):.3f}")
