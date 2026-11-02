# Paper 5 (PMC11109126): can a Ms6.2/Mw5.9 event like the 2023 Jishishan quake trigger liquefaction-mudflow at Lajia (~4 km from JERH)?
# (a) magnitude-distance bound for liquefaction, Ambraseys (1988): Mw = 4.64 + 2.65e-3*Re + 0.99*log10(Re) (Re epicentral km)
import numpy as np
from scipy.optimize import brentq
for Mw in (5.6,5.9,6.2):
    Re=brentq(lambda R: 4.64+2.65e-3*R+0.99*np.log10(R)-Mw,0.1,1000)
    print(f"Mw {Mw}: max epicentral distance for liquefaction ~{Re:.0f} km")
# Lajia lies ~4-10 km from the 2023 rupture/JERH area -> within bound (feasible IF soils saturated).
# (b) saturation: liquefaction needs saturated loose sand/silt. Paper: saturated layer ~14 m below terrace, surface frozen
# irrigated fields; it names winter irrigation as 'the culprit'. Mobilized volume 2023: source 604,900 m3, deposit 675,000 m3 over 181,800 m2
print("2023 mean deposit thickness %.1f m"%(675000/181800))
# Without irrigation-raised water table (dry loess, deep water table near Yellow River terrace ~ river level 20-60 m below 2nd terrace?)
# liquefaction susceptibility collapses: Youd&Perkins / CRR requires Sr~1; we flag the assumption rather than compute CRR (no SPT/CPT data given).
