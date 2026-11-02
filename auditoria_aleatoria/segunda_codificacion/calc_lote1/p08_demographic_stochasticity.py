# Paper 8 (PMC11814278): can pure demographic stochasticity (random births/deaths/individual migration)
# produce the observed village abandonment: 1596->1881 (285 yr) 42.5% (71/167); 1881->1931 (50 yr) 17.1% (24/140)?
# Village populations from the authors' own data (github yair-grinb/Metapopulation-Settlement-Dynamics, Settlement_Data.xlsx).
import numpy as np, pandas as pd, sys
f=sys.argv[1] if len(sys.argv)>1 else '/tmp/claude-0/recod/l1/ext8/repo/Data/Settlement_Data.xlsx'
x=pd.ExcelFile(f)
P1596=x.parse('1596')['Population'].astype(float).values
P1881=x.parse('1881')['Population'].astype(float).values
print("1596 pop: min %d median %d; 1881 pop: min %d median %d"%(P1596.min(),np.median(P1596),P1881.min(),np.median(P1881)))
def pext(N,b,mu,t):
    # linear birth-death, extinction prob of lineage of 1 by t, raised to N
    r=b-mu
    if abs(r)<1e-12: p1=b*t/(1+b*t)
    else: p1=mu*(np.exp(r*t)-1)/(b*np.exp(r*t)-mu)
    return p1**N
rng=np.random.default_rng(8); n=4000
res={'1596':[], '1881':[]}
for i in range(n):
    b=rng.uniform(0.03,0.05)            # crude birth rate per capita (pre-modern)
    r=rng.uniform(-0.005,0.010)         # net growth (region grew 1596-1931)
    m=rng.uniform(0.0,0.02)             # random individual emigration per capita, balanced by immigration elsewhere
    mu=b-r+m; bb=b+m                    # emigration as extra death, immigration as extra birth (keeps r)
    h=rng.uniform(1,6)                  # treat households (not individuals) as independent units -> N/h (generous)
    for key,P,t in (('1596',P1596,285.),('1881',P1881,50.)):
        N=np.maximum(np.round(P/h),1)
        res[key].append(np.mean(pext(N,bb,mu,t)))
for key,obs in (('1596',71/167),('1881',24/140)):
    pred=np.array(res[key]); ratio=obs/np.maximum(pred,1e-12)
    print(f"{key}: observed abandonment {obs:.3f}; predicted by demographic stochasticity median {np.median(pred):.2e} (95th pct {np.percentile(pred,95):.2e}); P(obs/pred>=3)={np.mean(ratio>=3):.3f}")
