# Paper 2 (PMC10167333): reproduce Table 2 "Modern C (%)" and test the paper's claim that modern C
# is 0.46-2.36 % of the TOC pool, using the paper's own Eq. 1 and Table 1 values.
import numpy as np
# sample: (TOC wt% Table1 [UO], TOC Table2 [UCI], D14C permil, reported ModernC %)
d={'Lakim0':(0.302,1/3.80,-943.5,1.70),'Lakim25':(0.116,1/11.21,-865.4,1.56),'Lakim50':(0.128,1/7.07,-921.1,1.00),
   'Lakim75':(0.251,1/4.23,-945.8,1.36),'Lakim100':(0.132,1/30.86,-820.7,2.36),'Luca22':(0.014,1/71.43,-770.3,0.32),
   'TC0':(0.170,1/5.87,-972.2,0.47),'TC25':(0.196,1/6.80,-971.8,0.55),'TC50':(0.261,1/4.35,-976.6,0.61),'TC100':(0.115,1/11.82,-938.5,0.71)}
print("sample  f_mod(0permil)%  f_mod(600permil)%  100*TOC1*f  reported  ratio f/reported")
rat=[]
for s,(t1,t2,D,rep) in d.items():
    f0=(D+1000)/1000; f600=(D+1000)/1600
    print(f"{s:9s} {100*f0:6.2f} {100*f600:6.2f} {100*t1*f0:6.2f} {rep:5.2f} {100*f0/rep:5.1f}")
    rat.append(100*f0/rep)
rat=np.array(rat); print("ratio range (0 permil endmember):",rat.min().round(1),rat.max().round(1),"all>=3:",np.all(rat>=3))
# => reported 'Modern C (%)' = 100 x TOC(wt%) x f, i.e. modern C in units of 0.01 wt% of ROCK, not % of TOC.
# Monte Carlo over endmembers: modern endmember 0..+600 permil, old endmember -1000..-990 permil
rng=np.random.default_rng(2); n=100000
Dm=rng.uniform(0,600,n); Do=rng.uniform(-1000,-990,n)
fr=[]
for s,(t1,t2,D,rep) in d.items():
    f=(D-Do)/(Dm-Do); fr.append(100*f/rep)
fr=np.array(fr)
print("MC: per-sample P(true % of TOC / reported >=3):",np.round((fr>=3).mean(axis=1),3))
print("MC: P(all 10 samples ratio>=3)=",np.mean(np.all(fr>=3,axis=0)).round(3), " median ratio per sample",np.round(np.median(fr,axis=1),1))
# Delivery check: modern-C stock in 1 m of outcrop and DOC infiltration time
rho=rng.uniform(1.8e3,2.4e3,n)  # kg/m3 bulk
fm=np.array([ (D+1000)/1000*t1/100 for (t1,t2,D,rep) in d.values()])  # mass fraction of rock that is modern C
stock=rho*rng.choice(fm,n)*1.0   # kg C per m2 of face, 1 m deep
P=rng.uniform(0.25,0.35,n); finf=np.exp(rng.uniform(np.log(0.02),np.log(0.3),n))
DOC=np.exp(rng.uniform(np.log(1e-3),np.log(20e-3),n)) # kg/m3 (1-20 mg/L)
ret=rng.uniform(0.1,0.8,n)
flux=P*finf*DOC*ret   # kg C /m2/yr
tyr=stock/flux
print("modern-C stock kg/m2 median",np.median(stock).round(3),"; years of DOC infiltration needed median %.0f (5-95%%: %.0f-%.0f)"%(np.median(tyr),*np.percentile(tyr,[5,95])))
print("P(time needed > 300 yr, i.e. inconsistent with a ~0 permil 'modern' endmember)=",np.mean(tyr>300).round(3))
# Same-endmember comparison: reported = 100*TOC*f, correct = 100*f  -> error factor = 1/TOC(wt%), endmember-independent
print("error factor 1/TOC(wt%, Table 1):",{s:round(1/t1,1) for s,(t1,t2,D,rep) in d.items()})
