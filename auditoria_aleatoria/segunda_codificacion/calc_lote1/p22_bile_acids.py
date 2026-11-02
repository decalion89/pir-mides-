# Paper 22 (PMC7878498): oxo-BA/BA ratios in Pompeii (~1945 yr) matched to modern faeces. Paper also states BAs are less
# stable than oxo-BAs. Differential degradation shifts the ratio by exp(dk*t). Tolerance needed for 'similar' ratios:
import numpy as np
t=1945.
for tol in (1.3,2.0):
    dk=np.log(tol)/t
    print(f"ratio drift <= x{tol}: requires k_BA - k_oxo <= {dk:.1e}/yr, i.e. differential half-life >= {np.log(2)/dk:.0f} yr")
print("No measured degradation rates for BAs/oxo-BAs in soil are given or available in standard sources -> INDETERMINADO")
