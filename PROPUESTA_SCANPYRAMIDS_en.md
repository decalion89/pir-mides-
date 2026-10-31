# Proposal: a decisive muography measurement of Khufu's Big Void from the King's Chamber

**To:** ScanPyramids collaboration — Nagoya University (nuclear emulsions), KEK (scintillator hodoscopes), CEA (Micromegas), HIP Institute, Cairo University Faculty of Engineering
**From:** Proyecto Pirámides (open-source, independent) — https://github.com/decalion89/pir-mides-
**Date:** 31 October 2026 · **Status:** draft for discussion

---

## 1. Summary
We built an open forward model of cosmic-ray muography in the Great Pyramid and validated it against your published results. Using that model, we show four things:

1. **The 2017 data cannot decide the Big Void's shape, and we can explain why.** From the Queen's Chamber, five candidate geometries produce almost the same muon image:
   - a horizontal corridor;
   - a corridor inclined at 26°;
   - a counterweight gallery joined to the relieving chambers;
   - stacked low chambers;
   - a loose-fill zone.
2. **Our independent reanalysis of your published figures agrees.** We digitized the 679 KEK points (Extended Data Fig. 4) and the Nagoya emulsion profiles (Extended Data Fig. 2).
   - Using the simulated Grand Gallery alone, our geometry recovers NE1 at +5.7 m and NE2 at −4.3 m from the Gallery axis. You published +5.8 m and −4.5 m.
   - The void lies on the Gallery axis (±0.3 m), with its centre at ~60–65 m, and a cross-section of ~10–13 m².
   - Its inclination is **not** constrained robustly. The emulsions prefer horizontal or shallow; KEK prefers inclined; and under a single straight corridor the two sets are mutually inconsistent (Δχ² ≈ 70).
3. **A detector of about 1 m² in the King's Chamber, mostly looking north and upward, separates all five hypotheses at ≥5σ in ≤2 months.** We tested this with a joint fit to the Queen's Chamber data and the new data, letting each rival hypothesis move ±3 m and rescale its cross-section ×0.75–1.25, and fitting normalization, gradient and spectral systematics freely. In blind tests with deliberately altered physics, the analysis identifies the true hypothesis in **96–98.5 %** of cases:
   - flux ±10 % and spectral index ±0.05;
   - limestone density 2.35 instead of 2.2 g/cm³;
   - known chambers displaced by 1 m.

   Campbell's Chamber, the top relieving chamber, is even better: about one week of exposure.
4. **What is at stake.** The predicted signature of each hypothesis is registered in advance (see `PREDICCIONES.md`, P1–P8, dated in git). One case would matter far beyond Egyptology: if the void is a **counterweight gallery** serving the granite roof beams (25–80 t), it would be the oldest known large-scale counterweight lifting system. That would predate the earliest attested shaduf (Akkadian seal, about 2200 BCE) by about three centuries.

## 2. What we ask
1. **Access to the full 2017 angular maps** (data and simulation) from the Queen's Chamber detectors. With them we could resolve the KEK–emulsion tension we find in the published figures and refine the predicted exposure times.
2. **Consideration of a measurement from the King's Chamber**, the most accessible decisive position, and, if possible, from **Campbell's Chamber**. Our model suggests:

| Position | Detector | Exposure for ≥5σ between all hypotheses (realistic systematics) |
|---|---|---|
| King's Chamber, NE corner, axis toward (x=7.3, y=17, z=63) m | ~1 m², resolution ≲20 mrad | 2–8 weeks (factor ~4 model uncertainty) |
| Campbell's Chamber (top relieving chamber) | ~1 m² | ~1 week |

3. **A pre-registered decision rule.** We propose fixing the analysis (hypothesis set, nuisance model, decision thresholds) **before** unblinding. Our condition P7 lists what would be required before claiming the counterweight interpretation:
   - ≥5σ against a plain inclined corridor;
   - in-situ open-sky flux calibration;
   - laser-scan geometry with error below 0.5 m;
   - confirmation from a second position.

## 3. What we offer
- **All code, data extraction scripts and results**, openly available, reproducible with a single command and covered by 21 automated tests.
- **Joint analysis support.** We are glad to work with your Geant4 simulations and the Dormion survey geometry, which would replace our approximate (±1–2 m) internal geometry.
- **Transparency about our own errors.** An early version of our reanalysis claimed an 18° inclination at 4–6σ. We traced it to a digitization artefact: the fitted red curve had been read instead of data points in 26 of 396 bins. We withdrew the claim and documented it in `docs/11`.

## 4. Limitations (stated plainly)
- **No full transport simulation.** We model the Reyna spectrum with continuous energy loss and a fitted angular smearing for multiple scattering; there is no Geant4 simulation yet.
- **Approximate internal geometry**, reconstructed from Petrie and Maragioglio & Rinaldi.
- **The reanalysis uses digitized figures**, not raw data.
- **Model significances are correct to within a factor ~2**, judged against your published 13.7σ (QC) and 5.8σ (outside).

## 5. Key references
- Morishima et al., *Nature* 552, 386 (2017), arXiv:1711.01576.
- Procureur et al., *Nat. Commun.* 14, 1144 (2023).
- Reyna, hep-ph/0604145 (2006).
- Repository documents: `docs/08` (decisive experiment), `docs/09` (robustness and blind tests), `docs/11` (reanalysis of the 2017 data), `PREDICCIONES.md`.

*We know that only authorized teams, with permission from Egypt's Supreme Council of Antiquities, can carry out measurements inside the pyramid. This proposal aims to make the decisive measurement as concrete, cheap and well-specified as possible.*
